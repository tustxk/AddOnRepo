# -*- coding: utf8 -*-

import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmcaddon,base64,socket,sys,string,random,cookielib,httplib,base64
from bs4 import BeautifulSoup as Soup



__settings__ = xbmcaddon.Addon(id='plugin.video.ittv')
#__settings__ = xbmcaddon.Addon()
__language__ = __settings__.getLocalizedString

#xbmc.PLAYER_CORE_MPLAYER

pluginhandle = int(sys.argv[1])
addon = xbmcaddon.Addon(id='plugin.video.ittv')

#testfile = xbmc.translatePath(addon.getAddonInfo('path')+"/test.flv")

COOKIEFILE = xbmc.translatePath(addon.getAddonInfo('path')+"/cookies.lwp")

debug = '1'

  














def INDEX():

	addDir('World Events','http://cdn.laola1.tv/ittf/iframe/menu_1.html',1,'')
	addDir('Continental Events','http://cdn.laola1.tv/ittf/iframe/menu_2.html',1,'')
	addDir('Junior Events','http://cdn.laola1.tv/ittf/iframe/menu_3.html',1,'')
	addDir('Education Development','http://cdn.laola1.tv/ittf/iframe/menu_4.html',1,'')
	addDir('Entertainment','http://cdn.laola1.tv/ittf/iframe/menu_5.html',1,'')
	addDir('President Interviews','http://cdn.laola1.tv/ittf/iframe/menu_6.html',1,'')


def TOPICSELECTION(url):#1
	response = getUrl(url)
	f = open(xbmc.translatePath(addon.getAddonInfo('path')+"/cache1.html"),"w+")
	f.write(response)
	f.close()
	soup_response=Soup(response)
	for entry in soup_response.find_all('ul'):
		print entry


	match_live=re.compile('class="td_live"(.+?)</li>').findall(response) 
	for item in match_live:
		match_url=re.compile('pfad=(.+?)"').findall(response) 
		match_name=re.compile('> (.+?)</a>').findall(response)
 		addLink('LIVE: '+match_name[0],match_url[0],4,'')

		#print '##########################'
		#print match_year[0]+' - '+ match_name[0]+match_url[0]
		#addLink(match_year[0]+' - '+ match_name[0],10,match_url[0],'')
		
		
	match_main=re.compile('<a href="#" onclick="javascript\:switchlayer\(\'(.+?)\'\); return false;" onFocus="if \(this\.blur\) this.blur\(\).+?"><span class="year"(.+?)</span>(.+?)</a>').findall(response) 


	
	for navi,year,name in match_main:
		print name
		print year
		print navi
		if '>' == year:
			addDir(name,navi,2,'')
		else:
			addDir(year.replace('>','')+' -'+name,navi,2,'')
		"""
		for entry in soup_response.find_all('ul'):
			#print entry
			if str(navi) in str(entry):
				#print entry
				addDir(year+' -'+name,'',2,'')
		"""
	#soup=Soup(response)
	#for entry in soup.find_all('ul'):
	#	print entry
	"""
		
		
        for url,name in match:
		if not "LIVE" in name:
			if not "Live" in name:
				addDir(name,url,2,'')
	"""
                
def FINESELECTION(url):#2
	f = open(xbmc.translatePath(addon.getAddonInfo('path')+"/cache1.html"),"r")
	lines = f.readlines()
	f.close()

	#f2.write(response)
	navi = url
	#print lines
	soup_response=Soup(lines[0])
	print '##############'+lines[0]
	for entry in soup_response.find_all('ul'):
		print entry
		print '##################################'
		print navi
		if str(navi)+'"' in str(entry):
			selection = str(entry)
			
	f2 = open(xbmc.translatePath(addon.getAddonInfo('path')+"/cache2.html"),"w+")
	f2.write(selection)
	f2.close()
	
	if not 'class="subheading"' in selection:
		match=re.compile('<a href="player\.html\?pfad=(.+?)".+?img.+?> (.+?)</a>').findall(selection) 
		for url,name in match:
			url = url.replace(' ','%20')
			addLinkOld(name,'rtmp://217.212.225.4:1935/ondemand?_fcs_vhost=cp77194.edgefcs.net&auth=undefined&aifp=v002&slist='+url+' swfUrl=http://cdn.laola1.tv/ittf/iframe/ittfplayer.swf swfVfy=true','')
	else:
		#selection = selection + '\n'
		#selection = selection.replace('<li class="subheading">','\n')
		
		match_head=re.compile('<b>(.+?)</b>').findall(selection) 
		for head in match_head:
			addDir(head,head,3,'')

	


		
def VIDEOSELECTION(url):#3
	f = open(xbmc.translatePath(addon.getAddonInfo('path')+"/cache2.html"),"r")
	lines = f.readlines()
	f.close()
	selection = lines[0]
	selection = selection + '\n'
	selection = selection.replace('<li class="subheading">','\n')
	match_entries=re.compile('<b>(.+?)\n').findall(selection) 
	for entries in match_entries:
		print '##################'
		#print 'url is '+url
		#print entries
		if url in entries:
			print 'chosen:'+entries
			match=re.compile('<a href="player\.html\?pfad=(.+?)".+?img.+?> (.+?)</a>').findall(selection) 
			for url,name in match:
				url = url.replace(' ','%20')
				addLinkOld(name,'rtmp://217.212.225.4:1935/ondemand?_fcs_vhost=cp77194.edgefcs.net&auth=undefined&aifp=v002&slist='+url+' swfUrl=http://cdn.laola1.tv/ittf/iframe/ittfplayer.swf swfVfy=true','')

	
def PLAY_LIVE(url,name):#4
	url = url.replace('%26partnerid=24','')
	response = getUrl(url)

	match_token=re.compile('auth="(.+?)".+?url="(.+?)".+?stream="(.+?)".+?status=".+?".+?statustext=".+?".+?aifp="(.+?)"', re.DOTALL).findall(response)

	for auth,url,stream,aifp in match_token:
		auth = auth
		url = url
		stream = stream
		aifp = aifp

	log('auth: "'+auth+'"')
	log('url: "'+url+'"')
	log('stream: "'+stream+'"')
	log('aifp: "'+aifp+'"')


	log('GET ip')
	server = 'http://cp37665.live.edgefcs.net/fcs/ident'
	#server = 'http://cp37665.live.edgefcs.net/live'
	#response = getUrl('http://'+server+'/fcs/ident')
	response = getUrl(server)

	match_path=re.compile('<ip>(.+?)</ip>').findall(response)

	ip = match_path[0]

	log('ip: "'+ip+'"')


	log('assembling rtmp')
	servertype = 'live'
	#rtmp://80.150.133.71:1935/live?_fcs_vhost=cp37665.live.edgefcs.net/ittf_kuwait_bet_1@s92820?auth=db.b4cWdwdYa9bLc3a7cja5cFcGdcc3cUbu-brhMEp-E-eS-xyKqCInCDoD-o6s9&p=24&e=111442&u=&t=livevideo&l=&a=&c=DE&i=&q=&k=&aifp=v001.
	#rtmpbody = 'rtmp://'+ip+':1935/'+servertype+'?_fcs_vhost='+server+'&auth='+auth+'&aifp='+aifp+'&slist='+stream
	rtmpbody = 'rtmp://'+ip+':1935/'+servertype+'?_fcs_vhost='+'cp37665.live.edgefcs.net/'+stream+'&auth='+auth+'&aifp='+aifp#+'&slist='+stream
	#rtmpbody = 'rtmp://'+ip+':1935/'+servertype+'?_fcs_vhost='+'cp37665.live.edgefcs.net/live/'+stream+'&auth='+auth+'&aifp='+aifp#+'&slist='+stream
	swf = ' swfUrl=http://cdn.laola1.tv/ittf/iframe/ittfplayer.swf swfVfy=true'
	#app = ' app=live?_fcs_vhost=cp37665.live.edgefcs.net'
	app = ' app=live?_fcs_vhost=cp37665.live.edgefcs.net/live'
	page = ' pageUrl='+'http://cdn.laola1.tv'

	if '.mp4' in stream:
		playpath = ' playpath=mp4:'+stream
	else:
		playpath = ' playpath='+stream #fix for beachvolleyball

	flashver = ' flashver=LNX\ 10,3,162,29'
	rtmppath = rtmpbody+swf+app+page+playpath+' live=true'
	rtmppath = rtmppath.replace('&amp;','&')
	rtmppath = rtmppath.replace('&p=','&p=24')
	rtmppath = rtmppath.replace('&partnerid=24','')
	#rtmppath = rtmppath.replace('&e=','&e='+playkey1)
	#rtmppath = rtmppath.replace('&t=','&t=livevideo')
	item = xbmcgui.ListItem(path=rtmppath)
	return xbmcplugin.setResolvedUrl(pluginhandle, True, item)
	











	

def list_aufmacher(url,site):
	log('List aufmacher')
	match_flashvars = re.compile('<param name="flashvars" value="(.+?)"').findall(site)
	match_url = re.compile('www.(.+?)/video').findall(url)
	flashvars = match_flashvars[0].replace('&amp;','&')
	url = 'http://www.'+ match_url[0] + '/video/server/aufmacher.php?' + flashvars + '&r=' + num_gen(8)
	response2 = getUrl(url)
	print response2
	response2= response2.replace('\n','  ')
	match_bild = re.compile('<bild(.+?)>').findall(response2)
	for bild in match_bild:
		if not 'liveicon="1"' in bild:
			match_url = re.compile('link="(.+?)"').findall(bild)
			match_head = re.compile('head="(.+?)"').findall(bild)
			match_txt = re.compile('txt="(.+?)"').findall(bild)
			match_tumb = re.compile('pfad="(.+?)"').findall(bild)
			match_url = re.compile('link="(.+?)"').findall(bild)
			print '#############################'
			print 'www.laola1.tv/'+match_tumb[0]
			addLink(match_txt[0].replace('  ',' '),match_url[0],3,'http://www.laola1.tv/'+match_tumb[0],'http://www.laola1.tv/'+match_tumb[0])


def get_playkeys(url):
	log("GET playkey1,playkey2")

	response = getUrl(url)
	#print response
	playkeys=re.compile('"playkey=(.+?)-(.+?)&adv.+?"').findall(response)

	for playkey1,playkey2 in playkeys:
		log('playkey1: "'+playkey1+'"')

		log('playkey2: "'+playkey2+'"')

	return playkeys

def VIDEOLINKS(url,name,thumb=''):
	response = getUrl(url)


	if xbmcplugin.getSetting(pluginhandle,"ads") == '1':
		match_flashvars=re.compile('"flashvars", "(.+?)"').findall(response)
		try:
			ad_url,ad_length = get_video_ad(match_flashvars[0])
			#stacked_url += ad_url + ' , '
			item=xbmcgui.ListItem(scommercial, thumbnailImage='')
			item.setProperty('mimetype', 'video/x-flv')
			xbmc.PlayList(1).add(ad_url, item)
		except:
			log('no commercial recieved')

	
	response = getUrl(url)
	match=re.compile('videopfad=(.+?)&', re.DOTALL).findall(response)

	item=xbmcgui.ListItem(name, thumbnailImage=thumb)
	item.setProperty('mimetype', 'video/x-flv')
	xbmc.PlayList(1).add('plugin://plugin.video.laola1live/?url='+enc_url(match[0])+'&mode=10&thumb='+enc_url(thumb)+'&name='+name, item)



def PLAY_VIDEO(url,name,thumb=''):#10
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        req.add_header('Host', 'streamaccess.unas.tv')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
	#log(link)



	match_httpBase=re.compile('<meta name="httpBase" content="(.+?)"', re.DOTALL).findall(link)
	match_vod=re.compile('<meta name="vod" content="true" value="/(.+?)"', re.DOTALL).findall(link)
	match_src=re.compile('<video src=".+?primaryToken=(.+?)" system-bitrate=".+?"/>', re.DOTALL).findall(link)
	match_srcb=re.compile('<video src="(.+?)" system-bitrate=".+?"/>', re.DOTALL).findall(link)

	src = match_src[0]

	vod = match_vod[0]
	#vod = match_vod[0].replace('bitrate=0','bitrate=950000')
	#vod = vod.replace(',low,high,','0_1')


	fullUrl = match_httpBase[0]+vod+"?primaryToken="+src
	#fullUrl = match_httpBase[0]+match_srcb[0]
	fullUrl = fullUrl.replace("&amp;","&")
	#fullUrl = fullUrl.replace("&p=","&p=22")
	#fullUrl = fullUrl.replace("&e=","&e=104258")
	#fullUrl = fullUrl.replace("&a=","&a=l1tvgerfbbl")
	#fullUrl = fullUrl.replace("&l=","&l=L1TV")
	fullUrl = fullUrl + "&v=2.10.3&fp=LNX%2011,1,102,63"
	fullUrl = fullUrl + "&r="+char_gen(5)#random uppercase string
	g = char_gen(12)#random uppercase string
	fullUrl = fullUrl + "&g="+g
	log('fullUrl: '+fullUrl)

	"""
	match_httpBase=re.compile('<meta name="httpBase" content="(.+?)"', re.DOTALL).findall(response)
	match_vod=re.compile('<meta name="vod" content="true" value="/(.+?)"', re.DOTALL).findall(response)
	match_src=re.compile('<video src=".+?primaryToken=(.+?)" system-bitrate=".+?"/>', re.DOTALL).findall(response)

	if setting_streamquality == '0':
		src = match_src[0]
		print "low quality"
	else:
		src = match_src[-1]
		print "high quality"
	
	fullUrl = match_httpBase[0]+match_vod[0]+"?primaryToken="+src
	fullUrl = fullUrl.replace("&amp;","&")
	fullUrl = fullUrl + "&v=2.10.3&fp=LNX%2011,1,102,63"
	fullUrl = fullUrl + "&r="+char_gen(5)#random uppercase string
	fullUrl = fullUrl + "&g="+char_gen(12)#random uppercase string
	"""


	###header inspection###
	"""
        req = urllib2.Request(fullUrl)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
	print'####################resp_info'
	print response.info()
        link=response.read()
        response.close()
	"""


	if setting_streamquality == '0':
		log("low quality")

		item=xbmcgui.ListItem(name, thumbnailImage=thumb, path=fullUrl)
		item.setProperty('mimetype', 'video/x-flv')
		xbmcplugin.setResolvedUrl(pluginhandle, True, item)

		force_play(fullUrl)

	else:
		log("high quality")

		VIDb64 = base64.encodestring(fullUrl).replace('\n', '')
		fullUrl = URL_AKAMAI_PROXY % VIDb64

		item=xbmcgui.ListItem(name, thumbnailImage=thumb, path=fullUrl)
		item.setProperty('mimetype', 'video/x-flv')
		xbmcplugin.setResolvedUrl(pluginhandle, True, item)







	"""
	if autoPlay>0:
		xbmc.sleep(autoPlay*100)
		if xbmc.Player().isPlaying()==True and int(xbmc.Player().getTime())==0:
			xbmc.Player().pause()
	"""
	"""
	xbmc.sleep(5000)

	mod_vod = vod.replace('mp4.csmil/bitrate=0','mp4.csmil_0_1@14')
	mod_vod = mod_vod+'?cmd=throttle,100&v=2.10.3&r='+char_gen(5)+'&g='+g+'&lvl1=9.84,10,15.458,11.49,12.66,NaN,1488,1488,1,950,16.353,1353800347.83,14.92,16.378,14.945,393.68,1445'

	control = match_httpBase[0]+mod_vod
	print '#################################control'+control
	print getUrl(control)
	"""

#'http://hdvodlaola1tv-f.akamaihd.net/control/hdflash/2012/eishockey/121123_man_kec_,low,high,.mp4.csmil_0_1@14?cmd=throttle,108&v=2.10.3&r=EYXCI&g=RVBLUXVNVBLK&lvl1=9.84,10,15.458,11.49,12.66,NaN,1488,1488,1,950,16.353,1353800347.83,14.92,16.378,14.945,393.68,1445,3.03,0,155,122,15003,u,false')



	"""
	if autoPlay>0:
		xbmc.sleep(autoPlay*100+int(float(ad_length)*float(1000)))
		time_difference = int(xbmc.Player().getTime())*1000 - int(float(ad_length)*float(1000))
		#deb_time += 'player time\n'
		#deb_time += str(int(xbmc.Player().getTime()))+'\n'
		#deb_time += 'time difference\n'
		#deb_time += str(time_difference)+'\n'
		#deb_time += 'round time\n'
		#deb_time += str(round(time_difference))+'\n'
		#deb_time += 'round time/100\n'
		#deb_time += str(round(time_difference/100))
		#print deb_time
		if xbmc.Player().isPlaying()==True and round(time_difference/1000)==0:

			xbmc.Player().pause()
	"""
	"""
    	#core_player = xbmc.PLAYER_CORE_MPLAYER
    	core_player = xbmc.PLAYER_CORE_DVDPLAYER
	stacked_url = stacked_url[:-3] 
	item=xbmcgui.ListItem(name, iconImage='', thumbnailImage='')

	ok=xbmc.Player( core_player ).play( stacked_url , item)
	autoPlay = 5
	if autoPlay>0:
		xbmc.sleep(autoPlay*1000)
		if xbmc.Player().isPlaying()==True and int(xbmc.Player().getTime())==0:
			xbmc.Player().pause()	

	return
	#item=xbmcgui.ListItem(name, thumbnailImage='', path=stacked_url)
	#xbmcplugin.setResolvedUrl(pluginhandle, True, item)

	#listitem = xbmcgui.ListItem(name,thumbnailImage='')#TODO:thumb
	#xbmc.PlayList(1).add(fullUrl, listitem)
	"""



	"""
	listitem.setProperty('mimetype', 'video/x-flv')
        return xbmcplugin.setResolvedUrl(pluginhandle, True, listitem)
	"""



"""
	pageurl = url #this is messy

	playkeys = get_playkeys(url)

	for playkey1,playkey2 in playkeys:
		playkey1 = playkey1
		playkey2 = playkey2
	

	log('GET streamquality,server,servertype,playpath,title')
	response = getUrl('http://www.laola1.tv/server/ondemand_xml_esi.php?playkey='+playkey1+'-'+playkey2)

	match_video=re.compile('<video.+?>(.+?)</video>', re.DOTALL).findall(response)

	video = match_video[0]

	match_rtmp=re.compile('<(.+?) .+?erver="(.+?)/(.+?)" pfad="(.+?)" .+? ptitle="(.+?)"').findall(video)#ugly, but behind low is one space too much: '  '

	for streamquality,server,servertype,playpath,title in match_rtmp:
		streamquality = streamquality
		server = server
		servertype = servertype
		playpath = playpath
		title = title
		if setting_streamquality == '1':
			break

	log('streamquality: "'+streamquality+'"')
	log('server: "'+server+'"')
	log('servertype: "'+servertype+'"')
	log('playpath: "'+playpath+'"')
	log('title: "'+title+'"')


	log('GET auth,url,stream,aifp')
	response = getUrl('http://streamaccess.laola1.tv/flash/vod/22/'+playkey1+'_'+streamquality+'.xml')

		match_token=re.compile('auth="(.+?)".+?url="(.+?)".+?stream="(.+?)".+?status=".+?".+?statustext=".+?".+?aifp="(.+?)"', re.DOTALL).findall(response)

	for auth,url,stream,aifp in match_token:
		auth = auth
		url = url
		stream = stream
		aifp = aifp

	log('auth: "'+auth+'"')
	log('url: "'+url+'"')
	log('stream: "'+stream+'"')
	log('aifp: "'+aifp+'"')


	log('GET ip')
	response = getUrl('http://'+server+'/fcs/ident')

	match_path=re.compile('<ip>(.+?)</ip>').findall(response)

	ip = match_path[0]

	log('ip: "'+ip+'"')


	log('assembling rtmp')
	rtmpbody = 'rtmp://'+ip+':1935/'+servertype+'?_fcs_vhost='+server+'&auth='+auth+'&aifp='+aifp+'&slist='+stream
	swf = ' swfUrl=http://www.laola1.tv/swf/player.v12.4.swf swfVfy=true'
	app = ' app='+servertype+'?_fcs_vhost='+server+'&auth='+auth+'&aifp='+aifp+'&slist='+stream
	page = ' pageUrl='+pageurl

	if '.mp4' in stream:
		playpath = ' playpath=mp4:'+stream
	else:
		playpath = ' playpath='+stream #fix for beachvolleyball

	flashver = ' flashver=LNX\ 10,3,162,29'
	rtmppath = rtmpbody+swf+app+page+playpath
	rtmppath = rtmppath.replace('&amp;','&')
	rtmppath = rtmppath.replace('&p=','&p=22')
	rtmppath = rtmppath.replace('&e=','&e='+playkey1)
	item = xbmcgui.ListItem(path=rtmppath)
	return xbmcplugin.setResolvedUrl(pluginhandle, True, item)													
"""


def LIVESELECTION(url):
        #print url
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	if xbmcplugin.getSetting(pluginhandle,"inside") == 'false':
		req.add_header('X-Forwarded-For', xip)
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match1=re.compile('<h2><a href="http://www.laola1.tv/(.+?)/upcoming-livestreams/(.+?)"').findall(link)
        #<h2><a href="http://www.laola1.tv/en/int/upcoming-livestreams/video/0-989-.html"
        for lang,videos in match1:
                #print videos
                req = urllib2.Request('http://www.laola1.tv/'+lang+'/upcoming-livestreams/'+videos)
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
#		if xbmcplugin.getSetting(pluginhandle,"inside") == 'false':
#			req.add_header('X-Forwarded-For', xip)
                response = urllib2.urlopen(req)
                link=response.read()
                #print link
                response.close()
        	match1=re.compile('<div class="teaser_bild_live" title=".+?"><a href="(.+?)"><img src="(.+?)" border=".+?" /></a></div>.+?<div class="teaser_head_live" title=".+?">(.+?)</div>.+?<div class="teaser_text" title=".+?"><a href=".+?>(.+?)</a>', re.DOTALL).findall(link)
#                match1=re.compile('<div class=".+?" title=".+?"><a href="(.+?)"><img src="(.+?)" border=".+?" /></a></div>.+?<div class="teaser_head_live" title=".+?">(.+?)</div>.+?<div class="teaser_text" title=".+?">(.+?)</div>', re.DOTALL).findall(link)


	        for url,thumbnail,date,name in match1:
#                for url,thumbnail,date,name in match1:
                        addLink(date+' - '+name,url,5,thumbnail)

                match_next=re.compile("<a href=\"(.+)\" class=\"teaser_text\">vor</a>").findall(link)
                for url in match_next:
                        addDir(__language__(30001),url,4,'')
                match_next=re.compile("<a href=\"(.+)\" class=\"teaser_text\">next</a>").findall(link)
                for url in match_next:
                        addDir(__language__(30001),url,4,'')


def VIDEOLIVELINKS(url,name,thumb):#5
	#print url
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
#	if xbmcplugin.getSetting(pluginhandle,"inside") == 'false':
#		req.add_header('X-Forwarded-For', xip)
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
	#print link

	#break if livestream isn't ready
	match_ready=re.compile('Dieser Stream beginnt am.+?<big>(.+?),(.+?)-(.+?)CET</big>', re.DOTALL).findall(link)
	for weekday,date,time in match_ready:
		#xbmcplugin.getSetting(pluginhandle,"streamquality") == '1':
		xbmc.executebuiltin("Notification("+snotstarted+","+sstartsat+" "+weekday.replace(' ','')+" - "+date.replace(' ','')+" "+sat+" "+time.replace(' ','').replace('Uhr','')+" "+scet+", 7000)")
		return

	match_ready=re.compile('This stream starts at.+?<big>(.+?),(.+?)-(.+?)CET</big>', re.DOTALL).findall(link)
	for weekday,date,time in match_ready:
		#xbmcplugin.getSetting(pluginhandle,"streamquality") == '1':
		xbmc.executebuiltin("Notification("+snotstarted+","+sstartsat+" "+weekday.replace(' ','')+" - "+date.replace(' ','')+" "+sat+" "+time.replace(' ','')+" "+scet+", 7000)")
		return

	if has_ended(link) == True:
		return

	pl=xbmc.PlayList(1)
	pl.clear()

	item = xbmcgui.ListItem('Dummy entry',thumbnailImage='')
	xbmc.PlayList(1).add('', item)

        match_playkey=re.compile('"playkey=(.+?)-(.+?)&adv.+?"').findall(link)

	if '"src", "http://www.laola1.tv/swf/hdplayer",' in link:

        	for playkey1,playkey2 in match_playkey:
			print 'laola: use streamtype 1a'
			req = urllib2.Request('http://streamaccess.laola1.tv/hdflash/1/hdlaola1_'+playkey1+'.xml?streamid='+playkey1+'&partnerid=1&quality=hdlive&t=.smil')

		        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
#			if xbmcplugin.getSetting(pluginhandle,"inside") == 'false':
#				req.add_header('X-Forwarded-For', xip)
		        response = urllib2.urlopen(req)
		        link=response.read()
		        response.close()
			#print link

		        match_rtmp=re.compile('<meta name="rtmpPlaybackBase" content="(.+?)" />').findall(link)
			match_http=re.compile('<meta name="httpBase" content="(.+?)" />').findall(link)
		        match_quality=re.compile('<video src="(.+?)" system-bitrate=".+?"/>').findall(link)
			item=xbmcgui.ListItem(name, thumbnailImage='')
			item.setProperty('mimetype', 'video/x-flv')
			#return xbmc.PlayList(1).add(match_http[0]+match_quality[-1], item)

                        #item = xbmcgui.ListItem(path=match_http[0]+match_quality[-1])
			#return xbmcplugin.setResolvedUrl(pluginhandle, True, item)

		log('use streamtype 1b')
		match_live_1b=re.compile('isLiveStream=true&videopfad=(.+?)&').findall(link)
		match_flashvars=re.compile('"flashvars", "(.+?)"').findall(link)
		ad_length = 0
		if xbmcplugin.getSetting(pluginhandle,"ads") == '1':
			try:
				ad_url,ad_length = get_video_ad(match_flashvars[0])
				item=xbmcgui.ListItem(scommercial, thumbnailImage='')
				xbmc.PlayList(1).add(ad_url, item)
			except:
				log('no commercial recieved')
		#else:
		#	PLAY_LIVE_1B(enc_url,name)


		item=xbmcgui.ListItem(name, thumbnailImage=thumb)
		item.setProperty('mimetype', 'video/x-flv')
		xbmc.PlayList(1).add('plugin://plugin.video.laola1live/?url='+enc_url(match_live_1b[0])+'&mode=11&thumb='+enc_url(thumb)+'&name='+name, item)



		#item = xbmcgui.ListItem(path=http+video+" live=true")
		#return xbmcplugin.setResolvedUrl(pluginhandle, True, item)


#        match_over=re.compile('<p>Lieber LAOLA(.+?)-User,</p>').findall(link)
#        if match_over[0] == '1':
#                addDir('vorbei/zu frueh',' ',5,'')
        ##"playkey=47060-Gut1cOWmlyix.&adv=laola1.tv/de/eishockey/ebel&adi=laola1.tv/de/eishockey/ebel&aps=Video1&szo=eishockey&deutschchannel=true&channel=222&teaser=1153&play=47060&fversion=player.v10.2"
	else:        
		log('use streamtype 2')
		for playkey1,playkey2 in match_playkey:
        	        print 'playkey1 '+playkey1
        	        print 'playkey2 '+playkey2                
        	        req = urllib2.Request('http://www.laola1.tv/server/ondemand_xml_esi.php?playkey='+playkey1+'-'+playkey2)
        	        #print 'http://www.laola1.tv/server/ondemand_xml_esi.php?playkey='+playkey1+'-'+playkey2
        	        ##http://www.laola1.tv/server/ondemand_xml_esi.php?playkey=47060-Gut1cOWmlyix.
        	        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
#			if xbmcplugin.getSetting(pluginhandle,"inside") == 'false':
#				req.add_header('X-Forwarded-For', xip)
        	        response = urllib2.urlopen(req)
        	        link_playkey=response.read()
        	        #print link_playkey
        	        response.close()
        	        match_video=re.compile('<video.+?>(.+?)</video>', re.DOTALL).findall(link_playkey)
        	        for video in match_video:
	#                        print 'video '+video
        	                match_rtmp=re.compile('<high server="(.+?)/(.+?)" pfad="(.+?)@(.+?)" .+? ptitle="(.+?)"').findall(video)#ugly, but behind low is one space too much: '  '
        	                ##<high server="cp77154.edgefcs.net/ondemand" pfad="77154/flash/2011/ebel/20102011/110327_vic_rbs_high" type="V" aifp="v002"
        	                ##token="true" ptitle="Eishockey Erste Bank EHL Erste Bank Eishockey Liga" etitle="Vienna Capitals - EC Red Bull Salzburg"
        	                ##firstair="2010/01/01" stype="VOD" cat="video ondemand" vidcat="laola1.tv/at/eishockey/ebel" round="" season="2010/2011" />
        	                for server,servertype,playpath1,playpath2,title in match_rtmp:
        	                #for streamquality,server,servertype,playpath1,playpath2,title in match_rtmp:
        	                        #print 'streamquality '+streamquality
        	                        print 'server '+server
        	                        print 'servertype '+servertype
        	                        print 'playpath '+playpath1+'@'+playpath2
        	                        print 'title '+title
        	                        req = urllib2.Request('http://streamaccess.laola1.tv/flash/1/'+playkey1+'_high.xml')
        	                        #req = urllib2.Request('http://streamaccess.laola1.tv/flash/1/'+playkey1+'_'+streamquality+'.xml')
        	                        
        	                        #print 'http://streamaccess.laola1.tv/flash/1/'+playkey1+'_'+streamquality+'.xml'
        	                        ##http://streamaccess.laola1.tv/flash/1/47327_high.xml?partnerid=1&streamid=47327
        	                        ##http://streamaccess.laola1.tv/flash/vod/22/47060_high.xml
        	                        ##http://streamaccess.laola1.tv/flash/1/47215_high.xml
        	                        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
#					if xbmcplugin.getSetting(pluginhandle,"inside") == 'false':
#						req.add_header('X-Forwarded-For', xip)
        	                        response = urllib2.urlopen(req)
        	                        link_token=response.read()
        	                        print link_token
        	                        response.close()
        	                        match_token=re.compile('auth="(.+?)&amp;p=.+?".+?url="(.+?)/live".+?stream="(.+?)".+?status=".+?".+?statustext=".+?".+?aifp="(.+?)"', re.DOTALL).findall(link_token)
        	                        ##auth="db.cibycHcwdEbhaKa4a3bUc7cIbpbLdtal-bnKofS-cOW-eS-CkBwmc-m6ke&p=&e=&u=&t=ondemandvideo&l=&a="
        	                        ##url="cp77154.edgefcs.net/ondemand" stream="77154/flash/2011/ebel/20102011/110327_vic_rbs_high" status="0" statustext="success" aifp="v001" comment="success"
        	                        for auth,url,stream,aifp in match_token:
        	                                print 'auth '+auth
        	                                print 'url '+url
        	                                print 'stream '+stream
        	                                print 'afip '+aifp
        	                                req = urllib2.Request('http://'+server+'/fcs/ident')
        	                                ##http://cp77154.edgefcs.net/fcs/ident
        	                                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
#						if xbmcplugin.getSetting(pluginhandle,"inside") == 'false':
#							req.add_header('X-Forwarded-For', xip)
        	                                response = urllib2.urlopen(req)
        	                                link_path=response.read()
        	                                response.close()
        	                                match_path=re.compile('<ip>(.+?)</ip>').findall(link_path)
        	                                ##<ip>213.198.95.204</ip>
        	                                for ip in match_path:
        	                                        print 'ip '+ip
        	                                ##http://cp77154.edgefcs.net/fcs/ident
	#    	                                         if streamquality == 'high':
        	                                        item = xbmcgui.ListItem(path='rtmp://'+ip+':1935/'+servertype+'?_fcs_vhost='+url+'/'+stream+'?auth='+auth+'&p=1&e='+playkey1+'&u=&t=livevideo&l='+'&a='+'&aifp='+aifp+' swfUrl=http://www.laola1.tv/swf/player.v12.4.swf swfVfy=true live=true')
							return xbmcplugin.setResolvedUrl(pluginhandle, True, item)
         	                                       #print 'name: '+name
         	                                       #print 'rtmp-link: rtmp://'+ip+':1935/'+servertype+'?_fcs_vhost='+url+'/'+stream+'?auth='+auth+'&p=1&e='+playkey1+'&u=&t=livevideo&l='+'&a='+'&aifp='+aifp

         	                                       #addLink('High: '+name,'rtmp://'+ip+':1935/'+servertype+'?_fcs_vhost='+server+'/'+playpath+'?auth='+auth+'&aifp='+aifp,'')



         	                                               ##rtmp://213.198.95.204:1935/ondemand?_fcs_vhost=cp77154.edgefcs.net&auth=db.cibycHcwdEbhaKa4a3bUc7cIbpbLdtal-bnKofS-cOW-eS-CkBwmc-m6ke&p=&e=&u=&t=ondemandvideo&l=&a=
         	                                               ##&aifp=v001&slist=77154/flash/2011/ebel/20102011/110327_vic_rbs_high
         	                                               ##rtmp://213.198.95.204:1935/ondemand?_fcs_vhost=cp77154.edgefcs.net&auth=db.cibycHcwdEbhaKa4a3bUc7cIbpbLdtal-bnKofS-cOW-eS-CkBwmc-m6ke&p=&e=&u=&t=ondemandvideo&l=&a=&aifp=v001&slist=77154/flash/2011/ebel/20102011/110327_vic_rbs_high
         	                                       #elif streamquality == 'low':
         	                                               #addLink('Low: '+name,'rtmp://'+ip+':1935/'+servertype+'?_fcs_vhost='+server+'/'+playpath+'?auth='+auth+'&aifp='+aifp,'')
	

         	                                               ##...yeah


def PLAY_LIVE_1B(url,name,thumb=''):#11
	link=getUrl(url)
	match_rtmp=re.compile('<meta name="rtmpPlaybackBase" content="(.+?)" />').findall(link)
	match_http=re.compile('<meta name="httpBase" content="(.+?)" />').findall(link)
	match_quality=re.compile('<video src="(.+?)" system-bitrate=".+?"/>').findall(link)
	http = match_http[0]
	http = http.replace("&l=","&l=&v=2.4.5&fp=LNX%2010,3,162,29&r="+char_gen(5)+"&g="+char_gen(12))

	if livequality == '0':
		video = match_quality[0]
	if livequality == '1':
		try:
			video = match_quality[1]
		except:
			video = match_quality[0]
	if livequality == '2':
		video = match_quality[-1]
	log("playing: "+http+video)

	item=xbmcgui.ListItem(name, thumbnailImage=thumb, path=http+video+" live=true")
	item.setProperty('mimetype', 'video/x-flv')
	xbmcplugin.setResolvedUrl(pluginhandle, True, item)

	force_play(http+video+" live=true")
	auto_resume()

	
def LIVE(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        #print link
        match_base=re.compile('<meta name="httpBase" content="(.+?)" />').findall(link)
        match_src=re.compile('<video src="(.+?)" system-bitrate="950000"/>').findall(link)
        print match_base[0]
        print match_src[-1]
        addLink('play',match_base[0]+match_src[-1],'')


def has_ended(site):
	if 'Dieser Stream ist bereits beendet.' in site or 'This stream has already finished.' in site:
		xbmc.executebuiltin("Notification("+__language__(30007)+","+__language__(30008)+", 7000)")
		return True
	#elif #TODO:
	else: False

def enc_url(url):
	url = url.replace(':','%3A')
	url = url.replace('/','%2F')
	url = url.replace('?','%3F')
	url = url.replace('=','%3D')
	url = url.replace('&','%26')
	return url

                
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

def char_gen(size=1, chars=string.ascii_uppercase):
	return ''.join(random.choice(chars) for x in range(size))

def num_gen(size=1, chars=string.digits):
	return ''.join(random.choice(chars) for x in range(size))


def getUrl(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
	return link



def getUrlCookie( url , extraheader=True):
    cj = cookielib.LWPCookieJar()
    if os.path.isfile(COOKIEFILE):
        cj.load(COOKIEFILE, ignore_discard=True)

    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    opener.addheaders = [('User-Agent', 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2;)')]
    opener.addheaders = [('Host', 'ad.smartclip.net')]
    """
    opener.addheaders = [('Referer', 'http://www.vevo.com'),
                         ('User-Agent', 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2;)')]

    if extraheader:
        opener.addheaders = [('X-Requested-With', 'XMLHttpRequest')]
    if addoncompat.get_setting('location')==1:
        opener.addheaders = [('X-Forwarded-For', '12.13.14.15')]
    """
    usock=opener.open(url)
    response=usock.read()
    usock.close()
    #if os.path.isfile(COOKIEFILE):
    cj.save(COOKIEFILE, ignore_discard=True)
    return response

def auto_resume():
	if __settings__.getSetting('autoresume') == '1':
		log('Using autoresume')
		xbmc.sleep(1000)
		while xbmc.getCondVisibility("Player.HasVideo"):
			xbmc.sleep(100)
			if xbmc.getCondVisibility("Player.Paused"):
				log('Video buffering')
				xbmc.sleep(5000)
				if xbmc.getCondVisibility("Player.Paused"):
					log('Attempt to resume')
					xbmc.Player().pause()

		log('Stopping autoresume')
		log('Restoring live menu')
		LIVESELECTION(livestream_url)
		log('Live menu restored')
		return

	else:
		log('Not using autoresume')

def get_video_ad(flashvars):
	log(flashvars)
	log('attempting to get commercial')

	match_preroll1_pfad_adv=re.compile('&preroll1_pfad_adv=(.+?)&').findall(flashvars)
	log('preroll1_pfad_adv: '+match_preroll1_pfad_adv[0])
	match_fallback_pfad=re.compile('&fallback_pfad=(.+?)&').findall(flashvars)
	log('fallback_pfad: '+match_fallback_pfad[0])
	match_opener_pfad=re.compile('&opener_pfad=(.+?)&').findall(flashvars)
	log('opener_pfad: '+match_opener_pfad[0])
	match_preroll1_pfad_sma=re.compile('preroll1_pfad_sma=(.+?)\?').findall(flashvars)
	log('preroll1_pfad_sma: '+match_preroll1_pfad_sma[0])


	#check if preroll1_pfad_adv is avaiable
	response = getUrlCookie(match_preroll1_pfad_adv[0])
	#print response
	log('Check for "OAS adverServe"')
	if 'OAS adverServe' in response:
		log('Trying "OAS adverServe"')
		try:
			log('Try to get preroll')
			match_MediaFiles=re.compile('<MediaFiles>(.+?)</MediaFiles>', re.DOTALL).findall(response)
			match_MediaFile=re.compile('<MediaFile.+?<!\[CDATA\[(.+?)\]\]>', re.DOTALL).findall(match_MediaFiles[0])
			video = match_MediaFile[0]
			log('Possible ad: '+video)
			return video,''#funktioniert
		except:#wenn der preroll scheitert, dann gehts hier mit den fallback+opener weiter
			log('Preroll failed, try fallback')
			#video = get_ad_oas(match_fallback_pfad[0])#3sek intro
			#log('Fallback is choosen')
			#log('Possible ad: '+video)
			#return video,''#funktioniert bis hier/2te ad muss noch rein
			try:
				video = get_ad_oas(match_opener_pfad[0])
				log('Opener is choosen')
				log('Possible ad: '+video)
				return video,''#funktioniert
			except:
				log('playing opener')
	else:
		log('No "OAS adverServe" found')
	
	log('Trying other ad')



	a = 1
	while not a == 0:
		url = match_preroll1_pfad_sma[0]
		url = url.replace('[random]',num_gen(11))
		log('doubleclick url: '+url)
		response = getUrlCookie(url)
		#print response
		if '<VASTAdTagURI>' in response:
			log('VAST ad found')
			match_VASTAdTagURI=re.compile('<VASTAdTagURI><!\[CDATA\[(.+?)\]\]></VASTAdTagURI>').findall(response)
			log('Opening: '+match_VASTAdTagURI[0])
			response = getUrl(match_VASTAdTagURI[0])
			match_MediaFiles=re.compile('<MediaFiles>(.+?)</MediaFiles>', re.DOTALL).findall(response)
			match_MediaFile=re.compile('<MediaFile .+?><!\[CDATA\[(.+?)\]\]>').findall(match_MediaFiles[0])

			log('Video file is: '+match_MediaFile[0])
			#match_Duration=re.compile('<Duration>.+?:.+?:(.+?)</Duration>', re.DOTALL).findall(response)
			return match_MediaFile[0],''#match_Duration[0]

		elif '<adDataURL>' in response:
			log('designTheme found')
			match_designTheme=re.compile('<adDataURL>(.+?)</adDataURL>').findall(response)
			log('designTheme url: '+match_designTheme[0])
			response = getUrl(match_designTheme[0])

			match_videoPath=re.compile('<videoPath>(.+?)</videoPath>').findall(response)
			log('videoPath: '+match_videoPath[0])
			match_videoID=re.compile('<videoID>(.+?)</videoID>').findall(response)
			log('videoID: '+match_videoID[0])
			match_videoName=re.compile('<videoName>(.+?)</videoName>').findall(response)
			log('videoName: '+match_videoName[0])
			match_realAdId=re.compile('<realAdId>(.+?)</realAdId>').findall(response)
			log('realAdId: '+match_realAdId[0])
			match_adId=re.compile('<adId>(.+?)</adId>').findall(response)
			log('adId: '+match_adId[0])
			match_videoLength=re.compile('<videoLength>(.+?)</videoLength>').findall(response)
			log('videoLength: '+match_videoLength[0])
			log('commercial url: '+match_videoPath[0]+match_videoID[0]+'/fl8_'+match_videoName[0]+'-600.flv?ewadid='+match_realAdId[0]+'&eid='+match_adId[0])
			return match_videoPath[0]+match_videoID[0]+'/fl8_'+match_videoName[0]+'-600.flv?ewadid='+match_realAdId[0]+'&eid='+match_adId[0],match_videoLength[0]

		elif '<Ad id="EWAD">' and 'MediaFile' in response:
			log('EWAD ad found')
			match_MediaFiles=re.compile('<MediaFiles>(.+?)</MediaFiles>', re.DOTALL).findall(response)
			#print match_MediaFiles[0]
			match_MediaFile=re.compile('<MediaFile .+?><!\[CDATA\[(.+?)\]\]>').findall(match_MediaFiles[0])
			log('Playing EWAD ad')
			log('File is: '+match_MediaFile[0])
			return match_MediaFile[0],''#works
		else:
			log('No ad recieved')
			log(response)
			log('Playing fallback')
			video = get_ad_oas(match_fallback_pfad[0])
			return video,''


def get_ad_oas(url):
	response = getUrlCookie(url)
	#print response
	match_MediaFile=re.compile('<MediaFile.+?<!\[CDATA\[(.+?)\]\]>', re.DOTALL).findall(response)
	return match_MediaFile[0]

	"""
	a = 1
	while not a == 0:

		log('attempting to get commercial')
		url = 'http://ad.de.doubleclick.net/ad/pushbackde.smartclip/laola1.tv.as3.smartclip/;scadn=0;sccat=adnpbk;scsid=1036492;sz=400x320;dcmt=text/xml;ord='+num_gen(11)
		log('doubleclick url: '+url)
		response = getUrlCookie(url)

		try:
			match_designTheme=re.compile('<adDataURL>(.+?)</adDataURL>').findall(response)
			log('designTheme url: '+match_designTheme[0])
			response = getUrl(match_designTheme[0])

			match_videoPath=re.compile('<videoPath>(.+?)</videoPath>').findall(response)
			log('videoPath: '+match_videoPath[0])
			match_videoID=re.compile('<videoID>(.+?)</videoID>').findall(response)
			log('videoID: '+match_videoID[0])
			match_videoName=re.compile('<videoName>(.+?)</videoName>').findall(response)
			log('videoName: '+match_videoName[0])
			match_realAdId=re.compile('<realAdId>(.+?)</realAdId>').findall(response)
			log('realAdId: '+match_realAdId[0])
			match_adId=re.compile('<adId>(.+?)</adId>').findall(response)
			log('adId: '+match_adId[0])
			match_videoLength=re.compile('<videoLength>(.+?)</videoLength>').findall(response)
			log('videoLength: '+match_videoLength[0])
			log('commercial url: '+match_videoPath[0]+match_videoID[0]+'/fl8_'+match_videoName[0]+'-600.flv?ewadid='+match_realAdId[0]+'&eid='+match_adId[0])
			return match_videoPath[0]+match_videoID[0]+'/fl8_'+match_videoName[0]+'-600.flv?ewadid='+match_realAdId[0]+'&eid='+match_adId[0],match_videoLength[0]
		except:
			#return
			#print response
			if 'cachebuster' in response:
				log('CACHEBUSTER ad')
				match_VASTAdTagURI=re.compile('CDATA\[(.+?)\]').findall(response)
				VASTAdTagURI = match_VASTAdTagURI[0]
				VASTAdTagURI = VASTAdTagURI.replace('[CACHEBUSTER',num_gen(11))
				log('VASTAdTagURI: '+match_VASTAdTagURI[0])
				log('TODO')
				#print response
				return
			
			else:
				
				if '<Ad id="EWAD">' in response:
					log('EWAD ad')
					return
				elif 'VINDICO' in response:
					log('VINDICO ad')
					match_MediaFile=re.compile('<MediaFile.+?CDATA\[(.+?)\]').findall(response)
					
					return match_MediaFile[0],''
				match_VASTAdTagURI=re.compile('<VASTAdTagURI><!CDATA\[(.+?)\]').findall(response)
				log('VASTAdTagURI: '+match_VASTAdTagURI[0])
				response = getUrlCookie(match_VASTAdTagURI[0])
				#print response
				#match_AdTitle=re.compile('<AdTitle>(.+?)</AdTitle>').findall(response)
				#log('AdTitle: '+match_AdTitle[0])
				#http://cache.vindicosuite.com/xumo/swf/prod/Xumo.swf?rt=swf&statusBar=false&rotationid=SMARTCLIP_DE_Sky_Preroll_VPAID&version=release&usage=vpaid&etoplevel=true&ximpid=1036492&rnd=1050124064
				response = getUrl('http://addirector.vindicosuite.com/feeds/addirector/vast/2/?renderVer=xumo_1.1.0.2hf41&rotationId='+match_AdTitle[0]+'&rnd='+num_gen(10)+'&version=release&rt=swf&ximpid=1036492&fromXumo=true')
				#print response
				match_MediaFile=re.compile('<MediaFile.+?CDATA\[(.+?)\]').findall(response)
				log('MediaFile: '+match_MediaFile[0])
				match_Duration=re.compile('<Duration>00:00:(.+?)</Duration>').findall(response)
				return match_MediaFile[0],match_Duration[0]
	"""

def force_play(video_url):
	
	if not xbmcplugin.getSetting(pluginhandle,"autoplay") == '0':
		log('autoplay enabled, waiting for player')
		i = 0
		while not xbmc.getCondVisibility("Player.HasVideo"):#wait till player started video
			i = i + 1
			if i == 500: #timeout after 5s
				log('videoplayer timeout')
				return
			xbmc.sleep(10)

		log('time till player started video: '+str(i*10)+'ms')

		xbmc.sleep(100)

		if xbmc.getCondVisibility("Player.Paused"):
			log('starting autoplay')
		else:
			log('video started on its own')
			return
		n = 1
		while n != 50:#timeout after 5s
			if xbmc.Player().isPlaying()==True and int(xbmc.Player().getTime())==0 and xbmc.getCondVisibility("Player.Paused"):#attempt to play video
				xbmc.Player().pause()
			else:
				log('autoplay successfull after '+str(n)+' attempt(s)')
				return
			xbmc.sleep(100)
			n = n + 1
		log('autoplay unsuccessfull after '+str(n)+' attempts')

	else:
		log("autoplay disabled")
		return
	"""
	if not xbmcplugin.getSetting(pluginhandle,"autoplay") == '0':
		log('Autoplay enabled')
		log('Chosen video: '+video_url)
		log('Check if an other video is playing')

		try: 
			current_video = xbmc.Player().getPlayingFile()
		except:
			log('No video active')
			current_video = ''


		#log('Current video: '+xbmc.Player().getPlayingFile())
		i = 0
		while not current_video == video_url:#wait till player finishes previous video
			if i == 1:
				log('Other video playing, waiting...')
			i = i + 1

			if i == 500: #timeout after 5s
				log('videoplayer timeout #1')
				return
			xbmc.sleep(10)

			try: 
				current_video = xbmc.Player().getPlayingFile()
			except:
				current_video = ''

		log('Current video old: '+current_video)
		log('Current video: '+xbmc.Player().getPlayingFile())

		if i == 0:
			log('Current video is active')

		
			#xbmc.sleep(100)
		else:
			log('Previous video has stopped')
			log('Time till player ended previous video: '+str(i*10)+'ms')

			log('Waiting for player to load the current video')
		i = 0
		while not xbmc.getCondVisibility("Player.HasVideo"):#wait till player started video
			i = i + 1
			if i == 500: #timeout after 5s
				log('videoplayer timeout#2')
				return
			xbmc.sleep(10)

		n = 0
		m = 0
		while not m == 1:#wait till time is in player, xbmc bug?
			try:
				get_time = int(xbmc.Player().getTime())
				log('Time is in player now')
				break
			except:
				n = n + 1
			
			if n == 500: #timeout after 5s
				log('videoplayer timeout#3')
				return

			xbmc.sleep(10)

		log('Time till player activated video: '+str(i*10)+'ms')
		log('Time till time took in player: '+str(n*10)+'ms')

		xbmc.sleep(100)
		print '++++++++++++++++++++++++++++++++++++++'
		print xbmc.getCondVisibility("Player.Paused")
		print xbmc.Player().isPlaying()
		print int(xbmc.Player().getTime())
		print xbmc.getCondVisibility("Player.Paused")
		"#"#"
		if xbmc.getCondVisibility("Player.Paused"):
			log('starting autoplay')
		else:
			xbmc.sleep(50)
			if not xbmc.getCondVisibility("Player.Paused"):
				print '######################################################'
				print xbmc.getCondVisibility("Player.Paused")
				xbmc.sleep(100)
				if not xbmc.getCondVisibility("Player.Paused"):
					print xbmc.getCondVisibility("Player.Paused")
					xbmc.sleep(10000)
					log('video started on its own')
					return
				else:
					log('starting autoplay')
			else:
				log('starting autoplay')
		"#"#"

		n = 0
		k = 0
		while n != 50:#timeout after 5s
			print '##################time int, real?'
			print int(xbmc.Player().getTime())
			print xbmc.Player().getTime()
			#if xbmc.Player().isPlaying()==True and int(xbmc.Player().getTime())==0 and xbmc.getCondVisibility("Player.Paused"):#attempt to play video
			if xbmc.Player().isPlaying()==True and int(xbmc.Player().getTime()*100)==0:# and xbmc.getCondVisibility("Player.Paused"):#attempt to play video
				xbmc.Player().pause()
			else:
				log('autoplay successfull after '+str(n)+' attempt(s)')
				print xbmc.getCondVisibility("Player.Paused")
				print xbmc.Player().isPlaying()
				print int(xbmc.Player().getTime())
				print xbmc.Player().getTime()
				if not k == 20:
					k = k + 1
				else:
					log('autoplay successfull after '+str(n)+' attempt(s)')
					print xbmc.getCondVisibility("Player.Paused")
					print xbmc.Player().isPlaying()
					print int(xbmc.Player().getTime())
					print xbmc.Player().getTime()
					return
			xbmc.sleep(100)
			n = n + 1
		log('autoplay unsuccessfull after '+str(n)+' attempts')

	else:
		log("autoplay disabled")
		return
			
	"""

def log(message):
	if debug == '1':
		print "#####Laola1 Debug: "+message
	return



def addLinkOld(name,url,iconimage):
	iconimage = 'http://streamaccess.unas.tv/flash/ittf/itTV_welcome_2.jpg'
	fanart = iconimage
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
	liz.setProperty('fanart_image',fanart)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        return ok

def addLink(name,url,mode,iconimage,fanart=''):
	iconimage = 'http://streamaccess.unas.tv/flash/ittf/itTV_welcome_2.jpg'
	fanart = iconimage
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&thumb="+urllib.quote_plus(iconimage)+"&name="+urllib.quote_plus(name)##
	ok=True##
	liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)##
	liz.setInfo( type="Video", infoLabels={ "Title": name } )##
	liz.setProperty('IsPlayable', 'true')##
	liz.setProperty('fanart_image',fanart)
	liz.setProperty('mimetype', 'video/x-flv')
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz)##
	return ok


def addDir(name,url,mode,iconimage):
	iconimage = 'http://streamaccess.unas.tv/flash/ittf/itTV_welcome_2.jpg'
	fanart = iconimage
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
	liz.setProperty('fanart_image',fanart)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
        
              
params=get_params()
url=None
name=None
mode=None
link=None
thumb=None

try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        name=urllib.unquote_plus(params["link"])
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
print "Thumbnail: "+str(thumb)

if mode==None or url==None or len(url)<1:
        print ""
        INDEX()
       
elif mode==1:
        print ""+url
        TOPICSELECTION(url)
        
elif mode==2:
        print ""+url
        FINESELECTION(url)  
		
elif mode==3:
        print ""+url
        VIDEOSELECTION(url)            

elif mode==4:
        print ""+url
        PLAY_LIVE(url,name)
        
elif mode==5:
        print ""+url
        LIVESELECTION(url)
        
elif mode==6:
        print ""+url
        VIDEOLIVELINKS(url,name,thumb)        

elif mode==7:
        print ""+url
        LIVE(url)  

elif mode==10:
        print ""+url
        PLAY_VIDEO(url,name,thumb) 

elif mode==11:
        print ""+url
        PLAY_LIVE_1B(url,name,thumb) 

  
xbmcplugin.endOfDirectory(int(sys.argv[1]))
