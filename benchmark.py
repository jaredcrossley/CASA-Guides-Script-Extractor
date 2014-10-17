#import Python modules
import os
import sys
import shutil
import time
from optparse import OptionParser
import socket
import tarfile

#import CASA modules
from taskinit import *
import casadef
from listobs_cli import listobs_cli as listobs
from gencal_cli import gencal_cli as gencal
from wvrgcal_cli import wvrgcal_cli as wvrgcal
from flagdata_cli import flagdata_cli as flagdata
from flagmanager_cli import flagmanager_cli as flagmanager
from applycal_cli import applycal_cli as applycal
from split_cli import split_cli as split
from concat_cli import concat_cli as concat
from fixplanets_cli import fixplanets_cli as fixplanets
from gaincal_cli import gaincal_cli as gaincal
from plotcal_cli import plotcal_cli as plotcal
from bandpass_cli import bandpass_cli as bandpass
from setjy_cli import setjy_cli as setjy
from fluxscale_cli import fluxscale_cli as fluxscale
from delmod_cli import delmod_cli as delmod
from imview_cli import imview_cli as imview
from clean_cli import clean_cli as clean

#import non-standard library Python modules
import extractCASAscript

#-I want to make the "logging to file" thing actually say in the output file
# what the date and time is coming from
#-should make the calibrationURL and imagingURL behavior reflect the fact that
# extractCASAscript.py can take local Python files there too
#-I should make all the multi-line print statements indented after method name
# is printed
#-I need to get the correct behavior when something doesn't exist etc. instead
# of just returning
#-all methods should probably return something
#-alphabetize the CASA modules
#-think of a way to automate importing CASA modules needed, maybe based on the
# scripts generated or just on tasklist
#-think about putting CASA module imports into a separate file just for
# appearances

class benchmark:
    '''
    list of methods:
      -__init__
      -createDirTree
      -removePreviousRun
      -downloadData
      -extractData
      -makeExtractOpts --- this should be private, if I keep it at all
      -runScriptExtractor --- this should probably be split into cal and imaging
      -runGuideScript --- should also have switch for cal and imaging
      -writeOutFile
    list of attributes:
      -workDir
      -calibrationURL
      -imagingURL
      -outString
      -dataPath
      -outFile
      -skipDownload
      -previousDir
      -localTar
      -extractLog
      -calScript
      -calScriptLog
      -imageScript
      -imageScriptLog
      -calBenchOutFile
      -imageBenchOutFile
      -calBenchSumm
      -imageBenchSumm
      -currentWorkDir
      -currentLogDir
      -currentTarDir
      -currentRedDir
      -allLogDir
    '''
    #I want to have a set order for the attributes being initialized, group them
    #in some way or have a particular order that I could continue if I were to
    #add more later on for example
    def __init__(self, scriptDir='',workDir='./', calibrationURL='', \
                 imagingURL='', dataPath='', outFile='', skipDownload=False):
        fullFuncName = __name__ + '::__init__'

        self.calScript = ''
        self.calScriptLog = ''
        self.imageScript = ''
        self.imageScriptLog = ''
        self.calBenchOutFile = ''
        self.imageBenchOutFile = ''
        self.calBenchSumm = ''
        self.imageBenchSumm = ''
        #add script directory to Python path if need be
        if scriptDir == '':
            print fullFuncName + ': ' + \
                  'Path to benchmarking scripts must be given.'
            return
        else:
            scriptDir = os.path.abspath(scriptDir) + '/'
            if scriptDir not in sys.path:
                sys.path.append(scriptDir)
        #initialize the working directory
        if not os.path.isdir(workDir):
            print fullFuncName + ': ' + \
                  'Working directory does not exist.'
            return
        if workDir == './': workDir = os.getcwd()
        if workDir[-1] != '/': workDir += '/'
        self.workDir = workDir
        self.currentWorkDir = self.workDir + \
                              time.strftime('%Y_%m_%dT%H_%M_%S') + '-' + \
                              socket.gethostname() + '/'
        self.currentLogDir = self.currentWorkDir + 'log_files/'
        self.currentTarDir = self.currentWorkDir + 'tarballs/'
        self.currentRedDir = ''
        self.allLogDir = self.workDir + 'all_logs/'
        self.outString = ''
        self.extractLog = self.currentLogDir + 'extractCASAscript.py.log'
        #check we were given URLs to the calibration and image guides
        if calibrationURL == '':
            print fullFuncName + ': ' + \
                  'URL to calibration CASA guide must be given.'
            return
        else:
            self.calibrationURL = calibrationURL
        if imagingURL == '':
            print fullFuncName + ': ' + \
                'URL to imaging CASA guide must be given.'
            return
        else:
            self.imagingURL = imagingURL
        #check we were given a URL or path to the data
        if dataPath == '':
            print fullFuncName + ': ' + \
                  'A URL or path must be given to the raw data.'
            return
        else:
            self.dataPath = dataPath
        #check we were given an output file
        if outFile == '':
            print fullFuncName + ': ' + \
                  'A file must be specified for the output of the script.'
            return
        else:
            self.outFile = self.currentLogDir + outFile
        self.skipDownload = skipDownload
        #check that the tarball does exist if not downloading it
        if self.skipDownload == True:
            if not os.path.isfile(self.dataPath):
                print fullFuncName + ': ' + \
                      'Cannot find tarball for extraction:' + \
                      os.path.basename(self.dataPath)
                print fullFuncName + ': ' + \
                      'Download may be required.'
                return
            else:
                print fullFuncName + ': ' + \
                      'Data available by filesystem.'
                self.localTar = self.dataPath
        #check dataPath is a URL if we will be downloading data
        else:
            self.localTar = ''
            if self.dataPath[0:4] != 'http':
                print fullFuncName + ': ' + \
                      'A valid URL must be specified to download the data.'
                return
        #check current directory for previous run
        prevDir = self.dataPath.split('/')[-1].split('.tgz')[0]
        if os.path.isdir(prevDir):
            self.previousDir = os.path.abspath(prevDir)
        else:
            self.previousDir = ''

    def createDirTree(self):
        fullFuncName = __name__ + '::createDirTree'

        #check if directories already exist
        if os.path.isdir(self.currentWorkDir) or \
           os.path.isdir(self.currentLogDir) or \
           os.path.isdir(self.currentTarDir):
            print fullFuncName + ': ' + \
                  'Current benchmark directories already exist.'
            return

        #make directories specific to a benchmark instance
        os.mkdir(self.currentWorkDir)
        os.mkdir(self.currentLogDir)
        if not self.skipDownload:
            os.mkdir(self.currentTarDir)

        #check if all_logs needs to be made
        if not os.path.isdir(self.allLogDir):
            os.mkdir(self.allLogDir)

    def removePreviousRun(self):
        fullFuncName = __name__ + '::removePreviousRun'

        print fullFuncName + ': ' + \
              'Removing preexisting data.'
        shutil.rmtree(self.previousDir)

    def downloadData(self):
        fullFuncName = __name__ + '::downloadData'

        command = 'wget -q --no-check-certificate --directory-prefix=' + \
                  self.currentTarDir + ' ' + self.dataPath

        #wget the data
        print fullFuncName + ': ' + \
              'Acquiring data by HTTP.\nLogging to', self.outFile + '.'
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
        fullFuncName = __name__ + '::extractData'

        command = "tar = tarfile.open('" + self.localTar + \
                  "')\ntar.extractall(path='" + self.currentWorkDir + \
                  "')\ntar.close()"

        #untar the raw data
        print fullFuncName + ': ' + \
              'Extracting data.\nLogging to', self.outFile + '.'
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
        fullFuncName = __name__ + '::makeExtractOpts'
        
        usage = \
            """ %prog [options] URL
                *URL* should point to a CASA Guide webpage or to a Python
                script. *URL* can also be a local file system path."""
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
        fullFuncName = __name__ + '::runScriptExtractor'

        #remember where we were and change to reduction directory
        oldPWD = os.getcwd()
        os.chdir(self.currentRedDir)

        #do the script extraction
        print fullFuncName + ':' + \
              'Extracting CASA Guide.\nLogging to ' + self.extractLog
        stdOut = sys.stdout
        stdErr = sys.stderr
        sys.stdout = open(self.extractLog, 'w')
        sys.stderr = sys.stdout
        extractCASAscript.main(self.calibrationURL, self.makeExtractOpts())
        print '---'
        extractCASAscript.main(self.imagingURL, self.makeExtractOpts())
        sys.stdout.close()
        sys.stdout = stdOut
        sys.stderr = stdErr

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
        self.calScriptLog = self.calScript + '.log'
        self.imageScriptLog = self.imageScript + '.log'
        self.calBenchOutFile = self.calScript[:-3] + '.benchmark.txt'
        self.imageBenchOutFile = self.imageScript[:-3] + '.benchmark.txt'
        self.calBenchSumm = self.calBenchOutFile + '.summary'
        self.imageBenchSumm = self.imageBenchOutFile + '.summary'

    def runGuideScript(self):
        fullFuncName = __name__ + '::runGuideScript'

        #remember where we were and change to reduction directory
        oldPWD = os.getcwd()
        os.chdir(self.currentRedDir)

        #run calibration script
        print fullFuncName + ':' + \
              'Beginning benchmark test of ' + self.calScript + '.\n' + \
              'Logging to ' + self.calScriptLog
        stdOut = sys.stdout
        stdErr = sys.stderr
        sys.stdout = open(self.calScriptLog, 'w')
        sys.stderr = sys.stdout
        execfile(self.calScript)
        sys.stdout.close()
        #I'm not sure what the old code was trying to do and how to fit it into
        #the new directory structuring
#        f1 = open('../' + self.calBenchSumm.split('/')[-1], 'a')
#        f2 = open(self.calBenchSumm, 'r')
#        f1.write('\n')
#        f1.write(f2.read())
#        f1.close()
#        f2.close()
        print fullFuncName + ':' + \
              'Finished test of ' + self.calScript

        #run imaging script
        print fullFuncName + ':' + \
              'Beginning benchmark test of ' + self.imageScript + '.\n' + \
              'Logging to ' + self.imageScriptLog
        sys.stdout = open(self.imageScriptLog, 'w')
        sys.stderr = sys.stdout
        execfile(self.imageScript)
        sys.stdout.close()
        #I'm not sure what the old code was trying to do and how to fit it into
        #the new directory structuring
#        f1 = open('../' + self.imageBenchSumm.split('/')[-1], 'a')
#        f2 = open(self.imageBenchSumm, 'r')
#        f1.write('\n')
#        f1.write(f2.read())
#        f1.close()
#        f2.close()
        print fullFuncName + ':' + \
              'Finished test of ' + self.imageScript
        sys.stdout = stdOut
        sys.stderr = stdErr

        #change directory back to wherever we started from
        os.chdir(oldPWD)

    def writeOutFile(self):
        fullFuncName = __name__ + '::writeOutFile'
        
        f = open(self.outFile, 'w')
        f.write(self.outString)
        f.close()
