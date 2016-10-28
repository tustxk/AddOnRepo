import xbmcplugin
import xbmcplugin
import xbmc
import xbmcgui
import urllib
import urllib2
import sys
import os
import re
import cookielib
from datetime import datetime
import time

import demjson
from BeautifulSoup import BeautifulSoup
from BeautifulSoup import MinimalSoup
import resources.lib._common as common
from BeautifulSoup import BeautifulSoup, BeautifulStoneSoup

pluginhandle = int (sys.argv[1])

BASE_URL = "http://www.cbs.com/"
BASE = "http://www.cbs.com"
#andyman 23 August 2013

def rootlist():
    print "DEBUG: CBS rootlist 230813"
    data = common.getURL(BASE_URL)
    data = unicode(data, 'utf-8', errors='ignore')
    tree = BeautifulSoup(data, convertEntities=BeautifulSoup.HTML_ENTITIES)
    categories = tree.findAll('h4', attrs={'class' : 'cbs-show-category'})
    for item in categories:
        catname = item.string
        skipCat = False
        if 'contests' in catname.lower():
            skipCat = True
        if not skipCat:
            common.addDirectory(catname, 'cbs', 'shows', str(categories.index(item)))
#    menu=tree.find(attrs={'id' : 'daypart_nav'})
#    categories=menu.findAll('a')
#    for item in categories:
#        if item['href'].find('javascript') == 0:
#            catid = item['onclick'].replace("showDaypart('",'').replace("');",'')
#            name = re.compile('<a.*>(.+)</a>').findall(str(item))[0].title()
#            common.addDirectory(name, 'cbs', 'shows', catid)
    common.setView('seasons')

def shows(catid = common.args.url):
    print "DEBUG: CBS shows - catid:" + catid
    icatid = int(catid)
    data = common.getURL(BASE_URL)
    data = unicode(data, 'utf-8', errors='ignore')
    tree = BeautifulSoup(data, convertEntities=BeautifulSoup.HTML_ENTITIES)
    showlists = tree.findAll('ul', attrs={'class' : 'cbs-show-list'})
    shows = showlists[icatid].findAll('li', attrs={'class' : 'show-list-item'})
    for show in shows:
        skipTitle = False
        name = unicode(show.contents[0].string)
        name = name.replace(u"\u2122", '').replace(u"\xae", '')
        print name.encode("utf-8")
        url = show.contents[0]['href']
        if not ('http://' in url):
            url = BASE + show.contents[0]['href'] + 'video/'
        #filter shows
        if 'luke-bryan' in url:
            url = 'http://www.cbs.com/shows/academy_of_country_music/luke-bryan/'
        elif 'cbsaroundtheworld' in url:
            skipTitle = True
        elif 'power-of-observation' in url:
            url = 'http://www.cbs.com/shows/elementary/power-of-observation/'
        elif 'say-it-right-on-sunday-night' in url:
            skipTitle = True
        elif 'after-show' in url:
            url = 'http://www.cbs.com/shows/survivor/after-show/'
        elif 'cbs_cares' in url:
            skipTitle = True
        elif 'comedy-buzz-tour' in url:
            skipTitle = True
        elif 'commercials' in url:  #filters clash of commercials and superbowl commercials
            skipTitle = True
        elif 'cbssports' in url:
            skipTitle = True
        elif 'superbowl' in url:
            skipTitle = True
        if ('preview' in name.lower()) or ('finales' in name.lower()) or ('new season' in name.lower()):
            skipTitle = True
        #add shows
        if not skipTitle:
            if icatid == 4:
                common.addShow(name, 'cbs', 'showClassicSeasons', url)
            else:
                common.addShow(name, 'cbs', 'showCategories', url)
    common.setView('tvshows')
    
# def shows(catid = common.args.url):
    # print "DEBUG: CBS shows - catid:" + catid
    # xbmcplugin.setContent(pluginhandle, 'tvshows')
    # data = common.getURL(BASE_URL)
    # data = re.compile('<!-- SHOWS LIST -->(.*?)<!-- END SHOWS LIST -->',re.DOTALL).findall(data)[0]  
    # tree=BeautifulSoup(data, convertEntities=BeautifulSoup.HTML_ENTITIES)
    # categories=tree.findAll('div', attrs={'id' : True}, recursive=False)
    # for item in categories:
        # if item['id'] == catid:
            # shows = item.findAll(attrs={'id' : 'show_block_interior'})
            # for show in shows:
                # name = show.find('img')['alt'].encode('utf-8')
                # thumbnail = BASE + show.find('img')['src']
                # url = show.find('a')['href']
                # if 'cbs_evening_news' in url:
                    # url = 'http://www.cbs.com/shows/cbs_evening_news/video/'
                # elif '/shows/elementary/' in url:
                    # url+='video/'
                # elif '/shows/vegas/' in url:
                    # url+='video/'
                # elif '/shows/nyc_22' in url:
                    # name = 'NYC 22'
                    # url+='video/'
                # elif 'under-the-dome/' in url:
                    # url+='video/'
                # if catid == 'classics':
                    # common.addShow(name, 'cbs', 'showClassicSeasons', url)
                # else:
                    # common.addShow(name, 'cbs', 'showCategories', url)#, thumb=thumbnail)
            # break
    # xbmcplugin.addSortMethod(pluginhandle, xbmcplugin.SORT_METHOD_LABEL)
    # common.setView('tvshows')

def showCategories(url = common.args.url):
    print "DEBUG: CBS showCategories"
    data = common.getURL(url)
    try:
        carousels = re.compile("loadUpCarousel\('(.*?)','(.*?)', '(.*?)', (.*?), true, stored").findall(data)
        carousels[0][0]
        for name,dir1,dir2,dir3 in carousels:
            url = 'http://www.cbs.com/carousels/'+dir3+'/video/'+dir1+'/'+dir2+'/0/400/'
            common.addDirectory(name, 'cbs', 'newvideos', url)
    except:
        print 'CBS: trying 16.04.2013 id-carousel'
        tree=BeautifulSoup(data, convertEntities=BeautifulSoup.HTML_ENTITIES)
        categories = re.compile("id-carousel-(\d+)").findall(str(tree))
        for catid in categories:
            if catid == '214878' and 'american-baking-competition' in url:
                continue
            thisUrl = 'http://www.cbs.com/carousels/videosBySection/'+catid+'/offset/0/limit/40/xs/0'
            data = common.getURL(thisUrl)
            name = demjson.decode(data)['result']['title']
            common.addDirectory(name, 'cbs', 'newvideos2', thisUrl)
    common.setView('seasons')                                      

def showClassicSeasons(url = common.args.url):
    url = url.replace('/classics/','/shows/')
    print "DEBUG Classic seasons: " + url
    data = common.getURL(url)
    tree=BeautifulSoup(data, convertEntities=BeautifulSoup.HTML_ENTITIES)
    seasons=tree.findAll(attrs={'name' : 'season'})
    if len(seasons) == 0:
        seasonurl = url.replace('/video/','/videos_more/') + 'season/%s/videos/episodes/' % '1'
        showClassicEpisodes(seasonurl)
    else:
        for season in seasons:
            seasonurl = url.replace('/video/','/videos_more/') + 'season/%s/videos/episodes/' % season['value']
            name = 'Season ' + str(season['value'])
            common.addDirectory(name, 'cbs', 'showClassicEpisodes', seasonurl)
        common.setView('seasons')

    
def showClassicEpisodes(seasonurl = common.args.url):
    print "DEBUG: CBS showClassicEpisodes"
    #now get the episode list from the json file
    try:
        epdata = common.getURL(seasonurl + "1")
        itemList = demjson.decode(epdata)
        if itemList['success'] == True:
            eptree = BeautifulSoup(itemList['html'], convertEntities=BeautifulSoup.HTML_ENTITIES)
            episodes = eptree.findAll(attrs={'class' : 'video-content-item'})
            for episode in episodes:
                addClassicEpisode(episode)
            #now check for "more videos"
            morevideos = itemList['more']
            while (morevideos):
                moreindex = int(itemList['next']) + 1
                epdata = common.getURL(seasonurl + str(moreindex))
                itemList = demjson.decode(epdata)
                if itemList['success'] == True:
                    eptree = BeautifulSoup(itemList['html'], convertEntities=BeautifulSoup.HTML_ENTITIES)
                    episodes = eptree.findAll(attrs={'class' : 'video-content-item'})
                    for episode in episodes:
                        addClassicEpisode(episode)
                morevideos = itemList['more']
        xbmcplugin.addSortMethod(pluginhandle, xbmcplugin.SORT_METHOD_EPISODE)
        common.setView('episodes')
    except:
        print "DEBUG: CBS showClassicEpisodes error"

def addClassicEpisode(thisEpisode):
    title = thisEpisode.find(attrs={'class' : 'video-content-title'}).string.encode('utf-8')
    url = BASE + thisEpisode.find('a')['href']
    description = thisEpisode.find(attrs={'class' : 'video-content-description'}).string
    thumblink = thisEpisode.find(attrs={'class' : 'video-content-thumb-container'}).contents[0]
    thumb = thumblink.find('img')['src']
    # seriesTitle = video['seriesTitle']
    seriesTitle = ''
    metadiv = thisEpisode.find(attrs={'class' : 'video-content-season-info'}).contents[0]
    # Season 1, Episode 12  -->  [(u'1', u'12')]
    meta = re.compile("Season (\d+), Episode (\d+).*").findall(str(metadiv))
    try:seasonNum = int(meta[0][0])
    except:seasonNum = 0
    try:episodeNum = int(meta[0][1])
    except:episodeNum = 0 
    durdiv = thisEpisode.find(attrs={'class' : 'video-content-duration'}).contents[1] #skip span tag
    duration = str(durdiv).replace('(', '').split(':')[0]
    try:
        airDateDiv = str(thisEpisode.find(attrs={'class' : 'video-content-air-date'}).contents[0])
        airDateMeta = re.compile("</span>: (\d+.\d+.\d+)").findall(str(airDateDiv))[0]
        airDate = common.formatDate(airDateMeta, '%m.%d.%Y')
    except:airDate=''
    rating = ''
    u = sys.argv[0]
    u += '?url="'+urllib.quote_plus(url)+'"'
    u += '&mode="cbs"'
    u += '&sitemode="play"'
    displayname = '%sx%s - %s' % (seasonNum,episodeNum,title)
    infoLabels={ "Title":title,
                 "Plot":description,
                 "Season":seasonNum,
                 "Episode":episodeNum,
                 "premiered":airDate,
                 "Duration":str(duration),
                 "mpaa":rating,
                 "TVShowTitle":seriesTitle
                 }
    common.addVideo(u,displayname,thumb,infoLabels=infoLabels)

def showsubcats(url = common.args.url):
    moduleid = url.split('<moduleid>')[1]
    url      = url.split('<moduleid>')[0]
    data = common.getURL(url)
    tree=BeautifulSoup(data, convertEntities=BeautifulSoup.HTML_ENTITIES)
    vid_module = tree.find(attrs={'id' : moduleid})
    PAGES(vid_module)
    common.setView('episodes')

def videos(url = common.args.url):
    xbmcplugin.setContent(pluginhandle, 'episodes')
    data = common.getURL(url)
    tree=BeautifulSoup(data, convertEntities=BeautifulSoup.HTML_ENTITIES)
    try:
        options = tree.findAll(attrs={'class' : 'vid_module'})
        if len(options) == 1:
            PAGES(tree)
        else:
            for option in options:
                moduleid = option['id']
                name = option.find(attrs={'class' : 'hdr'}).string
                common.addDirectory(name, 'cbs', 'showsubcats', url+'<moduleid>'+moduleid)                                        
    except:
        PAGES(tree)
    common.setView('episodes')
 
def newvideos(url = common.args.url):
    print "DEBUG: CBS newvideos"
    data = common.getURL(url)
    itemList = demjson.decode(data)['itemList']
    for video in itemList:
        url = video['pid']
        description = video['description']
        thumb = video['thumbnail']
        seriesTitle = video['seriesTitle']
        title = video['title']
        try:episodeNum = int(video['episodeNum'])
        except:episodeNum = 0 
        try:seasonNum = int(video['seasonNum'])
        except:seasonNum = 0
        duration = int(video['duration'])
        airDate = video['_airDate']
        rating = video['rating']
        u = sys.argv[0]
        u += '?url="'+urllib.quote_plus(url)+'"'
        u += '&mode="cbs"'
        u += '&sitemode="play"'
        if episodeNum == 0 and seasonNum == 0:
            displayname = title
        else:
            displayname = '%sx%s - %s' % (seasonNum,episodeNum,title)
        infoLabels={ "Title":title,
                     "Plot":description,
                     "Season":seasonNum,
                     "Episode":episodeNum,
                     "premiered":airDate,
                     "Duration":str(duration),
                     "mpaa":rating,
                     "TVShowTitle":seriesTitle
                     }
        common.addVideo(u,displayname,thumb,infoLabels=infoLabels)
    common.setView('episodes')  

def newvideos2(url = common.args.url):
    print "DEBUG: CBS newvideos2"
    data = common.getURL(url)
    itemList = demjson.decode(data)['result']['data']
    useProgress = False
    if len(itemList) > 9:
        useProgress = True
        progressBar = xbmcgui.DialogProgress()
        progressBar.create('Loading videos...')
        idx = 0
    for video in itemList:
        if useProgress:
            idx = idx + 1
            percent = int((float(idx) / len(itemList)) * 100)
            message = "Finding video " + str(idx) + " of " + str(len(itemList))
            progressBar.update(percent, message)
        
        # data from JSON file
        title = video['label']
        if title.strip() == '':
            title = video['episode_title']
        seriesTitle = video['series_title']
        try:
            dtAirDate = datetime.strptime(video['airdate'], '%m/%d/%y')
            airDate = datetime.strftime(dtAirDate, '%Y-%m-%d')
        except:
            airDate = 0
        thumb = video['thumb']['large']
        metaUrl = BASE + video['url']
        #videoUrl = video['streaming_url']
        videoUrl = metaUrl
        
        # need to fetch the video URL for the rest of the meta data
        metaData = common.getURL(metaUrl)
        metaTree = BeautifulSoup(metaData, convertEntities=BeautifulSoup.HTML_ENTITIES)
        description = metaTree.find('meta',attrs={'name' : 'description'})['content'].replace("\\'",'"')
        metadiv = metaTree.find('div',attrs={'class' : 'title'})
        # <span>S6 Ep18 (20:12)  -->  [(u'6', u'18', u'20', u'12')]
        meta = re.compile("<span>S(\d+)\D+(\d+)\D+(\d+)\:(\d+)").findall(str(metadiv))
        try:episodeNum = int(meta[0][1])
        except:episodeNum = 0 
        try:seasonNum = int(meta[0][0])
        except:seasonNum = 0
        try:duration = int(meta[0][2])
        except:duration = int('0')
        #rating = video['rating']
        rating = 0
        u = sys.argv[0]
        u += '?url="'+urllib.quote_plus(videoUrl)+'"'
        u += '&mode="cbs"'
        u += '&sitemode="play"'
        displayname = '%sx%s - %s' % (seasonNum,episodeNum,title)
        infoLabels={ "Title":title,
                     "Plot":description,
                     "Season":seasonNum,
                     "Episode":episodeNum,
                     "premiered":airDate,
                     "Duration":str(duration),
                     "mpaa":rating,
                     "TVShowTitle":seriesTitle
                     }
        common.addVideo(u,displayname,thumb,infoLabels=infoLabels)
        if useProgress:
            if progressBar.iscanceled():
                common.setView('episodes')
                break
    if useProgress:
        progressBar.close()
    common.setView('episodes')
    
def PAGES( tree ):
    try:
        print 'starting PAGES'
        try:
            search_elements = tree.find(attrs={'name' : 'searchEl'})['value']
            return_elements = tree.find(attrs={'name' : 'returnEl'})['value']
        except:
            print 'CBS: search and return elements failed'
        try:
            last_page = tree.find(attrs={'id' : 'pagination0'}).findAll(attrs={'class' : 'vids_pag_off'})[-1].string
            last_page = int(last_page) + 1
        except:
            print 'CBS: last page failed reverting to default'
            last_page = 2
        for pageNum in range(1,last_page):
            values = {'pg' : str(pageNum),
                      'repub' : 'yes',
                      'displayType' : 'twoby',
                      'search_elements' : search_elements,
                      'return_elements' : return_elements,
                      'carouselId' : '0',
                      'vs' : 'Default',
                      'play' : 'true'
                      }
            url = 'http://www.cbs.com/sitecommon/includes/video/2009_carousel_data_multiple.php' 
            data = common.getURL(url, values)
            VIDEOLINKS(data)
    except:
        print 'Pages Failed'

def VIDEOLINKS( data ):
    print "DEBUG: CBS VIDEOLINKS function"
    tree=BeautifulSoup(data, convertEntities=BeautifulSoup.HTML_ENTITIES)
    vidfeed=tree.find(attrs={'class' : 'vids_feed'})
    videos = vidfeed.findAll(attrs={'class' : 'floatLeft','style' : True})
    for video in videos:
        thumb = video.find('img')['src']
        vidtitle = video.find(attrs={'class' : 'vidtitle'})
        pid = vidtitle['href'].split('pid=')[1].split('&')[0]
        displayname = vidtitle.string.encode('utf-8')
        try:
            title = displayname.split('-')[1].strip()
            series = displayname.split('-')[0].strip()
        except:
            print 'title/series metadata failure'
            title = displayname
            series = ''

        metadata = video.find(attrs={'class' : 'season_episode'}).renderContents()
        try:
            duration = metadata.split('(')[1].replace(')','')
        except:
            print 'duration metadata failure'
            duration = ''
        try:
            aired = metadata.split('<')[0].split(':')[1].strip()
        except:
            print 'air date metadata failure'
            aired = ''
        try:
            seasonepisode = thumb.split('/')[-1].split('_')[2]
            if 3 == len(seasonepisode):
                season = int(seasonepisode[:1])
                episode = int(seasonepisode[-2:])
            elif 4 == len(seasonepisode):
                season = int(seasonepisode[:2])
                episode = int(seasonepisode[-2:])
            if season <> 0 or episode <> 0:
                displayname = '%sx%s - %s' % (str(season),str(episode),title)
        except:
            print 'season/episode metadata failed'
            season = 0
            episode = 0
        u = sys.argv[0]
        u += '?url="'+urllib.quote_plus(pid)+'"'
        u += '&mode="cbs"'
        u += '&sitemode="play"'
        infoLabels={ "Title":title,
                     "Season":season,
                     "Episode":episode,
                     "premiered":aired,
                     "Duration":duration,
                     "TVShowTitle":series
                     }
        common.addVideo(u,displayname,thumb,infoLabels=infoLabels)
    common.setView('episodes')
  
def clean_subs(data):
        br = re.compile(r'<br.*?>')
        br_2 = re.compile(r'\n')
        tag = re.compile(r'<.*?>')
        space = re.compile(r'\s\s\s+')
        sub = br.sub('\n', data)
        sub = tag.sub(' ', sub)
        sub = br_2.sub('<br/>', sub)
        sub = space.sub(' ', sub)
        return sub

def convert_subtitles(subtitles, output):
    subtitle_data = subtitles
    subtitle_data = subtitle_data.replace("\n","").replace("\r","")
    subtitle_data = BeautifulStoneSoup(subtitle_data)
    subtitle_array = []
    srt_output = ''

    print "CBS: --> Converting subtitles to SRT"
    #self.update_dialog('Converting Subtitles to SRT')
    lines = subtitle_data.findAll('p') #split the file into lines
    for line in lines:
        if line is not None:
            #print "LINE: " + str(line)
            #print "LINE BEGIN: " + str(line['begin'])
            
            sub=str(clean_subs(str(line)))
            try:
                newsub=sub
                sub = BeautifulStoneSoup(sub, convertEntities=BeautifulStoneSoup.ALL_ENTITIES)
            except:
                sub=newsub
            #print "CURRENT SUB: " + str(sub)
            begin_time = line['begin']
            end_time = line['end']
            start_split =begin_time.split(".")                        
            end_split =end_time.split(".")                        
            timestamp = "%s,%s" % (start_split[0], start_split[1])
            end_timestamp = "%s,%s" % (end_split[0], end_split[1])
            #print "TIMESTAMP " + str(timestamp) + " " + str(end_timestamp)
   
            temp_dict = {'start':timestamp, 'end':end_timestamp, 'text':sub}
            subtitle_array.append(temp_dict)
                
    for i, subtitle in enumerate(subtitle_array):
        line = str(i+1)+"\n"+str(subtitle['start'])+" --> "+str(subtitle['end'])+"\n"+str(subtitle['text'])+"\n\n"
        srt_output += line
                    
    file = open(os.path.join(common.pluginpath,'resources','cache',output+'.srt'), 'w')
    file.write(srt_output)
    file.close()
    print "CBS: --> Successfully converted subtitles to SRT"
    #self.update_dialog('Conversion Complete')
    return True
    
def play(url = common.args.url):
    print "DEBUG: CBS play"
    #swfUrl = 'http://can.cbs.com/thunder/player/chrome/canplayer.swf'
    swfUrl = 'http://canstatic.cbs.com/chrome/canplayer.swf'
    if 'http://' in url:
        data=common.getURL(url)
        try:
            pid = re.compile('video.settings.pid = "(.*?)";').findall(data)[0]
        except:
            pid = re.compile("video.settings.pid = '(.*?)';").findall(data)[0]
    else:
        pid = url  
    #print 'PID: ' + pid
    # OLD URL
    #url = "http://release.theplatform.com/content.select?format=SMIL&Tracking=true&balance=true&MBR=true&pid=" + pid
    url = "http://link.theplatform.com/s/dJ5BDC/%s?format=SMIL&Tracking=true&mbr=true" % pid
    if (common.settings['enableproxy'] == 'true'):
        proxy = True
    else:
        proxy = False
    data=common.getURL(url,proxy=proxy)
    tree=BeautifulStoneSoup(data, convertEntities=BeautifulStoneSoup.XML_ENTITIES)
    
    if (common.settings['enablesubtitles'] == 'true'):
        closedcaption = tree.find('param',attrs={'name':'ClosedCaptionURL'})
        if (closedcaption is not None):
            try:
                xml_closedcaption = common.getURL(closedcaption['value'])
                convert_subtitles(xml_closedcaption,pid)
            except:
                closecaption = None
    rtmpbase = tree.find('meta')
    if rtmpbase:
        rtmpbase = rtmpbase['base']
        items=tree.find('switch').findAll('video')
        hbitrate = -1
        sbitrate = int(common.settings['quality']) * 1024
        for item in items:
            bitrate = int(item['system-bitrate'])
            if bitrate > hbitrate and bitrate <= sbitrate:
                hbitrate = bitrate
                playpath = item['src']
                if '.mp4' in playpath:
                    playpath = 'mp4:'+playpath
                else:
                    playpath = playpath.replace('.flv','')
                finalurl = rtmpbase+' playpath='+playpath + " swfurl=" + swfUrl + " swfvfy=true"
    item = xbmcgui.ListItem(path=finalurl)
    xbmcplugin.setResolvedUrl(pluginhandle, True, item)
    if (common.settings['enablesubtitles'] == 'true') and (closedcaption is not None):
        while not xbmc.Player().isPlaying():
            print 'CBS--> Not Playing'
            xbmc.sleep(100)
    
        subtitles = os.path.join(common.pluginpath,'resources','cache',pid+'.srt')
        print "CBS --> Setting subtitles"
        xbmc.Player().setSubtitles(subtitles)

#Star Trek routines
def stShows(url = common.args.url,db=False):
    stbase = 'http://www.startrek.com'
    data = common.getURL(url)
    remove = re.compile('<!.*?">')
    data = re.sub(remove, '', data)
    tree=BeautifulSoup(data, convertEntities=BeautifulSoup.HTML_ENTITIES)
    stshows=tree.find('div',attrs={'id' : 'channels'}).findAll('li', attrs={'class' : True})
    st_shows = []      
    for show in stshows:
        name = show['class'].replace('-',' ').title()
        thumb = stbase+show.find('img')['src']
        url = stbase+show.find('a')['href']
        if 'Star Trek' not in name:
            name = 'Star Trek '+name
        if db:
            st_shows.append((name,'cbs','stshowcats',url))
        else:
            common.addShow(name, 'cbs', 'stshowcats', url)#, thumb=thumb)
    if db:
        return st_shows
 
def stshowcats(url = common.args.url):
    stbase = 'http://www.startrek.com'
    data = common.getURL(url)
    remove = re.compile('<!.*?">')
    data = re.sub(remove, '', data)
    tree=BeautifulSoup(data, convertEntities=BeautifulSoup.HTML_ENTITIES)
    stcats=tree.find('div',attrs={'id' : 'content'}).findAll('div', attrs={'class' : 'box_news'})       
    for cat in stcats:
        name = cat.find('h4').contents[1].strip()
        common.addDirectory(name, 'cbs', 'stvideos', url+'<name>'+name)
    common.setView('seasons')

def stvideos(url = common.args.url):
    stbase = 'http://www.startrek.com'
    argname = url.split('<name>')[1]
    url = url.split('<name>')[0]
    stbase = 'http://www.startrek.com'
    data = common.getURL(url)
    remove = re.compile('<!.*?">')
    data = re.sub(remove, '', data)
    tree=BeautifulSoup(data, convertEntities=BeautifulSoup.HTML_ENTITIES)
    stcats=tree.find('div',attrs={'id' : 'content'}).findAll('div', attrs={'class' : 'box_news'})       
    for cat in stcats:
        name = cat.find('h4').contents[1].strip()
        if name == argname:
            titleUrl=stbase+cat.find('a',attrs={'class' : 'title '})['onclick'].split("url:'")[1].split("'}); return")[0]
            if 'Full Episodes' in argname:
                titleUrl += '/page_full/1'
            stprocessvideos(titleUrl)
    common.setView('episodes')

def stprocessvideos(purl):
    print "enter stprocessvideos"
    stbase = 'http://www.startrek.com'
    xbmcplugin.addSortMethod(pluginhandle, xbmcplugin.SORT_METHOD_LABEL)
    data = common.getURL(purl)
    tree=BeautifulSoup(data, convertEntities=BeautifulSoup.HTML_ENTITIES)
    videos=tree.find(attrs={'class' : 'videos_container'}).findAll('li')
    for video in videos:
        thumb = video.find('img')['src']
        url = stbase+video.find('a')['href']
        try:
            showname,name = video.findAll('a')[1].string.split('-')
        except:
            name = video.findAll('a')[1].string
            showname = ''
        try:
            seasonepisode, duration = video.findAll('p')
            seasonepisode = seasonepisode.string.replace('Season ','').split(' Ep. ')
            season = int(seasonepisode[0])
            episode = int(seasonepisode[1])
            duration = duration.string.split('(')[1].replace(')','')
        except:
            season = 0
            episode = 0
            duration = ''
        if season <> 0 or episode <> 0:
            displayname = '%sx%s - %s' % (str(season),str(episode),name)
        else:
            displayname = name
        u = sys.argv[0]
        u += '?url="'+urllib.quote_plus(url)+'"'
        u += '&mode="cbs"'
        u += '&sitemode="playST"'
        infoLabels={ "Title":displayname,
                     "Season":season,
                     "Episode":episode,
                     #"premiered":aired,
                     "Duration":duration,
                     "TVShowTitle":showname
                     }
        common.addVideo(u,displayname,thumb,infoLabels=infoLabels)
    if len(videos) == 4:
        if '/page_full/' not in purl and '/page_other/' not in purl:
            nurl = purl+'/page_other/2'
        else:
            page = int(purl.split('/')[-1])
            nextpage = page + 1
            nurl = purl.replace('/'+str(page),'/'+str(nextpage))
        stprocessvideos(nurl)

def playST(url = common.args.url):
    print "Entering playST function"

    if 'watch_episode' in url:
        pid=url.split('/')[-1]
        play(pid)
    else:
        data=common.getURL(url)
        url = re.compile("flowplayer\\('flow_player', '.*?', '(.*?)'\\)").findall(data)[0]
        item = xbmcgui.ListItem(path=url)
        xbmcplugin.setResolvedUrl(pluginhandle, True, item)   
