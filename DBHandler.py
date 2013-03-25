import DirProcessor
import sqlite3
import os

class DBHandler():
    """class to wrap around sqlite DB and provide 
       functionality to define tables and update rows"""

    def __init__(self,fileName,debugLevel=0):
        self._dbFileName = fileName
        self._conn = None
        self._cursor = None
        self._debugLevel = debugLevel
        self._primaryTableMap = {}

    def Init(self):
        """ initialize the sqlite database """
        self._conn = sqlite3.connect(self._dbFileName);
        self._cursor = self._conn.cursor()
        self._all_table_map = {}
        self._cursor.execute("""select name,sql from sqlite_master where TYPE='table'""")
        cur_out_all = self._cursor.fetchall()
        for item in cur_out_all:
            if self._debugLevel > 0:
                print "table name %s"%(item[0])
            column_list_string = item[1].split("(")[1].split(")")[0]
            column_list = column_list_string.split(",")
            column_map = {}
            for citem in column_list:
                key,val = citem.split(" ")
                column_map[key] = val

            self._all_table_map[item[0]] = column_map

    def hasTable(self,tableName):
        if self._all_table_map.has_key(tableName):
            return 1
        return 0 

    def getTableColumnMap(self,tableName):
        if not self._all_table_map.has_key(tableName):
            print "table %s is not present in DB\n"%(tableName)
            return None
        return self._all_table_map[tableName]


    def ExecuteCmd(self,stmt):
        try:
            if (stmt.find("msvideo") != -1):
                x=3
            self._cursor.execute(stmt)
        except sqlite3.Error, e:
            print "Error %s:" % e.args[0]
            self._conn.rollback()
    def Commit(self):
        self._conn.commit()

    def Close(self):
        self._conn.close();

######################################################################################
# main routine
######################################################################################

if __name__ == "__main__":
    myDBH = DBHandler("trial.db")
    myDBH.Init()
    myDBH.Commit()    
    myDBH.Close()