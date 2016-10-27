### ############################################################################################################
###	#	
### # Project: 			#		videolinks - by The Highway 2013.
### # Author: 			#		The Highway
### # Version:			#		1.x (ever changing)
### # Description: 	#		My collection of tools for metadata and video url parsing.
###	#	              #		Meant for direct AddLink'ing.
###	#	
### ############################################################################################################
### ############################################################################################################
__plugin__	=	"The Anime Highway"
__authors__	=	"The Highway"
plugin_id		=	"plugin.video.codelyokoevolution"
### ############################################################################################################
### ############################################################################################################
import xbmc,xbmcplugin,xbmcgui,xbmcaddon,xbmcvfs
try: import urlresolver
except: t=''
import urllib,urllib2,re,os,sys,socket,string,StringIO,logging,random,array
import teh_tools
from teh_tools import *
try: import json
except ImportError: import simplejson as json
try: import StorageServer
except: import storageserverdummy as StorageServer
try: 		from t0mm0.common.addon 				import Addon
except: from t0mm0_common_addon 				import Addon
#import SimpleDownloader as downloader
### ############################################################################################################
### ############################################################################################################
cache						=	StorageServer.StorageServer(plugin_id)
addon						=	Addon(plugin_id, sys.argv)
local						=	xbmcaddon.Addon(id=plugin_id)
__settings__		=	xbmcaddon.Addon(id=plugin_id)
__home__				=	__settings__.getAddonInfo('path')
addonPath				=	__settings__.getAddonInfo('path')
artPath					=	addonPath+'/art/'	#special://home/addons/plugin.video.theanimehighway/art
#if __settings__.getSetting("enable-debug") == "true":debugging=True				#if (debugging==True): 
#else: debugging=False
#if __settings__.getSetting("show-debug") == "true": shoDebugging=True			#if (showDebugging==True): 
#else: shoDebugging=False
params=get_params()
ICON = os.path.join(__home__, 'icon.jpg')
fanart = os.path.join(__home__, 'fanart.jpg')

_addon=Addon(plugin_id, sys.argv);
_setting={}; _setting['debug-enable']=	_debugging			=tfalse(addst("debug-enable")); _setting['debug-show']	=	_shoDebugging		=tfalse(addst("debug-show"))
debugging=_debugging; shoDebugging=_shoDebugging

### ############################################################################################################
### ############################################################################################################
SiteNames=['nosite','[COLOR blue][COLOR white]Anime[/COLOR]Get[/COLOR]','[COLOR red][COLOR white]Anime[/COLOR]44[/COLOR]','[COLOR darkblue][COLOR white]Anime[/COLOR]Plus[/COLOR]','[COLOR grey]Good[COLOR white]Drama[/COLOR][/COLOR]','[COLOR maroon][COLOR white]Anime[/COLOR]Zone[/COLOR]','[COLOR teal]Dubbed[COLOR white]Anime[/COLOR]On [/COLOR]','[COLOR cornflowerblue][COLOR white]dub[/COLOR]happy[/COLOR]','[COLOR cornflowerblue]Watch[/COLOR][COLOR white]Dub[/COLOR]','','']
SiteBits=['nosite','animeget.com','anime44.com','animeplus.tv','gooddrama.net','anime44.co.uk','dubbedanimeon.com','dubhappy.eu','watchdub.com']
MyVideoLinkSrcMatches=['src="(.+?)"',			'<iframe.+?src="(.+?)"',			'<iframe.+?src="(.+?)"',			'<iframe.+?src="(.+?)"',			'<iframe.+?src="(.+?)"',			'<iframe.+?src="(.+?)"',			'<iframe.+?src="(.+?)"'			,'src="(.+?)"'		,'src="(.+?)"',		'src="(.+?)"']
MyVideoLinkSrcMatchesB=['src="(.+?)"',			'<embed.+?src="(.+?)"',			'<iframe.+?src="(.+?)"',			'<iframe.+?src="(.+?)"',			'<iframe.+?src="(.+?)"',			'<iframe.+?src="(.+?)"',			'<iframe.+?src="(.+?)"'			,'src="(.+?)"'		,'src="(.+?)"',		'src="(.+?)"']
MyVideoLinkBrackets=['<iframe.+?src="(.+?)"', '<embed.+?src="(.+?)"', '<object.+?data="(.+?)"','<EMBED src="(.+?)"',"<a .+?open_win\('(.+?)'\).+?>.+? .+?</a>"]
MyAlphabet=	['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
MyBrowser=	['User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3']
MySourcesV=		['videoweed.es',	'video44.net',	'novamov.com',	'dailymotion.com',	'videofun.me',	'yourupload.com',	'video.google.com',	'vidzur.com',	'upload2.com','putlocker.com','videoslasher.com','vidbull.com',		'uploadc.com',	'veevr.com',	'rutube.ru',	'trollvid.net',	'verilscriptz.com',	'vidup.org','veoh.com',	'megavideo.com',	'vbox7.com','mp4upload.com','zshare.net',	'stagevu.com','youtube.com',	'videobam.com',	'videonest.net','auengine.com',	'vimeo.com','videolog.tv','4shared.com']
MyIconsV=		[artPath + 'videoweed.jpg',	artPath + 'video44a.png',	artPath + 'novamov.jpg',	artPath + 'dailymotion.jpg',	artPath + 'videofun.png',	artPath + 'yourupload.jpg',	artPath + 'googlevideo.gif', artPath + 'vidzur.png', artPath + 'upload2.png', artPath + 'putlocker.png', artPath + 'preview.png', artPath + 'preview.png', artPath + 'preview.png', artPath + 'preview.png', artPath + 'preview.png', artPath + 'preview.png', artPath + 'preview.png', artPath + 'preview.png', artPath + 'trollvid_net.png',artPath + 'preview.png', artPath + 'preview.png', 'http://www.mp4upload.com/images/pic2.jpg', artPath + 'preview.png', artPath + 'preview.png', artPath + 'youtube.png', artPath + 'preview.png', artPath + 'preview.png', artPath + 'preview.png', artPath + 'preview.png', artPath + 'preview.png', artPath + 'preview.png', artPath + 'preview.png', artPath + 'preview.png', artPath + 'preview.png', artPath + 'preview.png']#BLANK.png
MyNamesV=		['VideoWeed',			'Video44',			'NovaMov',			'DailyMotion',			'VideoFun',			'YourUpload',				'Google Video',			'VidZur',			'Upload2',		'PutLocker',		'VideoSlasher',		'VidBull',				'UploadC',			'Veevr',			'RuTube',			'TrollVid',			'VerilScriptz',			'VidUp',		'Veoh',			'MegaVideo',			'VBox7',		'MP4Upload',		'ZShare',			'StageVu',		'YouTube',			'VideoBam',			'VideoNest',		'AUEngine',			'Vimeo',		'VideoLog.tv','4Shared',				'',				'',				'','']
MyColorsV=	['lime',					'red',					'silver',				'green',						'cyan',					'deepskyblue',			'blue',							'orange',			'lightsalmon','lightsteelblue',	'linen',				'magenta',				'limegreen',		'khaki',			'lemonchiffon','lawngreen', 	'white', 						'white', 		'white', 		'white', 					'white', 		'pink', 				'white', 			'white', 			'red', 					'white', 				'white', 				'white', 				'white', 		'white', 			'white', 			'white', 			'white']
### ############################################################################################################
### ############################################################################################################
def metaArt_DoCheck(nameToCheck,s=True,e=False):
	mc=metaArt_check(nameToCheck)
	if (mc==True): return s
	else: return e
def metaArt_check(nameToCheck):
  try: saved_metaArts = cache.get('MetaArt_')
  except: return False
  ##erNoFavs='XBMC.Notification([B][COLOR orange]Favorites[/COLOR][/B],[B]You have no favorites saved.[/B],5000,"")'
  if not saved_metaArts: return False ##xbmc.executebuiltin(erNoFavs)
  if saved_metaArts == '[]': return False ##xbmc.executebuiltin(erNoFavs)
  if saved_metaArts:
  	metaArts = eval(saved_metaArts)
  	#if (nameToCheck in metaArts): return True
  	for metaArt in metaArts:
  		if (nameToCheck==metaArt[0]) or (nameToCheck==metaArt[1]): return True
  return False
def metaArt_getCache(nameToCheck):
  tn = ('none','none','none','none','none','none','none','none','none','none','none','none')
  try: saved_metaArts = cache.get('MetaArt_')
  except: return tn
  ##erNoFavs='XBMC.Notification([B][COLOR orange]Favorites[/COLOR][/B],[B]You have no favorites saved.[/B],5000,"")'
  if not saved_metaArts: return tn ##xbmc.executebuiltin(erNoFavs)
  if saved_metaArts == '[]': return tn ##xbmc.executebuiltin(erNoFavs)
  if saved_metaArts:
  	metaArts = eval(saved_metaArts)
  	#if (nameToCheck in metaArts):
  	for metaArt in metaArts:
  		if (nameToCheck==metaArt[0]) or (nameToCheck==metaArt[1]):#0=given show_title , 1=gotten show_title from thetvdb.com
  			return (metaArt[0],metaArt[2],metaArt[3],metaArt[4],metaArt[5],metaArt[6],metaArt[7],metaArt[8],metaArt[9],metaArt[10],metaArt[11],metaArt[12])
  			#try:
  			#	return (metaArt[0],metaArt[2],metaArt[3],metaArt[4],metaArt[5],metaArt[6],metaArt[7],metaArt[8],metaArt[9],metaArt[10],metaArt[11],metaArt[12])
  			#except: continue
  return tn
def metaArt_get(show_name,show_id='none',url_thetvdb='none',show_fanart='none',show_poster='none',show_banner='none',show_desc='none'): #,get_which=3): #0=name,1=id,2=url_for_showhpage(thetvdb.com),3=fanart_url,4=poster_url,5=banner_url
  if ' - Movie' in show_name: show_name=show_name.replace(' - Movie','')
  if ': Movie' in show_name: show_name=show_name.replace(': Movie','')
  if ' Movie' in show_name: show_name=show_name.replace(' Movie','')
  saved_fans = cache.get('MetaArt_')
  erNoFans='XBMC.Notification([B][COLOR orange]MetaArt: [/COLOR]'+show_name+'[/B],[B]You have no MetaArt saved.[/B],5000,"")'
  fanart_found=False
  fanart_item='none'
  if not saved_fans: xbmc.executebuiltin(erNoFans)
  if saved_fans == '[]': xbmc.executebuiltin(erNoFans)
  if saved_fans:
    #fans = sorted(eval(saved_fans), key=lambda fan: fan[0])#favs = eval(saved_favs)
    fans = eval(saved_fans)
    for fan in fans:
    	if (show_name==fan[0]) or (show_name==fan[1]):#0=given show_title , 1=gotten show_title from thetvdb.com
    		try:
    			#notification('[B][COLOR orange]Metadata: '+fan[0]+'[/COLOR][/B]','[B] Data has been found in cache.[/B]')
    			fanart_item=(fan[0],fan[2],fan[3],fan[4],fan[5],fan[6],fan[7],fan[8],fan[9],fan[10],fan[11],fan[12])
    			fanart_found=True
    		except:
    			continue
  if fanart_found==False:
  	match_showname,match_showid,match_thetvdb_url,match_fanart,match_poster,match_banner,match_desc,match_genres,match_status,match_language,match_network,match_rating=thetvdb_com(show_name)#,'0','Fan Art')
  	if match_desc=='none': match_desc=show_desc.strip()
  	if show_fanart=='none': show_fanart=show_desc
  	if show_poster=='none': show_poster=show_desc
  	if show_banner=='none': show_banner=show_desc
  	if (match_showname=='none') or (match_showid=='none') or (match_thetvdb_url=='none') or (match_fanart=='none') or (match_poster=='none') or (match_banner=='none') or (match_desc=='none'):
  		fanart_item=(show_name,show_id,url_thetvdb,show_fanart,show_poster,show_banner,show_desc,match_genres,match_status,match_language,match_network,match_rating)
  	else:
  		metaArt_add(show_name,match_showname,match_showid,match_thetvdb_url,match_fanart,match_poster,match_banner,match_desc,match_genres,match_status,match_language,match_network,match_rating)
  		fanart_item=(match_showname,match_showid,match_thetvdb_url,match_fanart,match_poster,match_banner,match_desc,match_genres,match_status,match_language,match_network,match_rating)
  #else:
  #	fanart_item
  return fanart_item
  set_view('none',504)
def thetvdb_com(show_name,show_id='none',graphic_type='fanart'):
	if (debugging==True): print 'testing thetvdb_com'
	if (debugging==True): print 'showname: '+show_name
	if (debugging==True): print 'showid: '+show_id
	if (debugging==True): print 'graphic type: '+graphic_type
	if (show_id=='none') or (show_id=='0'):
		match=thetvdb_com_search(show_name,show_id)
		#if (debugging==True): print match
		match_showurl,match_name,match_genres,match_status,match_language,match_network,match_rating=match #.group()
		if (debugging==True): print 'match_name: '+match_name
		#### url, name, genres, status, language, network, rating
		#=getURL('http://thetvdb.com'+match_showurl).group()
		if match_showurl=='none': return ('none','none','none','none','none','none','none','none','none','none','none','none')
		match_showurl=urllib.unquote_plus('http://thetvdb.com'+match_showurl)
		if ('&amp;' in match_showurl): match_showurl=match_showurl.replace('&amp;','&')
		#if (debugging==True): print match_showurl
		match_id=re.compile('&id=(.+?)&').findall(match_showurl)[0]
		#match_name,match_language,match_id
		##<h1>Fan Art</h1>
		dat_a=getURL(match_showurl) #.group()
		#if ('/banners/_cache/topfanart/0.jpg' in dat_a): return ('none','none','none','none','none','none','none','none','none','none','none','none')
		#if (debugging==True): print dat_a
		dat_b=(dat_a.split('<h1>Fan Art</h1>')[1]).split('</table>')[0]
		if ('View Full Size' in dat_b):
			match_graphicURL=re.compile('<tr><td></td><td align=right><a href="(.+?)" target="_blank">View Full Size</a></td></tr>').findall(dat_b)[0]
			match_graphicURL='http://thetvdb.com/'+match_graphicURL
		else: match_graphicURL='none'
		#
		dat_c=(dat_a.split('<h1>Posters</h1>')[1]).split('</table>')[0]
		if ('View Full Size' in dat_c):
			match_posterURL=re.compile('<tr><td></td><td align=right><a href="(.+?)" target="_blank">View Full Size</a></td></tr>').findall(dat_c)[0]
			match_posterURL='http://thetvdb.com/'+match_posterURL
		else: match_posterURL='none'
		#
		dat_d=(dat_a.split('<h1>Banners</h1>')[1]).split('</table>')[0]
		if ('View Full Size' in dat_d):
			match_bannerURL=re.compile('<tr><td></td><td align=right><a href="(.+?)" target="_blank">View Full Size</a></td></tr>').findall(dat_d)[0]
			match_bannerURL='http://thetvdb.com/'+match_bannerURL
		else: match_bannerURL='none'
		#match_results=(show_name,match_id,match_showurl,match_graphicURL,match_posterURL,match_bannerURL)
		try: match_Desc=((dat_a.split('<h1>'+match_name+'</h1>')[1]).split('</div>')[0]).strip()
		except: match_Desc='none'
		if (match_Desc==''): match_Desc='none'
		if (debugging==True): print 'match_Desc: '+match_Desc
		match_results=(show_name,match_id,match_showurl,match_graphicURL,match_posterURL,match_bannerURL,match_Desc,match_genres,match_status,match_language,match_network,match_rating)
		#if (debugging==True): print match_results
		return match_results
	else:
		return ('none','none','none','none','none','none','none','none','none','none','none','none') #'none'
def thetvdb_com_search(show_name,show_id='none'):
	if (debugging==True): print 'thetvdb.com show: '+show_name
	#getURL('http://thetvdb.com/?searchseriesid=&tab=listseries&function=Search&string='+urllib.quote_plus(show_name))
	#http://thetvdb.com/index.php?fieldlocation=4&language=7&genre=&year=&network=&zap2it_id=&tvcom_id=&imdb_id=&order=translation&addedBy=&searching=Search&tab=advancedsearch&seriesname=Bleach
	#http://thetvdb.com/index.php?searchseriesid=&tab=listseries&function=Search&string=
	#http://thetvdb.com/index.php?fieldlocation=2&language=7&genre=&year=&network=&zap2it_id=&tvcom_id=&imdb_id=&order=translation&addedBy=&searching=Search&tab=advancedsearch&seriesname=Angel+Beats
	if (debugging==True): print 'thetvdb.com search: '+'http://thetvdb.com/index.php?fieldlocation=2&language=7&genre=&year=&network=&zap2it_id=&tvcom_id=&imdb_id=&order=translation&addedBy=&searching=Search&tab=advancedsearch&seriesname='+urllib.quote_plus(show_name)
	link=getURL('http://thetvdb.com/index.php?fieldlocation=2&language=7&genre=&year=&network=&zap2it_id=&tvcom_id=&imdb_id=&order=translation&addedBy=&searching=Search&tab=advancedsearch&seriesname='+urllib.quote_plus(show_name))
	if link=='none': return ('none','none','none','none','none','none','none')
	elif 'No Series found.' in link: return ('none','none','none','none','none','none','none')
	else:
		#match=re.compile('<tr><td class=".+?"><a href="(.+?)">(.+?) </a> </td><td class=".+?">(.+?)</td><td class=".+?">(.+?)</td></tr>').findall(link)[0]
		try: 
			match=re.compile('<tr><td class=".+?">.+?</td><td class=".+?"><a href="(.+?)">(.+?)</a></td><td class=".+?">(.+?)</a></td><td class=".+?">(.+?)</td><td class=".+?">(.+?)</td><td class=".+?">(.+?)</td><td class=".+?">(.+?)</td><td class=".+?">.+?</td></tr>').findall(link)[0]
			#match=(match[0],match[1],match[2],match[3],match[4],match[5],match[6])#,match[7])
		except:
			try: 
				match=re.compile('<tr><td class=".+?">.+?</td><td class=".+?"><a href="(.+?)">(.+?)</a></td><td class=".+?">(.+?)</a></td><td class=".+?">(.+?)</td><td class=".+?">(.+?)</td><td class=".+?"></td><td class=".+?">(.+?)</td><td class=".+?">.+?</td></tr>').findall(link)[0]
				match=(match[0],match[1],match[2],match[3],match[4],'none',match[5])
			except: return ('none','none','none','none','none','none','none')
		#									<tr><td class="odd">1</td><td class="odd"><a href="(url)">(title)</a></td><td class="odd">(genres)</a></td><td class="odd">(status)</td><td class="odd">(language)</td><td class="odd">(network)</td><td class="odd">(rating)</td><td class="odd">10</td></tr>
		#<tr><td class="odd">1</td><td class="odd"><a href="/index.php?tab=series&amp;id=150471&amp;lid=7">Angel Beats!</a></td><td class="odd">|Action|Adventure|Animation|Comedy|Drama|</a></td><td class="odd">Ended</td><td class="odd">English</td><td class="odd">Tokyo Broadcasting System</td><td class="odd">9</td><td class="odd">10</td></tr>
		#### url, name, genres, status, language, network, rating
		return match
	#match_showurl,match_name,match_language,match_id=match.group()
	#return (match_showurl,match_name,match_language,match_id)
	##
### ############################################################################################################
### ############################################################################################################

#def addfav(header="", message="", sleep=5000 ):
#	notify(msg=message, title=header, delay=sleep, image=ICON0)

### ############################################################################################################
### ############################################################################################################
def vvVIDEOLINKS(mainurl,name,name2='none',scr='none',imgfan='none',show='none',type2=0,mode=0):#vvVIDEOLINKS(mainurl,name,name2,scr,imgfan,show,type2,mode)
	urlA=mainurl
	link=getURL(mainurl)
	ListOfUrls=[]
	if (shoDebugging==True): 
		try: VaddDir('  [COLOR cornsilk][COLOR purple]Episode: [/COLOR]'+show+'[/COLOR]' + '[COLOR grey][/COLOR]', '', 1, ICON, fanart)
		except: t=''
	for VidLinkBrackets in MyVideoLinkBrackets:
		match=[]
		match=re.compile(VidLinkBrackets).findall(link)
		if (debugging==True): print 'Bracket Matches:',match
		ListOfUrls = ListOfUrls,match
		for url in match:
			vvVIDEOLINKS_doChecks(url,mainurl,name,name2,scr,imgfan,show,type2,mode)
	#if (debugging==True): print 'list of urls:',ListOfUrls
	#vvVIDEOLINKS_doChecks_others(ListOfUrls,0,url,mainurl,name,name2,scr,imgfan,show,type2,mode)

def vvVIDEOLINKS_doChecks(url,mainurl,name,name2='none',scr='none',imgfan='none',show='none',type2=0,mode=0):
	vvVIDEOLINKS_doChecks_videofun(4,url,mainurl,name,name2,scr,imgfan,show,type2,mode)
	vvVIDEOLINKS_doChecks_dailymotion(3,url,mainurl,name,name2,scr,imgfan,show,type2,mode)
	vvVIDEOLINKS_doChecks_videoweed(0,url,mainurl,name,name2,scr,imgfan,show,type2,mode)
	vvVIDEOLINKS_doChecks_video44(1,url,mainurl,name,name2,scr,imgfan,show,type2,mode)
	vvVIDEOLINKS_doChecks_novamov(2,url,mainurl,name,name2,scr,imgfan,show,type2,mode)
	vvVIDEOLINKS_doChecks_yourupload(5,url,mainurl,name,name2,scr,imgfan,show,type2,mode)
	vvVIDEOLINKS_doChecks_googlevideo(6,url,mainurl,name,name2,scr,imgfan,show,type2,mode)
	vvVIDEOLINKS_doChecks_vidzur(7,url,mainurl,name,name2,scr,imgfan,show,type2,mode)
	vvVIDEOLINKS_doChecks_upload2(8,url,mainurl,name,name2,scr,imgfan,show,type2,mode)
	vvVIDEOLINKS_doChecks_vidbull(11,url,mainurl,name,name2,scr,imgfan,show,type2,mode)
	vvVIDEOLINKS_doChecks_uploadc(12,url,mainurl,name,name2,scr,imgfan,show,type2,mode)
	vvVIDEOLINKS_doChecks_putlocker(9,url,mainurl,name,name2,scr,imgfan,show,type2,mode)
	vvVIDEOLINKS_doChecks_videoslasher(10,url,mainurl,name,name2,scr,imgfan,show,type2,mode)
	vvVIDEOLINKS_doChecks_veevr(13,url,mainurl,name,name2,scr,imgfan,show,type2,mode)
	vvVIDEOLINKS_doChecks_rutube(14,url,mainurl,name,name2,scr,imgfan,show,type2,mode)
	vvVIDEOLINKS_doChecks_trollvid(15,url,mainurl,name,name2,scr,imgfan,show,type2,mode)
	#vvVIDEOLINKS_doChecks_verilscriptz(16,url,mainurl,name,name2,scr,imgfan,show,type2,mode)
	vvVIDEOLINKS_doChecks_vidup(17,url,mainurl,name,name2,scr,imgfan,show,type2,mode)
	vvVIDEOLINKS_doChecks_veoh(18,url,mainurl,name,name2,scr,imgfan,show,type2,mode)
	vvVIDEOLINKS_doChecks_megavideo(19,url,mainurl,name,name2,scr,imgfan,show,type2,mode)
	vvVIDEOLINKS_doChecks_vbox7(20,url,mainurl,name,name2,scr,imgfan,show,type2,mode)
	vvVIDEOLINKS_doChecks_mp4upload(21,url,mainurl,name,name2,scr,imgfan,show,type2,mode)
	vvVIDEOLINKS_doChecks_zshare(22,url,mainurl,name,name2,scr,imgfan,show,type2,mode)
	vvVIDEOLINKS_doChecks_stagevu(23,url,mainurl,name,name2,scr,imgfan,show,type2,mode)
	vvVIDEOLINKS_doChecks_youtube(24,url,mainurl,name,name2,scr,imgfan,show,type2,mode)
	vvVIDEOLINKS_doChecks_videobam(25,url,mainurl,name,name2,scr,imgfan,show,type2,mode)
	vvVIDEOLINKS_doChecks_videonest(26,url,mainurl,name,name2,scr,imgfan,show,type2,mode)
	vvVIDEOLINKS_doChecks_auengine(27,url,mainurl,name,name2,scr,imgfan,show,type2,mode)
	vvVIDEOLINKS_doChecks_vimeo(28,url,mainurl,name,name2,scr,imgfan,show,type2,mode)
	vvVIDEOLINKS_doChecks_videologtv(29,url,mainurl,name,name2,scr,imgfan,show,type2,mode)
	vvVIDEOLINKS_doChecks_4shared(30,url,mainurl,name,name2,scr,imgfan,show,type2,mode)
	#

### ############################################################################################################
### ############################################################################################################
def vvVIDEOLINKS_doChecks_video44(tt,url,mainurl,name,name2='none',scr='none',imgfan='none',show='none',type2=0,mode=0):
	if MySourcesV[tt] in url:#video44#no-screenshot
		try:
			link=getURL(url)
			matcha=re.compile('file:\s+"(.+?)"').findall(link)
			partInfo=checkForPartNo(matcha[0])
			addLink('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + partInfo,urllib.unquote_plus(matcha[0]),scr,imgfan,show)
		except:
			VaddDir('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Error[/COLOR]', '', 1, MyIconsV[tt], fanart)
			#addLink('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]',urllib.unquote_plus(url),scr,imgfan,imgfan,show)

def vvVIDEOLINKS_doChecks_videofun(tt,url,mainurl,name,name2='none',scr='none',imgfan='none',show='none',type2=0,mode=0):
	if MySourcesV[tt] in url:#videofun.me
		if (debugging==True): print 'A Link ( ' + MySourcesV[tt] + ' ) was found: ' + url
		try:
			linka=getURL(url)
			if 'Error 404 - Not Found' not in linka:
				matcha=re.compile('url:\s+"(.+?)",\s+autoPlay:\s+true').findall(linka)#Screenshot
				linkb=getURL(matcha[0])
				matchb=re.compile('url:\s+"(.+?)",\s+autoPlay:\s+false').findall(linka)#Video
				partInfo=checkForPartNo(matchb[0])
				if (debugging==True): print matcha,matchb
				try:
					addLink('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + '  [COLOR grey][/COLOR]' + partInfo,urllib.unquote_plus(matchb[0]),matcha[0],imgfan,show)
				except:
					try:	
						addLink('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]*2[/COLOR]',matchb[0],matcha[0],imgfan,show)
					except:
						VaddDir('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Error[/COLOR]', '', 1, MyIconsV[tt], imgfan)
		except:
			VaddDir('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Error - Possible 404 Not Found.[/COLOR]', '', 1, MyIconsV[tt], imgfan)

def vvVIDEOLINKS_doChecks_dailymotion(tt,url,mainurl,name,name2='none',scr='none',imgfan='none',show='none',type2=0,mode=0):
	url=urllib.unquote_plus(url)
	if MySourcesV[tt] in url:#dailymotion ( Play: yes , Download: no )
		if ('/swf/video/' in url):
			matcha=re.compile('/video/([0-9A-Za-z]+)').findall(url)[0]
		if ('/sequence/' in url):
			matcha=re.compile('/sequence/([0-9A-Za-z]+)').findall(url)[0]
		elif 'http://www.dailymotion.com/swf/' in url:
			matcha=url.split('/swf/')[1]
			if '&' in matcha:
				try:
					matcha=re.compile('http://www.dailymotion.com/swf/(.+?)&').findall(url)[0]
				except:
					try:
						matcha=re.compile('http://www.dailymotion.com/swf/(.+?)').findall(url)[0]
					except:
						matcha=url
		elif ('/video/' in url) and ('_' in url):
			matcha=re.compile('/video/([0-9A-Za-z]+)_').findall(url)[0]
		elif ('/video/' in url):
			matcha=re.compile('/video/([0-9A-Za-z]+)').findall(url)[0]
		elif 'http://www.dailymotion.com/embed/video/' in url:
			matcha=url.split('/video/')[1]
		elif 'http://www.dailymotion.com/video/' in url:
			matcha=url.split('/video/')[1]
		#try:
		#	##if (debugging==True): print'dailymotion matcha:',matcha,url,matchaa
		#	#matcha=re.compile('http://www.dailymotion.com/swf/(.+?)&').findall(url)
		linka='http://www.dailymotion.com/video/'+matcha
		#	#addLink('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]*1a[/COLOR]',url,MyIconsV[tt],imgfan,show)
		#	#addLink('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]*1b[/COLOR]',linka,MyIconsV[tt],imgfan,show)
		linkb=getURL(linka)
		try: matchb=re.compile('var flashvars = {"(.*?)"};').findall(linkb)
		except: matchb=''
		try: datab=urllib.unquote_plus(matchb[0])###if (debugging==True): print datab
		except: datab=''
		#print datab
		try: vid_titlea=urllib.unquote_plus(re.compile('"title":"(.*?)"').findall(datab)[0]).replace('\/','/')
		except: vid_titlea=''
		try: vid_title=urllib.unquote_plus(re.compile('"videoTitle":"(.*?)"').findall(datab)[0]).replace('\/','/')
		except: vid_title=''
		try: vid_id=urllib.unquote_plus(re.compile('"videoId":"(.*?)"').findall(datab)[0]).replace('\/','/')
		except: vid_id=''
		try: vid_desc=urllib.unquote_plus(re.compile('"videoDescription":"(.*?)"').findall(datab)[0]).replace('\/','/')
		except: vid_desc=''
		try: vid_screenshot=urllib.unquote_plus(re.compile('"videoPreviewURL":"(.*?)"').findall(datab)[0]).replace('\/','/')
		except: vid_screenshot=''
		try: vid_videoauthor=urllib.unquote_plus(re.compile('"videoOwnerLogin":"(.*?)"').findall(datab)[0]).replace('\/','/')
		except: vid_videoauthor=''
		try: vid_lang=urllib.unquote_plus(re.compile('"videoLang":"(.*?)"').findall(datab)[0]).replace('\/','/')
		except: vid_lang=''
		try: vid_whenUploaded=urllib.unquote_plus(re.compile('"videoUploadDateTime":"(.*?)"').findall(datab)[0]).replace('\/','/')
		except: vid_whenUploaded=''
		try: vid_url=urllib.unquote_plus(re.compile('"video_url":"(.*?)"').findall(datab)[0]).replace('\/','/')
		except: vid_url=''
		try: vid_autoURL=urllib.unquote_plus(re.compile('"autoURL":"(.*?)"').findall(datab)[0]).replace('\/','/')
		except: vid_autoURL=''
		try: vid_ldURL=urllib.unquote_plus(re.compile('"ldURL":"(.*?)"').findall(datab)[0]).replace('\/','/')
		except: vid_ldURL=''
		try: vid_sdURL=urllib.unquote_plus(re.compile('"sdURL":"(.*?)"').findall(datab)[0]).replace('\/','/')
		except: vid_sdURL=''
		try: vid_urlOG=urllib.unquote_plus(re.compile('<meta property="og:video" content="(.+?)"').findall(linkb)[0]).replace('\/','/')
		except: vid_urlOG=''
		if (vid_screenshot==''): 
			try: vid_screenshot=urllib.unquote_plus(re.compile('<meta property="og:image" content="(.+?)"').findall(linkb)[0]).replace('\/','/')
			except: vid_screenshot=''
		try: vid_visual_science_video_view=urllib.unquote_plus(re.compile('"visual_science_video_view":"(.*?)"').findall(datab)[0]).replace('\/','/')
		except: vid_visual_science_video_view=''
		##if (debugging==True): print 'DailyMotion:',vid_url,vid_autoURL,vid_ldURL,vid_sdURL,vid_screenshot,vid_title
		try: linkc='http://www.dailymotion.com/embed/video/'+matcha
		except: linkc=''
		try: linkd=urllib.unquote_plus(getURL(linkc))
		except: linkd=''
		try: dm_live =urllib.unquote_plus(re.compile('live_rtsp_url":"(.+?)"', re.DOTALL).findall(linkd)[0]).replace('\/','/')
		except: dm_live =''
		try: dm_1080p=urllib.unquote_plus(re.compile('"stream_h264_hd1080_url":"(.+?)"', re.DOTALL).findall(linkd)[0]).replace('\/','/')
		except: dm_1080p=''
		try: dm_720p =urllib.unquote_plus(re.compile('"stream_h264_hd_url":"(.+?)"', re.DOTALL).findall(linkd)[0]).replace('\/','/')
		except: dm_720p =''
		try: dm_high =urllib.unquote_plus(re.compile('"stream_h264_hq_url":"(.+?)"', re.DOTALL).findall(linkd)[0]).replace('\/','/')
		except: dm_high =''
		try: dm_low  =urllib.unquote_plus(re.compile('"stream_h264_url":"(.+?)"', re.DOTALL).findall(linkd)[0]).replace('\/','/')
		except: dm_low  =''
		try: dm_low2 =urllib.unquote_plus(re.compile('"stream_h264_ld_url":"(.+?)"', re.DOTALL).findall(linkd)[0]).replace('\/','/')
		except: dm_low2 =''
		if (vid_screenshot==''): 
			try: vid_screenshot=urllib.unquote_plus(re.compile('"thumbnail_large_url":"(.+?)"', re.DOTALL).findall(linkd)[0]).replace('\/','/')
			except: vid_screenshot=''
		if (vid_screenshot==''): 
			try: vid_screenshot=urllib.unquote_plus(re.compile('"thumbnail_medium_url":"(.+?)"', re.DOTALL).findall(linkd)[0]).replace('\/','/')
			except: vid_screenshot=''
		if (vid_screenshot==''): 
			try: vid_screenshot=urllib.unquote_plus(re.compile('"thumbnail_url":"(.+?)"', re.DOTALL).findall(linkd)[0]).replace('\/','/')
			except: vid_screenshot=''
		deb('dm_live',dm_live)
		deb('dm_1080p',dm_1080p)
		deb('dm_720p',dm_720p)
		deb('dm_high',dm_high)
		deb('dm_low',dm_low)
		deb('dm_low2',dm_low2)
		deb('vid_urlOG',vid_urlOG)
		deb('vid_url',vid_url)
		deb('vid_autoURL',vid_autoURL)
		deb('vid_ldURL',vid_ldURL)
		deb('vid_sdURL',vid_sdURL)
		if (vid_screenshot==''): vid_screenshot=scr
		if (dm_live is not ''): 
			try: addLink('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - (dm_live) [COLOR grey][/COLOR]',dm_live,vid_screenshot,imgfan,vid_title)
			except: t=''
		if (dm_1080p is not ''): 
			try: addLink('[COLOR '+ MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - (dm_1080p) [COLOR grey][/COLOR]',dm_1080p,vid_screenshot,imgfan,vid_title)
			except: t=''
		if (dm_720p is not ''): 
			try: addLink('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - (dm_720p) [COLOR grey][/COLOR]',dm_720p,vid_screenshot,imgfan,vid_title)
			except: t=''
		if (dm_high is not ''): 
			try: addLink('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - (dm_high) [COLOR grey][/COLOR]',dm_high,vid_screenshot,imgfan,vid_title)
			except: t=''
		if (dm_low is not ''):  
			try: addLink('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - (dm_low) [COLOR grey][/COLOR]',dm_low,vid_screenshot,imgfan,vid_title)
			except: t=''
		if (dm_low2 is not ''): 
			try: addLink('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - (dm_low2) [COLOR grey][/COLOR]',dm_low2,vid_screenshot,imgfan,vid_title)
			except: t=''
		if (vid_urlOG is not '') and ('swf' not in vid_urlOG): 
			try: addLink('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - (OG) [COLOR grey][/COLOR]',vid_urlOG,vid_screenshot,imgfan,vid_title)
			except: t=''
		if (vid_url is not ''): 
			try: addLink('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - (Url) [COLOR grey][/COLOR]',vid_url,vid_screenshot,imgfan,vid_title)
			except: t=''
		#if (vid_autoURL is not ''): 
		#	try: addLink('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - (AutoUrl) [COLOR grey][/COLOR]',vid_autoURL,vid_screenshot,imgfan,vid_title)# doesn't seem to work atm #
		#	except: t=''
		if (vid_ldURL is not ''): 
			try: addLink('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - (LD) [COLOR grey][/COLOR]',vid_ldURL,vid_screenshot,imgfan,vid_title)
			except: t=''
		if (vid_sdURL is not ''): 
			try: addLink('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - (SD) [COLOR grey][/COLOR]',vid_sdURL,vid_screenshot,imgfan,vid_title)
			except: t=''
		#except:
		#	VaddDir('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Error[/COLOR]', '', 1, MyIconsV[tt], fanart)

def vvVIDEOLINKS_doChecks_videoweed(tt,url,mainurl,name,name2='none',scr='none',imgfan='none',show='none',type2=0,mode=0):
	if MySourcesV[tt] in url:#videoweed#no-screenshot###Needs worked on, wont show video.
		if (debugging==True): print 'doChecks videoweed url: '+url
		try: permalinkId=(re.compile('http://www.videoweed.es/file/([0-9A-Za-z]+)', re.MULTILINE | re.IGNORECASE | re.DOTALL).findall('__'+url+'__')[0]).strip()
		except:
			try: 		permalinkId=(re.compile('http://www.videoweed.es/.+?&file=([0-9A-Za-z]+)', re.MULTILINE | re.IGNORECASE | re.DOTALL).findall('__'+url+'__')[0]).strip()
			except: permalinkId=''
		if (debugging==True): print 'doChecks videoweed permalinkId: '+permalinkId
		if (permalinkId is not ''):
			link=getURL('http://www.videoweed.es/file/'+permalinkId+'')
			try: 		flashvar_advURL=(re.compile('flashvars.advURL="(.+?)"', re.MULTILINE | re.IGNORECASE | re.DOTALL).findall(link)[0]).strip()
			except: flashvar_advURL=''
			try: 		flashvar_domain=(re.compile('flashvars.domain="(.+?)"', re.MULTILINE | re.IGNORECASE | re.DOTALL).findall(link)[0]).strip()
			except: flashvar_domain=''
			try: 		flashvar_file(re.compile('flashvars.file="([0-9A-Za-z]+)"', re.MULTILINE | re.IGNORECASE | re.DOTALL).findall(link)[0]).strip()
			except: flashvar_file=permalinkId
			try: 		flashvar_filekey=(re.compile('flashvars.filekey="(.+?)"', re.MULTILINE | re.IGNORECASE | re.DOTALL).findall(link)[0]).strip()
			except: flashvar_filekey=''
			try: 		img_id=(re.compile('<link rel="image_src" href="http://k.".DOMAIN_URL."/thumbs_weed/([0-9A-Za-z]+).flv.jpg" / >', re.MULTILINE | re.IGNORECASE | re.DOTALL).findall(link)[0]).strip()
			except: img_id=''
			if (img_id is not ''): vid_img='http://thumbs.videoweed.es/thumbs/'+img_id[2:]+'-1.jpg'
			else: 
				linki=getURL('http://www.videoweed.es/mobile/share.php?id='+permalinkId+'')
				try: 		vid_img=(re.compile('<h3><a href=".+?">.+?</a></h3>[\n]<img .+? src="(.+?)".+?></img>', re.MULTILINE | re.IGNORECASE | re.DOTALL).findall(linki)[0]).strip()
				except: vid_img=MyIconsV[tt]
			if (debugging==True): print 'doChecks videoweed vid_img: '+vid_img
			if (flashvar_file=='') or (flashvar_file==None): flashvar_file=permalinkId
			if (flashvar_advURL is not '') and (flashvar_advURL is not '0'):
				partInfo=checkForPartNo(flashvar_advURL)
				vid_url=urlresolver.resolve(flashvar_advURL)
				try: 		addLink('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR] ' + partInfo,vid_url,scr,imgfan,show)
				except: VaddDir('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Error[/COLOR]', '', 1, MyIconsV[tt], fanart)
			elif (flashvar_domain is not '') and (flashvar_file is not '') and (flashvar_filekey is not ''):
				### url=http://s32.videoweed.es/dl/f326bbb9270cb5884b4529da5a2ada5c/51fc885a/ff7bbc3432b8fe81cc36ba564d099ca60f.flv&title=%26asdasdas&site_url=http://www.videoweed.es/file/c2piwuc52mgvp&seekparm=&enablelimit=0
				try:		linka=getURL(flashvar_domain+'/api/player.api.php?user=undefined&codes=1&file='+flashvar_file+'&pass=undefined&key='+flashvar_filekey)
				except: linka=''
				try: 		vid_url=(re.compile('url=(.+?)&', re.MULTILINE | re.IGNORECASE | re.DOTALL).findall('__'+linka+'__')[0]).strip()
				except: vid_url=''
				if (debugging==True): print 'doChecks videoweed api_url: '+flashvar_domain+'/api/player.api.php?user=undefined&codes=1&file='+flashvar_file+'&pass=undefined&key='+flashvar_filekey
				if (debugging==True): print 'doChecks videoweed vid_url: '+vid_url
				if (vid_url is not ''):
					try: 		
						addLink('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' [COLOR grey][/COLOR]',vid_url,vid_img,fanart,show); return
					except: 
						try: 
							addLink('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' [COLOR grey][/COLOR]',vid_url,ICON,fanart,show); return
						except: t=''
			VaddDir('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Error[/COLOR]', '', 1, MyIconsV[tt], fanart)
		VaddDir('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Error - No Perm. ID[/COLOR]', '', 1, MyIconsV[tt], fanart)

#		#VaddDir('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Error[/COLOR]', '', 1, MyIconsV[tt], fanart)
#		vid_url=''
#		try: link=getURL(url)
#		except: link=''
#		if (link is not '') and (link is not None) and (link is not 'none')
#			try: 
#				matcha=re.compile('flashvars.advURL="(.+?)"').findall(link)[0]
#				partInfo=checkForPartNo(matcha)
#				vid_url=urlresolver.resolve(matcha)
#			except: 
#				partInfo=''; vid_url=''
#			try: 		addLink('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR] ' + partInfo,vid_url,scr,imgfan,show)
#			except: VaddDir('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Error[/COLOR]', '', 1, MyIconsV[tt], fanart)

def vvVIDEOLINKS_doChecks_novamov(tt,url,mainurl,name,name2='none',scr='none',imgfan='none',show='none',type2=0,mode=0):
	if MySourcesV[tt] in url:#novamov#no-screenshot
		linka=getURL(url)
		if 'This file was Deleted' in linka:
			VaddDir('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Error: File was Deleted[/COLOR]', '', 1, MyIconsV[tt], imgfan)
		if 'The file has failed to convert!' in linka:
			VaddDir('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Error: File Failed to Convert[/COLOR]', '', 1, MyIconsV[tt], imgfan)
		else:
			if '&amp;' in url: url = urllib.unquote_plus(url)
			if '&amp;' in url: url = url.replace('&amp;','&')
			#matchb=url
			#if '&http:' in url:
			#	matcha=url.split('&http:')
			#	#if (debugging==True): print url,matcha
			#	matcha[1]='http:'+matcha[1]
			#	matchb=url.split('&v=')
			#	matcha[0]=matcha[0]+'&v='+matchb[1]
			#else:
			#	try: re.compile('&v=(.+?)&').findall(url)
			#	except: test=''
			linka=getURL(url)
			fil_nam=re.compile('flashvars.file="(.+?)"').findall(linka)[0]
			fil_key=re.compile('flashvars.filekey="(.+?)"').findall(linka)[0]
			linkb = 'http://www.novamov.com/api/player.api.php?key=%s&file=%s' % (fil_key, fil_nam)
			linkc=getURL(linkb)
			if 'The video no longer exists' in linkc:
				VaddDir('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Error: File was Deleted.[/COLOR]', '', 1, MyIconsV[tt], imgfan)
			else:
				#if (debugging==True): print 'linkb_c: ',linkb,linkc,url,linka
				fil_match=re.compile('url=(.+?)&title').findall(linkc)
				fil_url=fil_match[0]
				#if (debugging==True): print 'fil_url: ',fil_url #,linkb,linkc
				fil_url=urllib.unquote_plus(fil_url)
				try:
					#addLink('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' [COLOR grey][/COLOR]','http://www.novamov.com/video/' + matchb[1],scr,imgfan,show)#(N/A) NovaMov Page
					addLink('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' [COLOR grey][/COLOR]',fil_url,scr,imgfan,show)#(N/A) NovaMov Page
					#addLink('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey](N/A) Combined Link[/COLOR]',urlresolver.resolve(url),scr,imgfan,show)
					#addLink('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey](N/A) 718x420[/COLOR]',urlresolver.resolve(matcha[0]),scr,imgfan,show)
					#addLink('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey](N/A) 600x480[/COLOR]',urlresolver.resolve(matcha[1]),scr,imgfan,show)
					#VaddDir('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Error[/COLOR]', url, 1, MyIconsV[tt], fanart)
				except:
					try:
						addLink('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]*2[/COLOR]',fil_url,scr,imgfan,show)#MyIconsV[tt])
					except:
						VaddDir('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Error[/COLOR]', '', 1, MyIconsV[tt], fanart)

def vvVIDEOLINKS_doChecks_yourupload(tt,url,mainurl,name,name2='none',scr='none',imgfan='none',show='none',type2=0,mode=0):
	if MySourcesV[tt] in url:#yourupload
		linka=getURL(url)
		try:
			matcha=re.compile('&image=(.+?)&logo.file').findall(linka)
			matchb=re.compile('flashvars="id=.+?&file=(.+?)&image').findall(linka)
			addLink('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]',urllib.unquote_plus(matchb[0]),urllib.unquote_plus(matcha[0]),imgfan,show)#MyIconsV[tt])
		except:#failed at initial link
			try:
				#linkb=getURL(matcha[0])
				matcha=re.compile('<meta property="og:image" content="(.+?)"').findall(linka)
				matchb=re.compile('<meta property="og:video" content="(.+?)"').findall(linka)
				try:
					addLink('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey](Some lack time-seeking)[/COLOR]',matchb[0],matcha[0],imgfan,show)
				except:#failed @ og:video
					matchc=re.compile('&logo.link=(.+?)&logo.linktarget').findall(linka)
					try:
						addLink('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]*3[/COLOR]',unquote_plus(matchc[0]),matcha[0],imgfan,show)
					except:#failed @ logo.link
						VaddDir('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Error - Failed @  logo.link[/COLOR]', '', 1, MyIconsV[tt],imgfan)
			except:
				try:
					matcha=re.compile(",'image':\s+'(.+?)'").findall(linka)
					matchb=re.compile(",'file':\s+'(.+?)'").findall(linka)
					try:
						addLink('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]*2 Might be slow loading.[/COLOR]',matchb[0],matcha[0],imgfan,show)
					except:#failed @ og:video
						VaddDir('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Error - Failed @  File Not Found.[/COLOR]', '', 1, MyIconsV[tt],imgfan)
				except: 
					VaddDir('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Error - Failed @  File Not Found.[/COLOR]', '', 1, MyIconsV[tt],imgfan)
				#VaddDir('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Error - Failed @  File Not Found.[/COLOR]', '', 1, MyIconsV[tt],imgfan)

def vvVIDEOLINKS_doChecks_googlevideo(tt,url,mainurl,name,name2='none',scr='none',imgfan='none',show='none',type2=0,mode=0):
	if MySourcesV[tt] in url:#google video
		try:
			addLink('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]',urllib.unquote_plus(url),scr,imgfan,show)#MyIconsV[tt])
		except:
			try:
				addLink('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]*2[/COLOR]',urllib.unquote_plus(url),scr,imgfan,show)#MyIconsV[tt])
			except:
				VaddDir('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Error[/COLOR]', '', 1, MyIconsV[tt], fanart)

def vvVIDEOLINKS_doChecks_vidzur(tt,url,mainurl,name,name2='none',scr='none',imgfan='none',show='none',type2=0,mode=0):
	if MySourcesV[tt] in url:#vidzur#no-screenshot
		linka=getURL(url)
		matchb=re.compile("playlist:\s+\[\s+\{\s+url:\s+'(.+?)'.").findall(linka)
		try:
			addLink('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + '  [COLOR grey][/COLOR]',urllib.unquote_plus(matchb[0]),scr,imgfan,show)
		except:
			try:
				addLink('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]*2[/COLOR]',matchb[0],scr,imgfan,show)
			except:#failed @ logo.link
				VaddDir('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Error[/COLOR]', '', 1, MyIconsV[tt], matchb[0])

def vvVIDEOLINKS_doChecks_upload2(tt,url,mainurl,name,name2='none',scr='none',imgfan='none',show='none',type2=0,mode=0):
	if MySourcesV[tt] in url:#upload2#no-screenshot(only image is for upload2)###unchecked so far
		linka=getURL(url)
		#matchb=re.compile("playlist:\s+\[\s+\{\s+url:\s+'(.+?)'.").findall(linka)
		video_title,video_file,rating=re.compile("&video_title=(.+?)&","&video=(.+?)&","&rating=(.+?)&").findall(linka)
		try:
			addLink('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + '  [COLOR grey][/COLOR]',matchb[0],scr,imgfan,video_title)
		except:
			try:
				addLink('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]*2[/COLOR]',matchb[0],scr,imgfan,show)
			except:#failed @ logo.link
				VaddDir('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Error[/COLOR]', '', 1, MyIconsV[tt], matcha[0])

def vvVIDEOLINKS_doChecks_videoslasher(tt,url,mainurl,name,name2='none',scr='none',imgfan='none',show='none',type2=0,mode=0):
	if MySourcesV[tt] in url:#videoslasher
		linka=getURL(url)
		if 'File Does not Exist, or Has Been Removed' in linka:
			VaddDir('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Error: File was Deleted.[/COLOR]', '', 1, MyIconsV[tt], imgfan)
		else:
			#if 'embed' in url: url=url.replace('embed','video')
			linkd = urlresolver.resolve(url) 
			#linke = urlresolver.HostedMediaFile(linkd)#.resolve()
			###http://www.videoslasher.com/video/
			try:
				addLink('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + '  [COLOR grey][/COLOR]',linkd,scr,imgfan,show)
			except:
				try:
					addLink('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]*2[/COLOR]',url,scr,imgfan,show)
				except:#failed @ logo.link
					VaddDir('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Error[/COLOR]', url, 1, MyIconsV[tt], imgfan)


def vvVIDEOLINKS_doChecks_vidbull(tt,url,mainurl,name,name2='none',scr='none',imgfan='none',show='none',type2=0,mode=0):
	#if (debugging==True): print 'checkVideoBull Link: '+url
	if MySourcesV[tt] in url:#VideoBull.com
		linka=getURL(url)
		#if (debugging==True): print 'VideoBull Link: '+url
		if 'This file was Deleted' in linka:
			VaddDir('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Error: File was Deleted.[/COLOR]', '', 1, MyIconsV[tt], imgfan)
		else:
			VaddDir('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Error: Not Supported Yet.[/COLOR]', '', 1, MyIconsV[tt], imgfan)

def vvVIDEOLINKS_doChecks_veevr(tt,url,mainurl,name,name2='none',scr='none',imgfan='none',show='none',type2=0,mode=0):
	if MySourcesV[tt] in url:#veevr.com#13
		linka=getURL(url)
		if 'This file was Deleted' in linka:
			VaddDir('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Error: File was Deleted.[/COLOR]', '', 1, MyIconsV[tt], imgfan)
		else:
			#vid_image,vid_title = re.compile('<img id="vid-thumb" src="(.+?)".+?alt="(.+?)"').findall(linka)[0]
			#if (debugging==True): print 'url: ',url
			##match_image,match_url = re.compile("playlist:.+?url: '(.+?)',.+?scaling: '.+?'.+?url: '(.+?)'").findall(linka)
			#match_image = re.compile("playlist:.+?url: '(.+?)',.+?scaling:").findall(linka)[0]
			#match_url 	= re.compile("playlist:.+?scaling:.+?url: '(.+?)'").findall(linka)[0]
			#vid_image=match_image[0]
			#vid_url=match_url[0]
			##if (debugging==True): print linka
			#vid_image = re.compile("playlist:.+?url: '(.+?)',.+?scaling:").findall(linka)[0]
			#vid_url 	= re.compile("playlist:.+?scaling:.+?url: '(.+?)'").findall(linka)[0]
			vid_image=scr
			vid_url=''
			vid_urla=''
			match=re.compile("url: '(.+?)'").findall(linka)
			for link in match:
				if '.swf' in link:
					test='' 
				else:
					if ('.jpg' in link) and ('images' in link) and ('videos' in link) and ('thumbs' in link):
						vid_image=link
					if ('token' in link) and ('file=' in link) and ('videos' in link) and ('download' in link) and (vid_urla==''):
						vid_urla=urllib.unquote_plus(link)
			vid_image=urllib.unquote_plus(vid_image)
			#vid_url=urllib.unquote_plus(vid_url)
			linkb=getURL(vid_urla)
			vid_url=re.compile('url="(.+?)"').findall(linkb)[0]
			##matcha=re.compile("addVariable\('file','(.+?)'\)").findall(linka)[0]
			##matcha=urlresolver.resolve(matcha)
			##matcha=matcha.replace(' ','%20')
			##matcha=urllib.quote_plus(matcha)
			##if (debugging==True): print 'match: ',matcha
			if (debugging==True): print url,vid_image,vid_urla,vid_url
			try:
				#addLink('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' [COLOR grey][/COLOR]',matcha,scr,imgfan,show)
				addLink('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Error: Enjoy the screenshot. Video Bugged.[/COLOR]',vid_url,vid_image,imgfan,show)
				if (shoDebugging==True): addLink('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Error: *2 Enjoy the screenshot. Video Bugged.[/COLOR]',vid_url+'Seg1-Frag1',vid_image,imgfan,show)
				if (shoDebugging==True): addLink('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Error: *1 Enjoy the screenshot. Video Bugged.[/COLOR]',vid_urla,vid_image,imgfan,show)
			except:
				VaddDir('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Error[/COLOR]', matcha, 1, MyIconsV[tt], imgfan)
			#
		### 
		### http://veevr.com/embed/kdGk7L9__
		### http://doppler.ch3.hwcdn.net/mh003c3/y2x5c2k3/ads/videos/download/a2d287cfe9694988b54cd046b5d00ff8.smil/media_b826368_w880573809.abst/Seg1-Frag1
		### #player-logo {
		###             float:right; margin-right:0; height:19px; width:100px; background:url(http://hwcdn.net/j3v8m4w2/cds/www/images/templates/logo-small.png) no-repeat;
		###         }
		### http://hwcdn.net/j3v8m4w2/cds/www/images/templates/logo-small.png
		### LR_VIDEO_ID: '325384',
		### LR_PARTNERS: '698792',
		### LR_SCAN_566_TITLE: escape('C Control S01E03 720p '),
		### LR_SCAN_566_DESCRIPTION: escape('C Control S01E03 720p '),
		### http://mps.hwcdn.net/y2x5c2k3/ads/videos/download/a2d287cfe9694988b54cd046b5d00ff8.smil/Manifest.f4m?file=mp4&bitrate=1373207457&token=4105b834ebb02c8f4e581c3e2005856d
		### http://doppler.ch3.hwcdn.net/mh003c3/y2x5c2k3/ads/videos/download/a2d287cfe9694988b54cd046b5d00ff8.smil/media_b826368_w1877115775.abst/
		### mps/videos/download/a2d287cfe9694988b54cd046b5d00ff8.smil
		### Seg1-Frag1
		### 
		### 
		### 
		### 
		### 
		### 
		### 
		### 
		### 

def vvVIDEOLINKS_doChecks_uploadc(tt,url,mainurl,name,name2='none',scr='none',imgfan='none',show='none',type2=0,mode=0):
	if MySourcesV[tt] in url:#uploadc.com
		linka=getURL(url)
		if 'This file was Deleted' in linka:
			VaddDir('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Error: File was Deleted.[/COLOR]', '', 1, MyIconsV[tt], imgfan)
		else:
			matcha=re.compile("addVariable\('file','(.+?)'\)").findall(linka)[0]
			#if (debugging==True): print 'match: ',matcha
			try:
				#addLink('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' [COLOR grey][/COLOR]',matcha,scr,imgfan,show)
				addLink('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' [COLOR grey][/COLOR]',matcha,MyIconsV[tt],imgfan,show)
			except:
				VaddDir('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Error[/COLOR]', matcha, 1, MyIconsV[tt], imgfan)


def vvVIDEOLINKS_doChecks_verilscriptz(tt,url,mainurl,name,name2='none',scr=ICON,imgfan=fanart,show='none',type2=0,mode=0):
	if MySourcesV[tt] in url:#verilscriptz
		if (debugging==True): print 'doChecks_verilscriptz - url: '+url
		try: addLink('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' [COLOR grey][/COLOR]',video_url,scr,imgfan,show)
		except: VaddDir('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Error: Needs Testing.[/COLOR]', '', 1, ICON, fanart)
		#link1=getURL(url)#verilscriptz.com
		#if ('<location>' in link1) and ('<image>' in link1):
		#	video_url=(re.compile('<location>(.+?)</location>').findall(link1)[0]).strip()
		#	video_img=(re.compile('<image>(.+?)</image>').findall(link1)[0]).strip()
		#	try: addLink('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' [COLOR grey][/COLOR]',video_url,scr,imgfan,show)
		#	except: VaddDir('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Error: Needs Testing.[/COLOR]', '', 1, ICON, fanart)

def vvVIDEOLINKS_doChecks_zshare(tt,url,mainurl,name,name2='none',scr=ICON,imgfan=fanart,show='none',type2=0,mode=0):
	if MySourcesV[tt] in url:#zshare.net
		t=''
		### Example Url: http://www.zshare.net/videoplayer/player.php?SID=dl077*FID=84728575*FN=ark%202004.flv
		### Comment: Site seems to be bessed up currently and possibly for a while. Seems like many people can't connect but yet http://www.isitdownrightnow.com/zshare.net.html says its up where-as its comments say otherwise.


def vvVIDEOLINKS_doChecks_youtube(tt,url,mainurl,name,name2='none',scr=ICON,imgfan=fanart,show='none',type2=0,mode=0):
	if MySourcesV[tt] in url:#youtube.com
		permalinkId=''
		### 'plugin://plugin.video.youtube/?action=play_video&videoid='+permalinkId
		### 
		### 
		if (debugging==True): print 'doChecks '+MyNamesV[tt]+' url: '+url
		if (permalinkId=='') and ('youtube.com/watch?' in url): #http://www.youtube.com/watch?v=8LiKT_5I_4g
			try: permalinkId=(re.compile('v=([0-9A-Za-z]+)&', re.MULTILINE | re.IGNORECASE | re.DOTALL).findall('__'+url+'&__')[0]).strip()
			except: 
				try: permalinkId=(re.compile('v=(.+?)&', re.IGNORECASE | re.DOTALL).findall('__'+url+'&__')[0]).strip()
				except: permalinkId=''
		if (permalinkId=='') and ('youtube.com/embed/' in url): #http://www.youtube.com/embed/HINaeQ5cnec
			try: permalinkId=(re.compile('youtube.com/embed/([0-9A-Za-z]+)', re.MULTILINE | re.IGNORECASE | re.DOTALL).findall('__'+url+'__')[0]).strip()
			except: permalinkId=''
		if (permalinkId=='') and ('youtube.com/feeds/api/videos/' in url): #http://gdata.youtube.com/feeds/api/videos/HINaeQ5cnec
			try: permalinkId=(re.compile('youtube.com/feeds/api/videos/([0-9A-Za-z]+)', re.MULTILINE | re.IGNORECASE | re.DOTALL).findall('__'+url+'__')[0]).strip()
			except: permalinkId=''
		if (permalinkId=='') and ('youtube.com/get_video_info?' in url): #http://www.youtube.com/get_video_info?video_id=8LiKT_5I_4g
			try: permalinkId=(re.compile('video_id=([0-9A-Za-z]+)&', re.MULTILINE | re.IGNORECASE | re.DOTALL).findall('__'+url+'&__')[0]).strip()
			except: permalinkId=''
		if (debugging==True): print 'doChecks '+MyNamesV[tt]+' permalinkId: '+permalinkId
		if (permalinkId is not ''):
			##try: 		linka=getURL('http://www.youtube.com/watch?v='+permalinkId+'')
			##except: linka=''
			##if (debugging==True): print 'doChecks '+MyNamesV[tt]+' watch url:  '+'http://www.youtube.com/watch?v='+permalinkId+''
			##if ('<h1 id="unavailable-message" class="message">' in linka):
			##	if (shoDebugging==True): VaddDir('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Error: Video is Unavailable[/COLOR]', url, 1, MyIconsV[tt], fanart)
			##	return
			##if (linka is not ''):
			##	##try: vid_img=(re.compile('"iurlsd": "http:\\/\\/i1.ytimg.com\\/vi\\/(.+?)\\/sddefault.jpg"', re.MULTILINE | re.IGNORECASE | re.DOTALL).findall(linka)[0]).strip()
			##	##except: vid_img=MyIconsV[tt]
			##	### "iurlsd": "http:\/\/i1.ytimg.com\/vi\/HINaeQ5cnec\/sddefault.jpg"
			##	### http://i1.ytimg.com/vi/HINaeQ5cnec/sddefault.jpg
			vid_img='http://i1.ytimg.com/vi/'+permalinkId+'/sddefault.jpg'
			vid_img_hd='http://i1.ytimg.com/vi/'+permalinkId+'/hqdefault.jpg'
			#vid_url=permalinkId
			vid_url='plugin://plugin.video.youtube/?action=play_video&videoid='+permalinkId
			if (debugging==True): print 'doChecks '+MyNamesV[tt]+' vid_url: '+vid_url
			if (debugging==True): print 'doChecks '+MyNamesV[tt]+' vid_img sd: '+vid_img
			if (debugging==True): print 'doChecks '+MyNamesV[tt]+' vid_img hd: '+vid_img_hd
			try: 		addLink('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' [COLOR grey][/COLOR]',vid_url,vid_img_hd,fanart,show); return
			except: addLink('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' [COLOR grey][/COLOR]',vid_url,vid_img,fanart,show); return
			#try: 			addDirD('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Use: Youtube Plugin[/COLOR]',MyNamesV[tt],vid_url,type2,1990,vid_img_hd,fanart)
			#except: 
			#	try: 		addDirD('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Use: Youtube Plugin[/COLOR]*',MyNamesV[tt],vid_url,type2,1990,vid_img,fanart)
			#	except: addDirD('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Use: Youtube Plugin[/COLOR]**',MyNamesV[tt],vid_url,type2,1990,MyColorsV[tt],fanart)
			return
			##else:
			##	if (shoDebugging==True): VaddDir('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Error: Problem Loading Embed Page[/COLOR]', url, 1, MyIconsV[tt], fanart)
		else:
			if (shoDebugging==True): VaddDir('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Error: No PermID Found[/COLOR]', url, 1, MyIconsV[tt], fanart)


def vvVIDEOLINKS_doChecks_videobam(tt,url,mainurl,name,name2='none',scr=ICON,imgfan=fanart,show='none',type2=0,mode=0):
	if MySourcesV[tt] in url:#videobam.com
		permalinkId=''
		if (debugging==True): print 'doChecks '+MyNamesV[tt]+' url: '+url
		if (permalinkId=='') and ('videobam.com/widget/' in url) and ('/custom/' in url): ### http://videobam.com/widget/XCSIO/custom/712
			try: permalinkId=(re.compile('/widget/([0-9A-Za-z]+)/custom/', re.MULTILINE | re.IGNORECASE | re.DOTALL).findall('__'+url+'__')[0]).strip()
			except: permalinkId=''
		if (debugging==True): print 'doChecks '+MyNamesV[tt]+' permalinkId: '+permalinkId
		if (permalinkId is not''):
			#vid_img='http://i.videobam.com/'+permalinkId+'_o.jpg'
			try: linka=getURL('http://videobam.com/widget/'+permalinkId+'/')
			except: linka=''
			if (linka is not '') and (linka is not 'none') and (linka is not None):
				#try: vid_img=(urllib.unquote_plus((re.compile('"url":"(.+?\.jpg)"', re.MULTILINE | re.IGNORECASE | re.DOTALL).findall(linka)[0]).strip())).replace('\/','/')
				#except: vid_img='http://i.videobam.com/'+permalinkId+'_o.jpg'
				#except: vid_img='http://i.videobam.com/'+permalinkId+'.jpg'
				#vid_img='http://i.videobam.com/'+permalinkId+'.jpg'
				vid_img=MyIconsV[tt]
				### http://i.videobam.com/XCSIO.jpg
				### http://5.lw4.videobam.com/storage/5/videos/x/xc/XCSIO/encoded.mp4/b851c9447821710efe8c9bd018af6b7e/51fcdbcd?ss=165
				### http://5.lw4.videobam.com/storage/5/videos/x/xc/XCSIO/encoded.mp4/f1f335fc6de0591f95e50c68cc2eeb90/51fce1ef?ss=565
				try: vid_url=(urllib.unquote_plus((re.compile('"scaling":"fit","url":"(.+?storage.+?)"', re.IGNORECASE).findall(linka)[0]).strip())).replace('\/','/') #+'?start=0'
				except: vid_url=''
				if (debugging==True): print 'doChecks '+MyNamesV[tt]+' vid_url: '+vid_url
				if (debugging==True): print 'doChecks '+MyNamesV[tt]+' vid_img: '+vid_img
				if (vid_url is not ''):
					#try: addLink('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' [COLOR grey][/COLOR]',vid_url,vid_img,fanart,show); return
					try: addLink('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' [COLOR grey][/COLOR]',vid_url,vid_img,fanart,show); return
					except: 
						t=''
						try:  addLink('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' [COLOR grey][/COLOR]',vid_url,ICON,fanart,show); return
						except: 
							if (shoDebugging==True): VaddDir('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Error: Needs Testing[/COLOR]', url, 1, MyIconsV[tt], fanart)
							return
				else: 
					if (shoDebugging==True): VaddDir('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Error: No Url Found[/COLOR]', url, 1, MyIconsV[tt], fanart)
					return
			else:
				if (shoDebugging==True): VaddDir('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Error: Problem Loading Embed Page[/COLOR]', url, 1, MyIconsV[tt], fanart)
				return
		if (shoDebugging==True): VaddDir('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Error: No PermID Found[/COLOR]', url, 1, MyIconsV[tt], fanart)




def vvVIDEOLINKS_doChecks_videonest(tt,url,mainurl,name,name2='none',scr=ICON,imgfan=fanart,show='none',type2=0,mode=0):
	if MySourcesV[tt] in url:#videonest.net
		permalinkId=''
		if (debugging==True): print 'doChecks '+MyNamesV[tt]+' url: '+url
		if (permalinkId=='') and ('videonest.net/embed-' in url) and ('.html' in url): ### http://www.videonest.net/embed-my28tqcjn8e7-728x455.html
			try: permalinkId=(re.compile('videonest.net/embed-([0-9A-Za-z]+)-\d+x\d+.html', re.MULTILINE | re.IGNORECASE | re.DOTALL).findall('__'+url+'__')[0]).strip()
			except: ### http://www.videonest.net/embed-my28tqcjn8e7.html
				try: permalinkId=(re.compile('videonest.net/embed-([0-9A-Za-z]+).html', re.MULTILINE | re.IGNORECASE | re.DOTALL).findall('__'+url+'__')[0]).strip()
				except: permalinkId=''
		if (permalinkId=='') and ('videonest.net/' in url): ### 
			try: permalinkId=(re.compile('videonest.net/([0-9A-Za-z]+)_', re.MULTILINE | re.IGNORECASE | re.DOTALL).findall('__'+url+'__')[0]).strip()
			except: permalinkId=''
		if (debugging==True): print 'doChecks '+MyNamesV[tt]+' permalinkId: '+permalinkId
		if (permalinkId is not''):
			try: linka=getURL('http://www.videonest.net/embed-'+permalinkId+'.html')
			except: linka=''
			if (debugging==True): print 'http://www.videonest.net/embed-'+permalinkId+'.html'
			if (linka is not '') and (linka is not 'none') and (linka is not None):
				try: vid_img=(re.compile("'image': '(.+?\.jpg)'", re.MULTILINE | re.IGNORECASE | re.DOTALL).findall(linka)[0]).strip()
				except: vid_img=MyIconsV[tt]
				try: vid_url=(re.compile("'file': '(.+?\.mp4)'", re.IGNORECASE).findall(linka)[0]).strip() #+'?start=0'
				except: vid_url=''
				if (debugging==True): print 'doChecks '+MyNamesV[tt]+' vid_url: '+vid_url
				if (debugging==True): print 'doChecks '+MyNamesV[tt]+' vid_img: '+vid_img
				if (vid_url is not ''):
					try: addLink('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' [COLOR grey][/COLOR]',vid_url,vid_img,fanart,show); return
					except: 
						t=''
						try:  addLink('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' [COLOR grey][/COLOR]',vid_url,ICON,fanart,show); return
						except: 
							if (shoDebugging==True): VaddDir('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Error: Needs Testing[/COLOR]', url, 1, MyIconsV[tt], fanart)
							return
				else: 
					if (shoDebugging==True): VaddDir('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Error: No Url Found[/COLOR]', url, 1, MyIconsV[tt], fanart)
					return
			else:
				if (shoDebugging==True): VaddDir('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Error: Problem Loading Embed Page[/COLOR]', url, 1, MyIconsV[tt], fanart)
				return
		if (shoDebugging==True): VaddDir('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Error: No PermID Found[/COLOR]', url, 1, MyIconsV[tt], fanart)

def vvVIDEOLINKS_doChecks_auengine(tt,url,mainurl,name,name2='none',scr=ICON,imgfan=fanart,show='none',type2=0,mode=0):
	if MySourcesV[tt] in url:#auengine.com
		permalinkId=''
		if (debugging==True): print 'doChecks '+MyNamesV[tt]+' url: '+url
		if (permalinkId=='') and ('auengine.com/embed.php?' in url) and ('file=' in url): ### http://auengine.com/embed.php?file=APdFVX0k
			try: permalinkId=(re.compile('file=([0-9A-Za-z]+)&', re.MULTILINE | re.IGNORECASE | re.DOTALL).findall('__'+url+'&__')[0]).strip()
			except: permalinkId=''
		if (permalinkId=='') and ('auengine.com/' in url): ### 
			try: permalinkId=(re.compile('auengine.com/([0-9A-Za-z]+)_', re.MULTILINE | re.IGNORECASE | re.DOTALL).findall('__'+url+'__')[0]).strip()
			except: permalinkId=''
		if (debugging==True): print 'doChecks '+MyNamesV[tt]+' permalinkId: '+permalinkId
		if (permalinkId is not''):
			try: linka=getURL('http://auengine.com/embed.php?file='+permalinkId+'')
			except: linka=''
			if (debugging==True): print 'http://auengine.com/embed.php?file='+permalinkId+''
			if (linka is not '') and (linka is not 'none') and (linka is not None):
				try: vid_img=(re.compile("url:\s+'(http://s\d+.auengine.com.+?\.png)'", re.MULTILINE | re.IGNORECASE | re.DOTALL).findall(linka)[0]).strip()
				except: vid_img=MyIconsV[tt]
				try: vid_url=((re.compile("url: '(http://s\d+\.auengine\.com/videos/[0-9A-Za-z]+\.mp4\?st=.+?&e=\d+)'", re.IGNORECASE | re.DOTALL).findall(urllib.unquote_plus(linka))[0])).strip() #+'?start=0'
				#urllib.unquote_plus
				#http://s45.auengine.com/videos/APdFVX0k.mp4?st=RiJTy1rRAKS_qH-unK67-A&e=1375546972
				except: vid_url=''
				if (debugging==True): print 'doChecks '+MyNamesV[tt]+' vid_url: '+vid_url
				if (debugging==True): print 'doChecks '+MyNamesV[tt]+' vid_img: '+vid_img
				if (vid_url is not ''):
					try: addLink('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' [COLOR grey][/COLOR]',vid_url,vid_img,fanart,show); return
					except: 
						t=''
						try:  addLink('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' [COLOR grey][/COLOR]',vid_url,ICON,fanart,show); return
						except: 
							if (shoDebugging==True): VaddDir('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Error: Needs Testing[/COLOR]', url, 1, MyIconsV[tt], fanart)
							return
				else: 
					if (shoDebugging==True): VaddDir('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Error: No Url Found[/COLOR]', url, 1, MyIconsV[tt], fanart)
					return
			else:
				if (shoDebugging==True): VaddDir('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Error: Problem Loading Embed Page[/COLOR]', url, 1, MyIconsV[tt], fanart)
				return
		if (shoDebugging==True): VaddDir('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Error: No PermID Found[/COLOR]', url, 1, MyIconsV[tt], fanart)


def vvVIDEOLINKS_doChecks_stagevu(tt,url,mainurl,name,name2='none',scr=ICON,imgfan=fanart,show='none',type2=0,mode=0):
	if MySourcesV[tt] in url:#stagevu.com
		if ('&amp;' in url): url=url.replace('&amp;','&') ### http://stagevu.com/embed?width=500&amp;height=430&amp;background=3c3c3c&amp;uid=dbwwzgqilkvo
		permalinkId=''
		if (debugging==True): print 'doChecks '+MyNamesV[tt]+' url: '+url
		if (permalinkId=='') and ('?' in url): ### http://stagevu.com/embed?width=500&height=430&background=3c3c3c&uid=dbwwzgqilkvo
			try: permalinkId=(re.compile('&uid=([0-9A-Za-z]+)', re.MULTILINE | re.IGNORECASE | re.DOTALL).findall('__'+url+'__')[0]).strip()
			except: permalinkId=''
		if (permalinkId=='') and ('/video/' in url): ### http://stagevu.com/video/dbwwzgqilkvo
			try: permalinkId=(re.compile('/video/([0-9A-Za-z]+)', re.MULTILINE | re.IGNORECASE | re.DOTALL).findall('__'+url+'__')[0]).strip()
			except: permalinkId=''
		if (debugging==True): print 'doChecks '+MyNamesV[tt]+' permalinkId: '+permalinkId
		if (permalinkId is not''):
			try: linka=getURL('http://stagevu.com/embed?width=500&uid='+permalinkId+'')
			except: linka=''
			if (linka is not '') and (linka is not 'none') and (linka is not None):
				try: vid_url=(re.compile("url\[\d+\] = '(.+?)'", re.MULTILINE | re.IGNORECASE | re.DOTALL).findall(linka)[0]).strip()
				except: 
					try: vid_url=(re.compile('<param name="src" value="(.+?)" />', re.MULTILINE | re.IGNORECASE | re.DOTALL).findall(linka)[0]).strip()
					except: 
						try: vid_url=(re.compile('embed type="video/divx" src="(.+?)"', re.MULTILINE | re.IGNORECASE | re.DOTALL).findall(linka)[0]).strip()
						except: vid_url=''
				try: vid_img=(re.compile('<param name="previewImage" value="(.+?)" />', re.MULTILINE | re.IGNORECASE | re.DOTALL).findall(linka)[0]).strip()
				except: vid_img=ICON
				if (debugging==True): print 'doChecks '+MyNamesV[tt]+' vid_url: '+vid_url
				if (debugging==True): print 'doChecks '+MyNamesV[tt]+' vid_img: '+vid_img
				vid_img=ICON ### Quick Fix: stagevu screenshot is huge and doesn't seem to load as either a thumbnail or fanart in XBMC.
				if (vid_url is not ''):
					#try: addLink('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' [COLOR grey][/COLOR]',vid_url,vid_img,fanart,show); return
					try: addLink('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' [COLOR grey][/COLOR]',vid_url,vid_img,fanart,show); return
					except: 
						t=''
						try:  addLink('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' [COLOR grey][/COLOR]',vid_url,ICON,fanart,show); return
						except: t=''
				else: 
					if (shoDebugging==True): VaddDir('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Error: No Url Found[/COLOR]', url, 1, MyIconsV[tt], fanart); return
			else:
				if (shoDebugging==True): VaddDir('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Error: Problem Loading Embed Page[/COLOR]', url, 1, MyIconsV[tt], fanart); return
		if (shoDebugging==True): VaddDir('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Error: No PermID Found[/COLOR]', url, 1, MyIconsV[tt], fanart)

def vvVIDEOLINKS_doChecks_4shared(tt,url,mainurl,name,name2='none',scr=ICON,imgfan=fanart,show='none',type2=0,mode=0):
	if MySourcesV[tt] in url:#4shared.com
		permalinkId=''
		if (debugging==True): print 'doChecks '+MyNamesV[tt]+' url: '+url
		#if (permalinkId=='') and ('?' in url): ### 
		#	try: (permalinkId)=(re.compile('id=([0-9A-Za-z]+)', re.MULTILINE | re.IGNORECASE | re.DOTALL).findall('__'+url+'__')[0]).strip()
		#	except: permalinkId=''
		if (permalinkId=='') and ('4shared.com/video/' in url): ### 
			try: permalinkId=(re.compile('/video/([0-9A-Za-z]+/*[0-9A-Za-z]*)', re.MULTILINE | re.IGNORECASE | re.DOTALL).findall('__'+url+'__')[0]).strip()
			except: permalinkId=''
		if (permalinkId=='') and ('4shared.com/embed/' in url): ### 
			try: permalinkId=(re.compile('/embed/([0-9A-Za-z]+/*[0-9A-Za-z]*)', re.MULTILINE | re.IGNORECASE | re.DOTALL).findall('__'+url+'__')[0]).strip()
			except: permalinkId=''
		if (permalinkId=='') and ('static.4shared.com/flash/player/' in url) and ('4shared.com/img/' in url): ### http://stagevu.com/video/dbwwzgqilkvo
			try: permalinkId=(re.compile('/img/([0-9A-Za-z]+)/dlink__', re.MULTILINE | re.IGNORECASE | re.DOTALL).findall('__'+url+'__')[0]).strip()
			except: permalinkId=''
		### http://www.4shared.com/embed/3258682120/28a29181
		### http://static.4shared.com/flash/player/5.10/player.swf?file=http://dc301.4shared.com/img/3258682120/28a29181/dlink__2Fdownload_2FjYbVtfyK_3Ftsid_3D20130804-211137-3360aafb/preview.flv&image=http://dc407.4shared.com/img/jYbVtfyK/13c15c24a00/code_lyoko_evolution_episode_2.flv&logo.link=http://www.4shared.com/video/jYbVtfyK/code_lyoko_evolution_episode_2.html&logo.hide=false&logo.file=http://dc301.4shared.com/images/logo.png&logo.position=top-left&plugins=sharing-2&sharing-2.link=http://www.4shared.com/video/jYbVtfyK/code_lyoko_evolution_episode_2.html&sharing-2.code=%3Cembed%20src%3D%22http://www.4shared.com/embed/3258682120/28a29181%22%20width%3D%22420%22%20height%3D%22320%22%20allowfullscreen%3D%22true%22%20allowscriptaccess%3D%22always%22%20%2F%3E&sign=ad7f8eba9f2dd004bd0b062f10d5c1f8
		### http://www.4shared.com/video/zrh6_JQK/Code_Lyoko_Episode_93_part_1__.htm
		### http://www.4shared.com/video/3258682120/28a29181
		### http://dc407.4shared.com/img/jYbVtfyK/13c15c24a00/code_lyoko_evolution_episode_2.flv
		### http://www.4shared.com/video/jYbVtfyK/code_lyoko_evolution_episode_2.html
		### http://dc301.4shared.com/img/3258682120/28a29181/dlink__2Fdownload_2FjYbVtfyK_2Fcode_5Flyoko_5Fevolution_5Fepisode_5F2_3Ftsid_3D20130804-214159-64f9af04/preview.flv?sId=MhCoXsiF3VlZ8cF3
		### http://dc301.4shared.com/img/3258682120/28a29181/dlink__2Fdownload_2FjYbVtfyK_3Ftsid_3D20130804-211137-3360aafb/preview.flv
		### 
		if (debugging==True): print 'doChecks '+MyNamesV[tt]+' permalinkId'
		if (debugging==True): print 'doChecks '+MyNamesV[tt]+' permalinkId: '+permalinkId
		if (permalinkId is not''):
			try: linka=getURL('http://www.4shared.com/video/'+permalinkId+'')
			except: linka=''
			if (linka is not '') and (linka is not 'none') and (linka is not None):
				try: 		vid_img=(re.compile('<meta property="og:image" content="(http.+?/img/.+?)"', re.IGNORECASE | re.DOTALL).findall(linka)[0]).strip()
				except: vid_img=ICON
				if (debugging==True): print 'doChecks '+MyNamesV[tt]+' vid_img: '+vid_img
				try: vid_url=(re.compile("var flvLink = '(.*?)'", re.IGNORECASE | re.DOTALL).findall(linka)[0]).strip()
				except: vid_url=''
				try: vid_url_mp4=(re.compile("var mp4Link = '(.*?)'", re.IGNORECASE | re.DOTALL).findall(linka)[0]).strip()
				except: vid_url_mp4=''
				try: vid_url_ogg=(re.compile("var oggLink = '(.*?)'", re.IGNORECASE | re.DOTALL).findall(linka)[0]).strip()
				except: vid_url_ogg=''
				try: vid_url_streamer=(re.compile("var streamerLink = '(.*?)'", re.IGNORECASE | re.DOTALL).findall(linka)[0]).strip()
				except: vid_url_streamer=''
				if (debugging==True): print 'doChecks '+MyNamesV[tt]+' vid_url_mp4: '+vid_url_mp4
				if (debugging==True): print 'doChecks '+MyNamesV[tt]+' vid_url_ogg: '+vid_url_ogg
				if (debugging==True): print 'doChecks '+MyNamesV[tt]+' vid_url_streamer: '+vid_url_streamer
				if (debugging==True): print 'doChecks '+MyNamesV[tt]+' vid_url flv: '+vid_url
				#vid_img=ICON ### Quick Fix: stagevu screenshot is huge and doesn't seem to load as either a thumbnail or fanart in XBMC.
				#
				if (vid_url_mp4 is not ''):
					try: addLink('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' [COLOR grey](mp4)[/COLOR]',vid_url_mp4,vid_img,fanart,show)
					except: t=''
				if (vid_url_ogg is not ''):
					try: addLink('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' [COLOR grey](ogg)[/COLOR]',vid_url_ogg,vid_img,fanart,show)
					except: t=''
				if (vid_url_streamer is not ''):
					try: addLink('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' [COLOR grey](streamer)[/COLOR]',vid_url_streamer,vid_img,fanart,show)
					except: t=''
				#
				if (vid_url is not ''):
					try: addLink('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' [COLOR grey](flv)[/COLOR]',vid_url,vid_img,fanart,show); return
					except: 
						t=''
						try:  addLink('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' [COLOR grey][/COLOR]',vid_url,ICON,fanart,show); return
						except: t=''
				else: 
					if (shoDebugging==True): VaddDir('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Error: No Url Found[/COLOR]', url, 1, MyIconsV[tt], fanart); return
			else:
				if (shoDebugging==True): VaddDir('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Error: Problem Loading Embed Page[/COLOR]', url, 1, MyIconsV[tt], fanart); return
		if (shoDebugging==True): VaddDir('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Error: No PermID Found[/COLOR]', url, 1, MyIconsV[tt], fanart)

def vvVIDEOLINKS_doChecks_videologtv(tt,url,mainurl,name,name2='none',scr=ICON,imgfan=fanart,show='none',type2=0,mode=0):
	if MySourcesV[tt] in url:#videolog.tv
		permalinkId=''
		if (debugging==True): print 'doChecks '+MyNamesV[tt]+' url: '+url
		if (permalinkId=='') and ('embed.videolog.tv/v/index.php' in url): ### 
			try: permalinkId=(re.compile('id_video=([0-9A-Za-z]+)', re.MULTILINE | re.IGNORECASE | re.DOTALL).findall('__'+url+'__')[0]).strip()
			except: permalinkId=''
		if (permalinkId=='') and ('?' in url): ### 
			try: permalinkId=(re.compile('id_video=([0-9A-Za-z]+)', re.MULTILINE | re.IGNORECASE | re.DOTALL).findall('__'+url+'__')[0]).strip()
			except: permalinkId=''
		#if (permalinkId=='') and ('vimeo.com/video/' in url): ### 
		#	try: permalinkId=(re.compile('/video/([0-9A-Za-z]+)', re.MULTILINE | re.IGNORECASE | re.DOTALL).findall('__'+url+'__')[0]).strip()
		#	except: permalinkId=''
		#if (permalinkId=='') and ('vimeo.com/m/' in url): ### 
		#	try: permalinkId=(re.compile('/m/([0-9A-Za-z]+)', re.MULTILINE | re.IGNORECASE | re.DOTALL).findall('__'+url+'__')[0]).strip()
		#	except: permalinkId=''
		### http://embed.videolog.tv/v/index.php?id_video=998554&related=&hd=&color1=&color2=&color3=&slideshow=&config_url=&
		### http://embed.videolog.tv/swfs/player.swf?id_video=998554&related=&hd=&color1=ffffff&color2=ffffff&color3=000000&slideshow=true&config_url=&ext=1
		### embed.videolog.tv/v/998554
		### videolog.tv/v/998554
		### http://www2.videolog.tv/998554
		### emb.videolog.tv
		### http://cdn-br.videolog.tv/b0/9c/998554_SD.mp4?epochTTL=1375656407&token=710051edd72a2a4e2154c3a328d1d8a7&ri=10485760&rs=600&start=0
		### http://videos.videolog.tv/b0/9c/998554_medium_2.jpg?epochTTL=1375736071&token=dc85185d077285c6b5810324c764e215&ri=3145728&rs=500
		### http://embed.videolog.tv/swfs/player.swf?id_video=998554&autostart=true&v=2
		### 
		### 
		if (debugging==True): print 'doChecks '+MyNamesV[tt]+' permalinkId: '+permalinkId
		if (permalinkId is not''):
			try: linka=getURL('http://www2.videolog.tv/'+permalinkId+'')
			except: linka=''
			if (linka is not '') and (linka is not 'none') and (linka is not None):
				try: vid_img=(re.compile('<meta property="og:image" content="(.+?)"', re.MULTILINE | re.IGNORECASE | re.DOTALL).findall(linka)[0]).strip()
				except: vid_img=ICON
				try:		vid_epochTTL=(re.compile('epochTTL=([0-9A-Za-z]+)', re.IGNORECASE | re.DOTALL).findall(vid_img)[0]).strip()
				except: vid_epochTTL=''
				try:		vid_token=	 (re.compile('token=([0-9A-Za-z]+)', re.IGNORECASE | re.DOTALL).findall(vid_img)[0]).strip()
				except: vid_token=''
				try:		vid_ri=	 (re.compile('ri=([0-9A-Za-z]+)', re.IGNORECASE | re.DOTALL).findall(vid_img)[0]).strip()
				except: vid_ri=''
				try:		vid_rs=	 (re.compile('rs=([0-9]+)', re.IGNORECASE | re.DOTALL).findall(vid_img)[0]).strip()
				except: vid_rs=''
				try:		(vid_fold1,vid_fold2)=	 re.compile('videos.videolog.tv/([0-9A-Za-z]+)/([0-9A-Za-z]+)/', re.IGNORECASE | re.DOTALL).findall(vid_img)[0]
				except: vid_fold1=vid_fold2=''
				vid_url='http://cdn-br.videolog.tv/'+vid_fold1+'/'+vid_fold2+'/'+permalinkId+'_SD.mp4?epochTTL='+vid_epochTTL+'&token='+vid_token+'&ri='+vid_ri+'&rs='+vid_rs+'&start=0'
				#try: vid_url=(re.compile("url\[\d+\] = '(.+?)'", re.MULTILINE | re.IGNORECASE | re.DOTALL).findall(linka)[0]).strip()
				#except: 
				#	try: vid_url=(re.compile('<param name="src" value="(.+?)" />', re.MULTILINE | re.IGNORECASE | re.DOTALL).findall(linka)[0]).strip()
				#	except: 
				#		try: vid_url=(re.compile('embed type="video/divx" src="(.+?)"', re.MULTILINE | re.IGNORECASE | re.DOTALL).findall(linka)[0]).strip()
				#		except: vid_url=''
				if (debugging==True): print 'doChecks '+MyNamesV[tt]+' vid_url: '+vid_url
				if (debugging==True): print 'doChecks '+MyNamesV[tt]+' vid_img: '+vid_img
				#vid_img=ICON ### Quick Fix: stagevu screenshot is huge and doesn't seem to load as either a thumbnail or fanart in XBMC.
				if (vid_url is not ''):
					#try: addLink('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' [COLOR grey][/COLOR]',vid_url,vid_img,fanart,show); return
					try: addLink('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' [COLOR grey][/COLOR]',vid_url,vid_img,fanart,show); return
					except: 
						t=''
						try:  addLink('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' [COLOR grey][/COLOR]',vid_url,ICON,fanart,show); return
						except: t=''
				else: 
					if (shoDebugging==True): VaddDir('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Error: No Url Found[/COLOR]', url, 1, MyIconsV[tt], fanart); return
			else:
				if (shoDebugging==True): VaddDir('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Error: Problem Loading Embed Page[/COLOR]', url, 1, MyIconsV[tt], fanart); return
		if (shoDebugging==True): VaddDir('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Error: No PermID Found[/COLOR]', url, 1, MyIconsV[tt], fanart)


def vvVIDEOLINKS_doChecks_vimeo(tt,url,mainurl,name,name2='none',scr=ICON,imgfan=fanart,show='none',type2=0,mode=0):
	if MySourcesV[tt] in url:#vimeo.com
		permalinkId=''
		if (debugging==True): print 'doChecks '+MyNamesV[tt]+' url: '+url
		if (permalinkId=='') and ('?' in url): ### http://stagevu.com/embed?width=500&height=430&background=3c3c3c&uid=dbwwzgqilkvo
			try: permalinkId=(re.compile('id=([0-9A-Za-z]+)', re.MULTILINE | re.IGNORECASE | re.DOTALL).findall('__'+url+'__')[0]).strip()
			except: permalinkId=''
		if (permalinkId=='') and ('vimeo.com/video/' in url): ### http://stagevu.com/video/dbwwzgqilkvo
			try: permalinkId=(re.compile('/video/([0-9A-Za-z]+)', re.MULTILINE | re.IGNORECASE | re.DOTALL).findall('__'+url+'__')[0]).strip()
			except: permalinkId=''
		if (permalinkId=='') and ('vimeo.com/m/' in url): ### http://stagevu.com/video/dbwwzgqilkvo
			try: permalinkId=(re.compile('/m/([0-9A-Za-z]+)', re.MULTILINE | re.IGNORECASE | re.DOTALL).findall('__'+url+'__')[0]).strip()
			except: permalinkId=''
		### http://player.vimeo.com/video/57198321
		### http://vimeo.com/57198321
		### vid_url='plugin://plugin.video.vimeo/?action=play_video&videoid='+permalinkId
		### http://vimeo.com/moogaloop.swf?clip_id=57198321
		### http://b.vimeocdn.com/ts/403/194/403194924_640.jpg
		### 
		### 
		### 
		if (debugging==True): print 'doChecks '+MyNamesV[tt]+' permalinkId: '+permalinkId
		if (permalinkId is not''):
			### vid_url='plugin://plugin.video.vimeo/?action=play_video&videoid='+permalinkId
			try: linka=getURL('http://vimeo.com/'+permalinkId+'')
			except: linka=''
			if (linka is not '') and (linka is not 'none') and (linka is not None):
				try: vid_url=(re.compile("url\[\d+\] = '(.+?)'", re.MULTILINE | re.IGNORECASE | re.DOTALL).findall(linka)[0]).strip()
				except: 
					try: vid_url=(re.compile('<param name="src" value="(.+?)" />', re.MULTILINE | re.IGNORECASE | re.DOTALL).findall(linka)[0]).strip()
					except: 
						try: vid_url=(re.compile('embed type="video/divx" src="(.+?)"', re.MULTILINE | re.IGNORECASE | re.DOTALL).findall(linka)[0]).strip()
						except: vid_url='plugin://plugin.video.vimeo/?action=play_video&videoid='+permalinkId
				try: vid_img=(re.compile('<meta property="og:image" content="(.+?)"', re.MULTILINE | re.IGNORECASE | re.DOTALL).findall(linka)[0]).strip()
				except: vid_img=ICON
				if (debugging==True): print 'doChecks '+MyNamesV[tt]+' vid_url: '+vid_url
				if (debugging==True): print 'doChecks '+MyNamesV[tt]+' vid_img: '+vid_img
				#vid_img=ICON ### Quick Fix: stagevu screenshot is huge and doesn't seem to load as either a thumbnail or fanart in XBMC.
				if (vid_url is not ''):
					try: addLink('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' [COLOR grey][/COLOR]',vid_url,vid_img,fanart,show); return
					except: 
						t=''
						try:  addLink('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' [COLOR grey][/COLOR]',vid_url,ICON,fanart,show); return
						except: t=''
				else: 
					if (shoDebugging==True): VaddDir('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Error: No Url Found[/COLOR]', url, 1, MyIconsV[tt], fanart); return
			else:
				if (shoDebugging==True): VaddDir('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Error: Problem Loading Embed Page[/COLOR]', url, 1, MyIconsV[tt], fanart); return
		if (shoDebugging==True): VaddDir('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Error: No PermID Found[/COLOR]', url, 1, MyIconsV[tt], fanart)


def vvVIDEOLINKS_doChecks_mp4upload(tt,url,mainurl,name,name2='none',scr=ICON,imgfan=fanart,show='none',type2=0,mode=0):
	if MySourcesV[tt] in url:#mp4upload.com
		if (debugging==True): print 'doChecks mp4upload url: '+url
		try: permalinkId=(re.compile('mp4upload.com/embed-([0-9A-Za-z]+).html', re.MULTILINE | re.IGNORECASE | re.DOTALL).findall('__'+url+'__')[0]).strip()
		except:
			try: permalinkId=(re.compile('mp4upload.com/embed-([0-9A-Za-z]+)-\d+x\d+.html', re.MULTILINE | re.IGNORECASE | re.DOTALL).findall('__'+url+'__')[0]).strip()
			except:
				try: permalinkId=(re.compile('mp4upload.com/([0-9A-Za-z]+)', re.MULTILINE | re.IGNORECASE | re.DOTALL).findall('__'+url+'__')[0]).strip()
				except: permalinkId='none'
		if (debugging==True): print 'doChecks mp4upload permalinkId: '+permalinkId
		if (permalinkId is not'none'):
			linka=getURL('http://mp4upload.com/embed-'+permalinkId+'.html')
			try: vid_img=(re.compile("'image': '(.+?)',", re.MULTILINE | re.IGNORECASE | re.DOTALL).findall(linka)[0]).strip()
			except: vid_img=ICON
			try: vid_url=(re.compile("'file': '(.+?)',", re.MULTILINE | re.IGNORECASE | re.DOTALL).findall(linka)[0]).strip()
			except: vid_url=''
			if (debugging==True): print 'doChecks mp4upload vid_url: '+vid_url
			if (debugging==True): print 'doChecks mp4upload vid_img: '+vid_img
			if (vid_url is not ''):
				vid_url=vid_url+'?start=0'
				#vid_url=urllib.unquote_plus(vid_url)
				try: addLink('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' [COLOR grey][/COLOR]',vid_url,vid_img,fanart,show); return
				except:
					try: addLink('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' [COLOR grey][/COLOR]',vid_url,ICON,fanart,''); return
					except: 
						try: 		VaddDir('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Error: Needs Testing.[/COLOR]', vid_url, 1, MyIconsV[tt], fanart); return
						except: VaddDir('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Error: Needs Testing.[/COLOR]', '', 1, MyIconsV[tt], fanart); return
			else: 
				if (shoDebugging==True): VaddDir('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Error: No Url Found[/COLOR]', url, 1, MyIconsV[tt], fanart); return
		if (shoDebugging==True): VaddDir('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Error: No PermID Found[/COLOR]', url, 1, MyIconsV[tt], fanart)

def vvVIDEOLINKS_doChecks_veoh(tt,url,mainurl,name,name2='none',scr=ICON,imgfan=fanart,show='none',type2=0,mode=0):
	if MySourcesV[tt] in url:#veoh.com
		if ('&#038;' in url): url=url.replace('&#038;','&')
		if (debugging==True): print 'doChecks '+MyNamesV[tt]+' url: '+url
		try: permalinkId=(re.compile('permalinkId=(.+?)&', re.MULTILINE | re.IGNORECASE | re.DOTALL).findall(url+'&')[0]).strip()
		except: permalinkId=''
		if (permalinkId=='') and ('veoh.com/browse/videos/' in url): #http://www.veoh.com/browse/videos/category/animation/watch/v1038910cYD2D6F5
			#try: permalinkId=(re.compile('http://www.veoh.com/browse/.+?/([0-9A-Z]+)__').findall(url+'__')[0]).strip()
			try: permalinkId=(re.compile('/([0-9A-Za-z]+)__', re.MULTILINE | re.IGNORECASE | re.DOTALL).findall('__'+url+'__')[0]).strip()
			except: permalinkId=''
		if (permalinkId=='') and ('veoh.com/watch/' in url): #http://www.veoh.com/watch/v962546hjffhF4m
			try: permalinkId=(re.compile('veoh.com/watch/([0-9A-Za-z]+)_', re.MULTILINE | re.IGNORECASE | re.DOTALL).findall('__'+url+'__')[0]).strip()
			except: permalinkId=''
		if (permalinkId=='') and ('videoweed.es/mobile/share.php' in url): #http://www.videoweed.es/mobile/share.php?id=
			try: permalinkId=(re.compile('id=([0-9A-Za-z]+)&', re.MULTILINE | re.IGNORECASE | re.DOTALL).findall('__'+url+'&__')[0]).strip()
			except: permalinkId=''
		if (permalinkId=='') and ('videoweed.es/api/player.api.php' in url): #http://www.videoweed.es/api/player.api.php?user=undefined&codes=1&file=c2piwuc52mgvp&pass=undefined&key=199.0.197.160-47f12f32e459ad8f59efa356a01f68af
			try: permalinkId=(re.compile('&file=([0-9A-Za-z]+)&', re.MULTILINE | re.IGNORECASE | re.DOTALL).findall('__'+url+'&__')[0]).strip()
			except: permalinkId=''
		if (permalinkId=='') and ('veoh.com/file/' in url): #http://www.videoweed.es/file/c2piwuc52mgvp
			try: permalinkId=(re.compile('veoh.com/file/([0-9A-Za-z]+)_', re.MULTILINE | re.IGNORECASE | re.DOTALL).findall('__'+url+'__')[0]).strip()
			except: permalinkId=''
		#
		if (debugging==True): print 'doChecks '+MyNamesV[tt]+' permalinkId: '+permalinkId
		if (permalinkId==''):
			if (shoDebugging==True): VaddDir('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Error: No PermID[/COLOR]', url, 1, MyIconsV[tt], fanart)
			return
		else:
			if (debugging==True): print 'doChecks '+MyNamesV[tt]+' permalinkId: '+permalinkId
			if (debugging==True): print 'doChecks '+MyNamesV[tt]+' details url: '+'http://www.veoh.com/rest/video/'+permalinkId+'/details'
			linka=getURL('http://www.veoh.com/rest/video/'+permalinkId+'/details')
			if ('fullPreviewHashPath="' in linka):
				try: fullPreviewHashPath=(re.compile('fullPreviewHashPath="(.+?)"').findall(linka)[0]).strip()
				except: fullPreviewHashPath='none'
				#partInfo=checkForPartNo(linka)
				partInfo=checkForPartNo2(linka)
				if (debugging==True): print 'doChecks '+MyNamesV[tt]+' fullPreviewHashPath: '+fullPreviewHashPath
				if (fullPreviewHashPath=='none'):
					if (shoDebugging==True): VaddDir('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Error: Needs Testing...[/COLOR]', '', 1, ICON, fanart)
					return
				else:
					vid_url=fullPreviewHashPath
					try: vid_img=(re.compile('fullHighResImagePath="(.+?)"').findall(linka)[0]).strip()
					except: 
						try: vid_img=(re.compile('fullMedResImagePath="(.+?)"').findall(linka)[0]).strip()
						except: vid_img=ICON
					if (debugging==True): print 'doChecks '+MyNamesV[tt]+' vid_img: '+vid_img
					#
					if ('(eng)' in linka.lower()) or ('[eng]' in linka.lower()) or ('english' in linka.lower()): vtag=' (English)'
					else: vtag=''
					#
					try: addLink('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' +'[COLOR red]'+vtag+'[/COLOR]'+partInfo+' [COLOR grey][/COLOR]',vid_url,vid_img,fanart,show)
					except:
						try:
							if (shoDebugging==True): VaddDir('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Error: Needs Testing.[/COLOR]', vid_url, 1, MyIconsV[tt], fanart)
						except:
							if (shoDebugging==True): VaddDir('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Error: Needs Testing..[/COLOR]', '', 1, ICON, fanart)
			else:
				if (shoDebugging==True): VaddDir('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Error: No Video Found.[/COLOR]', url, 1, MyIconsV[tt], fanart)
				return

def vvVIDEOLINKS_doChecks_vbox7(tt,url,mainurl,name,name2='none',scr=ICON,imgfan=fanart,show='none',type2=0,mode=0):
	if MySourcesV[tt] in url:#vbox7.com ## 20
		if (debugging==True): print 'doChecks vbox7 url: '+url
		## Note: some thanks to https://github.com/olamedia/medialink/blob/master/mediaDrivers/vbox7MediaLinkDriver.php
		## http://i48.vbox7.com/player/ext.swf?vid=04d4d01c09
		if ('i48.vbox7.com' in (url)): pre1='i48.'
		if ('i47.vbox7.com' in (url)): pre1='i47.'
		else: pre1='i48.'
		if ('vid=' in (url+'&')):
			vid_id=(re.compile('vid=(.+?)&').findall((url+'&'))[0]).strip()
			## http://i48.vbox7.com/p/291300b10d5.jpg
			vid_thumbnail='http://'+pre1+'vbox7.com/p/'+vid_id+'5.jpg'
			vid_player='http://'+pre1+'vbox7.com/player/ext_v7.swf?vid='+vid_id
			#vid_player
			#open(path, 'r')
			vid_url=url
			ifound=False
			if (debugging==True): print 'vid thumbnail: '+vid_thumbnail
			for ii in range(60):
				if (ifound==False):
					iia=str(ii)
					if (ii==0): iia=''
					elif (ii<10) and (ii>0): iia='0'+str(ii)
					pre2=vid_id[:2]
					#if (debugging==True): print 'pre2: '+pre2
					ipath='http://media'+iia+'.vbox7.com/s/'+pre2+'/'+vid_id+'.flv'
					if (debugging==True): print 'testing path: '+ipath
					cc=check_url_v(ipath)
					if (cc==True):
						vid_url=ipath
						if (debugging==True): print 'found: '+ipath
						try: 		addLink('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]* Error: Undergoing Testing.[/COLOR]',vid_url,vid_thumbnail,fanart,show)
						except: 	VaddDir('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Error: Needs Testing.[/COLOR]', vid_url, 1, MyIconsV[tt], fanart)
						return


def vvVIDEOLINKS_doChecks_megavideo(tt,url,mainurl,name,name2='none',scr=ICON,imgfan=fanart,show='none',type2=0,mode=0):
	return
	if MySourcesV[tt] in url:#megavideo ## site shut down.
		if (debugging==True): print 'doChecks megavideo url: '+url
		vid_url=url
		#try: 		addLink('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]* Error: Undergoing Testing.[/COLOR]',vid_url,scr,fanart,show)
		#except: 	VaddDir('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Error: Needs Testing.[/COLOR]', vid_url, 1, MyIconsV[tt], fanart)
		if (shoDebugging==True): VaddDir('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Error: Host has been shutdown.[/COLOR]', vid_url, 1, ICON, fanart)

def vvVIDEOLINKS_doChecks_vidup(tt,url,mainurl,name,name2='none',scr=ICON,imgfan=fanart,show='none',type2=0,mode=0):
	if MySourcesV[tt] in url:#vidup
		#http://vidup.org/embed.php?file=2a28113d&w=550&h=420&bg=http://www.verilscriptz.com/anime/animedubbednow.jpg
		if (debugging==True): print 'doChecks_vidup url: '+url
		linka=getURL(url)
		try: vid_img=(re.compile("background-image: url('(.+?)'); background-repeat").findall(linka)[0]).strip()
		except:
			try: vid_img=(re.compile("background-image: url('(.+?)'").findall(linka)[0]).strip()
			except: vid_img=MyIconsV[tt]
		try: vid_clip_dat=(((linka.split('clip:')[1]).split('{')[1]).split('}')[0]).strip()
		except: vid_clip_dat=linka
		try: vid_url=(re.compile('url: "(.+?)",').findall(vid_clip_dat)[0]).strip() ## s11.
		except: 
			try: vid_url=(re.compile('url:(.+?),').findall(vid_clip_dat)[0]).strip() ## s10.
			except: vid_url=''
		if (debugging==True): print 'doChecks_vidup v url: '+vid_url
		if (debugging==True): print 'doChecks_vidup v img: '+vid_img
		if (vid_url==''): t=''
		else:
			try: 		addLink('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Can be slow to load.[/COLOR]',vid_url,vid_img,fanart,show)
			except: 	VaddDir('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Error[/COLOR]', vid_url, 1, MyIconsV[tt], fanart)
			#background-image: url('
		#
		t=''

def vvVIDEOLINKS_doChecks_trollvid(tt,url,mainurl,name,name2='none',scr='none',imgfan=fanart,show='none',type2=0,mode=0):
	if MySourcesV[tt] in url:#trollvid.net
		if (type2==6):
			linka=getURLr(url,'http://dubbedanimeon.com/')
		else:
			linka=getURL(url)
		#if (debugging==True): print linka
		try: vid_fanart_of_site=(url.split('&bg=')[1]).strip()
		except: vid_fanart_of_site=imgfan
		try: vid_id1=(re.compile("file=(.+?)&").findall(url)[0]).strip()
		except: vid_id1=''
		if (vid_id1==''): vid_img=ICON
		else: vid_img='http://cdn.trollvid.net/thumbs/'+vid_id1+'.jpg'
		if 'This file was Deleted' in linka:
			VaddDir('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Error: File was Deleted.[/COLOR]', '', 1, vid_img, vid_fanart_of_site)
		#elif '<div class="notice">' in linka:
		#	VaddDir('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Error: Site threw a fit.[/COLOR]', '', 1, vid_img, vid_fanart_of_site)
		else:
			#try: vid_img=(re.compile(";background-image:url('(.+?)');background-repeat:").findall(dat_show)[0]).strip()
			#except: t='' #vid_img=ICON
			if ('&quot;' in linka): linka=linka.replace('&quot;','')
			try: vid_clip_dat=(((linka.split('clip:')[1]).split('{')[1]).split('}')[0]).strip()
			except: vid_clip_dat=linka
			try: vid_url=(re.compile('url: "(.+?)",').findall(vid_clip_dat)[0]).strip() ## s11.
			except: 
				try: vid_url=(re.compile('url:(.+?),').findall(vid_clip_dat)[0]).strip() ## s10.
				except: vid_url=''
			if ('http%3A%2F%2F' in vid_url): vid_url=urllib.unquote_plus(vid_url)
			testString='41c3311b2678a9e93c202586fe8852c4'
			attemptingString=' -  Attempting Work-a-round '
			trollvid_prefixes=['s01','s02','s03','s04','s05','s06','s07','s08','s09','s10','s11','s12','s13','s14','s15','s16','s17','s18','s19','s20']
			if '<div class="notice">' in linka:
				##linka=dReferer(url,'http://dubbedanimeon.com/')
				for trollvid_prefix in trollvid_prefixes:
					#if (check_ifUrl_isHTML('http://'+trollvid_prefix+'.trollvid.net/videos/'+testString+'/'+vid_id1+'.mp4')==False):
					addLink('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' [COLOR grey]'+attemptingString+''+trollvid_prefix+'[/COLOR]','http://'+trollvid_prefix+'.trollvid.net/videos/'+testString+'/'+vid_id1+'.mp4',vid_img,vid_fanart_of_site,show)
				######'http://s12.trollvid.net/videos/'+testString+'/'+vid_id1+'.mp4'
				######
			else: 
				if (vid_url==''):
					VaddDir('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Error: Needs Testing.[/COLOR]', '', 1, vid_img, vid_fanart_of_site)
				else: 
					try: vid_img=(re.compile(";background-image:url('(.+?)');background-repeat:").findall(dat_show)[0]).strip()
					except: vid_img=scr
					try: 
						addLink('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' [COLOR grey] -- Click fast before it times out.[/COLOR]',vid_url,vid_img,vid_fanart_of_site,show)
						if (shoDebugging==True):
							for trollvid_prefix in trollvid_prefixes:
								addLink('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' [COLOR grey]'+attemptingString+''+trollvid_prefix+'[/COLOR]','http://'+trollvid_prefix+'.trollvid.net/videos/'+testString+'/'+vid_id1+'.mp4',vid_img,vid_fanart_of_site,show)
						#listitem = xbmcgui.ListItem(MyColorsV[tt], iconImage="DefaultVideo.png", thumbnailImage=vid_img)
						#listitem.setProperty('IsPlayable', 'true')
						#listitem.setPath(vid_url)
						#xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)
						#
						###
					except: VaddDir('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]*2 Error: Needs Testing.[/COLOR]', vid_url, 1, vid_img, vid_fanart_of_site)
					#xbmc.executebuiltin('PlayMedia('+vid_url+')')
					##xbmc.executebuiltin('PlayMedia(vid_url)')
					#player = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
					#player.play(vid_url)
					#player.play(vid_url, xbmcgui.ListItem(label=show, path=vid_url))
					#player.play(url, xbmcgui.ListItem(label='Test', path=url))
					#player.stop()
					#xbmc.sleep(1000)
					return
				#
				#
				#
				#
				#
			#
			### 
			### http://sv3.trollvid.net/embed.php?file=5ccf1c9c&site=on&w=566&h=360&bg=http://dubbedanimeon.com/wp-content/uploads/bgg.jpg
			### http://sv3.trollvid.net/embed.php?file=5ccf1c9c&w=566&h=360&bg=http://dubbedanimeon.com/wp-content/uploads/bgg.jpg
			### 
			### 
			### 
			### http://sv3.trollvid.net/embed.php?file=7b89d472&w=598&h=336&bg=
			### http://cdn.trollvid.net/thumbs/7b89d472.jpg
			### http://s11.trollvid.net/videos/41c3311b2678a9e93c202586fe8852c4/7b89d472.mp4
			### 
			### http://s11.trollvid.net/videos/41c3311b2678a9e93c202586fe8852c4/7b89d472.mp4
			### http://s10.trollvid.net/videos/41c3311b2678a9e93c202586fe8852c4/b2f156a3.mp4
			### http://s11.trollvid.net/videos/41c3311b2678a9e93c202586fe8852c4/5ccf1c9c.mp4 << http://dubbedanimeon.com/episode/is-this-a-zombie-episode-1-english-dubbed/
			### 
			### 
			### 
			### 
			### http://trollvid.net/dub.php?file=9729cf2a&w=560&h=360&bg=http://dubbedanimeon.com/wp-content/uploads/bgg.jpg ## Playable via firefox
			### http://s4.trollvid.net/videos/eg7ha2vktc/9729cf2a.mp4 ## download via firefox
			### http://trollvid.net/images/sup.mp4
			### http://dubbedanimeon.com/wp-content/uploads/bgg.jpg
			### http://s10.trollvid.net/videos/41c3311b2678a9e93c202586fe8852c4/fb6170ff.mp4
			### 
			### 
			#
			#
			#
			#



def vvVIDEOLINKS_doChecks_rutube(tt,url,mainurl,name,name2='none',scr='none',imgfan='none',show='none',type2=0,mode=0):
	if MySourcesV[tt] in url:#rutube.ru ## screenshot: working , video: no luck
		linka=getURL(url)
		if 'This file was Deleted' in linka:
			VaddDir('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Error: File was Deleted.[/COLOR]', '', 1, MyIconsV[tt], imgfan)
		else:
			if ('http://video.rutube.ru/' in url):
				vid_source=''; vid_embed=''; vid_thumbnail=''; vid_url=''
				vid_id=url.split('.rutube.ru/')[1]
				vid_thumbnail='http://img-1.rutube.ru/thumbs/'+vid_id[0:2]+'/'+vid_id[2:4]+'/'+vid_id+'-1.jpg'
				if (debugging==True):  print 'thumbnail: '+vid_thumbnail
				vid_xml='http://rutube.ru/api/video/'+vid_id+'/?format=xml'
				if (debugging==True): print 'xml: '+vid_xml
				linkb=getURL(vid_xml)
				if ('<div class="error-code">404</div>' in linkb) or (linkb==None) or (linkb=='none'):
					vid_xml='http://rutube.ru/cgi-bin/xmlapi.cgi?rt_mode=movie&rt_movie_id='+vid_id+'&utf=1'
					if (debugging==True): print 'xml: '+vid_xml
					linkb=getURL(vid_xml)
				##if (debugging==True): print linkb
				if ('<div class="error-code">404</div>' in linkb) or (linkb==None) or (linkb=='none'):
					VaddDir('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Error: Bad XML Url.[/COLOR]', vid_xml, 1, vid_thumbnail, imgfan)
					return
				if ('<thumbnail_url>http://' in linkb): vid_thumbnail=(re.compile("<thumbnail_url>(.+?)</thumbnail_url>").findall(linkb)[0]).strip()
				if ('<video_url>http://' in linkb): vid_url=(re.compile("<video_url>(.+?)</video_url>").findall(linkb)[0]).strip()
				if ('<embed_url>http://' in linkb): vid_embed=(re.compile("<embed_url>(.+?)</embed_url>").findall(linkb)[0]).strip()
				if ('<source_url>http://' in linkb): vid_source=(re.compile("<source_url>(.+?)</source_url>").findall(linkb)[0]).strip()
				if (debugging==True): 
					print 'thumbnail: '+vid_thumbnail
					print 'url: '+vid_url
					print 'embed: '+vid_embed
					print 'vid: '+vid_source
				#
				#vid_url='http://rutube.ru/player.swf?hash='+vid_id+'&&referer=' ## plays animation of a button from some flash player.
				#vid_url=url ## plays animation of a button from some flash player.
				#vid_url='http://rutube.ru/trackinfo/'+vid_id+'.xml' ## Playback failed.
				#vid_url='http://rutube.ru/video/'+vid_id+'/'
				try: addLink('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Error: Needs Testing.[/COLOR]',vid_url,vid_thumbnail,imgfan,show)
				except: VaddDir('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Error[/COLOR]', matcha, 1, vid_thumbnail, imgfan)
			#matcha=re.compile("addVariable\('file','(.+?)'\)").findall(linka)[0]
			##if (debugging==True): print 'match: ',matcha
			### vid_id
			### http://video.rutube.ru/64a7da0f3b1158b4830401f3ddfea34c
			### 'http://img-'.rand(1, 4).'.rutube.ru/thumbs/'.substr($videoId, 0, 2).'/'.substr($videoId, 2, 2).'/'.$videoId.'-1.jpg'
			### http://video.rutube.ru/43398d4a0260c6fa0634de666e6d670e
			### http://img-1.rutube.ru/thumbs/43/39/43398d4a0260c6fa0634de666e6d670e-1.jpg
			### 'http://img-1.rutube.ru/thumbs/'+vid_id[0:2]+'/'+vid_id[2:2]+'/'+vid_id+'-1.jpg'
			### http://video-12-7.rutube.ru/hdsv2/0GSkNrgI-Ur-hHv9nMTrHw/1374435821/n2vol1/43398d4a0260c6fa0634de666e6d670e.mp4Seg1-Frag1
			### http://video.rutube.ru/9137763f009758d936911a936bed9d28
			### http://video-1-28.rutube.ru/hdsv2/6ZlOmWZaDryFeZzdLL43-Q/1374435996/n2vol1/9137763f009758d936911a936bed9d28.mp4Seg1-Frag1
			### http://rutube.ru/player.swf?hash=9137763f009758d936911a936bed9d28&&referer=
			### 
			### 
			### 
			### 
			### 
			### 
			### 
			else:
				vid_url=url
				try: addLink('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Error: Needs Testing.[/COLOR]',vid_url,MyIconsV[tt],imgfan,show)
				except: VaddDir('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Error[/COLOR]', matcha, 1, MyIconsV[tt], imgfan)

def vvVIDEOLINKS_doChecks_putlocker(tt,url,mainurl,name,name2='none',scr=ICON,imgfan=fanart,show='none',type2=0,mode=0):
	if MySourcesV[tt] in url:#putlocker
		if ('http://www.putlocker.com/file/' in url): url=url.replace('http://www.putlocker.com/file/','http://www.putlocker.com/embed/')
		linkaa=getURL(url)
		if 'File Does not Exist, or Has Been Removed' in linkaa: VaddDir('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Error: File was Deleted.[/COLOR]', '', 1, MyIconsV[tt], imgfan)
		elif 'This file is temporary disabled (but not deleted).' in linkaa: VaddDir('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Error: temporary disabled (but not deleted).[/COLOR]', '', 1, MyIconsV[tt], imgfan)
		elif 'Try again a bit later.' in linkaa: VaddDir('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Error: Try again a bit later.[/COLOR]', '', 1, MyIconsV[tt], imgfan)
		else:
			##if 'embed' in url: url=url.replace('embed','file')
			#linkaa=getURL(url)
			if ('" name="fuck_you"' in linkaa):
				matchaa=re.compile('<input type="hidden" value="(.+?)" name="fuck_you"').findall(linkaa)[0]
				postData = { 'fuck_you' : matchaa , 'confirm' : 'Close Ad and Watch as Free User'}
				linka=postURL(url,postData)
			else:
				linka=linkaa
			if 'File Does not Exist, or Has Been Removed' in linka: VaddDir('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Error: File was Deleted.[/COLOR]', '', 1, MyIconsV[tt], imgfan)
			elif 'This file is temporary disabled (but not deleted).' in linka: VaddDir('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Error: temporary disabled (but not deleted).[/COLOR]', '', 1, MyIconsV[tt], imgfan)
			elif 'Try again a bit later.' in linka: VaddDir('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Error: Try again a bit later.[/COLOR]', '', 1, MyIconsV[tt], imgfan)
			else:
				###if (debugging==True): print 'testing for putlocker:',matchaa,url,linka,postData
				if 'playlist' in linka:
					matcha=re.compile("playlist: '(.+?)',").findall(linka)[0]
					#if (debugging==True): print 'Playlist found:','http://www.putlocker.com',matcha
					linkb=getURL('http://www.putlocker.com'+matcha)
					#matchb=re.compile('<media:content url="(.+?)" type="image/jpeg" /></item>','<media:content url="(.+?)" type="video/x-flv"  duration=".+?" /></item>').findall(linkb)[0]
					#(video_image,video_url)=re.compile('<media:content url="(.+?)" type="image/jpeg" /></item>','<media:content url="(.+?)" type="video/x-flv"  duration=".+?" /></item>').findall(linkb)[0]
					video_image=re.compile('<item><title>Preview</title><media:content url="(.+?)" type="image/jpeg".+?/></item>').findall(linkb)[0]
					video_url=re.compile('<item><title>Video</title><link>.+?</link><media:content url="(.+?)" type="video/x-flv".+?/></item>').findall(linkb)[0]
					#for video_image,video_url in matchb:
					video_url=urllib.unquote_plus(video_url.replace('&amp;','&'))
					video_image=urllib.unquote_plus(video_image)
					try:
						addLink('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + '  [COLOR grey][/COLOR]',video_url,video_image,imgfan,show)
					except:
						try:
							addLink('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]*2[/COLOR]',video_url,scr,imgfan,show)
						except:#failed @ logo.link
							VaddDir('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Error[/COLOR]', '', 1, MyIconsV[tt], imgfan)
				else: notification('Fetching Link: '+MyNamesV[tt],'Failed to find playlist.')
### ############################################################################################################
### ############################################################################################################
def vvVIDEOLINKS_doChecks_others(ListOfUrls,tt,url,mainurl,name,name2='none',scr='none',imgfan='none',show='none',type2=0,mode=0):
	######## I need to learn how to merge multiple Lists better before enabling this feature I guess. :(
	#ListOfUrls
	icnt = int(0)
	#if (debugging==True): print'test1:',ListOfUrls
	#for urlItemA in ListOfUrls:
	#	print'test2:',urlItemA
	#	for urlItem in urlItemA:
	#		vsCheck=False
	#		print'test3:',MySourcesV
	#		for VSites in MySourcesV:
	#			if (VSites in urlItem): 
	#				vsCheck=True # and ('yourupload' not in VSites):#Checking that it doesnt match any known site.
	#				print VSites +' is in '+ urlItem
	#		if ('facebook.com' in urlItem) or ('ads' in urlItem): 
	#			print'fb/ads: true'
	#			vsCheck=True
	#		if ('novamov' in urlItem): 
	#			print'novamov: true'
	#			vsCheck=False
	#		if vsCheck==False:
	#			icnt=(int(icnt) + 1)
	#			print 'Unknown Link Found For: # '+str(icnt)+'.) '+show,urllib.unquote_plus(url)
	#			#addLink('[COLOR white]Unknown[/COLOR] - [COLOR grey]Please report the Show and Episode to me[/COLOR]',urllib.unquote_plus(url),ICON, fanart,show)#MyIconsV[tt])
	#			VaddDir('[COLOR white]Unknown[/COLOR] - [COLOR grey]Please report the Show and Episode to me[/COLOR]', urllib.unquote_plus(url), 1, ICON, fanart)
### ############################################################################################################
### ############################################################################################################



### ############################################################################################################
### ############################################################################################################
### ############################################################################################################
#xbmcplugin.endOfDirectory(int(sys.argv[1]))
### ############################################################################################################
### ############################################################################################################
### ############################################################################################################
