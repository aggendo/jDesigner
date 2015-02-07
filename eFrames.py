from Tkinter import *
def numeric(action, index, value_if_allowed,
                       prior_value, text, validation_type, trigger_type, widget_name, coHo=""):
    global selected
    global canvas
    if text in '0123456789.-+':
        try:
            if(coHo!=""):
                coords = canvas.coords(selected)
                coords[int(coHo)] = cor(float(value_if_allowed))
                canvas.coords(selected, coords[0], coords[1], coords[2], coords[3])
            else:
                float(value_if_allowed)
            return True
        except ValueError:
            return False
    else:
        return False
def cor(x):
    ratio = gridSpacing/gridUnits
    nX=0
    if(x==0):
        return(half)
    if(x<0):
        return(x*ratio)
    else:
        nX=half
        eX=x*ratio
        return(nX+eX)

def ucor(x):
    ratio = gridSpacing/gridUnits
    nX=0
    if(x==half):
        return(0.0)
    if(x<half):
        pX = x/ratio
        return(0-pX)
    else:
        nX=x-half
        return(nX/ratio)
