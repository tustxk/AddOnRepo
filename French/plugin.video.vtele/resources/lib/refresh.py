import xbmc
import xbmcgui
import scraper

DIALOG_PROGRESS = xbmcgui.DialogProgress()

try:
    DIALOG_PROGRESS.create( "vTélé", "Rafraîchissement..." )
    xbmc.sleep( 1000 )
    scraper.refreshAllEmissions( DIALOG_PROGRESS )
except:
    pass

xbmc.executebuiltin( 'Dialog.Close(10101)' )
xbmc.executebuiltin( 'Container.Refresh' )