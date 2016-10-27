# -*- coding: utf-8 -*-
import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmcaddon,string,random,cookielib

try:
	import StorageServer
except:
	import storageserverdummy as StorageServer
cache = StorageServer.StorageServer("laola", 24)

cache.table_name = "testtable"


pluginhandle = int(sys.argv[1])

update_view = False

__settings__ = xbmcaddon.Addon(id='plugin.video.laola1live')
__language__ = __settings__.getLocalizedString

language = __language__(30214 + int(__settings__.getSetting('language')))
location = __language__(30208 + int(__settings__.getSetting('location')))

#language = 'de'
#location = 'de'

baseurl = 'http://www.laola1.tv/'+language+'-'+location

#baseurl = 'http://www.laola1.tv'
#baseurl = 'http://www.laola1.tv/de-de'




vod_quality = __settings__.getSetting('vod_quality')
if vod_quality == '0':
	max_bw = 350000
elif vod_quality == '1':
	max_bw = 600000
elif vod_quality == '2':
	max_bw = 1200000




def MAIN():
	response=getUrl(baseurl+'/home/0.html')
	#match_notifications=re.compile('<span class="notifications">(.+?)<').findall(response)
	#addDir(__language__(32001)+' ('+match_notifications[0]+')',baseurl+'/calendar/0.html',5,'')
	addDir(__language__(32001)+' ('+str(response.count('<li class="live">'))+')',baseurl+'/calendar/0.html',5,'')
	#item_latest_videos(response)
	match_all_cats=re.compile('<li class="heading">Sport Channels</li>(.+?)<li class="heading">More</li>', re.DOTALL).findall(response)
	match_cats=re.compile('<li class=" has_sub">.+?src="(.+?)".+?href="(.+?)">(.+?)<', re.DOTALL).findall(match_all_cats[0])
	for thumb,url,name in match_cats:
		name = name.replace("\n","")
		name = name.replace("	","")
		addDir(name,url,1,'')

def MAIN_NEXT(url,name):#1
	response=getUrl(url)

	#item_latest_videos(response)
	match_all_cats=re.compile('<li class="heading">Sport Channels</li>.+?'+name+'(.+?)</ul>', re.DOTALL).findall(response)
	match_cats=re.compile('src="(.+?)".+?href="(.+?)">(.+?)<', re.DOTALL).findall(match_all_cats[0])
	for thumb,url,name in match_cats:
		name = name.replace("\n","")
		addDir(name,url,2,thumb)
		
def item_latest_videos(response):
	log(response)
	clearcache()
	match_data=re.compile('<div class="stage_frame active"(.+?)>', re.DOTALL).findall(response)
	data = match_data[0]
	match_all_vids=re.compile('<span>Werbung</span>(.+?)<!-- STAGE ENDE -->', re.DOTALL).findall(response)
	
	list_vids(match_all_vids[0],data,'',0,False,False)#just stores videos

	
		
def LIST_VIDEOS(url):#2
	global update_view
	if __settings__.getSetting('back_hidden') == 'true':
		i = 0
	else:
		i = 1
	stuff = ''
	if '#just_list#' in url:
		data = url.replace('#just_list#','')
		stuff,i = list_stored()
		log(stuff)
		all_vids='nothing'
		update_view = False
	elif 'data-stageid' not in url:
		update_view = False
		response=getUrl(url)

		match_data=re.compile('<div class="stage_frame active"(.+?)>', re.DOTALL).findall(response)
		data = match_data[0]
		#match_all_vids=re.compile('<span>Werbung</span>(.+?)<!-- Querformat box ende -->', re.DOTALL).findall(response)
		match_all_vids=re.compile('<div class="stage_frame_content_live"></div>(.+?)<div class="stage_frame_content_live"></div>', re.DOTALL).findall(response)
		all_vids = match_all_vids[0]
		clearcache()
		
	else:
		update_view = True
		match_stageid=re.compile('data-stageid= "(.+?)"', re.DOTALL).findall(url)
		match_call=re.compile('data-call="(.+?)"', re.DOTALL).findall(url)
		match_htag=re.compile('data-htag="(.+?)"', re.DOTALL).findall(url)
		match_page=re.compile('data-page="(.+?)"', re.DOTALL).findall(url)
		match_startvids=re.compile('data-startvids="(.+?)"', re.DOTALL).findall(url)
		
		new_page = str( int(match_page[0]) + 1 )

		stageid = 'stageid='+match_stageid[0]
		call = '&call='+match_call[0]
		htag = '&htag='+match_htag[0]
		page = '&page='+new_page
		startvids = '&startvids='+match_startvids[0]
		anzahlblock = '&anzahlblock=11'

		post_data = stageid+call+htag+page+startvids+anzahlblock
		post_url = 'http://www.laola1.tv/de-at/nourish.php?key='+htag
		response=postUrl(post_url,post_data)
		
		data = url.replace('data-page="'+match_page[0]+'"','data-page="'+new_page+'"')
		all_vids=response
		
		##recall cached videos
		stuff = recall('stored_list')
		match_stored_vids=re.compile('<vid>(.+?)</vid>', re.DOTALL).findall(stuff)
		for vid in match_stored_vids:
			i = i + 1
			name,url,thumb=vid.split('#')
			addLink(name,url,10,thumb,'')

	list_vids(all_vids,data,stuff,i,update_view)
	
def list_stored(i=0):
	stuff = recall('stored_list')
	match_stored_vids=re.compile('<vid>(.+?)</vid>', re.DOTALL).findall(stuff)
	for vid in match_stored_vids:
		i = i + 1
		name,url,thumb=vid.split('#')
		addLink(name,url,10,thumb,'')
	return stuff,i
		

def LIST_LATEST(url):#3
	vids = recall('stored_list')
	list_vids(vids,url,'',0,False)

def list_vids(videos,data,stuff='',i=0,update_view=False,list_them=True):
	#log(videos)

	#match_some_vids=vids.split('<div class="grid')
	#match_some_vids=vids.split('<div class="overlay">')
	#match_all_vids=re.compile('<div class="stage_frame_content_live">(.+?)<div class="stage_frame_content_live">', re.DOTALL).findall(videos)
	match_some_vids=re.compile('<div class="overlay">(.+?)</div></div>', re.DOTALL).findall(videos.replace('\t','').replace('\n',''))

	for vids in match_some_vids:

		#log(some_vids)
		#split = some_vids.split('<div class="overlay">')
		#for vids in split:
		#log(vids)

		#match_vids=re.compile('<div class="overlay">.+?<h2>(.+?)</h2>.+?<span class="date">(.+?)</span>.+?<span class="mediatype">(.+?)</span>.+?href="(.+?)".+?src="(.+?)"', re.DOTALL).findall(vids)
		match_name=re.compile('<h2>(.+?)</h2>', re.DOTALL).findall(vids)
		match_date=re.compile('<span class="date">(.+?)</span>', re.DOTALL).findall(vids)
		match_thumb=re.compile('src="(.+?)"', re.DOTALL).findall(vids)
		match_mediatype=re.compile('<span class="mediatype">(.+?)</span>', re.DOTALL).findall(vids)
		match_url=re.compile('href="(.+?)"', re.DOTALL).findall(vids)
			
		try:
			name = match_name[0].replace('<div class="hdkenn_list"></div>','')
		except:
			name = ''
		try:
			date = match_date[0]
		except:
			date = ''
		try:
			thumb = match_thumb[0]
		except:
			thumb = ''
		try:
			mediatype = match_mediatype[0]
		except:
			mediatype = ''

		try:
			url = match_url[0]
		except:
			url = ''
				
		#log('<vid>'+name+'#'+baseurl+url+'#'+thumb+'</vid>')
		if __settings__.getSetting('hq_thumbnail') == '2':
			thumb = thumb.replace('188x108','798x449')
			thumb = thumb.replace('195x111','798x449')
			thumb = thumb.replace('396x223','798x449')
		elif __settings__.getSetting('hq_thumbnail') == '1':
			thumb = thumb.replace('188x108','396x223')
			thumb = thumb.replace('195x111','396x223')
		if name != '':
			name = name.replace("\n","")
			name = name.replace("	","")
			name = name.replace("&quot;",'"')
			name = name.replace("&amp;",'&')
			name = date+' - '+name
			if list_them == True:
				addLink(name,baseurl+url,10,thumb,'')

			#print name.encode("ascii")
			#print name.decode("ascii")
			#print name.encode("utf-8")
			##test = name.decode("utf-8")
			#test = test.encode("ascii")
			#print test
			#print baseurl+url
			#stuff = stuff + '<vid>'+name+'#'+baseurl+url+'#'+thumb+'</vid>'


			stuff = stuff + u'<vid>'.encode("utf-8")+name
			stuff = stuff + u'#'.encode("utf-8")+baseurl.encode("utf-8")+url
			stuff = stuff + u'#'.encode("utf-8")+thumb
			stuff = stuff + u'</vid>'.encode("utf-8")#temp disabled
				
				
				
	store(stuff,'stored_list')	
	if list_them == True:
		
		addDir(__language__(32000).encode("utf-8"),data,2,'')
		if update_view == True:
			try:
				wnd = xbmcgui.Window(xbmcgui.getCurrentWindowId())
				wnd.getControl(wnd.getFocusId()).selectItem(i)

				

			except:
				log('focusing not possible')
		
	else:
		addDir(__language__(32004).encode("utf-8"),data+'#just_list#',2,'')
		

def LIST_LIVE(url):
	response=getUrl(url)
	match_all_vids=re.compile('<div class="liveprogramm_full"(.+?)<div class="crane_footer has_rightbar inline_footer">', re.DOTALL).findall(response)
	all_vids = match_all_vids[0].split('span class="tag"')
	match_options=re.compile('<option value="(.+?)" data-filterid="1">(.+?)</option>', re.DOTALL).findall(response)
	for some_vids in all_vids:

		#match_vids=re.compile('	<img.+?src="(.+?)".+?<span.+?href="(.+?)".+?<h2>(.+?)</h2>.+?<span class="time live_countdown".+?>(.+?)</span>', re.DOTALL).findall(some_vids)
		#match_vids=re.compile('	<img.+?src="(.+?)".+?href="(.+?)".+?<h2>(.+?)</h2>.+?<span class="time live_countdown".+?>(.+?)</span>', re.DOTALL).findall(some_vids)
		match_vids=re.compile('<div class=".+?f1_(.+?) .+?<img.+?src="(.+?)".+?href="(.+?)".+?<h2>(.+?)</h2>.+?<span class="time live_countdown".+?>(.+?)</span>', re.DOTALL).findall(some_vids)
		#match_date=re.compile('<span.+?>(.+?)</span><div class="stream').findall(some_vids)
		for date,thumb,url,name,time in match_vids:
			name = name.replace('<div class="hdkennzeichnung"></div>','')
			if time == 'jetzt live':
				title = __language__(32003).encode('ascii')
				title = title+' - '
				title = title+name
			else:
				#title = match_date[0]+', '+time+' - '+name
				if '"' in date:
					date = date.split('"')[0]
				for ddmmyy, realdate in match_options:
					if date == ddmmyy:
						date = realdate
				title = date+', '+time+' - '+name
				
			if __settings__.getSetting('hq_thumbnail') != '0':
				split = url.split('/')
				id = split[-1].replace('.html','')
				id = id.replace('.htm','')
				thumb = 'http://images.laola1.tv/'+id
			if __settings__.getSetting('hq_thumbnail') == '2':
				thumb = thumb+'_798x449.jpg'
			elif __settings__.getSetting('hq_thumbnail') == '1':
				thumb = thumb+'_396x223.jpg'
			if '0.html' not in url:
				addLink(title,url,10,thumb)
			else:
				addLink(title,url,10,thumb)
	


def PLAY(url,name):#10
	dialog = xbmcgui.DialogProgress()
	dialog.create(__language__(32010), __language__(32011))
	dialog.update(0)
	
	response=getUrl(url)

	if 'Dieser Stream beginnt' in response:
		dialog.update(100, __language__(32016))

		log('Video has not jet started')
		match_big=re.compile('<big>(.+?)</big>', re.DOTALL).findall(response)
		xbmc.executebuiltin("Notification("+__language__(32002)+","+match_big[0].replace(',',' -')+", 7000)")
		dialog.close()
		return

	#match_player=re.compile('<iframe.+?src="(.+?)"', re.DOTALL).findall(response)
	dialog.update(25, __language__(32012))
	match_player=re.compile('<iframe(.+?)src="(.+?)"', re.DOTALL).findall(response)
	for iframestuff,possible_player in match_player:
		if 'class="main_tv_player"' in iframestuff:
			player = possible_player
	response=getUrl(player)
	#response=getUrl(match_player[0])
	match_streamid=re.compile('streamid = "(.+?)"', re.DOTALL).findall(response)
	streamid = match_streamid[0]
	
	match_partnerid=re.compile('partnerid = "(.+?)"', re.DOTALL).findall(response)
	partnerid = match_partnerid[0]

	match_portalid=re.compile('portalid = "(.+?)"', re.DOTALL).findall(response)
	portalid = match_portalid[0]

	match_sprache=re.compile('sprache = "(.+?)"', re.DOTALL).findall(response)
	sprache = match_sprache[0]

	match_auth=re.compile('auth = "(.+?)"', re.DOTALL).findall(response)
	auth = match_auth[0]

	match_timestamp=re.compile('timestamp = "(.+?)"', re.DOTALL).findall(response)
	timestamp = match_timestamp[0]

	response=getUrl('http://www.laola1.tv/server/hd_video.php?play='+streamid+'&partner='+partnerid+'&portal='+portalid+'&v5ident=&lang='+sprache)
	match_url=re.compile('<url>(.+?)<', re.DOTALL).findall(response)

	#http://streamaccess.unas.tv/hdflash2/vod/22/151260.xml?streamid=151260&partnerid=22&label=laola1tv&area=ice_hockey_khl_all_star_game
	#&ident=123456789012345678901&klub=0&unikey=0&timestamp=20140101000000&auth=1234567890abcdef1234567890abcdef
	#response=getUrl(match_url[0].replace('&amp;','&')+'&ident=123456789012345678901&klub=0&unikey=0&timestamp='+timestamp+'&auth='+auth)
	response=getUrl(match_url[0].replace('&amp;','&').replace('l-_a-','l-L1TV_a-l1tv')+'&timestamp='+timestamp+'&auth='+auth)

	dialog.update(50, __language__(32013))
	"""
	response=getUrl(match_m3u8[0])
	match_url=re.compile('url="(.+?)"', re.DOTALL).findall(response)
	match_auth=re.compile('auth="(.+?)"', re.DOTALL).findall(response)
	res_url=match_url[0].replace('l-_a-','l-L1TV_a-l1tv')
	
	m3u8_url = res_url+'?hdnea='+match_auth[0]+'&g='+char_gen(12)+'&hdcore=3.1.0'
	"""
	match_new_auth=re.compile('auth="(.+?)"', re.DOTALL).findall(response)
	match_new_url=re.compile('url="(.+?)"', re.DOTALL).findall(response)

	m3u8_url = match_new_url[0].replace('/z/','/i/').replace('manifest.f4m','master.m3u8')+'?hdnea='+match_new_auth[0]+'&g='+char_gen(12)+'&hdcore=3.2.0'
	try:
		dialog.update(75, __language__(32014))
		response=getUrl(m3u8_url)
		dialog.update(100, __language__(32015))
		match_sec_m3u8=re.compile('http(.+?)null=', re.DOTALL).findall(response)
		quality = int(__settings__.getSetting('vod_quality'))+1
		
		choose_url = False
		stored_bw = 0
		lines = response.split('\n')
		for line in lines:
			if '#EXT-X-STREAM-INF' in line:
				match_bw=re.compile('BANDWIDTH=(.+?),', re.DOTALL).findall(line)
				bw = int(match_bw[0])
				if bw > stored_bw and bw <= max_bw:
					choose_url = True
					stored_bw = bw

			elif choose_url == True:
				sec_m3u8 = line
				choose_url = False

		listitem = xbmcgui.ListItem(path=sec_m3u8)
		dialog.close()
		return xbmcplugin.setResolvedUrl(pluginhandle, True, listitem)
		

	except:
		log('Error: Video not found')

	dialog.close()
		
def PLAY_LIVE(url,name):#11
	dialog = xbmcgui.DialogProgress()
	dialog.create(__language__(32010), __language__(32011))
	dialog.update(0)
	
	response=getUrl(url)
	
	if 'Dieser Stream beginnt' in response:
		dialog.update(100, __language__(32016))

		log('Video has not jet started')
		match_big=re.compile('<big>(.+?)</big>', re.DOTALL).findall(response)
		xbmc.executebuiltin("Notification("+__language__(32002)+","+match_big[0].replace(',',' -')+", 7000)")
	else:
		dialog.update(25, __language__(32012))
		match_player=re.compile('<iframe(.+?)src="(.+?)"', re.DOTALL).findall(response)
		for iframestuff,possible_player in match_player:
			if 'class="main_tv_player"' in iframestuff:
				player = possible_player
				
		response=getUrl(player)
		log(response)
		match_m3u8=re.compile('url: "(.+?)"', re.DOTALL).findall(response)
		
		dialog.update(50, __language__(32013))
		
		response=getUrl(match_m3u8[0].replace('/vod/','/live/'))
		log(response)
		match_url=re.compile('url="(.+?)"', re.DOTALL).findall(response)
		match_auth=re.compile('auth="(.+?)"', re.DOTALL).findall(response)
		res_url=match_url[0].replace('l-_a-','l-L1TV_a-l1tv')
		
		m3u8_url = res_url+'?hdnea='+match_auth[0]
		
		dialog.update(75, __language__(32014))
		
		response=getUrl(m3u8_url)
		dialog.update(100, __language__(32015))
		match_sec_m3u8=re.compile('#EXT-X-STREAM-INF:(.+?)http(.+?)rebase=on', re.DOTALL).findall(response)
		quality = int(__settings__.getSetting('vod_quality'))+1

		#xbmc.PlayList(1).clear()
		while quality != 0:
			try:
				quality = quality - 1

				if "RESOLUTION" in match_sec_m3u8[quality][0]:
					sec_m3u8 = 'http'+match_sec_m3u8[quality][1]+'rebase=on'
					listitem = xbmcgui.ListItem(path=sec_m3u8)
					dialog.close()
					return xbmcplugin.setResolvedUrl(pluginhandle, True, listitem)
					"""
					sec_m3u8 = 'http'+match_sec_m3u8[quality][1]+'rebase=on'
					listitem = xbmcgui.ListItem(str(quality)+name, path=sec_m3u8)
					dialog.close()
					xbmc.PlayList(1).add(sec_m3u8, listitem)
					#return xbmcplugin.setResolvedUrl(pluginhandle, True, listitem)
					"""
				else:
					log('No video in url detected, trying lower one: '+str(quality))
					
			except:
				log('Quality setting not available, trying lower one: '+str(quality))
		#return xbmcplugin.setResolvedUrl(pluginhandle, True, listitem)
		log('Error: no video found')
	dialog.close()
		
		
def store(stuff,name):
	stuff = urllib.quote_plus(stuff).decode('utf-8')
	stuff = stuff.encode('ascii')
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
	cache.table_name = "testtable"
	log('storing')
	log('store: '+stuff)
	#cache.set('test', urllib.quote_plus(stuff))
	cache.set('cache', stuff)
	return True
	
def recall(name):
	cache.table_name = "testtable"
	stuff = cache.get('cache')
	stuff = stuff.decode("ascii")
	stuff = stuff.encode("utf-8")
	stuff = urllib.unquote_plus(stuff)

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
	
def clearcache():
	cache.table_name = "testtable"
	cache.delete("cache")
	
def log(message):
	if __settings__.getSetting('debug') == 'true':
		try:
			print "#####Laola1 Debug: "+message.encode('ascii', 'ignore')
		except:
			print "#####Laola1 Debug: Debug function failed thanks to unicode from HELL"
	return
	
def char_gen(size=1, chars=string.ascii_uppercase):
	return ''.join(random.choice(chars) for x in range(size))


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



def getUrl(url):
	url = url.replace('/de-de/','/'+language+'-'+location+'/')
	url = url.replace('/de-at/','/'+language+'-'+location+'/')

	log('Opening URL: '+url)
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
	return link
	
	
def postUrl(url,data):
	url = url.replace('/de-de/','/'+language+'-'+location+'/')
	url = url.replace('/de-at/','/'+language+'-'+location+'/')
        req = urllib2.Request(url,data)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
	return link


def addLink(name,url,mode,iconimage,plot=''):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
	liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": plot, "plotoutline": plot  } )
	liz.setProperty('IsPlayable', 'true')
	if __settings__.getSetting('hq_thumbnail') == '2':
		liz.setProperty('fanart_image',iconimage)
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz)
	return ok
	

def addDir(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
        

params=get_params()
url=None
name=None
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
        MAIN_NEXT(url,name)

elif mode==2:
        print ""+url
        LIST_VIDEOS(url)
		
elif mode==3:
        print ""+url
        LIST_LATEST(url)

elif mode==5:
        print ""+url
        LIST_LIVE(url)
		
elif mode==10:
        print ""+url
        PLAY(url,name)
		
elif mode==11:
        print ""+url
        PLAY_LIVE(url,name)

if update_view:
	xbmcplugin.endOfDirectory(int(sys.argv[1]), updateListing=True)
else:
	xbmcplugin.endOfDirectory(int(sys.argv[1]))
