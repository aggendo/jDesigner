import visualizer as v
from dxfwrite import DXFEngine as dxf
import currentf as currentf

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

def circle(x, y, r):
    global canvas
    c = v.circle(x, y, r)
    canvas.create_oval(c[0], c[1], c[2], c[3], width=v.lineTh, activeoutline="yellow")

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
                    cent = options.split("\"")[1]
                    del options[gw]
                    break
                elif(options[gw].startswith('center')):
                    cent = options.split("\"")[1]
                    del options[gw]
                    break
            if(cent==None):
                cent = "center"
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
                    print("line")
                    mez = getMes(uLine, x1=options[0], y1=options[1], x2=options[2], y2=options[3])
                    mess = mez[0]
                    uns = mez[1]
                    del mez
                    Id = lineDraw(mess['x1'], mess['y1'], mess['x2'], mess['y2'])
                    del mess
                    cur.addListLine(Id, center=cent **uns)
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
                    del mess
                    cur.addListCircle(Id, center=cent **uns)
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
            if(uLine[0:1]!="#"):
                raise unknownCommandException(str(lineNum+1) + ": Unknown command: " + uLine);

def getMes(lineNum, **lenStrs): #this converts strings that are numbers and strings with units into what they are
    units = []
    numbers = []
    i=0
    for ie in lenStrs.items():
        k = str(ie[0])
        v = str(ie[1])
        #print("k "+k)
        #print("v "+v)
        vv=v
        print(v.endswith(tuple(['mm'])))
        print(v.endswith(tuple(['mm', 'in','\'', '\"', 'cm', 'ft', 'yd', 'm'])))
        stupidvar = v.endswidth(tuple(['mm']))
        if(stupidvar): #fix this whole tupple thing
            u = 'mm'
            v.replace(u, 'mm')
            numbers[k] = int(v)
            units[k+"u"] = u
        elif(v.endswith(tuple(['in', '\'']))):
            u = 'in'
            v.replace(u, 'in')
            v.replace(u, '\'')
            numbers[k] = int(v)*24.5
            units[k+"u"] = u
        elif(v.endswith(tuple(['cm']))):
            u = 'cm'
            v.replace(u, 'cm')
            numbers[k] = int(v)*10
            units[k+"u"] = u
        elif(v.endswith(tuple(['ft','\"']))):
            u = 'ft'
            v.replace(u, 'ft')
            v.replace(u, '\"')
            numbers[k] = int(v)*294   #24.5*12
            units[k+"u"] = u
        elif(v.endswith(tuple(['yd']))):
            u = 'yd'
            v.replace(u, 'yd')
            numbers[k] = int(v)*882 #24.5*12*3
            units[k+"u"] = u
        elif(v.endswith(tuple(['m']))):
            u = 'm'
            v.replace(u, 'm')
            numbers[k] = int(v)*1000
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
