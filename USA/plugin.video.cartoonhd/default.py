import urllib,urllib2,sys,re,xbmcplugin,xbmcgui,xbmcaddon,xbmc,os

import json


ADDON = xbmcaddon.Addon(id='plugin.video.cartoonhd')

cartoon=os.path.join(ADDON.getAddonInfo('path'),'cartoon')



def CATEGORIES():
            
    xunity='http://gappcenter.com/app/cartoon/mapi.php?action=getcategory&os=newiosfull&version=2.1&deviceid=&token=&time=&device=iphone'
    response=OPEN_URL(xunity)
    
    link=json.loads(response)

    data=link['Data']

    for field in data:
        name= field['Name'].encode("utf-8")
        iconimage= field['Image'].encode("utf-8")
        action=field['Action'].encode("utf-8")
        if ('Top')in name or ('Disney Collection') in name:
            name='[COLOR cyan].%s[/COLOR]' % name
            
        if  ADDON.getSetting('parental')=='true':
            if not '14+' in name:    
                addDir(name,action,1,iconimage,'')
        else:
            addDir(name,action,1,iconimage,'')
        xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_TITLE)            
    setView('movies', 'default') 
       
       
                                                                      
def GetContent(url):
                #http://gappcenter.com/app/cartoon/mapi.php?action=getlistcontent&cate=%s&pageindex=0&pagesize=1000&os=newiosfull&version=2.1&deviceid=15146BE541BAB0D4628A14FBE7A25516&token=&time=&device=iphone
        new_url='http://gappcenter.com/app/cartoon/mapi.php?action=getlistcontent&cate=%s&pageindex=0&pagesize=1000&os=newiosfull&version=2.1&deviceid=&token=&time=&device=iphone'%url
        response=OPEN_URL(new_url)
        link=json.loads(response)

        data=link['Data']
        for field in data:
            name= field['Name'].encode("utf-8")
            iconimage= field['Image'].encode("utf-8")
            url=field['Link'].encode("utf-8")
            addDir(name,url,200,iconimage,'')
        setView('movies', 'movies') 

        if ADDON.getSetting('sort')=='true':
            xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_TITLE) 
    
               
 
def OPEN_URL(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    return link
    
    
    
def PLAY_STREAM(name,url,iconimage):
    if 'auengine.com' in url:
        html=OPEN_URL(url)
        url=re.compile("url: '(.+?)'").findall(html)[0]
        
    if 'animeonhand.com' in url:
        html=OPEN_URL(url)
        url=re.compile("'file': '(.+?)'").findall(html)[0]
        
        
    liz = xbmcgui.ListItem(name, iconImage='DefaultVideo.png', thumbnailImage=iconimage)
    liz.setInfo(type='Video', infoLabels={'Title':name})
    liz.setProperty("IsPlayable","true")
    liz.setPath(url)
    xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)



def playall(name,url):
    dp = xbmcgui.DialogProgress()
    dp.create("Cartoon HD",'Creating Your Playlist')
    dp.update(0)
    pl = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
    pl.clear()

    new_url='http://xty.me/xunitytalk/addons/plugin.video.cartoonhd/cats/%s' % url
    response=OPEN_URL(new_url)
    link=json.loads(response)
    data=link['Data']
    playlist = []
    match=re.compile('"Link":"(.+?)"').findall(response)
    nItem    = len(match)
    try:

        
        for field in data:
            name= field['Name'].encode("utf-8")
            iconimage= field['Image'].encode("utf-8")
            URL=field['Link'].encode("utf-8")
        

            liz = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
            liz.setInfo( type="Video", infoLabels={ "Title": name} )
            liz.setProperty("IsPlayable","true")

            playlist.insert(0,(URL ,liz))
    
            progress = len(playlist) / float(nItem) * 100  
            dp.update(int(progress), 'Adding to Your Playlist',name)

            if dp.iscanceled():
                return

        dp.close()
    
    
                
        for blob ,liz in playlist:
            try:
                if blob:
                    pl.add(blob,liz)
            except:
                pass

        if not xbmc.Player().isPlayingVideo():
	    xbmc.Player(xbmc.PLAYER_CORE_MPLAYER).play(pl)
    except:
        raise
        dialog = xbmcgui.Dialog()
        dialog.ok("Disney Junior", "Sorry Get All Valid Urls", "Why Not Try A Singular Video")     
    
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

def addDir(name,url,mode,iconimage,description):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&description="+urllib.quote_plus(description)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description} )
        menu = []
        if mode ==200:
            liz.setProperty("IsPlayable","true")
            
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        else:
            menu.append(('Play All Videos','XBMC.RunPlugin(%s?name=%s&mode=2001&iconimage=None&url=%s)'% (sys.argv[0],name,url)))
            liz.addContextMenuItems(items=menu, replaceItems=False)
            xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
        
        
 
        
def setView(content, viewType):
        if content:
                xbmcplugin.setContent(int(sys.argv[1]), content)
        if ADDON.getSetting('auto-view') == 'true':#<<<----see here if auto-view is enabled(true) 
                xbmc.executebuiltin("Container.SetViewMode(%s)" % ADDON.getSetting(viewType) )#<<<-----then get the view type
                      
               
params=get_params()
url=None
name=None
mode=None
iconimage=None
description=None


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
        description=urllib.unquote_plus(params["description"])
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
        GetContent(url)
        
elif mode==200:

        PLAY_STREAM(name,url,iconimage)

elif mode==2001:

        playall(name,url)        
       
xbmcplugin.endOfDirectory(int(sys.argv[1]))
