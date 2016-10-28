import os
import re
import sys
import time
import xbmc
import xbmcgui
import urllib
import urllib2
import cookielib
import subprocess
from crunchyDec import crunchyDec
from BeautifulSoup import BeautifulSoup

__settings__ = sys.modules[ "__main__" ].__settings__

class CrunchyPlayback:
	def __init__(self):
		self.base_cache_path = os.path.join(xbmc.translatePath("special://masterprofile/"), "addon_data", os.path.basename(os.getcwd()))
		self.subFormat = '.ass'
	
	def checkPlayer(self, url):
		hour = 3600
		max_age = 3*hour
		player_rev = None
		lastPlayerCheck = __settings__.getSetting("lastPlayerCheck")
		if not lastPlayerCheck:
			player_rev = self.returnPlayer(url)
			__settings__.setSetting("playerRevision", player_rev)
			new_time = time.time()
			print new_time
			__settings__.setSetting("lastPlayerCheck", str(new_time))
		else:
			time_now = time.time()
			if float(lastPlayerCheck) < (time_now - max_age):
				print "CRUNCHYROLL: --> Updating player version..."
				player_rev = self.returnPlayer(url)
				__settings__.setSetting("playerRevision", player_rev)
				__settings__.setSetting("lastPlayerCheck", str(time.time()))
			else:
				print "CRUNCHYROLL: --> Cache valid: using stored player version..."
				player_rev = __settings__.getSetting("playerRevision")
		return player_rev
		
	def returnPlayer(self, url):
		REGEX_PLAYER_REV = re.compile("(?<=swfobject\.embedSWF\(\").*(?:StandardVideoPlayer.swf)")
		cj = cookielib.CookieJar()
		intOpener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
		request = urllib2.Request(url)
		response = intOpener.open(request)
		soup = BeautifulSoup(response)
		interstitial = soup.find('div', attrs={'id': 'adt_interstitial'})
		if interstitial:
			continueLink = soup.find('a', attrs={'style': 'font-size:14px;line-height:25px;'})
			continueLink = continueLink['href']
			response = intOpener.open(continueLink)
			soup = BeautifulSoup(response)
		match = REGEX_PLAYER_REV.search(str(soup))
		if match:
			print "CRUNCHYROLL: --> Found new Player Revision"
			playerTemp = str(match.group(0))
			player = playerTemp.split('\/')[4]
			print player
		else:
			print "CRUNCHYROLL: --> NO MATCHES FOUND for new Player Revision"
			player = '20110110190253.eaa2220a32da869f33f1cefc8dc91b3b'
		return player
	
	def downloadHTML(self, url):
		self.currenturl = url
		response = self.opener.open(self.currenturl)
		html = response.read()
		print "CRUNCHYROLL: --> Grabbing URL: "+self.currenturl
		self.referer = self.currenturl
		return html
	
	def startPlayback(self, vid_id, page_url, resolutions):
		stream = {}
		settings = {}
		settings['username'] = __settings__.getSetting("crunchy_username")
		settings['password'] = __settings__.getSetting("crunchy_password")
		settings['quality'] = int(__settings__.getSetting("video_quality"))
		res_avail = [12, 20, 21]
		res_names = ['SD', '480p', '720p']
		res_newformat = {'12':'10','20':'20','21':'30'}
		
		if (len(res_avail) > 1 and settings['username'] != '' and settings['password'] != ''):
			res_options = []
			for res in res_avail:
				item = [res_names[res_avail.index(res)], res]
				res_options.append(item)
			#If the user has selected 'Ask', display the quality select dialog
			if settings['quality'] == 3:
				quality = xbmcgui.Dialog().select('Please select a quality level:', [opt[0] for opt in res_options])
			#If the user has selected 'Highest available quality', set it as such
			elif settings['quality'] == 4:
				quality = res_avail[len(res_avail)-1]
			#If the user has selected a specific resolution, use that instead
			elif settings['quality'] < 3:
				quality = settings['quality']
			else:
				quality = 0
			if(quality > (len(res_avail)-1)):
				quality = len(res_avail)-1;
			stream['resolution'] = res_avail[quality]
		else:
			stream['resolution'] = res_avail[0]
		print str(res_avail)
		print stream['resolution']
		stream['resolution'] = res_newformat[str(stream['resolution'])]
		playlist = playlist = "http://www.crunchyroll.com/xml/?req=RpcApiVideoPlayer_GetStandardConfig&media_id="+vid_id+"&video_format=102&video_quality="+stream['resolution']+"&auto_play=1&show_pop_out_controls=1"
		print "CRUNCHYROLL: --> Playlist is: "+playlist
		
		if (settings['username'] != '' and settings['password'] != ''):
			print "CRUNCHYROLL: --> Attempting to log-in with your user account..."
			url = 'https://www.crunchyroll.com/?a=formhandler'
			data = urllib.urlencode({'formname':'RpcApiUser_Login', 'next_url':'','fail_url':'/login','name':settings['username'],'password':settings['password']})

			COOKIEFILE= os.path.join(self.base_cache_path, "crunchycookie.lwp")
			cj = cookielib.LWPCookieJar()
			self.cookie = cj
			if os.path.isfile(COOKIEFILE):
				cj.load(COOKIEFILE)

			opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
			opener.addheaders = [('Referer', 'https://www.crunchyroll.com'),('User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')]
			self.opener = opener
			
			if not os.path.isfile(COOKIEFILE):
				print "CRUNCHYROLL: --> Cookie file doesn't exist; saving new one."
				urllib2.install_opener(opener)
				req = self.opener.open(url, data)
				req.close()
				cj.save(COOKIEFILE)

		else:
			print "CRUNCHYROLL: --> No user account found..."
			opener = urllib2.build_opener()
			opener.addheaders = [('Referer', 'http://www.crunchyroll.com'),('User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')]
			self.opener = opener
		response = self.opener.open(playlist)
		xmlSource = response.read()

		soup = BeautifulSoup(xmlSource)
		player_url = soup.find('default:chromelessplayerurl').string
		meta_info = soup.find('media_metadata')
		try:
			stream['episode_display'] = meta_info.series_title.string +" - "+ meta_info.episode_number.string
		except:
			stream['episode_display'] = '... Video presented by Crunchyroll.com'
		
		stream_info = soup.find('stream_info')
		if stream_info:
			player_revision = self.checkPlayer('http://www.crunchyroll.com/naruto/episode-193-the-man-who-died-twice-567104')
			try:
				stream['url'] = stream_info.host.string
				stream['token'] = stream_info.token.string
				stream['file'] = stream_info.file.string
				stream['page_url'] = page_url
				stream['swf_url'] = "http://static.lln.crunchyroll.com/flash/"+player_revision+"/"+player_url
				try:
					app = stream['url'].split('.net/')
					stream['app'] = app[1]
					print "CRUNCHYROLL: --> App - " + stream['app']
				except:
					print "Couldn't find App"
				
				useSubs = False
				mediaid = vid_id
				subtitles = soup.find('subtitles')
				print "CRUNCHYROLL: --> Attempting to find subtitles..."
				if(subtitles):
					print "CRUNCHYROLL: --> Found subtitles.  Continuing..."
					formattedSubs, formatSRT = crunchyDec().returnSubs(xmlSource)
					if formatSRT:
						print "CRUNCHYROLL: --> Using unstyled subs!"
						self.subFormat = '.srt'
					subfile = open(xbmc.translatePath('special://temp/crunchy_'+ mediaid + self.subFormat), 'w')
					subfile.write(formattedSubs.encode('utf-8'))
					subfile.close()
					useSubs = True
				else:
					print "CRUNCHYROLL: --> No subtitles available!"
					mediaid = ""
				
				self.playvideo(stream, mediaid, useSubs)
			except:
				if stream_info.find('upsell'):
					if stream_info.upsell.string == '1':
						ex = 'XBMC.Notification("Video restricted:","Video not available to your user account.", 3000)'
						xbmc.executebuiltin(ex)
						print "CRUNCHYROLL: --> Selected video quality is not available to your user account."
				elif stream_info.find('error'):
					if stream_info.error.code.string == '4':
						ex = 'XBMC.Notification("Mature Content:","Please login to view this video.", 3000)'
						xbmc.executebuiltin(ex)
						print "CRUNCHYROLL: --> This video is marked as Mature Content.  Please login to view it."
		else:
			print "Playback Failed!"
		
	def playvideo(self, stream, mediaid, useSubs):
		rtmp_url = stream['url'] + " swfUrl=" + stream['swf_url'] + " swfVfy=1 pageUrl=" + stream['page_url'] + " playPath=" + stream['file']
		item = xbmcgui.ListItem(stream['episode_display'])
		item.setInfo( type="Video", infoLabels={ "Title": stream['episode_display'] })
		item.setProperty('IsPlayable', 'true')
		
		if(useSubs == True):
			print "CRUNCHYROLL: --> Playing video and setting subtitles to special://temp/crunchy_"+mediaid+".ass"
			xbmc.Player().play(rtmp_url)
			xbmc.Player().setSubtitles(xbmc.translatePath('special://temp/crunchy_' + mediaid + self.subFormat))
		else:
			xbmc.Player().play(rtmp_url, item)