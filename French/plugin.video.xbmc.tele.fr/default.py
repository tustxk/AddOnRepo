# -*- coding: utf-8 -*-

import sys, os, time, stat, math, gzip, datetime
import xbmc, xbmcgui, xbmcplugin
import urllib, urllib2, re
import base64,zlib
import socket
import exceptions

import xml.dom.minidom
from xbmcaddon import Addon

# plugin constants
__plugin__ = "XBMC Télé Fr."
__author__ = "Angelscry"
__url__ = "http://sourceforge.net/projects/xbmctlfr/"
__version__ = "1.2.1"

# Parameters

handle = int(sys.argv[1])
PARAMETER_KEY_MODE = "mode"
addon_name = "plugin.video.xbmc.tele.fr"
plugin_data_path = xbmc.translatePath( os.path.join( "special://profile/addon_data", addon_name ) )
if not os.path.exists(plugin_data_path): os.makedirs(plugin_data_path)
base_current_source_path = os.path.join( plugin_data_path , "streams.gz" )
settings = Addon( id = addon_name )
lang = settings.getLocalizedString

# Functions

def language(string):
    return lang(string).encode('utf-8','ignore')

def parameters_string_to_dict(parameters):
    paramDict = {}
    if parameters:
        paramPairs = parameters[1:].split("&amp;")
        for paramsPair in paramPairs:
            paramSplits = paramsPair.split('=')
            if (len(paramSplits)) == 2:
                paramDict[paramSplits[0]] = paramSplits[1]
    return paramDict
 

def xml_decode(url):
    decoded=base64.b64decode(zlib.decompress(base64.b64decode(url)))
    return decoded

def dailymotion_decode(url):
    url_source = ''.join(re.findall('pageUrl=(.*?) live=', url))
    f = urllib.urlopen(url_source)
    for line in f.readlines():
        if '%3Fcell%3Dlive%26auth%3D' in line:
            token_url = ''.join(re.findall('customURL%22%3A%22(.*?)%22%2C%22cdnslb%22', line))
            token_url = urllib.unquote_plus(token_url.replace('%5C',''))
            f2 = urllib.urlopen(token_url)
            for line2 in f2.readlines():
                url = line2+" live=true swfVfy=true timeout=60"
    return url

def url_decode(url):
    url = xml_decode(url)
    # Check if Dailymotion source
    if ( url.find("www.dailymotion.com") > 0 ) :
        url = dailymotion_decode(url)
    return url

def downloadXml():
    xbmc.executebuiltin("XBMC.Notification(%s,%s, 300000)" % (language(30016), language(30017)))
    xbmc.executebuiltin( "ActivateWindow(busydialog)" )
    try:
        xmlfile = urllib2.urlopen("http://www.gwenael.org/xbmc-streams/streams.gz")
        output = open(base_current_source_path,'wb')
        output.write(xmlfile.read())
        output.close()
        xbmc.executebuiltin( "Dialog.Close(busydialog)" )
        xbmc.executebuiltin("XBMC.Notification(%s,%s, 3000)" % (language(30016), language(30018)))
    except socket.timeout:
        xbmc.executebuiltin( "Dialog.Close(busydialog)" )
        xbmc.executebuiltin("XBMC.Notification(%s,%s, 3000)" % (language(30016), language(30019)))
    except exceptions.IOError:
        xbmc.executebuiltin( "Dialog.Close(busydialog)" )
        xbmc.executebuiltin("XBMC.Notification(%s,%s, 3000)" % (language(30016), language(30020)))
    xbmc.executebuiltin("Container.Refresh")

def getXml():
    ok=True
    f = gzip.open(base_current_source_path, 'r')
    xmlSource = f.read().replace('\r','').replace('\n','')
    f.close()
    return xmlSource

def addDirectoryItem(name, thumb, fanart, plot, genre, studio, parameters={}):
    li = xbmcgui.ListItem(name, iconImage=xml_decode(thumb), thumbnailImage=xml_decode(thumb))
    if ( fanart != '' ):
        li.setProperty("Fanart_Image", xml_decode(fanart))
    li.setInfo( type="Video", infoLabels={ "Title": name, "Label": name, "Plot" : plot, "Tagline" : plot, "PlotOutline " : plot,"Genre" : genre , "Studio" : studio } )
    url = sys.argv[0] + '?' + urllib.urlencode(parameters)
    return xbmcplugin.addDirectoryItem(handle=handle, url=url, listitem=li, isFolder=True)

def addLink(name, url, thumb, fanart, plot, genre, studio):
    ok=True
    liz = xbmcgui.ListItem(name, iconImage=xml_decode(thumb), thumbnailImage=xml_decode(thumb))
    liz.setProperty("Fanart_Image", xml_decode(fanart))
    liz.setInfo( type="Video", infoLabels={ "Title": name, "Label": name, "Plot" : plot, "Tagline" : plot, "PlotOutline " : plot, "Genre" : genre , "Studio" : studio } )
    ok=xbmcplugin.addDirectoryItem(handle=handle, url=url_decode(url), listitem=liz, isFolder=False)
    return ok

def get_content(xmlSource,id):
    name = "---"
    xml_content = re.findall( '<contents>(.*?)</contents>', xmlSource )
    contents = re.findall( '<content>(.*?)</content>', xml_content[0] )
    for content in contents:
        content_id = re.findall( '<id>(.*?)</id>', content )
        content_name = re.findall( '<name>(.*?)</name>', content)
        if ( content_id[0] == id ):
            name = content_name[0]
    return name

def get_country(xmlSource,id):
    name = "---"
    xml_country = re.findall( '<countries>(.*?)</countries>', xmlSource )
    countries = re.findall( '<country>(.*?)</country>', xml_country[0] )
    for country in countries:
        country_id = re.findall( '<id>(.*?)</id>', country )
        country_name = re.findall( '<name>(.*?)</name>', country)
        if ( country_id[0] == id ):
            name = country_name[0]
    return name

def get_language(xmlSource,id,value):
    name = "---"
    xml_language = re.findall( '<languages>(.*?)</languages>', xmlSource )
    languages = re.findall( '<language>(.*?)</language>', xml_language[0] )
    for languagee in languages:
        language_id = re.findall( '<id>(.*?)</id>', languagee )
        language_name = re.findall( '<name>(.*?)</name>', languagee )
        language_symbol = re.findall( '<symbol>(.*?)</symbol>', languagee )
        if ( language_id[0] == id ):
            if ( value == 'symbol' ):
                name = language_symbol[0]
            if ( value == 'name' ):
                name = language_name[0]
    return name

def get_categories_list(xmlSource,selected):
    if ( selected == 'content' ) :
        xml_cat = re.findall( '<contents>(.*?)</contents>', xmlSource )
        cat_list = re.findall( '<content>(.*?)</content>', xml_cat[0] )
    if ( selected == 'country' ) :
        xml_cat = re.findall( '<countries>(.*?)</countries>', xmlSource )
        cat_list = re.findall( '<country>(.*?)</country>', xml_cat[0] )
    categories_list = []
    for cat_content in cat_list:
        cate = {}
        cate['id'] = re.findall( '<id>(.*?)</id>', cat_content)
        cate['name'] = re.findall( '<name>(.*?)</name>', cat_content)
        cate['thumb'] = re.findall( '<thumbnail>(.*?)</thumbnail>', cat_content)
        categories_list.append(cate)
    return categories_list

def get_channels_list(xmlSource):
    xml_channels = re.findall( '<channels>(.*?)</channels>', xmlSource )
    channels = re.findall( '<channel>(.*?)</channel>', xml_channels[0] )
    channels_list = []
    for channel in channels:
        chan = {}
        chan['id'] = re.findall( '<id>(.*?)</id>', channel )
        chan['title'] = re.findall( '<title>(.*?)</title>', channel )
        chan['content'] = re.findall( '<content>(.*?)</content>', channel )
        chan['country'] = re.findall( '<country>(.*?)</country>', channel )
        chan['language'] = re.findall( '<language>(.*?)</language>', channel )
        chan['plot'] = re.findall( '<description>(.*?)</description>', channel )
        chan['thumb'] = re.findall( '<thumbnail>(.*?)</thumbnail>', channel )
        chan['fanart'] = re.findall( '<fanart>(.*?)</fanart>', channel )
        chan['epg'] = re.findall( '<epg>(.*?)</epg>', channel )
        chan['active'] = re.findall( '<nb_active_stream>(.*?)</nb_active_stream>', channel )
        channels_list.append(chan)
    return channels_list

def get_streams_list(xmlSource):
    xml_streams = re.findall( '<streams>(.*?)</streams>', xmlSource )
    streams = re.findall( '<stream>(.*?)</stream>', xml_streams[0] )
    streams_list = []
    for stream in streams:
        stre = {}
        stre['channel'] = re.findall( '<channel>(.*?)</channel>', stream )
        stre['url'] = re.findall( '<link>(.*?)</link>', stream )
        stre['active'] = re.findall( '<active>(.*?)</active>', stream )
        stre['quality'] = re.findall( '<quality>(.*?)</quality>', stream )
        stre['format'] = re.findall( '<format>(.*?)</format>', stream )
        streams_list.append(stre)
    return streams_list

def display_epg(epg_txt,nb_content):
    epg_display = ""
    nb_line = 0
    get_timezone = datetime.datetime.utcnow() - datetime.datetime.now()
    prog_list = epg_txt.split(';;;')
    prog_list.pop()
    for prog in prog_list:
        prog_data = prog.split(';;')
        progtime = datetime.datetime.fromtimestamp(time.mktime(time.strptime(prog_data[0],"%Y-%m-%d %H:%M:%S")))
        displaytime = progtime - get_timezone
        if ( displaytime > datetime.datetime.now() ) :
            if ( nb_line < nb_content-1 ):
                epg_display += displaytime.strftime("%H:%M")+" - "+prog_data[1]+"[CR]"
                nb_line += 1
        else:
            epg_display = "[B]"+displaytime.strftime("%H:%M")+" - "+prog_data[1]+"[/B][CR]"
    return epg_display

def show_categories(xmlSource):
    # Get Add-on settings
    show_broken_channel = ( settings.getSetting( "broken_channel" ) == "true" )
    empty_category = ( settings.getSetting( "empty_category" ) == "true" )
    selected = ['content','country'][int(settings.getSetting("category"))]
    # Define sorting method
    xbmcplugin.addSortMethod(handle=int(sys.argv[1]), sortMethod=xbmcplugin.SORT_METHOD_LABEL)
    categories = get_categories_list(xmlSource,selected)
    for category in categories:
        listitem=xbmcgui.ListItem(category['name'][0])
        channels = get_channels_list(xmlSource)
        # Empty categories filtering
        if ( not empty_category ):
            channels = [row for row in channels if row[selected][0] == category['id'][0]]
        # Language filtering filtering
        channels = [row for row in channels if int(row['language'][0]) == 5]
        # Non-active channels filtering
        if ( not show_broken_channel ):
            channels = [row for row in channels if int(row['active'][0]) != 0]
        if ( len(channels) != 0 ):
            addDirectoryItem(category['name'][0], category['thumb'][0], '', '', '', '', parameters={ PARAMETER_KEY_MODE: category['id'][0] })
    xbmcplugin.endOfDirectory(handle=handle, succeeded=True)

def show_channels(xmlSource, category_nb):
    # Get Add-on settings
    selected = ['content','country'][int(settings.getSetting("category"))]
    show_broken_channel = ( settings.getSetting( "broken_channel" ) == "true" )
    multi_sources = ( settings.getSetting( "multi_sources" ) == "true" )
    epg_display = ( settings.getSetting( "epg_display" ) == "true" )
    nb_epg_program = int(float(settings.getSetting("nb_epg_program")))
    channels = get_channels_list(xmlSource)
    # Define sorting method
    xbmcplugin.addSortMethod(handle=int(sys.argv[1]), sortMethod=xbmcplugin.SORT_METHOD_LABEL)
    xbmcplugin.addSortMethod(handle=int(sys.argv[1]), sortMethod=xbmcplugin.SORT_METHOD_UNSORTED)
    # Categories filtering
    channels = [row for row in channels if int(row[selected][0]) == int(category_nb)]
    # Non-active channels filtering
    if ( not show_broken_channel ):
        channels = [row for row in channels if int(row['active'][0]) != 0]
    # Language filtering filtering
    channels = [row for row in channels if int(row['language'][0]) == 5]
    for channel in channels:
        channel_title = channel['title'][0]
        if (( show_broken_channel ) and (int(channel['active'][0]) == 0)):
            channel_title += " (!!)"
        genre_name = get_content(xmlSource,channel['content'][0])
        country_name = get_country(xmlSource,channel['country'][0])
        if ( (channel['epg'][0] != "" ) and (epg_display) ):
            info_display = display_epg(channel['epg'][0],nb_epg_program)
        else:
            info_display = channel['plot'][0]
        fanart_display = channel['fanart'][0]
        # Language filtering filtering
        if ( multi_sources ):
            addDirectoryItem(channel_title, channel['thumb'][0], fanart_display, info_display, genre_name, country_name, parameters={ PARAMETER_KEY_MODE: str(int(channel['id'][0])+1000000) })
        else:
            streams = get_streams_list(xmlSource)
            streams = [row for row in streams if channel['id'][0] == row['channel'][0]]
            streams = [row for row in streams if row['active'][0] != 'no']
            addLink(channel_title, streams[0]['url'][0], channel['thumb'][0], fanart_display, info_display, genre_name, country_name)
    xbmcplugin.endOfDirectory(handle=handle, succeeded=True)

def show_streams(xmlSource, channel_name):
    # Get Add-on settings
    active = ( settings.getSetting( "broken_stream" ) == "true" )
    epg_display = ( settings.getSetting( "epg_display" ) == "true" )
    nb_epg_program = int(float(settings.getSetting("nb_epg_program")))
    # Define sorting method
    streams = get_streams_list(xmlSource)
    streams = [row for row in streams if channel['id'][0] == row['channel'][0]]
    # Active / Inactive streams option
    if ( not active ) :
        streams = [row for row in streams if row['active'][0] != 'no']
    stream_nb = 0
    for stream in streams:
        stream_nb = stream_nb +1
        genre_name = get_content(xmlSource,channel['content'][0])
        country_name = get_country(xmlSource,channel['country'][0])
        if ( (channel['epg'][0] != "" ) and (epg_display) ):
            info_display = display_epg(channel['epg'][0],nb_epg_program)
        else:
            info_display = channel['plot'][0]
        fanart_display = channel['fanart'][0]
        stream_name = "Source #"+str(stream_nb)
        stream_name += " - "+language(30023)+" "+str.upper(stream['quality'][0])+" - "+language(30024)+" "+str.upper(stream['format'][0])
        if ( stream['active'][0] == 'no' ) :
            stream_name += " ( !! )"
        addLink(stream_name, stream['url'][0], channel['thumb'][0], fanart_display, info_display, genre_name, country_name)
    xbmcplugin.endOfDirectory(handle=handle, succeeded=True)

# Start Script

params = parameters_string_to_dict(sys.argv[2])
mode = int(params.get(PARAMETER_KEY_MODE, "0"))
if ( not os.path.exists(base_current_source_path) ) : downloadXml()
xml_source = getXml()

if mode==2000000:
    downloadXml()

if not sys.argv[2]:
    if ( (time.time()-os.path.getmtime(base_current_source_path)) >= 7200 ) : downloadXml()
    ok = show_categories(xml_source)
else :
    categories = get_categories_list(xml_source,['content','country'][int(settings.getSetting("category"))])
    channels = get_channels_list(xml_source)
    for category in categories:
        if mode == int(category['id'][0]):
            ok = show_channels(xml_source,mode)

    for channel in channels:
        if mode == 1000000+int(channel['id'][0]):
            ok = show_streams(xml_source,mode)
