from resources.lib.handler.jdownloaderHandler import cJDownloaderHandler
from resources.lib.download import cDownload
from resources.lib.handler.hosterHandler import cHosterHandler
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.player import cPlayer
from resources.lib.handler.requestHandler import cRequestHandler
import logger
import xbmcaddon

class cHosterGui:

    SITE_NAME = 'cHosterGui'

    # step 1 - bGetRedirectUrl in ein extra optionsObject verpacken
    def showHoster(self, oGui, oHoster, sMediaUrl, bGetRedirectUrl = False):
        oGuiElement = cGuiElement()
        oGuiElement.setSiteName(self.SITE_NAME)
        oGuiElement.setFunction('showHosterMenu')
        oGuiElement.setTitle(oHoster.getDisplayName())

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('sMediaUrl', sMediaUrl)
        oOutputParameterHandler.addParameter('sHosterIdentifier', oHoster.getPluginIdentifier())
        oOutputParameterHandler.addParameter('bGetRedirectUrl', bGetRedirectUrl)
        oOutputParameterHandler.addParameter('sFileName', oHoster.getFileName())

        oGui.addFolder(oGuiElement, oOutputParameterHandler)

    # step 2
    def showHosterMenu(self):
        oGui = cGui()
        oInputParameterHandler = cInputParameterHandler()

        sHosterIdentifier = oInputParameterHandler.getValue('sHosterIdentifier')
        sMediaUrl = oInputParameterHandler.getValue('sMediaUrl')
        bGetRedirectUrl = oInputParameterHandler.getValue('bGetRedirectUrl')
        sFileName = oInputParameterHandler.getValue('sFileName')

        oHoster = cHosterHandler().getHoster(sHosterIdentifier)
        oHoster.setFileName(sFileName)
        
        self.showHosterMenuDirect(oGui, oHoster, sMediaUrl, bGetRedirectUrl)
        
        oGui.setEndOfDirectory()

    def showHosterMenuDirect(self, oGui, oHoster, sMediaUrl, bGetRedirectUrl=False):
        # play
        self.__showPlayMenu(oGui, sMediaUrl, oHoster, bGetRedirectUrl)

        # playlist
        self.__showPlaylistMenu(oGui, sMediaUrl, oHoster, bGetRedirectUrl)

        # download
        if (oHoster.isDownloadable() == True):
            self.__showDownloadMenu(oGui, sMediaUrl, oHoster, bGetRedirectUrl)        

        # JD
        if (oHoster.isJDownloaderable() == True):
            self.__showJDMenu(oGui, sMediaUrl, oHoster, bGetRedirectUrl)	

        
    def __showPlayMenu(self, oGui, sMediaUrl, oHoster, bGetRedirectUrl):
        oGuiElement = cGuiElement()
        oGuiElement.setSiteName(self.SITE_NAME)
        oGuiElement.setFunction('play')
        oGuiElement.setTitle('play')
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('sMediaUrl', sMediaUrl)
        oOutputParameterHandler.addParameter('sHosterIdentifier', oHoster.getPluginIdentifier())
        oOutputParameterHandler.addParameter('bGetRedirectUrl', bGetRedirectUrl)
        oOutputParameterHandler.addParameter('sFileName', oHoster.getFileName())
        oGui.addFolder(oGuiElement, oOutputParameterHandler)

    def __showDownloadMenu(self, oGui, sMediaUrl, oHoster, bGetRedirectUrl):
        oGuiElement = cGuiElement()
        oGuiElement.setSiteName(self.SITE_NAME)
        oGuiElement.setFunction('download')
        oGuiElement.setTitle('download ueber XBMC')
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('sMediaUrl', sMediaUrl)
        oOutputParameterHandler.addParameter('sHosterIdentifier', oHoster.getPluginIdentifier())
        oOutputParameterHandler.addParameter('bGetRedirectUrl', bGetRedirectUrl)
        oOutputParameterHandler.addParameter('sFileName', oHoster.getFileName())
        oGui.addFolder(oGuiElement, oOutputParameterHandler)

    def __showJDMenu(self, oGui, sMediaUrl, oHoster, bGetRedirectUrl):
        oGuiElement = cGuiElement()
        oGuiElement.setSiteName(self.SITE_NAME)        
        oGuiElement.setTitle('an JDownloader senden')
        oGuiElement.setFunction('sendToJDownbloader')
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('sMediaUrl', sMediaUrl)
        oOutputParameterHandler.addParameter('sHosterIdentifier', oHoster.getPluginIdentifier())
        oOutputParameterHandler.addParameter('bGetRedirectUrl', bGetRedirectUrl)
        oOutputParameterHandler.addParameter('sFileName', oHoster.getFileName())
        oGui.addFolder(oGuiElement, oOutputParameterHandler)

    def __showPlaylistMenu(self, oGui, sMediaUrl, oHoster, bGetRedirectUrl):
        oGuiElement = cGuiElement()
        oGuiElement.setSiteName(self.SITE_NAME)
        oGuiElement.setFunction('addToPlaylist')
        oGuiElement.setTitle('add to playlist')
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('sMediaUrl', sMediaUrl)
        oOutputParameterHandler.addParameter('sHosterIdentifier', oHoster.getPluginIdentifier())
        oOutputParameterHandler.addParameter('bGetRedirectUrl', bGetRedirectUrl)
        oOutputParameterHandler.addParameter('sFileName', oHoster.getFileName())
        oGui.addFolder(oGuiElement, oOutputParameterHandler)

    def play(self):
        oGui = cGui()
        oInputParameterHandler = cInputParameterHandler()

        sHosterIdentifier = oInputParameterHandler.getValue('sHosterIdentifier')
        sMediaUrl = oInputParameterHandler.getValue('sMediaUrl')
        bGetRedirectUrl = oInputParameterHandler.getValue('bGetRedirectUrl')
        sFileName = oInputParameterHandler.getValue('sFileName')

        if (bGetRedirectUrl == 'True'):            
            sMediaUrl = self.__getRedirectUrl(sMediaUrl)

        logger.info('call play: ' + sMediaUrl)
        oHoster = cHosterHandler().getHoster(sHosterIdentifier)
        oHoster.setFileName(sFileName)

        #try:
        
        oHoster.setUrl(sMediaUrl)
        aLink = oHoster.getMediaLink()
        
        if (aLink[0] == True):
            oGuiElement = cGuiElement()
            oGuiElement.setSiteName(self.SITE_NAME)
            oGuiElement.setMediaUrl(aLink[1])
	    oGuiElement.setTitle(oHoster.getFileName())

            oPlayer = cPlayer()
	    oPlayer.clearPlayList()
            oPlayer.addItemToPlaylist(oGuiElement)
            oPlayer.startPlayer()
            return

        #except:
        #    logger.fatal('could not load plugin: ' + sHosterFileName)

        oGui.setEndOfDirectory()

    def addToPlaylist(self):
        oGui = cGui()
        oInputParameterHandler = cInputParameterHandler()

        sHosterIdentifier = oInputParameterHandler.getValue('sHosterIdentifier')
        sMediaUrl = oInputParameterHandler.getValue('sMediaUrl')
        bGetRedirectUrl = oInputParameterHandler.getValue('bGetRedirectUrl')
        sFileName = oInputParameterHandler.getValue('sFileName')

        if (bGetRedirectUrl == 'True'):
            sMediaUrl = self.__getRedirectUrl(sMediaUrl)

        logger.info('call play: ' + sMediaUrl)
        oHoster = cHosterHandler().getHoster(sHosterIdentifier)
        oHoster.setFileName(sFileName)

        #try:

        oHoster.setUrl(sMediaUrl)
        aLink = oHoster.getMediaLink()

        if (aLink[0] == True):
            oGuiElement = cGuiElement()
            oGuiElement.setSiteName(self.SITE_NAME)
            oGuiElement.setMediaUrl(aLink[1])
            oGuiElement.setTitle(oHoster.getFileName())

            oPlayer = cPlayer()
            oPlayer.addItemToPlaylist(oGuiElement)
            oGui.showInfo('Playlist', str(oHoster.getFileName()) +  ' wurde hinzugefuegt', 5);
            return

        #except:
        #    logger.fatal('could not load plugin: ' + sHosterFileName)

        oGui.setEndOfDirectory()

    def download(self):
        oGui = cGui()
        oInputParameterHandler = cInputParameterHandler()

        sHosterIdentifier = oInputParameterHandler.getValue('sHosterIdentifier')
        sMediaUrl = oInputParameterHandler.getValue('sMediaUrl')
        bGetRedirectUrl = oInputParameterHandler.getValue('bGetRedirectUrl')
        sFileName = oInputParameterHandler.getValue('sFileName')

        if (bGetRedirectUrl == 'True'):
            sMediaUrl = self.__getRedirectUrl(sMediaUrl)

        logger.info('call download: ' + sMediaUrl)

        oHoster = cHosterHandler().getHoster(sHosterIdentifier)
        oHoster.setFileName(sFileName)

        selfAddon = xbmcaddon.Addon(id='plugin.video.xstream')
        sPath = str(selfAddon.getSetting('download-folder'))

        #try:
        oHoster.setUrl(sMediaUrl)
        aLink = oHoster.getMediaLink()
        if (aLink[0] == True):
            oDownload = cDownload()
            oDownload.download(aLink[1], oHoster.getFileName(), sPath)
            return

        #except:
        #    logger.fatal('could not load plugin: ' + sHosterFileName)

        oGui.setEndOfDirectory()

    def sendToJDownbloader(self):
        oGui = cGui()
        oInputParameterHandler = cInputParameterHandler()

        sHosterIdentifier = oInputParameterHandler.getValue('sHosterIdentifier')
        sMediaUrl = oInputParameterHandler.getValue('sMediaUrl')
        bGetRedirectUrl = oInputParameterHandler.getValue('bGetRedirectUrl')
        sFileName = oInputParameterHandler.getValue('sFileName')

        if (bGetRedirectUrl == 'True'):
            sMediaUrl = self.__getRedirectUrl(sMediaUrl)

        oHoster = cHosterHandler().getHoster(sHosterIdentifier)
        oHoster.setFileName(sFileName)
        oHoster.setUrl(sMediaUrl)
        sMediaUrl = oHoster.getUrl()

        logger.info('call send to JDownloader: ' + sMediaUrl)

        cJDownloaderHandler().sendToJDownloader(sMediaUrl)

        

    def __getRedirectUrl(self, sUrl):
        oRequest = cRequestHandler(sUrl)
        oRequest.request()
        return oRequest.getRealUrl()
