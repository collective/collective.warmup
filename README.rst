Introduction
============

collective.warmup has been created to warm up web application's caches upon
start and restart.

It works by reading a configuration file containing a list of urls that
are then invoked.

collective.warmup is inspired by Gil Forcada's `warmup_plone.py`_ script.


Why not a simple bash script?
-----------------------------

While the basic use case is very simple,
collective.warmup offers the following extra features:

* Verifies the correctness of the response body (e.g. contains a certain string)
* Can operate in *crawl mode*,
  following links in pages to warm up all related pages
* Can filter out certain urls according to a general definition


Installation
============

collective.warmup can be installed in two ways:

* As a normal python package via pip
* Inside a `buildout`_, with optional integration with `Plone`_

Dependencies
------------

* `lxml`_


Manual installation
-------------------

To install it (using `virtualenv`_, on a GNU/Debian machine)::

    $ sudo apt-get install build-essential python-dev python-lxml python-virtualenv libxml2-dev libxslt1-dev
    $ virtualenv warmup && cd warmup && souce bin/activate
    (warmup) $ pip install collective.warmup

and launch it with::

    (warmup) $ bin/warmup <path/file.ini>


Alternative installation with buildout
--------------------------------------

To integrate collective.warmup in a `buildout`_ with `Plone`_,
add this to your configuration::

    [buildout]
    ...
    parts =
        ...
        warmup


    [instance]
    ...
    eggs +=
        collective.warmup


    [instance]
    environment-vars +=
        WARMUP_BIN ${buildout:directory}/bin/warmup
        WARMUP_INI ${buildout:directory}/warmup.ini
        WARMUP_HEALTH_THRESHOLD 50000


    [warmup]
    recipe = zc.recipe.egg:scripts
    eggs = collective.warmup


After executing the buildout you will find the warmup script
in the ``bin`` directory.

In this example, the script will be executed automatically
by the `Zope`_ instance each time it is started.


Configuration file
------------------

This is a sample ``warmup.ini`` configuration::

    [warmup]
    enabled = True
    sleep = 2
    base_url = http://localhost
    logfile = /path/to/warmup.log

    urls =
        Home page


    [config]
    max_attempts = 2
    base_path = mysite


    [Home page]
    path = ${config:base_path}/
    max_attempts = ${config:max_attempts}
    check_exists =
        Welcome
    check_not_exists =
        p0wned by
    follow_links = True
    ignore_middle =
        @@
        ++theme++
        #
        ?
    ignore_end =
        .css
        .js
        .png
        .jpg
        .jpeg
        .gif
        .xml
        RSS
        .ico


Options
-------

Global [warmup]
###############

enable : ``True`` or ``False``
    If ``False``, the script will do nothing when invoked.

sleep : integer
    The number of seconds the script waits between url retrievals.
    Defaults to ``2``.

base_url : a valid URL (**don't forget the protocol!**)
    The base URL to check
    (all paths in the various URL sections are relative to this URL).

log_file : a filesystem path
    The file where the logs will be written.

urls : a list of sections (separated by newline)
    The URLs that we want to check.
    Each URL must have its own section in the configuration file (see below)
    and we reference these sections here (do not put real URLs here!).
    It also set an order for the checks (which are executed sequentially).


URL section
###########

max_attempts : integer
    The maximum number of attempts to check the url.
    Defaults to ``2``

path : the path to check
    The path will be added to the ``base_url`` parameter in order to retrieve
    the page url

check_exists : list of strings
    A list of strings that must be present in the page

check_not_exists : list of strings
    A list of strings that must not be present in the page

follow_links : ``True`` or ``False``
    If ``True`` the script will follow the links in the page and will
    perform the same checks for each link.

ignore_middle : list of strings
    If ``follow_links`` is ``True``, the links containing one of these strings
    will be ignored

ignore_end : list of strings
    If ``follow_links`` is ``True``, the links ending with one of these strings
    will be ignored


Health check
------------
In order not to mark backend healthy too early by the load-balancer, before proper
warmup, this package defines a browser view called ``@@health.check`` which can be
used within your load-balancer probe mechanism. See bellow a Varnish configuration
example::

    backend instance_1 {
        .host = "localhost";
        .port = "8081";
        .probe = {
             .url = "/health.check";
             .interval = 5s;
             .timeout = 1s;
             .window = 5;
             .threshold = 3;
         }
    }

This way Varnish will mark the Zope instance backend healthy when
ZODB cache-size is bigger than ``WARMUP_HEALTH_THRESHOLD``. If you do not define
the ``WARMUP_HEALTH_THRESHOLD`` environment variable, the Zope instance backend
will be marked healthy as soon as Zope will be able to handle requests.


Credits
-------

.. image:: http://www.abstract.it/logo-abstract-readme
   :alt: Abstract Website
   :target: http://abstract-technology.com/



.. _virtualenv: http://www.virtualenv.org/en/latest/
.. _Plone: http://plone.org
.. _warmup_plone.py: https://gist.github.com/gforcada/7040082
.. _buildout: http://www.buildout.org
.. _Zope: http://zope.org
.. _lxml: http://pypi.python.org/pypi/lxml
