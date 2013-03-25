import sqlite3

class SqlCreateTableCmd(): 
    """ utility class to construct a SQL cmd to create a TABLE """
    def __init__(self,dbh,debugLevel=0):
        self._debugLevel = debugLevel
        self._dbh = dbh
        self._cmd = ""
        self._tableName = ""
        self._colNames = []
        self._sqlCmd = ""

    def initialize(self,tableName,argSet):
        self._tableName = tableName
        self._colNames = list(argSet)
        #append TEXT spec for the last column
        self._sqlCmd = '''CREATE TABLE {0} ({1} TEXT) '''.format(self._tableName,
               (' TEXT,'.join(self._colNames)))

    def RunCmd(self):
        if (self._debugLevel > 0):
            print "sqlCreateTableCmd::RunCmd %s\n"%(self._sqlCmd)
        #probe if we have the table already...
        if self._dbh.hasTable(self._tableName):
            if self._debugLevel > 0:
                print "table %s already present\n"%(self._tableName)
            existingColMap = self._dbh.getTableColumnMap(self._tableName)
            for colName in self._colNames:
                if not existingColMap.has_key(colName):
                    if self._debugLevel > 0:
                        print "table %s is missing new column %s"%(self._tableName,colName)
            return
        self._dbh.ExecuteCmd(self._sqlCmd)
        self._dbh.Commit()


