import visualizer as v
import os as os
import json
from shutil import rmtree
from os.path import expanduser
from os.path import join as OSpathJoin
global appLoc
appLoc = "C:\Users\john\Desktop\jDesigner"#C:\\Program Files\\aggendo\\jCode\\"
configFold = "C:\Users\john\Desktop\jDesigner\config"
recent = ""
canvas = ""
shortcuts = ""
prefs = ""
#jDe = json.JSONDecoder
recF = file
prefF = file
tempFold = "C:\\Users\\john\\Desktop\\jDesigner\\temp"
def genPaths():
    partialPath =  v.__file__ #get the path to visualizer.pyc
    partialPath = partialPath[:-15] #strip away the /visualizer.pyc
    appLoc = partialPath
    configFold = OSpathJoin(partialPath, "config")
    tempFold = OSpathJoin(partialPath, "temp")
    print(partialPath)
genPaths()
def getTemp():
    return(tempFold) #TODO make tempFold configurable

def singleton(cls):
    instances = {}
    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return getinstance

@singleton
class MyClass:
    appLoc = ""
    def __init__():
        if not os.path.exists(appLoc):
            os.makedirs(appLoc)
def getRecent():
    recF = open(recent, "r")
    jRec = json.load(recF)
    recF.close()
    return(jRec)

#TODO has something that add the path to identical filenames in drop down

def lastFile():
    recF = open(recent, "r")
    jRec = json.loads(recF.read())
    recF.close()
    if(len(jRec)!=0):
        return(jRec[0]["name"])
    else:
        return(None)
    
def addRecent(name, path):
    recF = open(recent, "r")
    jDe = json.JSONDecoder()
    jRec = jDe.decode(recF.read())
    recF.close()
    del jDe
    for dic in jRec:
        if(dic["path"]==path):
            jRec.remove(dic)
            break
    #if(jRec.count({name: path})==1):
        #jRec.remove({name: path})
    if(len(jRec)==getSetting('recents')):
        del jRec[getSetting('recents')-1]
    jRec.insert(0, {"name": name, "path": path})
    recF = open(recent, "w+")
    recF.write(json.dumps(jRec, sort_keys=True, indent=4, separators=(',', ': ')))
    recF.close()
    del jRec

def printRecents():
    recF = open(recent, "r")
    print(recF.read())
    recF.close()
    
def getSetting(name):
    global prefs
    prefF = open(prefs, "r")
    jPref = json.loads(prefF.read())
    prefF.close
    return(jPref[name])

def storeSetting(name, value):
    prefF = open(prefs, "r")
    jPref = json.loads(prefF.read())
    prefF.close()
    prefF = open(prefs, "w+")
    jPref[name] = value
    prefF.write(json.dumps(jPref, sort_keys=True, indent=4, separators=(',', ': ')))
    prefF.close()

def createDefaultPrefs():
    jPref = {}
    jPref['recents'] = 3
    jPref['sizeX'] = 700
    jPref['sizeY'] = 600
    jPref['defaultBitSize'] = 3.3
    jPref["defaultFolder"] = expanduser("~")
    jPref['defaultHomingPos'] = 0 #0=bot left, 1 = bot right, 2 = top left 3=top right
    return(json.dumps(jPref, sort_keys=True, indent=4, separators=(',', ': ')))

def createRecentsList():
    ret = [{'file.j':'location'},]
    return(ret)

def __init__():
    global recent
    global canvas
    global shortcuts
    global prefs
    if not os.path.exists(appLoc):
        print("creating files")        
        os.makedirs(appLoc)
    if not os.path.exists(configFold):
        os.mkdir(configFold)#{"filename": "filepath"},{"otherName": "filepath"}
        recent = open(os.path.join(configFold, "recent.json"), "w+")
        recent.write('[]')# indent=4))# separtors=(',', ': ')))
        canvas = open(os.path.join(configFold, "canvas.json"), "w+")
        shortcuts = open(os.path.join(configFold, "shortcuts.json"), "w+")
        prefs = open(os.path.join(configFold, "prefs.json"), "w+")
        prefs.write(createDefaultPrefs())
        #files are created
        recent.close()
        canvas.close()
        shortcuts.close()
        prefs.close()
    recent = os.path.join(configFold, "recent.json")
    canvas = os.path.join(configFold, "canvas.json")
    shortcuts = os.path.join(configFold, "shortcuts.json")
    prefs = os.path.join(configFold, "prefs.json")

def __kill__():
    global recF
    global prefF
    global recent
    global canvas
    global shortcuts
    global prefs
    try:
        recF.close()
    except:
        pass
    try:
        canvas.close()
    except:
        pass
    try:
        shortcuts.close()
    except:
        pass
    try:
        prefF.close()
    except:
        pass
    del recent
    del canvas
    del shortcuts
    del prefs
    del prefF
    del recF
    #del jDe

if(__name__=="__main__"):
    #singleton();
    try:
        rmtree(configFold)
    except:
        pass
    try:
        __init__()
        addRecent('test file', 'testLoc')
        addRecent('test2', 'loc')
        addRecent('test3', 'loc1')
        addRecent('test3', 'loc1')
        printRecents()
        __kill__()
    except Exception as inst:
       # print type(inst)     # the exception instance
       # print inst.args      # arguments stored in .args
       # print inst           # __str__ allows args to be printed directly
        __kill__()
        raise
if(prefs==""):
    try:
        __init__() #find a way to use with statements to close files
    except Exception as inst:
       # print type(inst)     # the exception instance
       # print inst.args      # arguments stored in .args
       # print inst           # __str__ allows args to be printed directly
        __kill__()
        raise
            
        
