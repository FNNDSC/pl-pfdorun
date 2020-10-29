pl-pfdorun
================================

.. image:: https://travis-ci.org/FNNDSC/pfdorun.svg?branch=master
    :target: https://travis-ci.org/FNNDSC/pfdorun

.. image:: https://img.shields.io/badge/python-3.8%2B-blue.svg
    :target: https://github.com/FNNDSC/pl-pfdorun/blob/master/setup.py

.. contents:: Table of Contents


Abstract
--------

The pf-pfdorun plugin is a general purpose "swiss army" knife DS plugin that can be used to execute some CLI type commands on input directories.


Description
-----------

The pf-pfdorun plugin is a general purpose "swiss army" knife type plugin that can be used to fill the space of needing to run/exec CLI type commands on input directores/data. For instance

    * Create explicit (g)zip files of data
    * Un(g)zip data
    * Reorganize data in the input dir in some idiosyncratic
      fashion in the ouput director

In some respects it functions as a dynamic "impedence matching" plugin that can be used to per-usecase match the output directories and files of one plugin to the input requirements of another.

Usage
-----

.. code::

    [python] pfdorun
        [-h|--help]
        [--json] [--man] [--meta]
        [--savejson <DIR>]
        [-v|--verbosity <level>]
        [--version]
        <inputDir> <outputDir>


Arguments
~~~~~~~~~

.. code::

    [-h] [--help]
    If specified, show help message and exit.

    [--json]
    If specified, show json representation of app and exit.

    [--man]
    If specified, print (this) man page and exit.

    [--meta]
    If specified, print plugin meta data and exit.

    [--savejson <DIR>]
    If specified, save json representation file to DIR and exit.

    [-v <level>] [--verbosity <level>]
    Verbosity level for app. Not used currently.

    [--version]
    If specified, print version number and exit.


Getting inline help is:

.. code:: bash

    docker run --rm fnndsc/pl-pfdorun pfdorun --man

Run
~~~

You need you need to specify input and output directories using the `-v` flag to `docker run`.


.. code:: bash

    docker run --rm -u $(id -u)                             \
        -v $(pwd)/in:/incoming -v $(pwd)/out:/outgoing      \
        fnndsc/pl-pfdorun pfdorun                           \
        /incoming /outgoing


Development
-----------

Build the Docker container:

.. code:: bash

    docker build -t local/pl-pfdorun .


Python dependencies can be added to ``setup.py``.
After a successful build, track which dependencies you have installed by
generating the `requirements.txt` file.

.. code:: bash

    docker run --rm local/pl-pfdorun -m pip freeze > requirements.txt


For the sake of reproducible builds, be sure that ``requirements.txt`` is up to date before you publish your code.


.. code:: bash

    git add requirements.txt && git commit -m "Bump requirements.txt" && git push


Examples
--------

Put some examples here!


.. image:: https://raw.githubusercontent.com/FNNDSC/cookiecutter-chrisapp/master/doc/assets/badge/light.png
    :target: https://chrisstore.co
