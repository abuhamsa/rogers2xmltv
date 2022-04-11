import datetime
from datetime import date
from datetime import timedelta
import pytz
import requests


class Loader:
    def __init__(self, url,file_path):
        # HTTP Stuff
        payload={}
        headers = {}

        response = requests.request("GET", url, headers=headers, data=payload)
        self.data = response.json()
        self.file_path = file_path

    def convert_datetime_timezone(self,dt, tz1, tz2):
        tz1 = pytz.timezone(tz1)
        tz2 = pytz.timezone(tz2)
        dt = datetime.datetime.strptime(dt,"%Y-%m-%dT%H:%M:%S")
        dt = tz1.localize(dt)
        dt = dt.astimezone(tz2)
        dt = dt.strftime("%Y%m%d%H%M%S %z")

        return dt  


    def get_nhl_games(self,tz,date_range,channel_source):
        games = []
        for game in self.data['schedule']:
            today = date.today()
            today_str = today.strftime("%Y-%m-%dT%H:%M:%S")
            limit = today + datetime.timedelta(days=int(date_range))
            limit_str = limit.strftime("%Y-%m-%dT%H:%M:%S")
            if game['spo'] == 'NHL' and game['dat'] >= today_str and game['dat'] <= limit_str and game[channel_source] != 'N/A':
                game['sta_tim_et']=self.convert_datetime_timezone(game['sta_tim_et'], "America/New_York", tz)
                games.append(game)
        return games


    def get_channels(self,games,channel_source):
        channels = []
        for game in games:
            id = game[channel_source]
            if id !='N/A' and id not in channels:
                channels.append(id)
        return channels 

    def write_xmltv_file (self,mychannels, mygames):
        f = open(self.file_path, "w") 
        f.write('<tv generator-info-name="rogers2xmltv" source-info-name="rogers2xmltv by abuhamsa">')
        for mychannel in mychannels:
            f.write(mychannel.print_xmltvchannel())
        for mygame in mygames:
            f.write(mygame.print_xmltvprogramme())
        f.write('</tv>')
        f.close       
  
