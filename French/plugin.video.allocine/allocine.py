# -*- coding: utf-8 -*-

# script constants
__plugin__ = "Allocine"
__addonID__ = "plugin.video.allocine"
__authors__ = "Ppic, Fanck, Louis"
__url__ = "http://code.google.com/p/passion-xbmc/"

__useragent__ = "Dalvik/1.6.0 (Linux; U; Android 4.3.1; Amazon Kindle Fire Build/JLS36I)"

import urllib
import urllib2
import re
import os
import time
import xbmcgui
import xbmcplugin
import json
from traceback import print_exc
from hashlib import sha1
from base64 import b64encode
from HTMLParser import HTMLParser
from datetime import date, datetime, timedelta


import xbmcaddon

__settings__ = xbmcaddon.Addon(__addonID__)
AddonPath = __settings__.getAddonInfo('path')

BASE_RESOURCE_PATH = os.path.join(AddonPath, "resources")
sys.path.append(os.path.join(BASE_RESOURCE_PATH, "lib"))

# Import custom libraries
from convert import translate_string
from ordereddict import OrderedDict
from relativedelta import relativedelta

cache_dir = os.path.join(
        xbmc.translatePath(__settings__.getAddonInfo('profile')), "cache")
trailer_dir = __settings__.getSetting("trailer_path")
trailer_dir = xbmc.translatePath(trailer_dir)
dialog = xbmcgui.Dialog()

#print "trailer dir: %s" % trailer_dir

tempfile = os.path.join(cache_dir, "data.html")
if not os.path.isdir(cache_dir):
    os.makedirs(cache_dir)

# Handle quality
qualities = (104001, 104002, 104003, 104004)
__quality__ = qualities[int(__settings__.getSetting("quality"))]

# Handle dates
date_limit = {0: 3, 1: 6, 2: 12, 3: 0}  # months to go back or forth

date_limit_nowshowing = int(__settings__.getSetting("date_limit_nowshowing"))
date_limit_comingsoon = int(__settings__.getSetting("date_limit_comingsoon"))
today = date.today()

__date_limit_nowshowing__ = today - relativedelta(months=date_limit[date_limit_nowshowing])
__date_limit_comingsoon__ = today + relativedelta(months=date_limit[date_limit_comingsoon])

if __settings__.getSetting("skiprerelease") == 'true':
    __skiprerelease__ = True
else:
    __skiprerelease__ = False

# Display release date
if __settings__.getSetting("displayreleasedate") == 'true':
    __displayreleasedate__ = True
else:
    __displayreleasedate__ = False

# Handle title
if __settings__.getSetting("keeporiginaltitle") == 'true':
    __keeporiginaltitle__ = True
else:
    __keeporiginaltitle__ = False

# Class to strip html tags from a string. Useful for displaying clean plots
class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()    

# video types
__video_trailers__ = (31003, 31004, 31016, 31018)
__video_interviews__ = (31007, 31010)
__video_shows__ = (31011,)

# static parameters
__partner_key__ = "100043982026"
__secret_key__ = "29d185d98c984a359e6e6f26a0474269"
__base_url__ = "http://api.allocine.fr/rest/v3/"
__output_format__ = "json"
__media_format__ = "mp4-hip"


def addItem(name):
    ok = True
    liz = xbmcgui.ListItem(name)
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url="",
            listitem=liz)
    return ok
    

def addLink(name, url, iconimage, c_items=None):
    ok = True
    liz = xbmcgui.ListItem(name, iconImage="DefaultVideo.png",
            thumbnailImage=iconimage)
    if c_items:
        liz.addContextMenuItems(c_items, replaceItems=True)
    liz.setInfo(type="Video", infoLabels={"Title": name})
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=url,
            listitem=liz)
    return ok


def addDir(name, url, mode, iconimage, c_items=None, infos=None):
    u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode) + "&name=" + urllib.quote_plus(name)
    ok = True
    liz = xbmcgui.ListItem(name, iconImage="DefaultFolder.png",
            thumbnailImage=iconimage)
    if c_items:
        liz.addContextMenuItems(c_items, replaceItems=True)
    if infos:
        liz.setInfo("video", infos)
    else:
        liz.setInfo("video", {"title": name})
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u,
            listitem=liz, isFolder=True)
    return ok


def end_of_directory(OK):
    xbmcplugin.endOfDirectory(handle=int(sys.argv[1]), succeeded=OK)


def get_params():
    param = []
    paramstring = sys.argv[2]
    if len(paramstring) >= 2:
        params = sys.argv[2]
        cleanedparams = params.replace('?', '')
        if (params[len(params) - 1] == '/'):
            params = params[0: len(params) - 2]
        pairsofparams = cleanedparams.split('&')
        param = {}
        for i in range(len(pairsofparams)):
            splitparams = {}
            splitparams = pairsofparams[i].split('=')
            if (len(splitparams)) == 2:
                param[splitparams[0]] = splitparams[1]
    return param


def save_data(txt, temp=tempfile):
    try:
        if txt:
            file(temp, "w").write(repr(txt))
    except:
        print_exc()
        print "impossible d'enregistrer le fichier %s" % temp


def load_data(file_path):
    try:
        temp_data = eval(file(file_path, "r").read())
    except:
        print_exc()
        print "impossible de charger le fichier %s" % tempfile
        temp_data = ""
    return temp_data


def create_DB(url, dbname):
    DB_file = os.path.join(cache_dir, translate_string("%s.txt" % dbname))
    try:
        save_data(get_film_list(url), DB_file)
    except:
        print "impossible de créer la base %s" % DB_file
        print_exc()


def load_DB(dbname):
    DB_file = os.path.join(cache_dir, translate_string("%s.txt" % dbname))

    if os.path.isfile(DB_file):
        try:
            if time.time() - os.path.getmtime(DB_file) > 3600:
                print "base de plus de 24h, reconstruction..."
                return("")
            data = load_data(DB_file)
        except:
            print "impossible de charger %s" % DB_file
            print_exc()
            data = ""
    else:
        data = ""
    return data

def __get_signed_url(method, query_params):
    # Generate signed url
    # Translated from php code available at https://github.com/gromez/allocine-api
    
    sed = str(time.strftime ('%Y%m%d'))
    
    # urlencode replaces "," by "%2C" but the api does not accept urls like that.
    # So just re-replace the "%2C" by "," after urlencode... damn this api is annoying...
    query_string = urllib.urlencode(query_params).replace("%2C", ",") + "&sed=" + sed

    # Again, put "," a safe character because the api does not accept "%2C"
    sig = urllib.quote(b64encode(sha1(__secret_key__ + query_string).digest()), ',')
    signed_url = __base_url__ + method + '?' + query_string + "&sig=" + sig
    return signed_url

def __getJson(method, query_params):
    "Make url calls to return Json parsed response"

    url = __get_signed_url(method, query_params)
    #print "req url: %s" % url

    req = urllib2.Request(url)
    req.add_header('User-Agent', __useragent__)

    # Api sometimes return 503 error. In that case, wait a bit and try again
    service_available = False
    while not service_available:
        try:
            response = urllib.unquote_plus(urllib2.urlopen(req).read())
            service_available = True
        except HTTPError, e:
            if e.code == 503:
                print "503 for url %s" % url
                time.sleep(0.5)
            else:
                print "%s for url %s" % (e.code, url)
                raise e
    return json.loads(response)


def __getVideo(video):
    # need to sort rendition before the magic can happen
    renditions = sorted(video['rendition'], key=lambda x:x.has_key('bandwidth') and x['bandwidth']['code'], reverse=True)
    # and that's what I love with python
    return max(renditions, key=lambda x:x.has_key('bandwidth') and x['bandwidth']['code'] <= __quality__)


def get_shows_list():
    "Get shows list"
    type_filter = "acshow"
    method = "termlist"
    query_string = OrderedDict([
            ('filter', type_filter),
            ('partner', __partner_key__),
            ('format', __output_format__)
    ])
    result = __getJson(method, query_string)
    return result['feed']['term']


def get_videolist(search):
    "Get show's videos"
    method = "videolist"
    count = 100
    query_string = OrderedDict([
            ('partner', __partner_key__),
            ('filter', search),
            ('format', __output_format__),
            ('mediafmt', __media_format__),
            ('count', count)
    ])

    loop = True
    processed = 0
    while loop:
        result = __getJson(method, query_string)
        if processed + int(result['feed']['count']) >= int(result['feed']['totalResults']):
            # last page
            loop = False
        else:
            processed += result['feed']['count']
            query_string['page'] = int(result['feed']['page']) + 1

        for episode in result['feed']['media']:
            if 'title' in episode:
                video = __getVideo(episode)
                try:
                    thumbnail = episode['thumbnail']['href']
                except KeyError:
                    thumbnail = ''
                addLink(episode['title'].encode('utf8'), video['href'], thumbnail)


def get_movies_list(type_filter, order="datedesc"):
    "Get movies list"

    method = "movielist"
    count = 25
    page = 1

    # Parameters order is important. Api will issue a 403 otherwise
    query_string = OrderedDict([
            ("partner", __partner_key__),
            ("count", count),
            ("filter", type_filter),
            ("page", page),
            ("order", order),
            ("format", __output_format__)
    ])

    if __keeporiginaltitle__:
        title = 'originalTitle'
    else:
        title = 'title'

    loop = True
    while loop:
        #try:
        result = __getJson(method, query_string)
        query_string['page'] = int(result['feed']['page']) + 1
        #except:
        #    loop = False
        #print "Updated: " + result['feed']['updated']

        for movie in result['feed']['movie']:

            #print movie['originalTitle'].encode('utf8')
            if 'trailer' not in movie or 'productionYear' not in movie:
                continue
            if 'release' in movie and __skiprerelease__ and int(movie['productionYear']) < (int(movie['release']['releaseDate'][:4]) - 1):
                    # minus one year to avoid skipping movies produced the year before
                continue
            # elif 'productionYear' in movie and __skiprerelease__ and int(movie['productionYear']) < (int(today[:4]) - 1):
                # continue
            if type_filter == "nowshowing" and __date_limit_nowshowing__ == date.today():
                pass
            elif type_filter == "comingsoon" and __date_limit_comingsoon__ == date.today():
                pass
            else:
                try:
                    releaseDate = datetime(*(time.strptime(movie['release']['releaseDate'], "%Y-%m-%d")[0:6])).date()
                    if type_filter == "nowshowing" and __date_limit_nowshowing__ > releaseDate:
                        loop = False
                        break
                    if type_filter == "comingsoon" and __date_limit_comingsoon__ < releaseDate:
                        loop = False
                        break
                except ValueError:
                    # can't process the date
                    pass
                except KeyError:
                    # no release date to test
                    pass
            try:
                poster = movie['poster']['href']
            except KeyError:
                poster = ""
            if 'release' in movie:
                if __displayreleasedate__:
                    movietitle = "%s - %s " % (movie['release']['releaseDate'].encode('utf8'), movie[title].encode('utf8'))
                else:
                    movietitle = movie[title].encode('utf8')
                infos = {}
                if title in movie:
                    infos['title'] = movie[title].encode('utf8')
                if 'productionYear' in movie:
                    infos['year'] = movie['productionYear']
                if 'statistics' in movie:
                    # Multiply rating by 2 because allocine ratings range 0..5 and xbmc 0..10
                    if 'userRating' in movie['statistics']:
                        infos['rating'] = movie['statistics']['userRating']*2
                        infos['votes'] = str(movie['statistics']['userRatingCount'])
                    elif 'pressRating' in movie['statistics']:
                        infos['rating'] = movie['statistics']['pressRating']*2
                        infos['votes'] = str(movie['statistics']['pressReviewCount'])
                if 'synopsisShort' in movie:
                    infos['plot'] = strip_tags(movie['synopsisShort']).encode('utf-8')
                if 'castingShort' in movie:
                    if 'directors' in movie['castingShort']:
                        infos['director'] = movie['castingShort']['directors'].encode('utf-8')
                    # Cannot get this one to work...
                    if 'actors' in movie['castingShort']:
                        infos['cast'] = movie['castingShort']['actors'].split(', ')
                if 'genre' in movie:
                    try:
                        infos['genre'] = movie['genre'][0]['$'].encode('utf-8')
                    except KeyError:
                        print "Could not find movie genre"
                if 'runtime' in movie:
                    infos['duration'] = "%s" % str(movie['runtime']//60)
                addDir(movietitle, str(movie['code']), 4, poster, None, infos)


def get_movie_videos(code, mode='trailers'):
    "Get trailers list"
    method = "movie"
    type_filter = "movie"
    profile = "large"
    query_string = OrderedDict([
            ('partner', __partner_key__),
            ('code', code),
            ('profile', profile),
            ('mediafmt', __media_format__),
            ('format', __output_format__),
            ('filter', type_filter),
            ('striptags', 'synopsis,synopsisshort')

    ])
    result = __getJson(method, query_string)

    if 'hasShowtime' in result['movie']:
        addDir("Voir les horaires en salles", code, 9, "")

    if 'media' in result['movie']:
        for media in result['movie']['media']:
            if mode == 'trailers':
                interviews = False
                shows = False
                if media['class'] == 'video' and media['type']['code'] in __video_trailers__:
                    try:
                        video = get_video(str(media['code']))
                        addLink(media['title'].encode('utf8'), video['href'], media['thumbnail']['href'])
                    except KeyError:
                        # no rendition key, so not a video after all
                        pass
                elif media['type']['code'] in __video_interviews__:
                    interviews = True
                elif media['type']['code'] in __video_shows__:
                    shows = True
            elif mode == 'interviews':
                if media['type']['code'] in __video_interviews__:
                    video = get_video(str(media['code']))
                    addLink(media['title'].encode('utf8'), video['href'], media['thumbnail']['href'])
            elif mode == 'shows':
                if media['type']['code'] in __video_shows__:
                    video = get_video(str(media['code']))
                    addLink(media['title'].encode('utf8'), video['href'], media['thumbnail']['href'])
    if mode == 'trailers':
        if interviews:
            addDir("Afficher les interviews", code, 5, "")
        if shows:
            addDir("Afficher les émissions", code, 6, "")


def get_movie_theaterslist(code):
    if __settings__.getSetting('zip') and __settings__.getSetting('radius'):
        "Get theaters list"
        method = "showtimelist"
        query_string = OrderedDict([
                ('partner', __partner_key__),
                ('zip', __settings__.getSetting('zip')),
                ('radius', __settings__.getSetting('radius')),
                ('movie', code),
                ('format', __output_format__)

        ])
        result = __getJson(method, query_string)
        
        if 'theaterShowtimes' in result['feed']:
            for theater in result['feed']['theaterShowtimes']:
                params = theater['place']['theater']['code'] + ',' + code
                addDir(theater['place']['theater']['name'].encode('utf8'), params, 10, "")
    else:
        popup = xbmcgui.Dialog().ok("Erreur", "Veuillez paramétrer votre code postal et le rayon de", "recherche dans les réglages du plugin.")


def get_theater_showtimelist(params, mode='versions'):
    "Get showtime list"
    method = "showtimelist"
    query_params = params.split(',')
    query_string = OrderedDict([
            ('partner', __partner_key__),
            ('theaters', query_params[0]),
            ('movie', query_params[1]),
            ('format', __output_format__)

    ])
    result = __getJson(method, query_string)
    
    if 'theaterShowtimes' in result['feed']:
        if mode == 'versions':
            i = 0
            for version in result['feed']['theaterShowtimes'][0]['movieShowtimes']:
                link_version = version['version']['$'] + ', ' + version['screenFormat']['$']
                url = params + ',' + str(i)
                addDir(link_version.encode('utf8'), url, 11, "")
                i += 1
        elif mode == 'days':
                version_number = int(query_params[2])
                i = 0
                for day in result['feed']['theaterShowtimes'][0]['movieShowtimes'][version_number]['scr']:
                    url = params + ',' + str(i)
                    addDir(day['d'].encode('utf8'), url, 12, "")
                    i += 1
        elif mode == 'showtimes':
                version_number = int(query_params[2])
                day_number = int(query_params[3])
                for show in result['feed']['theaterShowtimes'][0]['movieShowtimes'][version_number]['scr'][day_number]['t']:
                    addItem(show['$'].encode('utf8'))


def get_video(code):
    "Get actual video"
    method = "media"
    profile = "large"
    media_format = "mp4"
    query_string = OrderedDict([
            ('partner', __partner_key__),
            ('code', code),
            ('profile', profile),
            ('mediafmt', media_format),
            ('format', __output_format__)
    ])

    result = __getJson(method, query_string)
    return __getVideo(result['media'])


# menu principal:

params = get_params()

url = None
name = None
mode = None

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

print "Mode: " + str(mode)
print "URL: " + str(url)
print "Name: " + str(name)

OK = True

if mode == None or url == None or len(url) < 1:  # menu principal
    addDir('Films Au cinéma - par date de sortie', "nowshowing", 1, "")
    addDir('Films Au cinéma - par nombre de salles', "nowshowing", 2, "")
    addDir('Films - Prochainement', "comingsoon", 3, "")
    addDir("Séries Tv", "tvseries", 7, "")
    addDir("Émissions", "showslist", 8, "")
    addDir("Interviews", "interview", 7, "")


if mode == 1:
    get_movies_list(url, "datedesc")

if mode == 2:
    get_movies_list(url, "theatercount")

if mode == 3:
    get_movies_list(url, "dateasc")

if mode == 4:
    get_movie_videos(url)

if mode == 5:
    get_movie_videos(url, 'interviews')

if mode == 6:
    get_movie_videos(url, 'shows')

if mode == 7:
    get_videolist(url)

if mode == 8:
    shows_list = get_shows_list()
    base_picture = "http://images.allocine.fr/r_120_x/commons/logos/"
    # list pictures which don't match their short names
    picture = {
        "laminute": base_picture + "Logos_minute_160x128.jpg",
        "fauxraccord": base_picture + "Logos_FauxR_160x128.jpg",
        "tueursenseries": base_picture + "Logos_tes_160x128.jpg",
        "direct2dvd": base_picture + "Logos_D2D_160x128.jpg",
        "pleindecine": base_picture + "Logos_p2c_160x128.jpg",
        "lesondecinema": base_picture + "Logos_lsdc_160x128.jpg",   
        "gameincine": base_picture + "Logos_GIC_160x128.jpg",
        "skyfall": base_picture + "vignettesLogosEmissions_skyfall.jpg",
        "hobbittv": base_picture + "Logos_Hobbit_160x128.jpg",
        "nanarland": base_picture + "Logos__nanarland_160x128.jpg",
        "tapisrouge": base_picture + "vignettesLogosEmissions_tapisrouge.jpg",
        "mascenepreferee": base_picture + "Logos_mascene_160x128.jpg",
        "faceaufilm": base_picture + "Logos_faf_160x128.jpg"
    }
    for show in shows_list:
        image = "%smedia%simg%s.jpg" % (BASE_RESOURCE_PATH + os.path.sep, os.path.sep, os.path.sep + show['nameShort'].encode('utf8'))
        if not os.path.exists(image):
            try:
                image = picture["%s" % show['nameShort'].encode('utf8')]
            except KeyError:
                image = base_picture + "Logos_%s_160x128.jpg" % show['nameShort']
        addDir(show['$'].encode('utf8'), 'acshow:' + show['nameShort'], 7, image)

if mode == 9:
    get_movie_theaterslist(url)

if mode == 10:
	get_theater_showtimelist(url)

if mode == 11:
    get_theater_showtimelist(url, 'days')

if mode == 12:
    get_theater_showtimelist(url, 'showtimes')

end_of_directory(OK)
