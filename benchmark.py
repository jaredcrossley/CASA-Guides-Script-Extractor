import os
import sys
import shutil
import time
from optparse import OptionParser
import socket
import tarfile

#import non-standard Python modules
import extractCASAscript

#-should make the calibrationURL and imagingURL behavior reflect the fact that
# extractCASAscript.py can take local Python files there too
#  -this may require some reqorking of the object's attributes and the execution
#   method
#  -maybe change have a switch for __init__ that differentiates between a guide
#   and just a Python file to be benchmarked
#  -I think the best option would actually to remove the specifics of calibration
#   and imaging from the benchmark class
#    -make it literally a class for benchmarking scripts
#    -externally you deal with the calibration or imaging script and possibly the
#     process of extracting them from some webpage but the benchmark class just
#     deals with the directory structure and logging of a Python script run
#     inside CASA
#-all methods should probably return something
#-need to deal with how to keep extractCASAscript.py current with the tasklist
# and potentially changing parameters or functionality
#-figure out previous run stuff and about deleting them if that makes sense
#-if I split up the runGuideScript into separate calibration and imaging methods
# then I should think about making CASAglobals an input parameter to them so that
# I potentially wouldn't need to do the .pop stuff to clear out accreted
# variables

class benchmark:
    """A class for the execution of a single CASA guide
    on a single machine for benchmark testing and timing.

    Attributes
    ----------

    CASAglobals : dict
        Dictionary returned by Python globals() function within the CASA
        namespace (environment). Simply pass the return value of the globals()
        function from within CASA where this class should be instantiated
        within.

    workDir : str
        Absolute path to directory where benchmarking directory structure will
        be created, all data will be stored and processing will be done.

    calibrationURL : str
        URL to CASA guide calibration webpage.

    imagingURL : str
        URL to CASA guide imaging webpage.

    outString : str
        Container string that stores operations that do not automatically log
        themselves. Primarily for things like acquiring and extracting the
        data which are not wrapped up in a separate module.

    dataPath : str
        URL or absolute path to raw CASA guide data and calibration tables.

    outFile : str
        Log file for operations done outside of other wrapper modules such as
        acquiring and extracting the raw data. This is where the outString is
        saved at the end of execution.

    skipDownload : bool
        Switch to skip downloading the raw data from the web.

    previousDir (is this needed with the directory structure I'm using?): str
        Absolute path to directory of a previous benchmarking execution. This
        will be the previous run workDir path.

    localTar : str
        Absolute path to raw data .tgz file associated with CASA guide.

    extractLog : str
        Absolute path to CASA guide script extractor output.

    calScript : str
        Absolute path to Python file containing the calibration portion of the
        CASA guide being run through the benchmark.

    calScriptLog : str
        Absolute path to calibration script output.

    imageScript : str
        Absolute path to Python file containing the imaging portion of the CASA
        guide being run through the benchmark.

    calScriptExpect : str
        Absolute path to CASA guide script extractor output of expected
        calibraton task calls.

    imageScriptExpect : str
        Absolute path to CASA guide script extractor output of expected
        imaging task calls.

    imageScriptLog : str
        Absolute path to imaging script output.

    calBenchOutFile : str
        Absolute path to the log file containing the complete record of
        benchmarking output associated with running the calibration script.

    calBenchSumm : str
        Absolute path to the log file containing a summary of the calibration
        benchmark timing. Includes the total benchmark runtime, total task
        runtimes broken down by task and average task runtimes.

    imageBenchOutFile : str
        Absolute path to the log file containing the complete record of
        benchmarking output associated with running the imaging script.

    imageBenchSumm : str
        Absolute path to the log file containing a summary of the imaging
        benchmark timing. Includes the total benchmark runtime, total task
        runtimes broken down by task and average task runtimes.

    currentWorkDir : str
        Absolute path to the directory associated with the current benchmark
        instance. This includes the actual reduction, log file and raw data
        tar file directories. It is made inside workDir and named as
        YYYY_MMM_DDTHH_MM_SS-hostname.

    currentLogDir : str
        Absolute path to the directory containing the log files associated with
        the current benchmark instance.

    currentTarDir : str
        Absolute path to the directory containing the raw data .tgz files
        associated with the current benchmark instance.

    currentRedDir : str
        Absolute path to the directory where the calibration and/or imaging
        scripts are actually executed.

    allLogDir : str
        Absolute path to the directory where the most pertinent log files
        associated with each individual benchmark instance run within workDir
        are stored.

    Methods
    -------

    __init__
        Initializes benchmark instance attributes.

    createDirTree
        Creates current benchmark instance directory structure.

    removePreviousRun
        Deletes directory associated with a previous benchmark instance.

    downloadData
        Uses wget to download raw data from the web.

    extractData
        Unpacks the raw data .tgz file.

    makeExtractOpts (this should be private, if I keep it at all)
        Returns OptionParser.parse_args options variable for extractCASAscript.

    runScriptExtractor (this should probably be split into cal, imaging and .py)
        Calls extractCASAscript.main to create CASA guide Python scripts.

    runGuideScript (should also have switch for cal, imaging and .py files)
        Executes extracted CASA guide Python files.

    writeOutFile
        Writes outString to a text file.
    """
    def __init__(self, CASAglobals=None, scriptDir='', workDir='./', \
                 calibrationURL='', imagingURL='', dataPath='', outFile='', \
                 skipDownload=False):
        #for telling where printed messages originate from
        fullFuncName = __name__ + '::__init__'
        indent = len(fullFuncName) + 2

        #check that we have CASA globals
        if not CASAglobals:
            raise ValueError('Value returned by globals() function in ' + \
                             'CASA environment must be given.')
        self.CASAglobals = CASAglobals

        #add script directory to Python path if need be
        if scriptDir == '':
            raise ValueError('Path to benchmarking scripts must be given.')
        scriptDir = os.path.abspath(scriptDir) + '/'
        if scriptDir not in sys.path:
            sys.path.append(scriptDir)

        #initialize the working directory
        if not os.path.isdir(workDir):
            raise ValueError("Working directory '" + workDir + "' " + \
                             'does not exist.')
        if workDir == './': workDir = os.getcwd()
        if workDir[-1] != '/': workDir += '/'
        if workDir[0] != '/':
            raise ValueError('Working directory must be specified as an ' + \
                             'absolute path.')
        self.workDir = workDir

        #check other necessary parameters were specified
        if calibrationURL == '':
            raise ValueError('URL to calibration CASA guide must be given.')
        self.calibrationURL = calibrationURL
        if imagingURL == '':
            raise ValueError('URL to imaging CASA guide must be given.')
        self.imagingURL = imagingURL
        if dataPath == '':
            raise ValueError('A URL or path must be given pointing to the ' + \
                             'raw data.')
        self.dataPath = dataPath
        if outFile == '':
            raise ValueError('A file must be specified for the output ' + \
                             'of the script.')

        #check that the tarball does exist if not downloading it
        self.skipDownload = skipDownload
        if self.skipDownload == True:
            if not os.path.isfile(self.dataPath):
                raise ValueError('Cannot find local tarball for extraction ' + \
                                 'at ' + self.dataPath + '. ' + \
                                 'Download may be required.')
            print fullFuncName + ':', 'Data available by filesystem.'
            self.localTar = self.dataPath
        #check dataPath is a URL if we will be downloading data instead
        else:
            self.localTar = ''
            if self.dataPath[0:4] != 'http':
                raise ValueError("'" + self.dataPath + "' is not a valid " + \
                                 'URL for downloading the data.')

        #check current directory for previous run
        prevDir = self.dataPath.split('/')[-1].split('.tgz')[0]
        if os.path.isdir(prevDir):
            self.previousDir = os.path.abspath(prevDir)
        else:
            self.previousDir = ''

        #initialize the current benchmark instance directories and files
        self.currentWorkDir = self.workDir + \
                              time.strftime('%Y_%m_%dT%H_%M_%S') + '-' + \
                              socket.gethostname() + '/'
        self.currentLogDir = self.currentWorkDir + 'log_files/'
        self.outFile = self.currentLogDir + outFile
        self.currentTarDir = self.currentWorkDir + 'tarballs/'
        self.currentRedDir = ''
        self.allLogDir = self.workDir + 'all_logs/'
        self.outString = ''
        self.extractLog = self.currentLogDir + 'extractCASAscript.py.log'

        #strings that can be filled out by later methods
        self.calScript = ''
        self.calScriptLog = ''
        self.imageScript = ''
        self.imageScriptLog = ''
        self.calBenchOutFile = ''
        self.imageBenchOutFile = ''
        self.calBenchSumm = ''
        self.imageBenchSumm = ''


    def createDirTree(self):
        """ Creates the directory structure associated with this benchmark.

        Returns
        -------
        None

        Notes
        -----
        This creates currentWorkDir, currentLogDir, currentTarDir if the raw
        data will be downloaded and allLogDir for workDir if it has not been
        created already. Those directories are structured as:
            |-- currentWorkDir/
            |   |-- currentTarDir/
            |   |-- currentLogDir/
            |-- allLogDir/
        """
        #for telling where printed messages originate from
        fullFuncName = __name__ + '::createDirTree'
        indent = len(fullFuncName) + 2

        #check if directories already exist
        if os.path.isdir(self.currentWorkDir) or \
           os.path.isdir(self.currentLogDir) or \
           os.path.isdir(self.currentTarDir):
            print fullFuncName + ':', 'Current benchmark directories ' + \
                  'already exist. Skipping directory creation.'
            return

        #make directories for current benchmark instance
        os.mkdir(self.currentWorkDir)
        os.mkdir(self.currentLogDir)
        if not self.skipDownload:
            os.mkdir(self.currentTarDir)

        #check if all_logs directory needs to be made
        if not os.path.isdir(self.allLogDir):
            os.mkdir(self.allLogDir)


    def removePreviousRun(self):
        """ Removes directory tree associated with a previous benchmark.

        Returns
        -------
        None

        Notes
        -----
        This deletes the directory at the path stored in previousDir. It should
        be platform independent as it used shutil.rmtree (or at least as
        platform independent as that method is).
        """
        #for telling where printed messages originate from
        fullFuncName = __name__ + '::removePreviousRun'
        indent = len(fullFuncName) + 2

        if self.previousDir != '':
            print fullFuncName + ':', 'Removing preexisting data.'
            shutil.rmtree(self.previousDir)
        else:
            print fullFuncName + ':', 'No previous run to remove.'


    def downloadData(self):
        """ Downloads raw data .tgz file from the web.

        Returns
        -------
        None

        Notes
        -----
        This downloads the raw data .tgz file associated with the CASA guide
        from the web (dataPath) into currentTarDir using wget. Here os.system
        is used to execute wget so it is not perfectly platform independent
        but should be find across Linux and Mac. The wget options used are:
        
          wget -q --no-check-certificate --directory-prefix=currentTarDir
        """
        #for telling where printed messages originate from
        fullFuncName = __name__ + '::downloadData'
        indent = len(fullFuncName) + 2

        command = 'wget -q --no-check-certificate --directory-prefix=' + \
                  self.currentTarDir + ' ' + self.dataPath

        #wget the data
        print fullFuncName + ':', 'Acquiring data by HTTP.\n' + ' '*indent + \
              'Logging to', self.outFile + '.'
        self.outString += time.strftime('%a %b %d %H:%M:%S %Z %Y') + '\n'
        self.outString += 'Timing command:\n' + command + '\n'
        procT = time.clock()
        wallT = time.time()
        os.system(command)
        wallT = round(time.time() - wallT, 2)
        procT = round(time.clock() - procT, 2)
        self.outString += str(wallT) + 'wall ' + str(procT) + 'CPU\n\n'
        self.localTar = self.currentTarDir+ self.dataPath.split('/')[-1]


    def extractData(self):
        """ Unpacks the raw data .tgz file into the current benchmark directory.

        Returns
        -------
        None

        Notes
        -----
        This unpacks the raw data .tgz file in localTar and times the process.
        It uses the tarfile module so it should be platform independent (or at
        least as platform independent as this module is). The unpacked directory
        goes into currentWorkDir.
        """
        #for telling where printed messages originate from
        fullFuncName = __name__ + '::extractData'
        indent = len(fullFuncName) + 2

        command = "tar = tarfile.open('" + self.localTar + \
                  "')\ntar.extractall(path='" + self.currentWorkDir + \
                  "')\ntar.close()"

        #untar the raw data
        print fullFuncName + ':', 'Extracting data.\n' + ' '*indent + \
              'Logging to', self.outFile + '.'
        self.outString += time.strftime('%a %b %d %H:%M:%S %Z %Y') + '\n'
        self.outString += 'Timing command:\n' + command + '\n'
        procT = time.clock()
        wallT = time.time()
        tar = tarfile.open(self.localTar)
        tar.extractall(path=self.currentWorkDir)
        tar.close()
        wallT = round(time.time() - wallT, 2)
        procT = round(time.clock() - procT, 2)
        self.outString += str(wallT) + 'wall ' + str(procT) + 'CPU\n\n'
        self.currentRedDir = self.currentWorkDir + \
                             os.path.basename(self.localTar)[:-4] + '/'


    def makeExtractOpts(self):
        """ Returns OptionParser.parse_args options so extractCASAscript.main can
            be called directly.

        Returns
        -------
        options : Options object from OptionParser.parse_args

        Notes
        -----
        Returns an options object from OptionParser.parse_args to feed into
        extractCASAscript.main since that script is originally intended to be
        run from the command line.
        """
        #for telling where printed messages originate from
        fullFuncName = __name__ + '::makeExtractOpts'
        indent = len(fullFuncName) + 2
        
        usage = \
            ''' %prog [options] URL
                *URL* should point to a CASA Guide webpage or to a Python
                script. *URL* can also be a local file system path.'''
        parser = OptionParser(usage=usage)
        parser.add_option('-b', '--benchmark', action="store_true", \
                          default=False)
        parser.add_option('-n', '--noninteractive', action="store_true", \
                          default=False)
        parser.add_option('-p', '--plotmsoff', action="store_true")
        parser.add_option('-d', '--diagplotoff', action="store_true")
        (options, args) = parser.parse_args()
        options.benchmark = True
        return options


    def runScriptExtractor(self):
        """ Calls extractCASAscript.main to make the calibration and imaging
            scripts.

        Returns
        -------
        None

        Notes
        -----
        This runs extractCASAscript.main to make the calibration and imaging
        scripts from the CASA guide. Runs it on calibrationURL and imagingURL
        and puts the extracted Python files into currentRedDir. This also
        fills out the scripts, benchmarking and benchmark summary log file
        paths in the benchmark object.
        """
        #for telling where printed messages originate from
        fullFuncName = __name__ + '::runScriptExtractor'
        indent = len(fullFuncName) + 2

        #remember where we were and change to reduction directory
        oldPWD = os.getcwd()
        os.chdir(self.currentRedDir)

        #do the script extraction
        print fullFuncName + ':', 'Extracting CASA Guide.\n' + ' '*indent + \
              'Logging to ' + self.extractLog
        stdOut = sys.stdout
        stdErr = sys.stderr
        sys.stdout = open(self.extractLog, 'w')
        sys.stderr = sys.stdout
        extractCASAscript.main(self.calibrationURL, self.makeExtractOpts())
        print '\n'
        print '-'
        print '---'
        print '-'
        print '\n'
        extractCASAscript.main(self.imagingURL, self.makeExtractOpts())
        stdOut, sys.stdout = sys.stdout, stdOut
        stdOut.close()
        stdErr, sys.stderr = sys.stderr, stdErr
        stdErr.close

        #change directory back to wherever we started from
        os.chdir(oldPWD)

        #store the script name(s) in the object
        scripts = list()
        f = open(self.extractLog, 'r')
        for line in f:
            if 'New file' in line:
                scripts.append(line.split(' ')[2])
        f.close()
        if 'Calibration' in  scripts[0]:
            self.calScript = self.currentRedDir + scripts[0]
            self.imageScript = self.currentRedDir + scripts[1]
        else:
            self.calScript = self.currentRedDir + scripts[1]
            self.imageScript = self.currentRedDir + scripts[0]

        #store the log name(s) in the object
        self.calScriptExpect = self.calScript + '.expected'
        self.imageScriptExpect = self.imageScript + '.expected'
        self.calScriptLog = self.calScript + '.log'
        self.imageScriptLog = self.imageScript + '.log'
        self.calBenchOutFile = self.calScript[:-3] + '.benchmark.txt'
        self.imageBenchOutFile = self.imageScript[:-3] + '.benchmark.txt'
        self.calBenchSumm = self.calBenchOutFile + '.summary'
        self.imageBenchSumm = self.imageBenchOutFile + '.summary'

        shutil.copy(self.calScriptExpect, self.currentLogDir)
        shutil.copy(self.imageScriptExpect, self.currentLogDir)


    def runGuideScript(self):
        """ Executes the calibration and imaging CASA guide scripts.

        Returns
        -------
        None

        Notes
        -----
        This runs the calScript and imageScript files with execfile, passing in
        all of the CASA global definitions. It also directs standard out and
        standard error to calScriptLog and imageScriptLog. These are run inside
        currentRedDir.
        """
        #for telling where printed messages originate from
        fullFuncName = __name__ + '::runGuideScript'
        indent = len(fullFuncName) + 2

        #remember where we were and change to reduction directory
        oldPWD = os.getcwd()
        os.chdir(self.currentRedDir)

        #remember what is in the CASA global namespace
        preKeys = self.CASAglobals.keys()

        #run calibration script
        print fullFuncName + ':', 'Beginning benchmark test of ' + \
              self.calScript + '.\n' + ' '*indent + 'Logging to ' + \
              self.calScriptLog + '.'
        stdOut = sys.stdout
        stdErr = sys.stderr
        sys.stdout = open(self.calScriptLog, 'w')
        sys.stderr = sys.stdout
        print 'CASA Version ' + self.CASAglobals['casadef'].casa_version + \
              ' (r' + self.CASAglobals['casadef'].subversion_revision + \
              ')\n  Compiled on: ' + self.CASAglobals['casadef'].build_time + \
              '\n\n'
        origLog = self.CASAglobals['casalog'].logfile()
        self.CASAglobals['casalog'].setlogfile(self.calScriptLog)
        execfile(self.calScript, self.CASAglobals)
        closeFile = sys.stdout
        sys.stdout = stdOut
        self.CASAglobals['casalog'].setlogfile(origLog)
        closeFile.close()
        print fullFuncName + ':', 'Finished test of ' + self.calScript

        #remove anything the calibration script added
        for key in self.CASAglobals.keys():
            if key not in preKeys:
                self.CASAglobals.pop(key, None)

        #run imaging script
        print fullFuncName + ':', 'Beginning benchmark test of ' + \
              self.imageScript + '.\n' + ' '*indent + 'Logging to ' + \
              self.imageScriptLog + '.'
        sys.stdout = open(self.imageScriptLog, 'w')
        sys.stderr = sys.stdout
        print 'CASA Version ' + self.CASAglobals['casadef'].casa_version + \
              ' (r' + self.CASAglobals['casadef'].subversion_revision + \
              ')\n  Compiled on: ' + self.CASAglobals['casadef'].build_time + \
              '\n\n'
        self.CASAglobals['casalog'].setlogfile(self.imageScriptLog)
        execfile(self.imageScript, self.CASAglobals)
        closeFile = sys.stdout
        sys.stdout = stdOut
        sys.stderr = stdErr
        self.CASAglobals['casalog'].setlogfile(origLog)
        closeFile.close()
        print fullFuncName + ':', 'Finished test of ' + self.imageScript

        #remove anything the imaging script added
        for key in self.CASAglobals.keys():
            if key not in preKeys:
                self.CASAglobals.pop(key, None)

        #copy logs to the current log directory
        shutil.copy(self.calScriptLog, self.currentLogDir)
        shutil.copy(self.imageScriptLog, self.currentLogDir)
        shutil.copy(self.calBenchOutFile, self.currentLogDir)
        shutil.copy(self.imageBenchOutFile, self.currentLogDir)
        shutil.copy(self.calBenchSumm, self.currentLogDir)
        shutil.copy(self.imageBenchSumm, self.currentLogDir)

        #change directory back to wherever we started from
        os.chdir(oldPWD)


    def writeOutFile(self):
        """ Writes outString to a text file.

        Returns
        -------
        None

        Notes
        -----
        This writes messages stored in outString to a text file with name from
        outFile. These messages are the output from timing the raw data download
        and unpacking.
        """
        #for telling where printed messages originate from
        fullFuncName = __name__ + '::writeOutFile'
        indent = len(fullFuncName) + 2
        
        f = open(self.outFile, 'w')
        f.write(self.outString)
        f.close()
