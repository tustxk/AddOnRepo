import sys
import urllib
import xbmc
import xbmcgui
import xbmcplugin
import crunchy_scraper
import re
from crunchy_video import CrunchyPlayback

class updateArgs:

	def __init__(self, *args, **kwargs):
		for key, value in kwargs.iteritems():
			if value == 'None':
				kwargs[key] = None
			else:
				kwargs[key] = urllib.unquote_plus(kwargs[key])
		self.__dict__.update(kwargs)

class UI:
	
	def __init__(self):
		self.main = Main(checkMode = False)
		xbmcplugin.setContent(int(sys.argv[1]), 'movies')
	
	def endofdirectory(self, sortMethod = 'none'):
		# set sortmethod to something xbmc can use
		if sortMethod == 'title':
			sortMethod = xbmcplugin.SORT_METHOD_LABEL
		elif sortMethod == 'none':
			sortMethod = xbmcplugin.SORT_METHOD_NONE
		elif sortMethod == 'date':
			sortMethod = xbmcplugin.SORT_METHOD_DATE
		#Sort methods are required in library mode.
		xbmcplugin.addSortMethod(int(sys.argv[1]), sortMethod)
		#let xbmc know the script is done adding items to the list.
		dontAddToHierarchy = False
		xbmcplugin.endOfDirectory(handle = int(sys.argv[1]), updateListing = dontAddToHierarchy)
			
	def addItem(self, info, isFolder=True, total_items = 0):
		#Defaults in dict. Use 'None' instead of None so it is compatible for quote_plus in parseArgs
		info.setdefault('url','None')
		info.setdefault('Thumb','None')
		info.setdefault('id','None')
		info.setdefault('page_url','None')
		info.setdefault('Icon','None')
		info.setdefault('resolutions','10')
		info.setdefault('plot','No description available.')
		print info
		#create params for xbmcplugin module
		u = sys.argv[0]+\
			'?url='+urllib.quote_plus(info['url'])+\
			'&mode='+urllib.quote_plus(info['mode'])+\
			'&name='+urllib.quote_plus(info['Title'])+\
			'&id='+urllib.quote_plus(info['id'])+\
			'&resolutions='+urllib.quote_plus(info['resolutions'])+\
			'&page_url='+urllib.quote_plus(info['page_url'])+\
			'&icon='+urllib.quote_plus(info['Thumb'])+\
			'&plot='+urllib.quote_plus(info['plot'])
		#create list item
		li=xbmcgui.ListItem(label = info['Title'], iconImage = info['Icon'], thumbnailImage = info['Thumb'])
		li.setInfo( type="Video", infoLabels={ "Title":info['Title'], "Plot":info['plot']})
		#for videos, replace context menu with queue and add to favorites
		if not isFolder:
			li.setProperty("IsPlayable", "true")#let xbmc know this can be played, unlike a folder.
			#add context menu items to non-folder items.
			contextmenu = [('Queue Video', 'Action(Queue)')]
		#for folders, completely remove contextmenu, as it is totally useless.
		else:
			li.addContextMenuItems([], replaceItems=True)
		#add item to list
		ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=li, isFolder=isFolder, totalItems=total_items)

	def showCategories(self):
		self.addItem({'Title':'Anime', 'mode':'anime'})
		self.addItem({'Title':'Drama', 'mode':'drama'})
		self.endofdirectory()
		
	def showAnime(self):
		self.addItem({'Title':'All Anime', 'mode':'genre_anime_all'})
		self.addItem({'Title':'Recently Added', 'mode':'featured'})
		self.addItem({'Title':'Most Popular', 'mode':'anime_popular'})
		self.addItem({'Title':'Browse by Genre', 'mode':'anime_genre'})
		self.endofdirectory()
		
	def animeGenre(self):
		self.addItem({'Title':'Action', 'mode':'anime_withtag','id':'action'})
		self.addItem({'Title':'Adventure', 'mode':'anime_withtag','id':'adventure'})
		self.addItem({'Title':'Comedy', 'mode':'anime_withtag','id':'comedy'})
		self.addItem({'Title':'Drama', 'mode':'anime_withtag','id':'drama'})
		self.addItem({'Title':'Ecchi', 'mode':'anime_withtag','id':'ecchi'})
		self.addItem({'Title':'Fantasy', 'mode':'anime_withtag','id':'fantasy'})
		self.addItem({'Title':'Harem', 'mode':'anime_withtag','id':'harem'})
		self.addItem({'Title':'Horror', 'mode':'anime_withtag','id':'horror'})
		self.addItem({'Title':'Magic', 'mode':'anime_withtag','id':'magic'})
		self.addItem({'Title':'Martial Arts', 'mode':'anime_withtag','id':'martial_arts'})
		self.addItem({'Title':'Mecha', 'mode':'anime_withtag','id':'mecha'})
		self.addItem({'Title':'Military', 'mode':'anime_withtag','id':'military'})
		self.addItem({'Title':'Parody', 'mode':'anime_withtag','id':'parody'})
		self.addItem({'Title':'Psychological', 'mode':'anime_withtag','id':'psychological'})
		self.addItem({'Title':'Romance', 'mode':'anime_withtag','id':'romance'})
		self.addItem({'Title':'Science Fiction', 'mode':'anime_withtag','id':'science_fiction'})
		self.addItem({'Title':'Shoujo', 'mode':'anime_withtag','id':'shoujo'})
		self.addItem({'Title':'Slice of Life', 'mode':'anime_withtag','id':'slice_of_life'})
		self.addItem({'Title':'Space', 'mode':'anime_withtag','id':'space'})
		self.addItem({'Title':'Sports', 'mode':'anime_withtag','id':'sports'})
		self.addItem({'Title':'Supernatural', 'mode':'anime_withtag','id':'supernatural'})
		self.addItem({'Title':'Tournament', 'mode':'anime_withtag','id':'tournament'})
		self.endofdirectory()
		
	def series(self):
		crunchy_scraper.CrunchyScraper().getSeriesListing(self.main.args.mode, self.main.args.id)
		
	def episodes(self):
		crunchy_scraper.CrunchyScraper().getEpisodeListing(self.main.args.id)
		
	def featured(self):
		crunchy_scraper.CrunchyScraper().getEpisodeListing('featured', 'http://www.crunchyroll.com/boxee_feeds/featured')
		
	def startVideo(self):
		print 
		CrunchyPlayback().startPlayback(self.main.args.id, self.main.args.page_url, self.main.args.resolutions)

class Main:

	def __init__(self, checkMode = True):
		#self.user = None
		self.parseArgs()
		if checkMode:
			self.checkMode()

	def parseArgs(self):
		# call updateArgs() with our formatted argv to create the self.args object
		if (sys.argv[2]):
			exec "self.args = updateArgs(%s')" % (sys.argv[2][1:].replace('&', "',").replace('=', "='"))
		else:
			# updateArgs will turn the 'None' into None.
			# Don't simply define it as None because unquote_plus in updateArgs will throw an exception.
			# This is a pretty ugly solution, but fuck it :(
			self.args = updateArgs(mode = 'None', url = 'None', name = 'None')

	def checkMode(self):
		mode = self.args.mode
		if mode is None:
			UI().showCategories()
		elif mode == 'episode':
			UI().startVideo()
		elif mode == 'anime':
			UI().showAnime()
		elif mode == 'genre_anime_all' or mode == 'anime_popular' or mode=='drama' or mode=='anime_withtag':
			UI().series()
		elif mode == 'anime_genre':
			UI().animeGenre()
		elif mode == 'featured':
			UI().featured()
		elif mode == 'series':
			UI().episodes()