Introduction
============



Based on https://gist.github.com/gforcada/7040082

Installation
============

this package should be installed by zc.buildout::

    [buildout]
    ...
    parts =
       ...
       warmup


    [instance]
    ...
    eggs +=
       collective.warmup


    [warmup]
    recipe = zc.recipe.egg:scripts
    eggs = collective.warmup
    arguments = '${buildout:directory}/warump.ini'


Configuration file
==================

warmup.ini example::

    [warmup]
    enabled = True
    sleep = 2

    urls =
        home


    [config]
    base_url = http://localhost:8081


    [home]
    url = ${config:base_url}/Plone/front-page
    max_attempts = ${config:max_attempts}
    check_exists =
        http://localhost:8081/Plone/@@security-controlpanel
    check_not_exists =
        http://not.exists
    follow_links = True
    ignore_middle =
        @@
        ++theme++
        #
        /front-page/
        ?
    ignore_end =
        .css
        .js
        .png
        .jpg
        .jpeg
        .gif
