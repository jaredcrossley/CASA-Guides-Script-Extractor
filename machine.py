import os
import sys
import socket
import platform

#import non-standard Python modules
import benchmark
import parameters

#-I need to figure out if the downloading and untarring is something that we want
# to be timing. If not then I can make it so the loop only downloads (and
# untars?) things once rather than for each benchmark.
#-need to decide where to save the machine information (e.g. txt file somewhere)
#-the sharing and passing around of variables is really a mess between the
# benchmark and machine classes right now
#-need to include check for trying to use dataURL when it is set to None in the
# parameters dictionary
#-need to check that running version of CASA matches the data set name given

class machine:
    """A class associated with a single computer and all of
    the benchmarking done on it.

    Attributes
    ----------

    CASAglobals : dict
        Dictionary returned by Python globals() function within the CASA
        namespace (environment). Simply pass the return value of the globals()
        function from within CASA where this class should be instantiated
        within.

    hostName : str
        Name of the computer this class is associated with.

    os : str
        Description of underlying platform associated to hostName.

    lustreAccess : bool
        Determines whether this computer has access to the /lustre/naasc/
        filesystem (it is hard-coded to simply check for the existence of that
        directory).

    pythonVersion : str
        major.minor.patchlevel version number for currently running Python.

    casaVersion : str
        Version number for currently running CASA.

    casaRevision : str
        Revision number for currently running CASA.

    dataSets : list
        List of strings containing names of data sets to be benchmarked. Names
        must match the dictionary variable names in parameters.py.

    jobs: dict
        Container for each benchmark instance to be run on this machine along
        with information on whether to download the raw data and number of
        benchmarking iterations desired.

    workDir : str

    Methods
    -------

    __init__
        Initializes machine instance attributes.

    runBenchmarks

    prepareBenchmark
        Creates a benchmark object and sets up the directories and data.

    executeBenchmark
        Runs the benchmark calibration and imaging stages.
    """

    def __init__(self, CASAglobals=None, scriptDir='', dataSets=list(), \
                 nIters=list(), skipDownloads=list(), workDir='./'):
        #for telling where printed messages originate from
        fullFuncName = __name__ + '::__init__'
        indent = len(fullFuncName) + 2

        #check that we have CASA globals
        if not CASAglobals:
            raise ValueError('Value returned by globals() function in ' + \
                             'CASA environment must be given.')
        self.CASAglobals = CASAglobals

        #gather details of computer and installed packages
        self.hostName = socket.gethostname()
        self.os = platform.platform()
        self.lustreAccess = os.path.isdir('/lustre/naasc/')
        self.pythonVersion = platform.python_version()
        self.casaVersion = self.CASAglobals['casadef'].casa_version
        self.casaRevision = self.CASAglobals['casadef'].subversion_revision

        #add script directory to Python path if need be
        if scriptDir == '':
            raise ValueError('Path to benchmarking scripts must be given.')
        scriptDir = os.path.abspath(scriptDir) + '/'
        self.scriptDir = scriptDir
        if scriptDir not in sys.path:
            sys.path.append(self.scriptDir)

        #store which data sets will be benchmarked
        if len(dataSets) == 0:
            raise ValueError('At least one data set must be specified for ' + \
                             'benchmarking.')
        for dataSet in dataSets:
            if not hasattr(parameters, dataSet):
                raise ValueError("Data set name '" + dataSet + \
                                 "' not recognized.")
        self.dataSets = dataSets
        self.jobs = dict()
        for dataSet in self.dataSets:
            self.jobs[dataSet] = dict()
            self.jobs[dataSet]['benchmarks'] = list()
        if len(nIters) != len(dataSets):
            raise ValueError('nIters integer list must be of same length ' + \
                             'as dataSets list.')
        if len(skipDownloads) != len(dataSets):
            raise ValueError('skipDownloads boolean list must be of same ' + \
                             'length as dataSets list.')
        index = 0
        for dataSet in self.dataSets:
            if type(nIters[index]) != int:
                raise TypeError('nIters must be a list of all integers.')
            if type(skipDownloads[index]) != bool:
                raise ValueError('skipDownloads must be a list of all booleans.')
            self.jobs[dataSet]['niters'] = nIters[index]
            self.jobs[dataSet]['skipDownload'] = skipDownloads[index]
            index += 1

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


    def runBenchmarks(self):
        #for telling where printed messages originate from
        fullFuncName = __name__ + '::runBenchmarks'
        indent = len(fullFuncName) + 2

        for dataSet in self.dataSets:
            dataSetDir = self.workDir + dataSet + '/'
            if not os.path.isdir(dataSetDir):
                os.mkdir(dataSetDir)
            params = getattr(parameters, dataSet)
            if self.jobs[dataSet]['skipDownload']:
                dataPath = params['dataPath']
            else:
                dataPath = params['dataURL']
            for i in range(self.jobs[dataSet]['nIters']):
                self.jobs[dataSet]['benchmarks'].append(
                    benchmark.benchmark(CASAglobals=self.CASAglobals,
                                        workDir=dataSetDir,
                                        calibrationURL=params['calibrationURL'],
                                        imagingURL=params['imagingURL'],
                                        dataPath=dataPath,
                                        outFile=outFile,
                                        skipDownload=self.jobs[dataSet]['skipDownload']))
                self.jobs[dataSet]['benchmarks'][i].createDirTree()
                self.jobs[dataSet]['benchmarks'][i].removePreviousRun()
                if not self.jobs[dataSet]['skipDownload']:
                    self.jobs[dataSet]['benchmarks'][i].downloadData()
                self.jobs[dataSet]['benchmarks'][i].extractData()
                self.jobs[dataSet]['benchmarks'][i].runScriptExtractor()
                self.jobs[dataSet]['benchmarks'][i].runGuideScript()
                self.jobs[dataSet]['benchmarks'][i].writeOutFile()


    def createBenchmark(self, CASAglobals, workDir, calibrationURL, imagingURL, \
                        dataPath, outFile, skipDownload):
        #for telling where printed messages originate from
        fullFuncName = __name__ + '::createBenchmark'
        indent = len(fullFuncName) + 2

        x = benchmark.benchmark(CASAglobals=CASAglobals, workDir=workDir, \
                                calibrationURL=calibrationURL, \
                                imagingURL=imagingURL, dataPath=dataPath, \
                                outFile=outFile, skipDownload=skipDownload)
        x.createDirTree()
        x.removePreviousRun()
        if not skipDownload:
            x.downloadData()
        x.extractData()
        x.runScriptExtractor()


    def executeBenchmark(self):
        #for telling where printed messages originate from
        fullFuncName = __name__ + '::executeBenchmark'
        indent = len(fullFuncName) + 2
