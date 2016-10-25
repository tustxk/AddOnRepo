import	urllib2 
import	re
from	time import localtime, strftime, gmtime
from	BeautifulSoup import BeautifulStoneSoup,BeautifulSoup, NavigableString
import collections
import brightcove
import xml.etree.ElementTree


ADDON_ID='plugin.video.catchuptv.au.nten'


def geturl(url):
	#, headers = {"Accept-Encoding":"gzip"}
	print "getting: %s" % url
	return  urllib2.urlopen(urllib2.Request(url)).read().decode('iso-8859-1', 'ignore').encode('ascii', 'ignore')

def unescape(s):
        s = s.replace("&lt;", "<")
        s = s.replace("&gt;", ">")
        # this has to be last:
        s = s.replace("&amp;", "&")
        return s



class Scraper(object):
	URLS = {
		"base"		: "http://tenplay.com.au",
		"listing" 	: 'http://ten.com.au/watch-tv-episodes-online.htm'
	}
	
	def __init__(self, folders, play, record):
		self.folders	= folders
		self.play		= play
		self.record		= record
		
	def menu(self, params):
		out = []
		
		contents2 = geturl(Scraper.URLS['base']+"/browse-by-a-to-z")
		soup = BeautifulSoup(contents2)
		columns =   soup.find(text=re.compile("Featured TV Shows")).parent.parent.findAllNext('ul')
		for item in [i for c in list(columns)[:2] for i in c.findAll('a')]:
			if item.string and item.get('href'):
				out.append(
					{
						"url"		: Scraper.URLS['base']+item['href'], 
						"title"		: unescape(item.string) ,
						"path"		: "browse",
						"folder"	: True,
					
					}
				)
		#self.folders(sorted(out, key = lambda x: x['title']))
		self.folders(out)

	
	def browse(self, params):
		contents2 = geturl(params['url'])
		soup = BeautifulSoup(contents2)
		out = []
		#for ul in soup.find("div",{"class":"main-col-inner"}).findAll('ul', {"class" :"slides"}):
		for ul in [u for u in soup.findAll("h2") if "Latest Episodes" in (u.string or "")]:
			for item in ul.findParent('section').findAll('li'):
				details = item.find('div', {"class" :"media-details"})
				if details:
					print [x for x in item.img['src'].split("&")]
					out.append(
								{
									"url"		: Scraper.URLS['base']+details.a['href'], 
									"title"		: details.p.string,
									#"info"		: item.a['title'],
									"still"		: dict( (x.split("=", 1) +[''])[0:2] for x in item.img['src'].split("&")).get('u', ""),
									"path"		: "playitems",
									"folder"	: False,
								
								}
							)
		self.folders(out)
		
	
		
		
	def playitems(self, params):
		contents		= geturl(params['url'])
		name            = re.findall(r'"og:title" content="([^"]+)"', contents)[0]   
		playerKey       = re.findall(r'playerKey: "([^"]+)",', contents)[0]
		contentId       = re.findall(r'videoID: "([^"]+)",', contents)[0]
		key				= re.findall(r'apiToken: "([^"]+)"', contents)[0]
		seed			= 'bffc3c7ef0b4c65a8e54681f51a3701d554903be'
		swf 			= 'http://admin.brightcove.com/viewer/us20130702.1553/connection/ExternalConnection_2.swf'
		
		amfHelper       = brightcove.BrightCoveHelper( playerKey, contentId, Scraper.URLS["listing"], seed)
	   
		amfHelper.GetStreamInfo()
		print amfHelper.data['renditions']
		
		val = [
				{
						'url'           : chosen['defaultURL'].replace('&mp4:', ' playpath=mp4:') + ' swfVfy=true swfUrl=%s pageUrl=%s' % (swf, Scraper.URLS["listing"]),

						"name"          : name,
						'rate'          : chosen['encodingRate']
				}
				for chosen in amfHelper.data['renditions']
				if not chosen['audioOnly']
		]

		if "record" in params:
			self.record(val)
		else:
			self.play(val)



if __name__ == "__main__":
	pass