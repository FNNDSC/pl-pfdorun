#!/usr/bin/env python
#
# pfdorun: ChRIS DS plugin app
#
# (c) 2016-2020 Fetal-Neonatal Neuroimaging & Developmental Science Center
#                   Boston Children's Hospital
#
#              http://childrenshospital.org/FNNDSC/
#                        dev@babyMRI.org
#


import  os
import  importlib.metadata
import  pfdo

from chrisapp.base import ChrisApp

Gstr_description = '''
        The pf-pfdorun plugin is a general purpose "swiss army" knife type
        plugin that can be used to fill the space of needing to run/exec
        CLI type commands on input directores/data. For instance:

            * Create explicit (g)zip files of data
            * Un(g)zip data
            * Reorganize data in the input dir in some idiosyncratic
            fashion in the ouput directory

        In some respects it functions as a dynamic "impedence matching" plugin
        that can be used to per-usecase match the output directories and files
        of one plugin to the input requirements of another.
'''

Gstr_title = """

       _               __    _
      | |             / _|  | |
 _ __ | |______ _ __ | |_ __| | ___  _ __ _   _ _ __
| '_ \| |______| '_ \|  _/ _` |/ _ \| '__| | | | '_ \
| |_) | |      | |_) | || (_| | (_) | |  | |_| | | | |
| .__/|_|      | .__/|_| \__,_|\___/|_|   \__,_|_| |_|
| |            | |
|_|            |_|



"""

Gstr_synopsis = """

    NAME

       pfdorun.py

    SYNOPSIS

        [python] pfdorun                                                \\
            [-h] [--help]                                               \\
            [--json]                                                    \\
            [--man]                                                     \\
            [--meta]                                                    \\
            [--savejson <DIR>]                                          \\
            [-v <level>] [--verbosity <level>]                          \\
            [--version]                                                 \\
            <inputDir>                                                  \\
            <outputDir>

    BRIEF EXAMPLE

        * Bare bones execution

            docker run --rm -u $(id -u)                                 \\
                -v $(pwd)/in:/incoming -v $(pwd)/out:/outgoing          \\
                fnndsc/pl-pfdorun pfdorun                               \\
                /incoming /outgoing

    DESCRIPTION

        %s

    ARGS

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
""" % Gstr_description


class Pfdorun(ChrisApp):
    DESCRIPTION             = Gstr_description
    AUTHORS                 = 'Rudolph Pienaar <dev@babyMRI.org>'
    SELFPATH                = '/usr/local/bin'
    SELFEXEC                = 'pfdorun'
    EXECSHELL               = 'python'
    TITLE                   = 'pf-pfdorun: run some CLI on input directories.'
    CATEGORY                = 'Utility'
    TYPE                    = 'ds'
    DOCUMENTATION           = 'http://wiki'
    VERSION                 = importlib.metadata.version(__package__)
    ICON                    = '' # url of an icon image
    LICENSE                 = 'Opensource (MIT)'
    MAX_NUMBER_OF_WORKERS   = 1  # Override with integer value
    MIN_NUMBER_OF_WORKERS   = 1  # Override with integer value
    MAX_CPU_LIMIT           = '' # Override with millicore value as string, e.g. '2000m'
    MIN_CPU_LIMIT           = '' # Override with millicore value as string, e.g. '2000m'
    MAX_MEMORY_LIMIT        = '' # Override with string, e.g. '1Gi', '2000Mi'
    MIN_MEMORY_LIMIT        = '' # Override with string, e.g. '1Gi', '2000Mi'
    MIN_GPU_LIMIT           = 0  # Override with the minimum number of GPUs, as an integer, for your plugin
    MAX_GPU_LIMIT           = 0  # Override with the maximum number of GPUs, as an integer, for your plugin

    # Use this dictionary structure to provide key-value output descriptive information
    # that may be useful for the next downstream plugin. For example:
    #
    # {
    #   "finalOutputFile":  "final/file.out",
    #   "viewer":           "genericTextViewer",
    # }
    #
    # The above dictionary is saved when plugin is called with a ``--saveoutputmeta``
    # flag. Note also that all file paths are relative to the system specified
    # output directory.
    OUTPUT_META_DICT = {}

    def define_parameters(self):
        """
        Define the CLI arguments accepted by this plugin app.
        Use self.add_argument to specify a new app argument.
        """

    def run(self, options):
        """
        Define the code to be run by this plugin app.
        """
        print(Gstr_title)
        print('Version: %s' % self.get_version())

    def show_man_page(self):
        """
        Print the app's man page.
        """
        print(Gstr_synopsis)
