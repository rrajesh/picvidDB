import sqlite3 as lite
class DBTester():
    """description of class"""
    def __init__(self,fileName,debugLevel=0):
        self._debugLevel = debugLevel
        self._fileName = fileName
        self._con = None
        self._cursor = None
        self._all_table_map = {}

    def Init(self):
        self._con = lite.connect(fileName)
        self._cursor = self._con.cursor()
        self._cursor.execute("""select name,sql from sqlite_master where TYPE='table'""")
        cur_out_all = self._cursor.fetchall()
        for item in cur_out_all:
            print "table name %s"%(item[0])
            column_list_string = item[1].split("(")[1].split(")")[0]
            column_list = column_list_string.split(",")
            column_map = {}
            for citem in column_list:
                splitList = citem.split(" ")
                key = splitList[0]
                val = splitList[1]
                key,val = citem.split(" ")
                column_map[key] = val

            self._all_table_map[item[0]] = column_map

    def Finalize(self):
        self._con.commit()
        self._con.close()

    def allTableNames(self):
        return self._all_table_map.keys()

    def hasTable(self,tableName):
        if self._all_table_map.has_key(tableName):
            return 1
        return 0 


    def getTableColumnNames(self,tableName):
        if not self._all_table_map.has_key(tableName):
            print "table %s is not present in DB\n"%(tableName)
            return None
        return self._all_table_map[tableName].keys()

    def AddTextColumn(self,tableName,columnName):
        if not self._all_table_map.has_key(tableName):
            print "ERROR table %s not found\n"%(tableName)
            return
        if self._all_table_map[tableName].has_key(columnName):
            if (self._debugLevel > 0):
                print "column already present..ignore..."
        else:
            try:
                sqlCmd = """ALTER TABLE {0} add {1} TEXT""".format(tableName,columnName)
                if self._debugLevel > 0:
                    print "sqlCmd %s\n"%(sqlCmd)
                self._cursor.execute(sqlCmd)
            except sqlite3.Error, e:
                print "Error %s:" % e.args[0]
                self._con.rollback()

######################################################################################
# main routine
######################################################################################

if __name__ == "__main__":
    fileName = r"D:\pictures_sqlite_python\code\DirProcessor.py\DirProcessor.py\test2.db"
    debugLevel = 1
    myTester = DBTester(fileName,debugLevel)
    myTester.Init()
    tNames = myTester.allTableNames()
    for tname in tNames:
        print "table name: %s\n" %(tname)
        print "table cols : "
        print myTester.getTableColumnNames(tname)
        print "\n\n"
    tableName = "ImagesExif2012"
    columnName = "Hello"
    myTester.AddTextColumn(tableName,columnName)
    columnName = "world"
    myTester.AddTextColumn(tableName,columnName)

    myTester.Finalize()