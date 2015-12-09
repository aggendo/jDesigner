import visualizer as v
from dxfwrite import DXFEngine as dxf
import currentf as currentf
import re

def exportDxf(canvas, filename):
    drawing = dxf.drawing(filename)
    drawing.add_layer('LINES')
    drawing.add(dxf.line((0, 0), (1, 0), layer='LINES'))
    drawing.save

def spam():
    c = currentf.getInstance()
    return c.spam()

def exportSvg(canvas, filename):
    pass

def importDxf(canvas, filename):
    pass

def importSvg(canvas, filemane):
    pass

class unknownCommandException(Exception):
    pass

class MissMatchedOptionsException(Exception):
    pass

class unknownNumberOrUnit(Exception):
    pass

def notGrid(canvas, id):
    tags = canvas.gettags(id)            #get all of the tags for this item
    isGrid = True                       #we are going to initialize the var here
    for tag in tags:                    #loop through all the tags
        if(tag=="grid"):                #check if this tag if for the grid
            isGrid = False              #we know that it is part of the grid now
            break                       #we do not need to continue to search
    return(isGrid)

def save(filename, canvas):
    items = canvas.find_withtag('all')      #get everything
    lineList = []                           #this will store each line of the file so that we do not have the file open while we are preparing to save
    curLine = 0                               #this stores what the next empty cell is in the lineList table
    cur = currentf.getInstance()
    lines = []                              #all the lines in file
    throughLines = []                       #lines that cut though all
    holes = []                              #all the holes in the file
    removeMat = []                          #all the sections that completely remove material
    circles = list()                        #engraved circles
    lLine = 0                               #these store where we are in each array
    tLine = 0
    hLine = 0
    rLine = 0
    cLine = 0
    #TODO COMMENTS
    #TODO do this more efficiantly
    for i in items:
        if(notGrid(canvas, i)):             #check if it is part of the grid, because we do not export that
            itConf = cur.listConfig(i)
            ccent = cent = itConf['center'] #we are saving the numrical value for decording
            if(cent==2):
                cent="center"
            elif(cent==1):
                cent="outside"
            elif(cent==3):
                cent="inside"
            else:
                pass
                #raise() TODO
            itType = canvas.type(i)         #we should get the type here so we do not call type() every if loop
            if(itType=="oval"):
                coords = canvas.coords(i)
                ops = v.uCircle(coords[0], coords[1], coords[2], coords[3], ccent, i)
                print(ops);
                circles.insert(1, "circle(c=\"" + cent + "\"," + str(ops[0]) + "," + str(ops[1]) + "," + str(ops[2]) + ")")
                cLine=cLine+1
            elif(itType=="line"): #TODO finnish doing what I did to circle to line
              coords = canvas.coords(i)
              #TODO ucor these things
              lineList[lLine] = "line(c=\"" + cent + "\"" + str(coords[0]) + itConf['x1u'] + "," + str(coords[1]) + itConf['y1u'] + "," + str(coords[2]) + itConf['x2u'] + "," + str(coords[3]) + itConf['y2u'] + ")"
              lLine=lLine+1
              #todo finnish
            elif(itType=="arc"):
                pass
            #cLine=cLine+1
    lineList.extend(lines)
    lineList.extend(circles)
    lineList.extend(removeMat)
    lineList.extend(holes)
    lineList.extend(throughLines)
    with open(filename, "w+") as f:
        f.writelines(lineList)              #write lineList to file

def circle(x, y, r):
    global canvas
    c = v.circle(x, y, r)
    return(canvas.create_oval(c[0], c[1], c[2], c[3], width=v.lineTh, activeoutline="yellow"))

def lineDraw(x1, y1, x2, y2):
    return(canvas.create_line(v.cor(x1), v.cor(y1), v.cor(x2), v.cor(y2), width=v.lineTh, activefill="yellow"))
    
def imPorter(can, f):
    global canvas
    canvas = can
    for l in f:
        doCommand(l)

def doCommand(uLine):
    if(uLine[0]!="#"):
        line = uLine.lower();
        commands = [["layerBegin", 1], ["line", 4], ["comment", 1], ["circle", 3], ["arc", 7], ["hole", 2], ["layerEnd", 0]];
        global cType;
        global cBegin;
        cType = -1;
        cBegin = 0;
        for i in range(0, 7):#maybe needs to be 7
            if(line.find(commands[i][0])!=-1):
                cType = i;
                cBegin = len(commands[cType][0]) + line.find(commands[cType][0]);
                break
        b1 = line.find("(", cBegin);
        b2 = line.find(")", b1);
        options = [];
        if(line.find(",", b1, b2)!=-1):
            options = line[b1+1:b2].split(",");
        else:
            if(b1+1!=b2):
                options = [line[b1:b2]];
        print(uLine)
        if(cType!=-1):
            cent = None
            for gw in range(0, len(options), 1):
                if(options[gw].startswith('c')):
                    cent = options[gw].split("\"")[1]
                    del options[gw]
                    break
                elif(options[gw].startswith('center')):
                    cent = options[gw].split("\"")[1]
                    del options[gw]
                    break
            if(cent==None):
                cent = "center"
            if(cent=="center"):
                cent=2
            elif(cent=="outside"):
                cent=1
            elif(cent=="inside"):
                cent=3
            else:
                #raise() TODO
                pass
            if(len(options)!=commands[cType][1]):
                raise MissMatchedOptionsException(str(uLine+1) + ": not right number of arguments for command " + commands[cType][0] + " this method requires " + str(commands[cType][1]) + " options!");
            else:
                cur = currentf.getInstance()
                #print(str(options));
                if(cType==0): #layerBegin
                    pass
                    #currentLayerZ=int(options[0]);
                    #currentZ=currentLayerZ;
                    #addToOut(moveZ(int(options[0])), comment(lineNum, "moveZLayer"));
                elif(cType==1): #line
                    #print("line")
                    mez = getMes(uLine, x1=options[0], y1=options[1], x2=options[2], y2=options[3])
                    mess = mez[0]
                    uns = mez[1]
                    del mez
                    Id = lineDraw(mess['x1'], mess['y1'], mess['x2'], mess['y2'])
                    uns['center']=cent
                    del mess
                    cur.addListLine(Id, **uns)
                    del uns
                elif(cType==2): #comment
                    pass
                    #"; " + options[0]);
                    #TODO: fix not storing comments
                elif(cType==3): #circle
                    mez = getMes(uLine, x=options[0], y=options[1], r=options[2])
                    mess = mez[0]
                    uns = mez[1]
                    del mez
                    Id = circle(mess['x'], mess['y'], mess['r'])
                    print(Id)
                    uns['center']=cent
                    del mess
                    cur.addListCircle(Id, **uns)#center=cent, xu=uns['xu#wish I could figure out why this does not work using**uns)
                    del uns
                elif(cType==4): #arc
                    arc(int(options[0]), int(options[1]), int(options[2]), int(options[3]), int(options[4]), int(options[5]), int(options[6]))
                elif(cType==5): #hole
                    mez = getMes(uLine, x=options[0], y=options[1])
                    mess = mez[0]
                    uns = mez[1]
                    del mez
                    Id = hole(mess['x'], mess['y'])
                    del mess
                    cur.addListCircle(Id, **uns)
                    del uns
                elif(cType==6): #layerEnd
                    print("finnished a layer");
                else:
                    print("don't use "+uLine+" , there is a weird glitch");
                    #raise unknownCommandException(str(lineNum+1) + ": Unknown command: " + uLine);
        else:
            if(uLine[0:1]!="#"):        #really need to make this evaluated earlier
                raise unknownCommandException(str(lineNum+1) + ": Unknown command: " + uLine);

def Int(Int, Mult=1):
    if(Int=="0" or Int=="0.0"):
        return(0)       #prevent invalid int
    else:
        return(float(Int)*Mult) #multiply

def getMes(lineNum, **lenStrs): #this converts strings that are numbers and strings with units into what they are
    units = {}
    numbers = {}
    i=0
    for ie in lenStrs.items():
        k = str(ie[0])
        v = str(ie[1])
        #print("k "+k)
        #print("v "+v)
        vv=re.sub(r"[ +-0123456789.]", r"", v)
        v=re.sub(r"[ inmftyd'\"c]", r"", v)
        multipl = 0     #the object multiplier
        if(vv=="mm"): #fix this whole tupple thing
            u = 'mm'
            numbers[k] = Int(v)
            units[k+"u"] = u
        elif(vv=='in' or v=='\"'):
            u = 'in'#TODO EVENTUALLY keep track of if they use in or " same for ft
            numbers[k] = Int(v, 24.5)
            units[k+"u"] = u
        elif(vv=='cm'):
            u = 'cm'
            v.replace('cm', '')
            numbers[k] = Int(v,10)
            units[k+"u"] = u
        elif(vv=='ft' or v=='\''):
            u = 'ft'
            numbers[k] = Int(v,294)   #24.5*12
            units[k+"u"] = u
        elif(vv=='yd'):
            u = 'yd'
            numbers[k] = Int(v,882) #24.5*12*3
            units[k+"u"] = u
        elif(vv=='m'):
            u = 'm'
            numbers[k] = Int(v,1000)
            units[k+"u"] = u
        else:
            try: #TODO switch to using string.digits or is it string.isnumber?
                numbers[k] = int(v)
                #units[k+"u"] = 'mm'
            except:
                raise(unknownNumberOrUnit(str(lineNum+1) + ": " + str(v) + " is not a number or does not end with a valid unit"))
    return([numbers, units])

def __init__():
    pass

if(__name__=="__main__"):
    print("do not run this in terminal")
