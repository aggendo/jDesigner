#TODO store where default things are in config file
class getInstance:
    class __impl:
        """ Implementation of the singleton interface """

        def spam(self):
            """ Test method, return singleton id """
            return id(self)
        global obList
        obList = {}

        def addListLine(self, tag, **a):#center 1=outside, 2=middle, 3=inside
#type is always line for this pXj = id tag of line connected to first set of coords
            #pXo = which set of coords of the intersecting line intersect
            #units are ones that end in 'u's
            #dir = direction of movement, for when length is locked
            #showD = show Distance/line length
            global obList
            aa = {'Type':'LINES', 'center':2, 'x1u':'mm', 'x2u':'mm', 'y1u':'mm', 'y2u':'mm', 'locked':[], 'p1j':None, 'p1o':None, 'p2j':None, 'p2o':None, 'length':None, 'lU':'mm', 'dir':None, 'showD':False}
            aa.update(a)
            obList[tag] = aa

        def addListCircle(self, tag, **a):#center 1=outside, 2=middle, 3=inside
#type is always line for this pXj = id tag of line connected to first set of coords
            #pXo = which set of coords of the intersecting line intersect
            #showD = show Distance/line length
            global obList
            aa  = {'Type':'CIRCLES', 'center':2, 'cx':None, 'cy':None, 'r':None, 'cxU':'mm', 'cyU':'mm', 'rU':"mm", 'showD':False}
            aa.update(a)
            obList[tag] = aa

        def addListHole(self, tag, **a):
            #cXu = units of center
            global obList
            aa = {'Type':'HOLE', 'cxu':'mm', 'cyu':'mm', 'wU':'mm'}#cx, cy, and (maybe) cz are required for this to work, so hopefully they are passed
            aa.update(a)
            obList[tag] = aa
        
        def removeList(self, tag):
            global obList
            del obList[tag]

        def listConfig(self, tag, **a):
            global obList
            if(len(a)==0):
                return(obList[tag])
            else:
                obList[tag].update(a)
                
        def logObList(self):
            print(obList)
        
    # storage for the instance reference
    __instance = None#TODO make list and make __init__() take arg for file for multi file handling

    def __init__(self):
        """ Create singleton instance """
        # Check whether we already have an instance
        if getInstance.__instance is None:
            # Create and remember instance
            getInstance.__instance = getInstance.__impl()

        # Store instance reference as the only member in the handle
        self.__dict__['_Singleton__instance'] = getInstance.__instance

    def __getattr__(self, attr):
        """ Delegate access to implementation """
        return getattr(self.__instance, attr)

    def __setattr__(self, attr, value):
        """ Delegate access to implementation """
        return setattr(self.__instance, attr, value)
def __init__():
    pass
if(__name__=="__main__"):
    c = getInstance()
    print(c.spam())
    cc = getInstance()
    print(cc.spam())
    del cc
    c.addListCircle(89, delir="vovo")
    c.listConfig(89, delir='volvo')
    c.logObList()#print(c.listConfig(89))
    c.removeList(89)
