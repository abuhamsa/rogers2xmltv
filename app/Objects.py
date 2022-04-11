import datetime

from Utils import Teamnamer

class MyGame:
  def __init__(self, game, channel_source):
    self.channel = game[channel_source]
    self.start = game['sta_tim_et']
    self.end = datetime.datetime.strptime(game['sta_tim_et'],"%Y%m%d%H%M%S %z")+ datetime.timedelta(hours=4)
    self.end = self.end.strftime("%Y%m%d%H%M%S %z")
    self.home = Teamnamer.extend_teamnames(game['hom'])
    self.away = Teamnamer.extend_teamnames(game['awa'])
 
  def print_xmltvprogramme (mygame):
    programme = '<programme channel="'+mygame.channel+'" start=\"'+mygame.start+'" stop="'+mygame.end+'">\n'
    programme += '<title lang="en">'+mygame.home+' vs '+mygame.away+'</title>\n'
    programme += '<desc lang="en">Watch the '+mygame.home+' take on '+mygame.away+'</desc>\n'
    programme += '<category lang="en">Sports</category>'
    programme += '<icon height="" src="" width=""/>\n<credits/>\n<video/>\n<date/>\n</programme>\n'
    return programme

class MyChannel:
  def __init__(self, id,icon):
    self.id = str(id)
    self.icon = icon
  
  def print_xmltvchannel (mychannel):
    channel ='<channel id=\"'+mychannel.id+'\">\n<display-name>Rogers: HD SUPER SPORTS CH '+mychannel.id+' CA</display-name>\n<icon src="'+mychannel.icon+'"></icon>\n</channel>\n'
    return channel


