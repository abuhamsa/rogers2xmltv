import os
import logging
import sys
from fastapi import FastAPI, Response
from app.myObjects import MyVar
from app.myObjects import MyGame
from app.myObjects import MyChannel 
from app.Utils import Loader

# Create FastAPI Object
app = FastAPI()

# Setting the Environment Variables
DOCKER_MODE = os.getenv('DOCKER_MODE', 'False').lower() == 'true'
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO').upper()
SSL_CHECK = False #Only Setting cause of proxy problems


# If in DOCKER_MODE take ENVs from Dockerfile and/or env-parameters
if DOCKER_MODE:
    USE_STATIC_CHANNELS=os.getenv('USE_STATIC_CHANNELS', 'False').lower() == 'true'
    DATE_RANGE=os.environ['DATE_RANGE']
    CHANNEL_SOURCE=os.environ['CHANNEL_SOURCE']
    ICON=os.environ['ICON']
    TZ=os.environ['TZ']
    API_MODE=os.getenv('API_MODE', 'False').lower() == 'true'
    URL = os.environ['URL']
    SCRAPERAPIKEY = os.environ['SCRAPERAPIKEY']
    file_path="/data/"
    file_path_xml=file_path+"rogers2xmltv.xml"

# else use some defaults, most likely for local debugging    
else:
    USE_STATIC_CHANNELS=True
    DATE_RANGE="1"
    CHANNEL_SOURCE="rog_ott_sdh_ch"
    ICON="https://picon-13398.kxcdn.com/rogersca.jpg"
    TZ="Europe/Zurich"
    API_MODE=True
    URL = "https://rogerstv.com/api/ssp?f=schedule"
    SCRAPERAPIKEY = ""
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
logger.setLevel(level=LOG_LEVEL)


#### Here is the API-Stuff for FastAPI

# GET Method for getting an xml-reponse
# you can set some parameters. if not it takes defaults
@app.get("/xmltv/")
async def xmltv_get(use_static_channels: bool=True,date_range: str="7",channel_source: str="rog_ott_sdh_ch",icon: str="https://picon-13398.kxcdn.com/rogersca.jpg",tz: str="Europe/Zurich"):
    myvar = MyVar(use_static_channels=use_static_channels,date_range=date_range,channel_source=channel_source,icon=icon,tz=tz)
    return Response(content=main(myvar), media_type="application/xml") 

# POST Method for getting an xml-reponse
# you can set some parameters. if not it takes defaults
@app.post("/xmltv/")
async def xmltv_post(myvar: MyVar):
    return Response(content=main(myvar), media_type="application/xml")

# GET for root Path to retrun 444
@app.get("/",include_in_schema=False)
async def root_get():
    return Response(status_code=444)   

def main(api_variables):

    logger.info("API_MODE: "+str(API_MODE))
    if API_MODE:
        use_static_channels=api_variables.use_static_channels
        date_range=api_variables.date_range
        channel_source=api_variables.channel_source
        icon=api_variables.icon
        tz=api_variables.tz  
    else:
        use_static_channels=USE_STATIC_CHANNELS
        date_range=DATE_RANGE
        channel_source=CHANNEL_SOURCE
        icon=ICON
        tz=TZ   
       
    logger.info("DOCKER_MODE: "+str(DOCKER_MODE)) 

    logger.debug("Print Variables:")
    logger.debug("use_static_channels="+str(use_static_channels))
    logger.debug("date_range="+date_range)
    logger.debug("channel_source="+channel_source)
    logger.debug("icon="+icon)
    logger.debug("file_path="+file_path)
    logger.debug("tz="+tz)
    

    # URL of the API
    logger.info(URL)

    # Get the Data
    logger.info("Start downloading JSON")
    loader = Loader (URL,file_path_xml,SSL_CHECK,SCRAPERAPIKEY)  
    logger.info("Finished downloading JSON")

    # Extract NHL games out of the response
    logger.info("Extract NHL games for "+channel_source+". Timerange: "+date_range)
    games = loader.get_nhl_games(tz,date_range,channel_source)
    # Extract channels out of NHL games
    logger.info("Extract Channels IDs for "+channel_source)
    channels=loader.get_channels(games,channel_source)

    # Generate static XMLTV-channels based on https://www.rogers.com/customer/support/article/nhl-centre-ice
    if use_static_channels:
        logger.info("Create static channel-list")
        mychannels=[]
        for channel in range(450,468):
            mychannel = MyChannel(channel,icon)
            mychannels.append(mychannel)
    # Generate XMLTV-channels from NHL games
    else:
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
    
    #loader.write_xmltv_file(mychannels,mygames)
    
    if API_MODE:
        logger.info("Create response")    
        return loader.api_xmltv_file(mychannels,mygames)
    else:
        logger.info("Start writing XMLTV-file")
        loader.write_xmltv_file(mychannels,mygames)
        logger.info("Finished writing XMLTV-file")    

if __name__ == "__main__":
    main(None)