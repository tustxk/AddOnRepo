import xbmc, xbmcgui, xbmcplugin, urllib2, urllib, re, string, sys, os, traceback, xbmcaddon, urlparse, xml.etree.ElementTree as ET
from BeautifulSoup import BeautifulSoup
handle = int(sys.argv[1])
__plugin__ =  'TSN'
__author__ = 'teefer22'
__url__ = 'http://code.google.com/p/teefer-xbmc-repo/'
__date__ = '03-19-2013'
__version__ = '0.1.5'
__settings__ = xbmcaddon.Addon(id='plugin.video.tsn')


def open_url(url):
        req = urllib2.Request(url)
        req.add_header("Referer", "%s://%s/" % ('http', 'cls.ctvdigital.net'))
        content = urllib2.urlopen(req)
        data = content.read()
        content.close()
        return data

def build_main_directory():
        tsnurl = 'http://www.tsn.ca/config/videoHubMenu.xml'
        data = open_url(tsnurl)
        root = ET.fromstring(data)

        #the next 2 lines create a link for the featured section
        name = root.find("./item/text").text
        listitem = xbmcgui.ListItem(label = name)
        url = root.find("./item/urlLatest").text
        u = sys.argv[0] + "?mode=1&name=" + urllib.quote_plus(name) + "&url=" + urllib.quote_plus(url)
        ok = xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = u, listitem = listitem, isFolder = True)

        #the below nested loops, builds a menu of all the menu items in videoHubMenu.xml (no video links, just menu links)
        for menuitem in root.findall('item'):
                for rootmenu in menuitem.findall('text'):
                        ignorethisvariable = 1
                for submenu in menuitem.findall('item'):
                        for subsubmenu in submenu.findall('text'):
                                if submenu.attrib.get('type') == 'special':
                                        for specialmenu in submenu.findall('item'):
                                                name = rootmenu.text + '-' + subsubmenu.text + '-' + specialmenu[1].text
                                                listitem = xbmcgui.ListItem(label = name)
                                                url = specialmenu[4].text
                                                u = sys.argv[0] + "?mode=1&name=" + urllib.quote_plus(name) + "&url=" + urllib.quote_plus(url)
                                                ok = xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = u, listitem = listitem, isFolder = True)
                                for subsubmenuurl in submenu.findall('urlLatest'):
                                        name = rootmenu.text + '-' + subsubmenu.text
                                        listitem = xbmcgui.ListItem(label = name)
                                        url = subsubmenuurl.text
                                        u = sys.argv[0] + "?mode=1&name=" + urllib.quote_plus(name) + "&url=" + urllib.quote_plus(url)
                                        ok = xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = u, listitem = listitem, isFolder = True)

        xbmcplugin.addSortMethod( handle = int(sys.argv[ 1 ]), sortMethod = xbmcplugin.SORT_METHOD_NONE )
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

def build_clip_directory(url, clipid):
        numclips=__settings__.getSetting('numclips')
        numclips = (int(numclips) + 1) * 10

        url = url + '&pageSize=' + str(numclips)
        data = open_url(url)
        root = ET.fromstring(data)

        for menuitem in root.findall('channel/item'):
                title = menuitem.find('title').text
                description = menuitem.find('description').text
                image = menuitem.find('imgUrl').text
                clipid = menuitem.find('id').text
                vidtype = menuitem.find('type').text

                if vidtype == 'video':
                        #if vidtype is video that means that it's a game on demand or something longer than a clip.
                        listitem = xbmcgui.ListItem(label = title, iconImage = image, thumbnailImage = image)
                        listitem.setInfo( type = "Video", infoLabels = { "Title": title, "Director": __plugin__, "Plot": description } )
                        u = sys.argv[0] + "?mode=2&name=" + urllib.quote_plus(name) + "&url=" + urllib.quote_plus(url) + "&clipid=" + urllib.quote_plus(clipid)
                        ok = xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = u, listitem = listitem, isFolder = True)

                else:
                        listitem = xbmcgui.ListItem(label = title, iconImage = image, thumbnailImage = image)
                        listitem.setProperty('IsPlayable','true')
                        listitem.setInfo( type = "Video", infoLabels = { "Title": title, "Director": __plugin__, "Plot": description } )
                        u = sys.argv[0] + "?mode=3&clipid=" + urllib.quote_plus(clipid) + "&url=" + urllib.quote_plus(url)
                        ok = xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = u, listitem = listitem, isFolder = False)

        return xbmcplugin.endOfDirectory(int(sys.argv[1]))

def build_ondemand_directory(url, clipid):
        
        #this section is for the "on demand" games.  As of creating this plugin (version 0.1.2) there is only hockey canada games on demand, cfl games on demand, and curling matches on demand
        data = open_url(url)
        root = ET.fromstring(data)

        for menuitem in root.findall('channel/item'):
                allclipids = menuitem.find('id').text
                if allclipids == clipid:
                        for cliplist in menuitem.findall('clipList/item'):
                                videoclipid = cliplist.find('id').text
                                title = cliplist.find('title').text
                                description = cliplist.find('description').text
                                image = cliplist.find('imgUrl').text

                                #below creates menu items for the parts of the game/match (1st period, 2nd period, 3rd period)
                                listitem = xbmcgui.ListItem(label = title, iconImage = image, thumbnailImage = image)
                                listitem.setProperty('IsPlayable','true')
                                listitem.setInfo( type = "Video", infoLabels = { "Title": title, "Director": __plugin__, "Plot": description } )
                                u = sys.argv[0] + "?mode=3&clipid=" + urllib.quote_plus(videoclipid) + "&url=" + urllib.quote_plus(url)
                                ok = xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = u, listitem = listitem, isFolder = False)


        return xbmcplugin.endOfDirectory(int(sys.argv[1]))        

                
def clean(name):
        remove = [('&amp;','&'), ('&quot;','"'), ('&#039;','\''), ('\r\n',''), ('&apos;','\'')]
        for trash, crap in remove:
                name = name.replace(trash,crap)
        return name
                        
def play_video(url, clipid):
        
        tempurl = 'http://esi.ctv.ca/datafeed/urlgenjs.aspx?vid=' + clipid
        #below was the link to get the rtmp details before tsn changed from watch.tsn.ca to video.tsn.ca
        #tempurl = 'http://cls.ctvdigital.net/cliplookup.aspx?id=' + clipid
                
        data = open_url(tempurl)

        #get the entire rtmpe:// out of the contents of the esi.ctv.ca
        temprtmpe = re.compile('Video.Load\({url:\'(.+?)\'').findall(data)

        # there are currently 4 very different rtmpe strings from tsn.  My code isn't smart enough to everything
        # so this is a poor workaround
        o = urlparse.urlparse(temprtmpe[0])
        if o.netloc == 'tsn.fcod.llnwd.net':
                firstpart = 'rtmpe://tsn.fcod.llnwd.net/a5504'
                secondpart = re.compile('a5504/(.+?)\'').findall(data)
                playpath = re.compile('ondemand/(.+?).mp4').findall(temprtmpe[0])
                url = firstpart + ' playpath=mp4:' + secondpart[0]
        elif o.netloc == 'ctvmms.rd.llnwd.net':
                firstpart = 'http://ctvmms.vo.llnwd.net/kip0/_pxn=1+_pxI0=Ripod-h264+_pxL0=undefined+_pxM0=+_pxK=19321+_pxE=mp4/'
                secondpart = re.compile('ctvmms.rd.llnwd.net/(.+?).mp4').findall(temprtmpe[0])
                url = firstpart + secondpart[0] + '.mp4'
        elif o.netloc == 'tsnpmd.akamaihd.edgesuite.net':
                vidquality=__settings__.getSetting('vidquality')
                #adding 1 to the video quality because I don't use zero as the lowest quality, I use 1 as the lowest quality.
                vidquality=int(vidquality)+1
                
                url = temprtmpe[0]
                #starting in version 0.1.5 (March 19 2013) tsn started using adaptive quality in their http streams
                #the quality now goes up to 720p (adaptive_08)
                url = url.replace('Adaptive_04','Adaptive_0' + str(vidquality+3))
        else:
                #break that down into 3 parts so that we can build the final url and playpath
                firstpart = re.compile('rtmpe(.+?)ondemand/').findall(temprtmpe[0])
                firstpart = 'rtmpe' + firstpart[0] + 'ondemand?'
                secondpart = re.compile('\?(.+?)\'').findall(data)
                thirdpart = re.compile('ondemand/(.+?)\?').findall(temprtmpe[0])
                playpath = ' playpath=mp4:' + thirdpart[0]

                vidquality=__settings__.getSetting('vidquality')
                #adding 1 to the video quality because I don't use zero as the lowest quality, I use 1 as the lowest quality.
                vidquality=int(vidquality)+1

                #the tsn site adaptivly figures out what quality it should show you (maybe based on your bandwidth somehow?).  We can set the quality outselves in the settings of this plugin
                playpath = playpath.replace('Adaptive_05','Adaptive_0' + str(vidquality))
                playpath = playpath.replace('Adaptive_04','Adaptive_0' + str(vidquality))
                playpath = playpath.replace('Adaptive_03','Adaptive_0' + str(vidquality))
                playpath = playpath.replace('Adaptive_02','Adaptive_0' + str(vidquality))
                playpath = playpath.replace('Adaptive_01','Adaptive_0' + str(vidquality))
                url = firstpart + secondpart[0] + playpath

        item = xbmcgui.ListItem(path=url)
        return xbmcplugin.setResolvedUrl(handle, True, item)        

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

params = get_params()
url = None
name = None
mode = None
plot = None
genre = None
episode = None
clipid = None

try:
        url = urllib.unquote_plus(params["url"])
except:
        pass
try:
        name = urllib.unquote_plus(params["name"])
except:
        pass
try:
        mode = int(params["mode"])
except:
        pass
try:
        plot = urllib.unquote_plus(params["plot"])
except:
        pass
try:
        genre = urllib.unquote_plus(params["genre"])
except:
        pass
try:
        clipid = urllib.unquote_plus(params["clipid"])
except:
        pass
try:
        episode = int(params["episode"])
except:
        pass

if mode == None:
        build_main_directory()
elif mode == 1:
        build_clip_directory(url, clipid)
elif mode == 2:
        build_ondemand_directory(url, clipid)
elif mode == 3:
        play_video(url,clipid)
