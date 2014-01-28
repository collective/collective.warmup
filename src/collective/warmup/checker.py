from datetime import datetime

from urllib2 import URLError

import time
import re
import logging
import ConfigParser as configparser
import UserDict
import urllib2

logging.basicConfig()

logger = logging.getLogger('Collective Warmup')
logger.setLevel(logging.INFO)

FAILED = '\033[91mFAILED\033[0m'
OK = '\033[92mOK\033[0m'


class Checker(UserDict.DictMixin):

    urls = None
    sleep = 10

    def __init__(self, config_file):
        self.parser = configparser.ConfigParser({
            'enabled': 'True'
        })
        self.parser.read(config_file)
        self._data = {}
        self.enabled = self.parser.getboolean('warmup', 'enabled')

        if not self.enabled:
            logger.warning('Warmup script has been disabled')

    def _check(self, section):
        options = self.get(section)
        check_exists = options.get('check_exists')
        if check_exists:
            check_exists = [i for i in check_exists.splitlines() if i]
        check_not_exists = options.get('check_not_exists')
        if check_not_exists:
            check_not_exists = [i for i in check_not_exists.splitlines() if i]

        self._probing(
            options['url'],
            2,
            check_exists,
            check_not_exists
        )

    def _probing(self, url, max_attempts=10,
                 check_exists=None,
                 check_not_exists=None):
        i = 0
        start = datetime.now()
        check = True
        while True:
            try:
                output = urllib2.urlopen(url).read()
                elapsed = datetime.now() - start

                if check_exists and not \
                        [x for x in check_exists if x in output]:
                    import pdb; pdb.set_trace( )
                    check = False

                if check_not_exists and \
                        [x for x in check_not_exists if x in output]:
                    import pdb; pdb.set_trace( )
                    check = False

                if check:
                    logger.info('Warmup: {0} [ {1} sec. ] [ {2} ]'.format(
                        url,
                        elapsed.seconds,
                        OK)
                    )
                    return output
            except URLError:
                logger.erro('Warmup: {0} [ {1} sec. ] [ {2} ]'.format(
                    url,
                    elapsed.seconds,
                    FAILED)
                )

            time.sleep(self.sleep)
            if i >= max_attempts:
                elapsed = datetime.now() - start
                logger.info('Warmup: {0} [ {1} sec. ] [ {2} ]'.format(
                    url,
                    elapsed.seconds,
                    FAILED)
                )
                break
            i += 1

    def execute(self):
        # logger.info('execute {}'.format(configuration))

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
            try:
                self._raw[section] = dict(self.parser.items(section))
            except:
                import pdb; pdb.set_trace( )

        if not self.urls:
            logger.error('No urls specified')
        else:
            for section in self.urls:
                if not section:
                    continue

                if section not in self._raw:
                    logger.error("Section {0} doesn't exist".format(section))
                    continue

                self._check(section)

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

    # def __setitem__(self, option, value):
    #     if not isinstance(value, str):
    #         raise TypeError('Option values must be strings', value)
    #     self._data[option] = value

    # def __delitem__(self, key):
    #     if key in self._raw:
    #         del self._raw[key]
    #         if key in self._data:
    #             del self._data[key]
    #         if key in self._cooked:
    #             del self._cooked[key]
    #     elif key in self._data:
    #         del self._data[key]
    #     else:
    #         raise KeyError(key)

    def keys(self):
        raw = self._raw
        return list(self._raw) + [k for k in self._data if k not in raw]

    # def copy(self):
    #     result = self._raw.copy()
    #     result.update(self._cooked)
    #     result.update(self._data)
    #     return result
