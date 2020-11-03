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
import  pfdo_run
import  pudb

from chrisapp.base import ChrisApp

Gstr_description = '''

        The pf-pfdorun plugin is a general purpose "swiss army" knife type
        plugin that can be used to perform somewhat arbitrary exec command
        line type commands on input directores/data. For instance:

            * copy (subsets of) data from the input space to output
            * Create explicit (g)zip files of data
            * Un(g)zip data
            * Reorganize data in the input dir in some idiosyncratic
              fashion in the ouput directory

        In some  respects  it functions as a  dynamic "impedence  matching"
        plugin that can be used to per-usecase match the output directories
        and files of one plugin to the input requirements of another.

        This plugin is for the most a simple wrapper around an underlying
        pfdo_run module.
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

       pfdorun # DS plugin

    SYNOPSIS

        [python] pfdorun                                                \\
            --exec <CLIcmdToExec>                                       \\
            [-i|--inputFile <inputFile>]                                \\
            [-f|--filterExpression <someFilter>]                        \\
            [--analyzeFileIndex <someIndex>]                            \\
            [--outputLeafDir <outputLeafDirFormat>]                     \\
            [--threads <numThreads>]                                    \\
            [--noJobLogging]                                            \\
            [--test]                                                    \\
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
                --exec "copy %inputWorkingDir/%inputWorkingFile
                             %outputWorkingDir/%inputWorkingFile"       \\
                --threads 0 --printElapsedTime                          \\
                --verbose 5                                             \\
                /incoming /outgoing

    DESCRIPTION
        {desc}

    ARGS

        --exec <CLIcmdToExec>
        The command line expression to apply at each directory node of the
        input tree. See the CLI SPECIFICATION section for more information.

        [-i|--inputFile <inputFile>]
        An optional <inputFile> specified relative to the <inputDir>. If
        specified, then do not perform a directory walk, but convert only
        this file.

        [-f|--filterExpression <someFilter>]
        An optional string to filter the files of interest from the
        <inputDir> tree.

        [--analyzeFileIndex <someIndex>]
        An optional string to control which file(s) in a specific directory
        to which the analysis is applied. The default is "-1" which implies
        *ALL* files in a given directory. Other valid <someIndex> are:

            'm':   only the "middle" file in the returned file list
            "f":   only the first file in the returned file list
            "l":   only the last file in the returned file list
            "<N>": the file at index N in the file list. If this index
                   is out of bounds, no analysis is performed.

            "-1" means all files.

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

        [-v <level>] [--verbosity <level>]
        Verbosity level for app. Not used currently.

        [--version]
        If specified, print version number and exit.

    CLI SPECIFICATION

    Any text in the CLI prefixed with a percent char '%' is interpreted in one
    of two ways.

    First, any CLI to the ``pfdo_run`` itself can be accessed via '%'. Thus,
    for example a ``%outputDir`` in the ``--exec`` string will be expanded
    to the ``outputDir`` of the ``pfdo_run``.

    Secondly, three internal '%' variables are available:

        * '%inputWorkingDir'  - the current input tree working directory
        * '%outputWorkingDir' - the current output tree working directory
        * '%inputWorkingFile' - the current file being processed

    These internal variables allow for contextual specification of values. For
    example, a simple CLI touch command could be specified as

        --exec "touch %outputWorkingDir/%inputWorkingFile"

    or a command to convert an input ``png`` to an output ``jpg`` using the
    ImageMagick ``convert`` utility

        --exec "convert %inputWorkingDir/%inputWorkingFile
                        %outputWorkingDir/%inputWorkingFile.jpg"

    SPECIAL FUNCTIONS

    Furthermore, `pfdo_run` offers the ability to apply some interal functions
    to a tag. The template for specifying a function to apply is:

        %_<functionName>[|arg1|arg2|...]_<tag>

    thus, a function is identified by a function name that is prefixed and
    suffixed by an underscore and appears in front of the tag to process.
    Possible args to the <functionName> are separated by pipe "|" characters.

    For example a string snippet that contains

        %_strrepl|.|-_inputWorkingFile.txt

    will replace all occurences of '.' in the %inputWorkingFile with '-'.
    Also of interest, the trailing ".txt" is preserved in the final pattern
    for the result.

    The following functions are available:

        %_md5[|<len>]_<tagName>
        Apply an 'md5' hash to the value referenced by <tagName> and optionally
        return only the first <len> characters.

        %_strmsk|<mask>_<tagName>
        Apply a simple mask pattern to the value referenced by <tagName>. Chars
        that are "*" in the mask are passed through unchanged. The mask and its
        target should be the same length.

        %_strrepl|<target>|<replace>_<tagName>
        Replace the string <target> with <replace> in the value referenced by
        <tagName>.

        %_rmext_<tagName>
        Remove the "extension" of the value referenced by <tagName>. This
        of course only makes sense if the <tagName> denotes something with
        an extension!

        %_name_<tag>
        Replace the value referenced by <tag> with a name generated by the
        faker module.

    Functions cannot currently be nested.



""".format(desc = Gstr_description)


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
        self.add_argument("-i", "--inputFile",
                            help        = "input file",
                            dest        = 'inputFile',
                            type        = str,
                            optional    = True,
                            default     = '')
        self.add_argument("-e", "--exec",
                            type        = str,
                            optional    = True,
                            help        = "command line execution string to perform",
                            dest        = 'exec',
                            default     = '')
        self.add_argument("--filterExpression",
                            type        = str,
                            optional    = True,
                            help        = "string file filter",
                            dest        = 'filter',
                            default     = '')
        self.add_argument("--analyzeFileIndex",
                            type        = str,
                            optional    = True,
                            help        = "file index per directory to analyze",
                            dest        = 'analyzeFileIndex',
                            default     = '-1')
        self.add_argument("--printElapsedTime",
                            type        = bool,
                            optional    = True,
                            help        = "print program run time",
                            dest        = 'printElapsedTime',
                            action      = 'store_true',
                            default     = False)
        self.add_argument("--threads",
                            type        = str,
                            optional    = True,
                            help        = "number of threads for innermost loop processing",
                            dest        = 'threads',
                            default     = "0")
        self.add_argument("--outputLeafDir",
                            type        = str,
                            optional    = True,
                            help        = "formatting spec for output leaf directory",
                            dest        = 'outputLeafDir',
                            default     = "")
        self.add_argument("--test",
                            type        = bool,
                            optional    = True,
                            help        = "test",
                            dest        = 'test',
                            action      = 'store_true',
                            default     = False)
        self.add_argument("--noJobLogging",
                            type        = bool,
                            optional    = True,
                            help        = "Turn off per-job logging to file system",
                            dest        = 'noJobLogging',
                            action      = 'store_true',
                            default     = False)
        self.add_argument("-y", "--synopsis",
                            type        = bool,
                            optional    = True,
                            help        = "short synopsis",
                            dest        = 'synopsis',
                            action      = 'store_true',
                            default     = False)
        self.add_argument("--overwrite",
                            type        = str,
                            optional    = True,
                            help        = "overwrite files if already existing",
                            dest        = 'overwrite',
                            action      = 'store_true',
                            default = False)
        self.add_argument("--followLinks",
                            type        = bool,
                            optional    = True,
                            help        = "follow symbolic links",
                            dest        = 'followLinks',
                            action      = 'store_true',
                            default     = False)
        self.add_argument("--verbose",
                            type        = str,
                            optional    = True,
                            help        = "verbosity level for app",
                            dest        = 'verbose',
                            default     = "1")

    def run(self, options):
        """
        Define the code to be run by this plugin app.
        """
        # pudb.set_trace()
        print(Gstr_title)
        print('Version: %s' % self.get_version())

        # Some "helper" re-assignments
        options.str_desc    = Gstr_synopsis
        options.verbosity   = options.verbose
        options.inputDir    = options.inputdir
        options.outputDir   = options.outputdir

        # The main module instantiation
        pf_do_shell         = pfdo_run.pfdo_run(vars(options))

        # And now run it!
        d_pfdo_shell        = pf_do_shell.run(timerStart = True)

        if options.printElapsedTime:
            pf_do_shell.dp.qprint(
                    "Elapsed time = %f seconds" %
                    d_pfdo_shell['runTime']
            )

    def show_man_page(self):
        """
        Print the app's man page.
        """
        print(Gstr_synopsis)
