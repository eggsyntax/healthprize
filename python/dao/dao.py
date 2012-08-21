import pymysql
import config

_conn = None
cur = None

cachedClaims = {}

def open():
    global _conn
    global cur
    _conn = pymysql.connect(**config.dbparams)
    cur = _conn.cursor()
    cur.arraysize = 500

def executeSql(q):
    ''' Executes arbitrary sql '''
    if cur is None: open()
    cur.execute(q)
    
def executeQuery(q):
    ''' Responsible for actually executing a query. '''
    # TODO: return iterator which fetches, say, 500 rows at a time?
    #print "\n         ("+q + ")\n" 
    if cur is None: open()
    cur.execute(q)
    r = cur.fetchall()
    return asDicts(r)

def getConstrainedData(table,constraints):
    ''' takes a table and a list of where clauses and returns data as a list of dicts '''
    q = "select * from "+table+" where "
    q += " and ".join(constraints) + ";"
    return executeQuery(q)

def commit():
    _conn.commit()
    
def close():
    print "closing connections"
    # TODO: who's responsible for calling this? Do I need a connection pool?
    print "closing"
    if cur is not None: cur.close()
    if _conn is not None: _conn.close()

def asDicts(r):
    ''' takes the tuple of tuples returned by DB requests and converts them
        into a list of dicts with keys given by the column names.
    '''
    obs = []

    fieldnames = []
    for t in cur.description:
        fieldnames.append(t[0])

    for tup in r:
        newdict = {}
        for i,val in enumerate(tup):
            newdict[fieldnames[i]] = val
        obs.append(newdict)
    return obs

def __doctests():    
    ''' Doctests:
    >>> import dao
    >>> dao.open()
    >>> r = dao.executeQuery("SELECT * from membersy1 where memberid = 60481")
    >>> type(r)
    <type 'list'>
    >>> len(r)
    1
    >>> dao.close()

    '''

if __name__ == "__main__":
    import doctest
    doctest.testmod()



    
