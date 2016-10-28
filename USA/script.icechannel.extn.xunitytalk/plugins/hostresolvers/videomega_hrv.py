'''
    uptobox Host resolver
    for Istream ONLY
    25/07/2014

    Jas0npc

    Big thanks to all that has guided me on my XBMC Journey.

    A thank you to all members of the Xunity team.

    (c)2014 Xunity.

    This resolver IS NOT OPEN SOURCE, It is to be used as
    part of Istream ONLY.

    version 0.1
'''
from entertainment.plugnplay.interfaces import HostResolver
from entertainment.plugnplay.interfaces import CustomSettings
from entertainment.plugnplay import Plugin
from entertainment import common

import xbmcgui
import xbmc
import os
                    


class videomega(HostResolver, CustomSettings):
    implements = [HostResolver, CustomSettings]
    name = "VideoMega"
    resolverName = name.title()+' (Resolver)'
    match_list = ['videomega.tv']
    version = '0.1'
    profile_path = common.profile_path
    cookie_file = os.path.join(profile_path, 'cookies', '%s.cookies') % name
    puzzle_img = os.path.join(profile_path, 'captchas', '%s.png') % name
    icon = common.notify_icon

    try:
        os.makedirs(os.path.dirname(cookie_file))
    except OSError:
        pass

    def __init__(self):
        xml = '<settings>\n'
        xml += '<category label="">\n'
        xml += '<setting id="version" type="bool" label="'
        xml += '[COLOR blue]Version: '+self.version+'[/COLOR]" />\n'
        xml += '<setting type="sep"/>\n'
        xml += '</category>\n' 
        xml += '</settings>\n'
        self.CreateSettings(self.name, self.resolverName, xml)
    
    def Resolve(self, url):
        import re,urllib,urllib2
        from entertainment.net import Net
        
        
        net = Net(cached=False)
        common.addon.log( self.name.upper() + ' Link: %s' % url )
        common.addon.show_small_popup('[B][COLOR blue]I[/B][/COLOR]stream: [B][COLOR white]' + self.name.upper() + '[/B][/COLOR]',
                                      'Resolving', 700, self.icon)
        try:
            referer = url
            url = 'http://videomega.tv/iframe.php?ref=%s' % url.split('=')[1]
            
            req = urllib2.Request(url,None)
            req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:34.0) Gecko/20100101 Firefox/34.0')
            req.add_header('Referer', referer)
            response = urllib2.urlopen(req)
            link=response.read()
            response.close()
            url = re.compile('document.write.unescape."(.+?)"').findall(link)[-1]
            url = urllib.unquote_plus(url)
            return re.compile('file *: *"(.+?)"').findall(url)[0]
            
        except Exception, e:
            common.addon.log(self.name.upper() + ' - Exception occured: %s' % e)
            common.addon.show_small_popup('[B][COLOR blue]I[/B][/COLOR]stream: [B][COLOR white]' + self.name.upper() + '[/B][/COLOR]', '[COLOR red]'+str(e)+'[/COLOR]', 3000, self.icon)                
            return None
        
                
