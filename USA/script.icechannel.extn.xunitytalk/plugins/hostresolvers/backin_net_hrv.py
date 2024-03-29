'''
    backin.net Host resolver
    for Istream ONLY
'''

from entertainment import jsunpack
from entertainment.plugnplay.interfaces import HostResolver
from entertainment.plugnplay import Plugin
from entertainment import common

import xbmcgui

class backin_net(HostResolver):
    implements = [HostResolver]
    name = "Backin.Net"
    resolverName = 'Backin.Net (Resolver)'
    match_list = ['backin.net']

    icon = common.notify_icon

    def Resolve(self, url):
        try:
            dialog = xbmcgui.DialogProgress()
            dialog.create('Resolving', 'Resolving ' + self.name.upper() + ' Link...')
            dialog.update(0)
            
            common.addon.log( self.name.upper() + ' - Link: %s' % url )
            common.addon.show_small_popup('[B][COLOR blue]I[/B][/COLOR]stream: [B][COLOR white]' + self.name.upper() + '[/B][/COLOR]',
                                          'Resolving', 700, self.icon)
                                          
            from entertainment.net import Net
            net = Net(cached=False)
            html = net.http_GET(url).content

            if dialog.iscanceled(): return url
            dialog.update(25)
            
            import re
            
            link = re.search('top.location.href = [\'"](/stream\-.+?)[\'"]', html)
            if not link:
                raise Exception ('Unable to resolve.')
                
            if dialog.iscanceled(): return url
            dialog.update(50)
            
            link = 'http://backin.net' + link.group(1)
            html = net.http_GET(link).content
            
            if dialog.iscanceled(): return url
            dialog.update(75)
            
            playable_url = re.search('<source type=.+?src=[\'"](.+?)[\'"]', html)
            if not playable_url:
                raise Exception ('File not found.__url')
                
            playable_url = playable_url.group(1)
            
            dialog.update(100)
            
            return playable_url

        except Exception, e:
            return_value = None
            ex = '%s' % e
            if ex.endswith('__url'):
                return_value = url
                ex = ex.replace('__url', '')
                
            common.addon.log(self.name.upper() + ' - Exception occured: %s' % e)
            
            if return_value:
                common.addon.show_small_popup('[B][COLOR white]' + self.name.upper() + '[/COLOR][/B]', '[COLOR red]%s[/COLOR]' % ex)                
            else:
                common.addon.show_small_popup('[B][COLOR white]' + self.name.upper() + '[/COLOR][/B]', '[COLOR red]Exception occured, check logs.[/COLOR]')
            
            return return_value
            
