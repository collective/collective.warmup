import ConfigParser as configparser
from datetime import datetime
import logging
import lxml.html
import re
import time
import UserDict
import urllib2
import tempfile


FAILED = 'FAILED'
OK = 'OK'


class Checker(UserDict.DictMixin):
    """It reads the configuration file and extracts
    all the parts that have to be parsed.

    For all section defined in urls variable it try to
    retrieve a specific url and check some the output
    """
    urls = None
    sleep = 2

    def __init__(self, config_file, port):
        self.parser = configparser.ConfigParser({
            'enabled': 'True'
        })
        self.parser.read(config_file)
        self._data = {}
        self.enabled = self.parser.getboolean('warmup', 'enabled')
        self.port = port
        self.base_url = self.parser.get('warmup', 'base_url')

        # setup logger
        try:
            logfile = self.parser.get('warmup', 'logfile')
        except configparser.NoOptionError:
            logfile = 'warmup.log'

        # Check for write permissions to logfile
        try:
            with open(logfile, 'a') as ofile:
                ofile.write('--')
        except Exception:
            logfile = tempfile.mktemp(prefix='warmup.', suffix='.log')

        logging.basicConfig(
            filename=logfile,
            level=logging.INFO,
            format='%(asctime)s %(levelname)s %(message)s'
        )
        self.logger = logging.getLogger('Collective Warmup')

        if not self.enabled:
            self.logger.warning('Script has been disabled')

    def _get_url(self, path):
        if not path.startswith('/'):
            path = '/%s' % path

        if self.port != 80:
            url = '%s:%s%s' % (
                self.base_url,
                self.port,
                path
            )
        else:
            url = '%s%s' % (
                self.base_url,
                path
            )
        return url

    def _get_links(self, page, ignore_middle, ignore_end):
        tree = lxml.html.fromstring(page)
        links = []
        url = self._get_url('')
        for link in tree.iterlinks():
            link = link[2]
            ignore = False
            if not link.startswith(url):
                continue
            if link == url:
                continue
            for middle in ignore_middle:
                if not ignore and middle in link:
                    ignore = True
            if ignore:
                continue
            for end in ignore_end:
                if not ignore and link.endswith(end):
                    ignore = True
            if ignore:
                continue
            if link not in links:
                links.append(link)
        return links

    def _warmup(self, section):
        options = self.get(section)

        self.logger.info('Section %s' % section)

        def _get_option_array(name):
            value = options.get(name, '')
            return [i for i in value.splitlines() if i]

        check_exists = _get_option_array('check_exists')
        check_not_exists = _get_option_array('check_not_exists')

        max_attempts = options.get('max_attempts', 2)
        if isinstance(max_attempts, str):
            max_attempts = int(max_attempts)

        url = self._get_url(options['path'])
        page = self._probing(
            url,
            max_attempts,
            check_exists,
            check_not_exists
        )
        ignore_middle = _get_option_array('ignore_middle')
        ignore_end = _get_option_array('ignore_end')

        if page and options.get('follow_links', 'false').lower() == 'true':
            links = self._get_links(
                page,
                ignore_middle, ignore_end
            )
            self.logger.info(
                '%d links found on the %s.' % (
                    len(links), url
                )
            )
            for link in links:
                self._probing(
                    link,
                    max_attempts,
                    None,  # don't check the html output
                    None   # for the links found
                )

    def _probing(self, url, max_attempts=5,
                 check_exists=None,
                 check_not_exists=None):
        i = 1
        start = datetime.now()
        check = True
        while True:
            try:
                output = urllib2.urlopen(url).read()
                elapsed = datetime.now() - start

                # check that specific text in html output exists
                if check_exists and not \
                        [x for x in check_exists if x in output]:
                    check = False

                # check that specific text in html output doesn't exist
                if check_not_exists and \
                        [x for x in check_not_exists if x in output]:
                    check = False

                if check:
                    self.logger.info('%s [ %d sec. ] [ %s ]' % (
                        url,
                        elapsed.seconds,
                        OK)
                    )
                    return output
            except urllib2.URLError:
                self.logger.error('%s - Attempt %d' % (url, i))

            time.sleep(self.sleep)
            if i >= max_attempts:
                elapsed = datetime.now() - start
                self.logger.info('%s [ %d sec. ] [ %s ]' % (
                    url,
                    elapsed.seconds,
                    FAILED)
                )
                break
            i += 1

    def execute(self):
        try:
            self.sleep = self.parser.getint('warmup', 'sleep')
        except configparser.NoOptionError:
            pass

        self.urls = None
        try:
            urls = self.parser.get('warmup', 'urls')
            self.urls = urls.splitlines()
        except configparser.NoOptionError:
            pass

        self._raw = {}
        for section in self.parser.sections():
            self._raw[section] = dict(self.parser.items(section))

        if not self.urls:
            self.logger.error('No urls specified')
        else:
            for section in self.urls:
                if not section:
                    continue

                if section not in self._raw:
                    self.logger.error(
                        "Section %s doesn't exist" % section
                    )
                    continue

                self._warmup(section)

            self.logger.warning("Warmup Done")

    def __getitem__(self, section):
        try:
            return self._data[section]
        except KeyError:
            pass

        options = Options(self, section, self._raw[section])
        self._data[section] = options
        options._substitute()
        return options


class Options(UserDict.DictMixin):
    """Based on collective.transmogrifier code

    It extracts some options from a dictionary and performs text
    substitutions when a snippet like this is found
    ${<part>:<variable>}
    """
    def __init__(self, checker, section, data):
        self.checker = checker
        self.section = section
        self._raw = data
        self._cooked = {}
        self._data = {}

    def _substitute(self):
        for key, value in self._raw.items():
            if '${' in value:
                self._cooked[key] = self._sub(value, [(self.section, key)])

    def get(self, option, default=None, seen=None):
        try:
            return self._data[option]
        except KeyError:
            pass

        value = self._cooked.get(option)
        if value is None:
            value = self._raw.get(option)
            if value is None:
                return default

        if '${' in value:
            key = self.section, option
            if seen is None:
                seen = [key]
            elif key in seen:
                raise ValueError('Circular reference in substitutions.')
            else:
                seen.append(key)

            value = self._sub(value, seen)
            seen.pop()

        self._data[option] = value
        return value

    _template_split = re.compile('([$]{[^}]*})').split
    _valid = re.compile('\${[-a-zA-Z0-9 ._]+:[-a-zA-Z0-9 ._]+}$').match
    _tales = re.compile('^\s*string:', re.MULTILINE).match

    def _sub(self, template, seen):
        parts = self._template_split(template)
        subs = []
        for ref in parts[1::2]:
            if not self._valid(ref):
                 # A value with a string: TALES expression?
                if self._tales(template):
                    subs.append(ref)
                    continue
                raise ValueError('Not a valid substitution %s.' % ref)

            names = tuple(ref[2:-1].split(':'))
            value = self.checker[names[0]].get(names[1], None, seen)
            if value is None:
                raise KeyError('Referenced option does not exist:', *names)
            subs.append(value)
        subs.append('')

        return ''.join([''.join(v) for v in zip(parts[::2], subs)])

    def __getitem__(self, key):
        try:
            return self._data[key]
        except KeyError:
            pass

        v = self.get(key)
        if v is None:
            raise KeyError('Missing option: %s:%s' % (self.section, key))
        return v

    def keys(self):
        raw = self._raw
        return list(self._raw) + [k for k in self._data if k not in raw]
