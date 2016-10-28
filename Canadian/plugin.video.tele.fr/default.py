#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib, urllib2
import xbmcplugin, xbmcaddon, xbmcgui, xbmc
import sys, os, re, json, base64, operator, datetime, time

pluginhandle = int(sys.argv[1])
addon = xbmcaddon.Addon()
settings = xbmcaddon.Addon( id = "plugin.video.tele.fr" )
domain = base64.b64decode(settings.getSetting("domain"))

def parameters_string_to_dict(parameters):
    paramDict = {}
    if parameters:
        paramPairs = parameters[1:].split("&")
        for paramsPair in paramPairs:
            paramSplits = paramsPair.split('=')
            if (len(paramSplits)) == 2:
                paramDict[paramSplits[0]] = paramSplits[1]
    return paramDict
    
def translation(id):
    return addon.getLocalizedString(id).encode('utf-8','ignore')
    
def get_list(query,data):
    req = urllib2.Request(domain+'api/'+query+'.php')
    f = urllib2.urlopen(req,data)
    html = f.read()
    f.close()
    return html

def info_display(channel_info):
    if ";;;" in channel_info:
        channel_display = ""
        nb_line = 0
        nb_content = int(float(settings.getSetting("nb_epg_program")))
        get_timezone = datetime.datetime.utcnow() - datetime.datetime.now()
        prog_list = channel_info.split(';;;')
        prog_list.pop()
        for prog in prog_list:
            prog_data = prog.split(';;')
            progtime = datetime.datetime.fromtimestamp(time.mktime(time.strptime(prog_data[0],"%Y-%m-%d %H:%M:%S")))
            displaytime = progtime - get_timezone
            if ( displaytime > datetime.datetime.now() ) :
                if ( nb_line < nb_content-1 ):
                    channel_display += displaytime.strftime("%H:%M")+" - "+prog_data[1]+"[CR]"
                    nb_line += 1
            else:
                channel_display = "[B]"+displaytime.strftime("%H:%M")+" - "+prog_data[1]+"[/B][CR]"
        return channel_display.replace("\\", "")
    else:
        return channel_info.replace("\\", "")

def addDir(name, url, mode, iconimage, fanart, desc=""):
    u = sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)
    xbmcplugin.addSortMethod(pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_LABEL)
    ok = True
    liz = xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
    if ( fanart != '' ):
        liz.setProperty("Fanart_Image", fanart)
    liz.setInfo(type="Video", infoLabels={"Title": name, "Plot": desc})
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=True)
    return ok

def categories(mode,url,path,img):
    hide_adult = ( settings.getSetting( "hide_adult" ) == "true" )
    empty_category = ( settings.getSetting( "empty_category" ) == "true" )
    data_list = json.loads(get_list(mode,urllib.urlencode({'hide_adult': hide_adult,'empty_category': empty_category})))
    if (len(data_list) > 0):
        for (category_id, category_info) in data_list.items():
            add_category(category_info[0], category_id, url, domain+'images/'+path+'/'+category_id+'.'+img, domain+'images/channels/'+category_info[3]+'.jpg', category_info[4], category_info[2], category_info[1])
        xbmcplugin.endOfDirectory(pluginhandle)

def add_category(name, url, mode, iconimage, fanart, working, nb_channels, desc=""):
    u = sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)
    xbmcplugin.addSortMethod(pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_LABEL)
    ok = True
    if (working == 0):
        name = name+" | "+translation(30023)
    liz = xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
    if ( fanart != '' ):
        liz.setProperty("Fanart_Image", fanart)
    liz.setInfo(type="Video", infoLabels={"Title": name, "Plot": desc, "Genre": str(nb_channels)+" "+translation(30003)})
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=True)
    return ok

def channels(mode,url):
    hide_adult = ( settings.getSetting( "hide_adult" ) == "true" )
    broken_channel = ( settings.getSetting( "broken_channel" ) == "true" )
    epg_display = ( settings.getSetting( "epg_display" ) == "true" )
    data_list = json.loads(get_list(mode,urllib.urlencode({'content_id': url, 'hide_adult': hide_adult, 'broken_channel': broken_channel, 'epg_display': epg_display})))
    if (len(data_list) > 0):
        sorted_data_list = sorted(data_list.items(), key=lambda k: int(k[0]))
        for (channel_info) in (sorted_data_list):
            add_channel(channel_info[1][0], channel_info[1][2], 'sources', domain+'images/channels/'+channel_info[1][2]+'.png', domain+'images/channels/'+channel_info[1][2]+'.jpg', "", channel_info[1][3], channel_info[1][4], channel_info[1][1])
        xbmcplugin.endOfDirectory(pluginhandle)

def add_channel(name, url, mode, iconimage, fanart, channel_nb, genre, working, desc=""):
    u = sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)
    xbmcplugin.addSortMethod(pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_UNSORTED)
    xbmcplugin.addSortMethod(pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_LABEL)
    ok = True
    if (working == 0):
        name = name+" | "+translation(30023)
    liz = xbmcgui.ListItem(name.replace("\\", ""), iconImage=iconimage, thumbnailImage=iconimage)
    if ( fanart != '' ):
        liz.setProperty("Fanart_Image", fanart)
    liz.setInfo(type="Video", infoLabels={"Title": name.replace("\\", ""), "Plot": info_display(desc), "Genre": genre})
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=False)
    return ok

def sources(mode,url):
    source_list = []
    display_list = []
    broken_stream = ( settings.getSetting( "broken_stream" ) == "true" )
    geo_block = ( settings.getSetting( "geo_block" ) == "true" )
    ext_player = ( settings.getSetting( "ext_player" ) == "true" )
    decay_stream = ( settings.getSetting( "decay_stream" ) == "true" )
    show_domain = ( settings.getSetting( "show_domain" ) == "true" )
    data_list = json.loads(get_list(mode,urllib.urlencode({'channel_id': url, 'broken_stream': broken_stream, 'geo_block': geo_block, 'ext_player': ext_player, 'decay_stream': decay_stream})))
    if (len(data_list) > 0):
        dialog = xbmcgui.Dialog()
        for (source_id, source_info) in sorted(data_list.items(), key=operator.itemgetter(1), reverse=True):
            source_list.append(source_id)
            stream_txt = str(source_info[0])+" px | "+source_info[1].upper()
            if ( show_domain == True ):
                stream_txt = stream_txt+" | "+source_info[7]
            if ( source_info[3] != 'no' ):
                stream_txt = stream_txt+" | "+source_info[3].upper()+" "+translation(30019)
            if ( int(source_info[4]) != 0 ):
                if (int (source_info[4]) > 24):
                    stream_txt = stream_txt+" | +"+str(int(source_info[4])/24)+" "+translation(30024)
                else:
                    stream_txt = stream_txt+" | +"+source_info[4]+" "+translation(30020)
            if ( source_info[5] != 'no' ):
                stream_txt = stream_txt+" | "+translation(30021)
            if ( source_info[2] == 'no' ):
                stream_txt = stream_txt+" | "+translation(30022)
            display_list.append(stream_txt)
            stream_url = source_info[6]
        video_source = dialog.select(translation(30007), display_list)
        if (not video_source == -1 ):
            play_video("play_video", source_list[video_source],stream_url)
                        
def play_video(mode,stream_id,stream_url):
    data_list = json.loads(get_list(mode,urllib.urlencode({'stream_id': stream_id, 'stream_url': stream_url})))
    if (len(data_list) > 0):
        for (stream_id, stream_info) in data_list.items():
            liz = xbmcgui.ListItem(stream_info[1], iconImage=domain+'images/channels/'+stream_info[2]+'.png', thumbnailImage=domain+'images/channels/'+stream_info[2]+'.png')
            xbmc.Player( xbmc.PLAYER_CORE_MPLAYER ).play(base64.b64decode(stream_info[0]),listitem=liz)
                        
params = parameters_string_to_dict(sys.argv[2])
mode = urllib.unquote_plus(params.get('mode', ''))
url = urllib.unquote_plus(params.get('url', ''))
name = urllib.unquote_plus(params.get('name', ''))

if mode == 'play_video':
    play_video(mode,url)
elif mode == 'sources':
    sources(mode,url)
elif mode == 'channel_cont':
    channels(mode,url)
elif mode == 'channel_coun':
    channels(mode,url)
elif mode == 'category':
    categories('category','channel_cont','contents','jpg')
elif mode == 'country':
    categories('country','channel_coun','countries','png')
elif mode == 'channel_all':
    channels('channel_all',"")
else:
    channel_display = ( int(settings.getSetting("category")) )
    if channel_display == 0:
        categories('category','channel_cont','contents','jpg')
    elif channel_display == 1:
        categories('country','channel_coun','countries','png')
    else:
        channels('channel_all',"")
