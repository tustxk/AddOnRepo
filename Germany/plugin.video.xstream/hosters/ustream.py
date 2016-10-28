from resources.lib.parser import cParser
from resources.lib.handler.requestHandler import cRequestHandler
from hosters.hoster import iHoster
import logger

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'Ustream.tv'
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
        return 'ustream'

    def isDownloadable(self):
        return True

    def isJDownloaderable(self):
        return True

    def getPattern(self):
        return ''

    def setUrl(self, sUrl):
        self.__sUrl = sUrl

    def checkUrl(self, sUrl):
        return True

    def getUrl(self):
        return self.__sUrl

    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    def __getMediaLinkForGuest(self):
        oRequestHandler = cRequestHandler(self.__sUrl)
        sHtmlContent = oRequestHandler.request()

        sAmfUrl = self.__getAmfUrl(sHtmlContent)
        logger.info('amf: ' + str(sAmfUrl))
        if (sAmfUrl == False):
            return False, ''
        
        oRequestHandler = cRequestHandler(sAmfUrl)
        oRequestHandler.setRequestType(cRequestHandler.REQUEST_TYPE_POST)
        sAmfContent = oRequestHandler.request()

        sRtmp = self.__getRtmp(sAmfContent)
        logger.info('rtmp: ' + str(sRtmp))
        if (sRtmp == False):
            return False, ''

        sPageUrl = self.__getPageUrl()
        logger.info('pageurl: ' + str(sPageUrl))
        if (sPageUrl == False):
            return False, ''
        
        sSwf = self.__getSwf(sHtmlContent)
        logger.info('swf: ' + str(sSwf))
        if (sSwf == False):
            return False, ''
        
        sMediaLink = sRtmp + ' swfUrl=' + sSwf + ' swfVfy=1 live=true pageUrl=' + sPageUrl
        logger.info('medialink: ' + str(sMediaLink))
        
        return True, sMediaLink

    def __getAmfUrl(self, sHtmlContent):
        sPattern = "channelid: '(.*?)'"

        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
            sChannelId = aResult[1][0]        
            return 'http://cgw.ustream.tv/Viewer/getStream/1/' + str(sChannelId) +'.amf'

        return False


    def __getRtmp(self, sHtmlContent):        
        oParser = cParser()
        rtmp = False

        sPattern = '(rtmp://ustream.+?)\x00'
        aResult = oParser.parse(sHtmlContent, sPattern)      
        if (aResult[0] == True):
            sTemp = aResult[1][0].replace('/ustreamVideo', ':1935/ustreamVideo')
            rtmp = sTemp + "/"
        else:
            return False
            
        sPattern = 'streamName\W\W\W(.+?)[/]*\x00'
        aResult = oParser.parse(sHtmlContent, sPattern)      
        if (aResult[0] == True):
            sTemp = aResult[1][0]
            sTemp = sTemp
            rtmp += sTemp
        else:
            return False

        return rtmp

    def __getPageUrl(self):
        return self.__sUrl

    def __getSwf(self, sHtmlContent):
        sPattern = 'movie: "([^"]+)"'
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)
        
        if (aResult[0] == True):
            sTemp = str(aResult[1][0])
            return sTemp

        return False