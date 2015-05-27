import sys

CASAglobals = globals()
scriptDir = '/lustre/naasc/nbrunett/bench_code_devel/' + \
            'CASA-Guides-Script-Extractor'
dataSets = ['x2012_1_00912_S_43', 'NGC3256Band3_43']
nIters = [2, 2]
skipDownloads = [True, False]
steps = ['both', 'im']
scriptsSources = ['disk', 'web']

#dataSets = ['AntennaeBand7_43', 'x2012_1_00912_S_43', 'NGC3256Band3_43']
#nIters = [2, 2, 2]
#skipDownloads = [False, True, False]
#steps = ['cal', 'both', 'im']
#scriptsSources = ['web', 'disk', 'web']
workDir = '/lustre/naasc/nbrunett/bench_code_devel/testing/' + \
          'test_remote_subprocess'
quiet = True

#add script directory to Python path if need be
scriptDir = os.path.abspath(scriptDir) + '/'
if scriptDir not in sys.path:
    sys.path.append(scriptDir)

import machine

cvpost = machine.machine(CASAglobals=CASAglobals,
                         scriptDir=scriptDir,
                         dataSets=dataSets,
                         nIters=nIters,
                         skipDownloads=skipDownloads,
                         steps=steps,
                         workDir=workDir,
                         scriptsSources=scriptsSources,
                         quiet=quiet)
cvpost.runBenchmarks(cleanUp=True)


'''
#this is NOT general! this script is just for my testing and should not be the
#final wrapper for ANYTHING! i will be so unhappy if that's what happens >:[
print '\n\n\n'
print "here's my preliminary report, very rudimentary"
files = list()
for i in range(nIters[0]):
    files.append(multivac.jobs[dataSets[0]]['benchmarks'][i].calBenchSumm)
report = machine.makeReport(files)
print 'data set   host name   avg time   std time   run times'
print '##Calibration:'
print multivac.dataSets[0], multivac.hostName, report[0], report[1], report[2]

files = list()
for i in range(nIters[0]):
    files.append(multivac.jobs[dataSets[0]]['benchmarks'][i].imageBenchSumm)
report = machine.makeReport(files)
print '##Imaging'
print multivac.dataSets[0], multivac.hostName, report[0], report[1], report[2]
'''
