'''
    Ice Channel
'''

from entertainment.plugnplay.interfaces import LiveTVIndexer
from entertainment.plugnplay import Plugin
from entertainment import common

class bt_sport_2(LiveTVIndexer):
    implements = [LiveTVIndexer]
    
    display_name = "BT Sport 2"
    
    name = 'bt_sport_2'
    
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
    
