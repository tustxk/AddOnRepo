'''
    Ice Channel
    buzzfilms.co
'''

from entertainment.plugnplay.interfaces import MovieSource
from entertainment.plugnplay import Plugin
from entertainment import common


class muchmovies(MovieSource):
    implements = [MovieSource]
    
    name = "MuchMovies"
    display_name = "Much Movies"
    base_url = 'http://umovies.me'
    
    source_enabled_by_default = 'true'
    
    def GetFileHosts(self, url, list, lock, message_queue):
        url=url.replace('umovies.me','muchmovies.org')
        self.AddFileHost(list, 'HD', url)
                
    def GetFileHostsForContent(self, title, name, year, season, episode, type, list, lock, message_queue):  
    
        from entertainment.net import Net
        
        net = Net(user_agent='Apple-iPhone/')        
        title = self.CleanTextForSearch(title) 
        name = self.CleanTextForSearch(name) 
        
        search_term = name.replace(' ','-')+'-'+year
        
        import re
        url='http://umovies.me/search/'+search_term
        link=net.http_GET(url).content
        match = re.compile('class="movies list inset">.+?<li><a href="(.+?)">.+?<h.+?>(.+?)</h3>',re.DOTALL).findall(link)
   
        for movie_url, TITLE in match:
            if year in TITLE:
                self.GetFileHosts('http://umovies.me'+movie_url, list, lock, message_queue)
                
            
    def Resolve(self, url):
        
        import re        
        from entertainment.net import Net
        net = Net(user_agent='Apple-iPhone/')
        url=url.replace('muchmovies.org','umovies.me')
        content = net.http_GET(url).content
        content = content.replace('\n','')
        
        link=content.split('href=')
        for p in link:
            if '.mp4' in p:
                resolved_media_url = re.compile('"(.+?)"').findall(p)[0]
                
        return resolved_media_url
            
                
                
