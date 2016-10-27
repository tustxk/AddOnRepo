import xbmcplugin
import xbmcgui
import sys, random
import urllib, urllib2, cookielib
import re, base64
from htmlentitydefs import name2codepoint as n2cp

# new v0.95
import urlresolver

thisPlugin = int(sys.argv[1])

urlHost = "http://www.burning-seri.es/"

regexContentA = "<ul id='serSeries'>(.*?)</ul>"
regexContentB = '<li><a href="(.*?)">(.*?)</a></li>'
regexSeasonsA = '<ul class="pages">.*?</ul>'
regexSeasonsB = '<li.*?><a href="(.*?)".*?>(.*?)</a></li>'
regexEpisodesA = '<table>.*?</table>'
regexEpisodesB = '<tr>.*?<td>(.*?)</td>.*?<td>.*?<a href="(.*?)">.*?<strong>(.*?)</strong>.*?<td class="nowrap">.*?</tr>'
regexHostsA = 'Episode</h3>.*?<ul style="width: [0-9]{1,3}px;">(.*?)</ul>.*?</section>'
regexHostsB = '<a href="(.*?)"><span.*?class="icon (.*?)"></span>(.*?)</a>'
# ------------------------

def showContent():
	global thisPlugin
	print "-- showContent started"
	content = getUrl(urlHost+"andere-serien").replace("&amp;","&")
	#print content
	matchA = re.compile(regexContentA,re.DOTALL).findall(content)
	print matchA
	matchB = re.compile(regexContentB,re.DOTALL).findall(matchA[0])
	for m in matchB:
		#print m
		addDirectoryItem(m[1].strip(), {"urlS": m[0]})  
	print "--- showContent ok"	
	xbmcplugin.endOfDirectory(thisPlugin)

def showSeasons(urlS):
	global thisPlugin
	print "--- showSeasons started with "+urlS
	print "--- found"
	content = getUrl(urlS)
	matchA = re.compile(regexSeasonsA,re.DOTALL).findall(content)
	matchB = re.compile(regexSeasonsB,re.DOTALL).findall(matchA[0])
	for m in matchB:
			print m
			preString = ""
			if is_number(m[1]):
				preString = "Staffel "
			addDirectoryItem(preString+m[1], {"urlE": m[0]})
 
	print "--- showSeasons ok"	
	xbmcplugin.endOfDirectory(thisPlugin)

def showEpisodes(urlE):
	global thisPlugin
	print "---- showEpisodes started with "+urlE
	print "---- found"
	content = getUrl(urlE)
	#print "---content"
	#print content
	matchA = re.compile(regexEpisodesA,re.DOTALL).findall(content)
	print "---matchA"
	print matchA[0]
	matchB = re.compile(regexEpisodesB,re.DOTALL).findall(matchA[0])
	#print matchB[0]
	print "---matchB"
	for m in matchB:
			print m
			addDirectoryItem(m[0].strip()+" - "+m[2], {"urlH": m[1]}) 
	print "---- showEpisodes ok"	
	xbmcplugin.endOfDirectory(thisPlugin)

def showHosts(urlH):
	global thisPlugin
	print "----- showHosts started with "+urlH
	print "----- found"
	content = getUrl(urlH)
	#print "-- showHosts"
	#print content
	matchA = re.compile(regexHostsA,re.DOTALL).findall(content)
	print "-- matchesA"
	print matchA
	matchB = re.compile(regexHostsB,re.DOTALL).findall(matchA[0])
	print "-- matchB"
	print matchB
	addDirectoryItem("INFO - urlResolver is now active!", {"urlV": "/"})
	for m in matchB:
			#print m
			addDirectoryItem("Play from "+m[2].strip(), {"urlV": m[0]})
			print m[1]+" : "+m[0]  
	print "----- showHosts ok"	
	xbmcplugin.endOfDirectory(thisPlugin)
	
def showVideo(urlV):

	global thisPlugin
	print "--->> showVideo started on "+urlV
	content = getUrl(urlV)
	#print content
	matchVideo = re.compile('<div id="video_actions">.*?<div>.*?<a href="(.*?)" target="_blank"><span',re.DOTALL).findall(content)
	print " --> matchVideo - "+matchVideo[0]
	# --- sockShare ---
	#if urlV.find("Sockshare")>0 :
	#	matchA = re.compile('<a href="http://www.sockshare.com/file/(.*?)" target="_blank"><span',re.DOTALL).findall(content)
	#	print "-- matchA"
	#	print matchA
	#	newUrl ="http://www.sockshare.com/embed/"+matchA[0]
	#	content = getUrl(newUrl)
	#	print "-- content"
	#	print content
	#	matchB = re.compile('value="(.*?)" name="(.*?)"').findall(content)
	#	print "-- input hidden"
	#	print matchB
	#	
	#	matchB = re.compile("playlist: '/get_file.php?(.*?)',").findall(content)
	#	print "-> newUrl"
	#	newUrl = 'http://www.sockshare.com/get_file.php?'+matchB[0]
	#	print newUrl
	#	contentVideo2 =  getUrl(newUrl)
	#	print "-- contentVideo2"
	#	print contentVideo2
	#	
	#	videoLink=findVideoUrl[0].replace("','","");
	#	print "VideoLink :"+videoLink
	#	#print findKeys
	#	#videoLink = findKeys[0]
	#
	## --- RapidVideo ---
	#if urlV.find("RapidVideo")>0 :
	#	#matchB = re.compile('video_actions">.*?<a href="(.*?)" target="_blank"><span',re.DOTALL).findall(content)
	#	print "-> matchB"
	#	print matchB
	#	contentXML =  getUrl(matchB[0])
	#	print "-- ContentXML"
	#	print contentXML
	#	findKeys = re.compile('flashvars=\'file=(.*?)&amp;').findall(contentXML)
	#	print "-- findKeys"
	#	print findKeys
	#	videoLink = findKeys[0]
	#	
	## --- VideoBB ---
	#if urlV.find("VideoBB")>0 :
	#	matchB = re.compile('video_actions">.*?<a href="(.*?)" target="_blank"><span',re.DOTALL).findall(content)
	#	print "-> matchB"
	#	print matchB
	#	varsUrl =  getUrl(matchB[0])
	#	getJSONUrl = re.compile('value="setting=(.*?)" name').findall(varsUrl)
	#	print "-> JSONUrl encoded"
	#	print getJSONUrl[0]
	#	JSONurl = base64.b64decode(getJSONUrl[0])
	#	print "-> JSONUrl decoded"
	#	print JSONurl
	#	videoUrl = getUrl(JSONurl)
	#	#print videoUrl
	#	isVideoUrl = re.compile('"token1":"(.*?)"').findall(videoUrl)
	#	print "-> VideoUrl encoded"
	#	print isVideoUrl[0]
	#	videoLink = base64.b64decode(isVideoUrl[0])
 	#	print "-> VideoUrl decoded"
	#	
	#	# --- Putlocker ---
	#if urlV.find("PutLocker")>0 :
	#	matchB = re.compile('video_actions">.*?<a href="(.*?)" target="_blank"><span',re.DOTALL).findall(content)
	#	print "-> matchB"
	#	print matchB
	#	varsUrl =  getUrl(matchB[0])
	#	gethashValue = re.compile('type="hidden" value="(.*?)" name="hash"').findall(varsUrl)
	#	values = {'hash': gethashValue[0], 'confirm':'Continue as Free User'}
	#	print values
	#	user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
	#	headers = { 'User-Agent' : user_agent }
	#	cjar = cookielib.LWPCookieJar()
	#	cjar = urllib2.HTTPCookieProcessor(cjar) 
	#	opener = urllib2.build_opener(cjar)
	#	urllib2.install_opener(opener)
	#	data = urllib.urlencode(values)
	#	req = urllib2.Request(matchB[0], data, headers)
	#	response = urllib2.urlopen(req)
	#	link = response.read()
	#	code = re.compile("stream=(.+?)'").findall(link)
	#	req = urllib2.Request('http://www.putlocker.com/get_file.php?stream='+code[0])
	#	req.add_header('User-Agent', user_agent)
	#	response = urllib2.urlopen(req)
	#	link=response.read()
	#	videoLink = re.compile('<media:content url="(.+?)"').findall(link)[0]
	#
	videoLink = urlresolver.resolve(matchVideo[0]);
	if videoLink:
		print "--> urlResolver videoLink --"
		print videoLink
		videoLink = decode_htmlentities(videoLink)
		xbmc.Player().play(videoLink)
	else:
		addDirectoryItem("ERROR!", {"urlV": "/"})
		addDirectoryItem("Video 404 or urlResolver cant handle Host", {"urlV": "/"})
		addDirectoryItem("SORRY!", {"urlV": "/"})
		xbmcplugin.endOfDirectory(thisPlugin)

# -------- helper ------

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def baseN(num,b,numerals="0123456789abcdefghijklmnopqrstuvwxyz"):
	return ((num == 0) and numerals[0]) or (baseN(num // b, b, numerals).lstrip(numerals[0]) + numerals[num % b])

def getUrl(url):
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	return link

def addDirectoryItem(name, parameters={},pic=""):
    li = xbmcgui.ListItem(name,iconImage="DefaultFolder.png", thumbnailImage=pic)
    url = sys.argv[0] + '?' + urllib.urlencode(parameters)
    return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=url, listitem=li, isFolder=True)

def parameters_string_to_dict(parameters):
    ''' Convert parameters encoded in a URL to a dict. '''
    paramDict = {}
    if parameters:
        paramPairs = parameters[1:].split("&")
        for paramsPair in paramPairs:
            paramSplits = paramsPair.split('=')
            if (len(paramSplits)) == 2:
                paramDict[paramSplits[0]] = paramSplits[1]
    return paramDict

def substitute_entity(match):
    ent = match.group(3)
    
    if match.group(1) == "#":
        if match.group(2) == '':
            return unichr(int(ent))
        elif match.group(2) == 'x':
            return unichr(int('0x'+ent, 16))
    else:
        cp = n2cp.get(ent)

        if cp:
            return unichr(cp)
        else:
            return match.group()

def decode_htmlentities(string):
    entity_re = re.compile(r'&(#?)(x?)(\w+);')
    return entity_re.subn(substitute_entity, string)[0]

# ----- main -----

params = parameters_string_to_dict(sys.argv[2])
urlSeasons = str(params.get("urlS", ""))
urlEpisodes = str(params.get("urlE", ""))
urlHosts = str(params.get("urlH", ""))
urlVideo = str(params.get("urlV", ""))

if not sys.argv[2]:
	# new start
	ok = showContent()
else:
	if urlSeasons:
		newUrl = urlHost + urllib.unquote(urlSeasons)
		#print newUrl
		ok = showSeasons(newUrl)
	if urlEpisodes:
		newUrl = urlHost + urllib.unquote(urlEpisodes)
		#print newUrl
		ok = showEpisodes(newUrl)
	if urlHosts:
		newUrl = urlHost + urllib.unquote(urlHosts)
		#print newUrl
		ok = showHosts(newUrl)
	if urlVideo:
		newUrl = urlHost + urllib.unquote(urlVideo)
		#print newUrl
		ok = showVideo(newUrl)


