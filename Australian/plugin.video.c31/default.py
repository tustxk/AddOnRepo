import sys, os
import collections
import urllib
import re
import subprocess
import xbmc, xbmcgui, xbmcaddon, xbmcplugin

import scraper


##############################################################
__XBMC_Revision__	= xbmc.getInfoLabel('System.BuildVersion')
__settings__		= xbmcaddon.Addon( id=scraper.ADDON_ID)
__language__		= __settings__.getLocalizedString
__version__			= __settings__.getAddonInfo('version')
__cwd__				= __settings__.getAddonInfo('path')
__addonname__		= __settings__.getAddonInfo('name')
__addonid__			= __settings__.getAddonInfo('id')
##############################################################


def addDir(params, folder = False, info = {}, still="DefaultFolder.png"):
	name = params["name"]
	liz=xbmcgui.ListItem(name, iconImage=still, thumbnailImage=still)
	url =  sys.argv[0] + "?" + "&".join(["%s=%s" % (urllib.quote_plus(k),urllib.quote_plus(str(v)))    for k, v in params.items()])
	print ("::", url,  params, info, folder, "%%")		
	if info:
		liz.setInfo("video", info)
	if not folder:
		liz.addContextMenuItems( [("Record to disk", "XBMC.RunPlugin(%s?&%s)"   % (sys.argv[0], url + "&record=1"))] )
		
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz,isFolder=folder)
	return ok

##############################################################

	


def folders(params):
	for param in params:
		print "@@",param
		addDir({"name" : param['title'], "url" : param["url"], "path" : param["path"]}, param["folder"], info = param.get("info", {}), still = param.get("still", "DefaultFolder.png"))

	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_UNSORTED )
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_LABEL )
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_VIDEO_RATING )
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_DATE )
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_PROGRAM_COUNT )
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_VIDEO_RUNTIME )
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_GENRE )	   
	xbmcplugin.endOfDirectory(int(sys.argv[1]))

def play(params):
	print params
	xbmc.Player(xbmc.PLAYER_CORE_DVDPLAYER).play("{0}".format(params["url"]), xbmcgui.ListItem(params["name"]))

def record(params):		
	def rpt(c):
		if c not in set("/\\ %*^&$#@!~:"):
			return c
		else:
			return "_"

	print params
	items = params["url"].split()
	
	rtmp		= items[0]
	playpath	= items[1].split("=",1)[-1]
	swfurl		= items[2].split("=",1)[-1]
	swfvfy		= items[3].split("=",1)[-1]
	
	
	#outlog = open("%s.log" % (__settings__.getSetting( "path" )), 'w+')
	try:
		
		args = __settings__.getSetting( "rtmpdump" ), '-o%s%s.mp4' % (__settings__.getSetting( "path" ), "".join(rpt(c) for c in str(params["name"]))), "--rtmp=%s" % rtmp, "--playpath=%s" % playpath, "--swfVfy=%s" % swfurl, "--quiet"
		#, "--swfurl=%s" % swfurl, 
		print args
		startupinfo = None
		if os.name == 'nt':
			startupinfo = subprocess.STARTUPINFO()
			startupinfo.dwFlags |= 1#subprocess.STARTF_USESHOWWINDOW		
		subprocess.call(args, stdin= subprocess.PIPE, stdout= subprocess.PIPE, stderr= subprocess.STDOUT, shell= False, startupinfo=startupinfo)
	except:
		#outlog.close()
		raise
	
##############################################################


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
	mode	= params.get("path", "menu")
	print "$$", mode
	sc = scraper.Scraper(folders, play, record)
	getattr(sc, mode)(params)




main()