import os
class DirProcessor:
    """ Simple Class that processes a rootPath and builds up 
    a list of files that need to be processed"""
    def __init__(self,debugLevel=0):
        self.__rootPaths = []
        self._debugLevel = debugLevel
        self.__fileList = []
        self.__jpgList = []
        self.__aviList = []
        self.__mpgList = []
        self.__ignoreList = []

    def addRootPath(self,rootPath):
        self.__rootPaths.append(rootPath)

    def process(self):
        self.__ignoreList.append("$RECYCLE.BIN")
        [self.processFiles(x) for x in self.__rootPaths]
        
    def my_simple_walk(self,rootPath):
        files = []
        for dirname, dirnames, filenames in os.walk(dirpath):
            files += [os.path.join(dirname, filename) for filename in filenames]
        return files

    def my_walk(self,rootPath):
        for dirpath, dirnames, filenames in os.walk(rootPath):
            dirnames[:] = [ dn for dn in dirnames
                           if dn not in self.__ignoreList ]
            if self._debugLevel > 1:
                print "dirnames %s" %dirnames
            yield dirpath, dirnames, filenames

    def processFiles(self,rootPath):
        count = 0
        mygenerator = self.my_walk(rootPath)
        for dirpath,dirnames,filenames in self.my_walk(rootPath):
            if self._debugLevel > 1:
                print "dirPath: %s" %dirpath
                print "fileNames\n"
                print filenames
            #currPath = os.path.join(self._rootPath,dirPath)
            #print "currPath: %s" %currPath
            for currDirName in dirnames:
                if self._debugLevel > 1:
                    print "currDir %s" %currDirName
                if currDirName == "$RECYCLE.BIN":
                    continue
                myPath = os.path.join(dirpath,currDirName)
                if self._debugLevel > 1:
                    print "myPath %s" %myPath                
            for f in filenames:
                currFileName = os.path.join(dirpath,f)
                absPathName = os.path.abspath(currFileName)
                if self._debugLevel > 1:
                    print "absPathName: %s ext: %s" %(absPathName,os.path.splitext(currFileName))
                self.__fileList.append(absPathName)
                fileExt = os.path.splitext(currFileName)[1]
                if (fileExt.lower() == ".jpg"):
                    self.__jpgList.append(absPathName)
                elif (fileExt.lower() == ".avi"):
                    self.__aviList.append(absPathName)
                elif (fileExt.lower() == ".mpg"):
                    self.__mpgList.append(absPathName)

                    #self.__absFileList.append(os.path.abspath(currFileName))
                    count = count + 1
                    #if ( count == maxcount ):
                    #    return
        return

    def getFiles(self,begin,end):
        if begin > end:
            return None
        if begin < 0 or begin > self.__fileList.count:
            return None
        if end < 0 or end > self.__fileList.count:
            return None
        return self.__fileList[begin:end]

    def getJpgFiles(self,begin=None,end=None):
        try:
            return self.__jpgList[begin:end]
        except:
            "unexpected error in getjpgFiles"

    def getAviFiles(self,begin=None,end=None):
        try:
            return self.__aviList[begin:end]
        except:
            "unexpected error in getAviFiles"

    def getMpgFiles(self,begin=None,end=None):
        try:
            if ( end == None and begin == None):
                return self.__mpgList
            return self.__mpgList[begin:end]
        except:
            "unexpected error in getMpgFiles"

import sys

######################################################################################
# main routine
######################################################################################

if __name__ == "__main__":
    myDirProc = DirProcessor("j:")
    myDirProc.process()
    #top10Files = myDirProc.getFiles(0,10)
    #print top10Files
    top10AviFiles = myDirProc.getAviFiles(0,10)
    print top10AviFiles
    jpgFiles = myDirProc.getJpgFiles()
    print jpgFiles
    mpgFiles = myDirProc.getMpgFiles(0,10)
    print mpgFiles
    sys.stdin.read(1)
      
