import ftplib
import xml.etree.ElementTree as ET
import io
#import requests

textblue = "\033[1;38;2;80;80;255m"
textblue2 = "\033[1;38;2;120;120;255m"
textlightblue = "\033[1;38;2;160;160;255m"
textbrightyellow = "\033[1;38;2;255;255;0m"

import urllib.request
from html.parser import HTMLParser

class BOMParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_row = False
        self.in_cell = False
        self.row_data = []
        self.melbourne_rows = []

    def handle_starttag(self, tag, attrs):
        if tag == 'tr':
            self.in_row = True
            self.row_data = []
        elif tag == 'td' and self.in_row:
            self.in_cell = True

    def handle_endtag(self, tag):
        if tag == 'tr':
            self.in_row = False
            if self.row_data:
            #    print("🔍 Row:", self.row_data)
                 self.melbourne_rows.append(self.row_data)
        elif tag == 'td':
            self.in_cell = False

    def handle_data(self, data):
        if self.in_cell:
            self.row_data.append(data.strip())

def fetch_melbourne_observation():
    url = "http://www.bom.gov.au/products/IDV60801/IDV60801.95867.shtml"
    headers = {'User-Agent': 'Mozilla/5.0'}
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as response:
        html = response.read().decode()

    parser = BOMParser()
    parser.feed(html)

    #print(parser.melbourne_rows)

    if parser.melbourne_rows:
        latest = parser.melbourne_rows[1]  # Get the newest row
        temp = latest[1]
        apparent = latest[2]
        wind = latest[7]
        humidity = latest[4]
        time = latest[0]
        rain = latest[13]
        print(f"🌡️ Temp: {temp}°C | Feels Like: {apparent}°C")
        print(f"🌬️ Wind: {wind} km/h | 💧 Humidity: {humidity}% | rain: {rain}mm")
        print(f"🕒 Observed at: {time}")
    else:
        print("⚠️ No Melbourne data found.")
    return (temp,apparent, wind, humidity, rain,time)




def get_temperature(period):
    for temp_type in ['air_temperature', 'minimum_temperature', 'maximum_temperature']:
        temp = period.find(f"element[@type='{temp_type}']")
        if temp is not None and temp.text is not None:
            return temp.text
    return "N/A"

def fetch_bom_forecast():
    # BOM FTP server and file path
    ftp_host = "ftp.bom.gov.au"
    ftp_path = "/anon/gen/fwo/IDV10753.xml"  # Victoria forecast feed

    # Connect to FTP and retrieve file
    ftp = ftplib.FTP(ftp_host)
    ftp.login()
    buffer = io.BytesIO()
    ftp.retrbinary(f"RETR {ftp_path}", buffer.write)
    ftp.quit()

    # Parse XML from buffer
    buffer.seek(0)
    tree = ET.parse(buffer)
    root = tree.getroot()

    # Extract 3-hourly forecast for Melbourne
    forecasts = []
    for area in root.iter("area"):
        if "Melbourne" in area.attrib.get("description", ""):   
            for period in area.findall("forecast-period"):
                time = period.attrib.get("start-time-local")
                day = time[5:10]
                summary = period.find("text[@type='precis']")
                precip = "0mm"
                tempmax = "XX"
                tempmin = "XX"
                for element in period.findall("element"): 
                  element_type = element.attrib.get("type")
                  element_value = element.text
                  #print(f"  {element_type}: {element_value}") 
                  if element_type == "air_temperature_maximum":
                      tempmax = element_value
                  if element_type == "air_temperature_minimum":
                      tempmin = element_value
                  if element_type.find("precip") != -1:
                      precip = element_value
                if (time is not None) and (summary is not None):
                    forecasts.append((precip, tempmax, tempmin, summary.text))            
            break
    return forecasts

def ascii_icon(summary):
    summary = summary.lower()
    icon = "🌈"
    if "sun" in summary:
        icon = "☀️"
    if "cloudy" in  summary:
        icon = "☁️"
    if "partly cloudy" in  summary:
        icon = "☀️☁️"
    if "rain" in summary or "shower" in summary:
        icon = "🌧️"
    if "storm" in summary:
        icon = "⛈️"
    if "fog" in summary:
        icon = "🌫️"
    if "snow" in summary:
        icon = "❄️"
    return icon

def ascii_weather_display(forecasts):
    for precip, tempmax, tempmin, summary in forecasts:
        icon = ascii_icon(summary)
        print(icon +" " + textbrightyellow+ tempmax+"° ("+tempmin+"°) "+textblue2+summary)
        print(textlightblue+"  "+precip)

forecasts = fetch_bom_forecast()
if forecasts:
        ascii_weather_display(forecasts)
else:
        print("No forecast data found for Melbourne.")


