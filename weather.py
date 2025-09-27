import ftplib
import xml.etree.ElementTree as ET
import io

textblue = "\033[1;38;2;80;80;255m"
textblue2 = "\033[1;38;2;120;120;255m"
textlightblue = "\033[1;38;2;160;160;255m"
textbrightyellow = "\033[1;38;2;255;255;0m"

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
            precip = "No Rain"
            for period in area.findall("forecast-period"):
                time = period.attrib.get("start-time-local")
                day = time[5:10]
                summary = period.find("text[@type='precis']")
                for element in period.findall("element"):
                  element_type = element.attrib.get("type")
                  element_value = element.text
                  #print(f"  {element_type}: {element_value}")
                  if element_type == "air_temperature_maximum":
                      temp = element_value
                  if element_type.find("precip") != -1:
                      precip = element_value
                if time  and summary is not None:
                    forecasts.append((precip, temp, summary.text))            
            break
    return forecasts

def ascii_icon(summary):
    summary = summary.lower()
    if "sun" in summary:
        return "☀️"
    elif "cloud" in summary:
        return "☁️"
    elif "rain" in summary or "shower" in summary:
        return "🌧️"
    elif "storm" in summary:
        return "⛈️"
    elif "fog" in summary:
        return "🌫️"
    elif "snow" in summary:
        return "❄️"
    else:
        return "🌈"

def ascii_weather_display(forecasts):
    for precip, temp, summary in forecasts:
        icon = ascii_icon(summary)
        print(icon +" " + textbrightyellow+ temp+"°"+textblue2+summary)
        print(textlightblue+"  "+precip)


forecasts = fetch_bom_forecast()
if forecasts:
        ascii_weather_display(forecasts)
else:
        print("No forecast data found for Melbourne.")
