import json, math

def pos(x): return isinstance(x,(int,float)) and math.isfinite(x) and x>0
def num(x): return isinstance(x,(int,float)) and math.isfinite(x)
def jround(x): return math.floor(x+0.5)
def jsnum(x):
    if isinstance(x,float) and x==int(x): return str(int(x))
    return str(x)
def r1(x): return jround(x*10)/10

MONO={"6":0.23,"8":0.25,"10":0.28,"12":0.31,"14":0.33,"17":0.36,"20":0.41}
BRAID={"8":0.13,"10":0.15,"15":0.19,"20":0.23,"30":0.28,"40":0.32,"50":0.36}
FLUORO={"8":0.26,"10":0.29,"12":0.32,"15":0.35,"20":0.41}
TABLES={"mono":MONO,"braid":BRAID,"fluoro":FLUORO}

def capacity_plan(spoolYd,spoolLb,lineType,lineLb):
    if not pos(spoolYd): return {"error":"the spool yardage must be above zero"}
    if spoolLb not in MONO: return {"error":"pick the sticker's line test"}
    if lineType not in TABLES: return {"error":"pick a line type"}
    if lineLb not in TABLES[lineType]: return {"error":"pick your line's test"}
    return {"yd":r1(spoolYd*(MONO[spoolLb]/TABLES[lineType][lineLb])**2)}

def render_capacity(r,spoolYd,spoolLb,lineType,lineLb):
    return ("Your "+jsnum(spoolYd)+" yd / "+spoolLb+" lb spool holds about "+jsnum(r["yd"])+" yds of "+lineLb
            +" lb "+lineType+" - the sticker line was mono, and the spool never read the box.")

def window_plan(lure,lo,hi):
    if not pos(lure) or not pos(lo) or not pos(hi): return {"error":"ounces must all be above zero"}
    if lo>=hi: return {"error":"the window's low end must sit under its high end"}
    v="under" if lure<lo else ("over" if lure>hi else "inside")
    return {"verdict":v}

def render_window(r,lure,lo,hi):
    if r["verdict"]=="inside":
        return ("Your "+jsnum(lure)+" oz lure sits inside the rod's "+jsnum(lo)+"-"+jsnum(hi)
                +" oz window - the blank loads the way the sticker promised.")
    if r["verdict"]=="under":
        return ("Your "+jsnum(lure)+" oz lure never reaches the "+jsnum(lo)
                +" oz bottom of the rod's window - the blank barely bends, and the cast dies early.")
    return ("Your "+jsnum(lure)+" oz lure is past the "+jsnum(hi)
            +" oz top of the rod's window - the blank folds instead of loading, and the cast dies early.")

def sinker_plan(depth,current):
    if not pos(depth): return {"error":"the depth must be above zero"}
    if not num(current) or current<0: return {"error":"the current must be zero or more"}
    oz=depth*current/10
    if oz<=0: oz=0.25
    return {"oz":r1(oz)}

def render_sinker(r,depth,current):
    return ("Your "+jsnum(depth)+" ft at "+jsnum(current)+" mph figures about "+jsnum(r["oz"])
            +" oz of lead - the quarter-ounce drawer belongs to a lake at dawn.")

cases=[]
def add(tool,args):
    if tool=="capacity": r=capacity_plan(*args); fn=render_capacity
    elif tool=="window": r=window_plan(*args); fn=render_window
    else: r=sinker_plan(*args); fn=render_sinker
    case={"tool":tool,"args":args,"result":r}
    if "error" not in r: case["render"]=fn(r,*args)
    cases.append(case)

for a in [(200,"10","braid","20"),(200,"10","braid","10"),(150,"8","mono","12"),(250,"12","fluoro","15"),(300,"14","braid","30"),(100,"6","braid","8"),(200,"10","mono","10"),(150,"10","braid","50")]:
    add("capacity",a)
for a in [(0.5,0.375,0.75),(1,0.375,0.75),(0.25,0.375,0.75),(0.75,0.375,0.75),(0.375,0.375,0.75),(2,1,3),(0.75,1,3),(3.5,1,3)]:
    add("window",a)
for a in [(12,1.5),(8,1),(20,2),(15,0.5),(30,2.5),(10,3),(25,0),(6,1.2)]:
    add("sinker",a)
add("capacity",[0,"10","braid","20"]); add("capacity",[200,"10","wire","20"]); add("window",[0.5,0.75,0.375]); add("window",[0,0.375,0.75]); add("sinker",[0,1])

json.dump(cases,open("expected.json","w"),separators=(",",":"))
print(len(cases),"cases")
