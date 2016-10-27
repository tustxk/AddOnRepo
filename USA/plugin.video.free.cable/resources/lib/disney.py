#!/usr/bin/python
# -*- coding: utf-8 -*
import xbmcplugin
import xbmc
import xbmcgui
import os
import re
import sys
from BeautifulSoup import BeautifulStoneSoup
import resources.lib._common as common
import resources.lib.m3u8 as m3u8

pluginHandle = int(sys.argv[1])

BRANDID = '004'
PARTNERID = '585231'
SITE = 'disney'
SHOWLIST = 'http://abc.go.com/vp2/ws/s/contents/2012/shows/' + BRANDID + '/001/-1?rand=2.0.0000'
VIDEOLIST = 'http://abc.go.com/vp2/ws/s/contents/2012/videos/' + BRANDID + '/001/'
PLAYLISTMOV = 'http://www.kaltura.com/p/' + PARTNERID + '/sp/' + PARTNERID + '00/playManifest/format/rtmp/entryId/'
PLAYLISTMP4 = 'http://www.kaltura.com/p/' + PARTNERID + '/sp/' + PARTNERID + '00/playManifest/format/applehttp/entryId/'
PLAYLISTULNK = 'http://www.kaltura.com/p/' + PARTNERID + '/sp/' + PARTNERID + '00/playManifest/format/http/entryId/'
CLOSEDCAPTIONHOST = 'http://cdn.video.abc.com'

def masterlist():
    master_db = []
    master_data = common.getURL(SHOWLIST)
    master_tree = BeautifulStoneSoup(master_data, convertEntities=BeautifulStoneSoup.XML_ENTITIES)
    master_menu = master_tree.findAll('show')
    for master_item in master_menu:
        master_name = master_item('title')[0].string
        season_id = master_item['id']
        master_db.append((master_name, SITE,'seasons',season_id))
    return master_db

def rootlist():
    root_data = common.getURL(SHOWLIST)
    root_tree = BeautifulStoneSoup(root_data, convertEntities=BeautifulStoneSoup.XML_ENTITIES)
    root_menu = root_tree.findAll('show')
    for root_item in root_menu:
        root_name = root_item('title')[0].string
        season_id = root_item['id']
        common.addShow(root_name, SITE,'seasons',season_id)
    common.setView('tvshows')

def seasons(url=common.args.url):
    show_id = url
    show_url = VIDEOLIST + 'lf/' + show_id + '/-1/-1/-1/-1?rand=2.0.0000'
    show_data = common.getURL(show_url)
    show_menu = sorted(set(re.findall(r'<season id\=\"(.+?)\"',show_data)))
    for show_item in show_menu:
        show_name = 'Season ' + show_item
        show_url = VIDEOLIST + 'lf/' + show_id + '/' + show_item + '/-1/-1/-1?rand=2.0.0000'
        common.addDirectory(show_name, SITE, 'episodes', show_url)
    clip_id = url
    clip_url = VIDEOLIST + 'sf/' + show_id + '/-1/-1/-1/-1?rand=2.0.0000'
    clip_data = common.getURL(clip_url)
    clip_menu = sorted(set(re.findall(r'<season id\=\"(.+?)\"',clip_data)))
    for clip_item in clip_menu:
        clip_name = 'Clips Season ' + clip_item
        clip_url = VIDEOLIST + 'sf/' + clip_id + '/' + clip_item + '/-1/-1/-1?rand=2.0.0000'
        common.addDirectory(clip_name, SITE, 'episodes', clip_url)
    common.setView('seasons')

def episodes(url=common.args.url):
    episode_data = common.getURL(url)
    episode_tree = BeautifulStoneSoup(episode_data, convertEntities=BeautifulStoneSoup.XML_ENTITIES)
    episode_menu = episode_tree.findAll('video')
    for episode_item in episode_menu:
        episode_name = episode_item('title')[1].string
        try:
            episode_thumb = episode_item('thumbnails')[1]('thumbnail')[1].string
        except:
            try:
                episode_thumb = episode_item('thumbnails')[1]('thumbnail')[0].string
            except:
                episode_thumb = episode_item('thumbnail')[0].string
        if (episode_item('asset')[0]['format'] == 'MOV'):
            sitemode = 'playVideoMOV'
        elif (episode_item('asset')[0]['format'] == 'MP4'):
            sitemode = 'playVideoMP4'
        else:
            sitemode = 'playVideoULNK'
        url = episode_item['id'].replace('VDKA', '')
        try:
            episode_description = episode_item('longdescription')[0].string
        except:
            episode_description = episode_item('description')[0].string
        try:
            closedcaption = episode_item('closedcaption')[0]('src')[0].string
            closedcaption = CLOSEDCAPTIONHOST + closedcaption.split('.com')[1]
        except:
            closedcaption = 'false'
        episode_airDate = re.sub(r" P(.)T","",episode_item('airdate')[0].string)
        episode_duration = int(episode_item('duration')[0].string)/60000
        episode_number = episode_item('number')[0].string
        season_number = episode_item('season')[0]['id']
        u = sys.argv[0]
        u += '?url="' + url + '#' + closedcaption + '"'
        u += '&mode="' + SITE + '"'
        u += '&sitemode="' + sitemode + '"'
        infoLabels={ "Title":episode_name,
                     "Plot":episode_description,
                     "premiered":common.formatDate(episode_airDate,'%a, %d %b %Y %H:%M:%S','%d.%m.%Y'),
                     "Duration":episode_duration,
                     "Episode":episode_number,
                     "Season":season_number
                   }
        common.addVideo(u,episode_name,episode_thumb,infoLabels=infoLabels)
    common.setView('episodes')

def playVideoMOV(url=common.args.url):
    video_id = url.split('#')[0]
    closedcaption = url.split('#')[1]
    if (common.settings['enablesubtitles'] == 'true'):
        if (closedcaption != 'false'):
            convert_subtitles(closedcaption)
    hbitrate = -1
    sbitrate = int(common.settings['quality'])
    video_url = PLAYLISTMOV + video_id
    video_data = common.getURL(video_url)
    video_tree = BeautifulStoneSoup(video_data, convertEntities=BeautifulStoneSoup.XML_ENTITIES)
    base_url = video_tree('baseurl')[0].string
    video_url2 = video_tree.findAll('media')
    for video_index in video_url2:
        bitrate = int(video_index['bitrate'])
        if bitrate > hbitrate and bitrate <= sbitrate:
            hbitrate = bitrate
            playpath_url = video_index['url']
    swf_url = 'http://livepassdl.conviva.com/ver/2.61.0.65970/LivePassModuleMain.swf'
    finalurl = base_url + ' playpath=' + playpath_url + ' swfUrl=' + swf_url + ' swfVfy=true'
    xbmcplugin.setResolvedUrl(pluginHandle, True, xbmcgui.ListItem(path = finalurl))
    if (common.settings['enablesubtitles'] == 'true') and (closedcaption != 'false'):
        while not xbmc.Player().isPlaying():
            xbmc.sleep(100)
        subtitles = os.path.join(common.pluginpath,'resources','cache','subtitle.srt')
        xbmc.Player().setSubtitles(subtitles)

def playVideoMP4(url=common.args.url):
    video_id = url.split('#')[0]
    closedcaption = url.split('#')[1]
    if (common.settings['enablesubtitles'] == 'true'):
        if (closedcaption != 'false'):
            convert_subtitles(closedcaption)
    hbitrate = -1
    sbitrate = int(common.settings['quality'])
    video_url = PLAYLISTMP4 + video_id
    video_data = common.getURL(video_url)
    video_url2 = m3u8.parse(video_data)
    for video_index in video_url2.get('playlists'):
        bitrate = int(video_index.get('stream_info')['bandwidth'])
        if bitrate > hbitrate and bitrate <= (sbitrate * 1000):
            hbitrate = bitrate
            finalurl = video_index.get('uri')
    xbmcplugin.setResolvedUrl(pluginHandle, True, xbmcgui.ListItem(path=finalurl))
    if (common.settings['enablesubtitles'] == 'true') and (closedcaption != 'false'):
        while not xbmc.Player().isPlaying():
            xbmc.sleep(100)
        subtitles = os.path.join(common.pluginpath,'resources','cache','subtitle.srt')
        xbmc.Player().setSubtitles(subtitles)

def playVideoULNK(url=common.args.url):
    video_id = url.split('#')[0]
    closedcaption = url.split('#')[1]
    if (common.settings['enablesubtitles'] == 'true'):
        if (closedcaption != 'false'):
            convert_subtitles(closedcaption)
    hbitrate = -1
    sbitrate = int(common.settings['quality'])
    video_url = PLAYLISTULNK + video_id + '/a.f4m?playbackContext=brand%3D' + BRANDID + '%26device%3D001'
    video_data = common.getURL(video_url)
    video_tree = BeautifulStoneSoup(video_data, convertEntities=BeautifulStoneSoup.XML_ENTITIES)
    video_url2 = video_tree.find('media')['url']
    video_data2 = common.getURL(video_url2)
    video_url3 = m3u8.parse(video_data2)
    for video_index in video_url3.get('playlists'):
        bitrate = int(video_index.get('stream_info')['bandwidth'])
        if bitrate > hbitrate and bitrate <= (sbitrate * 1000):
            hbitrate = bitrate
            video_url4 = video_index.get('uri')
    video_data3 = re.sub(r"\#EXT-X-DISCONTINUITY\n","",common.getURL(video_url4))
    file = open(os.path.join(common.pluginpath,'resources','cache','play.m3u8'), 'w')
    file.write(video_data3)
    file.close()
    finalurl = os.path.join(common.pluginpath,'resources','cache','play.m3u8')
    xbmcplugin.setResolvedUrl(pluginHandle, True, xbmcgui.ListItem(path=finalurl))
    if (common.settings['enablesubtitles'] == 'true') and (closedcaption != 'false'):
        while not xbmc.Player().isPlaying():
            xbmc.sleep(100)
        subtitles = os.path.join(common.pluginpath,'resources','cache','subtitle.srt')
        xbmc.Player().setSubtitles(subtitles)

def clean_subs(data):
    br = re.compile(r'<br.*?>')
    br_2 = re.compile(r'\n')
    tag = re.compile(r'<.*?>')
    space = re.compile(r'\s\s\s+')
    sub = br.sub('\n', str(data))
    sub = tag.sub(' ', sub)
    sub = br_2.sub('<br/>', sub)
    sub = space.sub(' ', sub)
    return sub

def convert_subtitles(xml_closedcaption):
    subtitle_array = []
    str_output = ''
    subtitle_data = common.getURL(xml_closedcaption)
    subtitle_data = BeautifulStoneSoup(subtitle_data, convertEntities=BeautifulStoneSoup.XML_ENTITIES)
    lines = subtitle_data.findAll('p')
    for i, line in enumerate(lines):
        if line is not None:
            sub = clean_subs(line).decode('utf-8').encode('utf-8', 'ignore')
            try:
                newsub = sub
                sub = BeautifulStoneSoup(sub, convertEntities=BeautifulStoneSoup.ALL_ENTITIES)
            except:
                sub = newsub
            start_time_hours, start_time_rest = line['begin'].split(':',1)
            start_time_hours = '%02d' % (int(start_time_hours) - 1)
            start_time = start_time_hours + ':' + start_time_rest.replace('.',',')
            end_time_hours, end_time_rest = line['end'].split(':',1)
            end_time_hours = '%02d' % (int(end_time_hours) - 1)
            end_time = end_time_hours + ':' + end_time_rest.replace('.',',')
            str_output += str(i+1) + '\n' + str(start_time) + ' --> ' + str(end_time) + '\n' + str(sub) + '\n\n'
    file = open(os.path.join(common.pluginpath,'resources','cache','subtitle.srt'), 'w')
    file.write(str_output)
    file.close()
    return True