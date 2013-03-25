from DirProcessor import DirProcessor
import exiftool
import sys
from DBHandler import DBHandler
from FileBinder import FileBinder
from FileMetaData import FileMetaData
from SqlCreateTableCmd import SqlCreateTableCmd
from SqlInsertTableCmd import SqlInsertTableCmd

class ExifProcessor:
    """ Utility class to instantiate the perl tool process
        and use it multiple times using exiftool.get_metadata_batch
        Destructor will clean up the perl process
        """
    def __init__(self,debugLevel=0):
        self.__et = exiftool.ExifTool(r"D:\photo_library\exiftool(-k).exe")
        self.__et.start()
        self.__debugLevel = debugLevel

    def get_metadata_batch(self,fileList):
        return self.__et.get_metadata_batch(fileList)

    def __del__(self):
        if self.__debugLevel > 1:
            print "terminating the exifTool class...\n"
        self.et.terminate()

######################################################################################
# utility functions
######################################################################################
def get_metadata(fileList):
    et= exiftool.ExifTool(r"D:\photo_library\exiftool(-k).exe")
    et.start()
    metadata_map = et.get_metadata_batch(fileList)
    et.terminate()
    return metadata_map

######################################################################################
# utility functions
######################################################################################
def load_meta_data_for_files(fileList,binder,exifprocessor,batch_size=10,debugLevel=0):
    numFiles = len(fileList)
    if debugLevel > 0:
        print "numFiles = %d\n"%(numFiles)
        print "batch_size = %d\n"%(batch_size)
    if (batch_size > numFiles):
        batch_size = numFiles
    counter = 0
    while True:
        beginPos = counter
        endPos = counter+batch_size
        if(endPos > numFiles):
            endPos = numFiles
        if debugLevel > 1:
            print "Processing %d to %d"%(beginPos,endPos)
        myList = fileList[beginPos:endPos]
        md_map = exifprocessor.get_metadata_batch(myList)
        for d in md_map:
            binder.AddFileUsingExifToolMetaData(d)
        counter = endPos
        if (counter >= numFiles):
            break
    if debugLevel > 1:
        print "completed load_meta_deta_for_files\n"

######################################################################################
# main routine
######################################################################################

if __name__ == "__main__":
    dbName = "test6.db"
    rootDir = r"J:\2005" #r"D:\pics_2002_2005"
    myDirProc = DirProcessor()
    myDirProc.addRootPath(rootDir)
    rootDir = r"J:\2006"
    myDirProc.addRootPath(rootDir)
    rootDir = r"J:\2007"
    myDirProc.addRootPath(rootDir)
    myDirProc.process()

    jpgFiles = myDirProc.getJpgFiles()
    aviFiles = myDirProc.getAviFiles()
    movFiles = myDirProc.getMpgFiles()
    myBinder = FileBinder()
    myExifProcessor = ExifProcessor()
    batch_size=30
    debug_level=1
    load_meta_data_for_files(jpgFiles,myBinder,myExifProcessor,batch_size,debug_level)
    load_meta_data_for_files(aviFiles,myBinder,myExifProcessor,batch_size,debug_level)


    print myBinder.GetYears()

    myDBH = DBHandler(dbName)
    myDBH.Init()

    photoTags = myBinder.GetFileTags()
    print "photoTags: %s\n"%(photoTags)


    for year in myBinder.GetYears():
        myYearList = myBinder.GetFilesForYear(year)
        print "processing for year %s"%(year)
        print "numFiles: %d"%(len(myYearList))
        tableName = "FileMetaData{0}".format(year)
        tableCreateCmd = SqlCreateTableCmd(myDBH,1)
        tableCreateCmd.initialize(tableName,photoTags)
        tableCreateCmd.RunCmd()
        tableInsertCmd = SqlInsertTableCmd(myDBH,1)
        for myFMD in myYearList:
            f_exif_tags = myFMD.exif_tags()
            f_file_tags = myFMD.file_tags()
            f_riff_tags = myFMD.riff_tags()
            tableInsertCmd.initialize(tableName,photoTags,f_exif_tags)
            tableInsertCmd.UpdateTags(f_file_tags)
            tableInsertCmd.UpdateTags(f_riff_tags)
            tableInsertCmd.RunCmd()
            tableInsertCmd = SqlInsertTableCmd(myDBH,1)

    myDBH.Commit()
    myDBH.Close()
