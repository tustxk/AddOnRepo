import sys, os
import collections
import urllib
import re
import subprocess
import xbmc, xbmcgui, xbmcaddon, xbmcplugin

import scraper


##############################################################
ID = 'plugin.video.plus72' #os.path.basename(os.getcwd())
__XBMC_Revision__	= xbmc.getInfoLabel('System.BuildVersion')
__settings__		= xbmcaddon.Addon( id=ID) #xbmcaddon.Addon(id='plugin.video.sbs2')
__language__		= __settings__.getLocalizedString
__version__			= __settings__.getAddonInfo('version')
__cwd__				= __settings__.getAddonInfo('path')
__addonname__		= __settings__.getAddonInfo('name')
__addonid__			= __settings__.getAddonInfo('id')
##############################################################


def addDir(params, folder = False, info = {}, still="DefaultFolder.png"):
	name = params["name"]
	liz=xbmcgui.ListItem(name, iconImage=still, thumbnailImage="")
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
	addon	= xbmcaddon.Addon( id=ID )
	bitrate	= int(addon.getSetting( "vid_quality" ))

	chosen = sorted(params, key=lambda rendition: abs(bitrate - (rendition['rate']/1024)))[0]
	xbmc.Player().play(chosen['url'])
	
	
	
def playbrowser(swfurl):
	import subprocess
	subprocess.call([
		__settings__.getSetting( "browser" ), 
		swfurl

	])
	
def record(params):		
	def rpt(c):
		if c not in set(" %*^&$#@!~:"):
			return c
		else:
			return "_"
	print params
	
	addon	= xbmcaddon.Addon( id=ID )
	bitrate	= int(addon.getSetting( "vid_quality" ))
	chosen = sorted(params, key=lambda rendition: abs(bitrate - (rendition['rate']/1024)))[0]

	name= '%s%s.mp4' % (
			__settings__.getSetting( "path" ), 
			"".join(rpt(c) for c in str(chosen["name"])),
			
		)
	args = (
		__settings__.getSetting( "ffmpeg" ), 
		'-i',  chosen["url"],
		"-vcodec", "copy",
		"-acodec", "copy", 
		name
	)
	startupinfo = None
	if os.name == 'nt':
		startupinfo = subprocess.STARTUPINFO()
		startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW		
	
	print " ".join(args)
	sout = open(name+".fmpeg.out", "w")
	serr = open(name+".ffmpeg.err", "w")
	try:
		xx = subprocess.call(args, stdin= subprocess.PIPE, stdout= sout, stderr= serr,shell= False, startupinfo=startupinfo)
	finally:
		sout.close()
		serr.close()	
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
	sc = scraper.Scraper(folders, play, record, playbrowser)
	getattr(sc, mode)(params)




main()