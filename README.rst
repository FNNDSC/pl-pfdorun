pl-pfdorun
================================

.. image:: https://travis-ci.org/FNNDSC/pfdorun.svg?branch=master
    :target: https://travis-ci.org/FNNDSC/pfdorun

.. image:: https://img.shields.io/badge/python-3.8%2B-blue.svg
    :target: https://github.com/FNNDSC/pl-pfdorun/blob/master/setup.py

.. contents:: Table of Contents


Abstract
--------

The pl-pfdorun plugin is a general purpose "swiss army" knife DS plugin that can be used to execute some CLI type commands on input directories.


Description
-----------


The pl-pfdorun plugin is a general purpose "swiss army" knife type plugin that can be used to perform somewhat arbitrary exec command line type commands on input directores/data. For instance:

* copy (subsets of) data from the input space to output;
* create explicit (g)zip files of data;
* un(g)zip data;
* reorganize data in the input dir in some idiosyncratic
  fashion in the ouput directory;
* misc operations on images using imagemagick;
* and others..

In some  respects  it functions as a  dynamic "impedance  matching" plugin that can be used to per-usecase match the output directories and files of one plugin to the input requirements of another. This plugin is for the most a simple wrapper around an underlying pfdo_run CLI exec module.

Usage
-----

.. code::

        pfdorun                                                         \
            --exec <CLIcmdToExec>                                       \
            [-i|--inputFile <inputFile>]                                \
            [-f|--fileFilter <filter1,filter2,...>]                     \
            [-d|--dirFilter <filter1,filter2,...>]                      \
            [--analyzeFileIndex <someIndex>]                            \
            [--outputLeafDir <outputLeafDirFormat>]                     \
            [--threads <numThreads>]                                    \
            [--noJobLogging]                                            \
            [--test]                                                    \
            [--maxdepth <dirDepth>]                                     \
            [--syslog]                                                  \
            [-h] [--help]                                               \
            [--json]                                                    \
            [--man]                                                     \
            [--meta]                                                    \
            [--savejson <DIR>]                                          \
            [--verbose <level>]                                         \
            [--version]                                                 \
            <inputDir>                                                  \
            <outputDir>


Arguments
~~~~~~~~~

.. code:: html

        --exec <CLIcmdToExec>
        The command line expression to apply at each directory node of the
        input tree. See the CLI SPECIFICATION section for more information.

        [-i|--inputFile <inputFile>]
        An optional <inputFile> specified relative to the <inputDir>. If
        specified, then do not perform a directory walk, but function only
        on the directory containing this file.

        [-f|--fileFilter <someFilter1,someFilter2,...>]
        An optional comma-delimated string to filter out files of interest
        from the <inputDir> tree. Each token in the expression is applied in
        turn over the space of files in a directory location, and only files
        that contain this token string in their filename are preserved

        [-d|--dirFilter <someFilter1,someFilter2,...>]
        An additional filter that will further limit any files to process to
        only those files that exist in leaf directory nodes that have some
        substring of each of the comma separated <someFilter> in their
        directory name.

        [--analyzeFileIndex <someIndex>]
        An optional string to control which file(s) in a specific directory
        to which the analysis is applied. The default is "-1" which implies
        *ALL* files in a given directory. Other valid <someIndex> are:

            'm':   only the "middle" file in the returned file list
            "f":   only the first file in the returned file list
            "l":   only the last file in the returned file list
            "<N>": the file at index N in the file list. If this index
                   is out of bounds, no analysis is performed.

            "-1":  all files.

        [--outputLeafDir <outputLeafDirFormat>]
        If specified, will apply the <outputLeafDirFormat> to the output
        directories containing data. This is useful to blanket describe
        final output directories with some descriptive text, such as
        'anon' or 'preview'.

        This is a formatting spec, so

            --outputLeafDir 'preview-%%s'

        where %%s is the original leaf directory node, will prefix each
        final directory containing output with the text 'preview-' which
        can be useful in describing some features of the output set.

        [--maxdepth <dirDepth>]
        The maximum depth to descend relative to the <inputDir>. Note, that
        this counts from zero! Default of '-1' implies transverse the entire
        directory tree.

        [--syslog]
        If specified, prepend output 'log' messages in syslog style.

        [--threads <numThreads>]
        If specified, break the innermost analysis loop into <numThreads>
        threads.

        [--noJobLogging]
        If specified, then suppress the logging of per-job output. Usually
        each job that is run will have, in the output directory, three
        additional files:

                %inputWorkingFile-returncode
                %inputWorkingFile-stderr
                %inputWorkingFile-stdout

        By specifying this option, the above files are not recorded.

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

        [--verbose <level>]
        Verbosity level for app.

        [--version]
        If specified, print version number and exit.

Getting inline help:
~~~~~~~~~~~~~~~~~~~~

.. code:: bash

    docker run --rm fnndsc/pl-pfdorun pfdorun --man

CLI Specification
~~~~~~~~~~~~~~~~~

Any text in the CLI prefixed with a percent char ``%`` is interpreted in one of two ways.

First, any CLI to the ``pfdo_run`` itself can be accessed via ``%``. Thus, for example a ``%outputDir`` in the ``--exec`` string will be expanded to the ``outputDir`` of the ``pfdo_run``.

Secondly, three internal '%' variables are available:

* ``%inputWorkingDir``  - the current input tree working directory
* ``%outputWorkingDir`` - the current output tree working directory
* ``%inputWorkingFile`` - the current file being processed

These internal variables allow for contextual specification of values. For example, a simple CLI touch command could be specified as

.. code::

    --exec "touch %outputWorkingDir/%inputWorkingFile"

or a command to convert an input ``png`` to an output ``jpg`` using the ImageMagick ``convert`` utility

.. code::

    --exec "convert %inputWorkingDir/%inputWorkingFile
                    %outputWorkingDir/%inputWorkingFile.jpg"

Special Functions
~~~~~~~~~~~~~~~~~

Furthermore, ``pfdo_run`` offers the ability to apply some interal functions to a tag. The template for specifying a function to apply is:

.. code::

    %_<functionName>[|arg1|arg2|...]_<tag>

thus, a function is identified by a function name that is prefixed and suffixed by an underscore and appears in front of the tag to process.

Possible args to the <functionName> are separated by pipe "|" characters. For example a string snippet that contains

.. code::

    %_strrepl|.|-_inputWorkingFile.txt

will replace all occurences of ``.`` in the ``%inputWorkingFile`` with ``-``. Also of interest, the trailing ``.txt`` is preserved in the final pattern for the result.

The following functions are available:

.. code::

    %_md5[|<len>]_<tagName>

    Apply an ``md5`` hash to the value referenced by <tagName> and optionally
    return only the first <len> characters.

.. code::

    %_strmsk|<mask>_<tagName>

    Apply a simple mask pattern to the value referenced by ``<tagName>``.
    Chars that are ``*`` in the mask are passed through unchanged. The mask
    and its target should be the same length.

.. code::

    %_strrepl|<target>|<replace>_<tagName>

    Replace the string <target> with <replace> in the value referenced
    by <tagName>.

.. code::

    %_rmext_<tagName>

    Remove the "extension" of the value referenced by <tagName>. This of course
    only makes sense if the <tagName> denotes something with an extension!

.. code::

    %_name_<tag>

    Replace the value referenced by <tag> with a name generated by the faker
    module.

Functions cannot currently be nested.

Run
~~~

You need you need to specify input and output directories using the ``-v`` flag to ``docker run``.


.. code:: bash

    docker run --rm -u $(id -u) -ti                                         \
      -v $(pwd)/in:/in -v $(pwd)/out:/out                                   \
      -v $(pwd)/pfdorun:/usr/local/lib/python3.8/dist-packages/pfdorun:     \
      fnndsc/pl-pfdorun pfdorun                                             \
      /in /out


Development
-----------

Build the Docker container:

.. code:: bash

    docker build -t local/pl-pfdorun .


Python dependencies can be added to ``setup.py``. After a successful build, track which dependencies you have installed by generating the `requirements.txt` file.

.. code:: bash

    docker run --rm local/pl-pfdorun -m pip freeze > requirements.txt


For the sake of reproducible builds, be sure that ``requirements.txt`` is up to date before you publish your code.


.. code:: bash

    git add requirements.txt && git commit -m "Bump requirements.txt" && git push


Examples
--------

Copy files from the input dir to the output:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: bash

            docker run --rm -u $(id -u)                                 \
                -v $(pwd)/in:/incoming -v $(pwd)/out:/outgoing          \
                fnndsc/pl-pfdorun pfdorun                               \
                --exec "cp %inputWorkingDir/%inputWorkingFile
                           %outputWorkingDir/%inputWorkingFile"         \
                --threads 0 --printElapsedTime                          \
                --verbose 5                                             \
                /incoming /outgoing

Tar gzip up the input dir:
~~~~~~~~~~~~~~~~~~~~~~~~~~

Assume the ``inputDir`` has a file, ``input.json``. We use that file as a tag to search in order to process the whole directory tree:

.. code:: bash

    docker run -ti --rm -u $(id -u)                                         \
        -v /home/rudolphpienaar/data/convert_test:/incoming                 \
        -v $(pwd)/out:/outgoing                                             \
        fnndsc/pl-pfdorun                                                   \
        pfdorun --inputFile input.json                                      \
                --exec "tar cvfz %outputDir/out.tgz %inputDir"              \
                --threads 0                                                 \
                --printElapsedTime                                          \
                --verbose 5                                                 \
                /incoming /outgoing


Unpack a tarball that is in the input dir tree:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Assume the ``inputDir`` has a file ending in ``tgz`` somewhere in the tree we wish to unpack:

.. code:: bash

    docker run -ti --rm -u $(id -u)                                         \
        -v /home/rudolphpienaar/data/convert_test:/incoming                 \
        -v $(pwd)/out:/outgoing                                             \
        fnndsc/pl-pfdorun                                                   \
        pfdorun --filterExpression tgz                                      \
                --exec "tar xvfz %inputWorkingDir/%inputWorkingFile -C %outputDir"  \
                --threads 0                                                 \
                --printElapsedTime                                          \
                --verbose 5                                                 \
                /incoming /outgoing

Copy only a single target file from the input space using a dir filter
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Assume that the ``inputDir`` has many nested directories. One of them, ``100307`` contains a single file, ``brain.mgz``. We wish to only copy this single file to the ``outputDir``:

.. code:: bash

    docker run -ti --rm -u $(id -u)                                         \
        -v $(pwd)/in:/incoming                                              \
        -v $(pwd)/out:/outgoing                                             \
        fnndsc/pl-pfdorun                                                   \
        pfdorun --fileFilter " " --dirFilter 100307                         \
                --exec "cp %inputWorkingDir/brain.mgz
                %outputWorkingDir/brain.mgz"                                \
                --noJobLogging                                              \
                --threads 0                                                 \
                --printElapsedTime                                          \
                --verbose 5                                                 \
                /incoming /outgoing


Debug
-----

To debug the containerized version of this plugin, simply volume map the source directories of the repo into the relevant locations of the container image:

.. code:: bash

    docker run -ti --rm -v $PWD/in:/incoming:ro -v $PWD/out:/outgoing:rw    \
        -v $PWD/pfdorun:/usr/local/lib/python3.9/site-packages/pfdorun:ro   \
        fnndsc/pl-pfdorun pfdorun /incoming /outgoing

To enter the container:

.. code:: bash

    docker run -ti --rm -v $PWD/in:/incoming:ro -v $PWD/out:/outgoing:rw    \
        -v $PWD/pfdorun:/usr/local/lib/python3.9/site-packages/pfdorun:ro   \
        --entrypoint /bin/bash fnndsc/pl-pfdorun

Remember to use the ``-ti`` flag for interactivity!


*30*

.. image:: https://raw.githubusercontent.com/FNNDSC/cookiecutter-chrisapp/master/doc/assets/badge/light.png
    :target: https://chrisstore.co
