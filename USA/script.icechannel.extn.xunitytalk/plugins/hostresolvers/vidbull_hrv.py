'''
    Ice Channel    
'''

from entertainment import jsunpack
from entertainment.plugnplay.interfaces import HostResolver
from entertainment.plugnplay import Plugin
from entertainment import common
import xbmcgui

import re, xbmcgui



class VidBull(HostResolver):
    implements = [HostResolver]
    name = "vidbull"
    match_list = ['vidbull.com']    

    def Resolve(self, url):
        try:
            from entertainment.net import Net
            net = Net(cached=False)
    
            html = net.http_GET(url,headers={'User-Agent':'Mozilla/5.0 (Linux; Android 4.4; Nexus 5 Build/BuildID) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/30.0.0.0 Mobile Safari/537.36'}).content
            

            match = re.search('<source\s+src="([^"]+)', html)
            if match:
                return match.group(1)
                    
        except Exception, e:
            common.addon.log(self.name.upper() + ' - Exception occured: %s' % e)
            common.addon.show_small_popup('[B][COLOR white]' + self.name.upper() + '[/COLOR][/B]', '[COLOR red]Exception occured, check logs.[/COLOR]')                
            return None

