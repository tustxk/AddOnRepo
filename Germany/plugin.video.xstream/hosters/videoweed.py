from resources.lib.handler.hosterHandler import cHosterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from hosters.hoster import iHoster

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'VideoWeed.com'
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
        return 'videoweed'

    def isDownloadable(self):
        return True

    def isJDownloaderable(self):
        return True

    def getPattern(self):
        return 'flashvars.file=\"([^\"]+)\"';

    def getHosterLinkPattern(self):
        return '[\'"](http://(?:www.)?videoweed.(?:com|es)?/[^\'"]+)[\'"]'
    
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
        sPattern = 'flashvars.file="([^"]+)".*?flashvars.filekey="([^"]+)";'
        aResult = oParser.parse(html, sPattern)
        if aResult[0] == True:
            file = aResult[1][0][0]
            key = aResult[1][0][1]
            newUrl = 'http://www.videoweed.es/api/player.api.php?pass=undefined&codes=1&file=' + file + '&user=undefined&key=' + key
            oRequest = cRequestHandler(newUrl)
            html = oRequest.request()
            sPattern = 'url=([^&]+)&'
            aResult = oParser.parse(html, sPattern)
            if aResult[0] == True:
                return True, str(aResult[1][0])
        return False, False 