Referecence
===========

Based on https://gist.github.com/gforcada/7040082

Introduction
============

collective.warmup warmups the plone instance cache upon start and restart with that simple operations:

* Verify the existence of a specific content in the page
* Verify the correct response of a URL in the page

On every operation is possible to set a filter to exclude objects to be verified

HowTo
=====

There are two type of installation for the warmup script: Manual or Automatic with Buildout

Manual Installation in virtualenv on debian/ubuntu
--------------------------------------------------

::

    >_ sudo apt-ge install build-essential python-dev python-lxml python-virtualenv libxml2-dev libxslt1-dev
    >_ virtualenv warmup
    >_ cd warmup
    warmup >_ souce bin/activate
    (warmup) warmup >_ git clone https://github.com/collective/collective.warmup.git
    (warmup) warmup >_ cd collective.warmup
    (warmup) warmup >_ python setup.py install


Console script syntax execution:

::

    $ bin/warmup <path/file.ini> -p <instance_port>

Automatic installation with Buildout
------------------------------------

Put in buildout.cfg these parameters:

::

    [buildout]
    ...
    parts =
        ...
        warmup


    [instance]
    ...
    eggs +=
        collective.warmup

    [sources]
    ...
    collective.warmup = git https://github.com/collective/collective.warmup.git

    [instance]
    environment-vars +=
        WARMUP_BIN ${buildout:directory}/bin/warmup
        WARMUP_INI ${buildout:directory}/warmup.ini

    [warmup]
    recipe = zc.recipe.egg:scripts
    eggs = collective.warmup

Execute ``bin/buildout -N`` to obtain the warmup script in the buildout **bin** folder

Configure the *.ini file
------------------------

This is a sample *.ini syntax configuration::

    [warmup]
    enabled = True
    sleep = 2
    base_url = http://localhost
    logfile = /home/zope/instances/plone/buildout/var/log/warmup.log

    urls =
        Home page

    [config]
    max_attempts = 2
    base_path = simplemanagement

    [Home page]
    path = ${config:base_path}/
    max_attempts = ${config:max_attempts}
    check_exists =
        Welcome
    check_not_exists =
        http://not.exists
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

General section [warmup]
########################

::

    enable: True/False

Enable or Disable script execution

::

    sleep: 2

Set a pause timeout in seconds between instance interrogations

::

    base_url: http://localhost

Set the base URL to check **Note is important to specify the protocol ex. http:// or https://**

::

    logfile = /home/zope/instances/plone/buildout/var/log/warmup.log

Set the log file **Note insert the absolute path of the file**

::

    urls =
        Home page

With this option we should insert a list of section of webpages to check

Page Section
############

::

    max_attempts = 2

Set the maximum number of attempts of checks

::

    path = plone

Set the plonesite base path

::

    check_exists =
        Welcome

Set a list of terms or URL that MUST be present in the page

::

    check_not_exists =
        http://not.exists

Set a list of terms or URL that MUST NOT be present in the page

::

    follow_links = True/False

Enable or Disable the follow links checks

::

    ignore_middle =
        @@
        ++theme++
        #
        ?

Set a list of IGNORE URL with that parameter in the middle of the string

::

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

Set a list of IGNORE URL with that parameter in the end of the string

Log File
========

This is the warmup log messages::

    Positive Result after the scrip execution with follow_links = True

    2014-04-04 14:27:51,319 INFO Section Home page
    2014-04-04 14:27:51,425 INFO http://localhost/plone/ [ 0 sec. ] [ OK ]
    2014-04-04 14:27:51,428 INFO 4 links found on the http://localhost/plone/.
    2014-04-04 14:27:51,516 INFO http://localhost/plone/login [ 0 sec. ] [ OK ]
    2014-04-04 14:27:51,590 INFO http://localhost/plone/sitemap [ 0 sec. ] [ OK ]
    2014-04-04 14:27:51,668 INFO http://localhost/plone/accessibility-info [ 0 sec. ] [ OK ]
    2014-04-04 14:27:51,740 INFO http://localhost/plone/contact-info [ 0 sec. ] [ OK ]

    Positive Result after the scrip execution with follow_links = False

    2014-04-04 14:43:22,561 INFO Section Home page
    2014-04-04 14:43:26,766 INFO http://localhost/plone/ [ 4 sec. ] [ OK ]
    2014-04-04 14:43:26,766 WARNING Warmup Done

    Negative Result after the scrip execution

    2014-04-04 14:52:23,422 INFO Section Home page
    2014-04-04 14:52:27,624 INFO http://localhost/plone/ [ 4 sec. ] [ FAILED ]
    2014-04-04 14:52:27,624 WARNING Warmup Done

Credits
-------

.. image:: http://www.abstract.it/logo-abstract-readme?a
   :alt: Abstract Website
   :target: http://www.abstract.it
