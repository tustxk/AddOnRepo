'''
    Ice Channel
'''

from entertainment.plugnplay.interfaces import LiveTVIndexer
from entertainment.plugnplay import Plugin
from entertainment import common

class sky_sports_4(LiveTVIndexer):
    implements = [LiveTVIndexer]
    
    display_name = "Sky Sports 4"
    
    name = 'sky_sports_4'
    
    import xbmcaddon
    import os
    addon_id = 'script.icechannel.extn.xunitytalk'
    addon = xbmcaddon.Addon(addon_id)
    img = os.path.join( addon.getAddonInfo('path'), 'resources', 'images', name + '.png' )
    
    regions = [ 
            {
                'name':'United Kingdom', 
                'img':addon.getAddonInfo('icon'), 
                'fanart':addon.getAddonInfo('fanart')
                }, 
        ]
        
    languages = [ 
        {'name':'English', 'img':'', 'fanart':''}, 
        ]
        
    genres = [ 
        {'name':'Sports', 'img':'', 'fanart':''} 
        ]
    
    addon = None
    
