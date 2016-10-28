import urllib,urllib2,sys,re,xbmcplugin
import xbmcgui,xbmcaddon,xbmc,base64
import time,datetime,os,urlresolver
import cookielib,unicodedata,HTMLParser

local = xbmcaddon.Addon(id='plugin.video.movie105')#
sys.path.append( "%s/resources/"%local.getAddonInfo('path') )
from metahandler import metahandlers
from BeautifulSoup import BeautifulSoup
from sqlite3 import dbapi2 as database
from t0mm0.common.net import Net
from t0mm0.common.addon import Addon

addon = Addon('plugin.video.movie105', sys.argv)#
datapath = addon.get_profile()
grab = metahandlers.MetaData()
linkback = None
net = Net()
cookie_path = os.path.join(datapath, 'cookies')                 
cookie_jar = os.path.join(cookie_path, "cookiejar.lwp")
if os.path.exists(cookie_path) == False:                        
    os.makedirs(cookie_path)
    
BASE_URL = 'http://movie105.com/'#

def MAIN():
    addDir(100,'Latest',BASE_URL,None,'','','Latest','')
    addDir(150,'',BASE_URL,None,'','','By Language','')
    addDir(900,'Tv series',BASE_URL,None,'','','TV Series','')
    addDir(950,'',BASE_URL,None,'','','Movies By Genres','')
    addDir(1700,'Search',BASE_URL,None,'','','Search','')
    addSpecial('[COLOR yellow]Resolver Settings[/COLOR]','www.nonsense.com','60','')
    addSpecial('[COLOR blue]Having problems, Need help, Click here[/COLOR]','www.nonsense.com','50','')
        
def BY_LANGUAGE(url):    
    addDir(200,'Hindi Dubbed',BASE_URL,None,'','','Hindi Dubbed','')
    addDir(300,'Hollywood',BASE_URL,None,'','','Hollywood','')
    addDir(400,'Bollywood',BASE_URL,None,'','','Bollywood','')
    addDir(500,'Foreign',BASE_URL,None,'','','Foreign','')
    addDir(600,'Telugu',BASE_URL,None,'','','Telugu','')
    addDir(700,'Malayalam',BASE_URL,None,'','','Malayalam','')
    addDir(800,'Tamil',BASE_URL,None,'','','Tamil','')
    
def MOVIES_GENRES(url):    
    addDir(1000,'Action',BASE_URL,None,'','','Action','')
    addDir(1100,'Comedy',BASE_URL,None,'','','Comedy','')
    addDir(1200,'Drama',BASE_URL,None,'','','Drama','')
    addDir(1300,'Thriller',BASE_URL,None,'','','Thriller','')
    addDir(1400,'Adventure',BASE_URL,None,'','','Adventure','')
    addDir(1500,'Horror',BASE_URL,None,'','','Horror','')
    addDir(1600,'Romance',BASE_URL,None,'','','Romance','')

def INDEX(url):
    html = GET_HTML(url,'')
    if 'Latest' in mode2:
        r = re.findall(r'<h2 class="ti(tle">.+?)<div class="readmorecontent">',html,re.DOTALL|re.M)
        r = re.findall(r'tle"><a href="(.+?)" rel=.+?">(.+?)</a></h2>.+?src="(.+?)" width',str(r),re.I|re.DOTALL|re.M)
        for url, name, img in r:
            name = name.replace('-',' ').replace('\u2019',"'").replace('\u2013','-')
            addDir(2000,'',url,None,'','',name,img)
    if 'Hindi Dubbed' or 'Horror' or 'Romance' or 'Adventure' or 'Hollywood' or 'thriller' or 'Bollywood' or 'Foreign' or 'Telugu' or 'Malayalam' or 'Tamil' or 'Tv series' or 'BASE_URL' or 'Comedy' or 'Drama' in mode2:
        r = re.findall(r'<h2 class="title" id=(.+?)<div class="entry">',html,re.DOTALL|re.M)
        r = re.findall(r'post-.+?"><a href="(.+?)".+?title=".+?">(.+?)</a></h2>',str(r),re.M|re.DOTALL)
        for url, name in r:
            name = name.replace('-',' ').replace('\u2019',"'").replace('\u2013','-')
            addDir(2000,'',url,None,'','',name,'')
    if 'Search' in mode2:
        html = GET_HTML(url,'')
        r = re.findall(r'<h2 class="title"><a href="(.+?)" rel="bookmark" title=".+?">(.+?)</a></h2>',html,re.M|re.DOTALL)
        for url, name in r:
            name = name.replace('-',' ').replace('\u2019',"'").replace('\u2013','-')
            addDir(2000,'',url,None,'','',name,'')
    
    if '<div class=\'wp-pagenavi\'>' in html:
        r = re.findall(r'class=\'pages\'>Page (.+?) of (.+?)</span>.+?\'current\'>.+?</span><a href=\'(.+?)\' class=',html)
        for current_page, last_page, next_page_url in r:
            name = '[B][COLOR green]Page '+current_page+' Of '+last_page+': Next Page >>>[/B][/COLOR]'
            addDir(100,mode2,next_page_url,None,'','',name,'')
    
def SEARCH(url):
    print url
    last_search = addon.load_data('search')
    if not last_search: last_search = ''
    search_entered = ''
    keyboard = xbmc.Keyboard(search_entered, 'Search Movie105')
    last_search = last_search.replace('+',' ')
    keyboard.setDefault(last_search)
    keyboard.doModal()
    if keyboard.isConfirmed():
        search_entered = keyboard.getText()#.replace(' ','+')# sometimes you need to replace spaces with + or %20#
        addon.save_data('search',search_entered)
    if search_entered == None or len(search_entered)<1:
        MENU()
    else:
        url = 'http://movie105.com/?s="%s"'%(search_entered).replace(' ','+')
        mode2 = 'Search'
        INDEX(url)
        
def FIND_VIDEO_STREAMS(url):
    print url
    name2 = name
    html = GET_HTML(url,'')
    if '<strong>IMDb Ratings & Details:' in html:
        r = re.findall(r'<strong>IMDb Ratings & Details:.+?data-title="(.+?)" data-style=',html)
        imdb_no = r[0]
        print 'IMDB: '+imdb_no
    sources = []
    try:
        if '<strong>Watch Full Movie on' in html:
            r = re.findall(r'<p><strong>Movie Plot: </strong>(.+?)<script type="text/javascript" src=',html,re.M|re.DOTALL)
            r = re.findall(r'<a href="(.+?)" target="_blank">Click Here To Watch Full Movie (.+?)</a>',str(r))
            print r
            for url, part in r:
                domain = re.findall(r'//(.+?)/',url)
                hoster = domain[0]+': '+part.replace('\\xc2\\xa0',' ')
                print hoster
                source = urlresolver.HostedMediaFile(url=url, title=hoster)
                sources.append(source)
    except:
        pass
    try:
        r = re.findall(r'Watch Full.+?</strong>.+?<p><a href="(.+?)" target=',html,re.M|re.DOTALL)
        print r
        for url in r:
            hoster = re.findall(r'//(.+?)/',url)
            source = urlresolver.HostedMediaFile(url=url, title=hoster[0])
            sources.append(source)
    except:
        pass
    
    urlresolver.filter_source_list(sources)
    source = urlresolver.choose_source(sources)
    try:
        if source: stream_url = source.resolve()
        else: stream_url = ''
        liz=xbmcgui.ListItem(name, iconImage='',thumbnailImage='')
        liz.setInfo('Video', {'Title': name2} )
        liz.setProperty("IsPlayable","true")
        xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=stream_url,isFolder=False,listitem=liz)
        xbmc.Player().play(stream_url)
    except:
        pass

def GET_HTML(url,linkback):
    try:
        linkback = None
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-GB; rv:12.2) Gecko/20120605 Firefox/12.2 PaleMoon/12.2')
        req.add_header('Connection','keep-alive')
        if linkback != None:
            req.add_header('Referer', linkback)
        response = urllib2.urlopen(req)
        body = response.read()
        body = unicode(body,'iso-8859-1')
        h = HTMLParser.HTMLParser()
        body = h.unescape(body)
        return body
    except Exception, e:
        print "Failed to retrieve page: %s" %url
        print 'Urllib2 error: '+str(e)
        xbmc.executebuiltin('Notification([COLOR red]Network Error[/COLOR],Network Error: '+str(e)+',5000,)')
        return MAIN()

def HELP():
    help = SHOWHELP()
    help.doModal()
    del help

class SHOWHELP(xbmcgui.Window):
    def __init__(self):
        self.addControl(xbmcgui.ControlImage(0,0,1280,720,"%s/resources/art/Help.png"%local.getAddonInfo("path")))
    def onAction(self, action):
        if action == 92 or action == 10:
            xbmc.Player().stop()
            self.close()

def addDir(mode,mode2,url,types,linkback,meta_name,name,iconimage):
    if local.getSetting("enable_meta") == "true": infoLabels = GRABMETA(name,types)
    else: infoLabels = {'cover_url': '','title': name }
    if types == None: img = iconimage
    else: img = infoLabels['cover_url']
    u=sys.argv[0]+"?mode="+str(mode)+"&mode2="+str(mode2)+"&url="+str(url)+"&types="+str(types)+"&linkback="+str(linkback)+"&meta_name="+str(meta_name)+"&name="+str(name)+"&iconimage="+str(iconimage)
    ok=True
    liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=img)
    liz.setInfo( type="Video", infoLabels= infoLabels)#
    try:
        if types != None:
            liz.setProperty('fanart_image', infoLabels['backdrop_url'])#
    except:
        pass
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
    return ok

def addSpecial(name,url,mode,image):
    liz=xbmcgui.ListItem(label = '[B]%s[/B]'%name,iconImage="",thumbnailImage = image)
    xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=sys.argv[0]+"?url=%s&mode=%s&name=%s"%(url,mode,name),isFolder=False,listitem=liz)

def setView(content, viewType):
    if content:
        xbmcplugin.setContent(int(sys.argv[1]), content)
    if addon.get_setting('auto-view') == 'true':
        xbmc.executebuiltin("Container.SetViewMode(%s)" % addon.get_setting(viewType) )

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

params=get_params()
mode=None
mode2=None
url=None
types=None
linkback=None
meta_name=None
name=None
try:
        iconimage=urllib.unquote_plus(params["iconimage"])
except:
        pass
try:
        meta_name=urllib.unquote_plus(params["meta_name"])
except:
        pass

try:
        linkback=urllib.unquote_plus(params["linkback"])
except:
        pass
try:
        types=urllib.unquote_plus(params["types"])
except:
        pass
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
try:
        mode2=urllib.unquote_plus(params["mode2"])
except:
        pass
print '----------------------------------------------------'
print 'Mode: '+str(mode)
print 'Mode2: '+str(mode2)
print 'URL: '+str(url)
print 'TYPEs: '+str(types)
print 'Linkback: '+str(linkback)
print 'Meta_Name: '+str(meta_name)
print 'Name: '+str(name)
print '----------------------------------------------------'
if mode==None or url==None or len(url)<1:
    MAIN()
elif mode == 50:
    HELP()
elif mode == 60:
    urlresolver.display_settings()
elif mode == 100:
    INDEX(url)
elif mode == 150:
    BY_LANGUAGE(url)
elif mode == 200:
    url = 'http://movie105.com/category/hindi-dubbed'
    INDEX(url)
elif mode == 300:
    url = 'http://movie105.com/category/hollywood'
    INDEX(url)
elif mode == 400:
    url = 'http://movie105.com/category/bollywood'
    INDEX(url)
elif mode == 500:
    url = 'http://movie105.com/category/foreign-movies'
    INDEX(url)
elif mode == 600:
    url = 'http://movie105.com/category/telugu-movies'
    INDEX(url)
elif mode == 700:
    url = 'http://movie105.com/category/malayalam'
    INDEX(url)
elif mode == 800:
    url = 'http://movie105.com/category/tamil-movies'
    INDEX(url)
elif mode == 900:
    url = 'http://movie105.com/category/tv-series'
    INDEX(url)
elif mode == 950:
    MOVIES_GENRES(url)
elif mode == 1000:
    url = 'http://movie105.com/tag/action'
    INDEX(url)
elif mode == 1100:
    url = 'http://movie105.com/tag/comedy'
    INDEX(url)
elif mode == 1200:
    url = 'http://movie105.com/tag/drama'
    INDEX(url)
elif mode == 1300:
    url = 'http://movie105.com/tag/thriller'
    INDEX(url)
elif mode == 1400:
    url = 'http://movie105.com/tag/adventure'
    INDEX(url)
elif mode == 1500:
    url = 'http://movie105.com/tag/horror'
    INDEX(url)
elif mode == 1600:
    url = 'http://movie105.com/tag/romance'
    INDEX(url)
elif mode == 1700:
    SEARCH(url)
elif mode == 2000:
    FIND_VIDEO_STREAMS(url)

addon.end_of_directory()
