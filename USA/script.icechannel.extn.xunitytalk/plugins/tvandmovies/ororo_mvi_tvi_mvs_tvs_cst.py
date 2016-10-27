'''
    http://ororo.tv/en    
    Copyright (C) 2013 Coolwave
'''

from entertainment.plugnplay.interfaces import MovieIndexer
from entertainment.plugnplay.interfaces import TVShowIndexer
from entertainment.plugnplay.interfaces import MovieSource
from entertainment.plugnplay.interfaces import TVShowSource
from entertainment.plugnplay.interfaces import CustomSettings
from entertainment.plugnplay import Plugin
from entertainment import common
import os
from entertainment.xgoogle.search import GoogleSearch
import xbmc
import xbmcgui
import urllib,urllib2,urlparse,re,datetime,base64,xbmcaddon


class ororo(TVShowSource,CustomSettings):
    implements = [TVShowSource,CustomSettings]
    
    name = "ororo"
    display_name = "Ororo.tv"
    base_url = 'http://ororo.tv/en'
    login_url = 'http://ororo.tv/users/sign_in'
    img=''
    default_indexer_enabled = 'false'
    source_enabled_by_default = 'false'
    cookie_file = os.path.join(common.cookies_path, 'ORlogin.cookie')
    icon = common.notify_icon
    
    
    def __init__(self):
        xml = '<settings>\n'
        xml += '<category label="Account">\n'
        xml += '<setting id="tv_user" type="text" label="Username" default="Username" />\n'
        xml += '<setting id="tv_pwd" type="text" option="hidden" label="Password" default="password" />'
        xml += '</category>\n' 
        xml += '</settings>\n'
        self.CreateSettings(self.name, self.display_name, xml)
          
    
    def GetFileHosts(self, url, list, lock, message_queue):

        import re
        from entertainment.net import Net
        net = Net()
        print url
     
        content = net.http_GET(url).content
        r = "<source src='(.+?)' type='(.+?)'>"
        match  = re.compile(r).findall(content)
        
        for url,res in match:
            url = '%s|Cookie=%s' % (url, urllib.quote_plus('video=true'))
            quality = 'HD'
            if 'video/mp4' in res:
                quality = 'HD'
            else:
                quality = 'SD'
                             
            self.AddFileHost(list, quality, url,'ORORO.TV')
        
        
        
                
    def GetFileHostsForContent(self, title, name, year, season, episode, type, list, lock, message_queue):                 
        
        import re
        from entertainment.net import Net
        
        net = Net(cached=False)
        
        title = self.CleanTextForSearch(title) 
        name = self.CleanTextForSearch(name)
        main_url=self.base_url

        helper = '%s (%s)' %(name,year)
        html = net.http_GET(main_url).content
        #print html.encode('utf-8')    
        
        if type == 'movies':
            url='http://ororo.tv/en/movies'
            html = net.http_GET(url).content
            name_lower = common.CreateIdFromString(name)
            r = '<span class=\'value\'>(\d{4}).*?href="([^"]+)[^>]+>([^<]+)'
            match  = re.compile(r,re.DOTALL).findall(html)
            for item_year,item_url,item_title in match:
                item_title=item_title.lower()
                self.GetFileHosts(item_url, list, lock, message_queue)


        elif type == 'tv_episodes':
            name_lower = common.CreateIdFromString(name)
            name_lower = name_lower.replace('_',' ')
            r = '<span class=\'value\'>(\d{4}).*?href="([^"]+)[^>]+>([^<]+)'
            match  = re.compile(r,re.DOTALL).findall(html)
            for item_year,item_url,item_title in match:
                item_title=item_title.lower()
                print item_title
                if item_title == name_lower and item_year == year:
                    title_url='http://ororo.tv/'+item_url
                    html2 = net.http_GET(title_url).content
                    
                    r = '<a href="#%s-%s" class="episode" data-href="(.+?)" data-id=".+?" data-time=".+?"' % (season, episode)
                    match  = re.compile(r).findall(html2)
                    for item_url in match:
                        item_url='http://ororo.tv/'+item_url

                        self.GetFileHosts(item_url, list, lock, message_queue)
