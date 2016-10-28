import urllib,urllib2,sys,re,xbmcplugin,xbmcgui,xbmcaddon,xbmc,os
import datetime
import time


PLUGIN='plugin.video.expattv'

ADDON = xbmcaddon.Addon(id=PLUGIN)

swf='swfUrl=http://www.filmon.com/tv/modules/FilmOnTV/files/flashapp/filmon/FilmonPlayer.swf?v=4'
iconimage='http://static.filmon.com/couch/channels/%s/extra_big_logo.png'
from hashlib import md5
api ='http://www.filmon.com/api/'

if ADDON.getSetting('user')=='':
        dialog = xbmcgui.Dialog()
        xbmcgui.Dialog().ok('ExPat','Now ExPat Needs Your FilmOn User Details To Work','The Next Screen Will Get You To Input These','If You Havent Got A Filmon Account Sign Up')
if ADDON.getSetting('user')=='':
        search_entered = ''
        keyboard = xbmc.Keyboard(search_entered, 'Please Enter Email Address')
        keyboard.doModal()
        if keyboard.isConfirmed():
            search_entered = keyboard.getText() 
        ADDON.setSetting('user',search_entered)
        
if ADDON.getSetting('pass')=='':
        search_entered = ''
        keyboard = xbmc.Keyboard(search_entered, 'Please Enter Password')
        keyboard.doModal()
        if keyboard.isConfirmed():
            search_entered = keyboard.getText()
        ADDON.setSetting('pass',search_entered)

user=ADDON.getSetting('user')
passs=ADDON.getSetting('pass')
password = md5(passs).hexdigest()


ooOOOoo = ''
def ttTTtt(i, t1, t2=[]):
 t = ooOOOoo
 for c in t1:
  t += chr(c)
  i += 1
  if i > 1:
   t = t[:-1]
   i = 0  
 for c in t2:
  t += chr(c)
  i += 1
  if i > 1:
   t = t[:-1]
   i = 0
 return t            
    
    
    

def CATEGORIES():
    a=OPEN_URL('http://xty.me/xunitytalk/maintenance_do_not_touch/expat.txt')
    match=re.compile('name="(.+?)".+?iconimage="(.+?)".+?id="(.+?)".+?rtmp="(.+?)".+?app="(.+?)".+?playpath="(.+?)"',re.DOTALL).findall(a)
    for name ,iconimage,id,rtmp,app,playpath in match:
        addDir(name,id,1,iconimage,rtmp,app,playpath)
        setView('movies', 'default') 
       #setView is setting the automatic view.....first is what section "movies"......second is what you called it in the settings xml  
       
       
                                                                      
 
    
def GET_STREAM(name,url,iconimage,rtmp,app,playpath):
    auth=getid(url)
    if 'mp4:' in playpath:
        stream='%s%s?%s playpath=%s?%s app=%s swfUrl=https://www.filmon.com/tv/modules/FilmOnTV/files/flashapp/filmon/FilmonPlayer.swf?v=51 pageurl=http://www.filmon.com/ tcUrl=%s  live=1 timeout=25 swfVfy=1'%(rtmp,playpath,auth,playpath,auth,app,rtmp)
    else:
        stream='%s?id=%s/%s playpath=%s app=%s%s swfUrl=https://www.filmon.com/tv/modules/FilmOnTV/files/flashapp/filmon/FilmonPlayer.swf?v=51 pageurl=http://www.filmon.com/ tcUrl=%s live=1 timeout=25 swfVfy=1'%(rtmp,auth,playpath,playpath,app,auth,rtmp)
    if ADDON.getSetting('res')=='true':
        stream=str(stream).replace('low.stream','high.stream')
    liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name} )
    liz.setProperty("IsPlayable","true")
    liz.setPath(stream)
    xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
      
   
   
     
def OPEN_URL(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    return link
    
ooOOOoo = ''
def ttTTtt(i, t1, t2=[]):
 t = ooOOOoo
 for c in t1:
  t += chr(c)
  i += 1
  if i > 1:
   t = t[:-1]
   i = 0  
 for c in t2:
  t += chr(c)
  i += 1
  if i > 1:
   t = t[:-1]
   i = 0
 return t            
    
    
def GET_STREAM_RESOLUTION(channels):
    import json
    for item in channels:
        if 'low' in item['name']:
            return item['url'].split('?')[1].replace('id=','')
            
    return None  
 
 
def getid(id):
    url= ttTTtt(997,[54,104,197,116],[108,116,253,112,176,58,76,47,156,47,94,119,212,119,97,119,208,46,5,102,134,105,171,108,89,109,149,111,104,110,176,46,20,99,194,111,227,109,83,47,237,116,109,118,2,47,118,97,94,112,218,105,136,47,244,105,133,110,184,105,53,116,235,63,188,97,18,112,218,112,167,95,133,105,206,100,141,61,244,120,54,109,166,98,185,99,34,95,55,97,47,112,66,112,3,38,13,97,223,112,36,112,177,95,130,115,206,101,162,99,63,114,197,101,239,116,244,61,28,49,140,98,32,56,86,69,223,101,90,110,129,51,196,101])
    link=OPEN_URL(url)
    match= re.compile('"session_key":"(.+?)"').findall (link)
    sess=match[0]
    log=api+'login?session_key=%s&login=%s&password=%s' % (sess,user,password)
    OPEN_URL(log)
    import json
    try:
        url='http://www.filmon.com/api/channel/%s?session_key=%s' % (id,sess)
        link=OPEN_URL(url)
        data = json.loads(link)
        channels= data['streams']

        match = GET_STREAM_RESOLUTION(channels)        
        print '######## WORKING NORMALLY ########'      
        return match
    except:
        try:    
            url='http://www.filmon.com/api/channel/1676?session_key=%s' % (sess)
            link=OPEN_URL(url)
            data = json.loads(link)
            channels= data['streams']
    
            match = GET_STREAM_RESOLUTION(channels)        
            print '######## WORKING WITH 1676 ########'   
            return match
        except:
            try:
                url='http://www.filmon.com/api/channel/689?session_key=%s' % (sess)
                link=OPEN_URL(url)
                data = json.loads(link)
                channels= data['streams']
     
                match = GET_STREAM_RESOLUTION(channels)        
                print '######## WORKING WITH 689 ########'   
                return match
            except:
                url='http://www.filmon.com/api/channel/27?session_key=%s' % (sess)
                link=OPEN_URL(url)
                data = json.loads(link)
                channels= data['streams']
    
                match = GET_STREAM_RESOLUTION(channels)        
                print '######## WORKING WITH 27 ########'   
                return match
             
    
    
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

# this is the listing of the items        
def addDir(name,url,mode,iconimage,rtmp,app,playpath):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&rtmp="+urllib.quote_plus(rtmp)+"&app="+urllib.quote_plus(app)+"&playpath="+urllib.quote_plus(playpath)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name} )
        liz.setProperty("IsPlayable","true")
        if ADDON.getSetting('sort_method') == 'true':
            xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_LABEL)        
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        return ok
        
 
        
#below tells plugin about the views                
def setView(content, viewType):
        # set content type so library shows more views and info
        if content:
                xbmcplugin.setContent(int(sys.argv[1]), content)
        if ADDON.getSetting('auto-view') == 'true':#<<<----see here if auto-view is enabled(true) 
                xbmc.executebuiltin("Container.SetViewMode(%s)" % ADDON.getSetting(viewType) )#<<<-----then get the view type
                      
               
params=get_params()
url=None
name=None
mode=None
iconimage=None
rtmp=None
app=None
playpath=None


try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        iconimage=urllib.unquote_plus(params["iconimage"])
except:
        pass
try:        
        mode=int(params["mode"])
except:
        pass
try:        
        rtmp=urllib.unquote_plus(params["rtmp"])
except:
        pass
try:        
        app=urllib.unquote_plus(params["app"])
except:
        pass
try:        
        playpath=urllib.unquote_plus(params["playpath"])
except:
        pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "IconImage: "+str(iconimage)
   
        
#these are the modes which tells the plugin where to go
if mode==None or url==None or len(url)<1:
        print ""
        CATEGORIES()
       
elif mode==1:
        print ""+url
        GET_STREAM(name,url,iconimage,rtmp,app,playpath)
        

       
xbmcplugin.endOfDirectory(int(sys.argv[1]))
