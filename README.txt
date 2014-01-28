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

example::

    [warmup]
    enabled = False

