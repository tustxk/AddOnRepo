# -*- coding: utf-8 -*-
import urllib,urllib2,re,random,xbmcplugin,xbmcgui,xbmcaddon,cookielib,HTMLParser,datetime
from time import gmtime, strftime

urllib2.socket.setdefaulttimeout(30)
try:
	import StorageServer
except:
	import storageserverdummy as StorageServer
cache = StorageServer.StorageServer("zdf_new", 24)

html_parser = HTMLParser.HTMLParser()

month = strftime("%m", gmtime())
year = strftime("%Y", gmtime())

addon = xbmcaddon.Addon()
addonID = addon.getAddonInfo('id')


__settings__ = xbmcaddon.Addon(id='plugin.video.zdf_new')
__language__ = __settings__.getLocalizedString


COOKIEFILE = xbmc.translatePath(__settings__.getAddonInfo('profile')+"cookies.lwp")

showSubtitles = __settings__.getSetting("showSubtitles") == "true"
pluginhandle = int(sys.argv[1])

baseUrl = "http://www.zdf.de"
fallbackImage = "http://www.zdf.de/ZDFmediathek/img/fallback/946x532.jpg"

if __settings__.getSetting("firstrun") != 'false':
	__settings__.setSetting(id="firstrun",value='false')


if __settings__.getSetting("view") == '0':
	channel_as_icon = False
	forceViewMode = True
	add_channel_to_plot = True
	viewMode = '504'
	thumAsFanart = True

elif __settings__.getSetting("view") == '1':
	viewMode = '515'
	channel_as_icon = True
	forceViewMode = True
	add_channel_to_plot = False
	thumAsFanart = True

elif __settings__.getSetting("view") == '2':
	viewMode = '500'
	channel_as_icon = False
	forceViewMode = True
	add_channel_to_plot = True
	thumAsFanart = True

elif __settings__.getSetting("view") == '3':#todo
	channel_as_icon = False
	forceViewMode = False
	add_channel_to_plot = True
	#viewMode = '500'
	thumAsFanart = False

else:
	channel_as_icon = False
	forceViewMode = False
	add_channel_to_plot = True
	#viewMode = '500'
	thumAsFanart = True


def MAIN():
	addDir('Startseite','Startseite',12)
	addDir('Nachrichten','Nachrichten',13)
	#addDir('Sendung verpasst?','TODO',1)
	addDir('Live','http://www.zdf.de/ZDFmediathek/xmlservice/web/live?maxLength=50',2)#http://www.zdf.de/ZDFmediathek/xmlservice/web/beitragsDetails?ak=web&id=1822600
	addDir('Sendungen A-Z','abisz',1)
	addDir('Rubriken','http://www.zdf.de/ZDFmediathek/xmlservice/web/rubriken',2)
	addDir('Thema','http://www.zdf.de/ZDFmediathek/xmlservice/web/themen',2)
	#addDir('sender','http://www.zdf.de/ZDFmediathek/xmlservice/web/senderliste?ak=web&details=true',2)
	addDir('Specials','special',14)
	
	#addDir(__language__(30003),mainurl,4,'',__language__(30004))
	#LIST_VIDEOCENTER(mainurl)
	xbmcplugin.endOfDirectory(int(sys.argv[1]))

	
def listAZ():#1
	addDir("ABC", baseUrl+"/ZDFmediathek/xmlservice/web/sendungenAbisZ?characterRangeEnd=C&detailLevel=2&characterRangeStart=A", 2)
	addDir("DEF", baseUrl+"/ZDFmediathek/xmlservice/web/sendungenAbisZ?characterRangeEnd=F&detailLevel=2&characterRangeStart=D", 2)
	addDir("GHI", baseUrl+"/ZDFmediathek/xmlservice/web/sendungenAbisZ?characterRangeEnd=I&detailLevel=2&characterRangeStart=G", 2)
	addDir("JKL", baseUrl+"/ZDFmediathek/xmlservice/web/sendungenAbisZ?characterRangeEnd=L&detailLevel=2&characterRangeStart=J", 2)
	addDir("MNO", baseUrl+"/ZDFmediathek/xmlservice/web/sendungenAbisZ?characterRangeEnd=O&detailLevel=2&characterRangeStart=M", 2)
	addDir("PQRS", baseUrl+"/ZDFmediathek/xmlservice/web/sendungenAbisZ?characterRangeEnd=S&detailLevel=2&characterRangeStart=P", 2)
	addDir("TUV", baseUrl+ "/ZDFmediathek/xmlservice/web/sendungenAbisZ?characterRangeEnd=V&detailLevel=2&characterRangeStart=T", 2)
	addDir("WXYZ", baseUrl+"/ZDFmediathek/xmlservice/web/sendungenAbisZ?characterRangeEnd=Z&detailLevel=2&characterRangeStart=W", 2)
	addDir("0-9", baseUrl+"/ZDFmediathek/xmlservice/web/sendungenAbisZ?detailLevel=2&characterRangeStart=0%2D9&characterRangeEnd=0%2D9", 2)
	xbmcplugin.endOfDirectory(int(sys.argv[1]))

def START():#12
	addDir('Unsere Tipps','http://www.zdf.de/ZDFmediathek/xmlservice/web/tipps?maxLength=50&id=%5FSTARTSEITE',2)
	addDir('Aktuell','http://www.zdf.de/ZDFmediathek/xmlservice/web/aktuellste?maxLength=50&id=%5FSTARTSEITE',2)
	addDir('Meist gesehen','http://www.zdf.de/ZDFmediathek/xmlservice/web/meistGesehen?maxLength=50&id=%5FGLOBAL',2)
	xbmcplugin.endOfDirectory(int(sys.argv[1]))

def NACHRICHTEN():#13
	addDir('Aktuell','http://www.zdf.de/ZDFmediathek/xmlservice/web/aktuellste?maxLength=50&id=%5FNACHRICHTEN',2)
	addDir('Ganze Sendungen','http://www.zdf.de/ZDFmediathek/xmlservice/web/ganzeSendungen',2)
	addDir('Meist gesehen','http://www.zdf.de/ZDFmediathek/xmlservice/web/meistGesehen?maxLength=50&id=%5FNACHRICHTEN',2)
	xbmcplugin.endOfDirectory(int(sys.argv[1]))

def SPECIALS():#14
	addDir('3D Videos','http://www.zdf.de/ZDFmediathek/xmlservice/web/detailsSuche?maxLength=50&searchString=side%20by%20side&ak=web',2)
	addDir('Filme','http://www.zdf.de/ZDFmediathek/xmlservice/web/aktuellste?maxLength=50&id=1829656',2)
	addDir('Serien','http://www.zdf.de/ZDFmediathek/xmlservice/web/aktuellste?maxLength=50&id=1859968',2)
	addDir('HD','http://www.zdf.de/ZDFmediathek/xmlservice/web/detailsSuche?maxLength=50&ak=web&searchString=*&properties=HD',2)
	xbmcplugin.endOfDirectory(int(sys.argv[1]))
	

def listShows(listurl):#2
	if '&offset=' in listurl:
		i,stuff = cache_list_stored()
	else:
		stuff = ''
		i = 0
		cache_clear()
		
	response = getUrl(listurl)
	match_teasers=re.compile('<teasers>(.+?)</teasers>', re.DOTALL).findall(response)
	match_teaser=re.compile('<teaser(.+?)</teaser>', re.DOTALL).findall(match_teasers[0])
	for teaser in match_teaser:
		match_member=re.compile('member="(.+?)"', re.DOTALL).findall(teaser)
		match_type=re.compile('<type>(.+?)</type>', re.DOTALL).findall(teaser)
		match_teaserimages=re.compile('<teaserimages>(.+?)</teaserimages>', re.DOTALL).findall(teaser)
		thumb = chooseThumb(match_teaserimages[0])
		match_information=re.compile('<information>(.+?)</information>', re.DOTALL).findall(teaser)
		title,plot=getInfo(match_information[0])
		match_details=re.compile('<details>(.+?)</details>', re.DOTALL).findall(teaser)
		assetId,channel,length,channelLogo,airtime,timetolive,fsk,hasCaption,url=getDetails(match_details[0])
		title = cleanTitle(title)
		type = match_type[0]

		if type == 'sendung' and length != '0':
			stuff = stuff + addDir(title + ' (' + length + ')',baseUrl+'/ZDFmediathek/xmlservice/web/aktuellste?maxLength=50&id='+assetId,2,thumb,plot,channel)
		elif type == 'video':
			stuff = stuff + addLink(title,assetId,3,thumb,plot,length,airtime,timetolive,fsk,hasCaption,channel=channel)
		#elif type == 'imageseries_informativ':#TODO
		#	addLink(title,assetId,3,thumb,plot,length,airtime,timetolive,fsk,hasCaption)
		elif type == 'rubrik' and length != '0':
			stuff = stuff + addDir(title + ' (' + length + ')',baseUrl+'/ZDFmediathek/xmlservice/web/aktuellste?maxLength=50&ak=web&id='+assetId,2,thumb,plot,channel)
		elif type == 'topthema' or type == 'thema' and length != '0':
			stuff = stuff + addDir(title + ' (' + length + ')',baseUrl+'/ZDFmediathek/xmlservice/web/aktuellste?maxLength=50&ak=web&id='+assetId,2,thumb,plot,channel)
		elif type == 'sender' and length != '0':
			stuff = stuff + addDir(title + ' (' + length + ')',baseUrl+'/ZDFmediathek/xmlservice/web/aktuellste?maxLength=50&ak=web&id='+assetId,2,thumb,plot,channel)
		elif type == 'livevideo':
			if match_member[0] == 'onAir':
				stuff = stuff + addLink(title,assetId,3,thumb,plot,0,airtime,timetolive,fsk,hasCaption,channel=channel)
				
		else:
			print 'unknown type: '+type
	
	cache_store(stuff)
	
	if '<additionalTeaser>true</additionalTeaser>' in response:
		if '&offset=' in listurl:
			split = listurl.split('&offset=')
			org_offset = split[1]
			if org_offset != '100':
				offset = str(int(org_offset) + 50)
				
				newurl = listurl.replace('&offset='+org_offset,'&offset='+offset)
				#the api is limited :/
				addDir('More',newurl,2)
		else:
			addDir('More',listurl+'&offset=50',2)
		
	if '&offset=' in listurl:
		if __settings__.getSetting('back_hidden') != 'true':
			i = i + 1
		try:
			wnd = xbmcgui.Window(xbmcgui.getCurrentWindowId())
			wnd.getControl(wnd.getFocusId()).selectItem(i)
			

		except:
			log('focusing not possible')
		
		xbmcplugin.endOfDirectory(int(sys.argv[1]), updateListing=True)
	else:
		xbmcplugin.endOfDirectory(int(sys.argv[1]))

	if forceViewMode == True:

		xbmc.executebuiltin('Container.SetViewMode('+viewMode+')')

		
		
def getDetails(details):
	try:
		match_assetId=re.compile('<assetId>(.+?)</assetId>', re.DOTALL).findall(details)
		assetId = match_assetId[0]
	except:
		assetId = ''
	
	try:
		match_channel=re.compile('<channel>(.+?)</channel>', re.DOTALL).findall(details)
		channel = match_channel[0]
	except:
		channel = ''
	
	try:
		match_length=re.compile('<length>(.+?)</length>', re.DOTALL).findall(details)
		length = match_length[0]
		if ' min ' in length:
			l = length.split(' min ')
			length = int(l[0]) * 60 + int(l[1])
		elif ' min' in length:
			l = length.replace(' min','')
			length = int(l) * 60
		elif '.000' in length:#get seconds
			length = length.replace('.000','')
			l = length.split(':')
			length = int(l[0]) * 3600 + int(l[1]) * 60 + int(l[2])
	except:
		length = '0'
		
	try:
		match_channelLogoSmall=re.compile('<channelLogoSmall>(.+?)</channelLogoSmall>', re.DOTALL).findall(details)
		channelLogo = match_channelLogoSmall[0]
	except:
		channelLogo = '0'
		
	try:
		match_airtime=re.compile('<airtime>(.+?)</airtime>', re.DOTALL).findall(details)
		airtime = match_airtime[0]
	except:
		airtime = '0'
		
	try:
		match_timetolive=re.compile('<timetolive>(.+?)</timetolive>', re.DOTALL).findall(details)
		timetolive = match_timetolive[0]
	except:
		timetolive = '0'
		
	try:
		match_fsk=re.compile('<fsk>(.+?)</fsk>', re.DOTALL).findall(details)
		fsk = match_fsk[0]
	except:
		fsk = ''
	
	try:
		match_hasCaption=re.compile('<hasCaption>(.+?)</hasCaption>', re.DOTALL).findall(details)
		hasCaption = match_hasCaption[0]
	except:
		hasCaption = '0'
		
	try:
		match_vcmsUrl=re.compile('<vcmsUrl>(.+?)</vcmsUrl>', re.DOTALL).findall(details)
		url = match_vcmsUrl[0]
	except:
		url = ''
	
	return assetId,channel,length,channelLogo,airtime,timetolive,fsk,hasCaption,url
	
def getInfo(infos):
	match_title=re.compile('<title>(.+?)</title>', re.DOTALL).findall(infos)
	try:
		match_detail=re.compile('<detail>(.+?)</detail>', re.DOTALL).findall(infos)
		return match_title[0],match_detail[0]
	except:
		return match_title[0],''
	
def chooseThumb(images):
	thumb = fallbackImage
	height = 0
	width = 0
	match_images=re.compile('<teaserimage.+?key="(.+?)x(.+?)">(.+?)</teaserimage>', re.DOTALL).findall(images)
	for h,w,image in match_images:
		if not "fallback" in image:
			if int(h) > height or int(w) > width:
				height = int(h)
				width = int(w)
				thumb = image
	return thumb
	
def cleanTitle(title):
	title = title.replace('&amp;','&')
	return title

#def playVideo(id):
def playVideo(url):
    id = url
    content = getUrl(baseUrl+"/ZDFmediathek/xmlservice/web/beitragsDetails?id="+id)
    match0 = re.compile('<formitaet basetype="h264_aac_mp4_rtmp_zdfmeta_http" isDownload="false">.+?<quality>hd</quality>.+?<url>(.+?)</url>', re.DOTALL).findall(content)
    match1 = re.compile('<formitaet basetype="h264_aac_mp4_rtmp_zdfmeta_http" isDownload="false">.+?<quality>veryhigh</quality>.+?<url>(.+?)</url>', re.DOTALL).findall(content)
    match2 = re.compile('<formitaet basetype="h264_aac_mp4_rtmp_zdfmeta_http" isDownload="false">.+?<quality>high</quality>.+?<url>(.+?)</url>', re.DOTALL).findall(content)
    match3 = re.compile('<formitaet basetype="h264_aac_ts_http_m3u8_http" isDownload="false">.+?<quality>high</quality>.+?<url>(.+?)</url>', re.DOTALL).findall(content)
    matchUT = re.compile('<caption>.+?<url>(.+?)</url>', re.DOTALL).findall(content)
    url = ""
    if content.find("<type>livevideo</type>") >= 0:
        if match3:
            url = match3[0]
    elif content.find("<type>video</type>") >= 0:
        if match0:
            url = match0[0]
        elif match1:
            url = match1[0]
        elif match2:
            url = match2[1]
        if "http://" in url:
            content2 = getUrl(url)
            match = re.compile('<default-stream-url>(.+?)</default-stream-url>', re.DOTALL).findall(content2)
            url = match[0]
    if channel_as_icon:
        listitem = xbmcgui.ListItem(path=url)#, thumbnailImage=chooseThumb(content))
    else:
        listitem = xbmcgui.ListItem(path=url)
    xbmcplugin.setResolvedUrl(pluginhandle, True, listitem)
    if showSubtitles and matchUT:
        setSubtitle(matchUT[0])


def setSubtitle(url):
    if os.path.exists(subFile):
        os.remove(subFile)
    try:
        content = getUrl(url)
    except:
        content = ""
    if content:
        matchLine = re.compile('<p begin="(.+?)" end="(.+?)".+?>(.+?)</p>', re.DOTALL).findall(content)
        fh = open(subFile, 'a')
        count = 1
        for begin, end, line in matchLine:
            begin = float(begin)
            beginS = str(round(begin%60, 1)).replace(".",",")
            if len(beginS.split(",")[0])==1:
                beginS = "0"+beginS
            beginM = str(int(begin)/60)
            if len(beginM)==1:
                beginM = "0"+beginM
            beginH = str(int(begin)/60/60)
            if len(beginH)==1:
                beginH = "0"+beginH
            begin = beginH+":"+beginM+":"+beginS
            end = float(end)
            endS = str(round(end%60, 1)).replace(".",",")
            if len(endS.split(",")[0])==1:
                endS = "0"+endS
            endM = str(int(end)/60)
            if len(endM)==1:
                endM = "0"+endM
            endH = str(int(end)/60/60)
            if len(endH)==1:
                endH = "0"+endH
            end = endH+":"+endM+":"+endS
            match = re.compile('<span(.+?)>', re.DOTALL).findall(line)
            for span in match:
                line = line.replace("<span"+span+">","")
            line = line.replace("<br />","\n").replace("</span>","").strip()
            fh.write(str(count)+"\n"+begin+" --> "+end+"\n"+cleanTitle(line)+"\n\n")
            count+=1
        fh.close()
        xbmc.sleep(1000)
        xbmc.Player().setSubtitles(subFile)
		
def cache_store(stuff,name=''):
	stuff = stuff.decode('utf-8')
	"""
	stuff = stuff.replace('ä','&auml;')
	stuff = stuff.replace('Ä','&Auml;')
	stuff = stuff.replace('ö','&ouml;')
	stuff = stuff.replace('Ö','&Ouml;')
	stuff = stuff.replace('ü','&uuml;')
	stuff = stuff.replace('Ü','&Uuml;')
	stuff = stuff.replace('ß','&szlig;')
	stuff = stuff.replace('\n','&newline')
	"""
	cache.table_name = "nhltable"
	log('store: '+stuff)
	#cache.set('test', urllib.quote_plus(stuff))
	cache.set('cache', stuff)
	return True
	
def cache_recall(name=''):
	cache.table_name = "nhltable"
	stuff = cache.get('cache')
	stuff = stuff.encode("utf-8")
	"""
	stuff = stuff.replace('&auml;','ä')
	stuff = stuff.replace('&Auml;','Ä')
	stuff = stuff.replace('&ouml;','ö')
	stuff = stuff.replace('&Ouml;','Ö')
	stuff = stuff.replace('&uuml;','ü')
	stuff = stuff.replace('&Uuml;','Ü')
	stuff = stuff.replace('&szlig;','ß')
	stuff = stuff.replace('&newline','\n')
	"""
	log('recall: '+stuff)
	return stuff
	
	
def cache_list_stored():
	i = 0
	recalled = cache_recall()
	match_stored=re.compile('<s(.+?)</s>', re.DOTALL).findall(cache_recall())
	for s in match_stored:
		i = i + 1
		if 'type="vid">' in s:
			name,url,mode,thumb,plot,length,airtime,timetolive,fsk,hasCaption,networkicon,channelId,otherChannels=s.split('|')
			addLink(name.replace('type="vid">',''),url,int(mode),thumb,plot,int(length),airtime,timetolive,fsk,hasCaption,networkicon,channelId,otherChannels)
		elif 'type="dir">' in s:
			name,url,mode,thumb,plot=s.split('|')
			addDir(name.replace('type="dir">',''),url,mode,thumb,plot)
	return i,recalled
	
def cache_clear():
	cache.table_name = "nhltable"
	cache.delete("cache")
	
def searchbox():
	searchStr = ''
	keyboard = xbmc.Keyboard(searchStr,'Search')
	keyboard.doModal()
	if (keyboard.isConfirmed() == 'false'):
		return
	searchStr = keyboard.getText().replace(' ','%20')
	if len(searchStr) == 0:
		return
	else:
		return searchStr
		

def getUrl( url , extraheader=True):
	log('getting page: ' + url)
	cj = cookielib.LWPCookieJar()
	if os.path.isfile(COOKIEFILE):
		cj.load(COOKIEFILE, ignore_discard=True)

	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
	opener.addheaders = [('User-Agent', 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2;)')]
	usock=opener.open(url)
	response=usock.read()
	usock.close()
	cj.save(COOKIEFILE, ignore_discard=True)
	return response
	

def log(message):
	if xbmcplugin.getSetting(pluginhandle,"debug") == 'true':
		try:
			print "#####ZDF Debug: "+unicode(message)
		except:
			print "#####ZDF Debug: unicode from HELL"
	return


def get_params():
	param=[]
	paramstring=sys.argv[2]
	if len(paramstring)>=2:
		params=sys.argv[2]
		cleanedparams=params.replace('?','')
		if (params[len(params)-1]=='/'):
			params=params[0:len(params)-2]
		pairsofparams=cleanedparams.split('&')
		param={}
		for i in range(len(pairsofparams)):
			splitparams={}
			splitparams=pairsofparams[i].split('=')
			if (len(splitparams))==2:
				param[splitparams[0]]=splitparams[1]
								
	return param



def addLink(name,url,mode,iconimage,plot='',duration=False,airtime='',timetolive=False,fsk='18',hasCaption=False,channelId='526',otherChannels='',channel=''):
	to_store = '<s type="vid">'+name+'|'+url+'|'+str(mode)+'|'+iconimage+'|'+plot+'|'+str(duration)+'|'+airtime+'|'+timetolive+'|'+fsk+'|'+hasCaption+'|'+channel+'|'+channelId+'|'+otherChannels+'</s>'
	if fsk != '' and int(fsk) >= 16:
		name = name + ' (ab 22:00)'
	if xbmcplugin.getSetting(pluginhandle,"description") == 'true' and not plot == '':
		name = name + ' - ' + plot
	if timetolive:
		plot = plot + '\n\nVerfügbar bis: '+timetolive
	if channel and add_channel_to_plot:
		plot = plot + '\n\nSender: '+channel
	thumbnailImage = select_icon(channel,iconimage)
	if thumAsFanart:
		fanart = iconimage
	else:
		fanart = fallbackImage
	
		
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
	ok=True
	#liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
	liz=xbmcgui.ListItem(name, iconImage=thumbnailImage, thumbnailImage=thumbnailImage)
	#liz.setInfo( type="Video", infoLabels={ "Title": name , "Plot": plot , "Plotoutline": plot , "Duration": duration } )
	liz.setInfo( type="Video", infoLabels={ "Title": name , "Plot": plot , "Plotoutline": plot , "Mpaa": 'FSK ' + fsk , "Premiered": airtime} )
	liz.addStreamInfo('video', { 'codec': 'h264', 'width':960, 'height' : 540, 'duration' : int(duration) })

	commands = []
	
	if hasCaption:
		liz.addStreamInfo('subtitle', { 'language': 'de' })
	if channelId:
		commands.append(('Weitere Beitraege', 'RunPlugin('+sys.argv[0]+'?mode=2&url='+urllib.quote_plus('http://www.zdf.de/ZDFmediathek/xmlservice/web/weitereBeitraege?id='+channelId    +'&maxLength=50')+')',))
		#liz.addContextMenuItems([('Weitere Beitraege', 'RunPlugin(plugin://'+addonID+'/?mode=2&url='+urllib.quote_plus('http://www.zdf.de/ZDFmediathek/xmlservice/web/weitereBeitraege?id='+channelId    +'&maxLength=50')+')',)])
		#liz.addContextMenuItems([('Weitere Beitraege', 'RunPlugin(plugin://'+'plugin.video.zdf_new)',)])
	#if otherChannels != '':
	#	liz.addContextMenuItems(['Aehnliche Videos',   'RunPlugin(plugin://'+'plugin.video.zdf_new'+'/?mode=2&url='+urllib.quote_plus('http://www.zdf.de/ZDFmediathek/xmlservice/web/weitereBeitraege?id='+otherChannels+'&maxLength=50')+')',)])
	liz.addContextMenuItems(commands)
	liz.setProperty('IsPlayable', 'true')
	liz.setProperty('fanart_image',fanart)
	#liz.setProperty('Icon',networkicon)
	#liz.setProperty('Mpaa','FSK18')
	liz.setProperty('Premiered',airtime)
	xbmcplugin.setContent( handle=int( sys.argv[ 1 ] ), content="movies" )
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz)
	return to_store

def addDir(name,url,mode,iconimage=fallbackImage,plot='',channel=False):
	to_store = '<s type="dir">'+name+'|'+url+'|'+str(mode)+'|'+iconimage+'|'+plot+'</s>'
	if xbmcplugin.getSetting(pluginhandle,"description") == 'true' and not plot == '':
		name = name + ' - ' + plot
	if channel and add_channel_to_plot:
		plot = plot + '\n\nSender: '+channel
	if thumAsFanart:
		fanart = iconimage
	else:
		fanart = fallbackImage
	thumbnailImage = select_icon(channel,iconimage)
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
	ok=True
	#liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=thumbnailImage)
	liz=xbmcgui.ListItem(name, iconImage="http://www.zdf.de/ZDFmediathek/contentblob/1209114/tImg/8280929", thumbnailImage=thumbnailImage)
	liz.setInfo( type="Video", infoLabels={ "Title": name , "Plot": plot , "Plotoutline": plot } )
	liz.setProperty('fanart_image',fanart)
	xbmcplugin.setContent( handle=int( sys.argv[ 1 ] ), content="movies" )
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
	return to_store

def select_icon(channel,iconimage):
	if channel_as_icon:
		if channel == 'ZDF':
			#thumbnailImage = 'http://www.zdf.de/ZDFmediathek/contentblob/1822600/timg298x168blob/8339542'
			return 'http://www.zdf.de/ZDFmediathek/contentblob/1209114/tImg/8280929'
		elif channel == 'ZDFinfo':
			#thumbnailImage = 'http://www.zdf.de/ZDFmediathek/contentblob/1822586/timg298x168blob/8340364'
			return 'http://www.zdf.de/ZDFmediathek/contentblob/1209120/tImg/5026474'
		elif channel == 'ZDFneo':
			#thumbnailImage = 'http://www.zdf.de/ZDFmediathek/contentblob/1822440/timg298x168blob/8339473'
			return 'http://www.zdf.de/ZDFmediathek/contentblob/1209122/tImg/8782107'
		elif channel == 'ZDF.kultur':
			#thumbnailImage = 'http://www.zdf.de/ZDFmediathek/contentblob/1822544/timg298x168blob/8339490'
			return 'http://www.zdf.de/ZDFmediathek/contentblob/1317640/tImg/8780754'
		elif channel == '3sat':
			#thumbnailImage = iconimage
			return 'http://www.zdf.de/ZDFmediathek/contentblob/1209116/tImg/8325967'
		else:
			return fallbackImage
	else:
		return iconimage
			  
params=get_params()
url=None
name=None
thumb=None
mode=None
fanart=None

try:
		url=urllib.unquote_plus(params["url"])
except:
		pass
try:
		name=urllib.unquote_plus(params["name"])
except:
		pass
try:
		thumb=urllib.unquote_plus(params["thumb"])
except:
		pass
try:
		mode=int(params["mode"])
except:
		pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)

if mode==None or url==None or len(url)<1:
	print ""
	MAIN()

elif mode==1:
	print ""+url
	listAZ()
		
elif mode==2:
	print ""+url
	listShows(url)
		
elif mode == 3:
	playVideo(url)
	
elif mode == 12:
	START()

elif mode == 13:
	NACHRICHTEN()
	
elif mode == 14:
	SPECIALS()
	
#xbmcplugin.endOfDirectory(int(sys.argv[1]))
