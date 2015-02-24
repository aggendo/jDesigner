from Tkinter import *
import tkFileDialog
import ttk as ttk
import math as math
import inOutPorter as inOut
import configuration as cnf
import os.path as path
import currentf as currentf
import errors as errors
import mathCordHelper as mH
import re
#import eFrames as eF

gridSpacing = 50
gridUnits = 10
cWidth=550
cHeight=550
aShift=5 #arrow shift
tool=0
lineTH = 1.65 #line thickness IMPORTANT use lineTh in programming as that has
#gone through mes()
selected=0
global newFile
newFile = True #is the file new or an open file
global master
global objects
objects=[]
global canvas
global yHalf
global half
global mouseInside
global prop
global propertiesPane
global creating
global selectedOps #the options of selected circles and needed to be passed
mouseInside=False #is the mouse inside of the canvas widget

def move(event):
    global canvas
    global selected
    if(selected!=0):
        if(mouseInside):
            if(event.keycode==37):#left
                c = canvas.coords(selected)
                if(len(c)==4):
                    canvas.coords(selected, c[0]-mes(aShift), c[1], c[2]-mes(aShift), c[3])
                elif(len(c)==2):
                    canvas.coords(selected, c[0]-mes(aShift), c[1])
                else:
                    pass#error here
                updateProps()
            elif(event.keycode==40):#down
                c = canvas.coords(selected)
                if(len(c)==4):
                    canvas.coords(selected, c[0], c[1]+mes(aShift), c[2], c[3]+mes(aShift))
                elif(len(c)==2):
                    canvas.coords(selected, c[0], c[1]+aShift)
                else:
                    pass#error here
                updateProps()
            elif(event.keycode==38):#up
                c = canvas.coords(selected)
                if(len(c)==4):
                    canvas.coords(selected, c[0], c[1]-mes(aShift), c[2], c[3]-mes(aShift))
                elif(len(c)==2):
                    canvas.coords(selected, c[0], c[1]-mes(aShift))
                else:
                    pass#error here
                updateProps()
            elif(event.keycode==39):#right
                c = canvas.coords(selected)
                if(len(c)==4):
                    canvas.coords(selected, c[0]+mes(aShift), c[1], c[2]+mes(aShift), c[3])
                elif(len(c)==2):
                    canvas.coords(selected, c[0]+mes(aShift), c[1])
                else:
                    pass#error here
                updateProps()
            else:
                pass#error handle here
def inM(event):
    global mouseInside
    mouseInside=True
def outM(event):
    global mouseInside
    mouseInside=False
def clearProps():
    global propertiesPane
    if(propertiesPane!=""):
        propertiesPane.grid_remove()
        propertiesPane=""

def updateProps():
    global propertiesPane
    global prop
    global canvas
    global selected
    if(propertiesPane!=""): #check for presence of old property panel
        clearProps()        #make way for new properties panel
    if(canvas.type(selected)=="line"):
        propertiesPane = editLine(prop)
    elif(canvas.type(selected)=="oval"):
        propertiesPane = editCircle(prop)
        

def click(event):           #this event fires whenever there is a click while the application has focus
    global selected
    global canvas
    if(mouseInside):        #this narrows it down to clicks inside of the canvas.
                            #this way you do not click on a textbox in the properties panel only to deselect everything
        if(selected!=0):            #if there was something perviously selected
            try:
                canvas.itemconfig(selected, outline="black")    #attempt to set a black outline
            except(Exception):
                canvas.itemconfig(selected, fill="black")   #some items do not have an outline and have a fill instead
        current = canvas.find_withtag(CURRENT)  #set selected to the ids of the selected items
        if(str(current)!="()"):                 #if some item was actually clicked on
            notGrid=True                        #set variable initially
            tags = canvas.gettags(current)      #get all the tags for this object
            for tag in tags:            #loop through tags
                if(tag=="grid"):        #if this is part of grid
                    notGrid=False       #mark as not selectable
                    break               #exit from loop
            if(notGrid):                #continue if it passed the grid test
                selected = current
                try:
                    canvas.itemconfig(current, outline="green") #same as try above only for setting selection color
                except(Exception):
                    canvas.itemconfig(selected, fill="green")
                updateProps()           #change the property panel to reflect the new object
            else:                       #we clicked a grid object
                selected=0              #clear selected variable
                clearProps()            #get rid of properties panel
        else:
            clearProps()        #we did not click anything so get rid of properties panel
            select=0            #clear selected variable

def fullUnitify(x): #this if for when it comes as text like '10.0mm'
    vv=re.sub(r"[ -+0123456789.]", r"", x)
    v=re.sub(r"[ inmftyd'\"c]", r"", x)
    u='mm'
    if(vv=="mm"):
        texts = float(v)
    elif(vv=='in' or v=='\"'):
        u='in'
        texts = float(v)*24.5
    elif(vv=='cm'):
        u='cm'
        texts = float(v)*10
    elif(vv=='ft' or v=='\''):
        u='ft'
        texts = float(v)*294   #24.5*12
    elif(vv=='yd'):
        u='yd'
        texts = float(v)*882 #24.5*12*3
    elif(vv=='m'):
        u='m'
        texts = float(v)*1000
    else:
        try: #TODO switch to using string.digits or is it string.isnumber?
            texts = float(v)
        except:
            raise(errors.unknownUnit())
    return(texts) #TODO delete the u var

def numeric(action, index, value_if_allowed,
                       prior_value, text, validation_type, trigger_type, widget_name, coHo="", chow=""):
    global selected
    global canvas
    global selectedOps
    cur = currentf.getInstance()
    vv=re.sub(r"[ -+0123456789.]", r"", value_if_allowed)
    v=re.sub(r"[ inmftyd'\"c]", r"", value_if_allowed)
    u='mm'
    if(vv=="mm"):
        texts = float(v)
    elif(vv=='in' or v=='\"'):
        u='in'
        texts = float(v)*24.5
    elif(vv=='cm'):
        u='cm'
        texts = float(v)*10
    elif(vv=='ft' or v=='\''):
        u='ft'
        texts = float(v)*294   #24.5*12
    elif(vv=='yd'):
        u='yd'
        texts = float(v)*882 #24.5*12*3
    elif(vv=='m'):
        u='m'
        texts = float(v)*1000
    else:
        try: #TODO switch to using string.digits or is it string.isnumber?
            texts = float(v)
        except:
            return(True)#somehow need to show that the value will not work maybe it will turn red, or maybe it will revert and show a tooltip when they click away
    value_if_allowed = texts
    if(chow==""):
        coords = canvas.coords(selected)
        coords[int(coHo)] = cor(value_if_allowed)
        if(coHo==0):#x1
            cur.listConfig(selected[0], x1u=u)
        elif(coHo==1):#y1
            cur.listConfig(selected[0], y1u=u)
        elif(coHo==2):#x2
            cur.listConfig(selected[0], x2u=u)
        elif(coHo==3):#y2
            cur.listConfig(selected[0], y2u=u)
        canvas.coords(selected, coords[0], coords[1], coords[2], coords[3])
    elif(chow=='1'):
        coHo = int(coHo)
        for i in range(0, len(selectedOps), 1):
            if(type(selectedOps[i])==str):
                selectedOps[i] = fullUnitify(selectedOps[i])
        selectedOps[coHo] = value_if_allowed
        if(coHo==0):#y
            cur.listConfig(selected[0], xu=u)
        elif(coHo==1):#x
            cur.listConfig(selected[0], yu=u)
        elif(coHo==2):#r
            cur.listConfig(selected[0], ru=u)
        coords = circle(selectedOps[0], selectedOps[1], selectedOps[2])
        canvas.coords(selected, coords[0], coords[1], coords[2], coords[3])
    return True    

def callback(event):
    canvas = event.widget
    x = canvas.canvasx(event.x)
    y = canvas.canvasy(event.y)
    print canvas.find_closest(x, y)

def cor(x, u='mm', center=2):
    if(u=='in'):
        x=x*25.4
    elif(u=='ft'):
        x=x*304.8
    elif(u=='cm'):
        x=x*10
    elif(u=='mm'):
        pass
        #print('x' + str(x))
    else:
        raise(errors.unknownUnit())
    if(center==2):
        pass
    elif(center==1):
        dis = lineTH/2
        x=x-dis
    elif(center==3):
        dis = lineTH/2
        x=x+dis
    ratio = gridSpacing/gridUnits
    nX=0
    if(x==0):
        return(half)
    if(x<0):
        #print('true')
        x=x*-1
        xh = half/ratio
        x=xh-x
        #print(x*ratio)
        return(x*ratio)
    else:
        nX=half
        eX=x*ratio
        return(nX+eX)

def uucor(x):
    global half
    global yHalf
    ratio = gridSpacing/gridUnits
    nX=0
    if(x==half):
        return(0.0)
    if(x<half):
        pX = half-x
        pX = pX/ratio
        return(0-pX)
    else:
        nX=x-half
        return(nX/ratio)
def ucor(x, u='mm', center=2):
    x = uucor(x)
    dis = lineTH/2
    if(u=='in'):
        x=x/25.4
        dis = dis/25.4
    elif(u=='ft'):
        x=x/304.8
        dis = dis/304.8
    elif(u=='cm'):
        x=x/10
        dis = dis/10
    elif(u=='mm'):
        pass
    if(center==2):
        pass
    elif(center==1):
        x=x+dis
    elif(center==3):
        x=x-dis
    return x
        

def mes(x):
    ratio = gridSpacing/gridUnits
    if(x<0):
        return(x*ratio*-1)
    else:
        return(x*ratio)

class arcDialog:
    
    def __init__(self, parent):

        top = self.top = Toplevel(parent)

        l = Label(top, text="point 1 X")
        l.grid(row=1, column=1)
        l.pack()

        vcmd = (top.register(self.numeric),
                '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')

        self.x1 = Entry(top, validate = 'key', validatecommand = vcmd)
        self.x1.grid(row=2, column=1)
        self.x1.pack(padx=5)

        self.d = Label(top, text="point 1 Y")
        self.d.grid(row=3, column=1)
        self.d.pack(padx=10)

        self.y1 = Entry(top, validate = 'key', validatecommand = vcmd)
        self.y1.grid(row=4, column=1)
        self.y1.pack(padx=15)

        self.l = Label(top, text="point 2 X")
        self.l.grid(row=5, column=1)
        self.l.pack(padx=20)

        self.x2 = Entry(top, validate = 'key', validatecommand = vcmd)
        self.x2.grid(row=6, column=1)
        self.x2.pack(padx=15)

        self.l1 = Label(top, text="point 2 Y")
        self.l1.grid(row=7, column=1)
        self.l1.pack(padx=20)

        self.y2 = Entry(top, validate = 'key', validatecommand = vcmd)
        self.y2.grid(row=8, column=1)
        self.y2.pack(padx=25)

        b = Button(top, text="OK", command=self.ok)
        b.pack(pady=5)
        top.bind('<Return>', self.ok)

    def ok(self, fail = 0):
        global canvas
        v1x = int(self.x1.get())
        v1y = int(self.y1.get())
        v2x = int(self.x2.get())
        v2y = int(self.y2.get())
        ov = canvas.create_line(cor(v1x), cor(v1y), cor(v2x), cor(v2y), width=lineTh, activefill="yellow")
        self.top.destroy()

class lineDialog:

    def numeric(self, action, index, value_if_allowed,
                       prior_value, text, validation_type, trigger_type, widget_name):
        if text in '0123456789.-+':
            try:
                float(value_if_allowed)
                return True
            except ValueError:
                return False
        else:
            return False
    
    def __init__(self, parent):

        top = self.top = Toplevel(parent)

        l = Label(top, text="point 1 X")
        l.grid(row=1, column=1)
        l.pack()

        vcmd = (top.register(self.numeric),
                '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')

        self.x1 = Entry(top, validate = 'key', validatecommand = vcmd)
        self.x1.grid(row=2, column=1)
        self.x1.pack(padx=5)

        self.d = Label(top, text="point 1 Y")
        self.d.grid(row=3, column=1)
        self.d.pack(padx=10)

        self.y1 = Entry(top, validate = 'key', validatecommand = vcmd)
        self.y1.grid(row=4, column=1)
        self.y1.pack(padx=15)

        self.l = Label(top, text="point 2 X")
        self.l.grid(row=5, column=1)
        self.l.pack(padx=20)

        self.x2 = Entry(top, validate = 'key', validatecommand = vcmd)
        self.x2.grid(row=6, column=1)
        self.x2.pack(padx=15)

        self.l1 = Label(top, text="point 2 Y")
        self.l1.grid(row=7, column=1)
        self.l1.pack(padx=20)

        self.y2 = Entry(top, validate = 'key', validatecommand = vcmd)
        self.y2.grid(row=8, column=1)
        self.y2.pack(padx=25)

        b = Button(top, text="OK", command=self.ok)
        b.pack(pady=5)
        top.bind('<Return>', self.ok)
        OPTIONS = [
            "left bound",
            "center",
            "right bound"
        ]
        self.var = StringVar(master)
        self.var.set(OPTIONS[1]) # default value

        self.w = apply(OptionMenu, (top, self.var) + tuple(OPTIONS))
        self.w.config(width=25)
        self.w.grid(row=9, column=1)
        self.w.pack()

    def ok(self, fail = 0):
        global canvas
        c  = str(self.var.get())
        v1x = int(self.x1.get())
        v1y = int(self.y1.get())
        v2x = int(self.x2.get())
        v2y = int(self.y2.get())
        if(c=='left bound'):
            cent = 1
        elif(c=='center'):
            cent = 2
        else:
            cent = 3
        co = (cor(v1x, 'mm', cent), cor(v1y, 'mm', cent), cor(v2x, 'mm', cent), cor(v2y, 'mm', cent))
        ov = canvas.create_line(*co, width=lineTh, activefill="yellow", tags='LINES')
        cur = currentf.getInstance()
        cur.addListLine(ov, center=cent)
        self.top.destroy()

class MyDialog:

    def numeric(self, action, index, value_if_allowed,
                       prior_value, text, validation_type, trigger_type, widget_name):
        if text in '0123456789.-+':
            try:
                float(value_if_allowed)
                return True
            except ValueError:
                return False
        else:
            return False
    
    def __init__(self, parent):

        top = self.top = Toplevel(parent)

        l = Label(top, text="radius")
        l.grid(row=1, column=1)
        l.pack()

        vcmd = (top.register(self.numeric),
                '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')

        self.r = Entry(top, validate = 'key', validatecommand = vcmd)
        self.r.grid(row=2, column=1)
        self.r.pack(padx=5)

        self.d = Label(top, text="center x")
        self.d.grid(row=3, column=1)
        self.d.pack(padx=10)

        self.x = Entry(top, validate = 'key', validatecommand = vcmd)
        self.x.grid(row=4, column=1)
        self.x.pack(padx=15)

        self.l = Label(top, text="center y")
        self.l.grid(row=5, column=1)
        self.l.pack(padx=20)

        self.y = Entry(top, validate = 'key', validatecommand = vcmd)
        self.y.grid(row=6, column=1)
        self.y.pack(padx=25)

        b = Button(top, text="OK", command=self.ok)
        b.pack(pady=5)
        top.bind('<Return>', self.ok)
        OPTIONS = [
            "outside",
            "center",
            "inside"
        ]
        self.var = StringVar(master)
        self.var.set(OPTIONS[1]) # default value

        self.w = apply(OptionMenu, (top, self.var) + tuple(OPTIONS))
        self.w.config(width=25)
        self.w.grid(row=7, column=1)
        self.w.pack()


    def ok(self, fail = 0):
        global canvas
        c = str(self.var.get())
        x = int(self.x.get())
        y = int(self.y.get())
        r = int(self.r.get())
        if(c=='outside'):
            cent = 1
        elif(c=='center'):
            cent = 2
        else:
            cent = 3
        rr = r
        #ov = canvas.create_oval(cor(x)-mes(r), cor(y)-mes(r), cor(x)+mes(r), cor(y)+mes(r),
        c = circle(x, y, r, 'mm', cent)
        cc = canvas.create_oval(c[0], c[1], c[2], c[3], width=lineTh, activeoutline="yellow", tags='CIRCLES')
        cur = currentf.getInstance()
        cur.addListCircle(cc, cx=x, cy=y, r=rr, center=cent)
        cur.logObList()
        #print "circle: r", self.r.get(), "x", self.x.get(), "y", self.y.get()
        self.top.destroy()

def createGrid(canvas): #TODO keep track of lines in grid for grid updates
    global half
    global yHalf
    half=0
    whole=0
    for i in range(gridSpacing, cWidth, gridSpacing):
        half=half+gridSpacing
        whole=whole+gridUnits
    yHalf=0
    half = math.floor(half/2)
    whole= math.floor(whole/2)
    yWhole=0
    for i in range(gridSpacing, cHeight, gridSpacing):
        yHalf=yHalf+gridSpacing
        yWhole=yWhole+gridUnits
    yWhole= math.floor(yWhole/2)
    yHalf = math.floor(yHalf/2)
    ii=0
    positive=False
    for i in range(gridSpacing, cWidth, gridSpacing):
        if(positive):
            ii=ii+gridUnits
            canvas.create_text(i, 0, anchor="n", text=str(ii), fill="grey", tags="grid")
        elif(i==half):
            positive=True
            ii=0
            canvas.create_text(i, 0, anchor="n", text="0", fill="grey", tags="grid")
        else:
            ii=ii+gridUnits
            canvas.create_text(i, 0, anchor="n", text="-"+str(int(whole-ii)), fill="grey", tags="grid")
        canvas.create_line(i, 15, i, cHeight, fill="grey", tags="grid")
    positive=False
    ii=0
    for i in range(gridSpacing, cHeight, gridSpacing):
        if(positive):
            ii=ii+gridUnits
            canvas.create_text(0, i, anchor="w", text=str(ii), fill="grey", tags="grid")
        elif(i==yHalf):
            positive=True
            ii=0
            canvas.create_text(0, i, anchor="w", text="0", fill="grey", tags="grid")
        else:
            ii=ii+gridUnits
            canvas.create_text(0, i, anchor="w", text="-"+str(int(yWhole-ii)), fill="grey", tags="grid")
        #canvas.create_text(i, 0, anchor="N", text=str(0-half), fill="grey")
        canvas.create_line(15, i, cWidth, i, fill="grey", tags="grid")

def unitify(r, u):#make mm!!!!?
    if(u=='in'):#TODO make cor use this
        r=r*25.4
    elif(u=='ft'):
        r=r*304.8
    elif(u=='cm'):
        r=r*10
    elif(u=='mm'):
        pass
    else:
        raise(errors.unknownUnit())
    return(r)

def uUnitify(r, u, c=2):#unmake mm because some people like their stinking imperial system!?!?!?!??!!?!??!!?!??!?!?????????
    dis = unitify(lineTH/2, u)#make sure to convert displacement to new unit
    if(c==1):
        pass
    elif(c==2):
        r=r-dis
    elif(c==3):
        r=r+dis
    else:
        pass #TODO error handling here
    if(u=='in'):#TODO make ucor use this
        r=r/25.4
    elif(u=='ft'):
        r=r/304.8
    elif(u=='cm'):
        r=r/10
    elif(u=='mm'):
        pass
    else:
        raise(errors.unknownUnit())
    if(c==1):
        pass
    elif(c==2):
        r=r+dis
    elif(c==3):
        r=r-dis
    #no else because error would have triggered else above
    return(r)

def circle(cx, cy, cr, xu='mm', c=2, yu='mm', ru='mm'):#check if unit is nessessary
    x = unitify(cx, xu)
    y = unitify(cy, yu)
    r = unitify(cr, ru)
    u='mm'
    if(c==2):
        return([cor(x-r, u, c), cor(y-r, u, c), cor(x+r, u, c), cor(y+r, u, c)])
    elif(c==1):
        return([cor(x-r, u, 1), cor(y-r, u, 1), cor(x+r, u, 3), cor(y+r, u, 3)])
    else:
        return([cor(x-r, u, 3), cor(y-r, u, 3), cor(x+r, u, 1), cor(y+r, u, 1)])
    

def uCircle(px1, py1, px2, py2, center=2, Id=0):
    cur = currentf.getInstance()
    itConf=0
    if(Id==0):
        itConf = cur.listConfig(selected[0])
    else:
        itConf = cur.listConfig(Id)
    cc = c = center
    
    if(center==2):
        x1 = ucor(px1, 'mm', c)
        y1 = ucor(py1, 'mm', c)
        x2 = ucor(px2, 'mm', c)
        y2 = ucor(py2, 'mm', c)
    elif(center==3):
        c=3
        x1 = ucor(px1, 'mm', c)
        y1 = ucor(py1, 'mm', c)
        c=1
        x2 = ucor(px2, 'mm', c)
        y2 = ucor(py2, 'mm', c)
    else:
        c=1
        x1 = ucor(px1, 'mm', c)
        y1 = ucor(py1, 'mm', c)
        c=3
        x2 = ucor(px2, 'mm', c)
        y2 = ucor(py2, 'mm', c)
    cx = x1+x2
    cx = cx/2 #find average or in this case middle
    cy = y1+y2
    cy = cy/2
    r=0
    if(x1>cx):
        r=uUnitify(x1-cx, itConf['ru'], c)
    else:
        if(c==1):
            r=uUnitify(x2-cx, itConf['ru'], 3)
        elif(c==3):
            r=uUnitify(x2-cx, itConf['ru'], 1)
        else:
            r=uUnitify(x2-cx, itConf['ru'], c)
    cx=uUnitify(cx, itConf['xu'])
    cy=uUnitify(cy, itConf['yu'])
    d = r*2
    cx = str(cx) + itConf['xu']
    cy = str(cy) + itConf['yu']
    r  = str(r)  + itConf['ru']
    d  = str(d)  + itConf['ru']
    return([cx, cy, r, d])

def createCircle(event=""):
    d = MyDialog(master)
    master.wait_window(d.top)

def createLine(event=""):
    d = lineDialog(master)
    master.wait_window(d.top)

def createArc(event=""):
    pass

def createHole(event=""):
    pass

def new(event=""):
    global canvas
    #del canvas.find_withtag(ALL)
    #TODO prompt are you sure then make sure to get rid of the old stuff
    createGrid(canvas)

def generate(event=""):
    file_opt = options = {}
    options['defaultextension'] = '.gcode'
    options['filetypes'] = [('gcode files', '.gcode'), ('all files', '.*')]
    options['initialdir'] = cnf.getSetting('defaultFolder')
    lst = cnf.lastFile()
    if(lst!=None):
        options['initialfile'] = cnf.lastFile().split('.')[0] + ".gcode"
    options['parent'] = master
    options['title'] = 'Export'
    file_path = tkFileDialog.asksavefilename(**file_opt)
    inOut.importSvg
    pass

def select(event=""):
    print("select")

def saveStuff(event=""):
    global newFile
    global master
    global canvas
    file_opt = options = {}
    options['defaultextension'] = '.j'
    options['filetypes'] = [('john code files', '.j')]
    options['initialdir'] = cnf.getSetting('defaultFolder')
    if(newFile!=True):
        options['initialfile'] = cnf.lastFile()
    options['parent'] = master
    options['title'] = 'Open'
    file_path = tkFileDialog.asksaveasfilename(**file_opt)
    inOut.save(file_path, canvas)
    newFile=False
    

def delete(event=""):
    if(event!=""):
        event.widget.config(relief=SUNKEN)
        print("key delete")

def performOpen(event=""):
    global master
    global canvas
    #master.withdraw()
    file_opt = options = {}
    options['defaultextension'] = '.j'
    options['filetypes'] = [('john code files', '.j'), ('all files', '.*'), ('text files', '.txt'), ('unsupported import', '.gcode')]
    options['initialdir'] = cnf.getSetting('defaultFolder')
    lst = cnf.lastFile()
    if(lst!=None):
        options['initialfile'] = lst
    options['parent'] = master
    options['title'] = 'Open'
    file_path = tkFileDialog.askopenfilename(**file_opt)#mode='r'
    #if(os
    name = file_path.split("\\")[len(file_path.split('\\'))-1]
    openFile = name              #save name of current file
    cnf.addRecent(name, file_path)
    #TODO save default folder if the working directory is not set in settings
    w = open(file_path, "r")
    inOut.imPorter(canvas, w)
    w.close()
    master.title('JDesigner '+name)

def createSomething(event): #control shift
    k = event.keycode
    if(k==67): #c
        createCircle()
    elif(k==76): #l
        createLine()
    elif(k==65): #a
        createArc()
    elif(k==83): #s
        pass #save as
    else:
        #print(k)
        pass
    master.bind('a', createArc)
    master.bind('l', createLine)
    master.bind('h', createHole)
    master.bind('d', delete)
    master.bind('n', new)
    master.bind('g', generate)

def ctrlSomething(event): #control held
    k = event.keycode
    if(k==83): #s
        pass
    elif(k==65): #a
        pass
    elif(k==78): #n
         new()
    elif(k==71): #g
        generate()
    elif(k==73): #i
        pass #import (maybe)
    elif(k==79): #o
        performOpen()
    elif(k==80): #p
        pass #prep 3d print
    elif(k==68): #d
        pass #deselect
    else:
        print(k)
        pass

def createWindow():
    global master
    global canvas
    global prop
    global propertiesPane
    master = Tk()
    master.title("JDesigner *New File*")
    mainframe = Frame(master)#padding="3 3 12 12")
    master.columnconfigure(0, weight=2)
    master.columnconfigure(1, weight=1)
    canvas = w = Canvas(mainframe, width=cWidth, height=cHeight, relief=SUNKEN, borderwidth=2, bg='white', takefocus=True)
    w.grid(row=1, column=0)
    #p = Frame(mainframe)
    #p.grid(row=0, column=1)
    #Label(p, text="hello").grid(row=0, column=0)
    bBar = Frame(mainframe)
    bBar.grid(row=0, column=0)
    newBut = Button(bBar, text="new", command=new)
    newBut.grid(row=1, column=1)
    openBut = Button(bBar, text="open", command=performOpen)
    openBut.grid(row=1, column=2)
    saveBut = Button(bBar, text="save", command=saveStuff)
    saveBut.grid(row=1, column=3)
    gnrtBut = Button(bBar, text="generate", command=generate)
    gnrtBut.grid(row=1, column=4)
    dsplBut = Button(bBar, text="display")
    dsplBut.grid(row=1, column=5)
    gridBut = Button(bBar, text="grid")
    gridBut.grid(row=1, column=6)
    slctBut = Button(bBar, text="select", command=select)
    slctBut.grid(row=1, column=7)
    deltBut = Button(bBar, text="delete", command=delete)
    deltBut.grid(row=1, column=8)
    crclBut = Button(bBar, text="circle", command=createCircle)
    crclBut.grid(row=1, column=9)
    arcBut = Button(bBar, text="arc", command=createArc)
    arcBut.grid(row=1, column=10)
    lineBut = Button(bBar, text="line", command=createLine)
    lineBut.grid(row=1, column=11)
    holeBut = Button(bBar, text="hole", command=createHole)
    holeBut.grid(row=1, column=12)
    #bBar.pack()
    createGrid(w);
    #w.create_arc(10, 10, 200, 100, outline="black", width=5, extent=180, style=ARC);
    #w.create_line(0, 100, 200, 0, fill="black");
    #w.create_rectangle(50, 25, 150, 75, fill="black")
    #i= w.create_line(xy)
    #w.cords(i, new_xy)
    #w.delete(i)
    #w.delete(ALL)
    #p.pack()
    master.bind('<Control-Shift-Key>', createSomething)
    master.bind('<Control-Key>', ctrlSomething)
    master.bind('<Button-1>', click)
    master.bind('<Up>', move)
    master.bind('<Down>', move)
    master.bind('<Left>', move)
    master.bind('<Right>', move)
    #master.bind('<configure>' resize) #todo resize preformed
    w.bind('<Enter>', inM)
    w.bind('<Leave>', outM)
    mainframe.grid(row=0, column=0)
    n = ttk.Notebook(master)
    prop = f1 = ttk.Frame(n, width=cWidth/2, height=cHeight); # first page, which would get widgets gridded into it
    f2 = ttk.Frame(n, width=cWidth/2, height=cHeight); # second page
    #fe.grid(row=1, column=1)
    propertiesPane = ttk.Frame(f1, width=cWidth/2, height=cHeight)
    frame = ttk.Labelframe(propertiesPane, text="properties")
    Label(frame, text="label1").grid(row=1, column=1)
    ttk.Separator(frame, orient=HORIZONTAL).grid(row=2, column=1)
    Label(frame, text="label2").grid(row=3, column=1)
    frame.grid(row=0, column=0)
    propertiesPane.grid(row=0, column=0)
    n.add(f1, text='properties')
    n.add(f2, text='shit goes here')
    n.grid(row=0, column=1)
    fe = editDoc(f2)
    fe.pack()
    #master.update()
    #d = properties(master)
    master.mainloop()
def editLine(master):
    top = Frame(master)
    vcmd1 = (top.register(numeric),
            '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W', 0)
    vcmd2 = (top.register(numeric),
            '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W', 1)
    vcmd3 = (top.register(numeric),
            '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W', 2)
    vcmd4 = (top.register(numeric),
            '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W', 3)
    coords = canvas.coords(selected)
    vx1 = StringVar()
    vy1 = StringVar()
    vx2 = StringVar()
    vy2 = StringVar()
    
    fl = Label(top, text="point 1 X")
    fl.grid(row=1, column=1)
    fl.pack(padx=5)
    
    x1 = Entry(top, validate = 'key', textvariable=vx1)
    x1.grid(row=2, column=1)
    x1.pack(padx=5)

    d = Label(top, text="point 1 Y")
    d.grid(row=3, column=1)
    d.pack(padx=10)

    y1 = Entry(top, validate = 'key', textvariable=vy1)
    y1.grid(row=4, column=1)
    y1.pack(padx=15)

    l = Label(top, text="point 2 X")
    l.grid(row=5, column=1)
    l.pack(padx=20)

    x2 = Entry(top, validate = 'key', textvariable=vx2)
    x2.grid(row=6, column=1)
    x2.pack(padx=15)

    l1 = Label(top, text="point 2 Y")
    l1.grid(row=7, column=1)
    l1.pack(padx=20)

    y2 = Entry(top, validate = 'key', textvariable=vy2)
    y2.grid(row=8, column=1)
    y2.pack(padx=25)

    OPTIONS = [
        "left bound",
        "center",
        "right bound"
    ]
    var = StringVar(master)
    cur = currentf.getInstance()
    itConf = cur.listConfig(selected[0])
    cent = itConf['center']
    del itConf
    var.set(OPTIONS[cent-1]) # default value
    var.trace("w", lambda name, index, mode, var=var, ob=selected: centerChange(var, ob))
    w = apply(OptionMenu, (top, var) + tuple(OPTIONS))
    w.config(width=25)
    w.grid(row=9, column=1)
    w.pack()
    top.grid(row=0, column=0)
    vx1.set(ucor(coords[0], 'mm', cent))
    vy1.set(ucor(coords[1], 'mm', cent))
    vx2.set(ucor(coords[2], 'mm', cent))
    vy2.set(ucor(coords[3], 'mm', cent))
    x1.config(validatecommand = vcmd1)
    y1.config(validatecommand = vcmd2)
    x2.config(validatecommand = vcmd3)
    y2.config(validatecommand = vcmd4)
    return(top)

def editCircle(master):
    global selectedOps
    global canvas
    top = Frame(master)
    vx = StringVar()
    vy = StringVar()
    vr = StringVar()
    dd = [vx, vy, vr]
    vcmd1 = (top.register(numeric),
            '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W', 0, '1')
    vcmd2 = (top.register(numeric),
            '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W', 1, '1')
    vcmd3 = (top.register(numeric),
            '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W', 2, '1')
    coords = canvas.coords(selected)
    fl = Label(top, text="center X")
    fl.grid(row=1, column=1)
    fl.pack(padx=5)
    
    x = Entry(top, validate = 'key', textvariable=vx)
    x.grid(row=2, column=1)
    x.pack(padx=5)

    d = Label(top, text="center Y")
    d.grid(row=3, column=1)
    d.pack(padx=10)

    y = Entry(top, validate = 'key', textvariable=vy)
    y.grid(row=4, column=1)
    y.pack(padx=15)

    l = Label(top, text="Radius")
    l.grid(row=5, column=1)
    l.pack(padx=20)

    r = Entry(top, validate = 'key', textvariable=vr)
    r.grid(row=6, column=1)
    r.pack(padx=15)
    top.grid(row=0, column=0)
    OPTIONS = [
        "outside",
        "center",
        "inside"
    ]
    var = StringVar(master)
    w = apply(OptionMenu, (top, var) + tuple(OPTIONS))
    w.config(width=25)
    w.grid(row=7, column=1)
    w.pack()
    print(str(selected))
    cur = currentf.getInstance()
    itConf = cur.listConfig(selected[0])
    var.set(OPTIONS[itConf['center']-1]) # default value
    var.trace("w", lambda name, index, mode, var=var, ob=selected: centerChange(var, ob))
    vals = uCircle(coords[0], coords[1], coords[2], coords[3], itConf['center'])
    vx.set(vals[0])
    vy.set(vals[1])
    vr.set(vals[2])
    selectedOps = vals
    x.config(validatecommand = vcmd1)
    y.config(validatecommand = vcmd2)
    r.config(validatecommand = vcmd3)
    return(top)

def centerChange(var, ob):
    global canvas
    c = var.get()
    cent = 0
    if(c=="center"):
        cent=2
    elif(c=='inside'):
        cent=3
    else:
        cent=1
    del c
    cur = currentf.getInstance()
    e = cur.listConfig(ob[0])
    oc = e['center']
    del e
    cur.listConfig(ob[0], center=cent)
    c = canvas.coords(ob)
    ncord = uCircle(c[0], c[1], c[2], c[3], oc)
    ncoord = circle(ncord[0], ncord[1], ncord[2], 'mm', cent)
    canvas.coords(ob, ncoord[0], ncoord[1], ncoord[2], ncoord[3])

def editDoc(master):
    top = Frame(master)
    vcmd1 = (top.register(numeric),
            '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W', 0, '2')
    vcmd2 = (top.register(numeric),
            '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W', 0, '3')
    vcmd3 = (top.register(numeric),
            '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W', 0, '4')
    l1 = Label(top, text="document name") #TODO listener
    l1.grid(row=1, column=1, columnspan=1)
    
    nM = Entry(top)
    nM.grid(row=2, column=1, columnspan=1)

    l2 = Label(top, text="size X/Y")
    l2.grid(row=3, column=1, columnspan=1)

    sz = Entry(top, validate = 'key', validatecommand = vcmd1)
    sz.grid(row=4, column=1, columnspan=1)

    l3 = Label(top, text="scale")
    l3.grid(row=5, column=1, columnspan=1)

    l4 = Label(top, text="1:")
    l4.grid(row=6, column=1)#, weight=1)

    #sc = Entry(top, validate = 'key', validatecommand = vcmd2)
    #sc.grid(row=6, column=2)

    l5 = Label(top, text="bit radius")
    l5.grid(row=7, column=1, columnspan=1)

    bw = Entry(top, validate = 'key', validatecommand = vcmd3)
    bw.grid(row=8, column=1, columnspan=1)

    l6 = Label(top, text="home location")
    l6.grid(row=9, column=1, columnspan=1)

    #TODO have entry here

    #TODO entry ofset

    #TODO home center of bit

    #TODO home before begining
    return(top)
    

lineTh=mes(lineTH) #line thickness
                                
if(__name__=="__main__"):
    cc = currentf.getInstance()
    print(cc.spam())
    print(inOut.spam())
    createWindow()
else:
    global half
    global yHalf
    half=0
    whole=0
    for i in range(gridSpacing, cWidth, gridSpacing):
        half=half+gridSpacing
        whole=whole+gridUnits
    yHalf=0
    half = math.floor(half/2)
    whole= math.floor(whole/2)
    yWhole=0
    for i in range(gridSpacing, cHeight, gridSpacing):
        yHalf=yHalf+gridSpacing
        yWhole=yWhole+gridUnits
    yWhole= math.floor(yWhole/2)
    yHalf = math.floor(yHalf/2)

def is_within(point, circle):
    distance = math.sqrt(((point.x - circle.x) ** 2) + 
                    ((point.y - circle.y) ** 2))
    return distance < 3 #circlerad
