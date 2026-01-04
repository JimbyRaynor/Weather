from tkinter import *
import weather
from weatherLEDanimations import *
from time import *
import os

import sys

SHOWWEATHER  = True  #  False for fast debugging

# for loading files (.png, .txt), set current directory = location of this python script (needed for Linux)
current_script_directory = os.path.dirname(os.path.abspath(__file__))
os.chdir(current_script_directory)


class GameObject:
    def __init__(self,filelist,x=0,y=0):
        self.x = x
        self.y = y
        self.imagelist = []
        for myfile in filelist:
            self.imagelist.append(PhotoImage(file=myfile))
        self.sprite = canvas1.create_image(1,1,image=self.imagelist[0])
        canvas1.move(self.sprite,x,y)
    def move(self,dx=0,dy=0):
        self.x = self.x + dx
        self.y = self.y + dy
        canvas1.move(self.sprite,dx,dy)     
    def changeimage(self,imagenum):
        canvas1.itemconfigure(self.sprite,image=self.imagelist[imagenum])


mainwin = Tk()
mainwin.geometry("1277x1050+0+0") # window is at x=1, y=1 on screen (top left)
canvas1 = Canvas(mainwin,width=1920,height= 1080,bg="black")
canvas1.place(x=0,y=0)

iconlist = ["sun.png","Showers.png","PartlyCloudy.png","Cloudy.png","Rain.png"]

xmaslist = ["Themes/Tree.png", "Themes/House1.png","Themes/Santa1.png"]
xmaslocX = 1200
xmaslocY = 300

iconlistsmall = ["sunsmall.png","Showerssmall.png","PartlyCloudysmall.png","Cloudysmall.png","Rainsmall.png"]

StationNameList = ["Melbourne", "Scoresby"]
StationIndex = 1


#spritecloud3 = GameObject("Showers.png",x=500,y=30)
dy = 30
spriteForcast0 = GameObject(iconlist,x=500,y=30+dy)
spriteForcast1 = GameObject(iconlistsmall,x=350,y=195+dy)
spriteForcast2 = GameObject(iconlistsmall,x=350,y=295+dy)
spriteForcast3 = GameObject(iconlistsmall,x=350,y=395+dy)
spriteForcast4 = GameObject(iconlistsmall,x=350,y=495+dy)
spriteForcast5 = GameObject(iconlistsmall,x=350,y=595+dy)
spriteForcast6 = GameObject(iconlistsmall,x=350,y=695+dy)

#spriteTheme = GameObject(xmaslist,x=xmaslocX+200,y=xmaslocY+200)

fontbig = ("Arial",70)
fontmedium = ("Arial",45)
fontsmall = ("Arial",26)
fontsmall2 = ("Arial",22)
fonttiny = ("Courier",11)
fonttiny2 = ("Arial",18)
mytemptext = canvas1.create_text(300,40+dy,font=fontbig,text="temp",fill="yellow")
myraintext = canvas1.create_text(800,120+dy,font=fontsmall,text="rain summary",fill="#4343D3")
day0summary = canvas1.create_text(600,50+dy,font=fontsmall,text="summary",anchor="w",fill="#6B6BEE")
day1summary = canvas1.create_text(390,200+dy,font=fontsmall,text="summary1",anchor="w",fill="#7373DD")
day2summary = canvas1.create_text(390,300+dy,font=fontsmall,text="summary2",anchor="w",fill="#7373DD")
day3summary = canvas1.create_text(390,400+dy,font=fontsmall,text="summary3",anchor="w",fill="#7373DD")
day4summary = canvas1.create_text(390,500+dy,font=fontsmall,text="summary4",anchor="w",fill="#7373DD")
day5summary = canvas1.create_text(390,600+dy,font=fontsmall,text="summary4",anchor="w",fill="#7373DD")
day6summary = canvas1.create_text(390,700+dy,font=fontsmall,text="summary4",anchor="w",fill="#7373DD")

StationLabel = canvas1.create_text(10,70,font=fontsmall2,text=StationNameList[StationIndex],anchor="w",fill="#7373DD")
StationtimeLabel = canvas1.create_text(30,100,font=fonttiny,text="Updated",anchor="w",fill="#7373DD")

daynames = [0]
for i in range(1,7):
   daynames.append(canvas1.create_text(20,100+100*i+dy,font=fontsmall,text=f"day{i}",anchor="w",fill="#DDDB73"))

maxtemps = [0]
for i in range(1,7):
   maxtemps.append(canvas1.create_text(230,100+100*i+dy,font=fontsmall,text=f"max{i}",anchor="w",fill="#F7F308"))

daylist = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]

def chooseicon(myspriteobject, textinfo):
     myspriteobject.changeimage(0) # default to sun
     if "shower" in  textinfo: myspriteobject.changeimage(1)
     if "cloudy" in  textinfo: myspriteobject.changeimage(3)
     if "partly cloudy" in  textinfo: myspriteobject.changeimage(2)
     if "rain" in  textinfo: myspriteobject.changeimage(4)
     
def normalize(values, height, padding):
    min_val = min(values)
    max_val = max(values)
    if max_val - min_val > 0:
      scale = (height - 2 * padding) / (max_val - min_val)
    else:
      scale = height
    return [(height - padding - (v - min_val) * scale) for v in values]

listtemp = []
listtime = []
listwind = []
maxObsN = 60 # max number of observations  ... updated in drawgraph

def safe_float(value):
  try:
     return int(value)
  except (ValueError, TypeError):
     return 0

def drawgraph():
  global maxObsN
  canvas_width = 1900
  canvas_height = 400
  padding = 40
  rowobs = weather.fetchALL_melbourne_observation()
  if rowobs == None: return
  rows = []
  i = 0
  for row in rowobs:
   if i >= 1 and i <= 100 and row[0] != '':
      if i <= 30:
        rows.append((row[0],row[1],row[6]))
      elif i% 2 == 0:
        rows.append((row[0],row[1],row[6]))
   i = i + 1
  maxObsN = len(rows) 
  times = [row[0] for row in rows]
  temps = [safe_float(row[1]) for row in rows]
  winds = [row[2] for row in rows]
  temp_y = normalize(temps, canvas_height, padding)
  x_spacing = (canvas_width - 2 * padding) / (len(rows) - 1)
  x_coords = [padding + i * x_spacing for i in range(len(rows))]

  for i, time in enumerate(times):
    listtime.append(canvas1.create_text(1900-x_coords[i], 815+temp_y[i]/2, text=time, angle=90, anchor="nw",fill="blue" ,font=("Arial", 10)))
    tempcolour = "yellow"
    if i % 2 == 0: tempcolour = "white"
    listtemp.append(canvas1.create_text(1910-x_coords[i], 825+temp_y[i]/2, text=str(temps[i])+"°C",fill=tempcolour ,font=("Arial", 10)))
    listwind.append(canvas1.create_text(1910-x_coords[i], 835+temp_y[i]/2, text=winds[i],fill="light blue" ,font=("Arial", 6)))
    
def updategraph():
  canvas_width = 1900
  canvas_height = 400
  padding = 40
  rowobs = weather.fetchALL_melbourne_observation()
  if rowobs == None: return
  rows = []
  i = 0
  for row in rowobs:
   if i >= 1 and i <= 100 and row[0] != '':
      if i <= 30:
        rows.append((row[0],row[1],row[6]))
      elif i% 2 == 0:
        rows.append((row[0],row[1],row[6]))
   i = i + 1
  print("Number of temperature observations = ",len(rows)) 
  times = [row[0] for row in rows]
  temps = [safe_float(row[1]) for row in rows]
  winds = [row[2] for row in rows]
  temp_y = normalize(temps, canvas_height, padding)
  x_spacing = (canvas_width - 2 * padding) / (len(rows) - 1)
  x_coords = [padding + i * x_spacing for i in range(len(rows))]

  for i, time in enumerate(times):
    if i < maxObsN:
      canvas1.itemconfigure(listtime[i],text= time)
      canvas1.coords(listtime[i],1900-x_coords[i], 815+temp_y[i]/2)
      canvas1.itemconfigure(listtemp[i],text= temps[i])
      canvas1.coords(listtemp[i],1910-x_coords[i], 825+temp_y[i]/2)
      canvas1.itemconfigure(listwind[i],text= winds[i])
      canvas1.coords(listwind[i],1910-x_coords[i], 838+temp_y[i]/2)


def timer1():
    t = localtime()
    daynumber = t.tm_wday
    forecasts = weather.fetch_bom_forecast()
    if forecasts == None:
      mainwin.after(60000,timer1)
      return
    for i in range(1,7):
     canvas1.itemconfigure(daynames[i],text= daylist[daynumber+i])
    for i in range(1,7):
      canvas1.itemconfigure(maxtemps[i],text= forecasts[i][1]+"°C")
    weatherobserve = weather.fetch_melbourne_observation_name(StationNameList[StationIndex])
    if weatherobserve == None:
       mainwin.after(60000,timer1)
       return
    (temp, apparent,wind, humidity, rain,time) = weatherobserve
    canvas1.itemconfigure(mytemptext,text= temp+"°")
    canvas1.itemconfigure(myraintext,text=f"Feels like: {apparent}°C | 🌬️ Wind: {wind} km/h | 💧 Humidity: {humidity}% | 💧 rain: {rain}mm")
    canvas1.itemconfigure(StationtimeLabel,text = time)

    (precip, maxtemp, mintemp,summary) = forecasts[0]
    chooseicon(spriteForcast0, summary.lower())
    if precip != "0mm":
      canvas1.itemconfigure(day0summary,text=summary+" "+precip+" rain. Max "+maxtemp+"°C"+". Min "+mintemp+"°C")
    else:
      canvas1.itemconfigure(day0summary,text=summary+" Max "+maxtemp+"°C"+". Min "+mintemp+"°C")
    (precip, maxtemp,mintemp, summary) = forecasts[1]
    chooseicon(spriteForcast1, summary.lower())
    canvas1.itemconfigure(day1summary,text=summary+" "+precip+" rain. Min "+mintemp+"°C")
    
    (precip, maxtemp, mintemp, summary) = forecasts[2]
    chooseicon(spriteForcast2, summary.lower())
    canvas1.itemconfigure(day2summary,text=summary+" "+precip+" rain. Min "+mintemp+"°C")

    (precip, maxtemp, mintemp, summary) = forecasts[3]
    chooseicon(spriteForcast3, summary.lower())
    canvas1.itemconfigure(day3summary,text=summary+" "+precip+" rain. Min "+mintemp+"°C")

    (precip, maxtemp, mintemp, summary) = forecasts[4]
    chooseicon(spriteForcast4, summary.lower())
    canvas1.itemconfigure(day4summary,text=summary+" "+precip+" rain. Min "+mintemp+"°C")

    (precip, maxtemp, mintemp, summary) = forecasts[5]
    chooseicon(spriteForcast5, summary.lower())
    canvas1.itemconfigure(day5summary,text=summary+" "+precip+" rain. Min "+mintemp+"°C")

    (precip, maxtemp, mintemp, summary) = forecasts[6]
    chooseicon(spriteForcast6, summary.lower())
    canvas1.itemconfigure(day6summary,text=summary+" "+precip+" rain. Min "+mintemp+"°C")
    updategraph()
   
    mainwin.after(15*60000,timer1)

if SHOWWEATHER  == True: 
   drawgraph()
   timer1()

def onSpaceKey(event):
   global StationIndex
   StationIndex = StationIndex + 1
   if StationIndex >= len(StationNameList):
      StationIndex = 0
   weatherobserve = weather.fetch_melbourne_observation_name(StationNameList[StationIndex])
   if weatherobserve == None:
       mainwin.after(60000,timer1)
       return
   (temp, apparent,wind, humidity, rain,time) = weatherobserve
   canvas1.itemconfigure(mytemptext,text= temp+"°")
   canvas1.itemconfigure(myraintext,text=f"Feels like: {apparent}°C | 🌬️ Wind: {wind} km/h | 💧 Humidity: {humidity}% | 💧 rain: {rain}mm")
   canvas1.itemconfig(StationLabel, text = StationNameList[StationIndex])
   canvas1.itemconfigure(StationtimeLabel,text = time)



angle = 0
dangle = 1
presentlist = []
stackx = xmaslocX+80
stacky = xmaslocY+320

def stackpresent(thispresent):
   global stackx, stacky
   thispresent.resetposition(stackx,stacky)
   stackx = stackx + 40
   if stackx >= xmaslocX+80+240:
      stackx = xmaslocX+80
      stacky = stacky - 30
   presentlist.append(thispresent)
   if stacky < xmaslocY+280:
      for box in presentlist:
         box.undraw()
      presentlist.clear()
      stackx = xmaslocX+80
      stacky = xmaslocY+320

def animationtimer():
    global angle, charStars, mystars, dangle, mypresent
    angle = angle + dangle
    if angle == 6: dangle = -1
    if angle == -6: dangle = 1
    myship.rotate(angle)
    mystars.undraw()
    del mystars
    charStars = cycle_star_colours(charStars)
    mystars = LEDobj(canvas1,1100,0,dx = 0,dy = 0,CharPoints=charStars, pixelsize = 4)
    #mypresent.move()
    #if mypresent.y <= 730:
       #stackpresent(mypresent)
       #mypresent = LEDobj(canvas1,xmaslocX+170,xmaslocY+600,dx = 0,dy = -1,CharPoints=charPresent1, pixelsize = 2)
    mainwin.after(200,animationtimer)

myship = LEDobj(canvas1,xmaslocX+170,xmaslocY+400,dx = 0,dy = 0,CharPoints=charRaymond, pixelsize = 2)
mystars = LEDobj(canvas1,1000,0,dx = 0,dy = 0,CharPoints=charStars, pixelsize = 4)

#mypresent = LEDobj(canvas1,xmaslocX+170,xmaslocY+600,dx = 0,dy = -1,CharPoints=charPresent1, pixelsize = 2)
#mypresentseat = LEDobj(canvas1,xmaslocX+170,730,dx = 0,dy = 0,CharPoints=charPresent1, pixelsize = 2)

def on_click(event):
   print(f"x={event.x} and y={event.y}")
   coords = f"{event.x},{event.y}\n"
   charStars.append((event.x/4-276,event.y/4-1,'red'))
   #print(charStars)
   #with open("lights.txt","a") as f:
   #          f.write(coords)


animationtimer()


mainwin.bind("<space>", onSpaceKey)
mainwin.bind("<Button-1>", on_click)
mainwin.mainloop() 