from hosters.hoster import iHoster
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser

class cHoster(iHoster):

    URL_XML = 'http://intl.esperanto.mtvi.com/www/xml/media/mediaGen.jhtml'

    def __init__(self):
        self.__sDisplayName = 'MTV.de'
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
        return 'mtv'

    def isDownloadable(self):
        return True

    def isJDownloaderable(self):
        return True

    def getPattern(self):
        return '';

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
        sHtmlContent = oRequest.request()
        sPattern = 'vid=([^;]+);'
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)

        if (aResult[0] == True):
            videoId = aResult[1][0]
            sUrl = 'http://intl.esperanto.mtvi.com/www/xml/media/mediaGen.jhtml?uri=mgid%3Auma%3Avideo%3Amtv.de%3A' + videoId
            oRequest = cRequestHandler(sUrl)
            sHtmlContent = oRequest.request()

            sPattern = '<src>([^<]+)</src>'
            oParser = cParser()
            aResult = oParser.parse(sHtmlContent, sPattern)

            if (aResult[0] == True):
                i = len(aResult[1]) - 2
                sStreamUrl = aResult[1][i] + " swfVfy=1 swfUrl=" + 'http://media.mtvnservices.com/player/prime/mediaplayerprime.1.8.1.swf' + " pageUrl=" + self.__sUrl 
                return True, sStreamUrl

        return False, False
