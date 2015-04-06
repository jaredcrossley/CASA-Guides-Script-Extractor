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
#-figure out Python's version of private and public
#-need to change class docstring to standard Python style so information isn't
# redundant but I also still have a record of all the included attributes and
# methods
#-change docstrings to prescribe the function or method's effect as a command
# ("Do this", "Return that"), not as a description; e.g. don't write "Returns
# the pathname ...", instead write "Return the pathname..."

class benchmark:
    """A class for the execution of a single CASA guide
    on a single machine for benchmark testing and timing.

    Parameters
    ----------

    scriptDir : str
        Absolute path to directory containing the benchmarking module files.

    workDir : str
        Absolute path to directory where benchmarking directory structure will
        be created, all data will be stored and processing will be done.

    execStep : str
        String specifying what will be executed in this benchmarking run:
        calibration, imaging or both. Must be "cal", "im" or "both". Defaults to
        "both".

    calSource : str
        URL to CASA guide calibration webpage or path to Python script to
        extract the calibration commands from.

    imSource : str
        URL to CASA guide imaging webpage or path to Python script to extract
        the imaging commands from.

    uncalDataPath : str
        URL or absolute path to uncalibrated raw CASA guide data and
        calibration tables.

    calDataPath : str
        URL or absolute path to calibrated raw CASA guide data and
        calibration tables.

    skipDownload : bool
        Switch to skip downloading the raw data from the web. False means
        download the data from the URL provided in parameters.py variable.
        Defaults to False.

    Attributes
    ----------

    workDir : str
        Absolute path to directory where benchmarking directory structure will
        be created, all data will be stored and processing will be done.

    execStep : str
        String specifying what will be executed in this benchmarking run:
        calibration, imaging or both. Must be "cal", "im" or "both".

    calSource : str
        URL to CASA guide calibration webpage or path to Python script to
        extract the calibration commands from.

    imSource : str
        URL to CASA guide imaging webpage or path to Python script to extract
        the imaging commands from.

    uncalDataPath : str
        URL or absolute path to uncalibrated raw CASA guide data and
        calibration tables.

    calDataPath : str
        URL or absolute path to calibrated raw CASA guide data and
        calibration tables.

    skipDownload : bool
        Switch to skip downloading the raw data from the web.

    uncalLocalTar : str
        Absolute path to uncalibrated raw data .tgz file associated with CASA
        guide.

    calLocalTar : str
        Absolute path to calibrated raw data .tgz file associated with CASA
        guide.

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
    """
    def __init__(self, scriptDir='', workDir='./', execStep='both', \
                 calSource='', imSource='', uncalDataPath='', calDataPath='', \
                 skipDownload=False):
        #for telling where printed messages originate from
        fullFuncName = __name__ + '::__init__'
        indent = len(fullFuncName) + 2

        #default to an error unless at least __init__ finishes
        self.status = 'failure'

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
        if execStep != 'cal' and execStep != 'im' and execStep != 'both':
            raise ValueError('execStep must be set to "cal", "im" or "both".')
        self.execStep = execStep
        if self.execStep == 'cal':
            if calSource == '':
                raise ValueError('URL to calibration CASA guide must be given.')
            if uncalDataPath == '':
                raise ValueError('A URL or path must be given pointing to ' + \
                                 'the uncalibrated raw data.')
        if self.execStep == 'im':
            if imSource == '':
                raise ValueError('URL to imaging CASA guide must be given.')
            if calDataPath == '':
                raise ValueError('A URL or path must be given pointing to ' + \
                                 'the calibrated raw data.')
        if self.execStep == 'both':
            if calSource == '' or imSource == '':
                raise ValueError('URLs to calibration and imaging CASA ' + \
                                 'guides must be given.')
            if uncalDataPath == '':
                raise ValueError('A URL or path must be given pointing to ' + \
                                 'the uncalibrated raw data.')

        #other class variable initialization
        if self.execStep == 'cal':
            self.calSource = calSource
            self.imSource = ''
            self.uncalDataPath = uncalDataPath
            self.calDataPath = ''
        if self.execStep == 'im':
            self.calSource = ''
            self.imSource = imSource
            self.uncalDataPath = ''
            self.calDataPath = calDataPath
        if self.execStep == 'both':
            self.calSource = calSource
            self.imSource = imSource
            self.uncalDataPath = uncalDataPath
            self.calDataPath = ''
        self.skipDownload = skipDownload

        #check tarball exists if skipping download
        if self.skipDownload:
            if self.execStep == 'cal':
                if not os.path.isfile(self.uncalDataPath):
                    raise ValueError('Cannot find uncalibrated local ' + \
                                     'tarball for extraction. Download may ' + \
                                     'be required.')
                self.uncalLocalTar = self.uncalDataPath
                self.calLocalTar = ''
            if self.execStep == 'im':
                if not os.path.isfile(self.calDataPath):
                    raise ValueError('Cannot find calibrated local tarball ' + \
                                     'for extraction. Download may be required.')
                self.uncalLocalTar = ''
                self.calLocalTar = self.calDataPath
            if self.execStep == 'both':
                if not os.path.isfile(self.uncalDataPath):
                    raise ValueError('Cannot find uncalibrated local ' + \
                                     'tarball for extraction. Download may ' + \
                                     'be required.')
                self.uncalLocalTar = self.uncalDataPath
                self.calLocalTar = ''
            print fullFuncName + ':', 'Data available by filesystem.'
        #check data paths are URLs if downloading data instead
        else:
            self.uncalLocalTar = ''
            self.calLocalTar = ''
            if self.execStep == 'cal':
                if self.uncalDataPath[0:4] != 'http':
                    raise ValueError("'" + self.uncalDataPath + "' is not a " + \
                                     'valid URL for downloading the data.')
            if self.execStep == 'im':
                if self.calDataPath[0:4] != 'http':
                    raise ValueError("'" + self.calDataPath + "' is not a " + \
                                     'valid URL for downloading the data.')
            if self.execStep == 'both':
                if self.uncalDataPath[0:4] != 'http':
                    raise ValueError("'" + self.uncalDataPath + "' is not a " + \
                                     'valid URL for downloading the data.')

        #initialize the current benchmark instance directories and files
        self.currentWorkDir = self.workDir + \
                              time.strftime('%Y_%m_%dT%H_%M_%S') + \
                              '-benchmark/'
        self.currentLogDir = self.currentWorkDir + 'log_files/'
        self.daeLog = self.currentLogDir + 'download_and_extract.log'
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
        from the web (uncalDataPath or calDataPath) into currentTarDir using
        wget. Here os.system is used to execute wget so it is not perfectly
        platform independent but should be fine across Linux and Mac. The wget
        options used are:
        
          wget -q --no-check-certificate --directory-prefix=currentTarDir
        """
        #for telling where printed messages originate from
        fullFuncName = __name__ + '::downloadData'
        indent = len(fullFuncName) + 2

        #check that we should be downloading
        if self.skipDownload:
            raise ValueError('skipDownload is set to True so this benchmark ' + \
                             'cannot download the data. Create a new ' + \
                             'instance with skipDownload=False if you wish ' + \
                             'to download the data.')

        #build wget command
        if self.execStep == 'cal':
            dataPath = self.uncalDataPath
        if self.execStep == 'im':
            dataPath = self.calDataPath
        if self.execStep == 'both':
            dataPath = self.uncalDataPath
        command = 'wget -q --no-check-certificate --directory-prefix=' + \
                  self.currentTarDir + ' ' + dataPath

        #wget the data
        print fullFuncName + ':', 'Acquiring data by HTTP.\n' + ' '*indent + \
              'Logging to', self.daeLog + '.'
        outString = ''
        outString += time.strftime('%a %b %d %H:%M:%S %Z %Y') + '\n'
        outString += 'Timing command:\n' + command + '\n'
        procT = time.clock()
        wallT = time.time()
        os.system(command)
        wallT = round(time.time() - wallT, 2)
        procT = round(time.clock() - procT, 2)
        outString += str(wallT) + 'wall ' + str(procT) + 'CPU\n\n'
        self.writeToDaELog(outString)

        #set local tarball paths
        if self.execStep == 'cal':
            self.uncalLocalTar = self.currentTarDir + dataPath.split('/')[-1]
            self.calLocalTar = ''
        if self.execStep == 'im':
            self.uncalLocalTar = ''
            self.calLocalTar = self.currentTarDir + dataPath.split('/')[-1]
        if self.execStep == 'both':
            self.uncalLocalTar = self.currentTarDir + dataPath.split('/')[-1]
            self.calLocalTar = ''


    def extractData(self):
        """ Unpacks the raw data .tgz file into the current benchmark directory.

        Returns
        -------
        None

        Notes
        -----
        This unpacks the raw data .tgz file in uncalLocalTar or calLocalTar and
        times the process. It uses the tarfile module so it should be as
        platform independent as that module is. The unpacked directory goes into
        currentWorkDir.
        """
        #for telling where printed messages originate from
        fullFuncName = __name__ + '::extractData'
        indent = len(fullFuncName) + 2

        #build extraction commands
        if self.execStep == 'cal':
            localTar = self.uncalLocalTar
        if self.execStep == 'im':
            localTar = self.calLocalTar
        if self.execStep == 'both':
            localTar = self.uncalLocalTar
        command = "tar = tarfile.open('" + localTar + \
                  "')\ntar.extractall(path='" + self.currentWorkDir + \
                  "')\ntar.close()"

        #untar the raw data
        print fullFuncName + ':', 'Extracting data.\n' + ' '*indent + \
              'Logging to', self.daeLog + '.'
        outString = ''
        outString += time.strftime('%a %b %d %H:%M:%S %Z %Y') + '\n'
        outString += 'Timing command:\n' + command + '\n'
        procT = time.clock()
        wallT = time.time()
        tar = tarfile.open(localTar)
        tar.extractall(path=self.currentWorkDir)
        tar.close()
        wallT = round(time.time() - wallT, 2)
        procT = round(time.clock() - procT, 2)
        outString += str(wallT) + 'wall ' + str(procT) + 'CPU\n\n'
        self.writeToDaELog(outString)
        self.currentRedDir = self.currentWorkDir + \
                             os.path.basename(localTar)[:-4] + '/'


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

        Parameters
        ----------
        url : str
           Specifies URL to run extractCASAscript.main on.

        Returns
        -------
        True if extractCASAscript.main worked, False if it failed 3 times.

        Notes
        -----
        This runs extractCASAscript.main on the given url to make scripts from
        the associated CASA guide. Tries running the extraction 3 times, handling
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


    def doScriptExtraction(self):
        """ Runs the script extractor for the calibration and/or imaging script
        and arranges all of the associated details.

        Returns
        -------
        None

        Notes
        -----
        This ensures the extraction output is logged, runs the script extraction
        and fills out all of the associated attributes. Scripts are made from
        calSource and/or imSource and are put into currentRedDir. This will also
        write listTasksOut to extractLog.
        """
        #for telling where printed messages originate from
        fullFuncName = __name__ + '::doScriptExtraction'
        indent = len(fullFuncName) + 2

        #remember where we were and change to reduction directory
        oldPWD = os.getcwd()
        os.chdir(self.currentRedDir)

        #set the output to the extraction log
        print fullFuncName + ':', 'Extracting CASA Guide.\n' + ' '*indent + \
              'Logging to ' + self.extractLog
        outFDsave = os.dup(1)
        errFDsave = os.dup(2)
        extractLogF = open(self.extractLog, 'a')
        extractLogFD = extractLogF.fileno()
        os.dup2(extractLogFD, 1)
        os.dup2(extractLogFD, 2)

        print self.listTasksOut
        print '\n'

        if self.execStep == 'cal':
            result = self.runextractCASAscript(self.calSource)
        if self.execStep == 'im':
            result = self.runextractCASAscript(self.imSource)
        if self.execStep == 'both':
            result = self.runextractCASAscript(self.calSource)
            if result:
                result = self.runextractCASAscript(self.imSource)
        print '\n'
        print '='*80
        print '\n'

        #change logs back and go back to wherever we were before
        os.dup2(outFDsave, 1)
        os.close(outFDsave)
        os.dup2(errFDsave, 2)
        os.close(errFDsave)
        extractLogF.close()
        os.chdir(oldPWD)

        #report failure if extraction didn't work
        if not result:
            print fullFuncName + ':', 'Setting benchmark.status to ' + \
                  '"failure" and returning.'
            self.status = 'failure'
            return

        #grab script name(s)
        first = True
        f = open(self.extractLog, 'r')
        for line in f.readlines():
            if 'New file' in line:
                if self.execStep == 'cal':
                    calScriptName = line.split(' ')[2]
                    imScriptName = ''
                    break
                if self.execStep == 'im':
                    calScriptName = ''
                    imScriptName = line.split(' ')[2]
                    break
                if self.execStep == 'both':
                    if first:
                        calScriptName = line.split(' ')[2]
                        first = False
                    else:
                        imScriptName = line.split(' ')[2]
                        break
        f.close()

        #store file names in the object
        if self.execStep == 'cal':
            self.calScript = self.currentRedDir + calScriptName
            self.calScriptExpect = self.calScript + '.expected'
            self.calScriptLog = self.calScript + '.log'
            self.calBenchOutFile = self.calScript[:-3] + '.benchmark.txt'
            self.calBenchSumm = self.calBenchOutFile + '.summary'
            shutil.copy(self.calScriptExpect, self.currentLogDir)
            self.imageScript = ''
            self.imageScriptExpect = ''
            self.imageScriptLog = ''
            self.imageBenchOutFile = ''
            self.imageBenchSumm = ''
        if self.execStep == 'im':
            self.calScript = ''
            self.calScriptExpect = ''
            self.calScriptLog = ''
            self.calBenchOutFile = ''
            self.calBenchSumm = ''
            self.imageScript = self.currentRedDir + imScriptName
            self.imageScriptExpect = self.imageScript + '.expected'
            self.imageScriptLog = self.imageScript + '.log'
            self.imageBenchOutFile = self.imageScript[:-3] + '.benchmark.txt'
            self.imageBenchSumm = self.imageBenchOutFile + '.summary'
            shutil.copy(self.imageScriptExpect, self.currentLogDir)
        if self.execStep == 'both':
            self.calScript = self.currentRedDir + calScriptName
            self.calScriptExpect = self.calScript + '.expected'
            self.calScriptLog = self.calScript + '.log'
            self.calBenchOutFile = self.calScript[:-3] + '.benchmark.txt'
            self.calBenchSumm = self.calBenchOutFile + '.summary'
            shutil.copy(self.calScriptExpect, self.currentLogDir)
            self.imageScript = self.currentRedDir + imScriptName
            self.imageScriptExpect = self.imageScript + '.expected'
            self.imageScriptLog = self.imageScript + '.log'
            self.imageBenchOutFile = self.imageScript[:-3] + '.benchmark.txt'
            self.imageBenchSumm = self.imageBenchOutFile + '.summary'
            shutil.copy(self.imageScriptExpect, self.currentLogDir)


    def runGuideScripts(self, CASAglobals):
        """ Executes the calibration and/or imaging CASA guide script.

        Parameters
        ----------
        CASAglobals : dict
           Dictionary returned by Python globals() function within the CASA
           namespace (environment). Simply pass the return value of the globals()
           function.

        Returns
        -------
        None

        Notes
        -----
        This runs the calScript and/or imageScript file with execfile, passing
        in all of the CASA global definitions, depending on the setting of
        benchmark.execStep. It directs standard out and standard error to
        calScriptLog or imageScriptLog during execution. These are run inside
        currentRedDir. Lastly, it copies the calScriptLog, calBenchOutFile and
        calBenchSumm files and/or imageScriptLog, imageBenchOutFile and
        imageBenchSumm files to currentLogDir and (sans script logs) to
        allLogDir.
        """
        #for telling where printed messages originate from
        fullFuncName = __name__ + '::runGuideScripts'
        indent = len(fullFuncName) + 2

        #check input
        if type(CASAglobals) != dict:
            raise TypeError('CASAglobals must be dictionary returned by ' + \
                            'globals built-in function.')

        #remember where we were and change to reduction directory
        oldPWD = os.getcwd()
        os.chdir(self.currentRedDir)

        #remember what is in the CASA global namespace
        preKeys = CASAglobals.keys()

        #set local variables based on execStep
        if self.execStep == 'cal':
            scripts = [self.calScript]
            scriptLogs = [self.calScriptLog]
            benchOutFiles = [self.calBenchOutFile]
            benchSumms = [self.calBenchSumm]
        if self.execStep == 'im':
            scripts = [self.imageScript]
            scriptLogs = [self.imageScriptLog]
            benchOutFiles = [self.imageBenchOutFile]
            benchSumms = [self.imageBenchSumm]
        if self.execStep == 'both':
            scripts = [self.calScript, self.imageScript]
            scriptLogs = [self.calScriptLog, self.imageScriptLog]
            benchOutFiles = [self.calBenchOutFile, self.imageBenchOutFile]
            benchSumms = [self.calBenchSumm, self.imageBenchSumm]

        for i in range(len(scripts)):
            #setup logging
            print fullFuncName + ':', 'Beginning benchmark test of ' + \
                  scripts[i] + '.\n' + ' '*indent + 'Logging to ' + \
                  scriptLogs[i] + '.'
            outFDsave = os.dup(1)
            errFDsave = os.dup(2)
            scriptLogF = open(scriptLogs[i], 'a')
            scriptLogFD = scriptLogF.fileno()
            os.dup2(scriptLogFD, 1)
            os.dup2(scriptLogFD, 2)
            print 'CASA Version ' + CASAglobals['casadef'].casa_version + \
                  ' (r' + CASAglobals['casadef'].subversion_revision + \
                  ')\n  Compiled on: ' + CASAglobals['casadef'].build_time + \
                  '\n\n'
            origLog = CASAglobals['casalog'].logfile()
            CASAglobals['casalog'].setlogfile(scriptLogs[i])

            execfile(scripts[i], CASAglobals)

            #put logs back
            os.dup2(outFDsave, 1)
            os.close(outFDsave)
            os.dup2(errFDsave, 2)
            os.close(errFDsave)
            scriptLogF.close()
            CASAglobals['casalog'].setlogfile(origLog)
            print fullFuncName + ':', 'Finished test of ' + scripts[i]

            #remove anything the script added
            for key in CASAglobals.keys():
                if key not in preKeys:
                    CASAglobals.pop(key, None)

            #copy logs to current log directory
            shutil.copy(scriptLogs[i], self.currentLogDir)
            shutil.copy(benchOutFiles[i], self.currentLogDir)
            shutil.copy(benchSumms[i], self.currentLogDir)

            #copy pertinent logs to all_logs directory
            prefix = self.allLogDir + \
                     os.path.basename(self.currentWorkDir[:-1]) + '__'
            shutil.copy(benchOutFiles[i], prefix + \
                        os.path.basename(benchOutFiles[i]))
            shutil.copy(benchSumms[i], prefix + os.path.basename(benchSumms[i]))

        #change directory back to wherever we started from
        os.chdir(oldPWD)


    def writeToDaELog(self, outString):
        """ Writes outString to a text file.

        Parameters
        ----------
        outString : str
           String containing characters to be written to
           download_and_extract.log.

        Returns
        -------
        None

        Notes
        -----
        This writes messages stored in outString to a text file named
        download_and_extract.log in the logDir. These messages are the output
        from timing the raw data download and unpacking.
        """
        #for telling where printed messages originate from
        fullFuncName = __name__ + '::writeToDaELog'
        indent = len(fullFuncName) + 2
        
        f = open(self.daeLog, 'a')
        f.write(outString)
        f.close()

    def useOtherBmarkScripts(self, prevBmark):
        """ Sets this benchmark instance up to use extracted scripts from
        another benchmark object.

        Parameters
        ----------
        prevBmark : benchmark object
           Source object for copying scripts etcetera from. Wisest choice would
           be one that already finshed and was successful.

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

        #check prevBmark ran same step as current
        if self.execStep != prevBmark.execStep:
            raise ValueError('Previous benchmark instance is not setup for ' + \
                             'the same execStep as the current benchmark ' + \
                             'instance.')

        #copy the files to current directory tree
        shutil.copy(prevBmark.extractLog, self.currentLogDir)
        if prevBmark.execStep == 'cal':
            shutil.copy(prevBmark.calScript, self.currentRedDir)
            shutil.copy(prevBmark.calScriptExpect, self.currentRedDir)
            shutil.copy(prevBmark.calScriptExpect, self.currentLogDir)
        if prevBmark.execStep == 'im':
            shutil.copy(prevBmark.imageScript, self.currentRedDir)
            shutil.copy(prevBmark.imageScriptExpect, self.currentRedDir)
            shutil.copy(prevBmark.imageScriptExpect, self.currentLogDir)
        if prevBmark.execStep == 'both':
            shutil.copy(prevBmark.calScript, self.currentRedDir)
            shutil.copy(prevBmark.imageScript, self.currentRedDir)
            shutil.copy(prevBmark.calScriptExpect, self.currentRedDir)
            shutil.copy(prevBmark.calScriptExpect, self.currentLogDir)
            shutil.copy(prevBmark.imageScriptExpect, self.currentRedDir)
            shutil.copy(prevBmark.imageScriptExpect, self.currentLogDir)

        #setup current script associated attributes
        self.extractLog = self.currentLogDir + \
                          os.path.basename(prevBmark.extractLog)
        if prevBmark.execStep == 'cal':
            self.calScript = self.currentRedDir + \
                             os.path.basename(prevBmark.calScript)
            self.calScriptLog = self.currentRedDir + \
                                os.path.basename(prevBmark.calScriptLog)
            self.imageScript = ''
            self.imageScriptLog = ''
            self.calScriptExpect = self.currentRedDir + \
                                   os.path.basename(prevBmark.calScriptExpect)
            self.imageScriptExpect = ''
            self.calBenchOutFile = self.currentRedDir + \
                                   os.path.basename(prevBmark.calBenchOutFile)
            self.calBenchSumm = self.currentRedDir + \
                                os.path.basename(prevBmark.calBenchSumm)
            self.imageBenchOutFile = ''
            self.imageBenchSumm = ''
        if prevBmark.execStep == 'im':
            self.calScript = ''
            self.calScriptLog = ''
            self.imageScript = self.currentRedDir + \
                               os.path.basename(prevBmark.imageScript)
            self.imageScriptLog = self.currentRedDir + \
                                  os.path.basename(prevBmark.imageScriptLog)
            self.calScriptExpect = ''
            self.imageScriptExpect = self.currentRedDir + \
                                    os.path.basename(prevBmark.imageScriptExpect)
            self.calBenchOutFile = ''
            self.calBenchSumm = ''
            self.imageBenchOutFile = self.currentRedDir + \
                                    os.path.basename(prevBmark.imageBenchOutFile)
            self.imageBenchSumm = self.currentRedDir + \
                                  os.path.basename(prevBmark.imageBenchSumm)
        if prevBmark.execStep == 'both':
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
        if self.execStep == 'cal':
            shutil.move(self.calScript, '..')
        if self.execStep == 'im':
            shutil.move(self.imageScript, '..')
        if self.execStep == 'both':
            shutil.move(self.calScript, '..')
            shutil.move(self.imageScript, '..')

        #empty out the current reduction directory
        os.chdir(self.currentLogDir)
        shutil.rmtree(self.currentRedDir)
        os.mkdir(self.currentRedDir)

        #move scripts back
        os.chdir(self.currentRedDir)
        if self.execStep == 'cal':
            shutil.move('../' + os.path.basename(self.calScript), '.')
        if self.execStep == 'im':
            shutil.move('../' + os.path.basename(self.imageScript), '.')
        if self.execStep == 'both':
            shutil.move('../' + os.path.basename(self.calScript), '.')
            shutil.move('../' + os.path.basename(self.imageScript), '.')
        os.chdir(oldPWD)

        #change path attributes based on emptying directory
        if self.execStep == 'cal':
            self.calScriptLog = self.currentLogDir + \
                                os.path.basename(self.calScriptLog)
            self.imageScriptLog = ''
            self.calScriptExpect = self.currentLogDir + \
                                   os.path.basename(self.calScriptExpect)
            self.imageScriptExpect = ''
            self.calBenchOutFile = self.currentLogDir + \
                                   os.path.basename(self.calBenchOutFile)
            self.calBenchSumm = self.currentLogDir + \
                                os.path.basename(self.calBenchSumm)
            self.imageBenchOutFile = ''
            self.imageBenchSumm = ''
        if self.execStep == 'im':
            self.calScriptLog = ''
            self.imageScriptLog = self.currentLogDir + \
                                  os.path.basename(self.imageScriptLog)
            self.calScriptExpect = ''
            self.imageScriptExpect = self.currentLogDir + \
                                     os.path.basename(self.imageScriptExpect)
            self.calBenchOutFile = ''
            self.calBenchSumm = ''
            self.imageBenchOutFile = self.currentLogDir + \
                                     os.path.basename(self.imageBenchOutFile)
            self.imageBenchSumm = self.currentLogDir + \
                                  os.path.basename(self.imageBenchSumm)
        if self.execStep == 'both':
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
