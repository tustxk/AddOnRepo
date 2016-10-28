import urllib,urllib2,re,xbmcplugin,xbmcgui

pluginhandle = int(sys.argv[1])

cat_req = urllib2.Request('http://www.spobox.tv/')
cat_req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
cat_response = urllib2.urlopen(cat_req)
cat_list=cat_response.read()
cat_response.close()
cat=re.compile('<div id="bottom">(.+?)</div>', re.DOTALL).findall(cat_list)

def CATEGORIES():
        match=re.compile('<h3 style="background-image:url\((.+?)\)">\n<a href="(.+?)">(.+?)</a>\n</h3>', re.DOTALL).findall(cat[0])
        for thumb,url,name in match:
                addDir(name,url,1,thumb)
                       
def INDEX(url):
        match1=re.compile(url+'"(.+?)</ol>', re.DOTALL).findall(cat[0])
        match2=re.compile('<a href="(.+?)">(.+?)</a>').findall(match1[0])
        for url,name in match2:
                addDir(name,'http://www.spobox.tv'+url,2,'')
def VIDEOS(url):
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
#<a href="/hockey/vier-nationen-turnier/hockey-niederlande-deutschland" title="Hockey: Niederlande gegen Deutschland - Vier-Nationen Turnier, Hockey"><span class="thumb mini"><img alt="Vier-Nationen Turnier, Hockey: Hockey: Niederlande gegen Deutschland" src="http://manager.vidibus.net/mediafiles/d134/c070/9833/012e/6dcf/6c62/6d58/b44c/hockey-vier-nationen-turnier-2011-07-24-niederlande-deutschland_96x54.jpg" /><span class="duration prop">01:31:37</span></span>

        match=re.compile('<a href="(.+?)" title="(.+?)">.+?<img alt=".+?" src="(.+?)" />').findall(link)
        for url,name,thumb in match:
		thumb=thumb.replace('96x54','620x350')
                addLink(name,'http://www.spobox.tv'+url,3,thumb)


def VIDEOLINKS(url,name):
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	match=re.compile('<a data-acudeo=".+?" data-autoplay=".+?" data-duration=".+?" data-keyword=".+?" href="(.+?)" id=".+?">').findall(link)
	for url in match:
	        item = xbmcgui.ListItem(path=url)
	return xbmcplugin.setResolvedUrl(pluginhandle, True, item)
        
                
        

                
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



def addLink(name,url,mode,iconimage):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)##
	ok=True##
	liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)##
	liz.setInfo( type="Video", infoLabels={ "Title": name } )##
	liz.setProperty('IsPlayable', 'true')##
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz)##
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

elif mode==2:
        print ""+url
        VIDEOS(url)
        
elif mode==3:
        print ""+url
        VIDEOLINKS(url,name)



xbmcplugin.endOfDirectory(int(sys.argv[1]))
