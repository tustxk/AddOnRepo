import urllib,urllib2,re,os,xbmc,xbmcplugin,xbmcgui,xbmcaddon,xbmcvfs
import httplib,cookielib,sys,string,StringIO,time,base64,logging,urlresolver,datetime
import mechanize
import threading,BeautifulSoup,HTMLParser,zipfile,Queue,gzip,glob,random,socket,codecs
try:
    import json
except ImportError:
    import simplejson as json

from t0mm0.common.addon import Addon
addon = Addon('plugin.video.animeget', sys.argv)

__settings__ = xbmcaddon.Addon(id='plugin.video.animeget')
__home__ = __settings__.getAddonInfo('path')

addonPath=__home__
artPath=addonPath+'/art/'
ICON = os.path.join(__home__, 'icon.png')
fanart = os.path.join(__home__, 'fanart.jpg')

def addLink(name,url,iconimage):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        return ok

def addDirV(name,name2,url,type2,mode,iconimage,fanimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&nm="+urllib.quote_plus(name2)+"&tp="+str(type2)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        liz.setProperty( "Fanart_Image", fanimage )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

###########################################

def vvVIDEOLINKS(url,name):
        req = urllib2.Request(url)
        br =  mechanize.Browser()
        br.open(url)
        response1 = br.follow_link(url_regex = "http://www.video44.net")
        newurl = br.geturl()
        
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('src="(.+?)"').findall(link)

        print match
        for url in match:
                if "videoweed.es" in url:
                        req = urllib2.Request(url)
                        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
                        response = urllib2.urlopen(req)
                        link=response.read()
                        response.close()
                        match=re.compile('flashvars.advURL="(.+?)"').findall(link)
                        try:
                                addLink('Videoweed',urlresolver.resolve(match[0]),artPath + 'videoweed.jpg')
                        except:
                                continue

#                if "videofun.me" in url:
#												print "VideoFun.me is currently not handdled."
#                				addDirV('VideoFun.me is currently not handdled.','sorry',urlA,0,6,'','')
#                				addDirV('VideoFun.me is currently not handdled.','sorry',urlA,0,6,ICON,fanart)
#                        req = urllib2.Request(url)
#                        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
#                        response = urllib2.urlopen(req)
#                        link=response.read()
#                        response.close()
#                        matcha=re.compile('url: "(.+?)", autoPlay: true, scaling: \'fit\'').findall(link)
#                        img3=artPath + '\gogoanime\vidweed.png'
#                        for img2 in matcha:
#                					img3=img2
#                        match=re.compile('url: "(.+?)", autoPlay: false, scaling: \'fit\', autoBuffering: false').findall(link)
#                        try:
#                                addLink('VideoFun',urllib.unquote_plus(match[0]),img3)
#                                #addLink('VideoFun',urlresolver.resolve(match[0]),artPath + '\gogoanime\\vidweed.png')
#                        except:
#                                continue

#                if "yourupload.com" in url:
#                				addDir('YourUpload.com is currently not handdled.','sorry',urlA,0,6,ICON,fanart)
#                        req = urllib2.Request(url)
#                        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
#                        response = urllib2.urlopen(req)
#                        link=response.read()
#                        response.close()
#                        match=re.compile('flashvars.advURL="(.+?)"').findall(link)
#                        try:
#                                addLink('YourUpload',urlresolver.resolve(match[0]),artPath + '\gogoanime\\vidweed.png')
#                        except:
#                                continue

                if "dailymotion.com" in url:
                        try:
                                addLink('DailyMotion',urlresolver.resolve(match[0]),artPath + 'dailymotion.jpg')
                        except:
                                continue
#                        req = urllib2.Request(url)
#                        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
#                        response = urllib2.urlopen(req)
#                        link=response.read()
#                        response.close()
#                        match=re.compile('flashvars.advURL="(.+?)"').findall(link)
#                        try:
#                                addLink('DailyMotion',urlresolver.resolve(match[0]),artPath + '\gogoanime\\vidweed.png')
#                        except:
#                                continue

#                if "video.google.com" in url:
#                				addDir('GoogleVideo is currently not handdled.','sorry',urlA,0,6,ICON,fanart)
#										addLink('GoogleVideo',url,artPath + '\gogoanime\vidweed.png')
#                        req = urllib2.Request(url)
#                        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
#                        response = urllib2.urlopen(req)
#                        link=response.read()
#                        response.close()
#                        match=re.compile('flashvars.advURL="(.+?)"').findall(link)
#                        try:
#                                addLink('GoogleVideo',urlresolver.resolve(match[0]),artPath + '\gogoanime\\vidweed.png')
#                        except:
                                continue

        if "video44.net" in newurl:
                req = urllib2.Request(newurl)
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
                response = urllib2.urlopen(req)
                link=response.read()
                response.close()
                match=re.compile(' file: "(.+?)"').findall(link)
                addLink('Video44',match[0],artPath + '\gogoanime\\video44.png')



        xbmcplugin.endOfDirectory(int(sys.argv[1]))
                       
