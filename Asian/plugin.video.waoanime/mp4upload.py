"""
    urlresolver XBMC Addon
    Copyright (C) 2014 TheHighway

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
from t0mm0.common.net import Net
from urlresolver.plugnplay.interfaces import UrlResolver
from urlresolver.plugnplay.interfaces import PluginSettings
from urlresolver.plugnplay import Plugin
from urlresolver import common
import urllib,urllib2,re,time

class MyLittleResolver(Plugin,UrlResolver,PluginSettings):
    implements=[UrlResolver,PluginSettings]; name="mp4upload.com"; 
    def __init__(self):
        p=self.get_setting('priority') or 100
        self.net=Net(); self.priority=int(p); 
        self.pattern ='http://((?:www.)?mp4upload.com)/([0-9a-zA-Z\-_]+)*'; ## http://www.mp4upload.com/[id]
        self.pattern2='http://((?:www.)?mp4upload.com)/embed-([0-9a-zA-Z\-_]+)\.html'; ## http://www.mp4upload.com/embed-[id].html
    def get_url(self, host, media_id): 
    	common.addon.log(media_id); 
    	return 'http://www.mp4upload.com/embed-%s.html' % (media_id) #&w=800&h=600
    def get_host_and_id(self, url):
        if ('/embed-' in url) and ('.html' in url): r = re.search(self.pattern2, url)
        else: r = re.search(self.pattern, url)
        if r: return r.groups()
        else: return False
    def valid_url(self,url,host):
        if self.get_setting('enabled')=='false': return False
        return re.match(self.pattern2,url) or re.match(self.pattern,url) or self.name in host
    def get_media_url(self,host,media_id):
        hostname=self.name; web_url=self.get_url(host,media_id); 
        common.addon.log(web_url); 
        try: resp=self.net.http_GET(web_url); html=resp.content; 
        except urllib2.URLError, e: common.addon.log_error(hostname+': got http error %d fetching %s' % (e.code, web_url)); return self.unresolvable(code=3, msg='Exception: %s' % e);
        #time.sleep(2)
        r=re.search("'file'\s*:\s*'(.+?)'", html); 
        if r: 
            common.addon.log(r.group(1)); 
            stream_url=urllib.unquote_plus(r.group(1)); 
        else:
            r=re.search("file\s*:\s*'(.+?)'", html); 
            if r: 
                common.addon.log(r.group(1)); 
                stream_url=urllib.unquote_plus(r.group(1)); 
            else:
                r=re.search('<source src="(.+?)"', html); 
                if r: stream_url=urllib.unquote_plus(r.group(1)); 
                else: common.addon.log_error(hostname+': stream url not found'); return self.unresolvable(code=0, msg='no file located'); 
        return stream_url
	