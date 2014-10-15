#import Python modules
import os
import sys
import shutil
import time
from optparse import OptionParser

#import non-standard library Python modules
import extractCASAscript

#-I want to make the "logging to file" thing actually say in the output file
# what the date and time is coming from
#-should make the calibrationURL and imagingURL behavior reflect the fact that
# extractCASAscript.py can take local Python files there too
#-I should make all the multi-line print statements indented after method name
# is printed

class benchmark:
    '''
    list of methods:
      -__init__
      -removePreviousRun
      -downloadData
      -extractData
      -makeExtractOpts --- this should be private, if I keep it at all
      -runScriptExtractor --- this should probably be split into cal and imaging
      -runGuideScript --- should also have switch for cal and imaging
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
      -benchOutFile
      -benchSumm
    '''
    #I want to have a set order for the attributes being initialized, group them
    #in some way or have a particular order that I could continue if I were to
    #add more later on for example
    def __init__(self, workDir='./', calibrationURL='', imagingURL='', \
                 dataPath='', outFile='', skipDownload=False):
        fullFuncName = __name__ + '::__init__'

        self.calScript = ''
        self.calScriptLog = ''
        self.imageScript = ''
        self.imageScriptLog = ''
        self.benchOutFile = ''
        self.benchSumm = ''
        #initialize the working directory
        if not os.path.isdir(workDir):
            print fullFuncName + ': ' + \
                  'Working directory does not exist.'
            return
        if workDir[-1] != '/': workDir += '/'
        self.workDir = workDir
        self.outString = ''
        self.extractLog = workDir + 'extractCASAscript.py.log'
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
            self.outFile = outFile
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
    def removePreviousRun(self):
        fullFuncName = __name__ + '::removePreviousRun'

        print fullFuncName + ': ' + \
              'Removing preexisting data.'
        shutil.rmtree(self.previousDir)
    def downloadData(self):
        fullFuncName = __name__ + '::downloadData'

        #wget the data
        print fullFuncName + ': ' + \
              'Acquiring data by HTTP.\nLogging to', self.outFile + '.'
        self.outString += time.strftime('%a %b %d %H:%M:%S %Z %Y') + '\n'
        procT = time.clock()
        wallT = time.time()
        os.system('wget -q --no-check-certificate ' + self.dataPath)
        wallT = round(time.time() - wallT, 2)
        procT = round(time.clock() - procT, 2)
        self.outString += str(wallT) + 'wall ' + str(procT) + 'CPU\n'
        self.localTar = os.getcwd() + '/' + self.dataPath.split('/')[-1]

    def extractData(self):
        fullFuncName = __name__ + '::extractData'

        #untar the raw data
        print fullFuncName + ': ' + \
              'Extracting data.\nLogging to ', self.outFile + '.'
        self.outString += time.strftime('%a %b %d %H:%M:%S %Z %Y') + '\n'
        procT = time.clock()
        wallT = time.time()
        os.system('tar -x -z -f ' + self.localTar)
        wallT = round(time.time() - wallT, 2)
        procT = round(time.clock() - procT, 2)
        self.outString += str(wallT) + 'wall ' + str(procT) + 'CPU\n'

    def makeExtractOpts(self):
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

        #store the script name(s) in the object
        scripts = list()
        f = open(self.extractLog, 'r')
        for line in f:
            if 'New file' in line:
                scripts.append(line.split(' ')[2])
        f.close()
        if 'Calibration' in  scripts[0]:
            self.calScript = self.workDir + scripts[0]
            self.imageScript = self.workDir + scripts[1]
        else:
            self.calScript = self.workDir + scripts[1]
            self.imageScript = self.workDir + scripts[0]

        #store the log name(s) in the object
        self.calScriptLog = self.calScript + '.log'
        self.imageScriptLog = self.imageScript + '.log'
        self.benchOutFile = self.calScript[:-3] + '.benchmark.txt'
        self.benchSumm = self.benchOutFile + '.summary'

    def runGuideScript(self):
        fullFuncName = __name__ + '::runGuideScript'

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
        f1 = open('../' + self.benchSumm.split('/')[-1], 'a')
        f2 = open(self.benchSumm, 'r')
        f1.write('\n')
        f1.write(f2.read())
        f1.close()
        f2.close()
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
        f1 = open('../' + self.benchSumm.split('/')[-1], 'a')
        f2 = open(self.benchSumm, 'r')
        f1.write('\n')
        f1.write(f2.read())
        f1.close()
        f2.close()
        print fullFuncName + ':' + \
              'Finished test of ' + self.imageScript
        sys.stdout = stdOut
        sys.stderr = stdErr
