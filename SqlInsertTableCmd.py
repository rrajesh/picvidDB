class SqlInsertTableCmd():
    """ utility class to insert a row into an SQL TABLE 
        the constructor specifies a tagSet that are the possible
        column values in the TABLE
        """
    def __init__(self,dbh,debugLevel=0):
        self._debugLevel = debugLevel
        self._dbh = dbh
        self._cmd = ""
        self._tableName = ""
        self._sqlCmd = ""
        self._argList = []
        self._argValList = []
        self._tagSet = set()

    def initialize(self,tableName,tagSet,valueMap):
        self._tableName = tableName
        self._argList = []
        self._argValList = []
        valList = valueMap.keys()
        self._tagSet = tagSet
        for tag in valList:
            if tag in self._tagSet:
                self._argList.append(tag)
                self._argValList.append(valueMap[tag])

        if (self._debugLevel > 0):
            print 'argList %s\n'%(self._argList)
            print 'argValList %s\n'%(self._argValList)

    def UpdateTags(self,valueMap):
        debugArgs = []
        debugVals = []
        valList = valueMap.keys()
        for tag in valList:
            if tag in self._tagSet:
                self._argList.append(tag)
                debugArgs.append(tag)
                self._argValList.append(valueMap[tag])
                debugVals.append(self._argValList[-1])
            else:
                if self._debugLevel > 0:
                    print "missing column %s in table definition\n"%(tag)
        if (self._debugLevel > 0):
            print "updating args %s\n"%(debugArgs)
            print "updating vals %s\n"%(debugVals)
        
    def RunCmd(self):
        valList = [str(x) for x in self._argValList]
        insert_query = '''INSERT INTO {0} ({1}) VALUES {2}'''.format(self._tableName,
               (','.join(self._argList)), tuple(valList))
        if self._debugLevel > 0:
            print "sqlCmd: %s\n"%(insert_query)
        self._dbh.ExecuteCmd(insert_query)


