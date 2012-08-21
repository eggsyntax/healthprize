from dao import dao
from math import sqrt,log
import config

class Data:
    ''' Intended to be subclassed by Members, Claims, perhaps others. Makes a generic request;
        subclasses need only implement setTable() to complete, but may also add methods specific 
        to their type. Returns some subset of the rows of the specified table as a list
        of dicts.'''

    def __init__(self):
        self.constraints = []
        self.datalist = None
        self.table = None
        self.setTable()
        self._i = 0 # For iteration
        
    def where(self, c):
        ''' takes a constraint, eg "memberid = 60481" '''
        self.constraints.append(c)
        return self # for chaining
        
    def reset(self):
        self.__init__()
        
    def _populate(self):
        ''' Private method which is lazily evaluated as needed. From the user's perspective,
            the data should have all been present from the moment the object was instantiated.
        '''
        self.datalist = dao.getConstrainedData(self.table,self.constraints)
        return self.datalist

    def setTable(self):
        ''' Implemented by subclasses '''
        pass

    def validate(self):
        ''' Ensure that lazy evaluation has been completed. Should be called by any
            method that needs the dataset to be populated. '''
        if not self.datalist: self._populate()
        
    # Iterator methods
    def __iter__(self):
        return self

    def next(self):
        self.validate()
        if self._i >= len(self.datalist): 
            self._i = 0
            raise StopIteration
        o = self.datalist[self._i]
        self._i += 1
        return o
    
    def __repr__(self):
        self.validate()
        return "\n".join((str(i) for i in self.datalist))
       
    def __len__(self):
        self.validate()
        return len(self.datalist)
    
class Claims(Data):
    def setTable(self):
        self.table = config.claimstable
        
    def formember(self,m):
        ''' return all claims associated with a particular member. Evaluated eagerly
            so it can be cached. '''
        id = str(m["memberid"])
        try:
            return  dao.cachedClaims[id]
        except KeyError:
            docache = not self.constraints # Cache only simple by-member queries
            self.constraints.append("memberid = "+id)
            self.validate()
            if docache: dao.cachedClaims[id] = self.datalist
            return self

class Members(Data):
    
    def setTable(self):
        self.table = config.memberstable

    def makeprediction(self,f):
        self.validate()
        sum = 0
        for d in self.datalist:
            # Here's the evaluation function given
            p = f(d)
            a = d["daysin"]
            sum += (log(p+1) - log(a+1)) ** 2
        e = sqrt(sum/len(self.datalist))
        return e

    def avedaysin(self):
        self.validate()
        return sum([f["daysin"] for f in self.datalist]) / float(len(self.datalist))
    
    # TODO
    def withaclaimwhere(self,constraints):
        membersmeetingconstraints = []
        for m in self.datalist:
            claims = Claims().formember(self["memberid"])
            
