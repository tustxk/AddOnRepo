'''
    Vidspot Host resolver
    for Istream ONLY
    17/01/2014

    Jas0npc, the-one

    A thank you to all members of the Xunity team.

    (c)2014 Xunity.

    This resolver IS NOT OPEN SOURCE, It is to be used as
    part of Istream ONLY.

    version 0.1
'''
from entertainment import jsunpack
from entertainment.plugnplay.interfaces import HostResolver
from entertainment.plugnplay import Plugin
from entertainment import common
          


class Vidspot(HostResolver):
    implements = [HostResolver]
    name = "Vidspot"
    match_list = ['vidspot.net']

    icon = common.notify_icon

    
    def Resolve(self, url):
        from entertainment.net import Net
        import re
        net = Net(cached=False,user_agent='Apple-iPhone/')

        
        if 'embed' in url:
            url=url
        else:    
            fileid = re.search(r'net\/([a-zA-Z0-9]+)', url, re.I)

            if fileid:
                url = 'http://vidspot.net/'+fileid.group(1)+'-650x360.html'
        
        common.addon.log( self.name.upper() + ' - Link: %s' % url )
        common.addon.show_small_popup('[B][COLOR blue]I[/B][/COLOR]stream: [B][COLOR white]' + self.name.upper() + '[/B][/COLOR]',
                                      'Resolving', 700, self.icon)


        try:
            
            r = net.http_GET(url).content

            match= re.compile('"file" : "(.+?)"').findall(r)
            

            if not match:
                raise Exception ('Video Not Found.')
            
            if match:
                qbest=len(match)-1
                return match[qbest]+'&direct=false&ua=true'
                

        except Exception, e:
            common.addon.log(self.name.upper() + ' - Exception occured: %s' % e)
            common.addon.show_small_popup('[B][COLOR blue]I[/B][/COLOR]stream: [B][COLOR white]' + self.name.upper() + '[/B][/COLOR]', '[COLOR red]'+str(e)+'[/COLOR]', 700, self.icon)                
            return None
