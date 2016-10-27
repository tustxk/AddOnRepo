from resources.lib.parser import cParser
from resources.lib.handler.requestHandler import cRequestHandler
from hosters.hoster import iHoster
from resources.lib.gui.gui import cGui

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'EcoStream.tv'
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
        return 'ecostream'

    def isDownloadable(self):
        return True

    def isJDownloaderable(self):
        return True

    def getPattern(self):
        return ""

    def setUrl(self, sUrl):
        self.__sUrl = sUrl.replace('embed', 'stream')

    def checkUrl(self, sUrl):
        return True

    def getUrl(self):
        return self.__sUrl

    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    def __getIpFromUrl(self):
        sPattern = 'http://(.*?)/'
        oParser = cParser()
        aResult = oParser.parse(self.__sUrl, sPattern)
        if (aResult[0] == True):
            return str(aResult[1][0])

        return '213.247.44.150'

    def __getMediaLinkForGuest(self):
        sUrlIp = self.__getIpFromUrl()
        
        oGui = cGui()
        idx = self.__sUrl.find("?")
        if idx != -1:
          self.__sUrl = self.__sUrl[0:idx]
          self.__sUrl = self.__sUrl + "?ss=1"
        
        oRequest = cRequestHandler(self.__sUrl)
        sHtmlContent = oRequest.request()
        
        sPattern = "var t=setTimeout\(\"lc\('([^']+)','([^']+)','([^']+)'\)"
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)
        
        if (aResult[0] == True):
            for aEntry in aResult[1]:
                sS = str(aEntry[0])
                sK = str(aEntry[1])
                sT = str(aEntry[2])

                sNextUrl = 'http://' + str(sUrlIp) + '/object.php?s='+sS+'&k='+sK+'&t='+sT
                
                oRequest = cRequestHandler(sNextUrl)
                sHtmlContent = oRequest.request()

                sPattern = '<param name="flashvars" value="file=(.*?)&'
                oParser = cParser()
                aResult = oParser.parse(sHtmlContent, sPattern)
                
                if (aResult[0] == True):
                    sLinkToFile = str(aResult[1][0])
                    #.replace('/st2.','/st1.').replace('/st3.','/st1.')
                    return True, sLinkToFile
                
        return False, False