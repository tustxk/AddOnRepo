import	urllib2 
import gzip
from StringIO import StringIO

import	re
from	time import localtime, strftime, gmtime
from	BeautifulSoup import BeautifulStoneSoup,BeautifulSoup, NavigableString
import collections

def jsonc(st):
	for i,o in (
		('true', 'True'),
		('false', 'False'),
		('null', 'None')
	):
		st = st.replace(i,o)
	return eval(st)


ADDON_ID='plugin.video.dtv'


def geturl(url):
	#, headers = {"Accept-Encoding":"gzip"}
	print "getting: %s" % url
	http = urllib2.urlopen(
		urllib2.Request(url, None, {
			#'User-Agent' : config.user_agent,
			'Accept-Encoding' : 'gzip'
		})
	)
	headers = http.info()
	if 'content-encoding' in headers.keys() and headers['content-encoding'] == 'gzip':
		data = StringIO(http.read())
		dat =  gzip.GzipFile(fileobj=data).read()
	else:
		dat =  http.read()
	return dat.decode('iso-8859-1', 'ignore').encode('ascii', 'ignore')

def unescape(s):
        s = s.replace("&lt;", "<")
        s = s.replace("&gt;", ">")
        # this has to be last:
        s = s.replace("&amp;", "&")
        return s



class Scraper(object):
	URLS = {
		"base"		: "http://www.dw.de/media-center",
		"top"		: "http://www.dw.de/media-center/all-media-content/s-100826",
		
	}
	
	def __init__(self, folders, play, record):
		self.folders	= folders
		self.play		= play
		self.record		= record
		
	def menu(self, params):
		out = []
		
		contents2 = geturl(Scraper.URLS['top'])
		soup = BeautifulSoup(contents2)
		columns =   soup.find(text=re.compile("TV programs")).parent.parent
		for item in columns.findAll('a'):
			out.append(
				{
					"url"		: "{}/filter/type/video/programs/{}/sort/date/results/50/".format(Scraper.URLS['top'],item['href'].split("/")[-1].split("-")[1]), 
					"title"		: unescape(item.string) ,
					"path"		: "browse",
					"folder"	: True,
				
				}
			)
		#self.folders(sorted(out, key = lambda x: x['title']))
		self.folders(out)

	
	def browse(self, params):
		contents2 = geturl(params['url'])
		xx = re.sub(r'<p>(.*)</p>', r'<div class="p">\1</div>', contents2, re.MULTILINE)
		soup = BeautifulSoup(xx)
		out = []
		soup2= soup.find("div", {"id":"bodyContent"})
		for ul, dt in [(x.findParent('a'),x) for x in soup2.findAll("span", {'class' : 'date'})]:
			print type(ul), ul
			if ul.name == 'a':
				out.append(
					{
						"url"		: Scraper.URLS['base']+ul['href'], 
						"title"		: ul.h2.contents[0] or "",
						"info"		: {
							"plot"		: " ".join([x.string for x in ul.findAll('div', {"class" : "p"})]),
						#	"duration"	: "%s:%s:%s" % (hours, minutes, seconds),
							"date"		: dt.string.split("|")[0].replace(".", " "),
						},
						"still"		: ul.img['src'],
						"path"		: "playitems",
						"folder"	: False,
					
					}
			)

		self.folders(out)
		
	
		
		
	def playitems(self, params):
		contents		= geturl(params['url'])
		soup = BeautifulSoup(contents)
		import urlparse
		details = soup.find('meta',	 {"property" : "og:video"})['content']
		print ("swf=" + details).replace('?', '&').split('&')
		subs = {y[0] : urlparse.unquote(y[1]) for x in ("swf=" + details).replace('?', '&').split('&') for y in [x.split('=')]}
		print subs
		print jsonc(subs['levels'].replace('[[JSON]]','')), type(jsonc(subs['levels'].replace('[[JSON]]','')))
		name = soup.h1.string
		
		val = [
				{
						'url'           : "{} playpath=mp4:{}".format(subs["streamer"],chosen['file'])  if ".mp4" in chosen['file'] else "http://tv-download.dw.de/dwtv_video/flv/{}".format(chosen['file']),

						"name"          : name,
						'rate'          : int(chosen['bitrate']) * 1000
				}
				for chosen in jsonc(subs['levels'].replace('[[JSON]]',''))[:]
				#TODO: not sure how to deal with this
				if "sor.flv" not in chosen['file']
				
		]

		if "record" in params:
			self.record(val)
		else:
			self.play(val)



if __name__ == "__main__":
	pass