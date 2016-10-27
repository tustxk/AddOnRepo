from resources.lib.handler.hosterHandler import cHosterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from hosters.hoster import iHoster

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'VidStream.us'
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
        return 'vidstream'

    def isDownloadable(self):
        return True

    def isJDownloaderable(self):
        return True

    def getPattern(self):
        return 'flashvars.file=\"([^\"]+)\"';

    def getHosterLinkPattern(self):
        return '<a href="(http://vidstream.us/video/[^"]+)"'
    
    def setUrl(self, sUrl):
        self.__sUrl = sUrl

    def checkUrl(self, sUrl):
        return True

    def getUrl(self):
        return self.__sUrl

    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    def __getMediaLinkForGuest(self):
        from xbmc import log
        oRequest = cRequestHandler(self.__sUrl)
        html = oRequest.request()
        
        oParser = cParser()
        sPattern = 'settingsFile\:\s*"([^"]+)"'
        aResult = oParser.parse(html, sPattern)
        if aResult[0] == True:
            newUrl = aResult[1][0]
            oRequest = cRequestHandler(newUrl)
            html = oRequest.request()
            
            sPattern = '<videoPath value="([^"]+)"/>'
            aResult = oParser.parse(html, sPattern)
            if aResult[0] == True:
                return True, str(aResult[1][0])
        return False, False 