from resources.lib.parser import cParser
from resources.lib.handler.requestHandler import cRequestHandler
import logger

class cHosterHandler:

    def getUrl(self, oHoster):
        sUrl = oHoster.getUrl()
        if (oHoster.checkUrl(sUrl)):
            oRequest = cRequestHandler(sUrl)            
            sContent = oRequest.request()
            pattern = oHoster.getPattern()
            if type(pattern) == type(''):
                aMediaLink = cParser().parse(sContent, oHoster.getPattern())
                if (aMediaLink[0] == True):
                    logger.info('hosterhandler: ' + aMediaLink[1][0])
                    return True, aMediaLink[1][0]
            else:
                for p in pattern:
                    aMediaLink = cParser().parse(sContent, p)
                    if (aMediaLink[0] == True):
                        logger.info('hosterhandler: ' + aMediaLink[1][0])
                        return True, aMediaLink[1][0]
                        
        return False, ''

    def getHoster2(self, sHoster):    
        if (sHoster.find('.') != -1):
            Arr = sHoster.split('.')
            if (Arr[0].startswith('http') or Arr[0].startswith('www')):
                sHoster = Arr[1]
            else:
                sHoster = Arr[0]
        return self.getHoster(sHoster)        
        
    def getHoster(self, sHosterFileName):
        try:
            exec "from " + sHosterFileName + " import cHoster"
            return cHoster()
        except:
            return False
    