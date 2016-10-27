'''
    Cartoon HD Extra   
    Copyright (C) 2013 Mikey1234
'''

from entertainment.plugnplay.interfaces import MovieSource
from entertainment.plugnplay.interfaces import TVShowSource
from entertainment.plugnplay import Plugin
from entertainment import common
import xbmc

class cartoonhdextra(MovieSource,TVShowSource):
    implements = [MovieSource,TVShowSource]
    
    name = "CARTOONEXTRA"
    display_name = "CARTOONEXTRA"
    cartoon = xbmc.translatePath('special://home/userdata/addon_data/script.icechannel/databases/cartoon2')
   
    source_enabled_by_default = 'true'

            
    
    def GetFileHosts(self, url, list, lock, message_queue,type,season,episode):

        EPISODE = "0%s"%episode if len(episode)<2 else episode
        
        first='%sx%s'%(season,EPISODE)
        second='%sE%s'%(season,EPISODE)
  
        import json
        import re
        from entertainment.net import Net
        net = Net(cached=False,user_agent='Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
     
        new_url='http://gearscenter.com/cartoon_control/gapi-ios/index.php?id_select=%s&op_select=films&os=ios&param_10=AIzaSyBsxsynyeeRczZJbxE8tZjnWl_3ALYmODs&param_7=1.0.0&param_8=com.appmovies.gears'% url

        content = net.http_GET(new_url).content
        
        link=json.loads(content)
        
        data=link['films']
        amount=re.compile('"film_link":"(.+?)"').findall(content)
        
        for field in data:
            TITLE= field['film_name'].encode("utf-8")        
            TEST=field['film_link'].encode("utf-8")
            iconimage= field['film_icon'].encode("utf-8")
            test=TEST.split('https://')
            for p in test:
                try:
                    quality =re.compile('#(.+?)#').findall(p)[0]+'p'
                    URL= 'https://'+p.split('#')[0]
                    
                    if type == 'movies':

                        self.AddFileHost(list, quality.upper(), URL,host='CARTOONEXTRA')
                    else:
                        
                        if first in TITLE:

                            self.AddFileHost(list, quality.upper(), URL,host='CARTOONEXTRA')
                        elif second in TITLE:
                            
                            self.AddFileHost(list, quality.upper(), URL,host='CARTOONEXTRA')                            
                except:pass           
        
        
                
    def GetFileHostsForContent(self, title, name, year, season, episode, type, list, lock, message_queue):                 
        
    
        import json
        try:
            content = open(self.cartoon).read()

            link=json.loads(content)
            data=link['categories']        
            for field in data:
                TITLE= field['catalog_name'].encode("utf-8")
                action=field['catalog_id'].encode("utf-8")

                if name in TITLE:
                    if year in TITLE:

                        self.GetFileHosts(action, list, lock, message_queue,type,season,episode)
        except:pass                

    def Resolve(self, url):                 
        

        return url    









            
