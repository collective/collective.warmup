Introduction
============

Based on https://gist.github.com/gforcada/7040082


Installation
============

This package should be installed by zc.buildout::

    [buildout]
    ...
    parts =
       ...
       warmup


    [instance]
    ...
    eggs +=
       collective.warmup
    environment-vars =
        WARMUP_BIN ${buildout:directory}/bin/warmup


    [warmup]
    recipe = zc.recipe.egg:scripts
    eggs = collective.warmup
    arguments = '${buildout:directory}/warmup.ini'


Configuration file
==================

warmup.ini example::

    [warmup]
    enabled = True
    sleep = 2
    plone_instance = Plone
    host = localhost
    logfile = /path/to/warmup.log

    urls =
        Home page


    [config]
    max_attempts = 2


    [Home page]
    path = /
    max_attempts = ${config:max_attempts}
    check_exists =
        Welcome to Plone
        /Plone/@@security-controlpanel
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
