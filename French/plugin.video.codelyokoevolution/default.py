### ############################################################################################################
###	#	
### # Project: 			#		Code Lyoko Evolution - by The Highway 2013.
### # Author: 			#		The Highway
### # Version:			#		v0.1.4
### # Description: 	#		http://codelyokoevolutionfan.webs.com/
###	#	
### ############################################################################################################
### ############################################################################################################
##### Imports #####
import xbmc, xbmcplugin, xbmcgui, xbmcaddon, xbmcvfs
import urllib, urllib2
import re,os,sys,string,StringIO,array
import htmllib,logging,random,time,datetime
#try: import requests ### <import addon="script.module.requests" version="1.1.0"/> ### 
#except: t=''				 ### See https://github.com/kennethreitz/requests ### 
try: import urlresolver
except: t=''
#import unicodedata
#import zipfile ### Removed because it caused videos to not play. ###
import HTMLParser, htmlentitydefs
try: 		import StorageServer
except: import storageserverdummy as StorageServer
try: 		from t0mm0.common.addon 				import Addon
except: from t0mm0_common_addon 				import Addon
try: 		from t0mm0.common.net 					import Net
except: from t0mm0_common_net 					import Net
try: 		from sqlite3 										import dbapi2 as sqlite; print "Loading sqlite3 as DB engine"
except: from pysqlite2 									import dbapi2 as sqlite; print "Loading pysqlite2 as DB engine"
try: 		from script.module.metahandler 	import metahandlers
except: from metahandler 								import metahandlers
### 
from teh_tools 		import *
from config 			import *
from videolinks		import *
##### /\ ##### Imports #####
### ############################################################################################################
### ############################################################################################################
### ############################################################################################################
__plugin__=ps('__plugin__'); __authors__=ps('__authors__'); __credits__=ps('__credits__'); _addon_id=ps('_addon_id'); _domain_url=ps('_domain_url'); _database_name=ps('_database_name'); _plugin_id=ps('_addon_id')
_database_file=os.path.join(xbmc.translatePath("special://database"),ps('_database_name')+'.db'); 
### 
_addon=Addon(ps('_addon_id'), sys.argv); addon=_addon; _plugin=xbmcaddon.Addon(id=ps('_addon_id')); cache=StorageServer.StorageServer(ps('_addon_id'))
### ############################################################################################################
### ############################################################################################################
### ############################################################################################################
##### Paths #####
### # ps('')
_addonPath	=xbmc.translatePath(_plugin.getAddonInfo('path'))
_artPath		=xbmc.translatePath(os.path.join(_addonPath,ps('_addon_path_art')))
_datapath 	=xbmc.translatePath(_addon.get_profile()); _artIcon		=_addon.get_icon(); _artFanart	=_addon.get_fanart()
##### /\ ##### Paths #####
##### Important Functions with some dependencies #####
def art(f,fe=ps('default_art_ext')): return xbmc.translatePath(os.path.join(_artPath,f+fe)) ### for Making path+filename+ext data for Art Images. ###
def addst(r,s=''): return _addon.get_setting(r)   ## Get Settings
def addpr(r,s=''): return _addon.queries.get(r,s) ## Get Params
def cFL(t,c=ps('default_cFL_color')): ### For Coloring Text ###
	return '[COLOR '+c+']'+t+'[/COLOR]'
##### /\ ##### Important Functions with some dependencies #####
##### Settings #####
_setting={}; _setting['enableMeta']	=	_enableMeta			=tfalse(addst("enableMeta"))
_setting['debug-enable']=	_debugging			=tfalse(addst("debug-enable")); _setting['debug-show']	=	_shoDebugging		=tfalse(addst("debug-show"))
_setting['meta.movie.domain']=ps('meta.movie.domain'); _setting['meta.movie.search']=ps('meta.movie.search')
_setting['meta.tv.domain']   =ps('meta.tv.domain');    _setting['meta.tv.search']   =ps('meta.tv.search')
_setting['meta.tv.page']=ps('meta.tv.page'); _setting['meta.tv.fanart.url']=ps('meta.tv.fanart.url'); _setting['meta.tv.fanart.url2']=ps('meta.tv.fanart.url2'); _setting['label-empty-favorites']=tfalse(addst('label-empty-favorites'))

##### /\ ##### Settings #####
##### Variables #####
_art404='http://www.solarmovie.so/images/404.png' #_art404=art('404')
_art150='http://www.solarmovie.so/images/thumb150.png' #_art150=art('thumb150')
_artDead='http://www.solarmovie.so/images/deadplanet.png' #_artDead=art('deadplanet')
_artSun=art('sun'); COUNTRIES=ps('COUNTRIES'); GENRES=ps('GENRES'); _default_section_=ps('default_section'); net=Net(); DB=_database_file; BASE_URL=_domain_url;
##### /\ ##### Variables #####
deb('Addon Path',_addonPath);  deb('Art Path',_artPath); deb('Addon Icon Path',_artIcon); deb('Addon Fanart Path',_artFanart)
### ############################################################################################################
def eod(): _addon.end_of_directory()
def deadNote(header='',msg='',delay=5000,image=_artDead): _addon.show_small_popup(title=header,msg=msg,delay=delay,image=image)
def sunNote( header='',msg='',delay=5000,image=_artSun):
	header=cFL(header,ps('cFL_color')); msg=cFL(msg,ps('cFL_color2'))
	_addon.show_small_popup(title=header,msg=msg,delay=delay,image=image)
def messupText(t,_html=False,_ende=False,_a=False,Slashes=False):
	if (_html==True): t=ParseDescription(HTMLParser.HTMLParser().unescape(t))
	if (_ende==True): t=t.encode('ascii', 'ignore'); t=t.decode('iso-8859-1')
	if (_a==True): t=_addon.decode(t); t=_addon.unescape(t)
	if (Slashes==True): t=t.replace( '_',' ')
	return t
def name2path(name):  return (((name.lower()).replace('.','-')).replace(' ','-')).replace('--','-')
def name2pathU(name): return (((name.replace(' and ','-')).replace('.','-')).replace(' ','-')).replace('--','-')
### ############################################################################################################
### ############################################################################################################
##### Queries #####
_param={}
_param['mode'],_param['url']=addpr('mode',''),addpr('url',''); _param['pagesource'],_param['pageurl'],_param['pageno'],_param['pagecount']=addpr('pagesource',''),addpr('pageurl',''),addpr('pageno',0),addpr('pagecount',1)
_param['img']=addpr('img',''); _param['fanart']=addpr('fanart',''); _param['thumbnail'],_param['thumbnail'],_param['thumbnail']=addpr('thumbnail',''),addpr('thumbnailshow',''),addpr('thumbnailepisode','')
_param['section']=addpr('section','movies'); _param['title']=addpr('title',''); _param['year']=addpr('year',''); _param['genre']=addpr('genre','')
_param['by']=addpr('by',''); _param['letter']=addpr('letter',''); _param['showtitle']=addpr('showtitle',''); _param['showyear']=addpr('showyear',''); _param['listitem']=addpr('listitem',''); _param['infoLabels']=addpr('infoLabels',''); _param['season']=addpr('season',''); _param['episode']=addpr('episode','')
_param['pars']=addpr('pars',''); _param['labs']=addpr('labs',''); _param['name']=addpr('name',''); _param['thetvdbid']=addpr('thetvdbid','')
_param['plot']=addpr('plot',''); _param['tomode']=addpr('tomode',''); _param['country']=addpr('country','')
_param['thetvdb_series_id']=addpr('thetvdb_series_id',''); _param['dbid']=addpr('dbid',''); _param['user']=addpr('user','')
_param['subfav']=addpr('subfav','')

#_param['']=_addon.queries.get('','')
#_param['']=_addon.queries.get('','')
##_param['pagestart']=addpr('pagestart',0)
##### /\
### ############################################################################################################
### ############################################################################################################
### ############################################################################################################
### ############################################################################################################
### ############################################################################################################
##### Player Functions #####
def PlayVideo(url, infoLabels={}, listitem=[]):
	#WhereAmI('@ PlayVideo -- Getting ID From:  %s' % url); My_infoLabels=eval(infoLabels)
	#stream_url=urlresolver.HostedMediaFile(url=url).resolve()
	stream_url=urlresolver.HostedMediaFile(url).resolve()
	_addon.resolve_url(stream_url)
	infoLabels={ "Studio": addpr('title',''), 'Title': addpr('studio',''), 'url': url } ### yes i switched title and studio on purpose.
	li=xbmcgui.ListItem(_param['title'], iconImage=_param['img'], thumbnailImage=_param['img'])
	li.setInfo(type="Video", infoLabels=infoLabels ); li.setProperty('IsPlayable', 'true')
	_addon.end_of_directory()
	play=xbmc.Player(xbmc.PLAYER_CORE_AUTO) ### xbmc.PLAYER_CORE_AUTO | xbmc.PLAYER_CORE_DVDPLAYER | xbmc.PLAYER_CORE_MPLAYER | xbmc.PLAYER_CORE_PAPLAYER
	play.play(stream_url, li); xbmcplugin.setResolvedUrl(handle=int(sys.argv[1]), succeeded=True, listitem=li)


def PlayTrailer(url):
	sources=[]; url=url.decode('base-64'); WhereAmI('@ PlayVideo:  %s' % url)
	try: 
		hosted_media=urlresolver.HostedMediaFile(url=url); sources.append(hosted_media); source=urlresolver.choose_source(sources)
		if (source): stream_url=source.resolve()
	except:
		deb('Stream failed to resolve',url); return
	else: stream_url=''
	try: xbmc.Player().play(stream_url)
	except: 
		deb('Video failed to play',stream_url); return
##### /\ ##### Player Functions #####
### ############################################################################################################
### ############################################################################################################
### ############################################################################################################
##### Weird, Stupid, or Plain up Annoying Functions. #####
def netURL(url): ### Doesn't seem to work.
	return net.http_GET(url).content
def remove_accents(input_str): ### Not even sure rather this one works or not.
	nkfd_form = unicodedata.normalize('NFKD', unicode(input_str))
	return u"".join([c for c in nkfd_form if not unicodedata.combining(c)])
##### /\ ##### Weird, Stupid, or Plain up Annoying Functions. #####


def mGetItemPage(url):
	deb('Fetching html from Url',url)
	try: html=net.http_GET(url).content
	except: html=''
	if (html=='') or (html=='none') or (html==None) or (html==False): return ''
	else:
		html=HTMLParser.HTMLParser().unescape(html); html=_addon.decode(html); html=_addon.unescape(html); html=ParseDescription(html); html=html.encode('ascii', 'ignore'); html=html.decode('iso-8859-1'); deb('Length of HTML fetched',str(len(html)))
	return html
def mdGetSplitFindGroup(html,ifTag='', parseTag='',startTag='',endTag=''): 
	if (ifTag=='') or (parseTag=='') or (startTag=='') or (endTag==''): return ''
	if (ifTag in html):
		html=(((html.split(startTag)[1])).split(endTag)[0]).strip()
		try: return re.compile(parseTag, re.MULTILINE | re.IGNORECASE | re.DOTALL).findall(html)
		except: return ''
	else: return ''

### ############################################################################################################
### ############################################################################################################
### ############################################################################################################
##### Listings #####
def ListItems(section, url, pgNo='1', pgCount='1', oldTitle=''):
	WhereAmI('@ List Items -- url: %s' % url)
	WhereAmI('@ List Items')
	if (url==''): return
	html='' #; last=2; start=int(startPage); end=(start+int(numOfPages)); html_last=''; nextpage=startPage
	try:		html_=getURL(url)
	except: html_=''
	#print html_
	if (html_=='') or (html_=='none') or (html_==None): 
		deb('Error','Problem with page'); deadNote('Results:  '+section,'No results were found.'); eod(); return
	#if ('<h1>Nothing was found by your request</h1>' in html_):
	#	deadNote('Results:  '+section,'Nothing was found by your request'); eod(); return
	#
	try: 		pgNext=re.compile('</a> <a href="(http://[0-9A-Za-z]+\.[0-9A-Za-z]+\.[0-9A-Za-z]+/apps/videos/[channels/show/]*[\d]*\-*[0-9A-Za-z\-]*\?page=\d+)" class="next_page" rel="next">next</a></div>', re.IGNORECASE | re.DOTALL).findall(html_)[0] #<a href="http://codelyokoevolutionfan.webs.com/apps/videos/?page=2" class="next_page" rel="next">next</a>
	except: 
		try: 		pgNext=re.compile('> <a href="(.+?page=\d+.*?)" class="next_page" rel="next">next</a></div>', re.IGNORECASE | re.DOTALL).findall(html_)[0] #<a href="http://codelyokoevolutionfan.webs.com/apps/videos/?page=2" class="next_page" rel="next">next</a>
		except: pgNext=''
	deb('Next Page - Data',pgNext)
	print pgNext
	if (pgNext is not '') and ('http' in pgNext) and ('?page=' in pgNext) and ('<' not in pgNext): 
		cat_name=section; cat_url=pgNext
		try:		pgNextNo=re.compile('page=(\d+)&', re.IGNORECASE | re.DOTALL).findall(pgNext+'&')[0]
		except: 
			try:		pgNextNo=re.compile('page=(\d+)', re.IGNORECASE | re.DOTALL).findall(pgNext+'&')[0]
			except: pgNextNo='?'
		_addon.add_directory({'mode': 'GetTitles', 'section': section, 'url': cat_url },{'title':  cFL('['+cFL(iFL('Next: '+pgNextNo+' '),ps('cFL_color6'))+']',ps('cFL_color'))+'  '+cFL(cat_name[0:1],ps('cFL_color'))+cat_name[1:]},img=_artIcon, fanart=_artFanart)
	if ('<table cellspacing="0" cellpadding="0" border="0" class="fw-list-grid"><tr><td align="center"' in html_): html=html_.split('<table cellspacing="0" cellpadding="0" border="0" class="fw-list-grid"><tr><td align="center"')[1]
	else: html=html_
	### s='<div class="thumbnail" style="position:relative" onmouseover="fwGetContextBar\('+"'videoContextBar'\)\.show\(this, '(\d+)'\)"+';return false;">[\n]\s+<a href="(.+?)"><img src="(.+?)" border="0"></a>[\n]\s+<div style=".+?"></div>[\n]\s+</div>[\n]\s+<div class="clear"></div>[\n]\s+<b><a href=".+?" title=".+?"><span class="fw_sanitized">(.+?)</span></a></b>[\n]\s+<br>[\n]\s+<div style=".+?">[\n]\s+by <a href=".+?" style=".+?">.+?</a> on (\D+ \d+, \d\d\d\d) at (\d+:\d+ \D+)\s+<br>[\n]\s+(\d+) Views - (\d+) Comments'
	s='<div class="thumbnail" style=".+?" onmouseover=".+?'+"show\(this, '(\d+)'"+'.+?">[\n*]\s*<a href="(.+?)"><img src="(.+?)" border="\d*"></a>[\n*]\s*<div style=".+?"></div>[\n]\s*</div>'
	s+='\n*\s*<div class="clear"></div>[\n*]\s*<b><a href=".*?" title=".*?"><span class=".*?">(.+?)</span></a></b>[\n]\s*<br>[\n]\s*<div style=".+?">[\n]\s*by\s*<a href=".*?" style=".*?">.*?</a>\s+on\s*(\D* \d*,* \d*)\s+at\s*(\d*:*\d* \D*)\s*<br>[\n-]\s*(\d+) Views - (\d+) Comment'
	try: 		Items=re.compile(s, re.MULTILINE | re.IGNORECASE | re.DOTALL).findall(html)
	except: Items=''
	print Items
	### ( item_id , item_url , item_img , item_title , item_added_date, item_added_time, item_views, item_comments )
	if (not Items) or (Items==''): eod(); return
	for ( item_id , item_url , item_img , item_title , item_added_date, item_added_time, item_views, item_comments ) in Items:
		_addon.add_directory({'mode': 'GetVideos', 'section': section, 'title': item_title, 'url': item_url, 'img': item_img },{'date': item_added_date, 'time': item_added_time, 'title':  cFL('['+cFL(iFL(item_added_date+' '),ps('cFL_color6'))+']',ps('cFL_color'))+'  '+cFL(item_title[0:1],ps('cFL_color'))+item_title[1:]}, img=item_img, fanart=_artFanart)
	#
	#
	#
	#
	set_view('videos',515,False)
	eod()

def ListLinks(section, url, oldTitle=''):
	WhereAmI('@ List Links -- url: %s' % url)
	WhereAmI('@ List Links')
	if (url==''): return
	html='' #; last=2; start=int(startPage); end=(start+int(numOfPages)); html_last=''; nextpage=startPage
	try:		html_=getURL(url)
	except: html_=''
	#print html_
	if (html_=='') or (html_=='none') or (html_==None): 
		deb('Error','Problem with page'); deadNote('Results:  '+section,'No results were found.'); eod(); return
	### ( item_id , item_url , item_img , item_title , item_added_date, item_added_time, item_views, item_comments )
	oList=[]; hList=[]; r3=[]; Brackets=['<iframe.*?src="(.+?)"'] ### '<a href=".+?dailymotion.com/video/[A-Za-z0-9].+?)".*?>'
	for Bracket in Brackets:
		deb('Bracket',Bracket)
		try: 		Items=re.compile(Bracket, re.MULTILINE | re.IGNORECASE | re.DOTALL).findall(html_)
		except: Items=''
		print 'Items'
		print Items
		if (Items) or (Items is not ''):
			for Item in Items:
				r3.append(Item)
	#r3=sorted(r3)
	#c=0
	#vvVIDEOLINKS(url + '/2',name,name2,scr,imgfan,show,type2,mode)
	for r4 in r3:
		fa='http://d2bm3ljpacyxu8.cloudfront.net/fit/1920x1920/codelyokoevolutionfan.webs.com/01dd5fd8b68f4c43bf5b877ada1e5e37-d5jidv8-1.png'
		vvVIDEOLINKS_doChecks(r4,url,oldTitle,oldTitle,_param['img'],fa,oldTitle,0,0)
	eod(); return
#		#
#		#
#		#
#		#try:		host=re.compile('http://([0-9A-Za-z\.]+/)', re.IGNORECASE | re.DOTALL).findall(html)[0]
#		#except: host=''
#		##urlresolver.HostedMediaFile(url=r4, title=label)
#		#oList.append(urlresolver.HostedMediaFile(url=r4, title=str(c)))
#		if ('dailymotion.com/embed/video/' in r4):
#			r4=r4.replace('dailymotion.com/embed/video/','dailymotion.com/video/')
#		if ('youtube.com/embed/' in r4):
#			#if ('?' is n r4): r4=r4.split('?')[0]
#			r4=r4.replace('youtube.com/embed/','youtube.com/watch?v=')
#		hh='http://'+(r4.split('://')[1]).split('/')[0]+'/'
#		if (urlresolver.HostedMediaFile(url=r4).valid_url()):
#			host=urlresolver.HostedMediaFile(url=r4).get_url()
#			media_id=urlresolver.HostedMediaFile(url=r4).get_media_id()
#			#print urlresolver.HostedMediaFile(url=r4).get_media_url()
#			#print urlresolver.HostedMediaFile(url=r4).get_host()
#			#print urlresolver.HostedMediaFile(r4).get_url()
#			oList.append(urlresolver.HostedMediaFile(host=host, media_id=media_id))
#			hList.append(r4)
#			xbmc.Player(xbmc.PLAYER_CORE_AUTO).play(r4)
#		#oList.append(urlresolver.HostedMediaFile(host=r4, media_id='xxx'))
#		#oList.append(urlresolver.HostedMediaFile(url=r4, title=hh))
#		#oList.append(urlresolver.HostedMediaFile(url=r4))
#		#oList.append(urlresolver.HostedMediaFile(host=r4, media_id='xxx'))
#		#hList.append(r4)
#		c=c+1
#		host=r4
#		deb('host',host)
#		#if (host) and (host is not ''):
#		#	if urlresolver.HostedMediaFile(host=host, media_id='xxx'):
#		#		
#		#		#img=_param['img']; listitem={}; My_infoLabels=[]
#		#		#My_infoLabels['host']=host
#		#		#My_infoLabels['title']=oldTitle
#		#		#_addon.add_directory({'section': section, 'img': _param['img'], 'mode': 'PlayVideo', 'url': url, 'infoLabels': My_infoLabels, 'listitem': listitem}, {'title':  name}, img=img, is_folder=False);
#		#		oList.append(r4)
#		#		hList.append(host)
#	print 'oList'
#	print oList
#	print 'hList'
#	print hList
#	##media =urlresolver.HostedMediaFile(host=host, media_id=linkid, title=vidname + ' - ' + host + ' - ' + load + ' - ' + working)sources.append(media)
#	source=urlresolver.choose_source(oList)
#	iL={}
#	iL['title']=oldTitle
#	iL['studio']='CLE'
#	print source
#	PlayVideo(source,iL)
#	#PlayVideo(source['url'],iL)
#	#PlayVideo(source,{ 'title': oldTitle, 'studio': 'CLE'	 },[])
#	#if (hList==[]) or (oList==[]): eod(); return
#	#r=askSelection(option_list=hList,txtHeader='Select A Video Source:')
#	#if (r) and (r is not '') and (r is not False) and (r is not 'none'):
#	#	PlayVideo(oList[r],{ 'title': oldTitle, 'studio': host	 },[])
#	#set_view('videos',515,False)
#	#eod()

def DoVideo( url , oldTitle ):
	_addon.resolve_url(url)
	eod()
	if ('plugin://' in url):
		xbmc.executebuiltin("XBMC.RunPlugin(%s)" % url)
		return
	play=xbmc.Player(xbmc.PLAYER_CORE_AUTO) ### xbmc.PLAYER_CORE_AUTO | xbmc.PLAYER_CORE_DVDPLAYER | xbmc.PLAYER_CORE_MPLAYER | xbmc.PLAYER_CORE_PAPLAYER
	#infoLabels={ "Studio":  "CLE", "ShowTitle": oldTitle, "Title": oldTitle }
	infoLabels={ "Studio": addpr('studio',''), 'Title': addpr('title','') }
	li=xbmcgui.ListItem(_param['title'], iconImage=_param['img'], thumbnailImage=_param['img'])
	li.setInfo(type="Video", infoLabels=infoLabels ); li.setProperty('IsPlayable', 'true')
	play.play(url, li); xbmcplugin.setResolvedUrl(handle=int(sys.argv[1]), succeeded=True, listitem=li)



##### Menus #####
def Menu_LoadCategories(section=_default_section_): #Categories
	WhereAmI('@ the Category Menu')
	chtml=getURL(ps('_domain_url_cat'))
	chtml2=chtml.split('<div class="w-text ">Video Channels</div>')[1]
	cats=re.compile('<li style=".+?">[\n]\s+<a href="(.+?)">[\n]\s+<b>(.+?) \((\d+)\)</b>[\n]\s+</a>[\n]\s+</li>', re.MULTILINE | re.IGNORECASE | re.DOTALL).findall(chtml2)
	cats=sorted(cats, key=lambda cat: cat[2], reverse=True)
	### ( Cat_Url ,Cat_Name, Video_Count )
	if (not cats): eod(); return
	try:		AllCount=re.compile('<span style=".+?">\d+ - \d+ of (\d+) Videos', re.MULTILINE | re.IGNORECASE | re.DOTALL).findall(chtml)[0]
	except:	AllCount='??'
	_addon.add_directory({'mode': 'GetTitles', 'section': 'all', 'url': ps('_domain_url_cat') },{'title':  cFL('['+cFL(iFL(AllCount+' Videos '),ps('cFL_color6'))+']',ps('cFL_color'))+'  '+cFL('A',ps('cFL_color'))+'ll'},img=_artIcon, fanart=_artFanart)
	for (cat_url,cat_name,video_count) in cats:
		if (len(video_count)==1): video_count='0'+video_count
		_addon.add_directory({'mode': 'GetTitles', 'section': cat_name, 'url': cat_url },{'title':  cFL('['+cFL(iFL(video_count+' Videos '),ps('cFL_color6'))+']',ps('cFL_color'))+'  '+cFL(cat_name[0:1],ps('cFL_color'))+cat_name[1:]},img=_artIcon, fanart=_artFanart)
	#
	set_view('list',515,False)
	eod()
	#

def Menu_MainMenu(): #The Main Menu
	WhereAmI('@ the Main Menu')
	_addon.add_directory({'mode': 'LoadCategories', 'section': ''},{'title':  cFL('V',ps('cFL_color'))+'ideos'},img=_artIcon, fanart=_artFanart)
	#
	#
	#
	_addon.add_directory({'mode': 'ResolverSettings'}, {'title':  cFL('U',ps('cFL_color'))+'rl-Resolver Settings'},is_folder=False		,img=_artIcon	,fanart=_artFanart)
	_addon.add_directory({'mode': 'Settings'}, 				 {'title':  cFL('P',ps('cFL_color'))+'lugin Settings'}					,is_folder=False		,img=_artIcon							,fanart=_artFanart)
	_addon.add_directory({'mode': 'TextBoxFile', 'title': "[COLOR cornflowerblue]Local Change Log:[/COLOR]  %s"  % (__plugin__), 'url': ps('changelog.local')}, {'title': cFL('L',ps('cFL_color'))+'ocal Change Log'},					img=_artIcon,is_folder=False,fanart=_artFanart)
	#_addon.add_directory({'mode': 'TextBoxUrl',  'title': "[COLOR cornflowerblue]Latest Change Log:[/COLOR]  %s" % (__plugin__), 'url': ps('changelog.url')}, 	{'title': cFL('L',ps('cFL_color'))+'atest Online Change Log'},	img=art('thechangelog','.jpg'),is_folder=False,fanart=_artFanart)
	#_addon.add_directory({'mode': 'TextBoxUrl',  'title': "[COLOR cornflowerblue]Latest News:[/COLOR]  %s"       % (__plugin__), 'url': ps('news.url')}, 				{'title': cFL('L',ps('cFL_color'))+'atest Online News'},				img=_art404										,is_folder=False,fanart=_artFanart)
	### ############ 
	eod()
	### ############ 
	### _addon.show_countdown(9000,'Testing','Working...') ### Time seems to be in seconds.

##### /\ ##### Menus #####
### ############################################################################################################
### ############################################################################################################
### ############################################################################################################







### ############################################################################################################
### ############################################################################################################
### ############################################################################################################
##### Modes #####
def check_mode(mode=''):
	deb('Mode',mode)
	if (mode=='') or (mode=='main') or (mode=='MainMenu'): 
		#initDatabase()
		Menu_MainMenu()
	elif (mode=='PlayVideo'): 						PlayVideo(_param['url'], _param['infoLabels'], _param['listitem'])
	elif (mode=='Settings'): 							_addon.addon.openSettings() #_plugin.openSettings()
	elif (mode=='ResolverSettings'): 			urlresolver.display_settings()
	elif (mode=='LoadCategories'): 				Menu_LoadCategories(_param['section'])
	##elif (mode=='BrowseAtoZ'): 					BrowseAtoZ(_param['section'])
	#elif (mode=='BrowseYear'): 						Menu_BrowseByYear(_param['section'])
	#elif (mode=='BrowseGenre'): 					Menu_BrowseByGenre(_param['section'])
	#elif (mode=='BrowseCountry'): 				Menu_BrowseByCountry(_param['section'])
	#elif (mode=='BrowseLatest'): 				BrowseLatest(_param['section'])
	#elif (mode=='BrowsePopular'): 				BrowsePopular(_param['section'])
	##elif (mode=='GetResults'): 					GetResults(_param['section'], genre, letter, page)
	elif (mode=='GetTitles'): 						ListItems(_param['section'], _param['url'], _param['pageno'], _param['pagecount'], _param['title'])
	#elif (mode=='GetTitlesLatest'): 			listItems(_param['section'], _param['url'], _param['pageno'], _param['pagecount'], _param['genre'], _param['year'], _param['title'], chck=ps('LI.tv.latest.check'))
	#elif (mode=='GetTitlesPopular'): 			listItems(_param['section'], _param['url'], _param['pageno'], _param['pagecount'], _param['genre'], _param['year'], _param['title'], chck=ps('LI.tv.popular.all.check'))
	#elif (mode=='GetTitlesHDPopular'): 		listItems(_param['section'], _param['url'], _param['pageno'], _param['pagecount'], _param['genre'], _param['year'], _param['title'], chck=ps('LI.movies.popular.hd.check'))
	#elif (mode=='GetTitlesOtherPopular'): listItems(_param['section'], _param['url'], _param['pageno'], _param['pagecount'], _param['genre'], _param['year'], _param['title'], chck=ps('LI.movies.popular.other.check'))
	#elif (mode=='GetTitlesNewPopular'): 	listItems(_param['section'], _param['url'], _param['pageno'], _param['pagecount'], _param['genre'], _param['year'], _param['title'], chck=ps('LI.movies.popular.new.check'))
	#elif (mode=='GetLinks'): 							listLinks(_param['section'], _param['url'], showtitle=_param['showtitle'], showyear=_param['showyear'])
	elif (mode=='GetVideos'): 						ListLinks(_param['section'], _param['url'], _param['title'])
	#elif (ode=='GetLinks'): 							listLinks(_param['section'], _param['url'], showtitle=_param['showtitle'], showyear=_param['showyear'])
	#elif (mode=='GetSeasons'): 						listSeasons(_param['section'], _param['url'], _param['img'])
	#elif (mode=='GetEpisodes'): 					listEpisodes(_param['section'], _param['url'], _param['img'], _param['season'])
	elif (mode=='TextBoxFile'): 					TextBox2().load_file(_param['url'],_param['title']); eod()
	elif (mode=='TextBoxUrl'):  					TextBox2().load_url( _param['url'],_param['title']); eod()
	#elif (mode=='SearchForAirDates'):  		search_for_airdates(_param['title']); eod()
	#elif (mode=='Search'):  							doSearchNormal(_param['section'],_param['title'])
	#elif (mode=='AdvancedSearch'):  			doSearchAdvanced(_param['section'],_param['title'])
	#elif (mode=='FavoritesList'):  		  	fav__list(_param['section'],_param['subfav'])
	#elif (mode=='FavoritesEmpty'):  	 		fav__empty(_param['section'],_param['subfav'])
	#elif (mode=='FavoritesRemove'):  			fav__remove(_param['section'],_param['title'],_param['year'],_param['subfav'])
	#elif (mode=='FavoritesAdd'):  		  	fav__add(_param['section'],_param['title'],_param['year'],_param['img'],_param['fanart'],_param['subfav'])
	elif (mode=='sunNote'):  		   				sunNote( header=_param['title'],msg=_param['plot'])
	elif (mode=='deadNote'):  		   			deadNote(header=_param['title'],msg=_param['plot'])
	elif (mode=='0'):											DoVideo( _param['url'],_param['title'])
	elif (mode=='DoVideo'):								DoVideo( _param['url'],_param['title'])
	else: 
		deadNote(header='Mode:  "'+mode+'"',msg='[ mode ] not found.')
		#initDatabase()
		Menu_MainMenu()

##### /\ ##### Modes #####
### ############################################################################################################
deb('param >> mode',_param['mode'])
deb('param >> title',_param['title'])
deb('param >> url',_param['url']) ### Simply Logging the current query-passed / param -- URL
check_mode(_param['mode']) ### Runs the function that checks the mode and decides what the plugin should do. This should be at or near the end of the file.
### ############################################################################################################
### ############################################################################################################
### ############################################################################################################
