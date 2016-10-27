from resources.lib.util import cUtil
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.gui.hoster import cHosterGui
from resources.lib.handler.hosterHandler import cHosterHandler
from xbmc import log

SITE_IDENTIFIER = 'gstream_in'
SITE_NAME = 'G-Stream.in'

URL_MAIN = 'http://g-stream.in'
URL_SHOW_MOVIE = 'http://g-stream.in/showthread.php?t='
URL_CATEGORIES = 'http://g-stream.in/forumdisplay.php?f='
URL_HOSTER = 'http://g-stream.in/secure/'
URL_SEARCH = 'http://g-stream.in/search.php'


def load():
    oGui = cGui()
    __createMainMenuEntry(oGui, 'Aktuelle KinoFilme', 542)
    __createMainMenuEntry(oGui, 'Action', 591)
    __createMainMenuEntry(oGui, 'Horror', 593)
    __createMainMenuEntry(oGui, 'Komoedie', 592)
    __createMainMenuEntry(oGui, 'Thriller', 595)
    __createMainMenuEntry(oGui, 'Drama', 594)
    __createMainMenuEntry(oGui, 'Fantasy', 655)
    __createMainMenuEntry(oGui, 'Abenteuer', 596)
    __createMainMenuEntry(oGui, 'Animation', 677)
    __createMainMenuEntry(oGui, 'Dokumentation', 751)

    oGuiElement = cGuiElement()
    oGuiElement.setSiteName(SITE_IDENTIFIER)
    oGuiElement.setFunction('displaySearch')
    oGuiElement.setTitle('Suche')
    oGui.addFolder(oGuiElement)

    oGui.setEndOfDirectory()

def __createMainMenuEntry(oGui, sMenuName, iCategoryId):
    oGuiElement = cGuiElement()
    oGuiElement.setSiteName(SITE_IDENTIFIER)
    oGuiElement.setTitle(sMenuName)
    oGuiElement.setFunction('parseMovieResultSite')
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('normalySiteUrl', URL_CATEGORIES + str(iCategoryId) + '&order=desc&page=')
    oOutputParameterHandler.addParameter('siteUrl', URL_CATEGORIES + str(iCategoryId) + '&order=desc&page=1')
    oOutputParameterHandler.addParameter('iPage', 1)
    oGui.addFolder(oGuiElement, oOutputParameterHandler)

def displaySearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        __search(sSearchText)
        return

    oGui.setEndOfDirectory()

def __search(sSearchText):
    sUrl = 'http://g-stream.in/search.php?do=process&childforums=1&do=process&exactname=1&forumchoice[]=528&query=' + str(sSearchText) + '&quicksearch=1&s=&securitytoken=guest&titleonly=1'
        
    oRequestHandler = cRequestHandler(sUrl)
    sUrl = oRequestHandler.getHeaderLocationUrl()

    __parseMovieResultSite(sUrl, sUrl, 1)

def parseMovieResultSite():
    oInputParameterHandler = cInputParameterHandler()
    if (oInputParameterHandler.exist('siteUrl')):
        siteUrl = oInputParameterHandler.getValue('siteUrl')
        normalySiteUrl = oInputParameterHandler.getValue('normalySiteUrl')
        iPage = oInputParameterHandler.getValue('iPage')
        __parseMovieResultSite(siteUrl, normalySiteUrl, iPage)


def __parseMovieResultSite(siteUrl, normalySiteUrl, iPage):
    oGui = cGui()

    sPattern = '<a class="p1" href="[^"]+" >.*?<img class="large" src="(http://[^"]+)".*?<a href="([^"]+)" id="([^"]+)">([^<]+)<'

    # request
    oRequest = cRequestHandler(siteUrl)
    sHtmlContent = oRequest.request()

    # parse content
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        for aEntry in aResult[1]:
            sMovieTitle = aEntry[3].replace('&amp;','&')
            sUrl = URL_SHOW_MOVIE + str(aEntry[2]).replace('thread_title_', '')
            
            oGuiElement = cGuiElement()
            oGuiElement.setSiteName(SITE_IDENTIFIER)
            oGuiElement.setFunction('parseMovie')
            oGuiElement.setTitle(sMovieTitle)
            oGuiElement.setThumbnail(aEntry[0])
            
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('movieUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            
            oGui.addFolder(oGuiElement, oOutputParameterHandler)


    # check for next site
    sPattern = '<td class="thead">Zeige Themen .*?von ([^<]+)</td>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        for aEntry in aResult[1]:
            iTotalCount = aEntry[0]
            iNextPage = int(iPage) + 1
            iCurrentDisplayStart = __createDisplayStart(iNextPage)
            if (iCurrentDisplayStart < iTotalCount):
                oGuiElement = cGuiElement()
                oGuiElement.setSiteName(SITE_IDENTIFIER)
                oGuiElement.setFunction('parseMovieResultSite')
                oGuiElement.setTitle('next ..')

                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('iPage', iNextPage)
                oOutputParameterHandler.addParameter('normalySiteUrl', normalySiteUrl)
                normalySiteUrl = normalySiteUrl + str(iNextPage)
                oOutputParameterHandler.addParameter('siteUrl', normalySiteUrl)
                oGui.addFolder(oGuiElement, oOutputParameterHandler)


    oGui.setEndOfDirectory()

def __createDisplayStart(iPage):
    return (20 * int(iPage)) - 20

def __createInfo(oGui, sHtmlContent):
    sPattern = '<td class="alt1" id="td_post_.*?<img src="([^"]+)".*?<b>Inhalt:</b>(.*?)<br />'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    if (aResult[0] == True):
        for aEntry in aResult[1]:
            sThumbnail = str(aEntry[0])
            sDescription = cUtil().removeHtmlTags(str(aEntry[1])).replace('\t', '').strip()
            oGuiElement = cGuiElement()
            oGuiElement.setSiteName(SITE_IDENTIFIER)
            oGuiElement.setTitle('info (press Info Button)')
            oGuiElement.setThumbnail(sThumbnail)
            oGuiElement.setFunction('dummyFolder')
            oGuiElement.setDescription(sDescription)
            oGui.addFolder(oGuiElement)

def dummyFolder():
    oGui = cGui()
    oGui.setEndOfDirectory()

def parseMovie():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    if (oInputParameterHandler.exist('movieUrl') and oInputParameterHandler.exist('sMovieTitle')):
        sSiteUrl = oInputParameterHandler.getValue('movieUrl')
        sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')    
        
        oRequest = cRequestHandler(sSiteUrl)
        sHtmlContent = oRequest.request()

        __createInfo(oGui, sHtmlContent)
        
        Urls = []
        
        #Mehrteiler
        sPatternMehrteiler = '</div>CD(\d+):<br />\s*<div style="display: none;" id="[^"]+">\s*<a href="([^"]+)" title="[^"]+" target="_blank">([^<]+)</a>'
        aResult = cParser().parse(sHtmlContent, sPatternMehrteiler)
        if aResult[0] == True:
            for aEntry in aResult[1]:
                sNum = aEntry[0]
                sUrl = aEntry[1]
                sHoster = aEntry[2]
                
                Urls.append(sUrl)
                
                if sHoster == 'all':
                    sHoster = 'xvidstage'
                
                if sUrl.find('sockshare') > -1:             
                    oHoster = cHosterHandler().getHoster2('sockshare')
                elif sUrl.find('putlocker') > -1:
                    oHoster = cHosterHandler().getHoster2('putlocker')
                else:
                    oHoster = cHosterHandler().getHoster2(sHoster)
                
                if oHoster != False:
                    oHoster.setFileName(sMovieTitle)
                    oHoster.setDisplayName("Teil " + sNum + " - " + oHoster.getDisplayName())
                    cHosterGui().showHoster(oGui, oHoster, sUrl, True)
        
        #Einteiler
        sPattern = '<a href="([^"]+)" title="[^"]+" target="_blank">([^<]+)</a>'
        aResult = cParser().parse(sHtmlContent, sPattern)
        if aResult[0] == True:
            for aEntry in aResult[1]:
                sUrl = aEntry[0]
                sHoster = aEntry[1]
                
                if sUrl in Urls:
                    continue
                    
                if sHoster == 'all':
                    sHoster = 'xvidstage'
                    
                if sUrl.find('sockshare') > -1:             
                    oHoster = cHosterHandler().getHoster2('sockshare')
                elif sUrl.find('putlocker') > -1:
                    oHoster = cHosterHandler().getHoster2('putlocker')
                else:
                    oHoster = cHosterHandler().getHoster2(sHoster)
                    
                if oHoster != False:
                    oHoster.setFileName(sMovieTitle)
                    cHosterGui().showHoster(oGui, oHoster, sUrl, True)
            
    oGui.setEndOfDirectory()


def __parseHosterSiteFromSite(aHosters, sHtmlContent, sHosterIdentifier, sHosterId):
    aHoster = []
    sRegex = '<div style="display: none;" id="ame_noshow_post_.*?<a href="' + URL_HOSTER + sHosterId + '([^ ]+)" target="_blank" rel="nofollow" >'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sRegex)    
    if (aResult[0] == True):
        for aEntry in aResult[1]:            
            sUrl = URL_HOSTER + sHosterId + aEntry

            oHoster = cHosterHandler().getHoster2(sHosterIdentifier)
            aHoster.append(oHoster)
            aHoster.append(str(sUrl).replace(' ', '+'))
            aHosters.append(aHoster)
      
    return True
