import urllib,urllib2,re,os,xbmc,xbmcplugin,xbmcgui,xbmcaddon,xbmcvfs
import httplib,cookielib,sys,string,StringIO,time,base64,logging,urlresolver,datetime
import mechanize
import threading,BeautifulSoup,HTMLParser,zipfile,Queue,gzip,glob,random,socket,codecs
import videolinks
from videolinks import vvVIDEOLINKS
from videolinks import *
try:
    import json
except ImportError:
    import simplejson as json


#Anime44 - by The Highway 2013.


__settings__ = xbmcaddon.Addon(id='plugin.video.anime44')
##__language__ = __settings__.getLocalizedString
__home__ = __settings__.getAddonInfo('path')
##__home__ = 'special://home/addons/plugin.video.anime44/art'
#special://home/addons/plugin.video.anime44/art

#addonPath=os.getcwd()
addonPath=__home__
artPath=addonPath+'/art/'
mainSite='http://www.anime44.com/'

#icon = xbmc.translatePath( os.path.join( __home__, 'icon.png' ) )
#__plugin__ = "Anime44"
#__authors__ = "The Highway"
#__credits__ = "o9r1sh of plugin.video.gogoanime for Videoweed and Video44 source parsing. TheHighway(Myself) for AnimeGet plugin (simular site)"
#home = xbmc.translatePath(addon.getAddonInfo('path'))
ICON = os.path.join(__home__, 'icon.png')
#ICON2 = os.path.join(__home__, 'icon2.png')
#ICON3 = os.path.join(__home__, 'icon3.png')
#ICON4 = os.path.join(__home__, 'icon4.png')
fanart = os.path.join(__home__, 'fanart.jpg')
#fanart2 = os.path.join(__home__, 'fanart2.jpg')

def CATEGORIES():
#				#addDir(name,name2,url,type2,mode,iconimage,fanimage)
        addDir('Anime List','List',mainSite + 'anime-list',0,2,artPath + 'full.png',fanart)
        addDir('Anime Movies','Movies',mainSite + 'category/anime-movies',0,3,artPath + 'movies.png',fanart)
				###
        addDir('Ongoing Anime','List',mainSite + 'ongoing-anime',0,6,artPath + 'plus.png',fanart)
        #addDir('Latest Episodes','List',mainSite + 'anime-updates',0,7,artPath + 'full.png',fanart)
        ##addDir('New Series','List',mainSite + 'new-anime',0,6,artPath + 'gogoanime\\newseries.png',fanart)
        ##addDir('Suprise Me','List',mainSite + 'surprise',0,4,artPath + 'surpriseme1.jpg',fanart)
        #addDir('Search','List',mainSite + 'new-anime',0,8,artPath + 'full.png',fanart)

def CATEGORIESlist():
#				#addDir(name,name2,url,type2,mode,iconimage,fanimage)
        addDir('Index','List',mainSite + 'anime-list',0,201,artPath + 'full.png',fanart)
        addDir('Genre','List',mainSite + 'anime-genres',0,211,artPath + 'Glossy_Black\\genres.png',fanart)
        addDir('Popular','List',mainSite + 'popular-anime',0,6,artPath + 'BLANK.png',fanart)
        addDir('New','List',mainSite + 'new-anime',0,6,artPath + 'BLANK.png',fanart)
        addDir('Recent','List',mainSite + 'recent-anime',0,6,artPath + 'BLANK.png',fanart)
        addDir('Ongoing','List',mainSite + 'ongoing-anime',0,6,artPath + 'plus.png',fanart)
        addDir('Completed','List',mainSite + 'completed-anime',0,6,artPath + 'BLANK.png',fanart)

def CATEGORIESmovies():
#				#addDir(name,name2,url,type2,mode,iconimage,fanimage)
        addDir('Index','List',mainSite + 'category/anime-movies',0,301,artPath + 'movies.png',fanart)
        addDir('Genre','List',mainSite + 'anime-movie-genres',0,311,artPath + 'Glossy_Black\\genres.png',fanart)
        addDir('Popular','List',mainSite + 'popular-movies',0,6,artPath + 'BLANK.png',fanart)
        addDir('New','List',mainSite + 'new-movies',0,6,artPath + 'BLANK.png',fanart)
        addDir('Recent','List',mainSite + 'recent-movies',0,6,artPath + 'BLANK.png',fanart)

def showlistdir(vLetterA,vLetterB,vImageC):
	addDir(vLetterB,'shows',mainSite + 'alpha-shows/' + vLetterA,0,6,artPath + 'Glossy_Black\\' + vImageC + '.png',fanart)

def CATEGORIESlistaa():
	showlistdir('others','#','123')
	showlistdir('a','a','a')
	showlistdir('b','b','b')
	showlistdir('c','c','c')
	showlistdir('d','d','d')
	showlistdir('e','e','e')
	showlistdir('f','f','f')
	showlistdir('g','g','g')
	showlistdir('h','h','h')
	showlistdir('i','i','i')
	showlistdir('j','j','j')
	showlistdir('k','k','k')
	showlistdir('l','l','l')
	showlistdir('m','m','m')
	showlistdir('n','n','n')
	showlistdir('o','o','o')
	showlistdir('p','p','p')
	showlistdir('q','q','q')
	showlistdir('r','r','r')
	showlistdir('s','s','s')
	showlistdir('t','t','t')
	showlistdir('u','u','u')
	showlistdir('v','v','v')
	showlistdir('w','w','w')
	showlistdir('x','x','x')
	showlistdir('y','y','y')
	showlistdir('z','z','z')

def movielistdir(vLetterA,vLetterB,vImageC):
	addDir(vLetterB,'movies',mainSite + 'alpha-movies/' + vLetterA,0,6,artPath + 'Glossy_Black\\' + vImageC + '.png',fanart)

def CATEGORIESmoviesaa():
	movielistdir('others','#','123')
	movielistdir('a','a','a')
	movielistdir('b','b','b')
	movielistdir('c','c','c')
	movielistdir('d','d','d')
	movielistdir('e','e','e')
	movielistdir('f','f','f')
	movielistdir('g','g','g')
	movielistdir('h','h','h')
	movielistdir('i','i','i')
	movielistdir('j','j','j')
	movielistdir('k','k','k')
	movielistdir('l','l','l')
	movielistdir('m','m','m')
	movielistdir('n','n','n')
	movielistdir('o','o','o')
	movielistdir('p','p','p')
	movielistdir('q','q','q')
	movielistdir('r','r','r')
	movielistdir('s','s','s')
	movielistdir('t','t','t')
	movielistdir('u','u','u')
	movielistdir('v','v','v')
	movielistdir('w','w','w')
	movielistdir('x','x','x')
	movielistdir('y','y','y')
	movielistdir('z','z','z')

def genrelist(url,modeA):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('<tr>\s+<td>\s+<a href="(.+?)">(.+?)</a>\s+</td>\s+<td>(.+?)</td>\s+</tr>').findall(link)
        for url2,name,shocount in match:
                addDir(name + ' - (' + shocount + ')',name,url2,0,6,artPath + '',fanart)

def showlist(url,modeA):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('<a href="(.+?)"><img src="(.+?)" width="120" height="168" alt="Watch (.+?) online"').findall(link)
        for url2,img2,name in match:
                addDir(name,name,url2,0,4,img2,fanart)
        matchb=re.compile('<li><a href="(.+?)">Next</a></li>').findall(link)
        for url3 in matchb:
                addDir('Next','list',url3,0,modeA,artPath + 'gogoanime\\next.png',fanart)

def genrelistshows(url):
	genrelist(url,211)
def genrelistmovies(url):
	genrelist(url,311)
def EPISODESlist(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        img3=''
        matcha=re.compile('<img src="(.+?)" id="series_image" width="250" height="370" alt="').findall(link)
        for img2 in matcha:
                img3=img2
        match=re.compile('<li>\s+<a href="(.+?)">(.+?)</a>\s+<span class="right_text">(.+?)</span>').findall(link)
        for url2,name,dateadded in match:
                addDir(name + ' - (' + dateadded + ')',name,url2,0,5,img3,fanart)
        #matchb=re.compile('<li><a href="(.+?)">Next</a></li>').findall(link)
        #for url3 in matchb:
        #        addDir('Next','movies',url3,0,302,artPath + 'gogoanime\\next.png',fanart)

def VIDEOsource(url,name):
				vvVIDEOLINKS(url,name)

#########################################

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
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        return ok


def addDir(name,name2,url,type2,mode,iconimage,fanimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&nm="+urllib.quote_plus(name2)+"&tp="+str(type2)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        liz.setProperty( "Fanart_Image", fanimage )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
        
              
params=get_params()
url=None
name=None
name2=None
type2=None
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
        name2=urllib.unquote_plus(params["nm"])
except:
        pass
try:
        type2=int(params["tp"])
except:
        pass
try:
        mode=int(params["mode"])
except:
        pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "Name2: "+str(name2)
print "Type2: "+str(type2)

if mode==None or url==None or len(url)<1:
        print ""
        CATEGORIES()
elif mode==2:
        print ""+url
        CATEGORIESlist()
elif mode==201:
        print ""+url
        CATEGORIESlistaa()
#elif mode==202:
#        print ""+url
#        CATEGORIESlistab(url)
elif mode==211:
        print ""+url
        genrelistshows(url)
elif mode==3:
        print ""+url
        CATEGORIESmovies()
elif mode==301:
        print ""+url
        CATEGORIESmoviesaa()
#elif mode==302:
#        print ""+url
#        CATEGORIESmoviesab(url)
elif mode==311:
        print ""+url
        genrelistmovies(url)
elif mode==4:
        print ""+url
        EPISODESlist(url)
elif mode==5:
        print ""+url
        VIDEOsource(url,name)
elif mode==6:
        print ""+url
        showlist(url,mode)
#elif mode==16:
#        print ""+url
#        VIDEOLINKStrailers(url,name,name2,type2)




xbmcplugin.endOfDirectory(int(sys.argv[1]))
