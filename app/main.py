import datetime
import requests
import pytz
import os
import logging
import sys

from datetime import date
from datetime import timedelta
from Objects import MyGame
from Utils import Loader
from Objects import MyChannel 

def main():

    bol_docker = os.environ['DOCKER_MODE']
    file_path=""

    # Setting ENV
    if bol_docker == "yes":
        use_static_channels=os.environ['USE_STATIC_CHANNELS']
        date_range=os.environ['DATE_RANGE']
        channel_source=os.environ['CHANNEL_SOURCE']
        icon=os.environ['ICON']
        tz=os.environ['TZ']
        file_path="/data/"
        file_path_xml=file_path+"rogers2xmltv.xml"
    else:
        use_static_channels="yes"
        date_range="1"
        channel_source="rog_ott_sdh_ch"
        icon="https://picon-13398.kxcdn.com/rogersca.jpg"
        tz="Europe/Zurich"
        file_path=""
        file_path_xml="rogers2xmltv.xml"
       

    # Creating and Configuring Logger
    logger = logging.getLogger()
    fileHandler = logging.FileHandler(file_path+"rogers2xmltv.log")
    streamHandler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    streamHandler.setFormatter(formatter)
    fileHandler.setFormatter(formatter)
    logger.addHandler(streamHandler)
    logger.addHandler(fileHandler)
    logger.setLevel(logging.INFO)    
    
    logger.info("Docker mode: "+str(bol_docker)) 

    envs =  "Environment variables: \n"
    envs += "use_static_channels="+use_static_channels+"\n"
    envs += "date_range="+date_range+"\n"
    envs += "channel_source="+channel_source+"\n"
    envs += "icon="+icon+"\n"
    envs += "file_path="+file_path+"\n"
    envs += "tz="+tz
    
    logger.info(envs)

    # URL of the API
    url = "https://rogerstv.com/api/ssp?f=schedule"
    logger.info(url)

    # Get the Data
    logger.info("Start downloading JSON")
    loader = Loader (url,file_path_xml)  
    logger.info("Finished downloading JSON")

    # Extract NHL games out of the response
    logger.info("Extract NHL games for "+channel_source+". Timerange: "+date_range)
    games = loader.get_nhl_games(tz,date_range,channel_source)
    # Extract channels out of NHL games
    logger.info("Extract Channels IDs for "+channel_source)
    channels=loader.get_channels(games,channel_source)

    # Generate static XMLTV-channels based on https://www.rogers.com/customer/support/article/nhl-centre-ice
    if use_static_channels == 'yes':
        logger.info("Create static channel-list")
        mychannels=[]
        for channel in range(450,468):
            mychannel = MyChannel(channel,icon)
            mychannels.append(mychannel)
    # Generate XMLTV-channels from NHL games
    else :
        logger.info("Create dynamic channel-list")
        mychannels=[]
        for channel in channels:
            mychannel = MyChannel(channel,icon)
            mychannels.append(mychannel)

    # Create list with mygames-object
    logger.info("Create game-list")
    mygames=[]
    for game in games:
        mygame = MyGame(game,channel_source)
        mygames.append(mygame)

    # Generate XMLTV-file (putting all together)
    logger.info("Start writing XMLTV-file")
    loader.write_xmltv_file(mychannels,mygames)
    logger.info("Finished writing XMLTV-file")

if __name__ == "__main__":
    main()