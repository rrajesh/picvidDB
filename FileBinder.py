from FileMetaData import FileMetaData

class FileBinder():
    """ This Class has a collection of FileMetaData objects
        The class also provides methods to add additional 
        FileMetadata objects
        The FileMetaDataObjects are also arranged as 
        map<year,set<FileMetaData>>
        """

    def __init__(self,debugLevel = 0):
        self.__files = []
        self.__yearMap = {}
        self.__fileType = {}
        self.__yearlyFiles = {}
        self.__debugLevel = debugLevel
        #should this be photoExifTags or just ExifTags ?
        self.__fileTags = set()# file & exif tags & riff

    def AddFileUsingExifToolMetaData(self,exifMD):
        currMD = FileMetaData(exifMD,self.__debugLevel)
        currMD.initialize()
        self.__files.append(currMD)
        tp = currMD.exif_tags_types()
        if tp:
            for exif_tag in tp:
                self.__fileTags.add(exif_tag)
        tp = currMD.file_tags_types()
        if tp:
            for file_tag in tp:
                self.__fileTags.add(file_tag)
        tp = currMD.riff_tags_types()
        if tp:
            for file_tag in tp:
                self.__fileTags.add(file_tag)
        year = None        
        dateTaken = currMD.DateTaken()
        if dateTaken:
            yearString = dateTaken.split()[0]
            year = yearString.split(":")[0]
            if (self.__debugLevel > 1):
                print 'year full %s y: %s'%(yearString,year)

            if (self.__yearMap.has_key(year)):
                self.__yearMap[year] = self.__yearMap[year] + 1
            else:
                self.__yearMap[year] = 0
            if (self.__yearlyFiles.has_key(year)):
                self.__yearlyFiles[year].append(currMD)
            else:
                myList = []
                myList.append(currMD)
                self.__yearlyFiles[year] = myList
        else:
            if (self.__debugLevel > 1):
                print "cannot find date for\n"
                print currMD.meta_map

        if (self.__debugLevel > 2):
            print 'fileName: %s dir: %s' %(currMD.FileName(),currMD.Directory())


    def GetMDfilesByYear(self,inpYear):
        if self.__yearlyFiles.has_key(inpYear):
            return self.__yearlyFiles[inpYear]
        return None

    def GetYears(self):
        return self.__yearlyFiles.keys()
    
    def GetFilesForYear(self,year):
        if (self.__yearlyFiles.has_key(year)):
            return self.__yearlyFiles[year]
        return None

    def GetFileTags(self):
        return self.__fileTags

    def dump(self):
        print "dump of FileBinder\n"
        for v in self.__files:
            v.dump()
