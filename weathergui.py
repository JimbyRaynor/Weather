from tkinter import *
import weather
from time import *


mainwin = Tk()
mainwin.geometry("1600x900+1+1") # window is at x=1, y=1 on screen (top left)
canvas1 = Canvas(mainwin,width=1600,height= 900,bg="black")
canvas1.place(x=0,y=0)

fontbig = ("Arial",70)
fontmedium = ("Arial",45)
fontsmall = ("Arial",26)
fonttiny = ("Courier",11)
fonttiny2 = ("Arial",18)
mytemptext = canvas1.create_text(500,40,font=fontbig,text="temp",fill="yellow")
myraintext = canvas1.create_text(800,110,font=fontsmall,text="rain summary",fill="#4343D3")
myupdatedtext = canvas1.create_text(1400,850,font=fonttiny2,text="updated",fill="yellow")
day0summary = canvas1.create_text(1000,50,font=fontsmall,text="summary",fill="#6B6BEE")
day1summary = canvas1.create_text(260,200,font=fontsmall,text="summary1",anchor="w",fill="#7373DD")
day2summary = canvas1.create_text(260,300,font=fontsmall,text="summary2",anchor="w",fill="#7373DD")
day3summary = canvas1.create_text(260,400,font=fontsmall,text="summary3",anchor="w",fill="#7373DD")
day4summary = canvas1.create_text(260,500,font=fontsmall,text="summary4",anchor="w",fill="#7373DD")
day5summary = canvas1.create_text(260,600,font=fontsmall,text="summary4",anchor="w",fill="#7373DD")
day6summary = canvas1.create_text(260,700,font=fontsmall,text="summary4",anchor="w",fill="#7373DD")

daynames = [0]
for i in range(1,7):
   daynames.append(canvas1.create_text(20,100+100*i,font=fontsmall,text=f"day{i}",anchor="w",fill="#DDDB73"))


daylist = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]



def timer1():
    t = localtime()
    daynumber = t.tm_wday
    for i in range(1,7):
       canvas1.itemconfigure(daynames[i],text= daylist[daynumber+i])

    (temp, apparent,wind, humidity, rain,time) = weather.fetch_melbourne_observation()
    canvas1.itemconfigure(mytemptext,text= temp+"°")
    canvas1.itemconfigure(myraintext,text=f"Feels like: {apparent}°C | 🌬️ Wind: {wind} km/h | 💧 Humidity: {humidity}% | 💧 rain: {rain}mm")
    canvas1.itemconfigure(myupdatedtext,text=f"🕒 Updated: {time}")
    forecasts = weather.fetch_bom_forecast()
    (precip, maxtemp, summary) = forecasts[0]
    icon = weather.ascii_icon(summary.lower())
    canvas1.itemconfigure(day0summary,text=icon+" "+summary+" "+precip+". Max "+maxtemp+"°C")
    (precip, maxtemp, summary) = forecasts[1]
    icon = weather.ascii_icon(summary.lower())
    canvas1.itemconfigure(day1summary,text=icon+" "+summary+" "+precip+". Max "+maxtemp+"°C")
    (precip, maxtemp, summary) = forecasts[2]
    icon = weather.ascii_icon(summary.lower())
    canvas1.itemconfigure(day2summary,text=icon+" "+summary+" "+precip+". Max "+maxtemp+"°C")
    (precip, maxtemp, summary) = forecasts[3]
    icon = weather.ascii_icon(summary.lower())
    canvas1.itemconfigure(day3summary,text=icon+" "+summary+" "+precip+". Max "+maxtemp+"°C")
    (precip, maxtemp, summary) = forecasts[4]
    icon = weather.ascii_icon(summary.lower())
    canvas1.itemconfigure(day4summary,text=icon+" "+summary+" "+precip+". Max "+maxtemp+"°C")
    (precip, maxtemp, summary) = forecasts[5]
    icon = weather.ascii_icon(summary.lower())
    canvas1.itemconfigure(day5summary,text=icon+" "+summary+" "+precip+". Max "+maxtemp+"°C")
    (precip, maxtemp, summary) = forecasts[6]
    icon = weather.ascii_icon(summary.lower())
    canvas1.itemconfigure(day6summary,text=icon+" "+summary+" "+precip+". Max "+maxtemp+"°C")
    mainwin.after(60000,timer1)


timer1()


mainwin.mainloop() 