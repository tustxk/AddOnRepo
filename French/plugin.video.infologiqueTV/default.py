import httplib,urllib,urllib2,re,xbmcplugin,xbmcgui,pyamf,json

pluginhandle = int(sys.argv[1])
#base = "http://infologique.net/tv/"

# AMF wrapper for brightcove-call
# Dany Côté
# infologiqueTV 2013
import httplib,urllib,urllib2,pyamf
from pyamf import remoting, amf3, util

def get_episode_info_brightcove(key, content_id, url, exp_id, typevideo):
    print 'key:'+key
    print 'content_id:'+content_id
    #print 'URL:'+url
    print 'exp_id:'+exp_id
    #content_id = '2011056914001';
    conn = httplib.HTTPConnection("c.brightcove.com")
    envelope = build_amf_request(key, content_id, url, exp_id, typevideo)
    #print envelope
    conn.request("POST", "/services/messagebroker/amf?playerKey="+key, str(remoting.encode(envelope).read()),{'content-type': 'application/x-amf'})
    response = conn.getresponse().read()
    print "REPONSE : "
    #print response
    response = remoting.decode(response).bodies[0][1].body
    print response
    return response

class ViewerExperienceRequest(object):
   def __init__(self, URL, contentOverrides, experienceId, playerKey, TTLToken=''):
      self.TTLToken = TTLToken
      self.URL = URL
      self.deliveryType = float(0)
      self.contentOverrides = contentOverrides
      self.experienceId = experienceId
      self.playerKey = playerKey

class ContentOverride(object):
   def __init__(self, contentId, contentRefId, contentType=0, target='videoPlayer'):
      self.contentType = contentType
      self.contentId = contentId
      self.target = target
      self.contentIds = None
      self.contentRefId = contentRefId
      self.contentRefIds = None
      self.contentType = 0
      self.featureId = float(0)
      self.featuredRefId = None

def build_amf_request(key, content_id, url, exp_id, typevideo):
   print 'ContentId:'+content_id
   print 'ExperienceId:'+exp_id
   print 'URL:'
   #const = '5e953dada6862ed388075b269a11253eb52a15c4'
   #const = 'faf1b90dbe278e370da5a43bde59b6efcf841d9d'
   const = 'a5d0718fd177504aa67a9997e41106faa73edad3'
   pyamf.register_class(ViewerExperienceRequest, 'com.brightcove.experience.ViewerExperienceRequest')
   pyamf.register_class(ContentOverride, 'com.brightcove.experience.ContentOverride')
   print typevideo
   if ( "ref" in content_id):
        print "REMOVE REF-" + content_id[4:]
        content_override = ContentOverride(None,content_id[4:])
   else:
        try:
            content_override = ContentOverride(int(content_id),None)
        except ValueError:
            content_override = ContentOverride(None,content_id)
        
   viewer_exp_req = ViewerExperienceRequest(url, [content_override], int(exp_id), key)

   env = remoting.Envelope(amfVersion=3)
   env.bodies.append(
      (
         "/1",
         remoting.Request(
            target="com.brightcove.experience.ExperienceRuntimeFacade.getDataForExperience",
            body=[const, viewer_exp_req],
            envelope=env
         )
      )
   )
   print "PRESQUE FINI"
   print env
   return env

def get_html_source_nopost( url, get ):
    print "get_html_source_nopost : "+url+" get " + get
    data = urllib.urlencode({'u': 'anisite','p': '23634634745u54uy5y34u'})
    h = httplib.HTTPConnection('tv.infologique.net')
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
    h.request('POST', '/' + url + '/' + get, data, headers)
    r = h.getresponse()
    return r.read()

def MENU(get=""):
        content = get_html_source_nopost( 'GetMenu',  get )
        data = json.loads( content.encode("utf-8") )
        #name,url,mode,iconimage
        for lien in data:
            #print 'get: ' + lien['get']
            addDir((lien['name']+"").encode("utf-8"),
                    lien['url'],
                    lien['get'],
                    lien['typevideo'],
                    lien['iconimage'])

def LISTER_EMISSIONS(url , get):
        #url = url.split('?')
        content = get_html_source_nopost( url, get )
        data = json.loads( content )
        for episode in data:
            addDirPlay(""+episode['showName'].encode("utf-8") + "  -  " + episode['title'].encode("utf-8"),episode['id'], 3,episode['img_url'], episode) #thumbnail

def LISTER_EPISODES(url):
        print 'url: ' + url

def VIDEOLINKS(url,name,typevideo):
        content = get_html_source_nopost( 'GetShow', '/c/' + url + '/' )
        data = json.loads( content )
        print url
        print name
        print typevideo
        return play(data[0]['video_url'],name,data[0]['player_id'],data[0]['realvideo_id'],typevideo)

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
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        return ok

def addDir(name,url,get,typevideo,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&get="+str(get)+"&typevideo="+str(typevideo)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
        
def addDirPlay(name,url,mode,iconimage,data):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&typevideo="+str(typevideo)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels=data )
        #liz.setInfo('playcount','3')
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        return ok

def play(url,name,exp_id,content_id,typevideo):
    swfUrl = 'http://admin.brightcove.com/viewer/us20121128.1314/federatedVideoUI/BrightcovePlayer.swf'
    #target = url.split('target=')
    #url = 'http://www.ztele.com/webtele?target=' + target[1]
    #data = common.getURL(url)
    #data = 'aetn.biography.player.embedPlayer("1381361288001", "755732278001", "", "video-player-embed", "768", "479", true);'
    #exp_id,content_id = re.compile('embedPlayer\("(.+?)", "(.+?)",').findall(data)[0]
    #key = exp_id
    key =  {792857246001:"AQ~~,AAAAnreg3nE~,0dniHYWZ9tnmA03-H_0VYIA4QBv7O1HW",
            791146473001:"AQ~~,AAAAlw1g-ik~,-VUBorjek1EjQuz1HySKKyLA-1Ma9Ar0", 
            792851008001:exp_id,
            1381361288001:exp_id,
            1926989787001:exp_id,
            3450496672001:"AQ~~,AAACoOybPqE~,U0YPm6r--gbUl45Ufpw-oNkR4j8yPVna",
            2498508610001:exp_id}
    #key =  "AQ~~,AAAAnreg3nE~,0dniHYWZ9tnmA03-H_0VYIA4QBv7O1HW" #//canald
    #key =  "AQ~~,AAAAlw1g-ik~,-VUBorjek1EjQuz1HySKKyLA-1Ma9Ar0" #//canalvie
    #print exp_id
    #key = key[int(exp_id)]
    key= str(exp_id)
    #print "ahahahhaha" + key
    #renditions = get_episode_info('6816856070011', '755732278001', 'http://www.ztele.com/webtele?target=1.20616', '6816856070011')['programmedContent']['videoPlayer']['mediaDTO']['renditions']
    #print key;
    print content_id;
    #print url;
    #print exp_id;
    #print typevideo;
    #renditions = get_episode_info_brightcove(key, content_id, url, exp_id, typevideo)['programmedContent']['videoPlayer']['mediaDTO']['renditions']
    #renditions = get_episode_info_brightcove(key, content_id, url, exp_id, typevideo)['programmedContent']['videoPlayer']['mediaDTO']['IOSRenditions']
    renditions = get_episode_info_brightcove(key, content_id, url, exp_id, typevideo)['programmedContent']['videoPlayer']['mediaDTO']
    rtmp = ''
    hi_res = 0
    mode = 0
    
    print "IOS"
    
    print len(renditions['IOSRenditions'])
    
    if len(renditions['IOSRenditions']) > 0:
        renditions = renditions['IOSRenditions']
        mode=1
    else:
        renditions = renditions['renditions']
        mode=2
    
    selected_video = None
    for video in renditions:
        if(int(video['encodingRate'])>hi_res):
            selected_video = video
            hi_res = int(video['encodingRate'])
       
    if mode == 2:
        rtmpdata = selected_video['defaultURL'].split('&mp4:')
        #rtmpdata = selected_video['defaultURL']
        #rtmp = rtmpdata[0]+' playpath=mp4:'+rtmpdata[1]
        #rtmp += ' pageUrl='+url
        #print "finalurl:" + rtmp
        path2 = rtmpdata[1].split('?')
        rtmp = rtmpdata[0]+ '?' + path2[1] + ' playpath=mp4:'+rtmpdata[1] + " swfurl=" + swfUrl + " swfvfy=true"
    else:
        rtmp = selected_video['defaultURL']
    #rtmp = selected_video['defaultURL'] + ' playpath=mp4:'+rtmpdata[1] + " swfurl=" + swfUrl + " swfvfy=true"
    #print 'splittedd :  ' + path2[1]
    #rtmp://cp150446.edgefcs.net/ondemand/ playpath=mp4:681685607001/681685607001_755933543001_webvid8994-129534-z0298440gs-high.mp4?__nn__=1497926354001&slist=681685607001/&auth=daEardLccdGcRa_aZdVaJdYbsb0c2amaSa7-bqTQwa-bWG-roECtsty_yDxn_HCAB_EuC&aifp=bcosuds pageUrl=http://www.ztele.com/webtele?target=1.20616]
    #item = xbmcgui.ListItem(path=rtmp)
    #return xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)
    #displayName
    #videoStillURL
    #item = xbmcgui.ListItem(label=name,iconImage="DefaultVideo.png",thumbnailImage=thumb)
    item = xbmcgui.ListItem(label=name,iconImage="DefaultVideo.png")
    item.setInfo( type="Video", infoLabels={ "Title": name, "Plot": '' } )
    xbmc.Player(xbmc.PLAYER_CORE_DVDPLAYER).play(rtmp, item)
    


   

params=get_params()
url=None
name=None
typevideo=None
mode=None
get=""

try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        get=urllib.unquote_plus(params["get"])
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
        typevideo=int(params["typevideo"])
except:
        pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "get: "+str(get)
print "typevideo: "+str(typevideo)

if url=="GetMenu" or url==None or len(url)<1:
        print "== GET MENU START =="
        MENU(get)
       
elif mode==1 or url=="GetShows":
        print "mode 1 : "+url
        LISTER_EMISSIONS(url, get)
        
elif mode==2:
        print "mode 2: "+url
        LISTER_EPISODES(url)
        
elif mode==3:
        print "mode 3 : url "+url
        VIDEOLINKS(url,name,typevideo)


xbmcplugin.endOfDirectory(int(sys.argv[1]))