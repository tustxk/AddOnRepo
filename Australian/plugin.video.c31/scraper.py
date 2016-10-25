import	urllib2 
import	re
from	time import localtime, strftime, gmtime
from	BeautifulSoup import BeautifulStoneSoup,BeautifulSoup, NavigableString
import collections


ADDON_ID='plugin.video.c31'


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
		"base"		: "http://www.c31.org.au",
	}
	
	def __init__(self, folders, play, record):
		self.folders	= folders
		self.play		= play
		self.record		= record
		
	def menu(self, params):
		out = []
		
		contents2 = geturl(Scraper.URLS['base']+"/program")
		soup = BeautifulSoup(contents2)
		for item in soup.find('div', {"id" :"feature"}).findAll('a'):
			if Scraper.URLS['base']+item['href'] != Scraper.URLS['base']+"/program":
				out.append(
					{
						"url"		: Scraper.URLS['base']+item['href'], 
						"title"		: unescape(item.string),
						"path"		: "browse",
						"folder"	: True,
					
					}
				)
		self.folders(out)

	
	def browse(self, params):
		contents2 = geturl(params['url'])
		soup = BeautifulSoup(contents2)
		out = []
		for item in soup.find('ul', {"id" :"tv-shows"}).findAll('li'):
			out.append(
						{
							"url"		: Scraper.URLS['base']+item.a['href'], 
							"title"		: item.a.string,
							"info"		: item.a['title'],
							"path"		: "browse2",
							"folder"	: True,
						
						}
					)
		self.folders(out)
		
	def browse2(self, params):
		contents2 = geturl(params['url'])
		soup = BeautifulSoup(contents2)
		out = []
		for item in soup.find('div', {"id" :"tv-guide"}).findAll('li'):
			print "***", item.a.attrs
			if u'href' in dict(item.a.attrs):
				out.append(
							{
								"url"		: Scraper.URLS['base']+item.a['href'], 
								"title"		: item.a.string +" " + item.span.string,
								"info"		: item.a['title'],
								"path"		: "browse3",
								"folder"	: True,
							
							}
						)
		self.folders(out)

	def browse3(self, params):
		contents2 = geturl(params['url'])
		soup = BeautifulSoup(contents2)
		out = []
		for item in soup.findAll('script', {"type" :"text/javascript"}):
			print item
			for item2 in re.findall(r'file: "([^"]+)"',str(item)):
			#Folders
			
				val = { 
					"url"		: item2, 
					"title"		: item2,
					"path"		: "playitems",
				#	"still"		: p.get_thumbnail(),
				#	"info"		: p.get_xbmc_list_item(),
					"folder"	: False,
				}
				out.append(val)
					
		print out
		self.folders(out)

		
		
	def playitems(self, params):
		
		
		val = {
			"url"		: params['url'],
	
			"name"		: params['name']
		}
		print ("@2"	,  val)
		if "record" in params:
			self.record(val)
		else:
			self.play(val)


if __name__ == "__main__":
	pass