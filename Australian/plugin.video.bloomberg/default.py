import sys, os
import collections
import urllib
import re
import subprocess
import xbmc, xbmcgui, xbmcaddon, xbmcplugin

from resources.BeautifulSoup import BeautifulStoneSoup,NavigableString
import resources.scraper
reload( resources.scraper)


##############################################################
__XBMC_Revision__	= xbmc.getInfoLabel('System.BuildVersion')
__settings__		= xbmcaddon.Addon( id=os.path.basename(os.getcwd())) #xbmcaddon.Addon(id='plugin.video.sbs2')
__language__		= __settings__.getLocalizedString
__version__			= __settings__.getAddonInfo('version')
__cwd__				= __settings__.getAddonInfo('path')
__addonname__		= __settings__.getAddonInfo('name')
__addonid__			= __settings__.getAddonInfo('id')
##############################################################


def addDir(params, folder = False, info = {}, still="DefaultFolder.png"):
	name = params["name"]
	url =  sys.argv[0] + "?" + "&".join(["%s=%s" % (urllib.quote_plus(k),urllib.quote_plus(str(v)))    for k, v in params.items()])
	print "::", url,  params, info, "%%"
	liz=xbmcgui.ListItem(name, iconImage=still, thumbnailImage="")
	if info:
		liz.setInfo("video", info)

	if not folder:
		liz.addContextMenuItems( [("Record to disk", "XBMC.RunPlugin(%s?&%s)"   % (sys.argv[0], url.replace("mode=1", "mode=3").replace("mode=2", "mode=3") ))] )

	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz,isFolder=folder)
	return ok

##############################################################
def INDEX(params):
	path = params.get("path", None)
	
	scraper = resources.scraper.MenuItems()
	if path is None:
	
		#addDir({
		#	"path"	: "",
		#	"name"	: "Live Stream",
		#	"url"	: "rtmp://cp87869.live.edgefcs.net:1935/live app=ondemand?_fcs_vhost=cp115717.edgefcs.net playpath=us_300@21006 pageURL=http://www.bloomberg.com/tv/  swfUrl=http://player.ooyala.com/static/cacheable/1c3d7af1e06c53793eb20187993e2276/player_v2.swf/[[DYNAMIC]]/1  swfVfy=true live=true",
		#	"mode"	: "2"
		#}, False)
		addDir({"path" : "http://www.bloomberg.com/tv/", "name" : "Live Stream", "url" : "http://www.bloomberg.com/tv/", "mode" : "2"} , False)

		
		for title, id, desc, img in scraper.menu_main(path):
			addDir({"path" : id, "name" : title, "url" : id, "mode" : "0"}, True, {"plot": desc}, img)
	else:
		shows,pagination = scraper.menu_shows(path)
		for (title, id) in pagination:
			addDir({"path" : id, "name" : title, "url" : id, "mode" : "0"}, True, {})
		 
		for (title, id, desc, img,dur) in shows:
			addDir({"path" : id, "name" : title, "url" : id, "mode" : "1"}, False, {"plot": desc, "duration":dur }, img)
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_UNSORTED )
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_LABEL )		
	xbmcplugin.endOfDirectory(int(sys.argv[1]))


	
def play(params):
	scraper = resources.scraper.MenuItems()
	xbmc.Player(xbmc.PLAYER_CORE_DVDPLAYER).play(scraper.menu_play(params["url"])[0], xbmcgui.ListItem(params["name"]))
	
def play2(params):
	scraper = resources.scraper.MenuItems()
	
	rtmp		= "rtmp://%s/live?_fcs_vhost=cp116697.live.edgefcs.net/%s_640_360_1000@18679 live=true" % (scraper.rtmp_get(), scraper.embed_code_get(params["url"]))	
	xbmc.Player(xbmc.PLAYER_CORE_DVDPLAYER).play(rtmp, xbmcgui.ListItem(params["name"]))

def record(params):		
	scraper = resources.scraper.MenuItems()
	print scraper.menu_play(params["url"])
	rtmp, app, playpath = scraper.menu_play(params["url"])[1]
	
	args = __settings__.getSetting( "rtmpdump" ), "-o%s%s.mp4" % (__settings__.getSetting( "path" ), "".join(c for c in params["name"].split("/")[-1] if c not in "?:/\\*@#$!~^" )), "--rtmp=%s" % rtmp, "--playpath=%s" % playpath
	print args
	subprocess.call(args)
	
	
##############################################################
MODE_MAP	= {
	"0"	: lambda params:	INDEX(params),
	"1"	: lambda url:		play(url),
	"2"	: lambda url:		play2(url),
	"3"	: lambda params: 	record(params)
}


def parse_args(args):
	out = {}
	if args[2]:
		for item in (args[2].split("?")[-1].split("&")):
#			print item
			items = item.split("=")
			k,v = items[0], "=".join(items[1:])
			out[k] = urllib.unquote_plus(v)
	return out


def main():
	params = parse_args(sys.argv)
	print "##", sys.argv, params
	MODE_MAP[params.get("mode", "0")](params)


main()