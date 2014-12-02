import os
import sys
import socket
import platform

#import non-standard Python modules
import benchmark

#-I need to figure out if the downloading and untarring is something that we want
# to be timing. If not then I can make it so the loop only downloads (and
# untars?) things once rather than for each benchmark.
#-need to decide where to save the machine information (e.g. txt file somewhere)
#-the sharing and passing around of variables is really a mess between the
# benchmark and machine classes right now

class machine:
    """A class associated with a single computer and all of
    the benchmarking to be done on it.

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
        List of strings containing names of data sets to be benchmarked.

    benchmarks : dict
        Container for each benchmark instance to be run on this machine.

    nIters : int

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
                 nIters=None, workDir='./'):
        #for telling where printed messages originate from
        fullFuncName = __name__ + '::__init__'
        indent = len(fullFuncName)

        #check that we have CASA globals
        if not CASAglobals:
            raise ValueError('Value returned by globals() function in ' + \
                             'CASA environment must be given.')
        else:
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
        else:
            scriptDir = os.path.abspath(scriptDir) + '/'
            self.scriptDir = scriptDir
            if scriptDir not in sys.path:
                sys.path.append(self.scriptDir)

        #store which data sets will be benchmarked and how many times each
        if len(dataSets) == 0:
            raise ValueError('At least one data set must be specified for ' + \
                             'benchmarking.')
        else:
            self.dataSets = dataSets
            self.benchmarks = dict()
            for name in dataSets:
                self.benchmarks[name] = list()
        if type(nIters) != int:
            raise TypeError('The number of times each benchmark will be ' + \
                            'run must be specified and as an integer.')
        else:
            self.nIters = nIters

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


    def runBenchmarks(self, skipDownload):
        #for telling where printed messages originate from
        fullFuncName = __name__ + '::runBenchmarks'
        indent = len(fullFuncName)

        for dataSet in benchmarks:
            dataSetDir = self.workDir + dataSet + '/'
            if not os.path.isdir(dataSetDir):
                os.mkdir(dataSetDir)
            for i in range(self.nIters):
                self.benchmarks[name][i] = benchmark.benchmark(CASAglobals=self.CASAglobals, workDir=dataSetDir, calibrationURL=calibrationURL, imagingURL=imagingURL, dataPath=dataPath, outFile=outFile, skipDownload=skipDownload)
                self.benchmarks[name][i].createDirTree()
                self.benchmarks[name][i].removePreviousRun()
                if not skipDownload:
                    self.benchmarks[name][i].downloadData()
                self.benchmarks[name][i].extractData()
                self.benchmarks[name][i].runScriptExtractor()
                self.benchmarks[name][i].runGuideScript()
                self.benchmarks[name][i].writeOutFile()


    def createBenchmark(self, CASAglobals, workDir, calibrationURL, imagingURL, \
                        dataPath, outFile, skipDownload):
        #for telling where printed messages originate from
        fullFuncName = __name__ + '::createBenchmark'
        indent = len(fullFuncName)

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
        indent = len(fullFuncName)
