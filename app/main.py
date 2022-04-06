import datetime
from datetime import date
from datetime import timedelta
import requests
import pytz
import os

def convert_datetime_timezone(dt, tz1, tz2):
    tz1 = pytz.timezone(tz1)
    tz2 = pytz.timezone(tz2)
    dt = datetime.datetime.strptime(dt,"%Y-%m-%dT%H:%M:%S")
    dt = tz1.localize(dt)
    dt = dt.astimezone(tz2)
    dt = dt.strftime("%Y%m%d%H%M%S %z")

    return dt

def write_xmltv_file (xmlchannels, xmlprogrammes):
   f = open("/data/rogers2xmltv.xml", "w") 
   f.write('<tv generator-info-name="rogers_ssp_xmltv" source-info-name="Rogers SSP 2 XMLTV 0.1">')
   f.write(xmlchannels)
   f.write(xmlprogrammes)
   f.write('</tv>')
   f.close


def xmltv_programme (games,channel_source):
    programmes = ''
    for game in games:
        endtime = datetime.datetime.strptime(game['sta_tim_et'],"%Y%m%d%H%M%S %z")+ timedelta(hours=4)
        endtime = endtime.strftime("%Y%m%d%H%M%S %z")

        programmes += '<programme channel="'+game[channel_source]+'" start=\"'+game['sta_tim_et']+'" stop="'+endtime+'">\n'
        programmes += '<title lang="en">'+game['hom']+' vs '+game['awa']+'</title>\n'
        programmes += '<desc lang="en">Watch '+game['hom']+' take on '+game['awa']+'</desc>\n'
        programmes += '<category lang="en">Sports</category>'
        programmes += '<icon height="" src="" width=""/>\n<credits/>\n<video/>\n<date/>\n</programme>\n'
    return programmes    

def xmltv_channels (channels,icon):
    xmlchannels=''
    for channel in channels:
        xmlchannels +='<channel id=\"'+channel+'\">\n<display-name>Rogers: HD SUPER SPORTS CH '+channel+' CA</display-name>\n<icon src="'+icon+'"></icon>\n</channel>\n'
    return xmlchannels

def static_xmltv_channels (icon):
    xmlchannels=''
    for channel in range(450,468):
        xmlchannels +='<channel id=\"'+str(channel)+'\">\n<display-name>Rogers: HD SUPER SPORTS CH '+str(channel)+' CA</display-name>\n<icon src="'+icon+'"></icon>\n</channel>\n'
    return xmlchannels    

def get_channels(games,channel_source):
    channels = []
    for game in games:
        id = game[channel_source]
        if id !='N/A' and id not in channels:
            channels.append(id)
    return channels           

def get_nhl_games(data,tz,date_range):
    games = []
    for game in data['schedule']:
        today = date.today()
        today_str = today.strftime("%Y-%m-%dT%H:%M:%S")
        limit = today + datetime.timedelta(days=int(date_range))
        limit_str = limit.strftime("%Y-%m-%dT%H:%M:%S")
        if game['spo'] == 'NHL' and game['dat'] >= today_str and game['dat'] <= limit_str :
            game['sta_tim_et']=convert_datetime_timezone(game['sta_tim_et'], "America/New_York", tz)
            games.append(game)
    return games
def main():
    
    # Setting ENV
    use_static_channels=os.environ['USE_STATIC_CHANNELS']
    date_range=os.environ['DATE_RANGE']
    channel_source=os.environ['CHANNEL_SOURCE']
    icon=os.environ['ICON']
    tz=os.environ['TZ']


    url = "https://rogerstv.com/api/ssp?f=schedule"

    payload={}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)
    data = response.json()
    games = get_nhl_games(data,tz,date_range)
    channels=get_channels(games,channel_source)
    if use_static_channels == 'yes':
        xmlchannels=static_xmltv_channels(icon)
    else :    
        xmlchannels=xmltv_channels(channels,icon)
    xmlprogrammes=xmltv_programme(games,channel_source)
    write_xmltv_file(xmlchannels,xmlprogrammes)
    
if __name__ == "__main__":
    main()