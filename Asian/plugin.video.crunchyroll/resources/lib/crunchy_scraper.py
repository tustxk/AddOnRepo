import sys
import os
import xbmc
import xbmcgui
import urllib
import urllib2
import StringIO
import gzip
import re
import datetime
import crunchy_main
from BeautifulSoup import BeautifulSoup

__settings__ = sys.modules[ "__main__" ].__settings__

class _Info:
	
	def __init__( self, *args, **kwargs ):
		self.__dict__.update( kwargs )
        
class CrunchyParser:

	pattern_episode_id = re.compile('[0-9]{6}')
	
	def __init__(self):
		self.settings = {}
		self.settings['thumb_quality'] = int(__settings__.getSetting("thumb_quality"))
		print "CRUNCHY: --> Thumb Quality: " + str(self.settings['thumb_quality'])
		thumb_quality = ['_thumb', '_large', '_full']
		self.settings['thumb_quality'] = thumb_quality[self.settings['thumb_quality']]
	
	def parseSeries(self, feed, cat):
		info = []
		soup = BeautifulSoup(feed)
		series_list = soup.findAll('item')
		num_series = len(series_list)
		for series in series_list:
			item = {}
			item['name'] = series.title.string.encode('utf-8')
			item['description'] = series.description.string.encode('utf-8')
			item['img'] = series.find('boxee:property').string.replace("_large",self.settings['thumb_quality'])
			item['page_url'] = series.guid.string
			print item['page_url']
			temp = item['page_url'].split(".com/")
			print "\n\n"
			print temp
			item['id'] = temp[1]
			crunchy_main.UI().addItem({'Title':item['name'], 'mode':'series', 'Thumb':item['img'], 'id':item['id'], 'page_url':item['page_url'], 'plot':item['description']}, True, num_series)
		crunchy_main.UI().endofdirectory('none')

	def parseEpisodes(self, feed):
		info = []
		print "CRUNCHY: Parsing episodes..."
		soup = BeautifulSoup(feed)
		episode_list = soup.findAll('item')
		num_episodes = len(episode_list)
		for episode in episode_list:
			item = {}
			item['name'] = episode.title.string.encode('utf-8')
			item['series_name'] = episode.find('boxee:property', attrs={'name':'custom:seriesname'}).string.encode('utf-8')
			item['ordernum'] = ''
			item['description'] = unicode(episode.description.string).encode('utf-8')
			item['img'] = episode.find('media:thumbnail')['url'].replace("_large",self.settings['thumb_quality'])
			item['page_url'] = episode.guid.string.encode('utf-8')
			ep_number = episode.find('boxee:property', attrs={'name':'custom:episodenum'})
			if ep_number:
				item['ordernum'] = ep_number.string.encode('utf-8')
			else:
				item['ordernum'] = None
			resolutions = episode.find('boxee:property', attrs={'name':'custom:available_resolutions'})
			if resolutions.string:
				item['resolutions'] = resolutions.string
			else:
				item['resolutions'] = '12,20,21'
			ep_id = self.pattern_episode_id.search(item['page_url'])
			ep_id = ep_id.group()
			item['ep_id'] = ep_id
			crunchy_main.UI().addItem({'Title':item['series_name']+' - '+item['name'], 'mode':'episode', 'Thumb':item['img'], 'id':item['ep_id'], 'page_url':item['page_url'], 'plot':item['description'], 'resolutions':item['resolutions']}, True, num_episodes)
		crunchy_main.UI().endofdirectory('none')

class CrunchyScraper:
	
	def __init__(self):
		self.base_path = os.path.join(xbmc.translatePath("special://masterprofile/"), "addon_data", os.path.basename(os.getcwd()))
		self.base_cache_path = os.path.join(self.base_path, "cache")
		if not os.path.exists(self.base_cache_path):
			os.makedirs(self.base_cache_path)
		self.episodes_list = []
		
	def getSeriesListing(self, cat='anime', subcat=None):
		if subcat:
			subcat = subcat.replace('_','%20')
			url = "http://www.crunchyroll.com/boxee_feeds/"+ cat +"/"+ subcat
		else:
			url = "http://www.crunchyroll.com/boxee_feeds/"+ cat
		file_path = os.path.join(self.base_cache_path, cat +".rss")
		refreshRSS = self.check_cache_time(file_path)
		if(os.path.exists(file_path) and refreshRSS is False):
			usock = open(file_path, "r")
			rssFeed = usock.read()
		else:
			opener = urllib2.build_opener()
			opener.addheaders = [('User-Agent','curl/7.16.3 (Windows  build 7600; en-US; beta) boxee/0.9.21.12594'),('Accept-Encoding','deflate, gzip'),('Accept-Charset','ISO-8859-1,utf-8;q=0.7,*;q=0.7'),('Accept-Language','en-us,en;q=0.5')]
			usock = opener.open(url)
			rssFeed = usock.read()
			if usock.headers.get('content-encoding', None) == 'gzip':
				rssFeed = gzip.GzipFile(fileobj=StringIO.StringIO(rssFeed)).read()
		usock.close()
		if (not os.path.exists(file_path)):
			file_object = open(file_path, "w")
			file_object.write(rssFeed)
			file_object.close()
		CrunchyParser().parseSeries(rssFeed, cat)
		
	def getEpisodeListing(self, id, url=None):
		print id
		full_url = "http://www.crunchyroll.com/boxee_feeds/showseries/"+str(id)
		if url:
			full_url = url
		file_path = os.path.join(self.base_cache_path, id+".rss")
		refreshRSS = self.check_cache_time(file_path)
		if(os.path.exists(file_path) and refreshRSS is False):
			usock = open(file_path, "r")
			rssFeed = usock.read()
		else:
			opener = urllib2.build_opener()
			opener.addheaders = [('User-Agent','curl/7.16.3 (Windows  build 7600; en-US; beta) boxee/0.9.21.12594'),('Accept-Encoding','deflate, gzip'),('Accept-Charset','ISO-8859-1,utf-8;q=0.7,*;q=0.7'),('Accept-Language','en-us,en;q=0.5')]
			usock = opener.open(full_url)
			rssFeed = usock.read()
			if usock.headers.get('content-encoding', None) == 'gzip':
				rssFeed = gzip.GzipFile(fileobj=StringIO.StringIO(rssFeed)).read().decode('utf-8','ignore')
		usock.close()
		if (not os.path.exists(file_path)):
			file_object = open(file_path, "w")
			file_object.write(rssFeed.encode('utf-8'))
			file_object.close()
		CrunchyParser().parseEpisodes(rssFeed)
		
	def getImages(self, url, file_path):
		file_path += ".jpg"
		full_path = os.path.join(self.base_cache_path, file_path)
		try:
			if(url):
				if(not os.path.exists(full_path) and url != ""):
					urllib.urlretrieve( url, full_path )
				img_path = full_path
				return img_path
		except:
			urllib.urlcleanup()
			remove_tries = 3
			while remove_tries and os.path.isfile(full_path):
				try:
					os.remove(full_path)
				except:
					remove_tries -=1
					xbmc.sleep(1000)
					
			
	def check_cache_time(self, filename):
		if os.path.exists(filename):
			mod_time = datetime.datetime.fromtimestamp(os.path.getmtime(filename))
			cur_time = datetime.datetime.now()
			elapsed = cur_time - mod_time
			if(elapsed > datetime.timedelta(minutes=60)):
				print "CRUNCHY: --> Removing cached RSS feed..."
				os.remove(filename)
				return False
			else:
				print "CRUNCHY: --> RSS feed is still valid."
				return True
		else:
			print "CRUNCHY: --> RSS feed not found.  Downloading..."
			return True