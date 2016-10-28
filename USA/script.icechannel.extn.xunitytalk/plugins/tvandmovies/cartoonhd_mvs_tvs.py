'''
    Cartoon HD    
    Copyright (C) 2013 Mikey1234
'''

from entertainment.plugnplay.interfaces import MovieSource
from entertainment.plugnplay.interfaces import TVShowSource
from entertainment.plugnplay import Plugin
from entertainment import common


class cartoonhd(MovieSource,TVShowSource):
    implements = [MovieSource,TVShowSource]
    
    name = "Cartoon HD"
    display_name = "Cartoon HD"
    base_url = 'http://cartoonhd.is/'
   
    source_enabled_by_default = 'true'

            
    
    def GetFileHosts(self, url, list, lock, message_queue):

        import re
        from entertainment.net import Net
        net = Net(cached=False,user_agent='Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_2 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8H7 Safari/6533.18.5')
     
     
        content = net.http_GET(url).content
  
        
        if '/season/' in url:
            
                match=re.compile('id="selector(.+?)"><span>(.+?)</span>').findall(content)
        else:
                match=re.compile('id="selector(.+?)"><span><img src=".+?">(.+?)</span>').findall(content)

                
        for id , title in match:

            if '-' in title:
                quality= title.split('-')[1].strip().upper()
                name= title.split('-')[0].strip().upper()
                if '320P' in quality:
                    quality= 'SD'  
            else:
                quality= 'SD'
                name= title.upper()             

            r='''embeds[%s]='<iframe src="''' % id
            FINAL_URL  = content.replace('IFRAME SRC','iframe src').split(r)[1]
            self.AddFileHost(list, quality, FINAL_URL.split('"')[0],host=name)
        
        
        
                
    def GetFileHostsForContent(self, title, name, year, season, episode, type, list, lock, message_queue):                 
        
        from entertainment.net import Net
        import re
        net = Net(cached=False,user_agent='Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_2 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8H7 Safari/6533.18.5')
        name = self.CleanTextForSearch(name)
        import urllib

        token=re.compile("var token.+?'(.+?)'").findall(net.http_GET('http://www.cartoonhd.is').content)[0]
        
        main_url='http://www.cartoonhd.is/ajax/search.php?q=%s&verifiedCheck=%s' %(name.replace(' ','%20'),token)

      
        content=net.http_GET(main_url).content
        

        import json

        link=json.loads(content)
        
        for field in link:
          title=field['title'].strip()
          URL=field['permalink'].strip()
          if name.lower() == title.lower():
              if type == 'tv_episodes':
                name=name.lower()
                item_url = '%s/season/%s/episode/%s' %(URL,season,episode)
              else:
                item_url = URL
                
              self.GetFileHosts(item_url, list, lock, message_queue)
             

    def Resolve(self, url):                 

        
        if 'googleusercontent.com' in url:
            import urllib
            page = urllib.urlopen(url)
            resolved=page.geturl()
            
        elif 'googlevideo.com' in url:
            resolved =url
        else:
        
            from entertainment import istream
            resolved =istream.ResolveUrl(url)
        return resolved    









            
