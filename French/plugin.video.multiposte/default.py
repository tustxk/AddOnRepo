#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Released under GPLv3
"""
Permet de lire les chaînes du fournisseur d'accès Free.fr à l'aide du multiposte
"""
import os, urllib, xbmcplugin, xbmcgui, xbmcaddon, channellist

# plugin handle
HANDLE = int(sys.argv[1])

__settings__ = xbmcaddon.Addon( id="plugin.video.multiposte" )
__language__ = __settings__.getLocalizedString

def show_root_menu():
    """Menu d'accueil"""
    ok = True
    ok = ok and addDirectoryItem(__language__(30201), parameters={"flavour": "radio"})
    ok = ok and addDirectoryItem(__language__(30202), parameters={"flavour": "sd"})
    ok = ok and addDirectoryItem(__language__(30203), parameters={"flavour": "hd"})
    ok = ok and addDirectoryItem(__language__(30204), parameters={"flavour": "ld"})
    xbmcplugin.endOfDirectory(handle=HANDLE, succeeded=ok)
    return ok

def show_flavour_menu(flavour):
    """Choix du canal"""
    print "show_flavour_menu:%s" % flavour
    ok = True
    mychannellist  = channellist.ChannelListReader().get_instance()
    channels = mychannellist.all(flavour=flavour)
    
    if flavour == "radio":
	    # tri par nom
	    print_format = '%(name)s'
	    def cfs(a, b):
		    return cmp(a.name, b.name)
	    channels.sort(cfs)
    else:
	    # tri par numéro de canal
	    print_format = '%(id)s - %(name)s'
	    def cfs(a, b):
		    return cmp(a.id, b.id)
	    channels.sort(cfs)
	    
    for channelflavour in channels:
	    audiotrack = channelflavour.audiotrack
	    if audiotrack == None:
		    audiotrack = ""         
	    ok = ok and addLinkItem(print_format % { "id" : channelflavour.id, "name" : channelflavour.name }, 
				    parameters={"url": channelflavour.url, "audiotrack": audiotrack }
				    )
    xbmcplugin.endOfDirectory(handle=HANDLE, succeeded=ok)
    return True


def play_channelflavour(url, audiotrack):
    """Lecture d'un canal, avec éventuellement un id de piste audio"""
    print "play_channelflavour:%s,%s" % (url, audiotrack)
    play_with_vlc(url, audiotrack)

    return True


def play_with_xbmc(url, audiotrack):
    """Non utilisé puisqu'XBMC ne gère pas les id de piste audio"""
    # WARNING : audiotrack not handled
    player = xbmc.Player()
    player.play(url)
    # player.setAudioStream(audiotrackindex)
    # problem : getAvailableAudioStreams don't give enough information


def play_with_vlc(url, audiotrack):
    """Lecture d'une url en utilisant VLC"""
    if audiotrack == "":
	paramsaudio = ''
    else:
	paramsaudio = '--ts-es-id-pid --audio-track-id %s' % audiotrack

    cmd = __settings__.getSetting('path')
    params = '--one-instance --no-osd --fullscreen -I hotkeys --key-quit Esc --global-key-quit Esc --deinterlace 1 --deinterlace-mode X %s' % paramsaudio

    if (sys.platform == 'win32'):
        # windows
        xbmc.executebuiltin("%s(\"\\\"%s\\\" %s %s\")" % ("System.ExecWait", cmd, params , url))
    elif (sys.platform.startswith('linux')):
        # linux
        url = '"'+url+'"'
        os.system("%s %s %s" % (cmd, params, url))
    else:
        # autre : non géré
        return False

    return True


def parameters_string_to_dict(parameters):
    """Convert parameters encoded in a URL to a dict."""
    param_dict = {}
    if parameters:
        param_pairs = parameters[1:].split("&")
        for params_pair in param_pairs:
            param_splits = params_pair.split('=')
            if (len(param_splits)) == 2:
                param_dict[param_splits[0]] = urllib.unquote(param_splits[1])
    return param_dict

def addDirectoryItem(name, parameters={}, pic=""):
    li = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=pic)
    url = sys.argv[0] + '?' + urllib.urlencode(parameters)
    return xbmcplugin.addDirectoryItem(handle=HANDLE, url=url, listitem=li, isFolder=True)

def addLinkItem(name, parameters=None, pic=""):
    li = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=pic)
    url = sys.argv[0] + '?' + urllib.urlencode(parameters)
    return xbmcplugin.addDirectoryItem(handle=HANDLE, url=url, listitem=li, isFolder=False)

if not sys.argv[2]:
        # new start
        ok = show_root_menu()
else:
	# parameter values
	params = parameters_string_to_dict(sys.argv[2])
        flavour = str(params.get("flavour", ""))
        url = str(params.get("url", ""))
        audiotrack = str(params.get("audiotrack", ""))

        print "url=%s, audiotrack=%s, flavour=%s" % (url, audiotrack, flavour)

        if flavour != "":
                # flavour choosen, now choose channel
                ok = show_flavour_menu(flavour)
        else:
                # play (channel, flavour)
                ok = play_channelflavour(url, audiotrack)

