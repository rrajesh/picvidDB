

class FileMetaData():
    """ simple class to hold metadata of a picture/video file 
        taken with a camera
        """
    def __init__(self,metadata_map,debugLevel = 0):
        self.exifTags = {}
        self.fileTags = {}
        self.makerNotesTags = {}
        self.riffTags = {}
        self.miscTags = {}
        self.meta_map = metadata_map
        self.__debugLevel = debugLevel
        if self.__debugLevel > 1:
            print "meta_map"
            print self.meta_map

    def initialize(self):
        for key,value in self.meta_map.items():
            if key[:5].upper() == "EXIF:":
                self.exifTags[key[5:]] = value
            elif key[:5].upper() == "FILE:":
                self.fileTags[key[5:]] = value
            elif key[:11].upper() == "MAKERNOTES:":
                self.makerNotesTags[key[11:]] = value
            elif key[:5].upper() == "RIFF:":
                self.riffTags[key[5:]] = value
            else:
                self.miscTags[key] = value
    

    def exif_tags(self):
        return self.exifTags

    def exif_tags_types(self):
        return self.exifTags.keys()

    def file_tags(self):
        return self.fileTags
    
    def file_tags_types(self):
        return self.fileTags.keys()

    def riff_tags(self):
        return self.riffTags

    def riff_tags_types(self):
        return self.riffTags.keys()

    def FileName(self):
        try:
            return self.fileTags['FileName']
        except:
            print "cannot find fileName\n"
            print "fileTags:\n"
            print fileTags

    def Directory(self):
        return self.fileTags['Directory']

    def FileType(self):
        return self.fileTags['MimeType']

    def DateTaken(self):
        try:
            if self.exifTags.has_key('DateTimeOriginal'):
                return self.exifTags['DateTimeOriginal']
            # video files have RIFF tag for time taken
            elif self.riffTags.has_key('DateTimeOriginal'):
                return self.riffTags['DateTimeOriginal']
            else :
                print "cannot find exifTag:DateTimeOriginal"
                print "exif_map:\n"
                print self.exifTags
                print "meta_map\n"
                print self.meta_map
        except AttributeError:
            print "ERROR..."                        
        return None

    def dump(self):
        print "dump tags recovered using exiftool\n"
        for k,v in self.exifTags.items():
            print "exif : %s = %s\n"%(k,v)
        for k,v in self.fileTags.items():
            print "file : %s = %s\n"%(k,v)
        for k,v in self.riffTags.items():
            print "file : %s = %s\n"%(k,v)
        for k,v in self.makerNotesTags.items():
            print "makerNotes : %s = %s\n"%(k,v)
        for k,v in self.miscTags.items():
            print "misc : %s = %s\n"%(k,v)

