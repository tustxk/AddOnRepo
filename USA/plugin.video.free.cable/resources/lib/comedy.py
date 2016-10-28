import xbmc
import xbmcgui
import xbmcplugin
import urllib
import urllib2
import httplib
import sys
import os
import re

from BeautifulSoup import BeautifulSoup
from BeautifulSoup import BeautifulStoneSoup
import resources.lib._common as common

pluginhandle=int(sys.argv[1])

BASE_URL = 'http://www.comedycentral.com'

def rootlist(db=False):
    data = common.getURL(BASE_URL)
    data = unicode(data, 'utf-8', errors='ignore')
    tree=BeautifulSoup(data, convertEntities=BeautifulSoup.HTML_ENTITIES)
    menu=tree.find('li',attrs={'class':'nav_item_3'}).findAll('a')
    db_shows = []
    for item in menu:
        name = item.string
        url = item['href']
        if 'http://' not in url:
            url = BASE_URL+url 
        if name <> 'Episodes':
            if name == 'South Park':
                mode = 'sp_seasons'
            elif name <> 'The Daily Show with Jon Stewart' and name <> 'The Colbert Report':
                mode = 'ccepisodes'
            else:
                mode = 'episodes'
            if db==True:
                db_shows.append((name,'comedy',mode,url))
            else:
                common.addShow(name,'comedy',mode,url)
    if db==True:
        return db_shows
    else:
        common.setView('tvshows')

def ccepisodes(url=common.args.url):
    data = common.getURL(url)
    try:
        showcase=re.compile("var episodeShowcaseLlink = '(.+?)';").findall(data)[0]
        keepGoing=True
    except:
        keepGoing=False

        tree=BeautifulSoup(data, convertEntities=BeautifulSoup.HTML_ENTITIES)
        episodes=tree.findAll('div',attrs={'class':'episode_item'})
        for episode in episodes:
            infoLabels={}
            url=episode.find('a')['href']
            thumb=episode.find('img')['src'].split('?')[0]
            title=episode.find('h3').find('a').string
            u = sys.argv[0]
            u += '?url="'+urllib.quote_plus(url)+'"'
            u += '&mode="comedy"'
            u += '&sitemode="playurl"'
            #common.addVideo(u,"Play Episode")
            print episode
            premired=episode.find('div',attrs={'class':'video_meta'}).string.strip().encode('utf8')
            print premired
            premired=common.formatDate(premired.replace('Aired: ',''),'%m/%d/%Y') 
            infoLabels['premiered']=premired
            epid=re.compile('[a-z]+_([0-9])([0-9]{2})_').findall(thumb)[0]
            season=epid[0]
            episode=epid[1]
            print epid,episode
            infoLabels['Season']=season
            infoLabels['Episode']=episode
            infoLabels['Title']=title
            displayname=title.split(' - ')[1]
            common.addVideo(u,displayname,thumb,infoLabels=infoLabels)
    current=1
    while keepGoing:
        showcase_url = BASE_URL+showcase+'?currentPage='+str(current)
        data = common.getURL(showcase_url)
        videos=BeautifulSoup(data, convertEntities=BeautifulSoup.HTML_ENTITIES).findAll('div',attrs={'itemtype':'http://schema.org/TVEpisode'})
        for video in videos:
            infoLabels={}
            url=video.find('meta',attrs={'itemprop':'url'})['content']
            thumb=video.find('meta',attrs={'itemprop':'image'})['content']
            infoLabels['Title']=video.find('meta',attrs={'itemprop':'name'})['content']
            infoLabels['Plot']=video.find('meta',attrs={'itemprop':'description'})['content']
            infoLabels['premiered']=common.formatDate(video.find('meta',attrs={'itemprop':'datePublished'})['content'],'%b %d, %Y')
            seasonEpisode = video.find('div',attrs={'class':'video_meta'}).string.split('|')[0].split('-')
            infoLabels['Season'] = int(seasonEpisode[0].replace('Season','').strip())
            if 'Special' not in seasonEpisode[1]:
                episode = seasonEpisode[1].replace('Episode','').strip()
                if len(episode) > 2:
                    episode = episode[-2:]
                infoLabels['Episode'] = int(episode)
            else:
                infoLabels['Episode'] = 0
            if infoLabels['Season'] <> 0 or infoLabels['Episode'] <> 0:
                displayname = '%sx%s - %s' % (infoLabels['Season'],str(infoLabels['Episode']),infoLabels['Title'])
            else:
                displayname = infoLabels['Title']
            u = sys.argv[0]
            u += '?url="'+urllib.quote_plus(url)+'"'
            u += '&mode="comedy"'
            u += '&sitemode="playurl"'
            common.addVideo(u,displayname,thumb,infoLabels=infoLabels)
        if len(videos) < 5:
            keepGoing=False
        current+=1
    common.setView('episodes')
                
def episodes(url=common.args.url):
    data = common.getURL(url)
    tree = BeautifulSoup(data, convertEntities=BeautifulSoup.HTML_ENTITIES)
    menu = tree.find('ul', attrs={'class': 'more_episode_list'})
    airDatePattern = re.compile(r'([^-]*-[^-]*-[^-]*-[^-]*).*$')
    for item in menu.findAll('li'):
        link = item.find('a')
        url = link['href']
        path = url.rsplit('/', 1)[-1]
        airDate = airDatePattern.match(path).group(1)
        airDate = common.formatDate(airDate, '%a-%B-%d-%Y')
        thumb = item.find('img')['src'].split('?',  1)[0]
        dateSpan = item.find('span', attrs={'class': re.compile('air_date')})
        guestSpan = item.find('span', attrs={'class': 'guest'})
        dateStr = (''.join(dateSpan.findAll(text=True))).encode('utf8')
        guest = guestSpan.string.rstrip('-').strip().encode('utf8')
        if guest:
            name = '%s - %s' % (dateStr.title(), guest)
        else:
            name = dateStr
        if (common.settings['enablestrictnames'] == 'true'):
            print "strict names"
            if guest:
                if not dateSpan.find('span'):
                    displayname='Special Edition - '+guest
                else:
                    displayname=guest
            else:
                displayname='No Guest'
        else:
            displayname=name
        description = item.find('span', attrs={'class': 'details'}).text.encode('utf8')

        u = sys.argv[0]
        u += '?url="'+urllib.quote_plus(url)+'"'
        u += '&mode="comedy"'
        u += '&sitemode="playurl"'
        infoLabels={ "Title":name,
                     "Season":0,
                     "Episode":0,
                     "Plot":description,
                     "premiered":airDate,
                     "TVShowTitle":common.args.name
                     }
        common.addVideo(u,displayname,thumb,infoLabels=infoLabels)
    common.setView('episodes')

def sp_seasons(url=common.args.url):
    for sn in range(1,17):
        sn = str(sn)
        name = 'Season '+sn
        url = sn
        common.addDirectory(name,'comedy','sp_episodes',url)
    common.setView('seasons')

def sp_episodes():
    import demjson
    xbmcplugin.addSortMethod(pluginhandle, xbmcplugin.SORT_METHOD_EPISODE)
    url = 'http://www.southparkstudios.com/feeds/full-episode/carousel/'+common.args.url+'/dc400305-d548-4c30-8f05-0f27dc7e0d5c'
    json = common.getURL(url)
    episodes = demjson.decode(json)['season']['episode']
    for episode in episodes:
        #title = episode['title']
        title = episode['title'].replace(' Part',':Part')
        #replace roan numerals
        title=title.replace('II','2').replace('I','1')
        description = episode['description'].encode('ascii', 'ignore')
        thumbnail = episode['thumbnail'].replace('width=55','')
        episodeid = episode['id']
        senumber = episode['episodenumber']
        date = episode['airdate'].replace('.','-')
        seasonnumber = senumber[:-2]
        episodenumber = senumber[len(seasonnumber):]
        try:
            season = int(seasonnumber)
            episode = int(episodenumber)
        except:
            season = 0
            episode = 0
        u = sys.argv[0]
        u += '?url="'+urllib.quote_plus(episodeid)+'"'
        u += '&mode="comedy"'
        u += '&sitemode="sp_play"'
        infoLabels={ "Title": title,
                    "Season":season,
                    "Episode":episode,
                    "premiered":date,
                    "Plot":description,
                    "TVShowTitle":"South Park"
                    }
        common.addVideo(u,title,thumbnail,infoLabels=infoLabels)
    common.setView('episodes')

def sp_play():
    uri =  'mgid:cms:content:southparkstudios.com:'+common.args.url
    playuri(uri,referer='http://www.southparkstudios.com/full-episodes')

def playuri(uri = common.args.url,referer='http://www.comedycentral.com'):
    mp4_url = "http://mtvnmobile.vo.llnwd.net/kip0/_pxn=0+_pxK=18639+_pxE=/44620/mtvnorigin"
    mtvn = 'http://media.mtvnservices.com/'+uri 
    swfUrl = common.getRedirect(mtvn,referer=referer)
    configurl = urllib.unquote_plus(swfUrl.split('CONFIG_URL=')[1].split('&')[0]).strip()
    configxml = common.getURL(configurl)
    tree=BeautifulStoneSoup(configxml, convertEntities=BeautifulStoneSoup.HTML_ENTITIES)
    mrssurl = tree.find('feed').string.replace('{uri}',uri).replace('&amp;','&')
    mrssxml = common.getURL(mrssurl)
    tree=BeautifulStoneSoup(mrssxml, convertEntities=BeautifulStoneSoup.HTML_ENTITIES)
    segmenturls = tree.findAll('media:content')
    stacked_url = 'stack://'
    for segment in segmenturls:
        surl = segment['url']
        videos = common.getURL(surl)
        videos = BeautifulStoneSoup(videos, convertEntities=BeautifulStoneSoup.HTML_ENTITIES).findAll('rendition')
        hbitrate = -1
        sbitrate = int(common.settings['quality'])
        for video in videos:
            bitrate = int(video['bitrate'])
            if bitrate > hbitrate and bitrate <= sbitrate:
                hbitrate = bitrate
                rtmpdata = video.find('src').string
                if 'viacomspstrm' in rtmpdata:
                    rtmpurl = mp4_url+rtmpdata.split('viacomspstrm')[2]
                elif 'viacomccstrm' in rtmpdata:
                    rtmpurl = mp4_url+rtmpdata.split('viacomccstrm')[2]
                elif 'mtvnorigin' in rtmpdata:
                    rtmpurl = mp4_url+rtmpdata.split('mtvnorigin')[1]
                #app = rtmpdata.split('://')[1].split('/')[1]
                #rtmpdata = rtmpdata.split('/'+app+'/')
                #rtmp = rtmpdata[0]
                #playpath = rtmpdata[1]
                #f '.mp4' in playpath:
                #    playpath = 'mp4:'+playpath.replace('.mp4','')
                #else:
                #    playpath = playpath.replace('.flv','')
                #rtmpurl = rtmp+'/'+app+ ' playpath='+playpath + " swfurl=" + swfUrl.split('?')[0] +" pageUrl=" + referer + " swfvfy=true"
                #print rtmpurl
        stacked_url += rtmpurl.replace(',',',,')+' , '
    stacked_url = stacked_url[:-3]
    item = xbmcgui.ListItem(path=stacked_url)
    xbmcplugin.setResolvedUrl(pluginhandle, True, item)

def playurl(url = common.args.url):
    data=common.getURL(url)
    try:
        uri=re.compile('var url = "http://media.mtvnservices.com/(.+?)";').findall(data)[0]
    except:
        try:
            uri=re.compile('<param name="movie" value="http://media.mtvnservices.com/(.+?)"').findall(data)[0]
        except:
            uri=re.compile('data-mgid="(.+?)"').findall(data)[0]
    playuri(uri,referer=url)
