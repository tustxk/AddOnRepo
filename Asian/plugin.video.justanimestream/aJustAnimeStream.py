### ############################################################################################################
###	#	
### # Site: 				#		Anime FATE - http://www.justanimestream.net/
### # Author: 			#		The Highway
### # Description: 	#		
###	#	
### ############################################################################################################
### ############################################################################################################
### Imports ###
import xbmc
import os,sys,string,StringIO,logging,random,array,time,datetime,re
try: import copy
except: pass
import urllib,urllib2,xbmcaddon,xbmcplugin,xbmcgui
from common import *
from common import (_addon,_artIcon,_artFanart,_addonPath,_debugging)
### ############################################################################################################
### ############################################################################################################
SiteName='J[COLOR green]ust[/COLOR]A[COLOR white]nime[/COLOR]S[COLOR cornflowerblue]tream[/COLOR]  [v0.0.5]  [Anime]'
SiteTag='justsnimestream.net'
mainSite='http://www.justanimestream.net'
mainSite2='http://www.justanimestream.net'
iconSite='http://www.justanimestream.net/justanimestream.png' #_artIcon #'http://www.justanimestream.net/justanimestream.png'
fanartSite='http://i.imgur.com/tRXSbdI.png' #_artFanart #'http://www.justanimestream.net/wp-content/themes/justanimestreamv1/images/tpl_bg.gif'
colors={'0':'white','1':'red','2':'blue','3':'green','4':'yellow','5':'orange','6':'lime','7':'','8':'cornflowerblue','9':'blueviolet','10':'hotpink','11':'pink','12':'tan','13':'firebrick','14':'mediumpurple'}

CR='[CR]'
MyAlphabet=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
#MyGenres=[' Action','Action','Adventure','Animation','Cars','Comedy','Dementia','Demons','Drama','Ecchi','Fantasy','Game','Harem','Historical','Horror','Josei','Kids','Magic','Martial Arts','Mecha','Military','Movie','Music','Mutants','Mystery','Parody','Police','Psychological','Romance','Samurai','School','Sci-Fi','Seinen','Shoujo','Shoujo Ai','Shounen','Shounen Ai','Slice of Life','Space','Sports','Super Power','Supernatural','Thriller','Vampire']
MyGenres=['Action','Adventure','Animation','Children','Comedy','Drama','Fantasy','Horror','Magic','Mystery','Psychological','Romance','Science Fiction','Slice of Life','Supernatural','Thriller','Tournament']
MyBrowser=['User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3']
ww6='[COLOR black]@[/COLOR]'; 
ww7='[COLOR mediumpurple]@[/COLOR]'; 

workingUrl=mainSite+'ram.pls'
### ############################################################################################################
### ############################################################################################################
site=addpr('site','')
section=addpr('section','')
url=addpr('url','')
sections={'series':'series','movies':'movies'}
thumbnail=addpr('img','')
fanart=addpr('fanart','')
page=addpr('page','')
### ############################################################################################################
### ############################################################################################################
def About(head=''+cFL(SiteName,'blueviolet')+'',m=''):
	m=''
	if len(m)==0:
		m+='IRC Chat:  '+cFL('#XBMCHUB','blueviolet')+' @ '+cFL('irc.Freenode.net','blueviolet')
		m+=CR+'Site Name:  '+SiteName+CR+'Site Tag:  '+SiteTag+CR+'Site Domain:  '+mainSite+CR+'Site Icon:  '+iconSite+CR+'Site Fanart:  '+fanartSite
		m+=CR+'Age:  Please make sure you are of a valid age to watch the material shown.'
		m+=CR+CR+'Known Hosts for Videos:  '
		m+=CR+'* VideoCrazy'
		m+=CR+'* UploadCrazy'
		m+=CR+CR+'Features:  '
		#m+=CR+'* Browse Shows'
		#m+=CR+'* Browse Episodes'
		#m+=CR+'* Browse Host Links'
		#m+=CR+'* Play Videos with UrlResolver'
		#m+=CR+'* Download Videos with UrlResolver'
		#m+=CR+'* MetaData for Shows and 1st Season Episodes where data is available.'
		#m+=CR+'* MetaData auto-disabled for Anime List - ALL.  This is to prevent hammering with the huge list of nearly 400 shows.'
		m+=CR+CR+'Notes:  '
		#m+=CR+'* '
		#m+=CR+'* '
		m+=CR+''
		m+=CR+ps('ReferalMsg')
		m+=CR+''
		m+=CR+''
		m+=CR+''
	String2TextBox(message=cFL(m,'cornflowerblue'),HeaderMessage=head)
	#RefreshList()
def spAfterSplit(t,ss):
	if ss in t: t=t.split(ss)[1]
	return t
def spBeforeSplit(t,ss):
	if ss in t: t=t.split(ss)[0]
	return t
def FixImage(img):
	if 'http://' not in img: img=mainSite+img; 
	if mainSite+'/bimages/' in img: img=img.replace(mainSite+'/bimages/',mainSite+'/images/')
	#try: r1,r2=re.compile('(http://www.animefate.com/images/.+?)-\d+x\d+(\.[jpg|png|gif]+)').findall(img)[0]; img=r1+r2; 
	#except: pass
	return img
def AFColoring(t): 
	if len(t)==0: return t
	elif len(t)==1: return cFL(t,colors['13'])
	else: return cFL(cFL_(t,colors['13']),colors['14'])
def wwA(t,ww): #for Watched State Display
	if   ww==7: t=ww7+t
	elif ww==6: t=ww6+t
	return t

### ############################################################################################################
### ############################################################################################################
def psgn(x,t=".png"):
	s="http://i.imgur.com/"; 
	try:
		return {
			'action': 					s+"Q12cars"+t
			,' action': 				s+"Q12cars"+t
			,'adventure': 			s+"wq3rlj8"+t
			,'animation': 			s+"0Dy8M70"+t
			,'cars': 						s+"e9n9Hih"+t
			#,'cartoon': 				s+"yrrvbzw"+t
			,'children': 				s+"c5fk0fK"+t
			,'comedy': 					s+"FU3VJGg"+t
			,'dementia': 				s+"trimFik"+t
			,'demons': 					s+"NHLTav4"+t
			,'drama': 					s+"w7R77Dj"+t
			#,'dub': 						s+"3nc4UkN"+t
			,'ecchi': 					s+"2Y7s1d9"+t
			,'fantasy': 				s+"tspZm16"+t
			,'game': 						s+"NSLV38b"+t
			,'harem': 					s+"VSpcIo4"+t
			,'historical': 			s+"iyxap9I"+t
			,'horror': 					s+"EueQPn7"+t
			,'josei': 					s+"hR2UNOm"+t
			,'kids': 						s+"yzh5nBq"+t
			,'magic': 					s+"DOy6zZd"+t
			,'martial arts': 		s+"Nw4rjxJ"+t
			,'mecha': 					s+"XCZYIZo"+t
			,'military': 				s+"ZMXs7Gl"+t
			,'movie': 					s+"55YtzvJ"+t
			,'music': 					s+"tgcLRfv"+t
			,'mutants': 				s+"yrj3tDt"+t
			,'mystery': 				s+"37MUY4c"+t
			#,'ona': 						s+"WvIeCaj"+t
			#,'ova': 						s+"6GPcrWB"+t
			,'parody': 					s+"3hBYM4k"+t
			,'police': 					s+"zl4qBvk"+t
			,'psychological': 	s+"75bP7sP"+t
			,'romance': 				s+"ko0OKE4"+t
			,'samurai': 				s+"DDoZmKP"+t
			,'school': 					s+"FlS7hEm"+t
			,'sci-fi': 					s+"3B0dkvt"+t
			,'science fiction': s+"3B0dkvt"+t
			,'seinen': 					s+"6vc6cwB"+t
			,'shoujo': 					s+"JAsp9PL"+t
			,'shoujo ai': 			s+"PaLhEhj"+t
			,'shounen': 				s+"PeXK8An"+t
			,'shounen ai': 			s+"uvaepAZ"+t
			,'slice of life': 	s+"rh4voyt"+t
			,'space': 					s+"QReD8P3"+t
			#,'special': 				s+"lph1IaX"+t
			,'sports': 					s+"Ji1o6uG"+t
			,'super power': 		s+"6mHg5s6"+t
			,'supernatural': 		s+"8mAz2dT"+t
			,'thriller': 				s+"ZbW3BKy"+t
			,'tournament': 			s+"b3rlVQp"+t
			,'vampire': 				s+"Kn9Yi7C"+t
			#,'yuri': 						s+"VylolyV"+t
			,'a': 		s+"OvFHLK2"+t
			,'b': 		s+"ezem9mn"+t
			,'c': 		s+"707ILz1"+t
			,'d': 		s+"BUT7dUz"+t
			,'e': 		s+"mzNtW2U"+t
			,'f': 		s+"11cykaC"+t
			,'g': 		s+"l0CvvHo"+t
			,'h': 		s+"VOupMGK"+t
			,'i': 		s+"ps3YPHq"+t
			,'j': 		s+"oNHwZWv"+t
			,'k': 		s+"TwHANG6"+t
			,'l': 		s+"xiuR2WX"+t
			,'m': 		s+"GDEAPud"+t
			,'n': 		s+"9FjSiMu"+t
			,'o': 		s+"TcR1pa0"+t
			,'p': 		s+"OGc4VBR"+t
			,'q': 		s+"hL9tEkx"+t
			,'r': 		s+"37NNHm8"+t
			,'s': 		s+"mFQswUE"+t
			,'t': 		s+"4DBQVrd"+t
			,'u': 		s+"qpovLUW"+t
			,'v': 		s+"bnu5ByY"+t
			,'w': 		s+"0IHoHV2"+t
			,'x': 		s+"ic81iKY"+t
			,'y': 		s+"46IlmRH"+t
			,'z': 		s+"PWUSCsE"+t
			,'0': 		s+"7an2n4W"+t # 0RJOmkw
			,'all': 	s+"hrWVT21"+t
			#,'search': 										s+"mDSHRJX"+t
			,'plugin settings': 					s+"K4OuZcD"+t
			,'local change log': 					s+"f1nvgAM"+t
			#,'last': 											s+"FelUdDz"+t
			#,'favorites': 								s+"lUAS5AU"+t
			#,'favorites 2': 							s+"EA49Lt3"+t
			#,'favorites 3': 							s+"lwJoUqT"+t
			#,'favorites 4': 							s+"Wr7GPTf"+t
			,'latest update': 						s+"dNCxQbg"+t
			,'completed': 								s+"xcqaTKI"+t
			,'most popular': 							s+"T9LUsM2"+t
			#,'new anime': 								s+"BGZnMf5"+t
			#,'genre': 										s+"AmQHPvY"+t
			#,'ongoing': 									s+"EUak0Sg"+t
			,'anime list all': 						s+"t8b1hSX"+t
			,'anime list alphabet': 			s+"R0w0BAM"+t
			,'anime list latest update': 	s+"XG0LGQH"+t
			,'anime list newest': 				s+"eWAeuLG"+t
			,'anime list popularity': 		s+"eTrguP1"+t
			,'urlresolver settings': 			s+"PlROfSs"+t
			,'online bookmarks': 					s+"68ih1sx"+t
			#,'alphabetical': 							s+"sddCXQo"+t
			,'genre select': 							s+"MhNenb6"+t
#			,'': 								s+""+t
#			,'': 								s+""+t
			,'about': 										s+"8BLYGft"+t
			,'alphabetical': 							s+"aLKvpQD"+t
			,'favorites': 								s+"EsfpOBt"+t
			,'favorites 1': 							s+"sfwvd2z"+t
			,'favorites 2': 							s+"yRtrel2"+t
			,'favorites 3': 							s+"oXrNjB2"+t
			,'favorites 4': 							s+"VlAya5J"+t
			,'favorites 5': 							s+"Slj9gzb"+t
			,'favorites 6': 							s+"o27Hgb0"+t
			,'favorites 7': 							s+"2vFek2a"+t
			,'genre': 										s+"XEIr4Cz"+t
			,'last': 											s+"3g6S9UH"+t
			,'latest episodes': 					s+"r19ycox"+t
			,'latest updates': 						s+"E86Rnq5"+t
			,'most popular': 							s+"N69lo3G"+t
			,'new anime': 								s+"wZN1olE"+t
			,'search': 										s+"MTnRQJ3"+t
			,'fanart': 										s+"PcZjx2D"+t
			,'ongoing': 									s+"SUiKolu"+t
			,'anime': 										s+"Q6AHcxD"+t
			,'cartoon': 									s+"MxOxr7m"+t
			,'cartoons': 									s+"gr9YXnq"+t
			,'movie': 										s+"0Ce3mE8"+t
			,'movies': 										s+"LfOe6eF"+t
			,'animes': 										s+"0gwZCUE"+t
#			,'': 								s+""+t
			,'icon': 											s+"FJRilNi"+t
#			,'': 								s+""+t
#			,'': 								s+""+t
#			,'': 								s+""+t
			,'img_next':									'http://kissanime.com/Content/images/next.png'
			,'img_prev':									'http://kissanime.com/Content/images/previous.png'
# KissAnimeGenres
# http://imgur.com/a/rws19/all
# http://imgur.com/a/rws19#Q12cars
# http://imgur.com/a/rws19
		}[x]
	except: print 'failed to find graphc for %s' % (x); return ''
### ############################################################################################################
### ############################################################################################################
def GetMedia(Url,title,imdb_id,img,fimg,stitle,etitle,enumber,snumber,enumber2,wwT=''):
	if len(snumber)==0: snumber='0'; 
	if len(Url)==0: return
	if mainSite not in Url: Url=mainSite+Url; 
	deb('imdb_id',imdb_id); deb('title',title); deb('Url',Url); html=messupText(nolines(nURL(Url)),True,True); deb('length of html',str(len(html))); #debob(html); 
	if len(html)==0: return
	###
	_addon.addon.setSetting(id="LastEpisodeListedURL", value=Url)
	_addon.addon.setSetting(id="LastEpisodeListedNAME", value=title)
	_addon.addon.setSetting(id="LastEpisodeListedIMG", value=img)
	_addon.addon.setSetting(id="LastEpisodeListedFANART", value=fimg)
	_addon.addon.setSetting(id="LastEpisodeListedIMDBID", value=imdb_id)
	_addon.addon.setSetting(id="LastEpisodeListedSTITLE", value=str(stitle))
	_addon.addon.setSetting(id="LastEpisodeListedETITLE", value=str(etitle))
	_addon.addon.setSetting(id="LastEpisodeListedEpNo", value=str(enumber))
	_addon.addon.setSetting(id="LastEpisodeListedSNo", value=str(snumber))
	_addon.addon.setSetting(id="LastEpisodeListedEpNo2", value=str(enumber2))
	###
	s='<div id="nav_container"></div></div><script type="text/javascript">var vid=eval\(unescape\("(.+?)"\)\);</script>'; 
	try: result_string=re.compile(s).findall(html)[0]; #deb('# of matches found',str(len(result_string))); debob(result_string)
	except: result_string=''; 
	if len(result_string)==0: print "couldn't find encoded result(s) string."; return
	matche=urllib.unquote_plus(result_string); debob(matche); 
	s='{"provider":"(.+?)","video_id":"(.+?)"}'; 
	try: matches=re.compile(s).findall(matche); deb('# of matches found',str(len(matches))); debob(matches)
	except: matches=''; 
	if len(matches) > 0:
		iC=len(matches); 
		try: import urlresolver
		except: pass
		for (provider,video_id) in matches:
			cMI=[]; url=''; host_id=TagHostName(provider); labs={'title':provider+" "+video_id}; 
			url=TagHostUrl(provider) % video_id; 
			if len(url) > 0:
				if urlresolver.HostedMediaFile(url).valid_url(): deb("good link",url); labs[u'title']=cFL(url,'blue'); 
				else: deb("bad link",url); labs[u'title']=cFL(url,'red'); #url=''; 
				F=1
			else: F=2
			if F==1:
				m=url; 
				pars={'mode':'PlayFromHost','url':m,'studio':stitle+' - '+str(enumber)+' - '+etitle,'title':title,'etitle':etitle,'stitle':title,'imdb_id':imdb_id,'img':img,'fimg':fimg,'site':site,'section':section,'wwT':wwT,'MarkAsWatched':'true'}; 
				#pars={'mode':'PlayFromHostMT','url':m,'studio':stitle+' - '+str(enumber)+' - '+etitle,'title':title,'etitle':etitle,'stitle':title,'imdb_id':imdb_id,'img':img,'fimg':fimg,'site':site,'section':section,'wwT':wwT,'MarkAsWatched':'true'}; 
				destfile=str(stitle)+' - s'+str(snumber)+'e'+str(enumber)+' - '+str(enumber)+' - '+str(etitle)+'.mp4'
				if (int(snumber) > 1) and (int(enumber) is not enumber2):
					destfile=str(stitle)+' - s'+str(snumber)+'e'+str(enumber2)+' - '+str(enumber)+' - '+str(etitle)+'.mp4'
				destfile=destfile.replace(':','').replace('"','').replace("'","").replace("?","")
				Clabs={'title':title,'year':'','url':m,'destfile':destfile,'img':img,'fanart':fimg,'plot':'','todoparams':_addon.build_plugin_url(pars),'site':site,'section':section}; 
				cMI=ContextMenu_Hosts(Clabs); 
				try: _addon.add_directory(pars,labs,is_folder=False,fanart=fimg,img=img,contextmenu_items=cMI,total_items=iC)
				except: pass
			#else: 
	set_view('list',view_mode=addst('links-view')); eod()

def TagHostName(HostTag):
	default=HostTag+''; t={'nova':'novamov.com','autv':'animeultima.com','vweed':'videoweed.es','veevr':'veevr.com','au':'auengine.com','ucc-u':'uploadcrazy.net','ucc-v':'vidcrazy.net','ancv-u':'uploadcrazy.net','ancv-v':'vidcrazy.net','av-u':'uploadcrazy.net','av-v':'vidcrazy.net','nvs-u':'uploadcrazy.net','nvs-v':'vidcrazy.net','yu':'yourupload.com','mp4':'MP4Upload.com','vnest':'VideoNest.net','m4s':'MP4Star.com','1':'','':'2','3':''}
	try: return t[HostTag]
	except: return default
def TagHostUrl(HostTag):
	default=HostTag+'/%s'; t={'nova':'http://www.novamov.com/video/%s','autv':'http://animeultima.tv/%s','vweed':'http://www.videoweed.es/file/%s','veevr':'http://veevr.com/videos/%s','ucc-u':'http://embeds.uploadcrazy.net/embed.php?file=%s','ucc-v':'http://video.vidcrazy.net/embed.php?file=%s','ancv-u':'http://embeds.uploadcrazy.net/ancv.php?file=%s','ancv-v':'http://video.vidcrazy.net/ancv.php?file=%s','av-u':'http://embeds.uploadcrazy.net/avid.php?file=%s','av-v':'http://video.vidcrazy.net/avid.php?file=%s','nvs-u':'http://embeds.uploadcrazy.net/nvs.php?file=%s','nvs-v':'http://video.vidcrazy.net/nvs.php?file=%s','au':'http://www.auengine.com/embed.php?file=%s&w=800&h=600','yu':'http://yourupload.com/embed/%s&width=800&height=600','0':'','mp4':'http://www.mp4upload.com/%s','vnest':'http://www.videonest.net/embed-%s-800x600.html','m4s':'http://mp4star.com/embed/%s','1':'','':'2','3':''}
	## 
	## Seem to be working: videoweed.es, uploadcrazy.net, vidcrazy.net, auengine (with plugin)
	## Seem to NOT be working: novamov.com, animeultima.tv
	## 
	try: return t[HostTag]
	except: return default

def ListLatestEpisodes(Url=mainSite+'/latest/'):
	if len(Url)==0: Url=mainSite+'/latest/'; #return
	if mainSite not in Url: Url=mainSite+Url; 
	deb('Url',Url); html=messupText(nolines(nURL(Url)),True,True); deb('length of html',str(len(html))); #debob(html); 
	if len(html)==0: return
	#else: debob(html); 
	s='<div class="\D+ \D+"><span class="\D+-image"><a href="(.+?)" class="\D+"><figure><img class="primary" src="(.+?\.[png|jpg|gif]+)" alt=".+?"><div class="overlay"><i class="icon-play"></i></div></figure></a></span><div class="\D+-details">'; 
	s+='<h3><a href="(.+?)">\s*(.+?)\s*</a></h3><div><span class="\D+-status">Status</span><span class="\D+-type \D+">(\D+)</span><span class="\D+-meta">Added (\d+ \D+) ago</span></div></div></div>'; 
	#s='<div class="\D+ \D+">\s*<span class="\D+-image">\s*<a href="(.+?)" class="\D+">\s*<figure>\s*<img class="primary" src="(.+?\.[png|jpg|gif]+)" alt=".+?">\s*<div class="overlay">\s*<i class="icon-play">\s*</i>\s*</div>\s*</figure>\s*</a>\s*</span>\s*<div class="\D+-details">'; 
	#s+='\s*<h3>\s*<a href="(.+?)">\s*(.+?)\s*</a>\s*</h3>\s*<div>\s*<span class="\D+-status">Status</span>\s*<span class="\D+-type \D+">\s*(\D+)\s*</span>\s*<span class="\D+-meta">>\s*<Added (\d+ \D+) ago\s*</span>\s*</div>\s*</div>\s*</div>'; 
	for ttt in ['\t','\n','\r','\a']: html=html.replace(ttt,'')
	try: matches=re.compile(s).findall(html); deb('# of matches found',str(len(matches))); #debob(matches)
	except: matches=''; debob('no matches were found.'); 
	if len(matches) > 0:
		iC=len(matches) * 2; enMeta=tfalse(addst("enableMeta","false")); 
		if "' class='previouspostslink'>" in html:
			try: PrEVIOUS= html.split("' class='previouspostslink'>")[0].split("<a href='")[-1]; #re.compile("<a href='(.+?)' class='previouspostslink'>").findall(html)[0]; 
			except: PrEVIOUS=Url; 
			deb('previous',PrEVIOUS); _addon.add_directory({'mode':'ListLatestEpisodes','url':PrEVIOUS,'site':site,'section':section},{'title':cFL('<< Previous','green')+'  '+PrEVIOUS},is_folder=True,fanart=fanartSite,img=psgn('img_next'))
		if enMeta==True:
			try: from metahandler import metahandlers; grab=metahandlers.MetaData(preparezip=False); 
			except: debob("filed to import metahandler"); 
		for (url,img,url2,name,sType,datestamp) in matches:
			LeftColor='blue'; showUrl=''+url2+''; showName=''; img=FixImage(img); cMI=[]; img=img.replace(' ','%20'); fimg=fanartSite; deb('img',img); Genres2=""; g="<a href='http://www.animefate.com/.genre=.+?'>\s*(.+?)\s*</a>"; plot=""; labs={}; 
			if sType.lower()=='dubbed': LeftColor='lightskyblue'; 
			elif sType.lower()=='subbed': LeftColor='forestgreen'; 
			elif sType.lower()=='movie': LeftColor='burlywood'; 
			elif sType.lower()=='cartoon': LeftColor='darkorange'; 
			if    " Season " in name: showName=name.split( " Season ")[0]; 
			elif " Episode " in name: showName=name.split(" Episode ")[0]; 
			else:                    showName=''+name+''; 
			showName=showName.replace(" English Dubbed","").replace(" English Subbed",""); 
			if "Episode " in name:
				try: e=re.compile("Episode\s*(\d+)").findall(name)[0]; 
				except: e=""; 
			else: e=""; 
			if "Season " in name:
				try: s=re.compile("Season\s*(\d+)").findall(name)[0]; 
				except: s="1"; 
			else: s="1"; 
			wwT=showName+" ~~ "+name; 
			try:
				if visited_check2(wwT)==True: ww=7
				else: ww=6
			except: ww=6
			if enMeta==True: 
				try: labs=grab.get_meta('tvshow',TagAnimeName(showName)); 
				except: pass
				#try:
				#	if len(labs[u'cover_url']) > 0: img=labs[u'cover_url']; 
				#except: pass
				try:
					if len(labs[u'backdrop_url']) > 0: fimg=labs[u'backdrop_url']; 
				except: pass
			else: labs[u'plot']=''; labs[u'imdb_id']=''; labs[u'title']=name; labs[u'year']=''; 
			##labs[u'plot']=''; labs[u'imdb_id']=''; labs[u'title']=name; labs[u'year']=''; 
			labs[u'title']=name; 
			#
			##plot+=CR+"Genres:  [COLOR purple]"+Genres2+"[/COLOR]"; plot+="[CR]Year: [COLOR purple]"+year+"[/COLOR]"; plot+=" [COLOR black]|[/COLOR] Status: [COLOR purple]"+status+"[/COLOR]"; plot+=" [COLOR black]|[/COLOR] Episodes: [COLOR purple]"+NoEps+"[/COLOR]"; 
			pars={'mode':'GetMedia','url':url,'title':name,'imdb_id':labs[u'imdb_id'],'img':img,'fimg':fimg,'site':site,'section':section,'e':str(e),'s':str(1),'e2':str(e),'e3':str(0)}; 
			labs[u'plot']=plot+CR+CR+cFL(labs[u'plot'],'mediumpurple'); labs[u'title']=cFL(name,LeftColor); 
			labs[u'plot']=messupText(labs[u'plot'],True,True,True); labs[u'title']=messupText(labs[u'title'],True,True,True); 
			labs[u'plot']=CR+cFL('['+sType+']',LeftColor)+labs[u'plot']; 
			labs[u'title']=labs[u'title'].replace(" English Dubbed","").replace(" English Subbed",""); 
			if (" Season "+str(s)) in labs[u'title']: labs[u'title']=labs[u'title'].replace(" Season "+str(s),"[COLOR darkolivegreen] s"+str(s))+"[/COLOR]"; 
			if (" Episode "+str(e)) in labs[u'title']: labs[u'title']=labs[u'title'].replace(" Episode "+str(e),"[COLOR darkorchid] e"+str(e))+"[/COLOR]"; 
			labs[u'title']+=''+cFL("  ["+sType+"]",LeftColor); 
			##labs[u'title']+=cFL(' ('+cFL(year,'mediumpurple')+') ['+cFL(NoEps,'blue')+']'+CR+'['+status+']','purple')
			#labs[u'title']+=CR+cFL('['+datestamp+']',colors['13']); 
			labs[u'title']+=CR+wwA(cFL('['+datestamp+']',colors['13']),ww); 
			#labs[u'title']=wwA(labs[u'title'],ww); 
			Clabs={'title':name,'year':labs[u'year'],'url':url,'img':img,'fanart':fimg,'plot':labs[u'plot'],'todoparams':_addon.build_plugin_url(pars),'site':site,'section':section}; 
			try: cMI=ContextMenu_Episodes(Clabs); 
			except: pass
			#cMI=wwCMI(cMI,ww,wwT); 
			### Episode
			#try: labs2=copy.deepcopy(labs); 
			#except: labs2=labs; 
			#labs2[u'title']=showName; 
			#pars2={'mode':'ListEpisodes','url':showUrl,'title':name,'imdb_id':labs[u'imdb_id'],'img':img,'fimg':fimg,'site':site,'section':section}; 
			#labs2[u'title']=AFColoring(showName); 
			#Clabs2={'title':name,'year':labs[u'year'],'url':url,'commonid':labs[u'imdb_id'],'img':img,'fanart':fimg,'plot':labs[u'plot'],'todoparams':_addon.build_plugin_url(pars2),'site':site,'section':section}; 
			#try: cMI2=ContextMenu_Series(Clabs2); 
			#except: pass
			#try: _addon.add_directory(pars2,labs2,is_folder=True,fanart=fimg,img=img,contextmenu_items=cMI2,total_items=iC)
			#except: pass
			### Show
			try: _addon.add_directory(pars,labs,is_folder=True,fanart=fimg,img=img,contextmenu_items=cMI,total_items=iC)
			except: pass
		if "' class='nextpostslink'>" in html:
			try: NeXT=html.split("' class='nextpostslink'>")[0].split("<a href='")[-1]; #re.compile("</span><a href='("+mainSite+"/.+?/)' class='nextpostslink'>").findall(html)[0]; 
			except: NeXT=Url; 
			deb('next',NeXT); _addon.add_directory({'mode':'ListLatestEpisodes','url':NeXT,'site':site,'section':section},{'title':cFL('>> Next','green')+'  '+NeXT},is_folder=True,fanart=fanartSite,img=psgn('img_next'))
		if "' class='last'>Last " in html:
			try: LaST=html.split("' class='last'>Last ")[0].split("<a href='")[-1]; #re.compile("<a href='("+mainSite+"/.+?/)' class='last'>Last ").findall(html)[0]; 
			except: LaST=Url; 
			deb('last',LaST); _addon.add_directory({'mode':'ListLatestEpisodes','url':LaST,'site':site,'section':section},{'title':cFL('>> >> Last','green')+'  '+LaST},is_folder=True,fanart=fanartSite,img=psgn('img_next'))
	#set_view('tvshows',view_mode=addst('tvshows-view')); eod(); 
	set_view('episodes',view_mode=addst('episode-view')); eod(); 

def ListEpisodes(Url,title,imdb_id,img,fimg):
	debob([Url,title,imdb_id,img,fimg])
	if len(Url)==0: return
	if mainSite not in Url: Url=mainSite+Url; 
	deb('imdb_id',imdb_id); deb('title',title); deb('Url',Url); html=messupText(nolines(nURL(Url)),True,True); deb('length of html',str(len(html))); #debob(html); 
	if imdb_id=='0': imdb_id=''; 
	if len(html)==0: return
	###
	_addon.addon.setSetting(id="LastShowListedURL", value=Url)
	_addon.addon.setSetting(id="LastShowListedNAME", value=title)
	_addon.addon.setSetting(id="LastShowListedIMG", value=img)
	_addon.addon.setSetting(id="LastShowListedFANART", value=fimg)
	_addon.addon.setSetting(id="LastShowListedIMDBID", value=imdb_id)
	###
	#s='<li>\s*\n*\s*<a href="(http://www.animefate.com/.+?/)" rel="bookmark" title=".+?">\s*\n*\s*<p class="episode_number">\s*(.+?)\s*</p>\s*\n*\s*<p title="Added on .+?" class="date_published">(.+?)</p>\s*\n*\s*</a>\s*\n*\s*<div class="clear"></div>\s*\n*\s*</li>'; 
	s='<li><a class="(.+?)" href="(http://www.justanimestream.net/.+?/.+?/)"><i class="icon-angle-right" style="color:#([0-9A-Za-z]+)"></i>\s*(.+?\s*(\d*))\s*</a></li>'; 
	for ttt in ['\t','\n','\r','\a']: html=html.replace(ttt,'')
	try: matches=re.compile(s).findall(html); deb('# of matches found',str(len(matches))); #debob(matches)
	except: matches=''; debob('no matches were found.'); 
	if len(matches) > 0:
		s='1'; enMeta=tfalse(addst("enableMeta","false")); 
		iC=len(matches); n=False; e3='0'
		if enMeta==True:
			try: from metahandler import metahandlers; grab=metahandlers.MetaData(preparezip=False); 
			except: debob("filed to import metahandler"); 
			#ShowLabs=grab.get_seasons(tvshowtitle=title,imdb_id=imdb_id,seasons=s,overlay=6); debob(ShowLabs); 
			#labsZ=grab.get_episode_meta(tvshowtitle=title,imdb_id=imdb_id,season=s,episode='1',air_date='',episode_title='',overlay=6); debob(labsZ); 
		#matches=sorted(matches,key=lambda nn: (nn[1]),reverse=True)
		if 'Movie ' in title: s='0'; enMeta=False; 
		for (sType,url,StyleColor,name,ENumber) in matches: #[::-1]:
			debob([url,StyleColor,name,ENumber]); 
			LeftColor='blue'; cMI=[]; labs={}; #labs['plot']=''; labs['plotoutline']=''; labs['showtitle']=''; labs['episodetitle']=''; labs['videoid']=''; 
			if sType.lower()=='dubbed': LeftColor='lightskyblue'; 
			elif sType.lower()=='subbed': LeftColor='forestgreen'; 
			elif sType.lower()=='movie': LeftColor='burlywood'; 
			if "Episode " in name: 
				try: e=re.compile("Episode\s*(\d+)").findall(name)[0]; 
				except: e=""; 
				if len(str(e))==0:
					try: e=re.compile("Movie\s*(\d+)").findall(name)[0]; 
					except: e=""; 
			else: e=""; 
			name=name.replace(title,''); e2=copy.deepcopy(e); 
			#name=name.replace(title+" Episode","Episode")
			if (e=='1') or (e==''): s='1'; 
			wwT=title+" ~~ "+name
			try:
				if visited_check(wwT)==True: ww=7
				else: ww=6
			except: ww=6
			if (enMeta==True) and (len(imdb_id) > 1):
				#s='1'; 
				if len(e) > 0:
					###
					if int(s) > 1:
						e2=str(int(e)-int(e3))
					###
					#try: labs=grab.get_episode_meta(tvshowtitle=title,imdb_id=imdb_id,season=s,episode=e2,air_date='',episode_title='',overlay=6); 
					try: labs=grab.get_episode_meta(tvshowtitle=title,imdb_id=imdb_id,season=s,episode=e2,air_date='',episode_title='',overlay=ww); 
					except: n=True;
					###
					#debob(labs); 
					try:
						if (len(labs['title'])==0) and (len(labs['plot'])==0) and (len(labs['episode_id'])==0):
							s=str(int(s)+1); e3=str(int(e)-1)
							e2=str(int(e)-int(e3))
							try: labs=grab.get_episode_meta(tvshowtitle=title,imdb_id=imdb_id,season=s,episode=e2,air_date='',episode_title='',overlay=6); 
							except: n=True;
					except: pass
					
					###
					try:
						if len(labs[u'cover_url']) > 0: img=labs[u'cover_url']; 
					except: pass
					try:
						if len(labs[u'backdrop_url']) > 0: fimg=labs[u'backdrop_url']; 
					except: pass
					#try: tt=labs[u'title']; 
					#except: n=True; 
					#if len(labs[u'title'])==0: n=True; 
				else: n=True; 
			else: n=True; 
			if n==True: labs[u'plot']=''; labs[u'imdb_id']=''; labs[u'title']=name; labs[u'year']=''; labs[u'overlay']=ww
			if len(labs[u'title'])==0: labs[u'title']=name; 
			if len(labs[u'title'])==0: labs[u'title']=title; 
			#elif labs[u'title']==" ": labs[u'title']=name; 
			#labs[u'title']=labs[u'title'].replace(title+" Episode","Episode")
			etitle=labs[u'title']; 
			#labs[u'title']=cFL(str(e)+') ',LeftColor)+AFColoring(labs[u'title']); 
			if len(e) > 0: labs[u'title']=cFL(str(e)+') ',LeftColor)+AFColoring(labs[u'title']); 
			else: labs[u'title']=AFColoring(labs[u'title'])
			labs[u'plot']=CR+cFL(labs[u'plot'],'mediumpurple'); 
			labs[u'plot']=CR+cFL('['+sType+']',LeftColor)+labs[u'plot']; 
			#labs[u'title']+=CR+cFL("["+datestamp+"]",colors['13']); 
			labs[u'plot']+=CR+cFL(str(e)+")",LeftColor)+cFL(" Season "+cFL(str(s),colors['13'])+" Episode "+cFL(str(e2),colors['13'])+"",'mediumpurple')
			labs[u'title']+=''+cFL("  ["+sType+"]",LeftColor); 
			labs[u'title']=wwA(labs[u'title'],ww); 
			debob(labs); 
			pars={'mode':'GetMedia','url':url,'title':name,'etitle':etitle,'stitle':title,'imdb_id':labs[u'imdb_id'],'img':img,'fimg':fimg,'site':site,'section':section,'e':str(e),'s':str(s),'e2':str(e2),'e3':str(e3),'wwT':wwT}; 
			Clabs={'title':name,'year':'','url':url,'img':img,'fanart':fimg,'plot':labs[u'plot'],'todoparams':_addon.build_plugin_url(pars),'site':site,'section':section}; 
			try: cMI=ContextMenu_Episodes(Clabs); 
			except: pass
			try: cMI=wwCMI(cMI,ww,wwT); 
			except: pass
			try: _addon.add_directory(pars,labs,is_folder=True,fanart=fimg,img=img,contextmenu_items=cMI,total_items=iC)
			except: pass
	set_view('episodes',view_mode=addst('episode-view')); eod()

def TagAnimeName(animename):
	#return animename
	try:
		if animename=='Golden Time': animename+=' (2013)'
		#if animename=='Witch Craft Works': animename='Witch Craft Works (2014)'
		if animename=='Perfect Blue': animename+=' (1997)'
		if animename=='Kingdom': animename+=' (2012)'
		if animename=='Kingdom 2': animename='Kingdom (2012)'
		if animename=='Weiss Survive R': animename='Weiss Survive'
		if animename=='Jem and the Holograms': animename='Jem'
		return animename
	except: return animename


def ListShows(Url):
	if len(Url)==0: return
	if mainSite not in Url: Url=mainSite+Url; 
	deb('Url',Url); html=messupText(nolines(nURL(Url)),True,True); deb('length of html',str(len(html))); #debob(html); 
	if len(html)==0: return
	for ttt in ['\t','\n','\r','\a']: html=html.replace(ttt,'')
	#debob(html); 
	#s='<div class="span3" style=".+?"><div class="item"><a href="(http://.+?)" data-toggle="tooltip" data-placement="right" data-original-title=".+?"><figure><img src="(.+?\.[jpg|png|gif]+)" class=".+?" alt=".+?" width="\d+px" height="\d+px"/><div class="overlay"><i class="icon-play"></i></div></figure><article><h5>(.+?)</h5></article></a></div></div>'; 
	s='<div class="span3" style=".+?"><div class="item"><a href="(http://.+?)" data-toggle="tooltip" data-placement="right" data-original-title=".+?"><figure><img src="(.+?\.[jpg|png|gif]+)" class=".+?" alt=".+?" width="\d+px" height="\d+px"\s*/><div class="overlay"><i class="icon-play"></i></div></figure><article><h5>(.+?)</h5></article></a></div'; 
	#if mainSite+'/?s=' in Url: s='<div class="span3" style="width:\d+px;margin-left:1%;margin-bottom:10px;"><div class="item"><a href="http://www.justanimestream.net/anime-series/gantz-ii-perfect-answer/" data-toggle="tooltip" data-placement="right" data-original-title="Gantz II: Perfect Answer"><figure><img src="/bimages/gantz-ii-perfect-answer.jpg" class="animethumbs" alt="Gantz II: Perfect Answer" width="125px" height="190px"/><div class="overlay"><i class="icon-play"></i></div></figure><article><h5>(.+?)</h5></article></a></div></div>'; 
	### url,img,name
	try: matches=re.compile(s).findall(html); deb('# of matches found',str(len(matches))); #debob(matches)
	except: matches=''; debob('no matches were found.'); 
	if len(matches) > 0:
		iC=len(matches); enMeta=tfalse(addst("enableMeta","false")); 
		if "' class='previouspostslink'>" in html:
			try: PrEVIOUS= html.split("' class='previouspostslink'>")[0].split("<a href='")[-1]; #re.compile("<a href='(.+?)' class='previouspostslink'>").findall(html)[0]; 
			except: PrEVIOUS=Url; 
			deb('previous',PrEVIOUS); _addon.add_directory({'mode':'ListShows','url':PrEVIOUS,'site':site,'section':section},{'title':cFL('<< Previous','green')+'  '+PrEVIOUS},is_folder=True,fanart=fanartSite,img=psgn('img_next'))
		if enMeta==True:
			try: from metahandler import metahandlers; grab=metahandlers.MetaData(preparezip=False); 
			except: debob("filed to import metahandler"); 
		for (url,img,name) in matches:
			img=FixImage(img); cMI=[]; img=img.replace(' ','%20'); fimg=fanartSite; deb('img',img); Genres2=""; g="<a href='http://www.animefate.com/.genre=.+?'>\s*(.+?)\s*</a>"; plot=""; labs={}; 
			genres=""; 
			#try: Genres1=re.compile(g).findall(genres); debob(Genres1); 
			#except: Genres1=""; 
			#for g in Genres1: Genres2+="["+g+"] "; 
			#Genres2=str(Genres1); 
			wwT=name+" ~~ "; 
			try:
				if visited_check2(wwT)==True: ww=7
				else: ww=6
			except: ww=6
			if enMeta==True: 
				try: labs=grab.get_meta('tvshow',TagAnimeName(name),overlay=ww); debob(labs); 
				except: pass
				try:
					if len(labs[u'cover_url']) > 0: img=labs[u'cover_url']; 
				except: pass
				try:
					if len(labs[u'backdrop_url']) > 0: fimg=labs[u'backdrop_url']; 
				except:
					try:
						if len(labs['backdrop_url']) > 0: fimg=labs['backdrop_url']; 
					except: pass
			else: labs[u'plot']=''; labs[u'imdb_id']=''; labs[u'title']=''+name; labs[u'year']=''; 
			try:
				if len(labs['imdb_id'])==0: labs[u'imdb_id']=''
			except: labs[u'imdb_id']=''
			#plot+=CR+"Genres:  [COLOR purple]"+Genres2+"[/COLOR]"; #plot+="[CR]Year: [COLOR purple]"+year+"[/COLOR]"; #plot+="[CR]Status: [COLOR purple]"+status+"[/COLOR]"; #plot+="[CR]Number of Episodes: [COLOR purple]"+NoEps+"[/COLOR]"; 
			pars={'mode':'ListEpisodes','url':url,'title':name,'imdb_id':labs[u'imdb_id'],'img':img,'fimg':fimg,'site':site,'section':section}; 
			labs[u'plot']=plot+CR+cFL(labs[u'plot'],'mediumpurple'); labs[u'title']=AFColoring(name); 
			#Clabs=labs; 
			labs[u'title']=wwA(labs[u'title'],ww); 
			Clabs={'title':name,'year':labs[u'year'],'url':url,'commonid':labs[u'imdb_id'],'img':img,'fanart':fimg,'plot':labs[u'plot'],'todoparams':_addon.build_plugin_url(pars),'site':site,'section':section}; 
			try: cMI=ContextMenu_Series(Clabs); 
			except: pass
			try: _addon.add_directory(pars,labs,is_folder=True,fanart=fimg,img=img,contextmenu_items=cMI,total_items=iC,context_replace=True)
			except: pass
		#<a href='http://www.justanimestream.net/genres/drama/page/2/' class='nextpostslink'>
		if "' class='nextpostslink'>" in html:
			try: NeXT=html.split("' class='nextpostslink'>")[0].split("<a href='")[-1]; #re.compile("</span><a href='("+mainSite+"/.+?/)' class='nextpostslink'>").findall(html)[0]; 
			except: NeXT=Url; 
			deb('next',NeXT); _addon.add_directory({'mode':'ListShows','url':NeXT,'site':site,'section':section},{'title':cFL('>> Next','green')+'  '+NeXT},is_folder=True,fanart=fanartSite,img=psgn('img_next'))
		if "' class='last'>Last " in html:
			try: LaST=html.split("' class='last'>Last ")[0].split("<a href='")[-1]; #re.compile("<a href='("+mainSite+"/.+?/)' class='last'>Last ").findall(html)[0]; 
			except: LaST=Url; 
			deb('last',LaST); _addon.add_directory({'mode':'ListShows','url':LaST,'site':site,'section':section},{'title':cFL('>> >> Last','green')+'  '+LaST},is_folder=True,fanart=fanartSite,img=psgn('img_next'))
	set_view('tvshows',view_mode=addst('tvshows-view')); eod()

def ListShows2(Url):
	if len(Url)==0: return
	if mainSite not in Url: Url=mainSite+Url; 
	deb('Url',Url); html=messupText(nolines(nURL(Url)),True,True); deb('length of html',str(len(html))); #debob(html); 
	if len(html)==0: return
	s='<div class=\'anime_list_info\s*[clear]*\'>\s*<a href="(http://www.animefate.com/series/.+?/)" title=".+? English Dubbed Anime">\s*\n*\s*<div class="info_list_cover">\s*\n*\s*'; s+='<img src="(http://www.animefate.com/images/.+?-\d+x\d+.[jpg|png|gif]+)" alt=".+?" title=".+?" />\s*\n*\s*</div>\s*\n*\s*<div class="info_list_description">\s*\n*\s*'; s+='<p class=\'anime_list_title\'><strong>(.+?)</strong></p></a><p><strong>Genres: </strong>(.+?)'; s+='<p><strong>Status: </strong><span class=\'.+?\'>\s*(\D+)\s*</span></p>'; s+='<p><strong>No. of Episodes: </strong>\s*(\d*)\s*</p><p><strong>Released: </strong>\s*(\d*)\s*</p>\s*\n*\s*</div>\s*\n*\s*</div>'; 
	for ttt in ['\t','\n','\r','\a']: html=html.replace(ttt,'')
	try: matches=re.compile(s).findall(html); deb('# of matches found',str(len(matches))); debob(matches)
	except: matches=''; debob('no matches were found.'); 
	if len(matches) > 0:
		iC=len(matches); enMeta=tfalse(addst("enableMeta","false")); 
		if Url=='http://www.animefate.com/anime-list/?starting_char=all': enMeta=False
		if enMeta==True:
			try: from metahandler import metahandlers; grab=metahandlers.MetaData(preparezip=False); 
			except: debob("filed to import metahandler"); 
		#for (img,url,name,genres) in matches:
		for (url,img,name,genres,status,NoEps,year) in matches:
			img=FixImage(img); cMI=[]; img=img.replace(' ','%20'); fimg=fanartSite; deb('img',img); Genres2=""; g="<a href='http://www.animefate.com/.genre=.+?'>\s*(.+?)\s*</a>"; plot=""; labs={}; 
			try: Genres1=re.compile(g).findall(genres); debob(Genres1); 
			except: Genres1=""; 
			for g in Genres1: Genres2+="["+g+"] "; 
			#Genres2=str(Genres1); 
			if enMeta==True: 
				try: labs=grab.get_meta('tvshow',name,year=year); debob(labs); 
				except: pass
				try:
					if len(labs[u'cover_url']) > 0: img=labs[u'cover_url']; 
				except: pass
				try:
					if len(labs[u'backdrop_url']) > 0: fimg=labs[u'backdrop_url']; 
				except: pass
			else: labs[u'plot']=''; labs[u'imdb_id']=''; labs[u'title']=name; labs[u'year']=''; 
			plot+=CR+"Genres:  [COLOR purple]"+Genres2+"[/COLOR]"; 
			plot+="[CR]Year: [COLOR purple]"+year+"[/COLOR]"; 
			plot+=" [COLOR black]|[/COLOR] Status: [COLOR purple]"+status+"[/COLOR]"; 
			plot+=" [COLOR black]|[/COLOR] Episodes: [COLOR purple]"+NoEps+"[/COLOR]"; 
			pars={'mode':'ListEpisodes','url':url,'title':name,'imdb_id':labs[u'imdb_id'],'img':img,'fimg':fimg,'site':site,'section':section}; 
			labs[u'plot']=plot+CR+CR+cFL(labs[u'plot'],'mediumpurple'); labs[u'title']=AFColoring(name); 
			labs[u'plot']=messupText(labs[u'plot'],True,True,True); labs[u'title']=messupText(labs[u'title'],True,True,True); 
			#Clabs=labs; 
			Clabs={'title':name,'year':labs[u'year'],'url':url,'commonid':labs[u'imdb_id'],'img':img,'fanart':fimg,'plot':labs[u'plot'],'todoparams':_addon.build_plugin_url(pars),'site':site,'section':section}; 
			try: cMI=ContextMenu_Series(Clabs); 
			except: pass
			labs[u'title']+=cFL(' ('+cFL(year,'mediumpurple')+') ['+cFL(NoEps,'blue')+']'+CR+'['+status+']',colors['13'])
			try: _addon.add_directory(pars,labs,is_folder=True,fanart=fimg,img=img,contextmenu_items=cMI,total_items=iC)
			except: pass
	set_view('tvshows',view_mode=addst('tvshows-view')); eod()

def Fav_List(site='',section='',subfav=''):
	debob(['test1',site,section,subfav]); 
	favs=fav__COMMON__list_fetcher(site=site,section=section,subfav=subfav); 
	ItemCount=len(favs); 
	debob('test2 - '+str(ItemCount)); 
	if len(favs)==0: myNote('Favorites','None Found'); eod(); return
	favs=sorted(favs,key=lambda item: (item[0],item[1]),reverse=False); 
	debob(favs); 
	for (_name,_year,_img,_fanart,_Country,_Url,_plot,_Genres,_site,_subfav,_section,_ToDoParams,_commonID,_commonID2) in favs:
		debob([_name,_year,_img,_fanart,_Country,_Url,_plot,_Genres,_site,_subfav,_section,_ToDoParams,_commonID,_commonID2]); 
		if _img > 0: img=_img
		else: img=iconSite
		if _fanart > 0: fimg=_fanart
		else: fimg=fanartSite
		debob('_ToDoParams'); debob(_ToDoParams)
		pars=_addon.parse_query(_ToDoParams)
		pars[u'fimg']=_fanart; pars[u'img']=_img; 
		#if len(_commonID) > 0: pars['imdb_id']=_commonID
		try:
			if len(pars['imdb_id']) > 0: pars['imdb_id']='0'; 
		except: pars['imdb_id']='0'; 
		debob('pars'); debob(pars)
		_title=AFColoring(_name)
		if (len(_year) > 0) and (not _year=='0000'): _title+=cFL('  ('+cFL(_year,'mediumpurple')+')',colors['13'])
		if len(_Country) > 0: _title+=cFL('  ['+cFL(_Country,'mediumpurple')+']',colors['13'])
		wwT=_name+" ~~ "; 
		try:
			if visited_check2(wwT)==True: ww=7
			else: ww=6
		except: ww=6
		contextLabs={'title':_name,'year':_year,'img':_img,'fanart':_fanart,'country':_Country,'url':_Url,'plot':_plot,'genres':_Genres,'site':_site,'subfav':_subfav,'section':_section,'todoparams':_ToDoParams,'commonid':_commonID,'commonid2':_commonID2}
		##contextLabs={'title':_name,'year':'0000','url':_url,'img':img,'fanart':fimg,'DateAdded':'','todoparams':_addon.build_plugin_url(pars),'site':site,'section':section}
		contextMenuItems=ContextMenu_Favorites(contextLabs)
		contextMenuItems.append( ('Empty List','XBMC.RunPlugin(%s)' % _addon.build_plugin_url({'mode':'cFavoritesEmpty','site':site,'section':section,'subfav':subfav}) ) )
		#contextMenuItems=[]
		_title=wwA(_title,ww); 
		_addon.add_directory(pars,{'title':_title,'plot':_plot},is_folder=True,fanart=fimg,img=img,total_items=ItemCount,contextmenu_items=contextMenuItems)
		#
	#
	if 'movie' in section.lower(): content='movies'
	else: content='tvshows'
	set_view(content,view_mode=int(addst('tvshows-view'))); eod()


### ############################################################################################################
### ############################################################################################################
def MenuAZ(url):
	#_addon.add_directory({'mode':'ListShows','url':url+'/','site':site,'section':section},{'title':AFColoring('ALL')},is_folder=True,fanart=fanartSite,img=psgn('all')); 
	_addon.add_directory({'mode':'ListShows','url':url+'/0/','site':site,'section':section},{'title':AFColoring('#')},is_folder=True,fanart=fanartSite,img=psgn('0')); 
	for az in MyAlphabet:
		az=az.upper(); _addon.add_directory({'mode':'ListShows','url':url+'/'+az.lower()+'/','site':site,'section':section},{'title':AFColoring(az)},is_folder=True,fanart=fanartSite,img=psgn(az.lower())); 
	set_view('list',view_mode=addst('default-view')); eod()

def DoSearch(title='',Url='/?s='):
	if len(Url)==0: return
	if mainSite not in Url: Url=mainSite+Url; 
	if len(title)==0: title=showkeyboard(txtMessage=title,txtHeader="Search:  ("+site+")")
	if (title=='') or (title=='none') or (title==None) or (title==False): return
	deb('Searching for',title); title=title.replace('+','%2B').replace('&','%26').replace('?','%3F').replace(':','%3A').replace(',','%2C').replace('/','%2F').replace('=','%3D').replace('@','%40').replace(' ','+'); 
	deb('Searching for',title); ListShows( Url+( title.replace(' ','+') ) ); 

def MenuGenre():
	for az in MyGenres: 
		i=psgn(az.lower())
		if len(i)==0: i=iconSite
		_addon.add_directory({'mode':'ListShows','url':'/genres/'+az.lower().replace(' ','-')+'/','site':site,'section':section},{'title':AFColoring(az)},is_folder=True,fanart=fanartSite,img=i); 
	set_view('list',view_mode=addst('default-view')); eod()

def SectionMenu():
	_addon.add_directory({'mode':'ListLatestEpisodes1','site':site},{'title':AFColoring('Latest Episodes')},is_folder=True,fanart=fanartSite,img=psgn('latest episodes'))
	_addon.add_directory({'mode':'ListShows','site':site,'url':'/popular/'},{'title':AFColoring('Popular')},is_folder=True,fanart=fanartSite,img=psgn('most popular'))
	_addon.add_directory({'mode':'MenuGenre','site':site},{'title':AFColoring('Genre List')},is_folder=True,fanart=fanartSite,img=psgn('genre'))
	_addon.add_directory({'mode':'MenuAZ','site':site,'url':'/browse-anime'},{'title':AFColoring('Anime List')},is_folder=True,fanart=fanartSite,img=psgn('anime'))
	_addon.add_directory({'mode':'MenuAZ','site':site,'url':'/browse-cartoon'},{'title':AFColoring('Cartoon List')},is_folder=True,fanart=fanartSite,img=psgn('cartoons'))
	_addon.add_directory({'mode':'MenuAZ','site':site,'url':'/browse-movie/'},{'title':AFColoring('Movie List')},is_folder=True,fanart=fanartSite,img=psgn('movies'))
	
	if _debugging==True:
		_addon.add_directory({'mode':'ListShows','site':site,'url':'/ongoing/'},{'title':AFColoring('Ongoing Anime')},is_folder=True,fanart=fanartSite,img=psgn('ongoing'))
	
	_addon.add_directory({'mode':'Search','site':site,'url':'/?s='},{'title':AFColoring('Search')},is_folder=True,fanart=fanartSite,img=psgn('search'))
	
	##debob(urllib.unquote_plus("%5b%5b%7b%22%70%72%6f%76%69%64%65%72%22%3a%22%6e%6f%76%61%22%2c%22%76%69%64%65%6f%5f%69%64%22%3a%22%35%6f%34%61%67%31%74%35%72%6a%69%79%62%22%7d%5d%2c%5b%7b%22%70%72%6f%76%69%64%65%72%22%3a%22%61%75%74%76%22%2c%22%76%69%64%65%6f%5f%69%64%22%3a%22%33%30%34%35%39%37%22%7d%5d%2c%5b%7b%22%70%72%6f%76%69%64%65%72%22%3a%22%6e%6f%76%61%22%2c%22%76%69%64%65%6f%5f%69%64%22%3a%22%6b%79%75%32%79%74%39%33%69%72%63%72%65%22%7d%5d%2c%5b%7b%22%70%72%6f%76%69%64%65%72%22%3a%22%61%75%74%76%22%2c%22%76%69%64%65%6f%5f%69%64%22%3a%22%35%36%36%34%33%37%22%7d%5d%2c%5b%7b%22%70%72%6f%76%69%64%65%72%22%3a%22%76%77%65%65%64%22%2c%22%76%69%64%65%6f%5f%69%64%22%3a%22%74%73%39%6d%66%6b%76%64%32%78%39%74%6b%22%7d%5d%2c%5b%7b%22%70%72%6f%76%69%64%65%72%22%3a%22%76%65%65%76%72%22%2c%22%76%69%64%65%6f%5f%69%64%22%3a%22%6b%79%54%6a%2d%77%56%61%66%22%7d%5d%5d")); 
	
	##_addon.add_directory({'mode':'ListLatestShows','site':site},{'title':AFColoring('Latest Series')},is_folder=True,fanart=fanartSite,img=psgn('new anime'))
	##_addon.add_directory({'mode':'ListPopularShows','site':site},{'title':AFColoring('Popular Anime Series')},is_folder=True,fanart=fanartSite,img=psgn('most popular'))
	#
	_addon.add_directory({'mode':'FavoritesList','site':site,'section':section             },{'title':cFL(ps('WhatRFavsCalled'),colors['13'])+cFL(addst('fav.tv.1.name'),colors['14'])},fanart=fanartSite,img=psgn('favorites 1'))
	_addon.add_directory({'mode':'FavoritesList','site':site,'section':section,'subfav':'2'},{'title':cFL(ps('WhatRFavsCalled'),colors['13'])+cFL(addst('fav.tv.2.name'),colors['14'])},fanart=fanartSite,img=psgn('favorites 2'))
	_addon.add_directory({'mode':'FavoritesList','site':site,'section':section,'subfav':'3'},{'title':cFL(ps('WhatRFavsCalled'),colors['13'])+cFL(addst('fav.tv.3.name'),colors['14'])},fanart=fanartSite,img=psgn('favorites 3'))
	_addon.add_directory({'mode':'FavoritesList','site':site,'section':section,'subfav':'4'},{'title':cFL(ps('WhatRFavsCalled'),colors['13'])+cFL(addst('fav.tv.4.name'),colors['14'])},fanart=fanartSite,img=psgn('favorites 4'))
	_addon.add_directory({'mode':'FavoritesList','site':site,'section':section,'subfav':'5'},{'title':cFL(ps('WhatRFavsCalled'),colors['13'])+cFL(addst('fav.tv.5.name'),colors['14'])},fanart=fanartSite,img=psgn('favorites 5'))
	_addon.add_directory({'mode':'FavoritesList','site':site,'section':section,'subfav':'6'},{'title':cFL(ps('WhatRFavsCalled'),colors['13'])+cFL(addst('fav.tv.6.name'),colors['14'])},fanart=fanartSite,img=psgn('favorites 6'))
	_addon.add_directory({'mode':'FavoritesList','site':site,'section':section,'subfav':'7'},{'title':cFL(ps('WhatRFavsCalled'),colors['13'])+cFL(addst('fav.tv.7.name'),colors['14'])},fanart=fanartSite,img=psgn('favorites 7'))
	###
	if (len(addst("LastShowListedURL")) > 0): 
		pars={'site':site,'section':section,'mode':'ListEpisodes','url':addst("LastShowListedURL"),'title':addst("LastShowListedNAME"),'imdb_id':addst("LastShowListedIMDBID"),'img':addst("LastShowListedIMG"),'fimg':addst("LastShowListedFANART")}; 
		title=AFColoring(addst("LastShowListedNAME"))+CR+cFL('[Last Show]',colors['13']); 
		_addon.add_directory(pars,{'title':title},fanart=addst("LastShowListedFANART"),img=addst("LastShowListedIMG"),is_folder=True); 
	if (len(addst("LastEpisodeListedURL")) > 0): 
		pars={'site':site,'section':section,'mode':'GetMedia','url':addst("LastEpisodeListedURL"),'title':addst("LastEpisodeListedNAME"),'imdb_id':addst("LastEpisodeListedIMDBID"),'img':addst("LastEpisodeListedIMG"),'fimg':addst("LastEpisodeListedFANART"),'stitle':addst("LastEpisodeListedSTITLE"),'etitle':addst("LastEpisodeListedETITLE"),'e':addst("LastEpisodeListedEpNo"),'s':addst("LastEpisodeListedSNo"),'e2':addst("LastEpisodeListedEpNo2")}; 
		title=AFColoring(addst("LastEpisodeListedNAME"))+CR+cFL('[Last Episode]',colors['13']); 
		_addon.add_directory(pars,{'title':title},fanart=addst("LastEpisodeListedFANART"),img=addst("LastEpisodeListedIMG"),is_folder=True); 
	###
	_addon.add_directory({'mode':'About','site':site,'section':section},{'title':AFColoring('About')},is_folder=True,fanart=fanartSite,img='http://i.imgur.com/0h78x5V.png') # iconSite
	###
	set_view('list',view_mode=addst('default-view')); eod()
### ############################################################################################################
### ############################################################################################################
def mode_subcheck(mode='',site='',section='',url=''):
	deb('mode',mode); 
	if (mode=='SectionMenu'): 		SectionMenu()
	elif (mode=='') or (mode=='main') or (mode=='MainMenu'): SectionMenu()
	elif (mode=='SubMenu'): 			SubMenu()
	elif (mode=='ListShows'): 		ListShows(url)
	elif (mode=='ListShows2'): 		ListShows2(url)
	elif (mode=='ListEpisodes'): 	ListEpisodes(url,addpr('title',''),addpr('imdb_id',''),addpr('img',''),addpr('fimg',''))
	elif (mode=='ListLatestEpisodes'): ListLatestEpisodes(url)
	elif (mode=='ListLatestEpisodes1'): ListLatestEpisodes()
	elif (mode=='ListLatestShows'): ListLatestShows()
	elif (mode=='ListPopularShows'): ListPopularShows()
	elif (mode=='GetMedia'): 			GetMedia(url,addpr('title',''),addpr('imdb_id',''),addpr('img',''),addpr('fimg',''),addpr('stitle',''),addpr('etitle',''),addpr('e',''),addpr('s',''),addpr('e2',''),addpr('wwT',''))
	elif (mode=='Search'):				DoSearch(addpr('title',''),url)
	#elif (mode=='Hosts'): 				Browse_Hosts(url)
	#elif (mode=='Search'): 			Search_Site(title=addpr('title',''),url=url,page=page,metamethod=addpr('metamethod','')) #(site,section)
	#elif (mode=='SearchLast'): 	Search_Site(title=addst('LastSearchTitle'+SiteTag),url=url,page=page,metamethod=addpr('metamethod',''),endit=tfalse(addpr('endit','true'))) #(site,section)
	elif (mode=='About'): 				eod(); About()
	#elif (mode=='FavoritesList'): Fav_List(site=site,section=section,subfav=addpr('subfav',''))
	elif (mode=='MenuAZ'): 				MenuAZ(url)
	elif (mode=='MenuGenre'): 		MenuGenre()
	elif (mode=='FavoritesList'): Fav_List(site=site,section=section,subfav=addpr('subfav',''))
	elif (mode=='PlayURL'): 						PlayURL(url)
	elif (mode=='PlayURLs'): 						PlayURLs(url)
	elif (mode=='PlayURLstrm'): 				PlayURLstrm(url)
	elif (mode=='PlayFromHost'): 				PlayFromHost(url)
	elif (mode=='PlayFromHostMT'): 			PlayFromHostMT(url)
	elif (mode=='PlayVideo'): 					PlayVideo(url)
	elif (mode=='PlayItCustom'): 				PlayItCustom(url,addpr('streamurl',''),addpr('img',''),addpr('title',''))
	elif (mode=='PlayItCustomL2A'): 		PlayItCustomL2A(url,addpr('streamurl',''),addpr('img',''),addpr('title',''))
	elif (mode=='Settings'): 						_addon.addon.openSettings() # Another method: _plugin.openSettings() ## Settings for this addon.
	elif (mode=='ResolverSettings'): 		import urlresolver; urlresolver.display_settings()  ## Settings for UrlResolver script.module.
	elif (mode=='ResolverUpdateHostFiles'):	import urlresolver; urlresolver.display_settings()  ## Settings for UrlResolver script.module.
	elif (mode=='TextBoxFile'): 				TextBox2().load_file(url,addpr('title','')); #eod()
	elif (mode=='TextBoxUrl'):  				TextBox2().load_url(url,addpr('title','')); #eod()
	elif (mode=='Download'): 						
		try: _addon.resolve_url(url)
		except: pass
		debob([url,addpr('destfile',''),addpr('destpath',''),str(tfalse(addpr('useResolver','true')))])
		DownloadThis(url,addpr('destfile',''),addpr('destpath',''),tfalse(addpr('useResolver','true')))
	elif (mode=='toJDownloader'): 			SendTo_JDownloader(url,tfalse(addpr('useResolver','true')))
	elif (mode=='cFavoritesEmpty'):  	fav__COMMON__empty( site=site,section=section,subfav=addpr('subfav','') ); xbmc.executebuiltin("XBMC.Container.Refresh"); 
	elif (mode=='cFavoritesRemove'):  fav__COMMON__remove( site=site,section=section,subfav=addpr('subfav',''),name=addpr('title',''),year=addpr('year','') )
	elif (mode=='cFavoritesAdd'):  		fav__COMMON__add( site=site,section=section,subfav=addpr('subfav',''),name=addpr('title',''),year=addpr('year',''),img=addpr('img',''),fanart=addpr('fanart',''),plot=addpr('plot',''),commonID=addpr('commonID',''),commonID2=addpr('commonID2',''),ToDoParams=addpr('todoparams',''),Country=addpr('country',''),Genres=addpr('genres',''),Url=url ) #,=addpr('',''),=addpr('','')
	elif (mode=='AddVisit'):							
		try: visited_add(addpr('title')); RefreshList(); 
		except: pass
	elif (mode=='RemoveVisit'):							
		try: visited_remove(addpr('title')); RefreshList(); 
		except: pass
	elif (mode=='EmptyVisit'):						
		try: visited_empty(); RefreshList(); 
		except: pass
	elif (mode=='refresh_meta'):			refresh_meta(addpr('video_type',''),TagAnimeName(addpr('title','')),addpr('imdb_id',''),addpr('alt_id',''),addpr('year',''))
	else: myNote(header='Site:  "'+site+'"',msg=mode+' (mode) not found.'); import mMain
mode_subcheck(addpr('mode',''),addpr('site',''),addpr('section',''),addpr('url',''))
### ############################################################################################################
### ############################################################################################################
