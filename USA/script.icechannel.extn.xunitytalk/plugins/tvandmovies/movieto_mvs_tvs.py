'''
    Istream
    Scenelog.org
    Copyright (C) 2013 Coolwave, Jas0npc, the-one, voinage

    version 0.2

'''


from entertainment.plugnplay import Plugin
from entertainment import common
from entertainment.plugnplay.interfaces import MovieSource
from entertainment.plugnplay.interfaces import TVShowSource





class movieto(MovieSource,TVShowSource):
    implements = [MovieSource,TVShowSource]
	
    #unique name of the source
    name = "movie.to"
    source_enabled_by_default = 'true'
    #display name of the source
    display_name = "MovieTo"
    
    #base url of the source website
    base_url = 'http://movietv.to/'

    
    def GetFileHosts(self, url, list, lock, message_queue,ref):

            self.AddFileHost(list, '720P', url+'|'+ref,host='MOVIE.TO')



    def GetFileHostsForContent(self, title, name, year, season, episode, type, list, lock, message_queue):

        import urllib2
        import re
        from entertainment.net import Net

        net = Net(cached=False,user_agent='Mozilla/5.0 (Windows NT 6.1; rv:34.0) Gecko/20100101 Firefox/34.0')
        
        title = self.CleanTextForSearch(title) 
        name = self.CleanTextForSearch(name)


        wait=False
        new_url='http://movietv.to/search?q=%s' %(name.replace(' ','+'))

        
        content=net.http_GET(new_url).content
        
          
        match=re.compile('a href="(.+?)"> (.+?) </a>').findall (content)
        
        for URL , NAME in match:

            if type == 'tv_episodes':
                if name.lower() == NAME.lower():
                       
                        url=URL+'/seasons/'+season
                        print url
                        contents=net.http_GET(url).content
                        
                        link=contents.split('"id"')
                        
                        for p in link:
                            if '"season":'+season in p:
                                if '"episode":'+episode in p:
                                    match=re.compile('"url":"(.+?)"').findall(p)[0]
                                    self.GetFileHosts(match, list, lock, message_queue,URL)
                                    
            else:
                if name.lower() == NAME.lower():
                    
                    contents=net.http_GET(URL).content
                    
                    match=re.compile('"url":"(.+?)"').findall(contents)[0]
                    
                    self.GetFileHosts(match, list, lock, message_queue,URL)

                    

    def Resolve(self, url):
        import re
        import urllib
        
        ref=url.split('|')[1]
        url=url.split('|')[0]
        
        #cookie = match=re.compile('__cfduid=(.+?);').findall(open(self.cookie_file).read())[0]
        
        url += "|Referer="+ref
        return url.replace('\\','')
                                
