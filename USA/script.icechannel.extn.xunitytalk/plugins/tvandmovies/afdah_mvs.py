'''
    http://afdah.com/    
    Copyright (C) 2013 Mikey1234
'''


from entertainment.plugnplay.interfaces import MovieSource
from entertainment.plugnplay import Plugin
from entertainment import common
from entertainment.xgoogle.search import GoogleSearch



class afdah(MovieSource):
    implements = [MovieSource]
    
    name = "afdah"
    display_name = "afdah"
    base_url = 'http://afdah.org/'
    #img=''
    source_enabled_by_default = 'true'
    icon = common.notify_icon
    
        
    def GetFileHosts(self, url, list, lock, message_queue):

        import re
        from entertainment.net import Net
        
        net = Net(user_agent='Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_2 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8H7 Safari/6533.18.5')
                  

        loginurl = 'https://m.afdah.org/video_info/html5'
        
        v=url.split('v=')[1]
        data={'v': v}
        headers = {'host': 'm.afdah.org','origin':'https://m.afdah.org', 'referer': url,
                   'user-agent':'Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_2 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8H7 Safari/6533.18.5','x-requested-with':'XMLHttpRequest'}

        first= net.http_POST(loginurl,data,headers).content

        import json

        link= json.loads(first)

        for j in link:
            quality = j.upper()
            if '360P' in quality:
                quality='SD'
                
            THEURL = 'https://m.afdah.org'+link[j][3]+'**'+url
            self.AddFileHost(list, quality, THEURL,host='GOOGLEVIDEO.COM')
        
        
        
                
    def GetFileHostsForContent(self, title, name, year, season, episode, type, list, lock, message_queue):                 
        
        from entertainment.net import Net

        net = Net(cached=False)
        name = self.CleanTextForSearch(name)

        search_term = name.lower()
        helper_term = ''
        ttl_extrctr = ''

        movie_url = self.GoogleSearchByTitleReturnFirstResultOnlyIfValid(self.base_url, search_term, helper_term, title_extrctr=['(.+?)Full Movie \- AfDah'])

        if movie_url != '':
            movie_url = movie_url.replace('https://afdah.org','http://m.afdah.org')

            self.GetFileHosts(movie_url, list, lock, message_queue)



    def Resolve(self, url):

        v=url.split('**')[1]
        url=url.split('**')[0]

        headers={'dnt':'1','referer': v,
                 'user-agent':'Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_2 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8H7 Safari/6533.18.5','x-requested-with':'XMLHttpRequest'}

        import requests
        import re
        r=requests.get(url, headers=headers,allow_redirects=False)

        match=re.compile("(https\://redirector\.googlevideo.*?)'").findall(str(r.headers))[0]

        r = requests.get(match, headers={'Referer':str(v), 'user-agent':'Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_2 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8H7 Safari/6533.18.5','x-requested-with':'XMLHttpRequest'},
                         allow_redirects=False)

        return r.headers['location']
