from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.util import cUtil
from resources.lib.gui.hoster import cHosterGui
from resources.lib.handler.hosterHandler import cHosterHandler
from xbmc import log

SITE_IDENTIFIER = 'iload_to'
SITE_NAME = 'ILoad.to'

URL_MAIN = 'http://iload.to/de/'
URL_MOVIE_PAGE = URL_MAIN + 'category/1-Filme/'
URL_CHARACTERS = URL_MAIN + 'category/1-Filme/letter'
URL_SERIE_CHARACTERS = URL_MAIN + 'category/6-Serien/letter'
URL_SEARCH = URL_MAIN + 'ajax/module/category/1-Filme/search/'
URL_SEARCH_SERIES = URL_MAIN + 'ajax/module/category/6-Serien/search/'

COOKIE_SECURITY_NAME = 'suilid'

def load():
    sCookieValue = __getSecurityCookieValue()

    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_CHARACTERS)
    oOutputParameterHandler.addParameter('security', sCookieValue)
    oOutputParameterHandler.addParameter('nextFunction', 'showMovies')
    __createMenuEntry(oGui, 'showCharacters', 'Filme', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_SERIE_CHARACTERS)
    oOutputParameterHandler.addParameter('security', sCookieValue)
    oOutputParameterHandler.addParameter('nextFunction', 'showSeries')
    __createMenuEntry(oGui, 'showCharacters', 'Serien', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_MAIN)
    oOutputParameterHandler.addParameter('security', sCookieValue)
    __createMenuEntry(oGui, 'showCinemaMovies', 'aktuelle KinoFilme', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_MOVIE_PAGE)
    oOutputParameterHandler.addParameter('security', sCookieValue)
    __createMenuEntry(oGui, 'displayGenre', 'Genre', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH)
    oOutputParameterHandler.addParameter('security', sCookieValue)
    oOutputParameterHandler.addParameter('nextFunction', 'movies')
    __createMenuEntry(oGui, 'displaySearch', 'Film Suche', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH_SERIES)
    oOutputParameterHandler.addParameter('security', sCookieValue)
    oOutputParameterHandler.addParameter('nextFunction', 'series')
    __createMenuEntry(oGui, 'displaySearch', 'Serien Suche', oOutputParameterHandler)
    
    oGui.setEndOfDirectory()

def __getSecurityCookieValue():
    oRequestHandler = cRequestHandler(URL_MAIN)
    oRequestHandler.setRequestType(cRequestHandler.REQUEST_TYPE_POST)
    oRequestHandler.request();
    aHeader = oRequestHandler.getResponseHeader()    
    sReponseCookie = aHeader.getheader("Set-Cookie")
    
    if (sReponseCookie == None):
	return ''
    
    sPattern = COOKIE_SECURITY_NAME + '=([^;]+);'
    oParser = cParser()
    aResult = oParser.parse(sReponseCookie, sPattern)
    if (aResult[0] == True):        
        return COOKIE_SECURITY_NAME + '=' + str(aResult[1][0])

    return ''

def __createMenuEntry(oGui, sFunction, sLabel, oOutputParameterHandler = ''):
    oGuiElement = cGuiElement()
    oGuiElement.setSiteName(SITE_IDENTIFIER)
    oGuiElement.setFunction(sFunction)
    oGuiElement.setTitle(sLabel)
    oGui.addFolder(oGuiElement, oOutputParameterHandler)

def showCharacters():

    oInputParameterHandler = cInputParameterHandler()
    sSecurity = oInputParameterHandler.getValue('security')
    sSiteUrl = oInputParameterHandler.getValue('siteUrl')
    if not sSiteUrl.endswith('/letter'):
        sSiteUrl += '/letter'
     
    sNextFunction = oInputParameterHandler.getValue('nextFunction')

    oGui = cGui()
    __createCharacters(oGui, '#', sSecurity, sSiteUrl, sNextFunction)
    __createCharacters(oGui, 'A', sSecurity, sSiteUrl, sNextFunction)
    __createCharacters(oGui, 'B', sSecurity, sSiteUrl, sNextFunction)
    __createCharacters(oGui, 'C', sSecurity, sSiteUrl, sNextFunction)
    __createCharacters(oGui, 'D', sSecurity, sSiteUrl, sNextFunction)
    __createCharacters(oGui, 'E', sSecurity, sSiteUrl, sNextFunction)
    __createCharacters(oGui, 'F', sSecurity, sSiteUrl, sNextFunction)
    __createCharacters(oGui, 'G', sSecurity, sSiteUrl, sNextFunction)
    __createCharacters(oGui, 'H', sSecurity, sSiteUrl, sNextFunction)
    __createCharacters(oGui, 'I', sSecurity, sSiteUrl, sNextFunction)
    __createCharacters(oGui, 'J', sSecurity, sSiteUrl, sNextFunction)
    __createCharacters(oGui, 'K', sSecurity, sSiteUrl, sNextFunction)
    __createCharacters(oGui, 'L', sSecurity, sSiteUrl, sNextFunction)
    __createCharacters(oGui, 'M', sSecurity, sSiteUrl, sNextFunction)    
    __createCharacters(oGui, 'N', sSecurity, sSiteUrl, sNextFunction)
    __createCharacters(oGui, 'O', sSecurity, sSiteUrl, sNextFunction)
    __createCharacters(oGui, 'P', sSecurity, sSiteUrl, sNextFunction)    
    __createCharacters(oGui, 'Q', sSecurity, sSiteUrl, sNextFunction)
    __createCharacters(oGui, 'R', sSecurity, sSiteUrl, sNextFunction)
    __createCharacters(oGui, 'S', sSecurity, sSiteUrl, sNextFunction)
    __createCharacters(oGui, 'T', sSecurity, sSiteUrl, sNextFunction)
    __createCharacters(oGui, 'U', sSecurity, sSiteUrl, sNextFunction)
    __createCharacters(oGui, 'V', sSecurity, sSiteUrl, sNextFunction)
    __createCharacters(oGui, 'W', sSecurity, sSiteUrl, sNextFunction)
    __createCharacters(oGui, 'X', sSecurity, sSiteUrl, sNextFunction)
    __createCharacters(oGui, 'Y', sSecurity, sSiteUrl, sNextFunction)
    __createCharacters(oGui, 'Z', sSecurity, sSiteUrl, sNextFunction)
    
    oGui.setEndOfDirectory()

def __createCharacters(oGui, sCharacter, sCookieValue, sSiteUrl, sNextFunction):
    oGuiElement = cGuiElement()
    oGuiElement.setSiteName(SITE_IDENTIFIER)
    oGuiElement.setFunction(sNextFunction)
    oGuiElement.setTitle(sCharacter)

    if (sCharacter == '#'):
        sCharacter = '_'

    sUrl = sSiteUrl + '/' + str(sCharacter) + '/'

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', sUrl)
    oOutputParameterHandler.addParameter('page', '1')
    oOutputParameterHandler.addParameter('security', sCookieValue)
    oGui.addFolder(oGuiElement, oOutputParameterHandler)

def displaySearch():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sSecurity = oInputParameterHandler.getValue('security')
    sSiteUrl = oInputParameterHandler.getValue('siteUrl')
    sNextFunction = oInputParameterHandler.getValue('nextFunction')

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):

        sSearchText = sSearchText.replace(' ', '+')
        sUrl = sSiteUrl + str(sSearchText) + '/'
        if (sNextFunction == 'movies'):
            __showMovies(sUrl, 1, sSecurity)
            return
        if (sNextFunction == 'series'):
            __showSeries(sUrl, 1, sSecurity)
            return
        return
    else:
        return
    oGui.setEndOfDirectory()

def displayGenre():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sSecurity = oInputParameterHandler.getValue('security')

    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('Cookie', sSecurity)
    sHtmlContent = oRequestHandler.request();

    sPattern = '<a href="([^"]+)" class="next level3">.*?<div>(.*?)</div>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        for aEntry in aResult[1]:            
            oGuiElement = cGuiElement()
            oGuiElement.setSiteName(SITE_IDENTIFIER)
            oGuiElement.setTitle(aEntry[1])
            oGuiElement.setFunction('checkIndexing')    
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('page', '1')

            URL_GENRE_CHARACTERS = URL_MAIN + str(aEntry[0])
            
            oOutputParameterHandler.addParameter('siteUrl', URL_GENRE_CHARACTERS)        
            oOutputParameterHandler.addParameter('security', sSecurity)
            oOutputParameterHandler.addParameter('nextFunction', 'showMovies')

            oGui.addFolder(oGuiElement, oOutputParameterHandler)

    oGui.setEndOfDirectory()

def checkIndexing():
    oInputParameterHandler = cInputParameterHandler()
    sSiteUrl = oInputParameterHandler.getValue('siteUrl')
    
    oRequest = cRequestHandler(sSiteUrl)
    html = oRequest.request()
    
    if html.find('<div class="list-letters-top">') != -1:
        showCharacters()
    else:
        showMovies()

def showMovies():
    oInputParameterHandler = cInputParameterHandler()
    sSiteUrl = oInputParameterHandler.getValue('siteUrl')
    iPage = oInputParameterHandler.getValue('page')
    sSecurity = oInputParameterHandler.getValue('security')

    __showMovies(sSiteUrl, iPage, sSecurity)

def showSeries():
    oInputParameterHandler = cInputParameterHandler()
    sSiteUrl = oInputParameterHandler.getValue('siteUrl')
    iPage = oInputParameterHandler.getValue('page')
    sSecurity = oInputParameterHandler.getValue('security')

    __showSeries(sSiteUrl, iPage, sSecurity)

def __getLanguageTitle(sHtmlContent):
    sPattern = 'alt="([^"]+)"'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    sResult = '';

    if (aResult[0] == True):
        for aEntry in aResult[1]:
            if (aEntry == 'ENG'):
                sResult = sResult + ' (eng)'
            if (aEntry == 'GER'):
                sResult = sResult + ' (deu)'

    return sResult

def __replaceSpecialCharacters(txt):
    # Umlaute
    dict = {
        '\\u00e4':'\xe4',
        '\\u00f6':'\xf6',
        '\\u00fc':'\xfc',
        '\\u00df':'\xdf',
        '&amp;':'&'
    }
    for name, value in dict.iteritems():
        if name in txt:
            txt = txt.replace(name, value)
    return txt
    
def __showSeries(sSiteUrl, iPage, sSecurity):
    oGui = cGui()

    sUrl = str(sSiteUrl) + str('page/') + str(iPage)

    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('Cookie', sSecurity)
    sHtmlContent = oRequestHandler.request()
    
    sHtmlContent = __replaceSpecialCharacters(str(sHtmlContent))
    sHtmlContent = sHtmlContent.replace('\\', '')

    sPattern = '<tr class="row">.*?<a href="([^"]+).*?>(.*?)</a>.*?<td class="list-languages">(.*?)</td>'
    
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    if (aResult[0] == True):
        for aEntry in aResult[1]:
            oGuiElement = cGuiElement()
            oGuiElement.setSiteName(SITE_IDENTIFIER)
            oGuiElement.setFunction('showSeason')
            oGuiElement.setTitle(cUtil().removeHtmlTags(aEntry[1]) + __getLanguageTitle(str(aEntry[2])))
           
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + str(aEntry[0]))
            oOutputParameterHandler.addParameter('security', sSecurity)
            oGui.addFolder(oGuiElement, oOutputParameterHandler)
    else:
        log(sUrl)
        sPattern = '<p class="error center">.*?keine Eintr\u00e4ge.*?</p>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == False):
            # exaktes Suchergebnis
            sPattern = '<div class="description">\s*<div class="text">\s*<h3><a href="[^"]+">([^<]+)</a></h3>'
            #sPattern = '<table class="description">.*?<img src="([^"]+)".*?<h3>.*?>([^<]+)</a></h3>.*?</table>'
            sUrl = sUrl.replace('de/ajax/module','').replace('/page/1','')
            sHtmlContent = cRequestHandler(sUrl).request()
            aResult = oParser.parse(sHtmlContent, sPattern)
            
            oGuiElement = cGuiElement()
            oGuiElement.setSiteName(SITE_IDENTIFIER)
            oGuiElement.setFunction('showSeason')
            oGuiElement.setTitle(aResult[1][0])            
            
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('security', sSecurity)
            oGui.addFolder(oGuiElement, oOutputParameterHandler)
            oGui.setEndOfDirectory()
            return
            
    sNextUrl = __checkForNextPage(sHtmlContent, iPage)
    log('keine naechste Seite')
    if (sNextUrl != False):
        oGuiElement = cGuiElement()
        oGuiElement.setSiteName(SITE_IDENTIFIER)
        oGuiElement.setFunction('showSeries')
        oGuiElement.setTitle('next ..')

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sSiteUrl)
        oOutputParameterHandler.addParameter('page', int(iPage) + 1)
        oOutputParameterHandler.addParameter('security', sSecurity)
        oGui.addFolder(oGuiElement, oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showSeason():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sSiteUrl = oInputParameterHandler.getValue('siteUrl')
    sSecurity = oInputParameterHandler.getValue('security')

    oRequestHandler = cRequestHandler(sSiteUrl)
    oRequestHandler.addHeaderEntry('Cookie', sSecurity)
    sHtmlContent = oRequestHandler.request();
    sHtmlContent = __replaceSpecialCharacters(str(sHtmlContent)).replace('\\', '')
    
    sPattern = '<tr class="row">.*?<a href="([^"]+).*?>(.*?)</a>.*?<td class="list-languages">(.*?)</td>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        for aEntry in aResult[1]:
            oGuiElement = cGuiElement()
            oGuiElement.setSiteName(SITE_IDENTIFIER)
            if (aEntry[0].count('category') > 0):
              oGuiElement.setFunction('showEpisodes')
            else:
              oGuiElement.setFunction('showRelease')              
            oGuiElement.setTitle(cUtil().removeHtmlTags(aEntry[1]) + __getLanguageTitle(str(aEntry[2])))

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('movieUrl', URL_MAIN + str(aEntry[0]))
            oOutputParameterHandler.addParameter('security', sSecurity)
            oGui.addFolder(oGuiElement, oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showEpisodes():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sSiteUrl = oInputParameterHandler.getValue('movieUrl')
    sSecurity = oInputParameterHandler.getValue('security')

    oRequestHandler = cRequestHandler(sSiteUrl)
    oRequestHandler.addHeaderEntry('Cookie', sSecurity)
    sHtmlContent = oRequestHandler.request();
    sHtmlContent = __replaceSpecialCharacters(str(sHtmlContent)).replace('\\', '')

    sPattern = '<tr class="row">.*?<a href="([^"]+).*?>(.*?)</a>.*?<td class="list-languages">(.*?)</td>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        for aEntry in aResult[1]:
            oGuiElement = cGuiElement()
            oGuiElement.setSiteName(SITE_IDENTIFIER)
            oGuiElement.setFunction('showRelease')
            oGuiElement.setTitle(cUtil().removeHtmlTags(aEntry[1])  + __getLanguageTitle(str(aEntry[2])))

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('movieUrl', URL_MAIN + str(aEntry[0]))
            oOutputParameterHandler.addParameter('security', sSecurity)
            oGui.addFolder(oGuiElement, oOutputParameterHandler)

    oGui.setEndOfDirectory()

def __showMovies(sSiteUrl, iPage, sSecurity):
    oGui = cGui()

    sUrl = str(sSiteUrl) + str('page/') + str(iPage)

    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('Cookie', sSecurity)
    sHtmlContent = oRequestHandler.request();
    sHtmlContent = __replaceSpecialCharacters(str(sHtmlContent))
    sHtmlContent = sHtmlContent.replace('\\', '')
    sPattern = '<table class="row">.*?class="list-cover".*?<img src="([^"]+)">.*?class="list-name".*?<a href="([^"]+)".*?>(.*?)</a>.*?class="description".*?>(.*?)</td>.*?<td class="list-languages">(.*?)</td>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    if (aResult[0] == True):
        for aEntry in aResult[1]:
            oGuiElement = cGuiElement()
            oGuiElement.setSiteName(SITE_IDENTIFIER)
            oGuiElement.setFunction('showRelease')
            oGuiElement.setTitle(cUtil().removeHtmlTags(aEntry[2])  + __getLanguageTitle(str(aEntry[4])))
            oGuiElement.setThumbnail(aEntry[0])
            oGuiElement.setDescription(aEntry[3])

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('movieUrl', URL_MAIN + str(aEntry[1]))
            oOutputParameterHandler.addParameter('security', sSecurity)
            oGui.addFolder(oGuiElement, oOutputParameterHandler)
    else:
        sPattern = '<p class="error center">.*?keine Eintr.*?</p>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == False):
            # exaktes Suchergebnis
            sPattern = '<table class="description">.*?<img src="([^"]+)".*?<h3>.*?>([^<]+)</a></h3>.*?</table>'
            sUrl = sUrl.replace('de/ajax/module','').replace('/page/1','')
            sHtmlContent = cRequestHandler(sUrl).request()
            aResult = oParser.parse(sHtmlContent, sPattern)
            
            oGuiElement = cGuiElement()
            oGuiElement.setSiteName(SITE_IDENTIFIER)
            oGuiElement.setFunction('showRelease')
            oGuiElement.setTitle(aResult[1][0][1])
            oGuiElement.setThumbnail(aResult[1][0][0])
            oGuiElement.setDescription('')
            
            
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('movieUrl', sUrl)
            oOutputParameterHandler.addParameter('security', sSecurity)
            oGui.addFolder(oGuiElement, oOutputParameterHandler)
            oGui.setEndOfDirectory()
            return
        
    sNextUrl = __checkForNextPage(sHtmlContent, iPage)
    if (sNextUrl != False):
        oGuiElement = cGuiElement()
        oGuiElement.setSiteName(SITE_IDENTIFIER)
        oGuiElement.setFunction('showMovies')
        oGuiElement.setTitle('next ..')

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sSiteUrl)
        oOutputParameterHandler.addParameter('page', int(iPage) + 1)
        oOutputParameterHandler.addParameter('security', sSecurity)
        oGui.addFolder(oGuiElement, oOutputParameterHandler)

    oGui.setEndOfDirectory()

def __checkForNextPage(sHtmlContent, iCurrentPage):
    iNextPage = int(iCurrentPage) + 1
    iNextPage = str(iNextPage)

    if (sHtmlContent.find('<td class="list-pages-with-type pages">') != -1):
        sPattern = '<td class="list-pages-with-type pages">(.*?)</td>'
    else:
        sPattern = '<div class="list-pages pages">(.*?)</div>'
    
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        html = aResult[1][0]
        sPattern = '<a href=".*?/page/' + iNextPage + '/">(.*?)</a>'
        aResult = oParser.parse(html, sPattern)
        return aResult[0]
    
    return False


def showCinemaMovies():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')    
    sSecurity = oInputParameterHandler.getValue('security')

    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('Cookie', sSecurity)
    sHtmlContent = oRequestHandler.request();    
    sHtmlContent = __replaceSpecialCharacters(str(sHtmlContent)).replace('\\','')

    sPattern = '<div id="ToptitleSliderContent1" class="toptitle-slider-content".*?>(.*?)</div>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        for aEntryHtml in aResult[1]:
            sPattern = '<a href="([^"]+)"><img src="([^"]+)".*?data-tooltip="([^"]+)"'
            oParser = cParser()
            aResult = oParser.parse(aResult[1][0], sPattern)

            if (aResult[0] == True):
                for aEntry in aResult[1]:
                    oGuiElement = cGuiElement()
                    oGuiElement.setSiteName(SITE_IDENTIFIER)
                    oGuiElement.setFunction('showRelease')
                    oGuiElement.setTitle(cUtil().removeHtmlTags(aEntry[2]))
                    oGuiElement.setThumbnail(aEntry[1])
                  
                    oOutputParameterHandler = cOutputParameterHandler()
                    oOutputParameterHandler.addParameter('movieUrl', URL_MAIN + str(aEntry[0]))
                    oOutputParameterHandler.addParameter('security', sSecurity)
                    oGui.addFolder(oGuiElement, oOutputParameterHandler)

    oGui.setEndOfDirectory()

def __createInfo(oGui, sHtmlContent):
    sPattern = '<table class="description">.*?<td class="cover"><a href="([^"]+)".*?<td class="text">(.*?)</td>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        for aEntry in aResult[1]:
            oGuiElement = cGuiElement()
            oGuiElement.setSiteName(SITE_IDENTIFIER)
            oGuiElement.setTitle('info (press Info Button)')
            oGuiElement.setThumbnail(str(aEntry[0]))
            oGuiElement.setFunction('dummyFolder')
            oGuiElement.setDescription(cUtil().removeHtmlTags(str(aEntry[1])))
            oGui.addFolder(oGuiElement)

def dummyFolder():
    oGui = cGui()
    oGui.setEndOfDirectory()

def showRelease():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sSecurity = oInputParameterHandler.getValue('security')
    sUrl = oInputParameterHandler.getValue('movieUrl')
    
    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('Cookie', sSecurity)
    sHtmlContent = oRequestHandler.request();

    __createInfo(oGui, sHtmlContent)

    sPattern = '<table class="release-list">(.*?)</table>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        for aEntryHtml in aResult[1]:
            sPattern = '<tr class="row">.*?<a href="/de/([^"]+)">(.*?)</a>.*?<td class="list-languages">(.*?)</td>.*?class="release-types">(.*?)</td>'
            oParser = cParser()
            aResult = oParser.parse(aEntryHtml, sPattern)

            if (aResult[0] == True):
                for aEntry in aResult[1]:
                    oGuiElement = cGuiElement()
                    oGuiElement.setSiteName(SITE_IDENTIFIER)
                    oGuiElement.setFunction('showStreams')
                    oGuiElement.setTitle(cUtil().removeHtmlTags(aEntry[1]) + __getLanguageTitle(aEntry[2]))

                    oOutputParameterHandler = cOutputParameterHandler()
                    oOutputParameterHandler.addParameter('movieUrl', URL_MAIN + str(aEntry[0]))
                    oOutputParameterHandler.addParameter('security', sSecurity)
                    oGui.addFolder(oGuiElement, oOutputParameterHandler)
    else:
        sPattern = '<div class="module-item">\s*<h1>\s*([^<]+)\s*</h1>\s*<div class="module-content ddl">\s*<div id="rts">'
        #sPattern = '<a href="([^"]+)" target="_self" data-tab="ReleaseTab" data-tab-name="Downloads">Downloads</a>'
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)

        if (aResult[0] == True):
            for aEntry in aResult[1]:
                oGuiElement = cGuiElement()
                oGuiElement.setSiteName(SITE_IDENTIFIER)
                oGuiElement.setFunction('showStreams')

                #sPattern = '<a href="/de/de/release/(.*?)">([^"]+)</a>'
                #oParser = cParser()
                #aResultTitle = oParser.parse(sHtmlContent, sPattern)
                
                #if (aResultTitle[0] == True):
                #    sTitle = aResultTitle[1][0][1]                    
                #    oGuiElement.setTitle(sTitle)
                #else:
                #    oGuiElement.setTitle('no title')
                
                sTitle = aResult[1][0]
                oGuiElement.setTitle(sTitle)
                
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('movieUrl', sUrl)
                oOutputParameterHandler.addParameter('security', sSecurity)
                oGui.addFolder(oGuiElement, oOutputParameterHandler)
        else:
            #sPattern = '<div class="module-footer"></div>\r</div>\r<div class="module-item">\r <h1>\r (.*?)</h1>\r <div class="module-content ddl">\r <div id="ReleaseTabs">'
            #log('H2A2A2A2AA')
            sPattern = '(<a href="[^"]+">[^<]+</a> &raquo;.*?<a href="[^"]+">[^<]+</a>.*?</h1>)'
            oParser = cParser()
            aResult = oParser.parse(sHtmlContent, sPattern)
	    
            if (aResult[0] == True):
                for aEntry in aResult[1]:
                    oGuiElement = cGuiElement()
                    oGuiElement.setSiteName(SITE_IDENTIFIER)
                    oGuiElement.setFunction('showStreams')		    

                    sPattern = '&raquo;\s*<a href="(.*?)">([^<]+)</a>\s*</h1>'
                    oParser = cParser()
                    aResultTitle = oParser.parse(aEntry, sPattern)
		    
                    if (aResultTitle[0] == True):
                        sTitle = aResultTitle[1][0][1]                    
                        oGuiElement.setTitle(sTitle)
                    else:
                        oGuiElement.setTitle('no title')

                    oOutputParameterHandler = cOutputParameterHandler()
                    oOutputParameterHandler.addParameter('movieUrl', sUrl)
                    oOutputParameterHandler.addParameter('security', sSecurity)
                    oGui.addFolder(oGuiElement, oOutputParameterHandler)
    oGui.setEndOfDirectory()




def showStreams():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('movieUrl')
    sSecurity = oInputParameterHandler.getValue('security')

    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('Cookie', sSecurity)
    sHtmlContent = oRequestHandler.request();

    sPattern = 'id="LinksVideoStreams"(.*?)</table>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        for aEntryHtml in aResult[1]:
            __parseHosters('All', oGui, aEntryHtml)

    sPattern = '<div class="link-stream-files"(.*?)<div class="release-stream-embed"'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        sPattern = '<a class="link-stream-file-.*?</a>'
        aResult = oParser.parse(aResult[1][0], sPattern)
        if (aResult[0]==True):
            for aEntryHtml in aResult[1]:
                __parseHosters('All',oGui,aEntryHtml)
                
    oGui.setEndOfDirectory()
    return

def __parseHosters(sFormat, oGui, sHtmlContent):
    oGui = cGui()
    sPattern = "return se_ddd\(\d+,'([^']*)',\d+,'([^']*)','([^']*)'.*?"
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        for aEntry in aResult[1]:
            oHoster = __getHoster(str(aEntry[0]))
            if (oHoster != False):
                sTitle = str(aEntry[0]) + ' - ' + str(aEntry[1])
                oHoster.setDisplayName(sTitle)
                oHoster.setFileName(sTitle)
                cHosterGui().showHoster(oGui, oHoster, str(aEntry[2]))                


def __getHoster(sHosterName):
    return cHosterHandler().getHoster2(sHosterName)

def __createTitleWithLanguage(sLanguage, sTitle):
    sTitle = cUtil().removeHtmlTags(sTitle, '')
    sTitle = str(sTitle).replace('\t', '').replace('&amp;', '&')

    if (sLanguage == 'GER'):
        return sTitle + ' (de)'
    if (sLanguage == 'ENG'):
	return sTitle + ' (en)'

    return sTitle
