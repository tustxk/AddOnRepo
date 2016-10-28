# coding: utf-8
from addon.common.addon import Addon
from addon.common.net import Net
#from metahandler import metahandlers
import xbmc,xbmcplugin,xbmcgui,xbmcaddon,xbmcvfs
import urllib,urllib2,re,os,sys,htmllib,string,StringIO,logging,random,array,time,datetime
import unicodedata
import urlresolver
import copy
import HTMLParser







# 501-POSTER WRAP 503-MLIST3 504=MLIST2 508-FANARTPOSTER 
#confluence_views = [500,501,502,503,504,508]


addon = Addon('plugin.video.frmovies', sys.argv)
xaddon = xbmcaddon.Addon(id='plugin.video.frmovies')
AddonPath = xaddon.getAddonInfo('path')
IconPath = AddonPath + "/icons/"

def CATEGORIES():
	page='1'
	addDir('Top 20','http://frmovies.net/top.php?page='+page,1,'http://frmovies.net/imdoc/frmovies1.png')
	addDir('Action','http://frmovies.net/cat.php?film=2&page='+page,1,IconPath +'action.png')
	addDir('Aventure','http://frmovies.net/cat.php?film=9&page='+page,1,IconPath +'aventure.png')
	addDir('Comédies','http://frmovies.net/cat.php?film=6&page='+page,1,IconPath +'comedy.png')
	addDir('Animation','http://frmovies.net/cat.php?film=7&page='+page,1,IconPath +'animation.png')
	addDir('Horreur','http://frmovies.net/cat.php?film=13&page='+page,1,IconPath +'horror.png')
	addDir('Guerre','http://frmovies.net/cat.php?film=10&page='+page,1,IconPath +'guerre.png')
	addDir('Fantastique','http://frmovies.net/cat.php?film=8&page='+page,1, IconPath +'fantastique.png')
	addDir('Science Fiction','http://frmovies.net/cat.php?film=12&page='+page,1, IconPath +'scifi.png')
	addDir('Policier','http://frmovies.net/cat.php?film=3&page='+page,1, IconPath +'police.png')
	addDir('RECHERCHE',' ',5, 'http://frmovies.net/imdoc/frmovies1.png')

####################
#list top 20 movies 
###################                 
def INDEX(url):
	setView('movies', 'movie-view')
	req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()      
	match=re.compile('<a href="(.+?)"><img src="(.+?)" alt="(.+?)streaming').findall(link)
		
	try:
		match=[(x,y,HTMLParser.HTMLParser().unescape(z)) for x,y,z in match]
	except:
		pass
        for url,thumb,name in match:
                addDir3(name,url,2,thumb)


def BINDEX(url): 
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()      
	match=re.compile('img src=(.+?) border=0 height=52 width=39 alt=(.+?)></span></div></td>\s*<td width=1% height=2></td>\s*<td width=91% valign=top>\s*<a class=Style1 href=(.+?)>').findall(link) 
	match=str(match)
	match=match.replace('/watch','http://frmovies.net/watch')
	match=re.compile("\('(.+?)', '(.+?)', '(.+?)'").findall(match)
        for thumb,name,url in match:
                addDir(name,url,2,thumb)

	
####################
#find links to host 
################### 
def FILMPAGE(url): 
	#global host
	#global thumb	
	req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()    
	match=re.compile('style230"><a href="(.+?)" target').findall(link)
	match=str(match)
	match=match.replace('[','')
	match=match.replace(']','')
	match=re.sub("'http://frmovies.net/watch/vimpleru.*?'"," ",match)
	match=match.replace(',','')
	match=match.replace('\'','')
	match=match.split()

	host=re.compile('/><a href="http://frmovies.net/watch/(.+?).php').findall(link)
	host=fixnames(host)	
	thumb=re.compile('og:image" content="(.+?)"').findall(link) 
	thumb=str(thumb[0])
	result=zip(host,match)
	
	
        for host,url in result:
                addDir2(name,url,3,thumb,host)



##################################>
#fix host names
def fixnames(host):
	host = [h.replace('pic', 'phimdata') for h in host]
	host = [h.replace('ywatch', 'youwatch') for h in host]
	host=[x for x in host if x != "vimpleru"]
	return host
	

##################################>
def setView(content, viewType):

    if content:
        xbmcplugin.setContent(int(sys.argv[1]), content)
    if addon.get_setting('auto-view') == 'true':
        xbmc.executebuiltin("Container.SetViewMode(%s)" % addon.get_setting(viewType) )

####################
#resolve and play
###################
def VIDEOLINKS(url):
##################################>
	temp=globals()
	temp=str(temp)
	thumb=re.compile("'iconimage': '(.+?)',").findall(temp)
	thumb=urllib.unquote(thumb[0])
##################################>
	temp=globals()
	temp=str(temp)
	host=re.compile('/watch/(.+?).php').findall(temp)
	host=urllib.unquote(host[0])
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	
	if host=='pic':
		match=re.compile('proxy.swf&proxy.link=(.+?)&autostart').findall(link)	
		url=urllib.unquote(match[0])
		req = urllib2.Request(url)
		req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
		response = urllib2.urlopen(req)
		link=response.read()
		response.close()
		match=re.compile('{"url":"(.+?)","height"').findall(link)
		addLink(name,match[1],thumb)
	elif host=='vk' or host=='vkk':
		#req = urllib2.Request(url)
		#req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
		#response = urllib2.urlopen(req)
		#link=response.read()
		#response.close()
		match=re.compile("height: 350px' src='(.+?)' scrolling=").findall(link)		
		response = urllib2.urlopen(match[0])
		html = response.read()
		streamurl=re.compile('360=(.+?)&amp').findall(html)
		if len(streamurl)>0:
			addLink(name,streamurl[0],thumb)
		else:
			print 'ERROR MSG'
##############
	elif host=='ywatch':
		
		match=re.compile("src='(.+?)' scrolling").findall(link)
		match=urllib.unquote(match[0])
		response = urllib.urlopen(match)
		link = response.read()
		response.close()
		match=re.compile('\|provider\|(.+?)\|(.+?)\|(.+?)\|(.+?)\|(.+?)\|setup\|').findall(link)
		match=str(match)
		match=match.replace('[(\'','')
		match=match.replace('\')]','')
		match=match.split("', '")
		streamurl='http://'+match[4]+'.youwatch.org:'+match[3]+'/'+match[2]+'/'+match[1]+'.'+match[0]+'?start=0'
		
		addLink(name,streamurl,thumb)

	elif host=='vidto':
		match=re.compile("src='(.+?)' scrolling").findall(link)
		match=urllib.unquote(match[0])
		response = urllib.urlopen(match)
		link = response.read()
		response.close()
		response = urllib.urlopen('http://vidto.me/embed-z9vbakngpihg-700x350.html')
		link = response.read()
		response.close()
		match1=re.compile('\|video\|(.+?)\|').findall(link)
		match2=re.compile('\|240p\|(.+?)\|').findall(link)
		streamurl="http://31.207.1."+match1[0]+"/"+match2[0]+"/video.mp4?start=0"
		print streamurl
		print '^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^'
		addLink(name,streamurl,thumb)

	elif host=='streaml':
		match=re.compile("file: '(.+?)',").findall(link)
		addLink(name,match[0],thumb)

	elif host=='uph':
		match1=re.compile("src='(.+?)ideo' videoID=").findall(link)
		match2=re.compile("ideo' videoID='(.+?)'>").findall(link)
		link=match1[0]+"/"+match2[0]
		response = urllib.urlopen(link)
		link = response.read()
		response.close()
		match=re.compile("url: '(.+?)'").findall(link)
		addLink(name,match[1],thumb)

	else:

		for num in range(2, 3):
			match=re.compile("px' src='(.+?)' scrolling").findall(link)
			if len(match)!=0: break
			match=re.compile('src="(.+?)" frameborder').findall(link)
			if len(match)!=0: break
			match=re.compile("iframe src='(.+?)' scrolling").findall(link)
			if len(match)!=0: break
			match=re.compile('iframe src="(.+?)" width').findall(link)
		
		stream_url = urlresolver.HostedMediaFile(match[0]).resolve()#+'client%3DFLASH'
			
		#stream_url=urllib.unquote(stream_url)
		print stream_url
		print '^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^'
		for url in match:
                	addLink(name,stream_url,thumb)


		
	
###############################
#play strm file in movie folder
###############################
def STRM(url):
	
	stream_url = urlresolver.HostedMediaFile(url).resolve()
	play=xbmc.Player(xbmc.PLAYER_CORE_AUTO) 
	xbmc.executebuiltin("SendClick(101,10)")
	time.sleep(10)
	xbmc.executebuiltin("SendClick(2002,10)")
	play.play(stream_url)
	#time.sleep(5)
	
	#xbmc.executebuiltin('Dialog.Close()')
	#play.play(stream_url)
	#xbmc.executebuiltin( "PlayMedia(stream_url)" )

	

#########################################################
def SEARCH():
        search_entered = ''
        keyboard = xbmc.Keyboard(search_entered, 'SEARCH FRMOVIES')
        keyboard.doModal()
	if keyboard.isConfirmed():
		result = keyboard.getText() .replace(' ','+') 
		result = 'http://frmovies.net/vu.php?q='+result
		BINDEX(result)

            #if search_entered == None:
                #return False
		
  
#########################################################              
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




def addLink(name,url,iconimage):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=str(url),listitem=liz)
        return ok

def addDir(name,url,mode,iconimage):
	
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
def addDir3(name,url,mode,iconimage):
	try:	name=name.encode('utf-8')
	except:
		pass
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

def addDir2(host,url,mode,iconimage,name):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(host)+"&iconimage="+str(iconimage)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
	#iconimage=globals()["thumb"]

        return ok        
              
params=get_params()
url=None
name=None
mode=None

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
        CATEGORIES()
       
elif mode==1:
        print ""+url
        INDEX(url)
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	p=re.compile('color=red face="tahoma"><strong>&nbsp;(.+?)&nbsp').findall(link)
	page=int(float(p[0]))
	page += 1
	pp=str(page)
	url = re.sub(r'(?is)page=.+', 'page=', url)
	addDir('SUIVANT',url+pp,1,'http://frmovies.net/imdoc/frmovies1.png')
	addDir('RECHERCHE',' ',5,'http://frmovies.net/imdoc/frmovies1.png')
	setView('movies', 'movie-view')

elif mode==2:
        print ""+url
        FILMPAGE(url)
     
elif mode==3:
        print ""+url
        VIDEOLINKS(url)

elif mode==4:
	#xbmc.Player().stop()
	STRM(url)

elif mode==5:
	SEARCH()
	
xbmcplugin.endOfDirectory(int(sys.argv[1]))
