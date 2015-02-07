import math
class Coord(object):
    def __init__(self,x,y):
        self.x = x
        self.y = y

    def __sub__(self,other):
        # This allows you to substract vectors
        return Coord(self.x-other.x,self.y-other.y)

    def __repr__(self):
        # Used to get human readable coordinates when printing
        return "Coord(%f,%f)"%(self.x,self.y)

    def length(self):
        # Returns the length of the vector
        return math.sqrt(self.x**2 + self.y**2)

    def angle(self):
        # Returns the vector's angle
        return math.atan2(self.y,self.x)

def normalize(coord):
    return Coord(
        coord.x/coord.length(),
        coord.y/coord.length()
        )

def perpendicular(coord):
    # Shifts the angle by pi/2 and calculate the coordinates
    # using the original vector length
    return Coord(
        coord.length()*math.cos(coord.angle()+math.pi/2),
        coord.length()*math.sin(coord.angle()+math.pi/2)
        )

def getAngle(p1, p2):
    x1 = p1.x
    y1 = p1.y
    x2 = p2.x
    y2 = p2.y
    dx,dy = x2-x1,y2-y1
    rads = math.atan2(dx,dy)
    return(math.degrees(rads))

def angleDif(x,y):
  return min(y-x, y-x+2*math.pi, y-x-2*math.pi, key=abs)

def angleCompare(p1, p2=''):
    ang = 0
    if(p2==''):
        ang = p1
    else:
        ang = getAngle(p1, p2)
    if(ang==45):
        return(45)
    elif(ang==90+45):
        pass
    elif(ang==180+45):
        pass
    elif(ang==270+45):
        pass
    elif(ang==0):
        pass
    elif(ang==90):
        pass
    elif(ang==180):
        pass
    elif(ang==270):
        pass
    elif(ang==360):
        pass
    else:
        if(ang>179):
            pass

def moveAlongAngle(p1, p2, ang=""):
    if(ang==""):
        ang = angleDif(p1, p2)
    pang = angleDif

def DEPRICATEDangleCompare(p1, p2=""):
    ang = 0
    if(p2==""):
        ang = p1
    else:
        ang = getAngle(p1, p2)
    print("angle:  "+str(ang))
    testAng = range(0, 360, 90)#not much of a range, needs work
    angles = [0,0,0,0]
    for i in [0,1,2,3]:
        angles[i] = angleDif(testAng[i], ang)
    print(angles)
    mini = min(filter(lambda x:x>0,angles))
    if(angles.count(mini)!=1):
        pass #here we have a 45 degree angle
    else:
        return testAng[angles.index(mini)]

if(__name__=="__main__"):
    a = Coord(0,0)
    b = Coord(5,5)
    print(angleCompare(a,b))
    #print perpendicular(a)
