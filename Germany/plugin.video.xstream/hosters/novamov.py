import re
from resources.lib.handler.hosterHandler import cHosterHandler
from resources.lib.handler.requestHandler import cRequestHandler 
from hosters.hoster import iHoster

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'NovaMov.com'
	self.__sFileName = self.__sDisplayName

    def getDisplayName(self):
        return  self.__sDisplayName

    def setDisplayName(self, sDisplayName):
        self.__sDisplayName = sDisplayName

    def setFileName(self, sFileName):
	self.__sFileName = sFileName

    def getFileName(self):
	return self.__sFileName

    def getPluginIdentifier(self):
        return 'novamov'

    def isDownloadable(self):
        return True

    def isJDownloaderable(self):
        return True

    def getPattern(self):
        return 'flashvars.file=\"([^\"]+)\"';
     
    def getHosterLinkPattern(self):
        return "['\"](http://(?:www.)?novamov.com/(?:video|embed)?[^\"']+)['\"]"

    def setUrl(self, sUrl):
        self.__sUrl = sUrl

    def checkUrl(self, sUrl):
        return True

    def getUrl(self):
        return self.__sUrl

    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    def __getMediaLinkForGuest(self): 
        oRequest = cRequestHandler(self.__sUrl)             
        html = oRequest.request() 

        r = re.search('flashvars.file="(.+?)".+?flashvars.filekey="(.+?)"', html, re.DOTALL) 
        if r: 
            filename, filekey = r.groups() 
        api = 'http://www.novamov.com/api/player.api.php?key=%s&file=%s' % (filekey, filename) 
         
        html = cRequestHandler(api).request() 
     
        r = re.search('url=(.+?)&title', html) 
        if r: 
            stream_url = r.group(1) 
            return True,stream_url 
        return False,''