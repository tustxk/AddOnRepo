from about.about import cAboutGui
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.gui.gui import cGui
from resources.lib.handler.pluginHandler import cPluginHandler
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from xbmc import log
from xbmc import LOGDEBUG
import xbmc,xbmcplugin,xbmcgui,xbmcaddon
import sys,os

# Main starting function
def run():
  parseUrl()


def setView(content, viewType):
    #get settings
    selfAddon = xbmcaddon.Addon(id='plugin.video.xstream')

    # kept for reference only
    #movies_view = selfAddon.getSetting('movies-view')
    #tvshows_view = selfAddon.getSetting('tvshows-view')
    #episodes_view = selfAddon.getSetting('episodes-view')

    # set content type so library shows more views and info
    xbmcplugin.setContent(int(sys.argv[1]), content)
    if selfAddon.getSetting('auto-view') == 'true':
        xbmc.executebuiltin("Container.SetViewMode(%s)" % selfAddon.getSetting(viewType) )

    # set sort methods - probably we don't need all of them
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_UNSORTED )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_LABEL )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_VIDEO_RATING )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_DATE )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_PROGRAM_COUNT )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_VIDEO_RUNTIME )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_GENRE )
  
  
def parseUrl():
  setView('movies', 'movies-view')

  oInputParameterHandler = cInputParameterHandler()

  # If no function is set, we set it to the default "load" function
  if oInputParameterHandler.exist("function"):
    sFunction = oInputParameterHandler.getValue("function")
  else:
    sFunction = "load"

  log("Call %s function" % sFunction, level = LOGDEBUG)

  # Test if we should run a function on a special site
  if oInputParameterHandler.exist('site'):
    sSiteName = oInputParameterHandler.getValue('site')

    log("Call %s() from %s" % (sFunction, sSiteName), level = LOGDEBUG)

    # Don't want any statistic so i delete the plugin and comment this part out
#   if sFunction == "load":
#     cStatistic().callStartPlugin(sSiteName)

    # If the hoster gui is called, run the function on it and return
    if isHosterGui(sSiteName, sFunction):
      return

    # If the about gui is called, run the function on it and return
    if isAboutGui(sSiteName, sFunction):
      return

    # Else load any other site as plugin and run the function
    exec "import %s as plugin" % sSiteName
    exec "plugin.%s()" % sFunction
  else:
    # As a default if no site was specified, we run the default starting gui with all plugins
    oGui = cGui()
    oPluginHandler = cPluginHandler()

    aPlugins = oPluginHandler.getAvailablePlugins()

    if len(aPlugins) <= 0:
      log("No Plugins found", level = LOGDEBUG)

      # Open the settings dialog to choose a plugin that could be enable
      oGui.openSettings()
      oGui.updateDirectory()
    else:
      # Create a gui element for every plugin found
      for aPlugin in aPlugins:
        oGuiElement = cGuiElement()
        oGuiElement.setTitle(aPlugin[0])
        oGuiElement.setSiteName(aPlugin[1])
        oGuiElement.setFunction(sFunction)
        oGui.addFolder(oGuiElement)

    oGui.setEndOfDirectory()

def isHosterGui(sSiteName, sFunction):
  if sSiteName == "cHosterGui":
    oHosterGui = cHosterGui()
    exec "oHosterGui.%s()" % sFunction

    return True

  return False

def isAboutGui(sSiteName, sFunction):
  if sSiteName == "cAboutGui":
    oAboutGui = cAboutGui()
    exec "oAboutGui.%s()" % sFunction

    return True

  return False
