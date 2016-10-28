'''
    Ice Channel
    fanstash.eu
'''

from entertainment.plugnplay.interfaces import TVShowSource
from entertainment.xgoogle.search import GoogleSearch

class FanStash(TVShowSource):
    implements = [TVShowSource]
    
    name = "Fan-Stash"
    display_name = "Fan Stash"
    base_url = 'http://www.watch-series-online.li/'
    source_enabled_by_default = 'false'

    
    def GetFileHosts(self, url, list, lock, message_queue):
        from entertainment.net import Net
        import urllib
        import re
        net = Net()

        html = net.http_GET(url,headers={'User-Agent':'Magic-Browser'}).content
        link=re.compile('<strong>(.+?)</strong></td><td><a target="_blank" href="(.+?)" class="play_link').findall(html)
        for host,url in link:
            url='http://www.watch-series-online.li'+url
            if 'strong' in host:
                host='unknown'
            self.AddFileHost(list, 'SD', url, host=host.upper())

    def GetFileHostsForContent(self, title, name, year, season, episode, type, list, lock, message_queue):
        from entertainment.net import Net
        import re
        net = Net()
        
        search_term = '%s Season %s Episode %s'%(self.CleanTextForSearch(name),season,episode)
        url = self.GoogleSearchByTitleReturnFirstResultOnlyIfValid('http://www.watch-series-online.li/', search_term, title_extrctr='watch (.+?) online free')

        if url:
            
            self.GetFileHosts(url, list, lock, message_queue)

    def Resolve(self, url):
        from entertainment.net import Net
        import urllib
        import HTMLParser
        import re
        net = Net()

        html = net.http_GET(url,headers={'User-Agent':'Magic-Browser'}).content
        bits=re.compile("unescape.+?'(.+?)'").findall(html)
        url=urllib.unquote(bits[0]).decode('utf8')        
        from entertainment import istream
        play_url = istream.ResolveUrl(url)
        return play_url
        
        
        '''
        page=re.compile('<td class="current_pagination">.+?</td><td><a href=javascript:Links.+?link_search.+?;>(.+?)</a></td>').findall(html)
        epid=re.compile(r'Episode.+?-(.+?).html').findall(url)
        if page:
            html = net.http_GET('http://www.watch-series-online.li/ajax.php?action=watch_links&epid=%s&cp=%s&mode=ajax&s=&sselect=undefined'%(epid[0],page[0])).content
            link=re.compile('<a target="_blank" href="(.+?)" class="play_link').findall(html)
            print link
            for url in link:
                bits=re.compile("unescape.+?'(.+?)'").findall(net.http_GET('http://www.watch-series-online.li%s'%url).content)
                sources.append(urllib.unquote(bits[0]))
        '''        
        
        
        
            
