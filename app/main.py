import datetime
from datetime import date
from datetime import timedelta
import requests
import pytz
import os

from Objects import MyGame
from Utils import Loader
from Objects import MyChannel

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

def main():
    
    bol_docker = "yes"

    # Setting ENV
    if bol_docker == "yes":
        use_static_channels=os.environ['USE_STATIC_CHANNELS']
        date_range=os.environ['DATE_RANGE']
        channel_source=os.environ['CHANNEL_SOURCE']
        icon=os.environ['ICON']
        tz=os.environ['TZ']
        file_path="/data/rogers2xmltv.xml"
    else:
        use_static_channels="yes"
        date_range="1"
        channel_source="rog_ott_sdh_ch"
        icon="https://picon-13398.kxcdn.com/rogersca.jpg"
        tz="Europe/Zurich"
        file_path="rogers2xmltv.xml"
    
    # URL of the API
    url = "https://rogerstv.com/api/ssp?f=schedule"

    # Get the Data
    loader = Loader (url,file_path)  

    # Extract NHL games out of the response
    games = loader.get_nhl_games(tz,date_range,channel_source)
    # Extract channels out of NHL games
    channels=loader.get_channels(games,channel_source)

    # Generate static XMLTV-channels based on https://www.rogers.com/customer/support/article/nhl-centre-ice
    if use_static_channels == 'yes':
        mychannels=[]
        for channel in range(450,468):
            mychannel = MyChannel(channel,icon)
            mychannels.append(mychannel)
    # Generate XMLTV-channels from NHL games
    else :
        mychannels=[]
        for channel in channels:
            mychannel = MyChannel(channel,icon)
            mychannels.append(mychannel)

    # Create list with mygames-object
    mygames=[]
    for game in games:
        mygame = MyGame(game,channel_source)
        mygames.append(mygame)

    # Generate XMLTV-file (putting all together)
    loader.write_xmltv_file(mychannels,mygames)
    
if __name__ == "__main__":
    main()