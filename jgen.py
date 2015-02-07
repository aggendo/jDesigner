#generates simple gcode
import sys
global incontents;
incontents=[];
global outcontents;
outcontents=[];
global show
global liftAmount
liftAmount = "1";
global layerHeight
layerHeight = 2; #will use in future to avoid cutting to much but for now you just write support in code
global currentLayerZ
currentLayerZ = 1; #inverted so never negative
global materialThickness
materialThickness = "5"; #for drilling holes
global drillingFeedrate
drillingFeedrate = "50"; #feedrate for drilling
show = False;
class unknownCommandException(Exception):
    pass

class MissMatchedOptionsException(Exception):
    pass

class directionException(Exception):
    pass

def addToOut(command, comment=""):
    if(comment==""):
        outcontents.append(command);
    else:
        outcontents.append(command + comment);

def readFile(ifile):
    infile = open(ifile, "r")
    for line in infile:
        incontents.append(line);
    infile.close();

def moveTo(ex, ey, lineN): #go to the position of next shape
    addToOut(lift(lineN))
    addToOut(move(ex, ey, lineN));
    addToOut(lower(lineN));
    currentX=ex;
    currentY=ey;

def circle(cx, cy, radius, lineN): #a full circle always clockwise
    print("circle");
    addToOut(moveTo(cx-radius, cy, lineN))
    currentX=cx-radius;
    currentY=cy;
    return("G2X"+str(cx-radius)+"Y"+str(cy)+"I"+str(radius)+"J0");
    

def arc(sx, sy, ex, ey, cx, cy, direction, lineN): #an incomplete circle with a start and end x&y
    if(currentX!=sx):
        if(currentY!=sy):
            moveTo(sx, sy, lineN);
    currentX=ex;
    currentY=ey;
    if(direction==0): #clockwise
        return("G2X"+str(ex)+"Y"+str(ey)+"I"+str(sx-cx)+"J"+str(sy-cy))
    elif(direction==1): #counterclockwise
        return("G3X"+str(ex)+"Y"+str(ey)+"I"+str(sx-cx)+"J"+str(sy-cy))
    else:
        raise directionException(str(lineN)+": direction to high needs to be 0 for clockwise and 1 for counter!")

def lineDraw(sx, sy, ex, ey, lineN): #line, like move only intended of cutting and has a start and end x
    global currentX;
    global currentY;
    if(currentX!=sx):
        if(currentY!=sy):
            moveTo(sx, sy, lineN);
    currentX=ex;
    currentY=ey;
    return("G1X"+str(ex)+"Y"+str(ey));

def move(ex, ey, lineN): #move, intended for not cutting movements
    currentX=ex;
    currentY=ey;
    return("G0X" + str(ex) + "Y" + str(ey) + comment(lineN, "move"));

def moveZ(ez): #not sure when this will get used
    return("G0Z"+str(ez));

def lift(lineN): #move above material so not cutting
    currentZ=int(liftAmount);
    return("G0Z"+liftAmount + comment(lineN, "moveZMove"));

def lower(lineN): #lower back to being on material
    currentZ=0-int(currentLayerZ);
    return("G0Z"+str(0-currentLayerZ) + comment(lineN, "moveZBack"));

def hole(x, y, lineN): # drill a hole through material
    moveTo(x, y, lineN);
    currentX=x;
    currentY=y;
    return("G1Z"+materialThickness+"F"+drillingFeedrate);

def writeFile(ofile):
    outfile = open(ofile, "w");
    outfile.truncate();
    for i in range(0, len(outcontents)):
        outfile.write(outcontents[i]);
        outfile.write("\n")
    outfile.close();
    print("done writing file");

def comment(lineNum, Type): #add a comment to make gcode human readable
    if(Type=="line"):
        return(" ;cutting a line from line " + str(lineNum));
    elif(Type=="arc"):
        return(" ;cutting an arc from line " + str(lineNum));
    elif(Type=="circle"):
        return(" ;cutting a circle from line " + str(lineNum));
    elif(Type=="move"):
        return(" ;moving to next cutting position at line " + str(lineNum));
    elif(Type=="moveZMove"):
        return(" ;moving z above material to move to prepare for command on line " + str(lineNum));
    elif(Type=="moveZLayer"):
        return(" ;moving the z down to cut another layer");
    elif(Type=="moveZBack"):
        return(" ;moving z down to go back to cutting");
    elif(Type=="hole"):
        return(" ; drilling hole");
    else:
        return(" ;Unkown command type error");

def fileComment(comment):
    addToOut(";" + comment);

def header(filename):
    addToOut("; generated with jcut (by John Sandstedt)");
    addToOut("; " + filename);
    addToOut("; have fun!");

def doCommand(uLine, lineNum):
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
        if(cType!=-1):
            if(len(options)!=commands[cType][1]):
                raise MissMatchedOptionsException(str(lineNum+1) + ": not right number of arguments for command " + commands[cType][0] + " this method requires " + str(commands[cType][1]) + " options!");
            else:
                #print(str(options));
                if(cType==0): #layerBegin
                    currentLayerZ=int(options[0]);
                    currentZ=currentLayerZ;
                    addToOut(moveZ(int(options[0])), comment(lineNum, "moveZLayer"));
                elif(cType==1): #line
                    addToOut(lineDraw(int(options[0]),int(options[1]),int(options[2]),int(options[3]),int(lineNum)) + comment(lineNum,"line"));
                elif(cType==2): #comment
                    addToOut("; " + options[0]);
                elif(cType==3): #circle
                    addToOut(circle(int(options[0]), int(options[1]), int(options[2]), lineNum), comment(lineNum, "circle"));
                elif(cType==4): #arc
                    addToOut(arc(int(options[0]), int(options[1]), int(options[2]), int(options[3]), int(options[4]), int(options[5]), int(options[6]), lineNum), comment(lineNum, "arc"));
                elif(cType==5): #hole
                    addToOut(hole(int(options[0]), int(options[1]), lineNum), comment(lineNum, "hole"));
                elif(cType==6): #layerEnd
                    print("finnished a layer");
                else:
                    print("don't use "+uLine+" , there is a weird glitch");
                    #raise unknownCommandException(str(lineNum+1) + ": Unknown command: " + uLine);
        else:
            if(uLine[0:1]!="#"):
                raise unknownCommandException(str(lineNum+1) + ": Unknown command: " + uLine);

def parse(inFilename, outFilename):
    header(outFilename);
    readFile(inFilename);
    global currentX
    currentX=0;
    global currentY
    currentY=0;
    global currentZ
    currentZ=0;
    for i in range(0, len(incontents)):
        doCommand(incontents[i], i);
    writeFile(outFilename);
if(__name__=="__main__"):
    if(len(sys.argv)!=1):
        if(len(sys.argv)==2):
            parse(sys.argv[1], sys.argv[1].split(".")[0]+".gcode");
        else:
            parse(sys.argv[1], sys.argv[2]);
    else:
        print("help comming soon")
else:
    pass#party here we got work TODO
