from hosters.hoster import iHoster
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'RuTube.ru'
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
        return 'rutube'

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
        #self.__sUrl = 'http://video.rutube.ru/14bd98f3733ef080507ff5f517f28830'
        sId = self.__sUrl.replace('http://video.rutube.ru/', '')
        
        sNewUrl = 'http://bl.rutube.ru/' + str(sId) + '.xml?max-age=0&schema=rtmp'
        
        oRequest = cRequestHandler(sNewUrl)
        sHtmlContent = oRequest.request()

        sPattern = '<finalAddress>(.*?)</finalAddress>'
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)

        if (aResult[0] == True):
            sRtmpFile = aResult[1][0]
            sRtmpFile = sRtmpFile.replace('<![CDATA[', '')
            sRtmpFile = sRtmpFile.replace(']]>', '')
            sRtmpFile = sRtmpFile.replace(' ', '')
            
            aSplitt = sRtmpFile.split('mp4:')
            sPlaypath = 'mp4:' + aSplitt[1]
            
            aSplitt = sRtmpFile.split('.ru/')
            sRtmp = aSplitt[0] + '.ru:1935/'
            
            aSplitt = aSplitt[1].split('mp4')
            sApp = aSplitt[0]

            sSwfUrl = 'http://rutube.ru/player.swf'

            sStreamUrl = sRtmp + ' app=' + sApp + ' swfurl=' + sSwfUrl + ' playpath=' + sPlaypath
            #rtmp://video-1-1.rutube.ru:1935/ app=rutube_vod_2/_definst_/ swfurl=http://rutube.ru/player.swf playpath=mp4:vol32/movies/14/bd/14bd98f3733ef080507ff5f517f28830.mp4?e=1295385656&s=adb28dba086b7394013c37550cb48dd8&blid=957c0d2befa18c8d286b2076cecf01bd

            return True, sStreamUrl

        return False, ''