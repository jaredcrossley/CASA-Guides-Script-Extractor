import os
import sys
import shutil
import time
from cStringIO import StringIO
from optparse import OptionParser
import tarfile
from urllib2 import HTTPError

#import non-standard Python modules
import extractCASAscript

#-all methods should probably return something
#-make benchmark class work with just calibration or imaging script
#-I might not need to do the .pop stuff in runGuideScript now that it's
# generalized
#  -might be able to just pass CASAglobals an input parameter which could help
#-put in script extraction error handling (see notes.txt first entry for
# 2014-12-06)
#-investigate this message: "WARNING: reading as string array because float array
# failed"
#  -I see it from both calibration and imaging scripts for every test I run in
#   the .py.log files
#-does copy.copy need to be used when passing in CASAglobals to machine and
# benchmark?

class benchmark:
    """A class for the execution of a single CASA guide
    on a single machine for benchmark testing and timing.

    Parameters
    ----------

    CASAglobals : dict
        Dictionary returned by Python globals() function within the CASA
        namespace (environment). Simply pass the return value of the globals()
        function from within CASA where this class should be instantiated
        within.

    scriptDir : str
        Absolute path to directory containing the benchmarking module files.

    workDir : str
        Absolute path to directory where benchmarking directory structure will
        be created, all data will be stored and processing will be done.

    calibrationURL : str
        URL to CASA guide calibration webpage.

    imagingURL : str
        URL to CASA guide imaging webpage.

    dataPath : str
        URL or absolute path to raw CASA guide data and calibration tables.

    outFile : str
        Log file for operations done outside of other wrapper modules such as
        acquiring and extracting the raw data.

    skipDownload : bool
        Switch to skip downloading the raw data from the web. False means
        download the data from the URL provided in parameters.py variable.
        Defaults to False.

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

    dataPath : str
        URL or absolute path to raw CASA guide data and calibration tables.

    outFile : str
        Log file for operations done outside of other wrapper modules such as
        acquiring and extracting the raw data.

    skipDownload : bool
        Switch to skip downloading the raw data from the web.

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

    imageScriptLog : str
        Absolute path to imaging script output.

    calScriptExpect : str
        Absolute path to CASA guide script extractor output of expected
        calibraton task calls.

    imageScriptExpect : str
        Absolute path to CASA guide script extractor output of expected
        imaging task calls.

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
        YYYY_MMM_DDTHH_MM_SS-benchmark.

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

    status : str
        Code for the current benchmark instance determining what state the
        object is in. The primary use is to record if a handled error occurred
        that renders the benchmark useless. When the object is first
        instantiated this will be initialed to "normal" and will only be
        changed (to "failure") if a handled error is encountered.

    listTasksOut : str
        Holds the couple lines of output from the extractCASAscript.listCASAtasks
        call in __init__. It is written to extractLog just before the first
        script extraction is done. While the output should always be a couple of
        empty sets, it would be useful information if they are ever not empty.

    Methods
    -------

    __init__
        Initializes benchmark instance attributes.

    createDirTree
        Creates current benchmark instance directory structure.

    downloadData
        Uses wget to download raw data from the web.

    extractData
        Unpacks the raw data .tgz file.

    makeExtractOpts (this should be private, if I keep it at all)
        Returns OptionParser.parse_args options variable for extractCASAscript.

    runextractCASAscript (this should be private)
        Actually runs extractCASAscript.main with minimal checks for flaky URLs.

    doScriptExtraction (this should probably be split into cal, imaging and .py)
        Calls extractCASAscript.main to create CASA guide Python scripts.

    runGuideScript
        Executes either calibration or imaging extracted Python scripts.

    writeToOutFile
        Appends a string to outFile.

    useOtherBmarkScripts
        Copies extracted scripts and extraction logs into current benchmark.

    emptyCurrentRedDir
        Empties current reduction directory of everything except for scripts.
    """
    def __init__(self, CASAglobals=None, scriptDir='', workDir='./', \
                 calibrationURL='', imagingURL='', dataPath='', outFile='', \
                 skipDownload=False):
        #for telling where printed messages originate from
        fullFuncName = __name__ + '::__init__'
        indent = len(fullFuncName) + 2

        #default to an error unless __init__ at least finishes
        self.status = 'failure'

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

        #initialize the current benchmark instance directories and files
        self.currentWorkDir = self.workDir + \
                              time.strftime('%Y_%m_%dT%H_%M_%S') + \
                              '-benchmark/'
        self.currentLogDir = self.currentWorkDir + 'log_files/'
        self.outFile = self.currentLogDir + outFile
        self.currentTarDir = self.currentWorkDir + 'tarballs/'
        self.currentRedDir = ''
        self.allLogDir = self.workDir + 'all_logs/'
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

        #object is good to go at this point
        self.status = 'normal'

        #fill out casa_tasks with current CASA task list
        stdOut = sys.stdout
        stdErr = sys.stderr
        sys.stdout = StringIO()
        sys.stderr = sys.stdout
        myStdOut = sys.stdout
        extractCASAscript.casa_tasks = extractCASAscript.listCASATasks()
        stdOut, sys.stdout = sys.stdout, stdOut
        stdErr, sys.stderr = sys.stderr, stdErr
        self.listTasksOut = myStdOut.getvalue()


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
        outString = ''
        outString += time.strftime('%a %b %d %H:%M:%S %Z %Y') + '\n'
        outString += 'Timing command:\n' + command + '\n'
        procT = time.clock()
        wallT = time.time()
        os.system(command)
        wallT = round(time.time() - wallT, 2)
        procT = round(time.clock() - procT, 2)
        outString += str(wallT) + 'wall ' + str(procT) + 'CPU\n\n'
        self.writeToOutFile(outString)
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
        outString = ''
        outString += time.strftime('%a %b %d %H:%M:%S %Z %Y') + '\n'
        outString += 'Timing command:\n' + command + '\n'
        procT = time.clock()
        wallT = time.time()
        tar = tarfile.open(self.localTar)
        tar.extractall(path=self.currentWorkDir)
        tar.close()
        wallT = round(time.time() - wallT, 2)
        procT = round(time.clock() - procT, 2)
        outString += str(wallT) + 'wall ' + str(procT) + 'CPU\n\n'
        self.writeToOutFile(outString)
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


    def runextractCASAscript(self, url):
        """ Calls extractCASAscript.main on given url to make CASA script.
        (should probably be private)

        Returns
        -------
        True if extractCASAscript.main worked, False if it failed 3 times.

        Notes
        -----
        This runs extractCASAscript.main on the given url to make scripts from
        associated the CASA guide. Tries running the extraction 3 times, handling
        HTTPError exceptions. If an attempt fails then it waits 30 seconds and
        tries again. If it fails all 3 times then it gives up and returns False.
        Otherwise it returns True.
        """
        #for telling where printed messages originate from
        fullFuncName = __name__ + '::runextractCASAscript'
        indent = len(fullFuncName) + 2

        #try three times at most to extract the script
        for i in range(3):
            try:
                extractCASAscript.main(url, self.makeExtractOpts())
                return True
            except HTTPError, e:
                if i != 2:
                    time.sleep(30)
                else:
                    print fullFuncName + ':', 'Ran into HTTPError 3 times.\n' + \
                          ' '*indent + 'Giving up on extracting a script ' + \
                          'from ' + url + '.'
                    print fullFuncName + ':', 'Particular HTTPError info:\n' + \
                          ' '*indent + 'Code ' + e.code + ': ' + e.reason
                    return False


    def doScriptExtraction(self, stage):
        """ Runs the script extractor for the calibration or imaging script and
        arranges all of the associated details.

        Parameters
        ----------
        stage : str
           Specifies which script to extract, calibration or imaging. Can be
           either "cal" or "im" and will raise a ValueError otherwise.

        Returns
        -------
        None

        Notes
        -----
        This ensures the extraction output is logged, runs the script extraction
        and fills out all of the associated attributes. Scripts are made from
        calibrationURL or imagingURL and are put into currentRedDir. If this is
        the first script extraction, then it will also write listTasksOut to
        extractLog.
        """
        #for telling where printed messages originate from
        fullFuncName = __name__ + '::doScriptExtraction'
        indent = len(fullFuncName) + 2

        #check input
        if stage != 'cal' and stage != 'im':
            raise ValueError('stage must be either "cal" or "im".')

        #remember where we were and change to reduction directory
        oldPWD = os.getcwd()
        os.chdir(self.currentRedDir)

        #set the output to the extraction log
        print fullFuncName + ':', 'Extracting CASA Guide.\n' + ' '*indent + \
              'Logging to ' + self.extractLog
        stdOut = sys.stdout
        stdErr = sys.stderr
        sys.stdout = open(self.extractLog, 'a')
        sys.stderr = sys.stdout

        #write listTasksOut if this is first extraction
        if os.stat(self.extractLog).st_size == 0:
            print self.listTasksOut
            print

        #set local variables based on stage
        if stage == 'cal':
            scriptURL = self.calibrationURL
        else:
            scriptURL = self.imagingURL

        result = self.runextractCASAscript(scriptURL)
        print '\n'
        print '='*80
        print '\n'

        #change logs back and go back to wherever we were before
        stdOut, sys.stdout = sys.stdout, stdOut
        stdOut.close()
        stdErr, sys.stderr = sys.stderr, stdErr
        stdErr.close()
        os.chdir(oldPWD)

        #report failure if extraction didn't work
        if not result:
            self.status = 'failure'
            return

        #grab the new script name
        f = open(self.extractLog, 'r')
        for line in reversed(f.readlines()):
            if 'New file' in line:
                scriptName = line.split(' ')[2]
                break
        f.close()

        #store file names in the object
        if stage == 'cal':
            self.calScript = self.currentRedDir + scriptName
            self.calScriptExpect = self.calScript + '.expected'
            self.calScriptLog = self.calScript + '.log'
            self.calBenchOutFile = self.calScript[:-3] + '.benchmark.txt'
            self.calBenchSumm = self.calBenchOutFile + '.summary'
            shutil.copy(self.calScriptExpect, self.currentLogDir)
        else:
            self.imageScript = self.currentRedDir + scriptName
            self.imageScriptExpect = self.imageScript + '.expected'
            self.imageScriptLog = self.imageScript + '.log'
            self.imageBenchOutFile = self.imageScript[:-3] + '.benchmark.txt'
            self.imageBenchSumm = self.imageBenchOutFile + '.summary'
            shutil.copy(self.imageScriptExpect, self.currentLogDir)


    def runGuideScript(self, stage):
        """ Executes the calibration or imaging CASA guide script.

        Parameters
        ----------
        stage : str
           Specifies which script to run, calibration or imaging. Can be either
           "cal" or "im" and will raise a ValueError otherwise.

        Returns
        -------
        None

        Notes
        -----
        This runs either the calScript or imageScript file with execfile, passing
        in all of the CASA global definitions, depending on the setting of stage.
        It directs standard out and standard error to calScriptLog or
        imageScriptLog during execution. These are run inside currentRedDir.
        Lastly, it copies the calScriptLog, calBenchOutFile and calBenchSumm
        files or imageScriptLog, imageBenchOutFile and imageBenchSumm files to
        currentLogDir and (sans script logs) to allLogDir.
        """
        #for telling where printed messages originate from
        fullFuncName = __name__ + '::runGuideScript'
        indent = len(fullFuncName) + 2

        #check input
        if stage != 'cal' and stage != 'im':
            raise ValueError('stage must be either "cal" or "im".')

        #remember where we were and change to reduction directory
        oldPWD = os.getcwd()
        os.chdir(self.currentRedDir)

        #remember what is in the CASA global namespace
        preKeys = self.CASAglobals.keys()

        #set local variables based on stage
        if stage == 'cal':
            script = self.calScript
            scriptLog = self.calScriptLog
            benchOutFile = self.calBenchOutFile
            benchSumm = self.calBenchSumm
        else:
            script = self.imageScript
            scriptLog = self.imageScriptLog
            benchOutFile = self.imageBenchOutFile
            benchSumm = self.imageBenchSumm

        #setup logging
        print fullFuncName + ':', 'Beginning benchmark test of ' + \
              script + '.\n' + ' '*indent + 'Logging to ' + scriptLog + '.'
        stdOut = sys.stdout
        stdErr = sys.stderr
        sys.stdout = open(scriptLog, 'a')
        sys.stderr = sys.stdout
        print 'CASA Version ' + self.CASAglobals['casadef'].casa_version + \
              ' (r' + self.CASAglobals['casadef'].subversion_revision + \
              ')\n  Compiled on: ' + self.CASAglobals['casadef'].build_time + \
              '\n\n'
        origLog = self.CASAglobals['casalog'].logfile()
        self.CASAglobals['casalog'].setlogfile(scriptLog)

        execfile(script, self.CASAglobals)

        #put logs back
        closeFile = sys.stdout
        sys.stdout = stdOut
        self.CASAglobals['casalog'].setlogfile(origLog)
        closeFile.close()
        print fullFuncName + ':', 'Finished test of ' + script

        #remove anything the script added
        for key in self.CASAglobals.keys():
            if key not in preKeys:
                self.CASAglobals.pop(key, None)

        #copy logs to current log directory
        shutil.copy(scriptLog, self.currentLogDir)
        shutil.copy(benchOutFile, self.currentLogDir)
        shutil.copy(benchSumm, self.currentLogDir)

        #copy pertinent logs to all_logs directory
        prefix = self.allLogDir + os.path.basename(self.currentWorkDir[:-1]) + \
                 '__'
        shutil.copy(benchOutFile, prefix + os.path.basename(benchOutFile))
        shutil.copy(benchSumm, prefix + os.path.basename(benchSumm))

        #change directory back to wherever we started from
        os.chdir(oldPWD)


    def writeToOutFile(self, outString):
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
        fullFuncName = __name__ + '::writeToOutFile'
        indent = len(fullFuncName) + 2
        
        f = open(self.outFile, 'a')
        f.write(outString)
        f.close()

    def useOtherBmarkScripts(self, prevBmark):
        """ Sets this benchmark instance up to use extracted scripts from
        another benchmark object.

        Parameters
        ----------
        prevBmark : benchmark object
           Source object for copying scripts etc. from. Wisest choice would be
           one that already finshed and was successful.

        Returns
        -------
        None

        Notes
        -----
        Copies the extracted scripts, .expected files and extraction log
        from another benchmark object to the directory tree associated with
        this benchmark instance. Also fills out the script related attributes
        for this instance. These attributes are: extractLog, calScript,
        calScriptLog, imageScript, imageScriptLog, calScriptExpect,
        imageScriptExpect, calBenchOutFile, calBenchSumm, imageBenchOutFile and
        imageBenchSumm.
        """
        #for telling where printed messages originate from
        fullFuncName = __name__ + '::useOtherBmarkScripts'
        indent = len(fullFuncName) + 2

        #copy the files to current directory tree
        shutil.copy(prevBmark.calScript, self.currentRedDir)
        shutil.copy(prevBmark.imageScript, self.currentRedDir)
        shutil.copy(prevBmark.calScriptExpect, self.currentRedDir)
        shutil.copy(prevBmark.calScriptExpect, self.currentLogDir)
        shutil.copy(prevBmark.imageScriptExpect, self.currentRedDir)
        shutil.copy(prevBmark.imageScriptExpect, self.currentLogDir)
        shutil.copy(prevBmark.extractLog, self.currentLogDir)

        #setup current script associated attributes
        self.extractLog = self.currentLogDir + \
                          os.path.basename(prevBmark.extractLog)
        self.calScript = self.currentRedDir + \
                         os.path.basename(prevBmark.calScript)
        self.calScriptLog = self.currentRedDir + \
                            os.path.basename(prevBmark.calScriptLog)
        self.imageScript = self.currentRedDir + \
                           os.path.basename(prevBmark.imageScript)
        self.imageScriptLog = self.currentRedDir + \
                              os.path.basename(prevBmark.imageScriptLog)
        self.calScriptExpect = self.currentRedDir + \
                               os.path.basename(prevBmark.calScriptExpect)
        self.imageScriptExpect = self.currentRedDir + \
                                os.path.basename(prevBmark.imageScriptExpect)
        self.calBenchOutFile = self.currentRedDir + \
                               os.path.basename(prevBmark.calBenchOutFile)
        self.calBenchSumm = self.currentRedDir + \
                            os.path.basename(prevBmark.calBenchSumm)
        self.imageBenchOutFile = self.currentRedDir + \
                                 os.path.basename(prevBmark.imageBenchOutFile)
        self.imageBenchSumm = self.currentRedDir + \
                              os.path.basename(prevBmark.imageBenchSumm)


    def emptyCurrentRedDir(self):
        """ Empties out the current reduction directory (except for the
        calibration and imaging scripts) and reassigns affected attributes.

        Returns
        -------
        None

        Notes
        -----
        The intention is to use this once a benchmark execution is complete so
        that disk space can be conserved, but this can technically be run
        anytime after the extractData method is run. This uses shutil.rmtree so
        it should be as platform-independent as that module. Everything in the
        current reduction directory is removed except for the calibration and
        imaging scripts. After directory is emptied, all attributes associated
        with removed files are changed to references to the log_files/ directory.
        Affected attributes are calScriptLog, imageScriptLog, calScriptExpect,
        imageScriptExpect, calBenchOutFile, calBenchSumm, imageBenchOutFile and
        imageBenchSumm.
        """
        #for telling where printed messages originate from
        fullFuncName = __name__ + '::emptyCurrentRedDir'
        indent = len(fullFuncName) + 2

        #move scripts to save them
        oldPWD = os.getcwd()
        os.chdir(self.currentRedDir)
        shutil.move(self.calScript, '..')
        shutil.move(self.imageScript, '..')

        #empty out the current reduction directory
        os.chdir(self.currentLogDir)
        shutil.rmtree(self.currentRedDir)
        os.mkdir(self.currentRedDir)

        #move scripts back
        os.chdir(self.currentRedDir)
        shutil.move('../' + os.path.basename(self.calScript), '.')
        shutil.move('../' + os.path.basename(self.imageScript), '.')
        os.chdir(oldPWD)

        #change path attributes based on emptying directory
        self.calScriptLog = self.currentLogDir + \
                            os.path.basename(self.calScriptLog)
        self.imageScriptLog = self.currentLogDir + \
                              os.path.basename(self.imageScriptLog)
        self.calScriptExpect = self.currentLogDir + \
                               os.path.basename(self.calScriptExpect)
        self.imageScriptExpect = self.currentLogDir + \
                                 os.path.basename(self.imageScriptExpect)
        self.calBenchOutFile = self.currentLogDir + \
                               os.path.basename(self.calBenchOutFile)
        self.calBenchSumm = self.currentLogDir + \
                            os.path.basename(self.calBenchSumm)
        self.imageBenchOutFile = self.currentLogDir + \
                                 os.path.basename(self.imageBenchOutFile)
        self.imageBenchSumm = self.currentLogDir + \
                              os.path.basename(self.imageBenchSumm)
