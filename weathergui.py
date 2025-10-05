from tkinter import *
import weather
from time import *
import os

import sys

# for loading files (.png, .txt), set current directory = location of this python script (needed for Linux)
current_script_directory = os.path.dirname(os.path.abspath(__file__))
os.chdir(current_script_directory)


class GameObject:
    def __init__(self,file1="",file2="",file3="",file4="",x=0,y=0):
        self.x = x
        self.y = y
        self.image = PhotoImage(file=file1)
        self.sprite = canvas1.create_image(2,2,image=self.image)
        if file2 != "":
           self.image2 = PhotoImage(file=file2)
        if file3 != "":
           self.image3 = PhotoImage(file=file3)
        if file4 != "":
           self.image4 = PhotoImage(file=file4)
        canvas1.move(self.sprite,x,y)
    def move(self,dx=0,dy=0):
        self.x = self.x + dx
        self.y = self.y + dy
        canvas1.move(self.sprite,dx,dy)     
    def changeimage(self,imagenum):
         if imagenum == 0:
           canvas1.itemconfigure(self.sprite,image=self.image)
         elif imagenum == 1:
           canvas1.itemconfigure(self.sprite,image=self.image2)
         elif imagenum == 2:
           canvas1.itemconfigure(self.sprite,image=self.image3)
         elif imagenum == 3:
           canvas1.itemconfigure(self.sprite,image=self.image4)
         else: print("Error: add to change image")


mainwin = Tk()
mainwin.geometry("1600x900+1+1") # window is at x=1, y=1 on screen (top left)
canvas1 = Canvas(mainwin,width=1920,height= 1080,bg="black")
canvas1.place(x=0,y=0)


#spritecloud3 = GameObject("Showers.png",x=500,y=30)
spriteForcast0 = GameObject("sun.png","Showers.png","PartlyCloudy.png","Cloudy.png",x=500,y=30)
spriteForcast1 = GameObject("sunsmall.png","Showerssmall.png","PartlyCloudysmall.png","Cloudysmall.png",x=350,y=195)
spriteForcast2 = GameObject("sunsmall.png","Showerssmall.png","PartlyCloudysmall.png","Cloudysmall.png",x=350,y=295)
spriteForcast3 = GameObject("sunsmall.png","Showerssmall.png","PartlyCloudysmall.png","Cloudysmall.png",x=350,y=395)
spriteForcast4 = GameObject("sunsmall.png","Showerssmall.png","PartlyCloudysmall.png","Cloudysmall.png",x=350,y=495)
spriteForcast5 = GameObject("sunsmall.png","Showerssmall.png","PartlyCloudysmall.png","Cloudysmall.png",x=350,y=595)
spriteForcast6 = GameObject("sunsmall.png","Showerssmall.png","PartlyCloudysmall.png","Cloudysmall.png",x=350,y=695)

fontbig = ("Arial",70)
fontmedium = ("Arial",45)
fontsmall = ("Arial",26)
fonttiny = ("Courier",11)
fonttiny2 = ("Arial",18)
mytemptext = canvas1.create_text(300,40,font=fontbig,text="temp",fill="yellow")
myraintext = canvas1.create_text(800,110,font=fontsmall,text="rain summary",fill="#4343D3")
myupdatedtext = canvas1.create_text(1400,850,font=fonttiny2,text="updated",fill="yellow")
day0summary = canvas1.create_text(600,50,font=fontsmall,text="summary",anchor="w",fill="#6B6BEE")
day1summary = canvas1.create_text(390,200,font=fontsmall,text="summary1",anchor="w",fill="#7373DD")
day2summary = canvas1.create_text(390,300,font=fontsmall,text="summary2",anchor="w",fill="#7373DD")
day3summary = canvas1.create_text(390,400,font=fontsmall,text="summary3",anchor="w",fill="#7373DD")
day4summary = canvas1.create_text(390,500,font=fontsmall,text="summary4",anchor="w",fill="#7373DD")
day5summary = canvas1.create_text(390,600,font=fontsmall,text="summary4",anchor="w",fill="#7373DD")
day6summary = canvas1.create_text(390,700,font=fontsmall,text="summary4",anchor="w",fill="#7373DD")

daynames = [0]
for i in range(1,7):
   daynames.append(canvas1.create_text(20,100+100*i,font=fontsmall,text=f"day{i}",anchor="w",fill="#DDDB73"))

maxtemps = [0]
for i in range(1,7):
   maxtemps.append(canvas1.create_text(230,100+100*i,font=fontsmall,text=f"max{i}",anchor="w",fill="#F7F308"))

daylist = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]

def chooseicon(myspriteobject, textinfo):
     myspriteobject.changeimage(0) # default to sun
     if "shower" in  textinfo or "rain" in  textinfo: myspriteobject.changeimage(1)
     if "cloudy" in  textinfo: myspriteobject.changeimage(3)
     if "partly cloudy" in  textinfo: myspriteobject.changeimage(2)
     

def timer1():
    t = localtime()
    daynumber = t.tm_wday
    forecasts = weather.fetch_bom_forecast()
    for i in range(1,7):
       canvas1.itemconfigure(daynames[i],text= daylist[daynumber+i])
    for i in range(1,7):
       canvas1.itemconfigure(maxtemps[i],text= forecasts[i][1]+"°C")
    (temp, apparent,wind, humidity, rain,time) = weather.fetch_melbourne_observation()
    canvas1.itemconfigure(mytemptext,text= temp+"°")
    canvas1.itemconfigure(myraintext,text=f"Feels like: {apparent}°C | 🌬️ Wind: {wind} km/h | 💧 Humidity: {humidity}% | 💧 rain: {rain}mm")
    canvas1.itemconfigure(myupdatedtext,text=f"🕒 Updated: {time}")
    
    (precip, maxtemp, mintemp,summary) = forecasts[0]
    chooseicon(spriteForcast0, summary.lower())
    canvas1.itemconfigure(day0summary,text=summary+" "+precip+" rain. Max "+maxtemp+"°C"+". Min "+mintemp+"°C")
    
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
    mainwin.after(60000,timer1)


timer1()


mainwin.mainloop() 