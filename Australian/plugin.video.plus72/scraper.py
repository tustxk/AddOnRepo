import	urllib2 , urllib 
import	re
import	collections
from	BeautifulSoup import BeautifulStoneSoup,BeautifulSoup, NavigableString
import threading
import pprint
import helpers.brightcovehelper
	

try:
    import json
except ImportError:
    import simplejson as json
 

def geturl(url):
	#, headers = {"Accept-Encoding":"gzip"}
	print "getting: %s" % url
	return  urllib2.urlopen(urllib2.Request(url),timeout=60).read().decode('iso-8859-1', 'ignore').encode('ascii', 'ignore')

def pretty(st):
	return BeautifulSoup(st, convertEntities=BeautifulSoup.HTML_ENTITIES).prettify().strip()
	
class Scraper(object):
	URLS = {
		"base"		: "http://au.tv.yahoo.com",
	}
	
	def __init__(self, folders, play, record,playbrowser):
		self.folders	= folders
		self.play		= play
		self.record		= record
		self.playbrowser= playbrowser
		
	def menu(self, params):
		contents =  geturl(self.URLS['base'] + "/plus7/browse/")
		soup = BeautifulSoup(contents)
		out = []
		for item in soup.find('div', {"id":"atoz", "class" : "bd"}).findAll("li"):
			if dict(item.attrs).get("class", None) != "letter":
				print item
				val = { 
					"url"	: item.a["href"], 
					"title"	: pretty(item.h3.a.string),
					"still"	: item.a.img["src"] ,
					"path"	: "browse",
					"folder"	: True,
				}
				print val
				out.append(val)
		return self.folders(out)
	

	
	def browse(self, params):
		soup = BeautifulSoup(geturl(params['url']))
		
		ginf = {}
		hd = str(soup.find('div', {"class" :"mod tv-plus7-info"})).replace('\n', '')
		print ("Y1", hd)
		ginf['genre'] =  re.findall(r"Genre:\s*<strong>(.*?)</strong>", str(soup))[0]
		ginf['mpaa'] =  re.findall(r"Classified:\s*<strong>(.*?)</strong>", str(soup))[0]
		print ("info11", ginf)
		out = []
		for item in soup.find("ul", {"id": "related-episodes", "class" : "featlist"}).findAll("li", {"class" : "clearfix"}):
			#Folders
			print ("!@", item)
			inf = ginf.copy()
			inf["plot"] = (item.div.p.string or "").strip()
			val = { 
				"url"		: "%s%s" % (self.URLS['base'], item.a["href"]), 
				"title"		: pretty(" - ".join(it.string.strip() for it in item.div.h3.findAll('span') if it.string )),
				"path"		: "playitems",
				"still"		: item.a.img["src"] ,
				"info"		: inf,
				"folder"	: False,
			}
			out.append(val)
				
		
		return self.folders(out)


	def playitems(self, params):
		print params
		html = geturl(params['url'])
		
		soup = BeautifulSoup(html)
		
		if 1:
			name		= soup.find('meta', {"property" :"og:title"})['content']
			
			playerKey	= soup.find('param', {"name" :"playerKey"})['value']
			contentId	= soup.find('param', {"name" :"playerID"})['value']
			key			= soup.find('param', {"name" :"@videoPlayer"})['value'].split(':')[-1]
			seed		= 'ff51606519f716952a8db17f076fad130f8d2337'
			amfHelper	= helpers.brightcovehelper.BrightCoveHelper({}, playerKey, contentId, params['url'], seed,  contentRefId = key)
			
			amfHelper.GetStreamInfo()
			
			
			
			print "$" * 120
			import pprint
			print pprint.pformat(amfHelper.full_response)
			print "!" * 120	
			
			
			val = [
				{
					'url'		: chosen['defaultURL'],
					"name"		: name,
					'rate'		: chosen['encodingRate']
				}
				for chosen in amfHelper.full_response["programmedContent"]["videoPlayer"]["mediaDTO"]["IOSRenditions"]
				if not chosen['audioOnly']
			]
	
			if "record" in params:
				return self.record(val)
			else:
				return self.play(val)



if __name__ == "__main__":
	pass