### ############################################################################################################
###	#	
### # Project: 			#		The Anime Highway - by The Highway 2013.
### # Author: 			#		The Highway
### # Version:			#		v0.1.2
### # Description: 	#		Default .py file for the project.
###	#	
### ############################################################################################################
### ############################################################################################################
__plugin__	=	"The Anime Highway"
__authors__	=	"The Highway"
__credits__	=	"o9r1sh of plugin.video.gogoanime for Videoweed and Video44 source parsing. TheHighway(Myself) for AnimeGet plugin (simular site)"
plugin_id		=	"plugin.video.theanimehighway"
### ############################################################################################################
### ############################################################################################################
### ############################################################################################################
import xbmc,xbmcplugin,xbmcgui,xbmcaddon,xbmcvfs
try: import urlresolver
except: t=''
import urllib,urllib2,re,os,sys,string,StringIO,logging,random,array,time
#try: import requests ### <import addon="script.module.requests" version="1.1.0"/> ### 
#except: t=''				 ### See https://github.com/kennethreitz/requests ### 
import videolinks
from videolinks import vvVIDEOLINKS
from videolinks import *
#from videolinks2 import *
from teh_tools import *
try: import json
except ImportError: import simplejson as json
from t0mm0.common.net import Net as net
from t0mm0.common.addon import Addon
try: import StorageServer
except: import storageserverdummy as StorageServer
### ############################################################################################################
### ############################################################################################################
### ############################################################################################################
cache						=	StorageServer.StorageServer(plugin_id)
addon						=	Addon(plugin_id, sys.argv)
local						=	xbmcaddon.Addon(id=plugin_id)
__settings__		=	xbmcaddon.Addon(id=plugin_id)
__home__				=	__settings__.getAddonInfo('path')
addonPath				=	__settings__.getAddonInfo('path')
artPath					=	addonPath+'/art/'	#special://home/addons/plugin.video.theanimehighway/art
###	icon = xbmc.translatePath( os.path.join( __home__, 'icon.png' ) )
###	home = xbmc.translatePath(addon.getAddonInfo('path'))
if __settings__.getSetting("enable-debug") == "true":	debugging=True			#if (debugging==True): 
else: 																								debugging=False
if __settings__.getSetting("show-debug") == "true":		shoDebugging=True		#if (showDebugging==True): 
else: 																								shoDebugging=False
params=get_params()
MyMenu=class_MyMenu()
### ############################################################################################################
### ############################################################################################################
### ############################################################################################################
url=None; urlbac=None; name=None; name2=None; type2=None; favcmd=None; mode=None; scr=None; imgfan=None; show=None; category=None
try: category=urllib.unquote_plus(params["cat"])
except: pass
if category==None: category='Base'
try:
        url=urllib.unquote_plus(params["url"])
        urlbac=url
except: pass
try: scr=urllib.unquote_plus(params["scr"])
except: pass
try: imgfan=urllib.unquote_plus(params["fan"])
except: pass
try: favcmd=urllib.unquote_plus(params["fav"])
except: pass
try: name=urllib.unquote_plus(params["name"])
except: pass
try: name2=urllib.unquote_plus(params["nm"])
except: pass
try: show=urllib.unquote_plus(params["show"])
except: pass
try: type2=int(params["tp"])
except: pass
try: mode=int(params["mode"])
except: pass
### ############################################################################################################
### ############################################################################################################
### ############################################################################################################
ICON8 = os.path.join(artPath, 'icon_watchdub.png');ICON7 = os.path.join(artPath, 'icon_dubhappy.png');ICON6 = os.path.join(artPath, 'iconDAOn2.png');ICON5 = os.path.join(artPath, 'iconA44couk.png');ICON4 = os.path.join(artPath, 'icongd.png');ICON3 = os.path.join(artPath, 'iconAPlus.png');ICON2 = os.path.join(artPath, 'iconA44.png');ICON1 = os.path.join(artPath, 'iconAG.png');ICON0 = os.path.join(__home__, 'icon.png')
fanart8 = os.path.join(artPath, 'fanart_watchdub.jpg');fanart7 = os.path.join(artPath, 'fanart_dubhappy.jpg');fanart6 = os.path.join(artPath, 'fanartDAOn2.jpg');fanart5 = os.path.join(artPath, 'fanartA44couk.jpg');fanart4 = os.path.join(artPath, 'fanartgd.jpg');fanart3 = os.path.join(artPath, 'fanartAPlus.jpg');fanart2 = os.path.join(artPath, 'fanartA44.jpg');fanart1 = os.path.join(artPath, 'fanartAG.jpg');fanart0 = os.path.join(__home__, 'fanart.jpg')
if type2==8:			#site 8
	fanart = os.path.join(artPath, 'fanart_watchdub.jpg');ICON = os.path.join(artPath, 'icon_watchdub.png');mainSite='http://www.watchdub.com/'
elif type2==7:			#site 7
	fanart = os.path.join(artPath, 'fanart_dubhappy.jpg');ICON = os.path.join(artPath, 'icon_dubhappy.png');mainSite='http://www.dubhappy.eu/'
elif type2==6:			#site 6
	fanart = os.path.join(artPath, 'fanartDAOn2.jpg');ICON = os.path.join(artPath, 'iconDAOn2.png');mainSite='http://dubbedanimeon.com/'
elif type2==5:			#site 5
	fanart = os.path.join(artPath, 'fanartA44couk.jpg');ICON = os.path.join(artPath, 'iconA44couk.png');mainSite='http://www.anime44.co.uk/'
	if ('-anime' in url) and ('http://' not in url): url = mainSite + 'subanime/' + url
	if ('-anime' in url) and ('http://' not in scr) and (artPath not in scr): scr = mainSite + 'subanime/' + scr
	if ('-anime' in url) and ('http://' not in imgfan) and (artPath not in imgfan): imgfan = mainSite + 'subanime/' + imgfan
	#if ('-anime' not in url) and ('http://' not in url): url = mainSite + 'english-dubbed/' + url
	#if ('-anime' not in url) and ('http://' not in scr) and (artPath not in scr): scr = mainSite + 'english-dubbed/' + scr
	#if ('-anime' not in url) and ('http://' not in imgfan) and (artPath not in imgfan): imgfan = mainSite + 'english-dubbed/' + imgfan
	#if ('alpha-anime' in url): url.replace('alpha-anime','subanime')
	#if ('alpha-movies' in url): url.replace('alpha-movies','subanime')
	#if ('alpha-anime' in show): show.replace('alpha-anime','subanime')
	#if ('alpha-movies' in show): show.replace('alpha-movies','subanime')
elif type2==4:			#site 4
	fanart = os.path.join(artPath, 'fanartgd.jpg');ICON = os.path.join(artPath, 'icongd.png');mainSite='http://www.gooddrama.net/'
elif type2==3:		#site 3
	fanart = os.path.join(artPath, 'fanartplus.jpg');ICON = os.path.join(artPath, 'iconplus.png');mainSite='http://www.animeplus.tv/'
elif type2==2:		#site 2
	fanart = os.path.join(artPath, 'fanartA44.jpg');ICON = os.path.join(artPath, 'iconA44.png');mainSite='http://www.anime44.com/'
else:							#site 1
	fanart = os.path.join(artPath, 'fanartAG.jpg');ICON = os.path.join(artPath, 'iconAG.png');mainSite='http://www.animeget.com/'
### ############################################################################################################
### ############################################################################################################
### ############################################################################################################
SiteBits=['nosite','animeget.com','anime44.com','animeplus.tv','gooddrama.net','anime44.co.uk','dubbedanimeon.com','dubhappy.eu','watchdub.com']
SiteNames=['nosite','[COLOR blue][COLOR white]Anime[/COLOR]Get[/COLOR]','[COLOR red][COLOR white]Anime[/COLOR]44[/COLOR]','[COLOR darkblue][COLOR white]Anime[/COLOR]Plus[/COLOR]','[COLOR grey]Good[COLOR white]Drama[/COLOR][/COLOR]','[COLOR maroon][COLOR white]Anime[/COLOR]Zone[/COLOR]','[COLOR teal]Dubbed[COLOR white]Anime[/COLOR]On [/COLOR]','[COLOR cornflowerblue][COLOR white]dub[/COLOR]happy.eu[/COLOR]','[COLOR cornflowerblue]Watch[/COLOR][COLOR white]Dub[/COLOR]','','']
SitePrefixes=['nosite','','','','','subanime/','','','','','','','','','','','','']
SiteSufixes= ['nosite','','','','','.html','','','','','','','','','','','','','']
SiteSearchUrls= ['nosite','http://www.animeget.com/search','http://www.anime44.com/anime/search?search_submit=Go&key=','http://www.animeplus.tv/anime/search?search_submit=Go&key=','http://www.gooddrama.net/drama/search?stype=drama&search_submit=Go&key=','No Search Engine for VideoZone','http://dubbedanimeon.com/?s=','','','','','','','']
SiteSearchMethod= ['nosite','post','get','get','get','VideoZone','get','','','','','','','']
Sites=['animeget.com','anime44.com','animeplus.tv','gooddrama.net','anime44.co.uk','dubbedanimeon.com','dubhappy.eu','watchdub.com']
MyAlphabet=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
MyColors=['red','blue','darkblue','grey','maroon','teal','cornflowerblue','cornflowerblue','','','']
MyBrowser=['User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3']
### ############################################################################################################
if debugging==True:
	print 'Category from URL: ',category
	print "Mode: "+str(mode)
	print "URL: "+str(url)
	print "Name: "+str(name)
	print "Name2: "+str(name2)
	print "Type2: "+str(type2)
	print "FavCmd: "+str(favcmd)
	print "uScreenShot: "+str(scr)
	print "uFanart: "+str(imgfan)
	print "show: "+str(show)
	print "Category: "+str(category)
### ############################################################################################################
### ############################################################################################################
def menu0_MainMenu():#Site Selection Menu
	mm=[] ## Note:  Provides a list of menu items for later use.
	if (getsetbool_('esite-extras')==True): mm.append(make_item('                          [B][COLOR purple]--  The  [COLOR white]Anime[/COLOR]  [COLOR tan]Highway[/COLOR]  --[/COLOR][/B]'))
	if (getsetbool_('esite-extras')==True): mm.append(make_item('[COLOR grey] Please select a site:[/COLOR]'))
	if (getsetbool_('esite-1')==True): mm.append(make_item('[COLOR ' + MyColors[1] + '][COLOR white]Anime[/COLOR]Get[/COLOR]',True,1,1,SiteBits[1],ICON1,fanart1,'ag'))
	if (getsetbool_('esite-2')==True): mm.append(make_item('[COLOR ' + MyColors[0] + '][COLOR white]Anime[/COLOR]44[/COLOR]',True,1,2,SiteBits[2],ICON2,fanart2,'a44.com'))
	if (getsetbool_('esite-3')==True): mm.append(make_item('[COLOR ' + MyColors[2] + '][COLOR white]Anime[/COLOR]Plus[/COLOR]',True,1,3,SiteBits[3],ICON3,fanart3,'aplus'))
	if (getsetbool_('esite-5')==True): mm.append(make_item('[COLOR ' + MyColors[4] + '][COLOR white]Anime[/COLOR]Zone[/COLOR]',True,1,5,SiteBits[5],ICON5,fanart5,'az'))
	if (getsetbool_('esite-6')==True): mm.append(make_item('[COLOR ' + MyColors[5] + ']Dubbed[COLOR white]Anime[/COLOR]On[/COLOR]',True,1,6,SiteBits[6],ICON6,fanart6,'dao'))
	if (getsetbool_('esite-7')==True): mm.append(make_item('[COLOR ' + MyColors[6] + '][COLOR white]Dub[/COLOR]Happy.eu[/COLOR]',True,1,7,SiteBits[7],ICON7,fanart7,'dh'))
	if (getsetbool_('esite-8')==True): mm.append(make_item('[COLOR ' + MyColors[7] + ']Watch[COLOR white]Dub[/COLOR][/COLOR]',True,1,8,SiteBits[8],ICON8,fanart8,'wd'))
	if (getsetbool_('esite-4')==True): mm.append(make_item('[COLOR ' + MyColors[3] + ']Good[COLOR white]Drama[/COLOR][/COLOR]',True,1,4,SiteBits[4],ICON4,fanart4,'gd'))
	#
	#
	#
	#
	mm.append(make_item('[COLOR tan]F[COLOR maroon]a[/COLOR]vorites[/COLOR]',True,888,1,'Favorites',ICON0,fanart0,'favs'))
	if (getsetbool_('esite-extras2')==False):
		mm.append(make_item('[COLOR tan]E[COLOR maroon]x[/COLOR]tras[/COLOR]',True,101,0,'Extras',ICON0,fanart0,''))
	if (getsetbool_('esite-extras2')==True):
		mm.append(make_item_cmd('showsettingwindow','[COLOR tan]Settings[/COLOR]',False,0,0,'Show Setting Window',ICON0,fanart0))
		mm.append(make_item_cmd('showtextwindow','[COLOR white]Latest Online[/COLOR] [COLOR tan]News[/COLOR]  [COLOR grey][/COLOR]',False,0,0,'Latest Online News',ICON0,fanart0,'https://raw.github.com/HIGHWAY99/plugin.video.theanimehighway/master/news.txt',"[COLOR cornflowerblue]Latest News:[/COLOR]  %s" % (__plugin__)))
		mm.append(make_item_cmd('showtextwindow','[COLOR white]Latest Online[/COLOR] [COLOR tan]Change Log[/COLOR]  [COLOR grey][/COLOR]',False,0,0,'Latest Change Log',ICON0,fanart0,'https://raw.github.com/HIGHWAY99/plugin.video.theanimehighway/master/changelog.txt',"[COLOR cornflowerblue]Latest Change Log:[/COLOR]  %s" % (__plugin__)))
		mm.append(make_item_cmd('showtextwindow2','[COLOR white]Local[/COLOR] [COLOR tan]Change Log[/COLOR]  [COLOR grey][/COLOR]',False,0,0,'Local Change Log',ICON0,fanart0,'changelog.txt',"[COLOR cornflowerblue]Local Change Log:[/COLOR]  %s" % (__plugin__)))
		mm.append(make_item('[COLOR maroon] Visit with [COLOR tan]Highway[/COLOR] and others @ [COLOR white]#XBMCHUB[/COLOR] on [COLOR white]irc.freenode.net[/COLOR]:6667 [/COLOR]'))
		mm.append(make_item('[COLOR tan]Search[/COLOR] [COLOR white]AirDates[/COLOR]',False,1800,0,'Search', os.path.join(artPath,'tvdb_logo2.png'),'http://www.thetvdb.com/images/header.jpg','search'))
	set_view('none',int(getset('viewmode-sites')))
### ############################################################################################################
def menu101_Extras():#Extras Menu
	mm=[] ## Note:  Provides a list of menu items for later use.
	if (getsetbool_('esite-extras')==True): mm.append(make_item('                          [B][COLOR purple]--  The  [COLOR white]Anime[/COLOR]  [COLOR tan]Highway[/COLOR]  --[/COLOR][/B]'))
	if (getsetbool_('esite-extras')==True): mm.append(make_item('[COLOR grey] List of Extras:[/COLOR]'))
	mm.append(make_item('[COLOR tan]Search[/COLOR] [COLOR white]AirDates[/COLOR]',False,1800,0,'Search', os.path.join(artPath,'tvdb_logo2.png'),'http://www.thetvdb.com/images/header.jpg','search'))
	mm.append(make_item('[COLOR tan]F[COLOR maroon]a[/COLOR]vorites[/COLOR]',True,888,1,'Favorites',ICON0,fanart0,'favs'))
	mm.append(make_item_cmd('showtextwindow','[COLOR white]Latest Online[/COLOR] [COLOR tan]News[/COLOR]  [COLOR grey][/COLOR]',False,0,0,'Latest Online News',ICON0,fanart0,'https://raw.github.com/HIGHWAY99/plugin.video.theanimehighway/master/news.txt',"[COLOR cornflowerblue]Latest News:[/COLOR]  %s" % (__plugin__)))
	mm.append(make_item_cmd('showtextwindow','[COLOR white]Latest Online[/COLOR] [COLOR tan]Change Log[/COLOR]  [COLOR grey][/COLOR]',False,0,0,'Latest Change Log',ICON0,fanart0,'https://raw.github.com/HIGHWAY99/plugin.video.theanimehighway/master/changelog.txt',"[COLOR cornflowerblue]Latest Change Log:[/COLOR]  %s" % (__plugin__)))
	mm.append(make_item_cmd('showtextwindow2','[COLOR white]Local[/COLOR] [COLOR tan]Change Log[/COLOR]  [COLOR grey][/COLOR]',False,0,0,'Local Change Log',ICON0,fanart0,'changelog.txt',"[COLOR cornflowerblue]Local Change Log:[/COLOR]  %s" % (__plugin__)))
	mm.append(make_item_cmd('showsettingwindow','[COLOR tan]Settings[/COLOR]',False,0,0,'Show Setting Window',ICON0,fanart0))
	mm.append(make_item('[COLOR maroon] Visit with [COLOR tan]Highway[/COLOR] and others @ [COLOR white]#XBMCHUB[/COLOR] on [COLOR white]irc.freenode.net[/COLOR]:6667 [/COLOR]'))
	#
	set_view('none',int(getset('viewmode-sites')))
### ############################################################################################################
def menu1_BrowseMethod():#Main Menu (for each site)
        if type2==4:#gooddrama
        	addFolder('[COLOR ' + MyColors[0] + ']Drama Movies[/COLOR]','Movies','drama-movies',type2,3,'movies.png','Drama Movies')
        	addFolder('[COLOR ' + MyColors[1] + ']Drama Series[/COLOR]','List','drama-shows',type2,2,'full.png','Drama Series')
        elif (type2==1) or (type2==3) or (type2==5):#animeget & animeplus & animezone
        	addFolder('[COLOR ' + MyColors[0] + ']Anime Movies[/COLOR]','Movies','anime-movies',type2,3,'movies.png','Anime Movies')
        	addFolder('[COLOR ' + MyColors[1] + ']Anime Series[/COLOR]','List','anime-shows',type2,2,'full.png','Anime Series')
        elif (type2==6):
        	addFolder('[COLOR ' + MyColors[1] + ']Genre[/COLOR]','List',mainSite+'genres/',type2,252,'Glossy_Black\\genres.png','Genre')
        	#
        	#
        	# Random Show, Top Anime, Anime Series
        	addDir('[COLOR tan]Search[/COLOR]','',mainSite + 'Search',type2,400,artPath + 'search-icon.png',fanart,'Search')
        elif (type2==7):#dubhappy
        	addFolder('[COLOR ' + MyColors[1] + ']Genre[/COLOR]','List','?SearchByGenre=True',type2,211,'Glossy_Black\\genres.png','Genre')
        	addFolder('[COLOR ' + MyColors[1] + ']Anime List[/COLOR]','List','/anime-list/',type2,258	,'full.png','Anime List')
        	addFolder('[COLOR ' + MyColors[1] + ']AnimeStatic.[org|com] - Anime Movies[/COLOR]','List','/anime-movies/',type2,358	,'movies.png','Anime Movies')
        	#
        elif (type2==8):#watchdub
        	addFolder('[COLOR ' + MyColors[1] + ']Genre[/COLOR]','List','multiple-anime-genres-search/',type2,252,'Glossy_Black\\genres.png','Genre')
        	addFolder('[COLOR ' + MyColors[1] + ']Recent Anime[/COLOR]','List','/',type2,258,'gogoanime\\newseries.png','Recent Anime')
        	addFolder('[COLOR ' + MyColors[1] + ']WatchAnimeMovie.com - Anime Movies[/COLOR]'		,'List','http://video.watchanimemovie.com/animelist.php?site=movie'		,type2,358,'movies.png','WatchAnimeMovie.com')
        	addFolder('[COLOR ' + MyColors[1] + ']WatchAnimeMovie.com - Anime OVA[/COLOR]'			,'List','http://video.watchanimemovie.com/animelist.php?site=ova'			,type2,358,'movies.png','WatchAnimeMovie.com')
        	addFolder('[COLOR ' + MyColors[1] + ']WatchAnimeMovie.com - Anime Specials[/COLOR]'	,'List','http://video.watchanimemovie.com/animelist.php?site=special'	,type2,358,'movies.png','WatchAnimeMovie.com')
        	addFolder('[COLOR ' + MyColors[1] + ']WatchAnimeMovie.com - Abridged Series[/COLOR]','List','http://video.watchanimemovie.com/animelist.php?site=abridged',type2,358,'movies.png','WatchAnimeMovie.com')
        	addFolder('[COLOR ' + MyColors[1] + ']WatchAnimeMovie.com - Cartoon Movies[/COLOR]'	,'List','http://video.watchanimemovie.com/animelist.php?site=cartoon'	,type2,358,'movies.png','WatchAnimeMovie.com')
        	addFolder('[COLOR ' + MyColors[1] + ']WatchAnimeMovie.com - Animated Films[/COLOR]'	,'List','http://video.watchanimemovie.com/animelist.php?site=animated',type2,358,'movies.png','WatchAnimeMovie.com')
        	addFolder('[COLOR ' + MyColors[1] + ']WatchAnimeMovie.com - Cutscene Games[/COLOR]'	,'List','http://video.watchanimemovie.com/animelist.php?site=games'		,type2,358,'movies.png','WatchAnimeMovie.com')
        	#addFolder('[COLOR ' + MyColors[1] + ']Genre[/COLOR]','List','anime-genres'+SiteSufixes[type2],type2,211,'Glossy_Black\\genres.png','Genre')
        	#
        else:
        	addFolder('[COLOR ' + MyColors[0] + ']Anime Movies[/COLOR]','Movies','category/anime-movies',type2,601,'movies.png','Anime Movies')
        	addFolder('[COLOR ' + MyColors[1] + ']Anime Series[/COLOR]','List','anime-list',type2,2,'full.png','Anime Series')
        if (type2==1) or (type2==2):#animeget & anime44
        	addFolder('[COLOR ' + MyColors[1] + ']Ongoing Series[/COLOR]','List','ongoing-anime',type2,6,'plus.png','Ongoing Anime')
        #addDir('Latest Episodes','List',mainSite + 'anime-updates',0,7,artPath + 'full.png',fanart)
        if type2==1:
        	addDir('[COLOR ' + MyColors[1] + ']New Series[/COLOR]','List',mainSite + 'new-anime',type2,6,artPath + 'gogoanime\\newseries.png',fanart,'New Anime Series')
        	addDir('[COLOR ' + MyColors[2] + ']Suprise Me[/COLOR]','List',mainSite + 'surprise',type2,4,artPath + 'surpriseme1.jpg',fanart,'Surprise Me')
        if (type2==5):
        	#addDir('[COLOR ' + MyColors[2] + ']Dubbed Anime List[/COLOR]','List','http://animeinfo.co.uk/index.html',type2,4,artPath + 'full.png',fanart)
        	#addFolder('[COLOR ' + MyColors[2] + ']Dubbed Anime List[/COLOR]','Dubbed Anime','http://animeinfo.co.uk/index.html',type2,601,'full.png')
        	addFolder('[COLOR lime]Dubbed Anime[/COLOR]','Dubbed Anime','http://animeinfo.co.uk/index.html',type2,250,'full.png','Dubbed Anime')
        #if type2==2:
        #	#addFolder('[COLOR tan]Search[/COLOR]','','',type2,400,'search-icon.png')
        if (type2==1) or (type2==2) or (type2==3) or (type2==4):
        	addDir('[COLOR tan]Search[/COLOR]','',mainSite + 'Search',type2,400,artPath + 'search-icon.png',fanart,'Search')
        #addDir('Search','List',mainSite + 'new-anime',0,8,artPath + 'full.png',fanart)
        set_view('none',int(getset('viewmode-default')))
### ############################################################################################################
def menu2():#series
        if type2==4:#gooddrama
        	addFolder('[COLOR ' + MyColors[1] + ']Index[/COLOR]','List','drama-shows',type2,201,'full.png')
        	addFolder('[COLOR ' + MyColors[1] + ']Genre[/COLOR]','List','drama-show-genres',type2,211,'Glossy_Black\\genres.png')
        	addFolder('[COLOR ' + MyColors[1] + ']Popular[/COLOR]','List','popular-shows',type2,6,'BLANK.png')
        	addFolder('[COLOR ' + MyColors[1] + ']New[/COLOR]','List','new-shows',type2,6,'BLANK.png')
        	addFolder('[COLOR ' + MyColors[1] + ']Recent[/COLOR]','List','recent-shows',type2,6,'BLANK.png','Recent')
        	addFolder('[COLOR ' + MyColors[1] + ']Ongoing[/COLOR]','List','ongoing-shows',type2,6,'plus.png')
        	addFolder('[COLOR ' + MyColors[1] + ']Completed[/COLOR]','List','completed-shows',type2,6,'BLANK.png')
        elif (type2==1) or (type2==3) or (type2==5):#animeget & animeplus & animezone
        	addFolder('[COLOR ' + MyColors[1] + ']Index[/COLOR]','List',SitePrefixes[type2]+'anime-shows'+SiteSufixes[type2],type2,201,'full.png','Index')
        	addFolder('[COLOR ' + MyColors[1] + ']Genre[/COLOR]','List',SitePrefixes[type2]+'anime-genres'+SiteSufixes[type2],type2,211,'Glossy_Black\\genres.png','Genre')
        	addFolder('[COLOR ' + MyColors[1] + ']Popular[/COLOR]','List',SitePrefixes[type2]+'popular-shows'+SiteSufixes[type2],type2,6,'BLANK.png','Popular')
        	addFolder('[COLOR ' + MyColors[1] + ']New[/COLOR]','List',SitePrefixes[type2]+'new-shows'+SiteSufixes[type2],type2,6,'BLANK.png','New')
        	addFolder('[COLOR ' + MyColors[1] + ']Recent[/COLOR]','List',SitePrefixes[type2]+'recent-shows'+SiteSufixes[type2],type2,6,'BLANK.png','Recent')
        	addFolder('[COLOR ' + MyColors[1] + ']Ongoing[/COLOR]','List',SitePrefixes[type2]+'ongoing-shows'+SiteSufixes[type2],type2,6,'plus.png','Ongoing')
        	addFolder('[COLOR ' + MyColors[1] + ']Completed[/COLOR]','List',SitePrefixes[type2]+'completed-shows'+SiteSufixes[type2],type2,6,'BLANK.png','Completed')
        elif type2==2:#anime44
        	addFolder('[COLOR ' + MyColors[1] + ']Index[/COLOR]','List','anime-list',type2,201,'full.png','Index')
        	addFolder('[COLOR ' + MyColors[1] + ']Genre[/COLOR]','List','anime-genres',type2,211,'Glossy_Black\\genres.png','Genre')
        	addFolder('[COLOR ' + MyColors[1] + ']Popular[/COLOR]','List','popular-anime',type2,6,'BLANK.png','Popular')
        	addFolder('[COLOR ' + MyColors[1] + ']New[/COLOR]','List','new-anime',type2,6,'BLANK.png','New')
        	addFolder('[COLOR ' + MyColors[1] + ']Recent[/COLOR]','List','recent-anime',type2,6,'BLANK.png','Recent')
        	addFolder('[COLOR ' + MyColors[1] + ']Ongoing[/COLOR]','List','ongoing-anime',type2,6,'plus.png','Ongoing')
        	addFolder('[COLOR ' + MyColors[1] + ']Completed[/COLOR]','List','completed-anime',type2,6,'BLANK.png','Completed')
        set_view('none',int(getset('viewmode-default')))
def menu3():#movies
        if (type2==1) or (type2==5):
        	addFolder('Index','List',SitePrefixes[type2]+'anime-movies'+SiteSufixes[type2],type2,301,'movies.png')
        	addFolder('Genre','List',SitePrefixes[type2]+'anime-movie-genres'+SiteSufixes[type2],type2,311,'Glossy_Black\\genres.png')
        	addFolder('Popular','List',SitePrefixes[type2]+'popular-movies'+SiteSufixes[type2],type2,6,'BLANK.png')
        	addFolder('New','List',SitePrefixes[type2]+'new-movies'+SiteSufixes[type2],type2,6,'BLANK.png')
        	addFolder('Recent','List',SitePrefixes[type2]+'recent-movies'+SiteSufixes[type2],type2,6,'BLANK.png')
        else:
        	addFolder('Index','List','category/anime-movies',type2,301,'movies.png')
        	addFolder('Genre','List','anime-movie-genres',type2,311,'Glossy_Black\\genres.png')
        	addFolder('Popular','List','popular-movies',type2,6,'BLANK.png')
        	addFolder('New','List','new-movies',type2,6,'BLANK.png')
        	addFolder('Recent','List','recent-movies',type2,6,'BLANK.png')
        set_view('none',int(getset('viewmode-default')))
def menu250():#dubbed-anime
	if (type2==5):
		addFolder('Index  - (05 per page)','List','index.html?max-results=15&sort=1',type2,253,'full.png')
		addFolder('Genre - (15 per page) * Suggested','List','indexef22.html?max-results=15&cat-id=5',type2,252,'Glossy_Black\\genres.png')
		#addFolder('Popular','List',SitePrefixes[type2]+'popular-movies'+SiteSufixes[type2],type2,6,'BLANK.png')
		#addFolder('New','List',SitePrefixes[type2]+'new-movies'+SiteSufixes[type2],type2,6,'BLANK.png')
		#addFolder('Recent','List',SitePrefixes[type2]+'recent-movies'+SiteSufixes[type2],type2,6,'BLANK.png')
	set_view('none',int(getset('viewmode-default')))
### ############################################################################################################
def menu252_genre_list():#dubbed-anime#genres
	if (type2==8):#watchdub
		#http://www.watchdub.com/?max-results=100&cat-id=11
		nextNo=256 #253
		pgSort='&sort=2' ## 1=scores, 2=rating, 3=comments ## ?? &animesort= ??   0=Date, 4=Alphabetical
		pgMaxResults='50' ## Site allows this to be adjustable.
		## &animetype=2 &animetype=1 ## 1=List, 2=Details with description and image.
		### http://www.watchdub.com/anime-genres-search-results/?CHECKBOX[]=9&CHECKBOX[]=6&CHECKBOX[]=11&animesort=4&animetype=2&Submit=Submit
		addDirD('- All Anime List -',	name,mainSite+'?max-results='+pgMaxResults+'&cat-id=5' +pgSort,type2,nextNo,ICON,fanart,True)
		addDirD('Action',							name,mainSite+'?max-results='+pgMaxResults+'&cat-id=9' +pgSort,type2,nextNo,ICON,fanart,True)
		addDirD('Adventure',					name,mainSite+'?max-results='+pgMaxResults+'&cat-id=12'+pgSort,type2,nextNo,ICON,fanart,True)
		addDirD('Comedy',							name,mainSite+'?max-results='+pgMaxResults+'&cat-id=13'+pgSort,type2,nextNo,ICON,fanart,True)
		addDirD('Drama',							name,mainSite+'?max-results='+pgMaxResults+'&cat-id=6' +pgSort,type2,nextNo,ICON,fanart,True)
		addDirD('Fantasy',						name,mainSite+'?max-results='+pgMaxResults+'&cat-id=11'+pgSort,type2,nextNo,ICON,fanart,True)
		addDirD('Horror',							name,mainSite+'?max-results='+pgMaxResults+'&cat-id=8' +pgSort,type2,nextNo,ICON,fanart,True)
		addDirD('Magic',							name,mainSite+'?max-results='+pgMaxResults+'&cat-id=17'+pgSort,type2,nextNo,ICON,fanart,True)
		addDirD('Mystery',						name,mainSite+'?max-results='+pgMaxResults+'&cat-id=14'+pgSort,type2,nextNo,ICON,fanart,True)
		addDirD('Psychological',			name,mainSite+'?max-results='+pgMaxResults+'&cat-id=3' +pgSort,type2,nextNo,ICON,fanart,True)
		addDirD('Romance',						name,mainSite+'?max-results='+pgMaxResults+'&cat-id=4' +pgSort,type2,nextNo,ICON,fanart,True)
		addDirD('Science Fiction',		name,mainSite+'?max-results='+pgMaxResults+'&cat-id=7' +pgSort,type2,nextNo,ICON,fanart,True)
		addDirD('Slice of Life',			name,mainSite+'?max-results='+pgMaxResults+'&cat-id=15'+pgSort,type2,nextNo,ICON,fanart,True)
		addDirD('Supernatural',				name,mainSite+'?max-results='+pgMaxResults+'&cat-id=10'+pgSort,type2,nextNo,ICON,fanart,True)
		addDirD('Thriller',						name,mainSite+'?max-results='+pgMaxResults+'&cat-id=16'+pgSort,type2,nextNo,ICON,fanart,True)
		addDirD('Tournament',					name,mainSite+'?max-results='+pgMaxResults+'&cat-id=18'+pgSort,type2,nextNo,ICON,fanart,True)
		addDirD('Yaoi',								name,mainSite+'?max-results='+pgMaxResults+'&cat-id=19'+pgSort,type2,nextNo,ICON,fanart,True)
		addDirD('Yuri',								name,mainSite+'?max-results='+pgMaxResults+'&cat-id=20'+pgSort,type2,nextNo,ICON,fanart,True)
		#addDirD('',	name,mainSite+'?max-results='+pgMaxResults+'&cat-id='+pgSort,type2,nextNo,ICON,fanart,True)
		set_view('none',int(getset('viewmode-default')))
	#
	if (type2==5):
		addDirD('- All Anime List -',	name,mainSite+'indexef22.html?max-results=15&sort=1&cat-id=5',type2,253,ICON,fanart,True)
		addDirD('action',							name,mainSite+'index2373.html?max-results=15&sort=1&cat-id=9',type2,253,ICON,fanart,True)
		addDirD('adventure',					name,mainSite+'indexcaef.html?max-results=15&sort=1&cat-id=12',type2,253,ICON,fanart,True)
		addDirD('comedy',							name,mainSite+'indexdad4.html?max-results=15&sort=1&cat-id=13',type2,253,ICON,fanart,True)
		addDirD('drama',							name,mainSite+'index9d40.html?max-results=15&sort=1&cat-id=6',type2,253,ICON,fanart,True)
		addDirD('fantasy',						name,mainSite+'index63e1.html?max-results=15&sort=1&cat-id=11',type2,253,ICON,fanart,True)
		addDirD('horror',							name,mainSite+'index918a.html?max-results=15&sort=1&cat-id=8',type2,253,ICON,fanart,True)
		addDirD('magic',							name,mainSite+'indexe1d7.html?max-results=15&sort=1&cat-id=17',type2,253,ICON,fanart,True)
		addDirD('mystery',						name,mainSite+'index5211.html?max-results=15&sort=1&cat-id=14',type2,253,ICON,fanart,True)
		addDirD('psychological',			name,mainSite+'index1919.html?max-results=15&sort=1&cat-id=3',type2,253,ICON,fanart,True)
		addDirD('romance',						name,mainSite+'index7bb9.html?max-results=15&sort=1&cat-id=4',type2,253,ICON,fanart,True)
		addDirD('science fiction',		name,mainSite+'indexb3bc.html?max-results=15&sort=1&cat-id=7',type2,253,ICON,fanart,True)
		addDirD('slice of life',			name,mainSite+'index7e70.html?max-results=15&sort=1&cat-id=15',type2,253,ICON,fanart,True)
		addDirD('supernatural',				name,mainSite+'index5e21.html?max-results=15&sort=1&cat-id=10',type2,253,ICON,fanart,True)
		addDirD('thriller',						name,mainSite+'indexec00.html?max-results=15&sort=1&cat-id=16',type2,253,ICON,fanart,True)
		addDirD('tournament',					name,mainSite+'index09d2.html?max-results=15&sort=1&cat-id=18',type2,253,ICON,fanart,True)
		addDirD('yaoi',								name,mainSite+'indexe2f0.html?max-results=15&sort=1&cat-id=19',type2,253,ICON,fanart,True)
		addDirD('yuri',								name,mainSite+'index16d2.html?max-results=15&sort=1&cat-id=20',type2,253,ICON,fanart,True)
	if (type2==6):
		#http://dubbedanimeon.com/genres/?genre=School
		nextMode=256
		genreUrl=mainSite+'genres/?genre='
		addDirD('Action',							name,genreUrl+'Action',type2,nextMode,ICON,fanart,True)
		addDirD('Adventure',					name,genreUrl+'Adventure',type2,nextMode,ICON,fanart,True)
		addDirD('Bishounen',					name,genreUrl+'Bishounen',type2,nextMode,ICON,fanart,True)
		addDirD('Comedy',							name,genreUrl+'Comedy',type2,nextMode,ICON,fanart,True)
		addDirD('Demons',							name,genreUrl+'Demons',type2,nextMode,ICON,fanart,True)
		addDirD('Drama',							name,genreUrl+'Drama',type2,nextMode,ICON,fanart,True)
		addDirD('Ecchi',							name,genreUrl+'Ecchi',type2,nextMode,ICON,fanart,True)
		addDirD('Fantasy',						name,genreUrl+'Fantasy',type2,nextMode,ICON,fanart,True)
		addDirD('Harem',							name,genreUrl+'Harem',type2,nextMode,ICON,fanart,True)
		addDirD('Horror',							name,genreUrl+'Horror',type2,nextMode,ICON,fanart,True)
		addDirD('Josei',							name,genreUrl+'Josei',type2,nextMode,ICON,fanart,True)
		addDirD('Magic',							name,genreUrl+'Magic',type2,nextMode,ICON,fanart,True)
		addDirD('Martial Arts',				name,genreUrl+'Martial Arts',type2,nextMode,ICON,fanart,True)
		addDirD('Mecha',							name,genreUrl+'Mecha',type2,nextMode,ICON,fanart,True)
		addDirD('Music',							name,genreUrl+'Music',type2,nextMode,ICON,fanart,True)
		addDirD('Mystery',						name,genreUrl+'Mystery',type2,nextMode,ICON,fanart,True)
		addDirD('Ninja',							name,genreUrl+'Ninja',type2,nextMode,ICON,fanart,True)
		addDirD('Parody',							name,genreUrl+'Parody',type2,nextMode,ICON,fanart,True)
		addDirD('Psychological',			name,genreUrl+'Psychological',type2,nextMode,ICON,fanart,True)
		addDirD('Reverse Harem',			name,genreUrl+'Reverse Harem',type2,nextMode,ICON,fanart,True)
		addDirD('Romance',						name,genreUrl+'Romance',type2,nextMode,ICON,fanart,True)
		addDirD('Samurai',						name,genreUrl+'Samurai',type2,nextMode,ICON,fanart,True)
		addDirD('School',							name,genreUrl+'School',type2,nextMode,ICON,fanart,True)
		addDirD('Sci-Fi',							name,genreUrl+'Sci-Fi',type2,nextMode,ICON,fanart,True)
		addDirD('Seinen',							name,genreUrl+'Seinen',type2,nextMode,ICON,fanart,True)
		addDirD('Shoujo',							name,genreUrl+'Shoujo',type2,nextMode,ICON,fanart,True)
		addDirD('Shoujo Ai',					name,genreUrl+'Shoujo Ai',type2,nextMode,ICON,fanart,True)
		addDirD('Shounen',						name,genreUrl+'Shounen',type2,nextMode,ICON,fanart,True)
		addDirD('Shounen Ai',					name,genreUrl+'Shounen Ai',type2,nextMode,ICON,fanart,True)
		addDirD('Slapstick',					name,genreUrl+'Slapstick',type2,nextMode,ICON,fanart,True)
		addDirD('Slice of Life',			name,genreUrl+'Slice of Life',type2,nextMode,ICON,fanart,True)
		addDirD('Sports',							name,genreUrl+'Sports',type2,nextMode,ICON,fanart,True)
		addDirD('Supernatural',				name,genreUrl+'Supernatural',type2,nextMode,ICON,fanart,True)
		addDirD('Thriller',						name,genreUrl+'Thriller',type2,nextMode,ICON,fanart,True)
		addDirD('Tragedy',						name,genreUrl+'Tragedy',type2,nextMode,ICON,fanart,True)
		addDirD('Vampire',						name,genreUrl+'Vampire',type2,nextMode,ICON,fanart,True)
		#
		#
		#
	set_view('none',int(getset('viewmode-default')))
### ############################################################################################################
def menu358_list__Name_and_Url__(url): ### For Simply -Name & Url- Lists
	viewtyp='movies'
	link=getURL(url)
	if (type2==7): ### Full Movie List - Alphabetical
		dat_shows=(link.split('<h4 class="post-title"><a href="http://www.dubhappy.eu/anime-movies/" title="Anime Movies">Anime Movies</a></h4><div class="post-head">')[1]).split('<div id="sidebar1">')[0]
		#dat_show=re.compile('<li><a href="http://www.dubhappy.eu/(.+?)/">(.+?)</a></li>', re.MULTILINE | re.IGNORECASE | re.DOTALL).findall('__'+dat_shows+'__')
		dat_show=re.compile('<li><a href="(http://.+?)">(.+?)</a></li>', re.MULTILINE | re.IGNORECASE | re.DOTALL).findall('__'+dat_shows+'__')
		for item_folder, item_name in dat_show:
			#show_url=item_page='http://www.dubhappy.eu/'+item_folder+'/'; show_title=ParseDescription(item_name)
			show_url=item_page=''+item_folder+''; show_title=ParseDescription(item_name)
			show_img=ICON
			#
			#
			vid_poster=show_img; vid_fanart=fanart
			Labels={ 'Title':show_title,'Plot':'','Year':'','Status':'','Rating':'', 'ShowID':'','Votes':'','Type':'', 'Fanart':vid_fanart, 'Poster':vid_poster, 'Banner':'', 'Language':'', 'Network':'', 'Genre':'' } 
			#Labels={ 'Title':show_title,'Plot':vid_descr,'Year':vid_released,'Status':vid_status,'Rating':vid_rating, 'ShowID':vid_id,'Votes':vid_votes,'Type':vid_type, 'Fanart':vid_fanart, 'Poster':vid_poster, 'Banner':vid_banner, 'Language':vid_language, 'Network':vid_network, 'Genre':vid_genres } 
			addDirD(show_title,show_title,show_url,type2,501,vid_poster,vid_fanart,True,'',Labels)
	if (type2==8): ### Full Movie List(s) - They Actually from WatchAnimeMovie.com 's listings.
		dat_shows=(link.split('<ul class=')[1]).split('</ul>')[0]
		dat_show=re.compile('<li><a target="_blank" href="http://www.watchanimemovie.com/sub-dub/(.+?)">(.+?)</a> </li>', re.MULTILINE | re.IGNORECASE | re.DOTALL).findall('__'+dat_shows+'__') ### hackthe-movie-sekai-no-mukou-ni.html
		#(.+?)
		for item_folder, item_name in dat_show:
			show_url=item_page='http://www.watchanimemovie.com/sub-dub/'+item_folder+''; show_title=ParseDescription(item_name)
			show_img=ICON
			#
			#
			vid_poster=show_img; vid_fanart=fanart
			Labels={ 'Title':show_title,'Plot':'','Year':'','Status':'','Rating':'', 'ShowID':'','Votes':'','Type':'', 'Fanart':vid_fanart, 'Poster':vid_poster, 'Banner':'', 'Language':'', 'Network':'', 'Genre':'' } 
			#Labels={ 'Title':show_title,'Plot':vid_descr,'Year':vid_released,'Status':vid_status,'Rating':vid_rating, 'ShowID':vid_id,'Votes':vid_votes,'Type':vid_type, 'Fanart':vid_fanart, 'Poster':vid_poster, 'Banner':vid_banner, 'Language':vid_language, 'Network':vid_network, 'Genre':vid_genres } 
			addDirD(show_title,show_title,show_url,type2,501,vid_poster,vid_fanart,True,'',Labels)

def menu258_list__WatchDub_com__Series_RecentAnime(url): ### For Simply -Name & Url- Lists
	viewtyp='tvshows'
	link=getURL(url)
	if (type2==7): ### Full Anime List - Alphabetical
		dat_shows=(link.split('<h4 class="post-title"><a href="http://www.dubhappy.eu/anime-list/" title="Dubbed Anime List">Dubbed Anime List</a></h4><div class="post-head">')[1]).split('<div id="sidebar1">')[0]
		dat_show=re.compile('<li><a href="http://www.dubhappy.eu/anime/(.+?)/">(.+?)</a></li>', re.MULTILINE | re.IGNORECASE | re.DOTALL).findall('__'+dat_shows+'__')
		for item_folder, item_name in dat_show:
			show_url=item_page='http://www.dubhappy.eu/anime/'+item_folder+'/'; show_title=ParseDescription(item_name)
			#show_html=getURL(show_url)
			#show_img=checkImgUrl('http://dubhappy.eu/images/'+item_folder+'.jpg')
			show_img='http://dubhappy.eu/images/'+item_folder+'.jpg'
			if (show_img==''): show_img=ICON
			#
			#
			vid_poster=show_img; vid_fanart=fanart
			Labels={ 'Title':show_title,'Plot':'','Year':'','Status':'','Rating':'', 'ShowID':'','Votes':'','Type':'', 'Fanart':vid_fanart, 'Poster':vid_poster, 'Banner':'', 'Language':'', 'Network':'', 'Genre':'' } 
			#Labels={ 'Title':show_title,'Plot':vid_descr,'Year':vid_released,'Status':vid_status,'Rating':vid_rating, 'ShowID':vid_id,'Votes':vid_votes,'Type':vid_type, 'Fanart':vid_fanart, 'Poster':vid_poster, 'Banner':vid_banner, 'Language':vid_language, 'Network':vid_network, 'Genre':vid_genres } 
			addDirD(show_title,show_title,show_url,type2,257,vid_poster,vid_fanart,True,'',Labels)

	if (type2==8): ### Recent Anime 
		dat_shows=(link.split('<h2 class="widgettitle">Recent Anime</h2><ul class="">')[1]).split('</ul>')[0]
		dat_show=re.compile('<li><a href="http://www.watchdub.com/english-dubbed/(.+?)/">(.+?)</a> </li>', re.MULTILINE | re.IGNORECASE | re.DOTALL).findall('__'+dat_shows+'__')
		for item_folder, item_name in dat_show:
			show_url=item_page='http://www.watchdub.com/english-dubbed/'+item_folder+'/'; show_title=ParseDescription(item_name)
			show_html=getURL(show_url)
			if (len(show_html) > 0) and (show_html is not None) and (show_html is not 'none'):
				#try: show_img=(re.compile('<img class="photo" alt=".+?" src="(.+?)" width="\d+" height="\d+" />', re.MULTILINE | re.IGNORECASE | re.DOTALL).findall(show_html)[0]).strip()
				try: show_img=(re.compile('<div align="center"><img.+?src="(.+?)".+?/></div>', re.MULTILINE | re.IGNORECASE | re.DOTALL).findall(show_html)[0]).strip()
				except: show_img=ICON
				try: show_plot=(re.compile('Plot Summary: (.+?)</p>', re.MULTILINE | re.IGNORECASE | re.DOTALL).findall(show_html)[0]).strip()
				except: show_plot=''
			else:
				show_img=ICON
				show_plot=''
			if (metaArt_DoCheck(show_title)==True):
				if (debugging==True): print show_title + ' found in cached metaArt Data.'
				thetvdb_data=metaArt_getCache(show_title)
				#thetvdb_data=['','','','','','','','','','','','','','','','','']
			else:
				thetvdb_data=metaArt_get(show_title,0,'none',fanart,show_img,'none',show_plot)###( Getting Metadata from thetvdb for show_name )###
				#thetvdb_data=['','','','','','','','','','','','','','','','','']
			##
			if (debugging==True): print thetvdb_data
			vid_descr=show_plot #thetvdb_data[6]
			if (vid_descr=='(Not Available)') or (vid_descr==''): vid_descr=thetvdb_data[6]
			vid_descr=ParseDescription(vid_descr)
			#
			vid_status=thetvdb_data[8]
			vid_fanart=thetvdb_data[3]
			if (vid_fanart=='none') or (vid_fanart==''): vid_fanart=fanart
			vid_poster=thetvdb_data[4]
			if (vid_poster=='none') or (vid_poster==''): vid_poster=show_img
			vid_banner=thetvdb_data[5]
			vid_language=thetvdb_data[9]
			vid_network=thetvdb_data[10]
			vid_id=thetvdb_data[1]
			vid_genres=thetvdb_data[7]
			#if vid_genres=='none': vid_genres=show_genres
			vid_rating=thetvdb_data[11]
			vid_votes='Unknown'#thetvdb_data[6]##not handled atm
			vid_released='Unknown'#thetvdb_data[]
			vid_type='Dubbed Anime'#'Unknown'#thetvdb_data[6]
			Labels={ 'Title':show_title,'Plot':vid_descr,'Year':vid_released,'Status':vid_status,'Rating':vid_rating, 'ShowID':vid_id,'Votes':vid_votes,'Type':vid_type, 'Fanart':vid_fanart, 'Poster':vid_poster, 'Banner':vid_banner, 'Language':vid_language, 'Network':vid_network, 'Genre':vid_genres } 
			addDirD(show_title,show_title,show_url,type2,257,vid_poster,vid_fanart,True,'',Labels)
	set_view(viewtyp,int(getset('viewmode-shows')))#set_view('none',508)


def menu256_show_list(url):#dubbed-anime#show-listings
	viewtyp='tvshows'
	link=getURL(url)
	matchbb=re.compile('<li><a href="(.+?)">&gt;</a></li>').findall(link)
	for url33 in matchbb:
		Labels={ 'Title':' Next' }
		addDirD(' Next','list',url33,type2,mode,artPath + 'next-icon.png',fanart,True,' Next',Labels)#gogoanime\\next.png
	matchb=re.compile('<li><a href="(.+?)">Next</a></li>').findall(link)
	for url3 in matchb:
		Labels={ 'Title':' Next' }
		addDirD(' Next','list',url3,type2,mode,artPath + 'next-icon.png',fanart,True,' Next',Labels)#gogoanime\\next.png
	if (type2==8):
		dat_aa=link.split('<p><b>Filter by Genres:</b>')[1]
		dat_a=dat_aa.split('<div class="post-')
		for dat_show in dat_a:
			#if (debugging==True): print dat_show
			dat_show=dat_show.split('</div><!--/post-')[0]
			if ('<h2 class="title"><a href="' in dat_show):
				#if (debugging==True): print dat_show
				show_url=(re.compile('<h2 class="title"><a href="(.+?)"').findall(dat_show)[0]).strip()
				if (debugging==True): print 'show url: '+show_url
				# rel="bookmark" title="Permanent Link to Maburaho">Maburaho
				try: show_title=(re.compile('rel="bookmark" title="Permanent Link to .+?">(.+?)</a></h2>').findall(dat_show)[0]).strip()
				except: show_title='Unknown'
				show_title=ParseDescription(show_title)
				if (debugging==True): print 'show title: '+show_title
				## site does have Votes, Rating(# out of 5), Rated, stars, genres, themes
				try: show_img=(re.compile('<img src="(.+?)" width="165" height="200" style="float: left;margin:0px 5px 0px 5px;" />').findall(dat_show)[0]).strip()
				except: show_img=ICON
				if (debugging==True): print 'show img: '+show_img
				try: show_plot=(((dat_show.split('<br />Plot Summary: ')[1])).split('</p>')[0]).strip()
				except:
					try: show_plot=(((dat_show.split('Plot Summary: ')[1])).split('</p>')[0]).strip()
					except: show_plot='(Not Available)'
				if (debugging==True): print 'show plot: '+show_plot
				#
				#
				##
				if (metaArt_DoCheck(show_title)==True):
					if (debugging==True): print show_title + ' found in cached metaArt Data.'
					thetvdb_data=metaArt_getCache(show_title)
				else:
					thetvdb_data=metaArt_get(show_title,0,'none',fanart,show_img,'none',show_plot)###( Getting Metadata from thetvdb for show_name )###
				##
				#thetvdb_data=metaArt_get(show_title,0,'none',fanart,show_img,'none',show_plot)###( Getting Metadata from thetvdb for show_name )###
				if (debugging==True): print thetvdb_data
				vid_descr=show_plot #thetvdb_data[6]
				if (vid_descr=='(Not Available)'): vid_descr=thetvdb_data[6]
				vid_descr=ParseDescription(vid_descr)
				#
				vid_status=thetvdb_data[8]
				vid_fanart=thetvdb_data[3]
				if vid_fanart=='none': vid_fanart=fanart
				vid_poster=thetvdb_data[4]
				if vid_poster=='none': vid_poster=show_img
				vid_banner=thetvdb_data[5]
				vid_language=thetvdb_data[9]
				vid_network=thetvdb_data[10]
				vid_id=thetvdb_data[1]
				vid_genres=thetvdb_data[7]
				#if vid_genres=='none': vid_genres=show_genres
				vid_rating=thetvdb_data[11]
				vid_votes='Unknown'#thetvdb_data[6]##not handled atm
				vid_released='Unknown'#thetvdb_data[]
				vid_type='Dubbed Anime'#'Unknown'#thetvdb_data[6]
				Labels={ 'Title':show_title,'Plot':vid_descr,'Year':vid_released,'Status':vid_status,'Rating':vid_rating, 'ShowID':vid_id,'Votes':vid_votes,'Type':vid_type, 'Fanart':vid_fanart, 'Poster':vid_poster, 'Banner':vid_banner, 'Language':vid_language, 'Network':vid_network, 'Genre':vid_genres } 
				addDirD(show_title,show_title,show_url,type2,257,vid_poster,vid_fanart,True,'',Labels)
		set_view(viewtyp,int(getset('viewmode-shows')))#set_view('none',508)
	if (type2==7):
		dat_a=link.split('<div class="genre-flasher"><h4 class="post-title" style="border-radius:0;-moz-border-radius: 0;-webkit-border-radius: 0;border-right: none;border-left: none;margin: 7px auto;">')
		#if (debugging==True): print dat_a
		for dat_show in dat_a:
			#if (debugging==True): print dat_show
			if ('<div><b>Title:</b> <span style="color:black;">' in dat_show):
				#if (debugging==True): print dat_show
				show_url=(re.compile('<a href="(.+?)"').findall(dat_show)[0]).strip()
				if (debugging==True): print 'show url: '+show_url
				try: show_title=(re.compile('<div><b>Title:</b> <span style="color:black;">(.+?)</span></div>').findall(dat_show)[0]).strip()
				except: show_title='Unknown'
				if (debugging==True): print 'show title: '+show_title
				#<img width="215" height="300" src="http://www.dubhappy.eu/images/blue-gender.jpg" />
				try: show_img=(re.compile('<img width=".+?" height=".+?" src="(.+?)" />').findall(dat_show)[0]).strip()
				except: show_img=ICON
				if (debugging==True): print 'show img: '+show_img
				try: show_plot=(((dat_show.split('>Sypnosis</h2>')[1]).split('<p>')[1]).split('</p>')[0]).strip()
				except: show_plot='(Not Available)'
				if (debugging==True): print 'show plot: '+show_plot
				#
				#
				##
				if (metaArt_DoCheck(show_title)==True):
					if (debugging==True): print show_title + ' found in cached metaArt Data.'
					thetvdb_data=metaArt_getCache(show_title)
				else:
					thetvdb_data=metaArt_get(show_title,0,'none',fanart,show_img,'none',show_plot)###( Getting Metadata from thetvdb for show_name )###
				##
				#thetvdb_data=metaArt_get(show_title,0,'none',fanart,show_img,'none',show_plot)###( Getting Metadata from thetvdb for show_name )###
				if (debugging==True): print thetvdb_data
				vid_descr=show_plot #thetvdb_data[6]
				if (vid_descr=='(Not Available)'): vid_descr=thetvdb_data[6]
				vid_descr=ParseDescription(vid_descr)
				#
				vid_status=thetvdb_data[8]
				vid_fanart=thetvdb_data[3]
				if vid_fanart=='none': vid_fanart=fanart
				vid_poster=thetvdb_data[4]
				if vid_poster=='none': vid_poster=show_img
				vid_banner=thetvdb_data[5]
				vid_language=thetvdb_data[9]
				vid_network=thetvdb_data[10]
				vid_id=thetvdb_data[1]
				vid_genres=thetvdb_data[7]
				#if vid_genres=='none': vid_genres=show_genres
				vid_rating=thetvdb_data[11]
				vid_votes='Unknown'#thetvdb_data[6]##not handled atm
				vid_released='Unknown'#thetvdb_data[]
				vid_type='Dubbed Anime'#'Unknown'#thetvdb_data[6]
				Labels={ 'Title':show_title,'Plot':vid_descr,'Year':vid_released,'Status':vid_status,'Rating':vid_rating, 'ShowID':vid_id,'Votes':vid_votes,'Type':vid_type, 'Fanart':vid_fanart, 'Poster':vid_poster, 'Banner':vid_banner, 'Language':vid_language, 'Network':vid_network, 'Genre':vid_genres } 
				addDirD(show_title,show_title,show_url,type2,257,vid_poster,vid_fanart,True,'',Labels)
				#
		set_view(viewtyp,int(getset('viewmode-shows')))#set_view('none',508)
	if (type2==6):
		dat_a=link.split('<div style="width:570px; width:100%; padding:7px; float:left;">')
		for dat_show in dat_a:
			if 'href="' in dat_show: 
				show_url=(re.compile(' href="(.+?)"').findall(dat_show)[0]).strip()
				try: show_title=(re.compile(' title="(.+?)"').findall(dat_show)[0]).strip()
				except: show_title='Unknown'
				try: show_img=(re.compile('<img src="(.+?)"').findall(dat_show)[0]).strip()
				except: show_img=ICON
				try: show_plot=(((dat_show.split('<span style="')[1]).split('">')[1]).split('<a style="')[0]).strip()
				except: show_plot='(Not Available)'
				#
				##
				if (metaArt_DoCheck(show_title)==True):
					if (debugging==True): print show_title + ' found in cached metaArt Data.'
					thetvdb_data=metaArt_getCache(show_title)
				else:
					thetvdb_data=metaArt_get(show_title,0,'none',fanart,show_img,'none',show_plot)###( Getting Metadata from thetvdb for show_name )###
				##
				#thetvdb_data=metaArt_get(show_title,0,'none',fanart,show_img,'none',show_plot)###( Getting Metadata from thetvdb for show_name )###
				if (debugging==True): print thetvdb_data
				vid_descr=show_plot #thetvdb_data[6]
				if (vid_descr=='(Not Available)'): vid_descr=thetvdb_data[6]
				vid_descr=ParseDescription(vid_descr)
				#
				vid_status=thetvdb_data[8]
				vid_fanart=thetvdb_data[3]
				if vid_fanart=='none': vid_fanart=fanart
				vid_poster=thetvdb_data[4]
				if vid_poster=='none': vid_poster=show_img
				vid_banner=thetvdb_data[5]
				vid_language=thetvdb_data[9]
				vid_network=thetvdb_data[10]
				vid_id=thetvdb_data[1]
				vid_genres=thetvdb_data[7]
				#if vid_genres=='none': vid_genres=show_genres
				vid_rating=thetvdb_data[11]
				vid_votes='Unknown'#thetvdb_data[6]##not handled atm
				vid_released='Unknown'#thetvdb_data[]
				vid_type='Dubbed Anime'#'Unknown'#thetvdb_data[6]
				Labels={ 'Title':show_title,'Plot':vid_descr,'Year':vid_released,'Status':vid_status,'Rating':vid_rating, 'ShowID':vid_id,'Votes':vid_votes,'Type':vid_type, 'Fanart':vid_fanart, 'Poster':vid_poster, 'Banner':vid_banner, 'Language':vid_language, 'Network':vid_network, 'Genre':vid_genres } 
				addDirD(show_title,show_title,show_url,type2,257,vid_poster,vid_fanart,True,'',Labels)
				#ParseDescription()
			#
		#
	#elif (type2==0):
	set_view(viewtyp,int(getset('viewmode-shows')))#set_view('none',508)
### ############################################################################################################
def menu253(url):#dubbed-anime#show-listings
	viewtyp='tvshows'
	link=getURL(url)
	if type2==5:t=''
	else: return
	dat_a=(link.split('<p><b>Filter by Genres:</b>')[1]).split('<div class="navigation">')[0]
	dat_b=(link.split('</div><!--/post-'))
	for dat_show in dat_b:
		if '/><b>Watch ' in dat_show:
			if '/><b>Watch ' in dat_show: show_title=(re.compile('/><b>Watch (.+?)</b>').findall(dat_show)[0]).strip()
			else: show_title='[Unknown]'
			try: show_url=mainSite+(((re.compile("<a href='(.+?)'>Watch This Anime >>></a></b></p>").findall(dat_show)[0]).strip()).replace('../',''))
			except: show_url='Unknown'
			if (show_url=='Unknown') or (show_title=='[Unknown]'): t=''
			else:
				try: show_img=mainSite+(((re.compile('<img src="(.+?)" width="165" height="200" style="float: left;margin:.+?;" /><b>Watch ').findall(dat_show)[0]).strip()).replace('../',''))
				except: show_img=ICON
				try: show_genres=((re.compile('>Genres <font color=".+?"> : (.+?)<').findall(dat_show)[0]).strip())
				except: show_genres='Unknown' ##Example: 'action, adventure, comedy, drama, magic, romance'
				try: show_themes=((re.compile('Themes: (.+?)<').findall(dat_show)[0]).strip())
				except: show_themes='Unknown' ##Example: 'dragons, fanservice, harem, magical girl, school, tsundere'
				try: show_plot=((dat_show.split('> Plot Summary: ')[1]).split('...</p>')[0]).strip()
				except: show_plot='(Not Available)'
				try: show_episode_count=((re.compile('Number of Episodes : (.+?) Episode').findall(dat_show)[0]).strip())
				except: show_episode_count='0'
				try: show_comment_count=((re.compile('Total of Comments :  (.+?) Comment').findall(dat_show)[0]).strip())
				except: show_comment_count='0'
				try: show_votes=((re.compile('title="(.+?) votes,').findall(dat_show)[0]).strip())
				except: show_votes='0'
				#try: show_rating=((re.compile('votes, average: (.+?) out of 5"').findall(dat_show)[0]).strip())
				#try: show_rating=((dat_show.split(' out of 5"')[0]).split('average: ')[1]).strip()
				try: show_rating=((dat_show.split('average: ')[1]).split(' out of 5"')[0]).strip()
				except: show_rating='0'
				#
				##
				if (metaArt_DoCheck(show_title)==True):
					if (debugging==True): print show_title + ' found in cached metaArt Data.'
					thetvdb_data=metaArt_getCache(show_title)
				else:
					thetvdb_data=metaArt_get(show_title,0,'none',fanart,show_img,'none',show_plot)###( Getting Metadata from thetvdb for show_name )###
				##
				##thetvdb_data=metaArt_get(show_title,0,'none',fanart,show_img,'none',show_plot)###( Getting Metadata from thetvdb for show_name )###
				#
				if (debugging==True): print thetvdb_data
				vid_descr=show_plot #thetvdb_data[6]
				#if vid_descr=='none': vid_descr=show_plot
				if ("&#8217;" in vid_descr): vid_descr=vid_descr.replace("&#8217;","'")
				if ("&#8220;" in vid_descr): vid_descr=vid_descr.replace('&#8220;','"')
				if ("&#8221;" in vid_descr): vid_descr=vid_descr.replace('&#8221;','"')
				vid_status=thetvdb_data[8]
				vid_fanart=thetvdb_data[3]
				if vid_fanart=='none': vid_fanart=fanart
				vid_poster=thetvdb_data[4]
				if vid_poster=='none': vid_poster=show_img
				vid_banner=thetvdb_data[5]
				vid_language=thetvdb_data[9]
				vid_network=thetvdb_data[10]
				vid_id=thetvdb_data[1]
				vid_genres=show_genres #thetvdb_data[7]
				#if vid_genres=='none': vid_genres=show_genres
				vid_rating=show_rating #thetvdb_data[11]
				vid_votes=show_votes #'Unknown'#thetvdb_data[6]##not handled atm
				vid_released='Unknown'#thetvdb_data[]
				vid_type='Dubbed Anime'#'Unknown'#thetvdb_data[6]
				Labels={ 'Title':show_title,'Plot':vid_descr,'Year':vid_released,'Status':vid_status,'Rating':vid_rating, 'ShowID':vid_id,'Votes':vid_votes,'Type':vid_type, 'Fanart':vid_fanart, 'Poster':vid_poster, 'Banner':vid_banner, 'Language':vid_language, 'Network':vid_network, 'Genre':vid_genres, 'Theme': show_themes, 'Comments':show_comment_count, 'Total Episodes':show_episode_count } 
				addDirD(show_title,show_title,show_url,type2,254,vid_poster,vid_fanart,True,'',Labels)
	if ('">&gt;</a></li>' in link):
		matchb=re.compile('<li><a href="(.+?)">&gt;</a></li>').findall(link)
		for url3 in matchb:
			if '../' in url3: url3=(url3.replace('../','page/'))
			url3=mainSite+url3
			addDir(' Next',show,url3,type2,253,artPath + 'next-icon.png',fanart)#gogoanime\\next.png
	set_view(viewtyp,int(getset('viewmode-shows')))#set_view('none',508)
def menu253_old(url):#dubbed-anime#show-listings #### fails to display some results
	viewtyp='tvshows'
	link=getURL(url)
	match=re.compile('<img src="../(.+?)" width="165" height="200" style="float: left;margin:.+?;" /><b>Watch (.+?)</b><br/>Genres <font color="#FFFFCC"> : (.+?)<br />\s+<font color="#FFFFCC"> Plot Summary: (.+?)\s+...</p>\s+<p align="right"><b><a href=\'(.+?)\'>Watch This Anime >>></a></b></p>').findall(link)
	if (debugging==True): print match
	#show_img,show_title,show_genres,show_plot,show_url
	for show_img,show_title,show_genres,show_plot,show_url in match:
		if type2==5:
			#
			thetvdb_data=metaArt_get(show_title,0,'none',fanart,mainSite+show_img,'none',show_plot)###( Getting Metadata from thetvdb for show_name )###
			if (debugging==True): print thetvdb_data
			vid_descr=thetvdb_data[6]
			vid_released='Unknown'#thetvdb_data[]
			vid_status=thetvdb_data[8]
			vid_rating=thetvdb_data[11]
			vid_votes='Unknown'#thetvdb_data[6]##not handled atm
			vid_type='Unknown'#thetvdb_data[6]
			show_fanart=thetvdb_data[3]
			if show_fanart=='none': show_fanart=fanart
			show_poster=thetvdb_data[4]
			if show_poster=='none': show_poster=mainSite+show_img
			show_banner=thetvdb_data[5]
			show_genres=thetvdb_data[7]
			show_language=thetvdb_data[9]
			show_network=thetvdb_data[10]
			show_id=thetvdb_data[1]
			if vid_descr=='none': vid_descr=show_plot
			if show_genres=='none': show_genres=show_genres
			Labels={ 'Title':show_title,'Plot':vid_descr,'Year':vid_released,'Status':vid_status,'Rating':vid_rating, 'ShowID':show_id,'Votes':vid_votes,'Type':vid_type, 'Fanart':show_fanart, 'Poster':show_poster, 'Banner':show_banner, 'Language':show_language, 'Network':show_network, 'Genre':show_genres }
			#Labels={ 'Title':show_title,'Plot':show_plot,'Genre':show_genres }
			addDirD(show_title,show_title,mainSite+show_url,type2,254,show_poster,show_fanart,True,'',Labels)
			#addDirD(name,name2,url,type2,mode,iconimage,fanimage,doSorting=False,categoryA='Blank',Labels='none')
		else:
			#addDirD(show_title,show_title,show_url,type2,4,show_img,fanart,False,'',show_plot,show_genres)
			test=''
	matchb=re.compile('<li><a href="(.+?)">&gt;</a></li>').findall(link)
	for url3 in matchb:
		if '..' in url3: url3=url3.replace('..','page')
		addDir(' Next',show,mainSite+url3,type2,253,artPath + 'next-icon.png',fanart)#gogoanime\\next.png
	#set_view('none',508)
	set_view(viewtyp,int(getset('viewmode-shows')))
### ############################################################################################################
def menu254(url):#dubbed-anime#list episodes
	test=''
	#
def menu201():#Series by A-Z
	showlistdir('others','#','123')
	for ii in MyAlphabet[:]:
		showlistdir(ii,ii,ii)
	set_view('none',int(getset('viewmode-default')))
def menu301():#Movies by A-Z (if option is available)
	movielistdir('others','#','123')
	for ii in MyAlphabet[:]:
		movielistdir(ii,ii,ii)
	set_view('none',int(getset('viewmode-default')))
def menu211(url):#List Available Genres for series
	genrelist(url,211)
	set_view('none',int(getset('viewmode-default')))#set_view('none',50)
def menu311(url):#List Available Genres for movies
	genrelist(url,311)
	set_view('none',int(getset('viewmode-default')))#set_view('none',50)
def genrelist(url,modeA):#Get list of Available Genres from Site
	link=getURL(url)
	if (shoDebugging==True): notification('Genre List',url)
	if (type2==7):
		match=re.compile("<a class='ctag' href='(.+?)'>(.+?)</a>").findall(link)
		for url2,name in match:
			if (' ' in url2): url2=url2.replace(' ','+')
			addDirD(name,name,url2,type2,256,ICON,fanart,True)#testing: change addDirD back to addDir later
	else:
		match=re.compile('<tr>\s+<td>\s+<a href="(.+?)">(.+?)</a>\s+</td>\s+<td>(.+?)</td>\s+</tr>').findall(link)
		for url2,name,shocount in match:
			addDirD(name + ' - (' + shocount + ')',name,url2,type2,6,ICON,fanart,True)#testing: change addDirD back to addDir later
	##set_view('none',50)
### ############################################################################################################
def showlistnames(url,modeA):
	if ('movie' in url): viewtyp='movies'
	else: viewtyp='tvshows'
	link=getURL(url)
	match=re.compile('<li>\s+<a href="(.+?)"\>(.+?)</a>').findall(link)
	for url2,name in match:
		addDir(name,name,url2,type2,5,ICON,fanart)
	matchb=re.compile('<li><a href="(.+?)">Next</a></li>').findall(link)
	for url3 in matchb:
		addDir('Next','list',url3,type2,modeA,artPath + 'next-icon.png',fanart)#gogoanime\\next.png
	set_view(viewtyp,int(getset('viewmode-shows')),True)#set_view('none',50)
def showlist(url,modeA=0,postBool=False,postData={'search':''}):#mode=6
	if ('movie' in url): viewtyp='movies'
	else: viewtyp='tvshows'
	if postBool==True:
		#if (debugging==True): print 'showlist function data:',postData,'url:',url
		link=postURL(url,postData)
	else:
		link=getURL(url)
	#set_view(viewtyp,515,True)
	matchbb=re.compile('<li><a href="(.+?)">&gt;</a></li>').findall(link)
	for url33 in matchbb:
		Labels={ 'Title':' Next' }
		#if (type2==5):
		#	addDirD(' Next','list',mainSite + 'subanime/' + url3,type2,modeA,artPath + 'next-icon.png',fanart,True,' Next',Labels)#gogoanime\\next.png
		#else:
		addDirD(' Next','list',url33,type2,modeA,artPath + 'next-icon.png',fanart,True,' Next',Labels)#gogoanime\\next.png
	matchb=re.compile('<li><a href="(.+?)">Next</a></li>').findall(link)
	for url3 in matchb:
		Labels={ 'Title':' Next' }
		if (type2==5):
			addDirD(' Next','list',mainSite + 'subanime/' + url3,type2,modeA,artPath + 'next-icon.png',fanart,True,' Next',Labels)#gogoanime\\next.png
		else:
			addDirD(' Next','list',url3,type2,modeA,artPath + 'next-icon.png',fanart,True,' Next',Labels)#gogoanime\\next.png
	match=re.compile('<a href="(.+?)"><img src="(.+?)" width="120" height="168" alt="Watch (.+?) online"').findall(link) #(.*)</li>
	#if (debugging==True): print'match: ',match
	for url2,img2,name in match: #,dat_
		Labels={ 'Title':name }
		#
		##
		if (metaArt_DoCheck(name)==True):
			if (debugging==True): print name + ' found in cached metaArt Data.'
			thetvdb_data=metaArt_getCache(name)
		else:
			thetvdb_data=metaArt_get(name)###( Getting Metadata from thetvdb for show_name )###
		##
		#thetvdb_data=metaArt_get(name)###( Getting Metadata from thetvdb for show_name )###
		##if (debugging==True): print thetvdb_data
		####0show_name,1show_id,2url_thetvdb,3show_fanart,4show_poster,5show_banner,6show_desc
		#######,7match_genres,8match_status,9match_language,10match_network,11match_rating
		if thetvdb_data[3]=='none': thetvdb_fanart=fanart
		else: thetvdb_fanart=thetvdb_data[3]
		##if thetvdb_data[6]=='none': show_desc=''
		##else: show_desc=thetvdb_data[6]
		##
		vid_descr=thetvdb_data[6]
		vid_released='Unknown'#thetvdb_data[]
		vid_status=thetvdb_data[8]
		vid_rating=thetvdb_data[11]
		vid_votes='Unknown'#thetvdb_data[6]##not handled atm
		vid_type='Unknown'#thetvdb_data[6]
		show_fanart=thetvdb_data[3]
		if show_fanart=='none': show_fanart=fanart
		show_poster=thetvdb_data[4]
		show_banner=thetvdb_data[5]
		show_genres=thetvdb_data[7]
		show_language=thetvdb_data[9]
		show_network=thetvdb_data[10]
		show_id=thetvdb_data[1]
		#Labels={ 'Title':name,'Plot':vid_descr,'Year':vid_released,'Status':vid_status,'Rating':vid_rating, 'ShowID':show_id,'Votes':vid_votes,'Type':vid_type, 'Fanart':show_fanart, 'Poster':show_poster, 'Banner':show_banner, 'Language':show_language, 'Network':show_network, 'Genre':show_genres }
		#
		#
		if (type2==5):
			if show_poster=='none': show_poster=mainSite + 'subanime/' + img2
			oldString='<a href="'+url2+'"><img src="'+img2+'" width="120" height="168" alt="Watch '+name+' online"'#+'.+?'
			htmlPart=(link.split(oldString)[1]).split('</li>')[0]
			if (vid_descr=='none') 		or (vid_descr=='Unknown'): 		vid_descr=		((htmlPart.split('<div class="descr">')[1]).split('[<a href="')[0]).strip()
			if (vid_released=='none') or (vid_released=='Unknown'): vid_released=	(((htmlPart.split('<span class="small">Released:</span>')[1]).split('</span>')[0]).split('class="bold">')[1]).strip()
			if (vid_status=='none') 	or (vid_status=='Unknown'): 	vid_status=		(((htmlPart.split('<span class="small">Status:</span>')[1]).split('</span>')[0]).split('class="bold">')[1]).strip()
			if (vid_rating=='none') 	or (vid_rating=='Unknown'): 	vid_rating=		(((htmlPart.split('<span class="small">Rating:</span>')[1]).split('(')[0]).split('class="bold">')[1]).strip()
			if (vid_votes=='none') 		or (vid_votes=='Unknown'): 		vid_votes=		(((htmlPart.split('<span class="small">Rating:</span>')[1]).split('Votes)')[0]).split('(')[1]).strip()
			Labels={ 'Title':name,'Plot':vid_descr,'Year':vid_released,'Status':vid_status,'Rating':vid_rating, 'ShowID':show_id,'Votes':vid_votes,'Type':vid_type, 'Fanart':show_fanart, 'Poster':show_poster, 'Banner':show_banner, 'Language':show_language, 'Network':show_network, 'Genre':show_genres }
			addDirD(name,name,mainSite + 'subanime/' + url2,type2,4,show_poster,show_fanart,True,name,Labels)
		elif (type2==1):#animeget
			if show_poster=='none': show_poster=img2
			oldString='<a href="'+url2+'"><img src="'+img2+'" width="120" height="168" alt="Watch '+name+' online"'#+'.+?'
			htmlPart=(link.split(oldString)[1]).split('</li>')[0]
			if (vid_descr=='none') 		or (vid_descr=='Unknown'): 		vid_descr=		((htmlPart.split('<div class="descr">')[1]).split('[<a href="')[0]).strip()
			if (vid_released=='none') or (vid_released=='Unknown'): vid_released=	(((htmlPart.split('<span class="small">Released:</span>')[1]).split('</span>')[0]).split('class="bold">')[1]).strip()
			if (vid_status=='none') 	or (vid_status=='Unknown'): 	vid_status=		(((htmlPart.split('<span class="small">Status:</span>')[1]).split('</span>')[0]).split('class="bold">')[1]).strip()
			if (vid_rating=='none') 	or (vid_rating=='Unknown'): 	vid_rating=		(((htmlPart.split('<span class="small">Rating:</span>')[1]).split('(')[0]).split('class="bold">')[1]).strip()
			if (vid_votes=='none') 		or (vid_votes=='Unknown'): 		vid_votes=		(((htmlPart.split('<span class="small">Rating:</span>')[1]).split('Votes)')[0]).split('(')[1]).strip()
			if (vid_type=='none') 		or (vid_type=='Unknown'): 		vid_type=			((htmlPart.split('<span class="type_indic">')[1]).split('</span>')[0]).strip()
			#if (debugging==True): print name,vid_descr,vid_released,vid_status,vid_rating,vid_votes
			#Labels={ 'Title':name,'Plot':vid_descr,'Year':vid_released,'Status':vid_status,'Rating':vid_rating,'Votes':vid_votes,'Type':vid_type }
			Labels={ 'Title':name,'Plot':vid_descr,'Year':vid_released,'Status':vid_status,'Rating':vid_rating, 'ShowID':show_id,'Votes':vid_votes,'Type':vid_type, 'Fanart':show_fanart, 'Poster':show_poster, 'Banner':show_banner, 'Language':show_language, 'Network':show_network, 'Genre':show_genres }
			addDirD(name,name,url2,type2,4,show_poster,show_fanart,True,name,Labels)
		elif (type2==2) or (type2==3):#anime44 & animeplus
			if show_poster=='none': show_poster=img2
			oldString='<a href="'+url2+'"><img src="'+img2+'" width="120" height="168" alt="Watch '+name+' online"'#+'.+?'
			htmlPart=(link.split(oldString)[1]).split('</li>')[0]
			if (vid_descr=='none') 		or (vid_descr=='Unknown'): 		vid_descr=		((htmlPart.split('<div class="descr">')[1]).split('[<a href="')[0]).strip()
			if (vid_released=='none') or (vid_released=='Unknown'): vid_released=	(((htmlPart.split('<span class="small">Released:</span>')[1]).split('</span>')[0]).split('class="bold">')[1]).strip()
			if (vid_status=='none') 	or (vid_status=='Unknown'): 	vid_status=		(((htmlPart.split('<span class="small">Status:</span>')[1]).split('</span>')[0]).split('class="bold">')[1]).strip()
			if (vid_rating=='none') 	or (vid_rating=='Unknown'): 	vid_rating=		(((htmlPart.split('<span class="small">Rating:</span>')[1]).split('(')[0]).split('class="bold">')[1]).strip()
			if (vid_votes=='none') 		or (vid_votes=='Unknown'): 		vid_votes=		(((htmlPart.split('<span class="small">Rating:</span>')[1]).split('Votes)')[0]).split('(')[1]).strip()
			#if (debugging==True): print name,vid_descr,vid_released,vid_status,vid_rating,vid_votes
			#Labels={ 'Title':name,'Plot':vid_descr,'Year':vid_released,'Status':vid_status,'Rating':vid_rating,'Votes':vid_votes,'Type':vid_type }
			Labels={ 'Title':name,'Plot':vid_descr,'Year':vid_released,'Status':vid_status,'Rating':vid_rating, 'ShowID':show_id,'Votes':vid_votes,'Type':vid_type, 'Fanart':show_fanart, 'Poster':show_poster, 'Banner':show_banner, 'Language':show_language, 'Network':show_network, 'Genre':show_genres }
			addDirD(name,name,url2,type2,4,show_poster,show_fanart,True,name,Labels)
		else:
			if show_poster=='none': show_poster=img2
			Labels={ 'Title':name,'Plot':vid_descr,'Year':vid_released,'Status':vid_status,'Rating':vid_rating, 'ShowID':show_id,'Votes':vid_votes,'Type':vid_type, 'Fanart':show_fanart, 'Poster':show_poster, 'Banner':show_banner, 'Language':show_language, 'Network':show_network, 'Genre':show_genres }
			addDirD(name,name,url2,type2,4,show_poster,show_fanart,True,name,Labels)
	xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_TITLE)
	set_view(viewtyp,int(getset('viewmode-shows')),True)
### ############################################################################################################
def EPISODESlist(url,mediaType='Subbed'):
        #
        if (shoDebugging==True): 
        	try: VaddDir('  [COLOR cornsilk][COLOR purple]Show: [/COLOR]'+show+'[/COLOR]' + '[COLOR grey][/COLOR]', '', 1, ICON, fanart)
        	except: t=''
        #
        #if ('movie' in url): viewtyp='movies'
        #else: viewtyp='tvshows'
        viewtyp='episodes'
        #if (debugging==True): print 'testing for animeget thetvdb'
        ##
        if (metaArt_DoCheck(show)==True):
        	if (debugging==True): print show + ' found in cached metaArt Data.'
        	thetvdb_data=metaArt_getCache(show)
        else:
        	thetvdb_data=metaArt_get(show)
        ##
        ##
        ##
        #thetvdb_data=metaArt_get(show)
        ##
        ##
        ###show_name,show_id,url_thetvdb,show_fanart,show_poster,show_banner,show_desc,match_genres,match_status,match_language,match_network,match_rating
        if thetvdb_data[3]=='none': thetvdb_fanart=fanart
        else: thetvdb_fanart=thetvdb_data[3]
        if thetvdb_data[6]=='none': show_desc=''
        else: show_desc=thetvdb_data[6]
        #if (debugging==True): print 'thetvdb_fanart: '+thetvdb_fanart
        #
        link=getURL(url)
        matchb=re.compile('<li><a href="(.+?)">Next</a></li>').findall(link)
        for url3 in matchb:
        	addDirD(' Next',show,url3,type2,mode,artPath + 'next-icon.png',thetvdb_fanart)#gogoanime\\next.png
        img3=''
        matcha=re.compile('<img src="(.+?)" id="series_image" width="250" height="370" alt="').findall(link)
        for img2 in matcha:
          img3=img2
        if thetvdb_data[4]=='none': thetvdb_poster=img3
        else: thetvdb_poster=thetvdb_data[4]
        if (type2==1) or (Sites[0] in url) or (type2==3) or (Sites[2] in url) or (type2==4) or (Sites[3] in url):#animeget, animeplus, gooddrama
        	match=re.compile('<li>\s+<a href="(.+?)">(.+?)</a>\s+<span class="right_text">(.+?)</span>').findall(link)
        	for url2,name,dateadded in match:
        		addDirD(name + ' - (' + dateadded + ')',name,url2,type2,5,img3,thetvdb_fanart)
        		#addDir(name + ' - (' + dateadded + ')',name,url2,type2,5,img3,fanart)
        elif (type2==5):#AnimeZone
        	match=re.compile('<a href="../(.+?)">(.+?)</a><br />').findall(link)
        	if mediaType=='Dubbed': url_pre=mainSite+'english-dubbed/'+''
        	else: url_pre=mainSite+'subanime/'+''
        	for url2,name in match:
        		addDirD(name,name,url_pre+url2,type2,5,img3,thetvdb_fanart)
        #elif (type2==8):#
        #	if ('Dub Link<br />' in link):
        #		link_dub=(link.split('Dub Link<br />')[1]).split('</p>')[0]
        #		match=re.compile('<a href="javascript:void(0)" onclick="open_win(\'http://www.veoh.com/watch/v476081J5Er7RqC\')">A Wind Named Amnesia English Dubbed (Veoh)</a>', re.MULTILINE | re.IGNORECASE | re.DOTALL).findall('__'+link+'__')
        #		for url2,name,dateadded in match:
        #			addDirD(name + ' - (' + dateadded + ')',name,url2,type2,5,img3,thetvdb_fanart)
        #	if ('Sub Link<br />' in link):
        #		link_sub=(link.split('Sub Link<br />')[1]).split('</p>')[0]
        #		match=re.compile('<li>\s+<a href="(.+?)">(.+?)</a>\s+<span class="right_text">(.+?)</span>', re.MULTILINE | re.IGNORECASE | re.DOTALL).findall('__'+link+'__')
        #		for url2,name,dateadded in match:
        #			addDirD(name + ' - (' + dateadded + ')',name,url2,type2,5,img3,thetvdb_fanart)
        else:#type2==2 or Sites[1]#anime44
        	#if (debugging==True): print 'test failed'
        	match=re.compile('<li>\s+<a href="(.+?)"\>(.+?)</a>').findall(link)
        	for url2,name in match:
        		if ('Privacy' in name) and ('Disclaimer' in name): continue
        		else:
        			#thetvdb_fanart=thetvdb_com(name)
        			#if thetvdb_fanart=='none':thetvdb_fanart=fanart
        			#addDir(name,name,url2,type2,5,img3,thetvdb_fanart)
        			#Labels={ 'Title':name,'Plot':vid_descr,'Year':vid_released,'Status':vid_status,'Rating':vid_rating,'Votes':vid_votes,'Type':vid_type }
        			Labels={ 'Title':name,'Plot':show_desc }
        			addDirD(name,name,url2,type2,5,thetvdb_poster,thetvdb_fanart,True,name,Labels)
        			addDirD(name,name,url2,type2,5,img3,thetvdb_fanart)
        ##matchb=re.compile('<li><a href="(.+?)">Next</a></li>').findall(link)
        ##for url3 in matchb:
        ##        addDir('Next','movies',url3,0,302,artPath + 'gogoanime\\next.png',fanart)
        #set_view('none',50)
        xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_TITLE)
        set_view(viewtyp,int(getset('viewmode-episodes')),True)

def menu257_episode_list(url,mediaType='Subbed'): ## Episode Listings
	if ('movie' in url): viewtyp='movies'
	else: viewtyp='tvshows'
	viewtyp='episodes'
	if (shoDebugging==True): 
		try: VaddDir('  [COLOR cornsilk][COLOR purple]Show: [/COLOR]'+show+'[/COLOR]' + '[COLOR grey][/COLOR]', '', 1, ICON, fanart)
		except: t=''
	link=getURL(url)
	link_=link
	#
	#
	show_title=show
	if (metaArt_DoCheck(show_title)==True):
		if (debugging==True): print show_title + ' found in cached metaArt Data.'
		thetvdb_data=metaArt_getCache(show_title)
		show_id=thetvdb_data[1]; show_fanart=thetvdb_data[3]; show_poster=thetvdb_data[4]; show_banner=thetvdb_data[5]
		thetvdb_episodes =thetvdb_com_episodes(show_id)
		epi_data_found=True
	else:
		show_fanart=''; show_poster=''; show_banner=''
		epi_data_found=False
	#
	#
	##
	##dat_a=(link.split('<p><b>Filter by Genres:</b>')[1]).split('<div class="navigation">')[0]
	##try: show_img=(re.compile('<img src="(.+?)"').findall(dat_show)[0]).strip()
	##except: show_img=ICON0
	##try: show_plot=(((dat_show.split('<span style="')[1]).split('">')[1]).split('<a style="')[0]).strip()
	##match=re.compile('<li>\s+<a href="(.+?)"\>(.+?)</a>').findall(link)
	#
	if (type2==6): ## Getting text area down to just around the episode listings.
		link=(link.split('<ul class="ul-ep-list">')[1]).split('</ul>')[0]
	elif (type2==7): ## Getting text area down to just around the episode listings.
		link=(link.split('<tr style="border-bottom: 2px solid #90C0D9;" class="table_heading">')[1]).split('</tbody>')[0]
	elif (type2==8): ## Getting text area down to just around the episode listings.
		link=(link.split('</span> Episodes Links:</b></span>')[1]).split('class="post-ratings">Rate this anime :')[0]
	#
	#
	if (type2==6): ## Parsing episode listings
		#
		dat_a=link.split('<li><strong>')
		try: show_img=(re.compile('<img style=".+?" src="(.+?)" width="225" height="350" title="').findall(link_)[0]).strip()
		except: show_img=ICON
		#try: show_plot=(((dat_show.split('<span style="')[1]).split('">')[1]).split('<a style="')[0]).strip()
		#except: show_plot='(Not Available)'
		#if (show_plot=='(Not Available)'): t=''
		#else: ParseDescription(show_plot)
		for dat_show in dat_a:
			if 'href="' in dat_show: 
				episode_url=(re.compile(' href="(.+?)"').findall(dat_show)[0]).strip()
				#try: episode_title=(re.compile(' title="(.+?)"').findall(dat_show)[0])
				try: episode_title=(((dat_show.split('title="')[1]).split('">')[1]).split('<')[0]).strip()
				except: episode_title='Unknown'
				try: episode_dateposted=(re.compile('"date-post">(.+?)</span>').findall(dat_show)[0]).strip()
				except: episode_dateposted='Unknown'
				#
				episode_title_old=episode_title; epi_data_done=False
				if (epi_data_found==True):
					(season_number, episode_number) = Episode__get_S_Ep_No(episode_title)
					if (episode_number is not ''): ### <tr><td class="even"><a href="/?tab=episode&seriesid=72454&seasonid=4166&id=86048&amp;lid=7">1 x 2</a></td><td class="even"><a href="/?tab=episode&seriesid=72454&seasonid=4166&id=86048&amp;lid=7">The Kidnapping of a Company President's Daughter Case</a></td><td class="even">1996-01-15</td><td class="even"><img src="/images/checkmark.png" width=10 height=10> &nbsp;</td></tr>
						for thetvdb_episode in thetvdb_episodes:
							if (thetvdb_episode[1].strip()==(season_number+' x '+episode_number)):
								episode_title=thetvdb_episode[1].strip()+' - '+thetvdb_episode[3].strip()
								(episode_dateaired,episode_year,episode_month,episode_day) = Episode__get_date(thetvdb_episode)
								(episode_thumbnail,id_series,id_episode) = Episode__get_thumb(thetvdb_episode[0].strip(),show_img)
								episode_fanart=show_img; episode_plot=''; epi_data_done=True
				if (epi_data_done==False):
					episode_fanart=fanart; episode_thumbnail=show_img; episode_dateaired=''; id_series=''; id_episode=''; season_number=''; episode_number=''; episode_year=''; episode_month=''; episode_day=''; episode_plot=''
				#
				episode_title=ParseDescription(episode_title)
				#Labels={ 'Title': episode_title, 'Dated Posted': episode_dateposted }#,'Plot':show_desc }
				Labels={ 'Title': '[B]'+show_title+'[/B][CR] - '+episode_title, 'Dated Posted': episode_dateposted, 'Premiered': episode_dateaired, 'Date Aired': episode_dateaired, 'Date': episode_dateaired, 'Season': season_number, 'Episode': episode_number, 'Year': episode_year, 'Month': episode_month, 'Day': episode_day, 'Plot': episode_plot, 'TVShowTitle': show_title, 'Poster': show_poster, 'FanArt': show_fanart, 'Banner': show_banner }
				addDirD(episode_title,'[B]'+show_title+'[/B] - '+episode_title,episode_url,type2,501,episode_thumbnail,show_fanart,True,'[B]'+show_title+'[/B] - '+episode_title,Labels)
				#addDirD(episode_title+'   ('+episode_dateposted+')',episode_title,episode_url,type2,5,show_img,fanart,True,episode_title,Labels)
				#addDirD(episode_title,episode_title,url2,type2,5,thetvdb_poster,thetvdb_fanart,True,episode_title,Labels)
				#addDirD(name,name,url2,type2,5,img3,thetvdb_fanart)
	if (type2==7): ## Parsing episode listings
		dat_a=link.split('<tr style="border: 1px solid #90C0D9;">')
		try: show_img=(re.compile('<img width="215" height="300" src="(.+?)" />').findall(link_)[0]).strip()
		except: show_img=ICON
		for dat_show in dat_a:
			if 'href="' in dat_show: 
				episode_url=(re.compile('<a style="color:#333; text-decoration:none;" href="(.+?)">').findall(dat_show)[0]).strip()
				try: episode_title=(((dat_show.split('title="')[1]).split('">')[1]).split('<')[0]).strip()
				except: episode_title='Unknown'
				#try: episode_dateposted=(re.compile('"date-post">(.+?)</span>').findall(dat_show)[0]).strip()
				#except: episode_dateposted='Unknown'
				episode_dateposted='Unknown'
				#
				episode_title_old=episode_title; epi_data_done=False
				if (epi_data_found==True):
					(season_number, episode_number) = Episode__get_S_Ep_No(episode_title)
					if (episode_number is not ''): ### <tr><td class="even"><a href="/?tab=episode&seriesid=72454&seasonid=4166&id=86048&amp;lid=7">1 x 2</a></td><td class="even"><a href="/?tab=episode&seriesid=72454&seasonid=4166&id=86048&amp;lid=7">The Kidnapping of a Company President's Daughter Case</a></td><td class="even">1996-01-15</td><td class="even"><img src="/images/checkmark.png" width=10 height=10> &nbsp;</td></tr>
						for thetvdb_episode in thetvdb_episodes:
							if (thetvdb_episode[1].strip()==(season_number+' x '+episode_number)):
								episode_title=thetvdb_episode[1].strip()+' - '+thetvdb_episode[3].strip()
								(episode_dateaired,episode_year,episode_month,episode_day) = Episode__get_date(thetvdb_episode)
								(episode_thumbnail,id_series,id_episode) = Episode__get_thumb(thetvdb_episode[0].strip(),show_img)
								episode_fanart=show_img; episode_plot=''; epi_data_done=True
				if (epi_data_done==False):
					episode_fanart=fanart; episode_thumbnail=show_img; episode_dateaired=''; id_series=''; id_episode=''; season_number=''; episode_number=''; episode_year=''; episode_month=''; episode_day=''; episode_plot=''
				#
				if ('' in episode_title): episode_title=episode_title.replace('English Dubbed','[COLOR lime](English Dubbed)[/COLOR]')
				episode_title=ParseDescription(episode_title)
				#Labels={ 'Title': episode_title, 'Dated Posted': episode_dateposted }#,'Plot':show_desc }
				Labels={ 'Title': '[B]'+show_title+'[/B][CR] - '+episode_title, 'Date Posted': episode_dateposted, 'Premiered': episode_dateaired, 'Date Aired': episode_dateaired, 'Date': episode_dateaired, 'Season': season_number, 'Episode': episode_number, 'Year': episode_year, 'Month': episode_month, 'Day': episode_day, 'Plot': episode_plot, 'TVShowTitle': show_title, 'Poster': show_poster, 'FanArt': show_fanart, 'Banner': show_banner }
				addDirD(episode_title,'[B]'+show_title+'[/B] - '+episode_title,episode_url,type2,501,episode_thumbnail,show_fanart,True,'[B]'+show_title+'[/B] - '+episode_title,Labels)
				#addDirD(episode_title,episode_title,episode_url,type2,501,show_img,fanart,True,episode_title,Labels)
	if (type2==8): ## Parsing episode listings
		link=link.replace('</p>','<br />')
		dat_a=link.split('<br />')
		try: show_img=(re.compile('<img class="photo" alt=".+?" style=".+?" src="(.+?)" border="0" alt=""id="BLOGGER_PHOTO_ID_').findall(link_)[0]).strip()
		except:
			try: show_img=(re.compile('<img class="photo" alt=".+?" src="(.+?)" width=".+?" height=".+?" /></div>').findall(link_)[0]).strip()
			except: show_img=ICON
		for dat_show in dat_a:
			#<br /><a href="http://www.watchdub.com/2009/10/maburaho-episode-1.html">Maburaho Episode 1</a>
			if '<a href="' in dat_show: 
				episode_url=(re.compile('<a href="(.+?)"').findall(dat_show)[0]).strip()
				#episode_url=(re.compile('<a href="(.+?)">.+?</a>').findall(dat_show)[0]).strip()
				#try: episode_title=(re.compile('<a href=".+?">(.+?)</a>').findall(dat_show)[0]).strip() #(((dat_show.split('title="')[1]).split('">')[1]).split('<')[0]).strip()
				try: episode_title=(re.compile('">(.+?)</a>').findall(dat_show)[0]).strip() #(((dat_show.split('title="')[1]).split('">')[1]).split('<')[0]).strip()
				except: episode_title='Unknown'
				episode_title=ParseDescription(episode_title)
				episode_dateposted='Unknown'
				#
				episode_title_old=episode_title; epi_data_done=False; thetvdb_isImg=''
				if (epi_data_found==True):
					(season_number, episode_number) = Episode__get_S_Ep_No(episode_title)
					if (episode_number is not ''): ### <tr><td class="even"><a href="/?tab=episode&seriesid=72454&seasonid=4166&id=86048&amp;lid=7">1 x 2</a></td><td class="even"><a href="/?tab=episode&seriesid=72454&seasonid=4166&id=86048&amp;lid=7">The Kidnapping of a Company President's Daughter Case</a></td><td class="even">1996-01-15</td><td class="even"><img src="/images/checkmark.png" width=10 height=10> &nbsp;</td></tr>
						for thetvdb_episode in thetvdb_episodes:
							if (thetvdb_episode[1].strip()==(season_number+' x '+episode_number)):
								print thetvdb_episode
								episode_title=thetvdb_episode[1].strip()+' - '+thetvdb_episode[3].strip()
								(episode_dateaired,episode_year,episode_month,episode_day) = Episode__get_date(thetvdb_episode)
								(episode_thumbnail,id_series,id_episode) = Episode__get_thumb(thetvdb_episode[0].strip(),show_img)
								episode_fanart=show_img; episode_plot=''; epi_data_done=True
								thetvdb_isImg=thetvdb_episode[7]
								print '7:  '+thetvdb_isImg
				if (epi_data_done==False):
					episode_fanart=fanart; episode_thumbnail=show_img; episode_dateaired=''; id_series=''; id_episode=''; season_number=''; episode_number=''; episode_year=''; episode_month=''; episode_day=''; episode_plot=''
				#
				#print '7:  '+thetvdb_isImg
				#if (thetvdb_isImg=='<img src="/images/checkmark.png" width=10 height=10>'): episode_thumbnail=ICON
				if   (not thetvdb_isImg): episode_thumbnail=show_img
				elif (thetvdb_isImg==''): episode_thumbnail=show_img
				#else: episode_thumbnail=show_img
				#if (thetvdb_episode[7]):
				#	print thetvdb_episode[7]
				#	if ('<img ' not in thetvdb_episode[7]): episode_thumbnail=show_img
				#else: episode_thumbnail=show_img
				if ('English Dubbed' in episode_title): episode_title=episode_title.replace('English Dubbed','[COLOR lime](English Dubbed)[/COLOR]')
				episode_title=ParseDescription(episode_title)
				Labels={ 'Title': '[B]'+show_title+'[/B][CR] - '+episode_title, 'Dated Posted': episode_dateposted, 'Premiered': episode_dateaired, 'Date Aired': episode_dateaired, 'Date': episode_dateaired, 'Season': season_number, 'Episode': episode_number, 'Year': episode_year, 'Month': episode_month, 'Day': episode_day, 'Plot': episode_plot, 'TVShowTitle': show_title, 'Poster': show_poster, 'FanArt': show_fanart, 'Banner': show_banner }#,'Plot':show_desc }
				addDirD(episode_title,'[B]'+show_title+'[/B] - '+episode_title,episode_url,type2,501,episode_thumbnail,show_fanart,True,'[B]'+show_title+'[/B] - '+episode_title,Labels)
				#addDirD(episode_title,'[B]'+show_title+'[/B] - '+episode_title,episode_url,type2,501,episode_thumbnail,episode_fanart,True,'[B]'+show_title+'[/B] - '+episode_title,Labels)
				#addDirD(episode_title,episode_title,episode_url,type2,501,show_img,fanart,True,episode_title,Labels)
		#
	#
	xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_TITLE)
	set_view(viewtyp,int(getset('viewmode-episodes')),True)

def CheckFor_PreviousNext_Episodes(page_dat,type2):
	if (type2==7):
		if ("<link rel='prev' title='" in page_dat):
			page_prev_title , page_prev_url = re.compile("<link rel='prev' title='(.+?)' href='(.+?)' />").findall(page_dat)[0]
			page_prev_title=ParseDescription(page_prev_title)
			Labels={ 'Title': page_prev_title }
			addDirD(' <<Previous Episode<<: '+page_prev_title,page_prev_title,page_prev_url,type2,501,ICON,fanart,True,page_prev_title,Labels)
		if ("<link rel='next' title='" in page_dat):
			page_next_title , page_next_url = re.compile("<link rel='next' title='(.+?)' href='(.+?)' />").findall(page_dat)[0]
			page_next_title=ParseDescription(page_next_title)
			Labels={ 'Title': page_next_title }
			addDirD(' >>Next Episode>>: '+page_next_title,page_next_title,page_next_url,type2,501,ICON,fanart,True,page_next_title,Labels)
	if (type2==6):
		if ("<link rel='prev' title='" in page_dat):
			page_prev_title , page_prev_url = re.compile("<link rel='prev' title='(.+?)' href='(.+?)'/>").findall(page_dat)[0]
			page_prev_title=ParseDescription(page_prev_title)
			Labels={ 'Title': page_prev_title }
			addDirD(' <<Previous Episode<<: '+page_prev_title,page_prev_title,page_prev_url,type2,5,ICON,fanart,True,page_prev_title,Labels)
			#<link rel='prev' title='Xamd Lost Memories Episode 13' href='http://dubbedanimeon.com/episode/xamd-lost-memories-episode-13-english-dubbed/'/>
		if ("<link rel='next' title='" in page_dat):
			page_next_title , page_next_url = re.compile("<link rel='next' title='(.+?)' href='(.+?)'/>").findall(page_dat)[0]
			page_next_title=ParseDescription(page_next_title)
			Labels={ 'Title': page_next_title }
			addDirD(' >>Next Episode>>: '+page_next_title,page_next_title,page_next_url,type2,5,ICON,fanart,True,page_next_title,Labels)
			#<link rel='next' title='Xamd Lost Memories Episode 15' href='http://dubbedanimeon.com/episode/xamd-lost-memories-episode-15-english-dubbed/'/>
		###
	#####
### ############################################################################################################
def VIDEOsource(url,name):
				vvVIDEOLINKS(url,name,name2,scr,imgfan,show,type2,mode)
				linkO=getURL(url)
				CheckFor_PreviousNext_Episodes(linkO,type2)
				if '/2">Playlist 2</a></li>' in linkO: 
					vvVIDEOLINKS(url + '/2',name,name2,scr,imgfan,show,type2,mode)
				if '/3">Playlist 3</a></li>' in linkO: 
					vvVIDEOLINKS(url + '/3',name,name2,scr,imgfan,show,type2,mode)
				xbmcplugin.endOfDirectory(int(sys.argv[1]))
				#url=None	urlbac=None	name=None	name2=None	type2=None	favcmd=None	mode=None	scr=None	imgfan=None	show=None
				#set_view('none',50)
def VIDEOsource_501(url,name):
	### ###  Testing knew v2 Videolinks setup  ### 
	#if (type2==7): t=''
	#else:
	#	v2vvVIDEOLINKS(url,name,name2,scr,imgfan,show,type2,mode)
	#	return
	### ### 
	vvVIDEOLINKS(url,name,name2,scr,imgfan,show,type2,mode)
	linkO=getURL(url)
	###
	if (type2==7):
		if (debugging==True): print '501 url: '+url
		matches=re.compile("file: '(.+?)'").findall(linkO)
		for match in matches:
			if (debugging==True): print '501 match: '+match
			link1=getURL(match)
			if ('<location>' in link1) and ('<image>' in link1):
				video_url=(re.compile('<location>(.+?)</location>').findall(link1)[0]).strip()
				video_img=(re.compile('<image>(.+?)</image>').findall(link1)[0]).strip()
				if (debugging==True): print '501 v url: '+video_url
				if (debugging==True): print '501 v img: '+video_img
				#vvVIDEOLINKS_doChecks(video_url,url,name,name2,video_img,fanart,show,type2,mode)
				try: addLink('[COLOR white]VerilScriptz[/COLOR]' + ' [COLOR grey][/COLOR]',video_url,video_img,imgfan,show)
				except: VaddDir('[COLOR white]VerilScriptz[/COLOR]' + ' - [COLOR grey]Error: Needs Testing.[/COLOR]', '', 1, ICON, fanart)
				#vvVIDEOLINKS(match,name,name2,scr,imgfan,show,type2,mode)
				#vvVIDEOLINKS_doChecks(match,url,name,name2,scr,imgfan,show,type2,mode)
				#
				#file: 'http://www.dubhappy.eu/wp-content/plugins/proplayer/playlist-controller.php?pp_playlist_id=11053pp-single-51df94bc83823&sid=1373607100'
				#http://www.dubhappy.eu/wp-content/plugins/proplayer/playlist-controller.php?pp_playlist_id=11053pp-single-51df94bc83823&sid=1373607100
				#http://www.dubhappy.eu/wp-content/plugins/proplayer/playlist-controller.php?pp_playlist_id=11053pp-single-51df92f643877&sid=1373606646
				#http://verilscriptz.com/scripts/sapo.php?id=GwDCJzbc9z8cEFITYGD2
				#http://cache02.stormap.sapo.pt/dld/e73d329509863b3b5bfabbdc688520d5/51df9722/vidstore08/videos/11/72/b9/3979960_MyI4G.mp4
				###
				##vvVIDEOLINKS(url,name,name2,scr,imgfan,show,type2,mode)
				##linkO=getURL(url)
				##CheckFor_PreviousNext_Episodes(linkO,type2)
				##if '/2">Playlist 2</a></li>' in linkO: 
				##	vvVIDEOLINKS(url + '/2',name,name2,scr,imgfan,show,type2,mode)
				##if '/3">Playlist 3</a></li>' in linkO: 
				##	vvVIDEOLINKS(url + '/3',name,name2,scr,imgfan,show,type2,mode)
	##linkO=getURL(url)
	#CheckFor_PreviousNext_Episodes(linkO,type2)
	xbmcplugin.endOfDirectory(int(sys.argv[1]))
	##url=None	urlbac=None	name=None	name2=None	type2=None	favcmd=None	mode=None	scr=None	imgfan=None	show=None
	##set_view('none',50)
### ############################################################################################################
def searchwindow(sitName,sitSearchmethod,sitSearchUrl,aMode,aUrl='',aName='',aType2=0):
	##searchwindow(SiteNames[type2],SiteSearchMethod[type2],SiteSearchUrls[type2],type2,name,url)
	#notification('Testing:','Search Engine.')
	aName=''
	kmsg=showkeyboard(aName, '[COLOR orange]Search: [/COLOR]'+str(sitName))
	if (kmsg == 'False'): 
		notification('Search Engine:','No message was found.')
	else:
		if sitSearchmethod=='post':
			postData = { 'search' : kmsg }
			showlist(sitSearchUrl,aMode,True,postData)
		elif sitSearchmethod=='get':
			if (type2==6): #DubbedAnimeOn
				menu257_episode_list(sitSearchUrl+urllib.quote_plus(kmsg),'Dubbed')
			else:
				showlist(sitSearchUrl+urllib.quote_plus(kmsg),aMode)
				#addDirD(name,name,url2,type2,4,img2,fanart)
### ############################################################################################################
def primewire_links(url,name):
	priUrl='http://www.primewire.ag'
	priUrlExt='http://www.primewire.ag/external.php?'
	if priUrl in url: test=''
	else: url=priUrl+url
	#if (debugging==True): print 'PrimeWire.ag URL: '+url
	if 'watch-' in url: 
		test=''
		#if (debugging==True): print '"watch-" is in url: '+url
	else: return
	page_show=getURL(url)
	if page_show=='none': return
	else:
		test=''
		#if (debugging==True): print 'page_show not == "none"'
	if '<meta property="og:title"' in page_show: show_title=re.compile('<meta property="og:title" content="(.+?)">').findall(page_show)[0]
	else: show_title='Unknown'
	if '<meta name="description"' in page_show: show_desc =re.compile('<meta name="description" content="Watch .+? online - (.+?). Download .+?.">').findall(page_show)[0]
	else: show_desc='Unknown'
	if '<meta property="og:type"' in page_show: show_type =re.compile('<meta property="og:type" content="(.+?)">').findall(page_show)[0]
	else: show_type='Unknown'
	if ('movie' in show_type): viewtyp='movies'
	else: viewtyp='tvshows'
	if '<meta property="og:image"' in page_show: show_image=re.compile('<meta property="og:image" content="(.+?)"/>').findall(page_show)[0]
	else: show_image=fanart0
	#if (debugging==True): print show_title,show_desc,show_type,show_image
	#
	Labels={ 'Title':show_title,'Plot':show_desc,'Type':show_type, 'Fanart':show_image, 'Poster':show_image }
	addDirD(show_title,show_title,'' + url,type2,1900,show_image,show_image,False,show_title,Labels)
	#
	if '<h1 class="titles"><span>Derelict Links</span></h1>' in page_show: test=''
	else: return
	page_show_part=(page_show.split('<h1 class="titles"><span>Derelict Links</span></h1>')[1]).split('<h1 class="titles">')[0]
	page_show_parts=page_show_part.split('<tbody>')
	for page_show_tbody in page_show_parts:
		page_show_tbody=page_show_tbody.split('</tbody>')[0]
		if 'sponsored' in page_show_tbody: continue
		else:
			if '<span class=quality_' in page_show_tbody: link_quality=re.compile('<span class=quality_(.+?)></span>').findall(page_show_tbody)[0]
			else: link_quality='Unknown'
			if '<a href="/external.php?' in page_show_tbody: link_extUrl=re.compile('<a href="/external.php?(.+?)"').findall(page_show_tbody)[0]
			else: link_extUrl='Unknown'
			if '<span class="version_host"><script type="text/javascript">document.writeln' in page_show_tbody: link_srcHost=re.compile('<span class="version_host"><script type="text/javascript">document.writeln\(\'(.+?)\'').findall(page_show_tbody)[0]
			else: link_srcHost='Unknown'
			if '<span class="version_veiws"> ' in page_show_tbody: link_verViews=re.compile('<span class="version_veiws"> (.+?) views</span>').findall(page_show_tbody)[0]
			else: link_verViews='Unknown'
			if '>Version ' in page_show_tbody: link_verNo=re.compile('>Version (.+?)<').findall(page_show_tbody)[0]
			else: link_verNo='0'
			if link_extUrl=='Unknown': continue
			else:
				Labels={ 'Title':link_verNo+'. - '+link_srcHost,'Plot':show_desc,'Type':show_type, 'Fanart':show_image, 'Poster':show_image, 'Quality':link_quality, 'Views':link_verViews, 'Host':link_srcHost }
				#if (debugging==True): print Labels
				#hosted_media = urlresolver.HostedMediaFile(url=item['url'], title=label)
				page_ref=getURL(priUrlExt + link_extUrl)
				if ('<noframes>' in page_ref) and ('</noframes>' in page_ref): link_hosterURL=re.compile('<noframes>(.+?)</noframes>').findall(page_ref)[0]
				else: link_hosterURL='Unknown'
				###<noframes>http://filenuke.com/ao1tn5ay9zq9
				if link_hosterURL=='Unknown': 
					#if (debugging==True): print 'hosterURL: '+link_hosterURL
					continue
				else:
					#stream_url=[]
					#hosted_media = urlresolver.HostedMediaFile(link_hosterURL, title=show_title).resolve()
					##if (debugging==True): print hosted_media
					#stream_url.append(hosted_media)
					##usable_url = urlresolver.choose_source(stream_url).get_url()
					#usable_url = stream_url
					usable_url = link_hosterURL
					#if (debugging==True): print usable_url
					filname=show_title+' ['+link_quality+']'
					#if (debugging==True): print filname
					addDirD(link_verNo+'. '+link_quality+' - '+link_srcHost+' ('+link_verViews+' views)',filname,priUrlExt + link_extUrl,type2,1902,show_image,show_image,False,show_title,Labels) ##url: file to download.
					#
					#
				#usable_url = urlresolver.choose_source(stream_url).get_url()
				#usable_url = stream_url
				#
				#usable_url= priUrlExt + link_extUrl
				#addDirD(link_verNo+'. '+link_quality+' - '+link_srcHost+' ('+link_verViews+' views)',link_srcHost,priUrlExt + link_extUrl,type2,1901,show_image,show_image,False,show_title,Labels) ##url: file to download.
				#addDirD(link_verNo+'. '+link_quality+' - '+link_srcHost+' ('+link_verViews+' views)',link_srcHost,usable_url,type2,1902,show_image,show_image,False,show_title,Labels) ##url: page needs parsed.
				#
			#
			#<a href="/external.php?gd=1890694741&title=Derelict&url=aHR0cDovL3d3dy52aWR4ZGVuLmNvbS94dzhnM2R2emwybjg=&domain=dmlkeGRlbi5jb20=&loggedin=0"
			#
			#<span class=quality_dvd></span>
			#
		#
		#
		#
	#
	#Labels={ 'Title':name,'Plot':vid_descr,'Year':vid_released,'Status':vid_status,'Rating':vid_rating, 'ShowID':show_id,'Votes':vid_votes,'Type':vid_type, 'Fanart':show_fanart, 'Poster':show_poster, 'Banner':show_banner, 'Language':show_language, 'Network':show_network, 'Genre':show_genres }
	#addDirD(name,name,mainSite + 'subanime/' + url2,type2,4,show_poster,show_fanart,True,name,Labels)
	#
	if ('movie' in show_type): set_view(viewtyp,int(getset('viewmode-movies')),False)
	else: set_view(viewtyp,int(getset('viewmode-shows')),False)
	#
### ############################################################################################################
def u_get(u=''):
	u= sys.argv[0]
	u += "?url="+qp_get(url)
	u += "&mode="+st_get(mode)
	u += "&name="+qp_get(name)
	u += "&nm="+qp_get(name2)
	u += "&tp="+st_get(type2)
	u += "&scr="+qp_get(scr)
	u += "&fan="+qp_get(imgfan)
	u += "&show="+qp_get(name2)
	u += "&cat="+qp_get(category)
	#return sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&nm="+urllib.quote_plus(name2)+"&tp="+str(type2)+"&scr="+urllib.quote_plus(scr)+"&fan="+urllib.quote_plus(imgfan)+"&show="+urllib.quote_plus(name2)+"&cat="+urllib.quote_plus(category)
	return u
##print sys.argv[0]
##print sys.argv[1]
##print sys.argv[2]
### ############################################################################################################
### ############################################################################################################
def FAVS():
  saved_favs = cache.get('favourites_')
  erNoFavs='XBMC.Notification([B][COLOR orange]Favorites[/COLOR][/B],[B]You have no favorites saved.[/B],5000,"")'
  if not saved_favs:
    xbmc.executebuiltin(erNoFavs)
  if saved_favs == '[]':
    xbmc.executebuiltin(erNoFavs)
  if saved_favs:
    favs = sorted(eval(saved_favs), key=lambda fav: fav[0])#favs = eval(saved_favs)
    for fav in favs:
    	if (metaArt_DoCheck(fav[0])==True):
    		if (debugging==True): print fav[0] + ' found in cached metaArt Data.'
    		thetvdb_data=metaArt_getCache(fav[0])
    		cio=class_itmOBJ()
    		cio['Plot']=ParseDescription(thetvdb_data[6])
    		cio['Status']=thetvdb_data[8]
    		cio['image_fanart']=thetvdb_data[3] #fav[3]
    		cio['image_banner']=thetvdb_data[5]
    		cio['image_thumbnail']=thetvdb_data[4] #fav[2]
    		cio['id_show']=thetvdb_data[1]
    		cio['Language']=thetvdb_data[9]
    		cio['Network']=thetvdb_data[10]
    		cio['Genres']=thetvdb_data[7]
    		cio['Rating']=thetvdb_data[11]
    		cio['Votes']='Unknown'
    		cio['Date_Released']='Unknown'
    		cio['Type']='Anime' #'Dubbed Anime'
    		cio['label_title']=fav[0]
    		cio['name']=fav[0]
    		cio['url']=fav[1]
    		cio['mode']=fav[5]
    		cio['type2']=fav[4]
    		cio['name2']=fav[0]
    		cio['show']=fav[0]
    		cio['category']=fav[0]
    		#cio['']=
    		#cio['']=
    		#cio['']=
    		## addDirD(name,name2,url,type2,mode,iconimage,fanimage,doSorting=False,categoryA='Blank',Labels='none')
    		mm=make_item_show(cio)
    	else: 
    		cio=class_itmOBJ()
    		cio['Plot']=''; cio['Status']=''; cio['image_fanart']=fav[3]; cio['image_banner']=''; cio['image_thumbnail']=fav[2]; cio['id_show']=''; cio['Language']='Unknown'; cio['Network']='Unknown'; cio['Genres']='Unknown'; cio['Rating']='Unknown'; cio['Votes']='Unknown'; cio['Date_Released']='Unknown'; cio['Type']='Anime'; cio['label_title']=fav[0]; cio['name']=fav[0]; cio['url']=fav[1]; cio['mode']=fav[5]; cio['type2']=fav[4]; cio['name2']=fav[0]; cio['show']=fav[0]; cio['category']=fav[0]
    		mm=make_item_show(cio)
    		#try:
    		#	addDirD("%s" % fav[0],fav[0],fav[1],fav[4],fav[5],fav[2],fav[3])
    		#except:
    		#	#addDirD("%s" % fav[0].upper(),fav[0],fav[1],1,6,artPath + ICON0,fanart0)
    		#	continue
  set_view('tvshows',int(getset('viewmode-favs')),False)
### ############################################################################################################
### ############################################################################################################
def check_cmd(special_command=favcmd,url=url, urlbac=urlbac, name=name, name2=name2, type2=type2, favcmd=favcmd, mode=mode, scr=scr, imgfan=imgfan, show=show, category=category):
	#notification('Special Command',special_command)
	if (url is not None) and (url is not '') and (debugging==True): print "url: "+url
	if (special_command is not None) and (special_command is not '') and (debugging==True): print 'Special Command: '+special_command
	if favcmd=='add':
		##s='[B][COLOR yellowgreen]@[/COLOR][/B] '
		##e='[COLOR black]@[/COLOR] '
		if (debugging==True): print "name: "+name
		if ('[/COLOR] ' in name): name = name.split('[/COLOR] ')[1]
		if ('[/COLOR]' in name): name = name.split('[/COLOR]')[1]
		addfavorite(name,url,scr,imgfan,type2,mode)
	elif favcmd=='rem':
		if ('[/COLOR] ' in name): name = name.split('[/COLOR] ')[1]
		if ('[/COLOR]' in name): name = name.split('[/COLOR]')[1]
		removefavorite(name,url,scr,imgfan,type2,mode)
	elif favcmd=='clr': emptyFavorites()
	elif favcmd=='showurl': showurl(name,url,scr,imgfan)
	elif favcmd=='download':
		download_file_prep(url,name,name2,show)
		#download_file(url,name)
	elif favcmd=='metaclear': metaArt_empty()
	elif favcmd=='visitedclear': visited_empty()
	elif favcmd=='showtextwindow2': TextBox2().load_file(url,name2)
	elif favcmd=='showtextwindow':
		#TextBox_FromUrl().load(url,name2)
		TextBox2().load_url(url,name2)
		##xbmc.executebuiltin("XBMC.Container.Refresh")
	elif favcmd=='showsettingwindow': __settings__.openSettings()
	elif favcmd=='metachangeshowname': metachange__Show_Name(name2)
	else:
		if (debugging==True): print u_get()
		visited_add(u_get()) ## Marks the current plugin url as having been visited.
		check_mode(mode) ## Mode to determine what Command(s) or Menu to do.
### ############################################################################################################
### ############################################################################################################
def check_mode(_mode_=mode):
	if (url is not None) and (url is not '') and (debugging==True): print "url: "+url
	#if (mode==None) or (url==None) or (len(url)<1): menu0()
	if (mode==None): menu0_MainMenu()
	elif mode==1: menu1_BrowseMethod()
	elif mode==101: menu101_Extras()
	elif mode==2: menu2()
	elif mode==201: menu201()
	#elif mode==202:
	#        CATEGORIESlistab(url)
	elif mode==211: menu211(url)
	elif mode==250: menu250()#dubbed anime
	elif mode==251: menu251()#dubbed anime
	elif mode==252: menu252_genre_list()#dubbed anime
	elif mode==253: menu253(url)#dubbed anime
	elif mode==254: EPISODESlist(url,'Dubbed')#dubbed anime
	elif mode==256: menu256_show_list(url)#dubbed anime#DAOn
	elif mode==257: menu257_episode_list(url,'Dubbed') #EPISODESlist(url,'Dubbed') #dubbed anime
	elif mode==258: menu258_list__WatchDub_com__Series_RecentAnime(url)
	elif mode==3: menu3()
	elif mode==301: menu301()
	#elif mode==302: CATEGORIESmoviesab(url)
	elif mode==311: menu311(url)
	elif mode==358: menu358_list__Name_and_Url__(url)
	elif mode==4: EPISODESlist(url)
	elif mode==5: VIDEOsource(url,name)
	elif mode==501: VIDEOsource_501(url,name)
	elif mode==6: showlist(url,mode)
	elif mode==601: showlistnames(url,mode)
	elif mode==400: searchwindow(SiteNames[type2],SiteSearchMethod[type2],SiteSearchUrls[type2],mode,type2,name2,url)
	elif mode==888: FAVS()
	elif mode==999: downloadfile(url,name)
	elif mode==1800: search_for_airdates()
	elif mode==1801: search_for_airdates(name)
	elif mode==1900: primewire_links(url,name)
	elif mode==1901: download_it_now(url,name) ## Mode for use when wanting to download a file. This can be directed from another plugin.
	elif mode==1902: download_it_now(url,name2) ## Mode for use when wanting to download a file. This can be directed from another plugin.
	elif mode==1990: xbmc.executebuiltin('XBMC.RunPlugin(plugin://plugin.video.youtube/?action=play_video&videoid=%s)' % url)
### ############################################################################################################
### ############################################################################################################
### ############################################################################################################
### ############################################################################################################
### ############################################################################################################


check_cmd(favcmd) ## Special Command Structure to override mode commands.
#check_mode(mode) ## Mode to determine what Command(s) or Menu to do. ## This has been moved into the end of the check_cmd() function.

page_last_update() ## Marks this as the last page visited after having done nearly everything else.
if (favcmd==None) or (favcmd==''): xbmcplugin.endOfDirectory(int(sys.argv[1]))
### ############################################################################################################
### ############################################################################################################
### ############################################################################################################
### ############################################################################################################
### ############################################################################################################
