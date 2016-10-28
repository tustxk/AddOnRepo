# -*- coding: iso-8859-1 -*-
import urllib,urllib2,re,xbmcplugin,xbmcgui

pluginhandle = int(sys.argv[1])


base_s = 'http://www.sachsen-fernsehen.de'
base_l = 'http://www.leipzig-fernsehen.de'
base_dd = 'http://www.dresden-fernsehen.de'

def CATEGORIES():
        addLinkOld('Sachsen Fernsehen Live','rtmp://video01.kanal8.de/sachsenfernsehenlive app=sachsenfernsehenlive swfurl=http://www.sachsen-fernsehen.de/jw/player/5.10/player.swf swfvfy=true pageUrl=http://www.sachsen-fernsehen.de playpath=Ug4wic7Hf21mEidKRMBLb621GMGBHhWC live=true','')
        addLinkOld('Leipzig Fernsehen Live','rtmp://video01.kanal8.de/leipzigfernsehenlive app=leipzigfernsehenlive swfurl=http://www.leipzig-fernsehen.de/jw/player/5.10/player.swf swfvfy=true pageUrl=http://www.leipzig-fernsehen.de playpath=myStream.sdp live=true','')
        addLinkOld('Dresden Fernsehen Live','rtmp://video07.kanal8.de/dresdenfernsehenlive app=dresdenfernsehenlive swfurl=http://www.dresden-fernsehen.de/jw/player/5.10/player.swf swfvfy=true pageUrl=http://www.dresden-fernsehen.de playpath=myStream.sdp live=true','')

	a = '8'
	s = 'sport'
	S = 'Sport'
	v = 'video'
	k = 'kanal'
	f = '5'
	l = 'leipzig'
        addLinkOld(a+S+' Live','rtmp://'+v+'90.'+k+a+'.de/'+a+s+'live app='+a+s+'live swfurl=http://www.'+l+'-'+f+'.de/swf/mediaplayer-'+f+'.'+f+'-licensed/player.swf swfvfy=true pageUrl=http://www.leipzig-fernsehen.de playpath=myStream.sdp live=true','')
        addDir('Sachsen Mediathek','meh',1,'')
        addDir('Leipzig Mediathek','http://www.leipzig-fernsehen.de/default.aspx?ID=5850',5,'')
        addDir('Dresden Mediathek','http://www.dresden-fernsehen.de/default.aspx?ID=11405',8,'')
        
################################sachsen################################


def LIST_S(url):#1
	addDir('Aktuell','http://www.sachsen-fernsehen.de/',2,'')
	addDir('Chemnitz','http://www.sachsen-fernsehen.de/Aktuell/Chemnitz/Seite/',2,'')
	addDir('Chemnitzer-Umland','http://www.sachsen-fernsehen.de/Aktuell/Chemnitzer-Umland/Seite/',2,'')
	addDir('Sachsen','http://www.sachsen-fernsehen.de/Aktuell/Sachsen/Seite/',2,'')
	addDir('Überregional','http://www.sachsen-fernsehen.de/Aktuell/Ueberregional/Seite/',2,'')
	addDir('campusKISTE','http://www.sachsen-fernsehen.de/Aktuell/campusKISTE/Seite/',2,'')
	addDir('Sport','http://www.sachsen-fernsehen.de/Aktuell/Sport/Meldungen-/Seite/',2,'')
	#addDir('Drehscheibe Chemnitz','http://www.sachsen-fernsehen.de/Archiv/Seite/',2,'')#TODO





def LIST_SENDUNGEN_S(url):#2
	response = getUrl(url)
	#print response
	#match_all=re.compile('<div id="ctl00_cphMain_ctl00_Position(.+?)<div class="positions right', re.DOTALL).findall(response)
	#print match_all[0]
	#match_item=re.compile('<div class="panel"(.+?)</div>', re.DOTALL).findall(match_all[0])
	match_item=re.compile('<div class="border">(.+?)</div>', re.DOTALL).findall(response)
	for item in match_item:
		if 'Video(s)' in item:
			#print '##################################'
			#print item

			match_thumb=re.compile('<img.+?src="(.+?)"', re.DOTALL).findall(item)
			match_name_a=re.compile('<h2.+?<a.+?>(.+?)</a>', re.DOTALL).findall(item)
			match_name_b=re.compile('<p class="text teaserText">(.+?)</p>', re.DOTALL).findall(item)
			match_url=re.compile('href="(.+?)"', re.DOTALL).findall(item)

			#print match_thumb[0].replace('&amp;','&')
			#print match_name_a[0]
			#print match_name_b[0]
			#print match_url[0]

			addLink(match_name_a[0]+' - '+match_name_b[0],base_s+match_url[1],4,match_thumb[0])

def PLAY_KANAL8(url,name):#4

	response = getUrl(url)
	#print response
	match=re.compile("'file': '(.+?)'").findall(response)
	#video = urllib.unquote(match[0])
	video = match[0]
	item=xbmcgui.ListItem(name, thumbnailImage='', path=video)
	item.setProperty('mimetype', 'video/x-flv')
	xbmcplugin.setResolvedUrl(pluginhandle, True, item)


################################leipzig################################

def LIST_L(url):#5
	response = getUrl(url)
	match_all=re.compile('<div id="ctl11_content_div">(.+?)</div>', re.DOTALL).findall(response)
	#print match_all[0]
	match_item=re.compile('<img(.+?)</a>', re.DOTALL).findall(match_all[0])

	for item in match_item:
		#print '#################################'
		#print item
		match_thumb=re.compile('src="(.+?)"', re.DOTALL).findall(item)
		match_name=re.compile('<a.+?<strong>(.+?)/strong>', re.DOTALL).findall(item)
		match_url=re.compile('href="(.+?)"', re.DOTALL).findall(item)
		#print match_thumb[0].replace('&amp;','&')
		#print match_name[0]
		#print match_url[0]
		if not match_name[0] == 'Drehscheibe<br /><':
			if 'http' in match_thumb[0]:
				thumb = match_thumb[0]
			else:
				thumb = 'http://media61.kanal8.de/'+match_thumb[0]
			name = repair_name(match_name[0])
			name = name.replace('<br />','')
			name = name.replace(' <','')
			name = name.replace('<','')
			name = name.replace('&nbsp;','')
			addDir(name,match_url[0],6,thumb)


def LIST_SENDUNGEN_REGIO(url,name,thumb):#6
	#print '#####################################thumb'
	#print thumb
	response = getUrl(url)
	match_iframe=re.compile('iframe.+?src="(.+?)"', re.DOTALL).findall(response)#wtf... iframes in 2013
	#print '#####################################iframe'
	#print match_iframe
	for miframe in match_iframe:
		if 'www.regio-tv-stream.de' in miframe:
			iframe = miframe
			#print '############################################'
			#print iframe
			
	response = getUrl(iframe)
	match_item=re.compile('<li><a href="(.+?)">(.+?)</a>', re.DOTALL).findall(response)
	#print match_item
	for half_url,date in match_item:

		#match_name=re.compile('<h2.+?<a.+?>(.+?)</a>', re.DOTALL).findall(item)
		#match_url=re.compile('href="(.+?)"', re.DOTALL).findall(item)
		#print match_thumb[0].replace('&amp;','&')
		#print match_name_a[0]
		#print match_name_b[0]
		#print match_url[0]

		addLink(name+' - '+date,iframe+'/'+half_url,7,thumb)

def PLAY_REGIO(url,name,thumb):#7
	response = getUrl(url)
	#print response
	"""
	match=re.compile("flashvars='file=(.+?)&").findall(response)
	video = urllib.unquote(match[0])
	#video = match[0]
	item=xbmcgui.ListItem(name, thumbnailImage=thumb, path=video)
	#item.setProperty('mimetype', 'video/x-flv')
	xbmcplugin.setResolvedUrl(pluginhandle, True, item)
	"""
	match_swf=re.compile("src:'(.+?)'").findall(response)
	match_rtmp=re.compile("streamer: '(.+?)'").findall(response)
	match_file=re.compile("file': '(.+?)'").findall(response)
	#'rtmp://video01.kanal8.de/sachsenfernsehenlive app=sachsenfernsehenlive swfurl=http://www.sachsen-fernsehen.de/jw/player/5.10/player.swf swfvfy=true pageUrl=http://www.sachsen-fernsehen.de playpath=Ug4wic7Hf21mEidKRMBLb621GMGBHhWC live=true'

	try:
		video= match_rtmp[0]+' swfurl='+match_swf[0]+' swfvfy=true playpath='+match_file[0]
	except:
		match=re.compile("flashvars='file=(.+?)&").findall(response)
		video = urllib.unquote(match[0])

	item=xbmcgui.ListItem(name, thumbnailImage=thumb, path=video)
	#item.setProperty('mimetype', 'video/x-flv')
	xbmcplugin.setResolvedUrl(pluginhandle, True, item)
        

################################nunuland################################

def LIST_DD(url):#8
	response = getUrl(url)
	#print '#################################'
	#print response
	match_all=re.compile('<a class="MainMenuL" href="default.aspx\?ID=11405">TV-Serien</a>(.+?)<td class="MainMenuCell">', re.DOTALL).findall(response)
	#print '#################################'
	#print match_all
	match_item=re.compile('<td class="SubMenuCell">(.+?)</td>', re.DOTALL).findall(match_all[0])
	#print '#################################'
	#print match_item

	for item in match_item:
		#print '#################################'
		#print item
		match_name=re.compile('>(.+?)<', re.DOTALL).findall(item)
		match_url=re.compile('href="(.+?)"', re.DOTALL).findall(item)
		addDir(match_name[0],base_dd+'/'+match_url[0],9,'')
	addDir('Dresden Markt','http://www.dresden-fernsehen.de/default.aspx?ID=12368',6,'')


def LIST_SENDUNGEN_DD(url):#9
	response = getUrl(url)
	#print response
	#match_all=re.compile('<div id="ctl00_cphMain_ctl00_Position(.+?)<div class="positions right', re.DOTALL).findall(response)
	#print match_all[0]
	#match_item=re.compile('<div class="panel"(.+?)</div>', re.DOTALL).findall(match_all[0])
	match_item=re.compile('<div class="newsListDiv listitem clearfix">(.+?)<span class="floater" >', re.DOTALL).findall(response)
	for item in match_item:
		#print '##################################'
		#print item

		#match_thumb=re.compile('<img.+?src="(.+?)"', re.DOTALL).findall(item)
		match_name=re.compile('<a.+?>(.+?)</a>').findall(item)
		match_url=re.compile('href="(.+?)"', re.DOTALL).findall(item)

		#print match_thumb[0].replace('&amp;','&')
		#print match_name_a[0]
		#print match_name_b[0]
		#print match_url[0]

		addLink(match_name[-3],base_dd+'/'+match_url[0],4,'')


def getUrl(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
	return link

def repair_name(name):
	#name = name.replace('','')
	name = name.replace('&amp;','&')
	name = name.replace('&uuml;','ü')
	name = name.replace('&auml;','ä')
	return name

                
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


def addLinkOld(name,url,iconimage):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        return ok

def addLink(name,url,mode,iconimage):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
	liz.setInfo( type="Video", infoLabels={ "Title": name } )
	liz.setProperty('IsPlayable', 'true')
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz)
	return ok

def addDir(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&thumb="+urllib.quote_plus(iconimage)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
        
              
params=get_params()
url=None
name=None
mode=None
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
        CATEGORIES()
       
elif mode==1:
        print ""+url
        LIST_S(url)
        
elif mode==2:
        print ""+url
        LIST_SENDUNGEN_S(url)
        
#elif mode==3:
#        print ""+url
#        INDEX_PLAYTUBE(url)

elif mode==4:
        print ""+url
        PLAY_KANAL8(url,name)

elif mode==5:
        print ""+url
        LIST_L(url)
        
elif mode==6:
        print ""+url
        LIST_SENDUNGEN_REGIO(url,name,thumb)

elif mode==7:
        print ""+url
        PLAY_REGIO(url,name,thumb)

elif mode==8:
        print ""+url
        LIST_DD(url)

elif mode==9:
        print ""+url
        LIST_SENDUNGEN_DD(url)



xbmcplugin.endOfDirectory(int(sys.argv[1]))
