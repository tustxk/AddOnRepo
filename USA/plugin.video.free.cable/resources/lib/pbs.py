import xbmcplugin
import xbmc
import xbmcgui
import urllib
import urllib2
import sys
import os
import re
import base64

from BeautifulSoup import BeautifulSoup
from BeautifulSoup import BeautifulStoneSoup
#import demjson
import resources.lib._common as common

import coveapi

pluginhandle = int (sys.argv[1])

key='RnJlZUNhYmxlLTgxMzQyMmE5LTg0YWMtNDdjYy1iYzVhLTliMDZhY2NlM2I2YQ=='
secret='MDEyYzcxMDgtNWJiNS00YmFlLWI1MWYtMDRkMTIzNGZjZWRk'

cove = coveapi.connect( base64.b64decode(key), base64.b64decode(secret) )

def masterlist():
    return rootlist(db=True)

def rootlist(db=False):
    start = 0
    count = 200
    db_shows = []
    while start < count:
        data = cove.programs.filter(fields='mediafiles',filter_producer__name='PBS',order_by='title',limit_start=start)
        results = data['results']
        count = data['count']
        stop = data['stop']
        del data
        for result in results:
            if len(result['nola_root'].strip()) != 0:
                program_id = re.compile( '/cove/v1/programs/(.*?)/' ).findall( result['resource_uri'] )[0]
                name = result['title'].encode('utf-8').replace(' Classic','') #remove misleading
                if db==True:
                    db_shows.append((name, 'pbs', 'showroot', program_id))
                else:
                    common.addShow(name, 'pbs', 'showroot', program_id)
        start = stop
    if db==True:
        return db_shows
    else:
        common.setView('tvshows')

def showroot():
   # common.args.show='test'
    common.addDirectory('Full Episodes', 'pbs', 'episodes', common.args.url)
    common.addDirectory('All Videos', 'pbs', 'allvideos', common.args.url)
    common.setView('seasons')
         

def allvideos(program_id=common.args.url):
    show(program_id,True)
    common.setView('episodes')
    
def episodes(program_id=common.args.url):
    show(program_id,False)
    common.setView('episodes')

def show(program_id=common.args.url,clips=False):
    start = 0
    count = 200
    #clips = False
    if clips:
        data = cove.videos.filter(fields='associated_images,mediafiles',filter_program=program_id,order_by='-airdate',filter_availability_status='Available',limit_start=start,exclude_type='Chapter')
    else:
        print "**Episodes**"
        data = cove.videos.filter(fields='associated_images,mediafiles',filter_program=program_id,order_by='-airdate',filter_availability_status='Available',limit_start=start,filter_type='Episode')
    #print "d",data
    #if data['count'] == 0:
    #    clips = True

    videos = data['results']
    total = data['count']
    stop = data['stop']
    for video in videos:
        #print "v",video
        infoLabels={}
        #print video

        if video['mediafiles']: #filter missing streams
            try:thumb=video['associated_images'][2]['url']
            except:thumb=video['associated_images'][0]['url']
            url=video['mediafiles'][0]['video_data_url']
           # print video
            #a bit daft but fixes scraping issues
            title=video['title'].replace(' Hour','').replace('Special | ','').replace('|','').replace(' - ','-') #standarise multipart names
            #print video['slug']
            if 'julia' in video['slug'] and 'with'in title: 
                title=title.split('with ')[1]
                #parts=re.compile('([0-9])').findall(title)
               # if parts:title=title.replace(parts[0],'Pt.'+parts[0])
            if re.compile('Season ([0-9])').match(title):season=re.compile('Season ([0-9])').findall(title)[0]
            else: season=-1
            if re.compile('Episode ([0-9])').match(title):episode=re.compile('Episode ([0-9])').findall(title)[0]
            else: episode=-1
            #if re.compile('.*, [A-Za-z]{3,}.*').match(title) and 'Episode' not in title:
             #   print "found"
              #  numbers=re.compile('([0-9])').findall(title.split(',')[1])
              #  title=title.split(',')[0]
              #  if numbers:
              #      title=title+' '+numbers[0]
            
            #if ':' in video['title']:
             #  title=common.args.showname+':'+video['title']
            infoLabels['Title']=title
            infoLabels['Season']=season
            infoLabels['Episode']=episode
            infoLabels['Plot']=video['long_description']
            infoLabels['Premiered']=video['airdate'].split(' ')[0]
            #infoLabels['TVShowTitle']=common.args.showname
            infoLabels['Duration']=str(int(video['mediafiles'][0]['length_mseconds'])/1000)
            u = sys.argv[0]
            u += '?url="'+urllib.quote_plus(url)+'"'
            u += '&mode="pbs"'
            u += '&sitemode="play"'
            common.addVideo(u,infoLabels['Title'],thumb,infoLabels=infoLabels)
    start = stop
    while start < count:
        if clips:
            data = cove.videos.filter(fields='associated_images,mediafiles',filter_program=program_id,order_by='-airdate',filter_availability_status='Available',limit_start=start,filter_mediafile_set__video_encoding__mime_type='video/mp4')
        else:
            data = cove.videos.filter(fields='associated_images,mediafiles',filter_program=program_id,order_by='-airdate',filter_availability_status='Available',limit_start=start,filter_type='Episode',filter_mediafile_set__video_encoding__mime_type='video/mp4')
        videos = data['results']
        total = data['count']
        stop = data['stop']
        del data
        for video in videos:
            infoLabels={}
            try:thumb=video['associated_images'][2]['url']
            except:thumb=video['associated_images'][0]['url']
            url=video['mediafiles'][0]['video_data_url']
            infoLabels['Title']=video['title'].replace(' Hour','') 
            infoLabels['Plot']=video['long_description']
            infoLabels['Premiered']=video['airdate'].split(' ')[0]
            infoLabels['TVShowTitle']=common.args.name
            infoLabels['Duration']=str(int(video['mediafiles'][0]['length_mseconds'])/1000)
            u = sys.argv[0] 
            u += '?url="'+urllib.quote_plus(url)+'"'
            u += '&mode="pbs"'
            u += '&sitemode="play"'
            common.addVideo(u,infoLabels['Title'],thumb,infoLabels=infoLabels)
        start = stop
    common.setView('episodes')

def play():
    url=common.args.url
    finalurl=common.getRedirect(url)
    #tree=BeautifulStoneSoup(data, convertEntities=BeautifulStoneSoup.HTML_ENTITIES)
    #print tree.prettify()
    #base = tree.find('meta')
    #if base:
     #   base = base['base']
      #  if 'rtmp://' in base:
       #     playpath=tree.find('ref')['src']
        #    if '.mp4' in playpath:
         #       playpath = 'mp4:'+playpath
          #  else:
           #     playpath = playpath.replace('.flv','')
           # finalurl = base+' playpath='+playpath
       # elif 'http://' in base:
        #    playpath=tree.find('ref')['src']
         #   finalurl = base+playpath
    #else:
     #   finalurl=tree.find('ref')['src']
    item = xbmcgui.ListItem(path=finalurl)
    xbmcplugin.setResolvedUrl(pluginhandle, True, item)