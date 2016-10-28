### ############################################################################################################
###	#	
### # Site: 				#		Anime FATE - http://www.waoanime.tv/
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
from common import (_addon,_artIcon,_artFanart,_addonPath)
### ############################################################################################################
### ############################################################################################################
SiteName='W[COLOR deepskyblue]AO[/COLOR] [COLOR white][I]Anime[/I][/COLOR]  [COLOR deepskyblue]TV[/COLOR]  [v0.0.1]  [Anime]'
SiteTag='waoanime.tv'
mainSite='http://www.waoanime.tv'
mainSite2='http://www.waoanime.tv/'
mainSiteI='http://images1.waoanime.tv/'
mainSiteI2='http//images1.waoanime.tv/'
iconSite=_artIcon
fanartSite=_artFanart
colors={'0':'white','1':'red','2':'blue','3':'green','4':'yellow','5':'orange','6':'lime','7':'','8':'cornflowerblue','9':'blueviolet','10':'hotpink','11':'pink','12':'tan','13':'firebrick','14':'mediumpurple'}

CR='[CR]'
MyAlphabet=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
#MyGenres=[' Action','Action','Adventure','Animation','Cars','Comedy','Dementia','Demons','Drama','Ecchi','Fantasy','Game','Harem','Historical','Horror','Josei','Kids','Magic','Martial Arts','Mecha','Military','Movie','Music','Mutants','Mystery','Novel','Parody','Police','Psychological','Romance','Samurai','School','Sci-Fi','Seinen','Shoujo','Shoujo Ai','Shounen','Shounen Ai','Slice of Life','Space','Sports','Super Power','Supernatural','Thriller','Vampire']
MyGenres=['Anime Movies','Kids','Action','Adventure','Comedy','Conspiracy','Cyborgs','Demons','Against Demons','Angels','Supernatural','Horror','Magic','Drama','Fantasy','Contemporary Fantasy','Ecchi','18+','Erotica','Pantsu','Incest','Gunfights','Harem','Male Harem','Historical','Mecha','Martial Arts','Mystery','Military','Police','Cops','Law and Order','Parody','Psychological','Romance','Samurai','Sci-Fi','Science Fiction','Tournament','Idol','Band','Music','Sports','Clubs','Baseball','Football','Boing','Slice of Life','Daily Life','School Life','Coming of Age','High School','Slow Paced','Special Squads','Super Power','Seinen','Shoujo','Bishounen','Vampire','Violence','School','Shoujo Ai','Literature','Bishojo','Thriller','Josei','Cyberpunk','Power Suits','Aliens','Tragedy','Yaoi','FanService','Proxy Battles','Human Enhancement','Sudden Girlfriend Appearance','Female Students','Light Novel','Piloted Robots','Slapstick']
## Genres ## 'Action','Adventure','Comedy','Drama','Supernatural','Slice of Life','Science Fiction','Magic','Romance','Tournament','Horror','','','','','','','','','','','','' ##
MyBrowser=['User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3']
ww6='[COLOR black]@[/COLOR]'; 
ww7='[COLOR deepskyblue]@[/COLOR]'; 
clr1='white'; clr2='deepskyblue'; 

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
		#m+=CR+CR+'Known Hosts for Videos:  '
		m+=CR+'* mp4upload.com [I](working)[/I]'
		m+=CR+'* watchanimeon.com [I](not working)[/I]' ## 
		m+=CR+'* megavideo.com [I](not working)[/I]' ## http://wwwstatic.megavideo.com/mv_player.swf?image=http://www.watchanimeon.com/flv/videoplay2.gif&v=IFJZ3S6Y
		m+=CR+'* youtube.com [I](working via youtube addon)[/I]' ## http://www.youtube.com/v/4jRqgiGir8I&hl=en_US&fs=1&
		#m+=CR+'* UNKNOWN [I](not working)[/I]'
		#m+=CR+'* UNKNOWN [I](not working)[/I]'
		#m+=CR+'* UNKNOWN [I](not working)[/I]'
		m+=CR+CR+'Features:  '
		m+=CR+'* Browse Shows - Lists'
		m+=CR+'* Browse Shows - Genres'
		m+=CR+'* Browse Shows - AtoZ'
		m+=CR+'* Browse Random Show'
		m+=CR+'* Browse Episodes'
		m+=CR+'* Browse Show information from site while on Episodes Lists'
		m+=CR+'* Browse Next Page Link on Episodes Lists'
		m+=CR+'* Browse Host Links'
		m+=CR+'* Browse Mirrors'
		m+=CR+'* Play [I]SOME[/I] Videos with UrlResolver'
		#m+=CR+'* Download Videos with UrlResolver'
		m+=CR+'* MetaData for Shows and 1st Season Episodes where data is available.'
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
	try: r1,r2=re.compile('(http://www.animefate.com/images/.+?)-\d+x\d+(\.[jpg|png|gif]+)').findall(img)[0]; img=r1+r2; 
	except: pass
	return img
def AFColoring(t): 
	if len(t)==0: return t
	elif len(t)==1: return cFL(t,clr1)
	else: return cFL(cFL_(t,clr1),clr2)
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
			,'ongoing': 									s+"mBqFW3r"+t #EUak0Sg #ozEg86L
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
			,'favorites': 								s+"mVxogXL"+t #
			,'favorites 1': 							s+"cyDyVuh"+t #
			,'favorites 2': 							s+"GxH6BbM"+t #yRtrel2
			,'favorites 3': 							s+"Z9zKGJU"+t #
			,'favorites 4': 							s+"ovjBVu3"+t #
			,'favorites 5': 							s+"n8LUh2R"+t #
			,'favorites 6': 							s+"qN6FEit"+t #
			,'favorites 7': 							s+"3yQYXNh"+t #
			,'genre': 										s+"ObKUcJT"+t #XEIr4Cz
			,'icon': 											s+"VshtskV"+t
			,'fanart': 										s+"OSv7S2u"+t
			,'last': 											s+"3g6S9UH"+t
			,'latest episodes': 					s+"Skoe3Fm"+t #r19ycox
			,'latest updates': 						s+"E86Rnq5"+t
			,'most popular': 							s+"N69lo3G"+t
			,'new anime': 								s+"wZN1olE"+t
			,'search': 										s+"MTnRQJ3"+t
			,'random anime': 							s+"Rjag7b3"+t
			,'_': 												s+"bGMWifZ"+t
			,'anime 2013': 								s+"4SgqERs"+t
			,'anime 2014': 								s+"ijvRzvJ"+t
			,'anime 2015': 								s+"IYPai5I"+t
			,'anime 2016': 								s+"UqAYilt"+t
			,'anime list': 								s+"NTPFfwQ"+t
			,'a-z': 											s+"Br4ltnl"+t
			,'hot this season': 					s+"KcymQWL"+t
			,'latest animes': 						s+"mDFKTFN"+t
			,'movies': 										s+"hDYdtIr"+t
			,'random': 										s+"5uYkgTx"+t
#			,'': 								s+""+t
#			,'': 								s+""+t
#			,'': 								s+""+t
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
def Fav_List(site='',section='',subfav=''):
	debob(['test1',site,section,subfav]); 
	favs=fav__COMMON__list_fetcher(site=site,section=section,subfav=subfav); 
	ItemCount=len(favs); 
	debob('test2 - '+str(ItemCount)); 
	if len(favs)==0: myNote('Favorites','None Found'); eod(); return
	debob(favs); 
	favs=sorted(favs,key=lambda item: (item[0],item[1]),reverse=False); 
	for (_name,_year,_img,_fanart,_Country,_Url,_plot,_Genres,_site,_subfav,_section,_ToDoParams,_commonID,_commonID2) in favs:
		if _img > 0: img=_img
		else: img=iconSite
		if _fanart > 0: fimg=_fanart
		else: fimg=fanartSite
		debob('_ToDoParams'); debob(_ToDoParams)
		pars=_addon.parse_query(_ToDoParams)
		pars[u'fimg']=_fanart; pars[u'img']=_img; 
		#if len(_commonID) > 0: pars['imdb_id']=_commonID
		debob('pars'); debob(pars)
		_title=AFColoring(_name)
		if (len(_year) > 0) and (not _year=='0000'): _title+=cFL('  ('+cFL(_year,clr2)+')',clr1)
		if len(_Country) > 0: _title+=cFL('  ['+cFL(_Country,clr2)+']',clr1)
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
def GetMedia(Url,title,imdb_id,img,fimg,stitle,etitle,enumber,snumber,enumber2,wwT=''):
	if len(snumber)==0: snumber='0'; 
	if len(Url)==0: return
	if mainSite not in Url: Url=mainSite+Url; 
	deb('imdb_id',imdb_id); deb('title',title); deb('Url',Url); html=messupText(nolines(nURL(Url)),True,True); deb('length of html',str(len(html))); #debob(html); 
	if len(html)==0: return
	###
	try:
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
	except: pass
	###
	s='<script pagespeed_orig_type="text/javascript" type="text/\D+" orig_index="\d+">document.write\(unescape\("(\%[\%0-9A-Za-z]+)"\)\);</script>'
	try: matchesA=re.compile(s).findall(html); deb('# of matches found',str(len(matchesA))); debob(matchesA)
	except: matchesA=''; 
	matchesB=''
	if len(matchesA) > 0:
		for m in matchesA:
			matchesB+=urllib.unquote_plus(m)
	debob(matchesB); 
	#s='<iframe\s+id="video"\s+src="(http[s]*://.+?)"'; 
	s='src="(http.+?)"'
	#s='<iframe .*?src="(http.+?)"'
	try: matches=re.compile(s).findall(matchesB); deb('# of matches found',str(len(matches))); debob(matches)
	except: matches=''; 
	if len(matches) > 0:
		#for (url,img,name,genres,status,NoEps,year) in matches:
		iC=len(matches); 
		try: import urlresolver
		except: pass
		for m in matches:
			###
			if "http://animeonair.com/" in m: m=m.replace("http://animeonair.com/","http://videoboxone.com/")
			if "http://www.youtube.com/v/" in m: 
				#m=m.replace("http://www.youtube.com/v/","http://youtube.com/watch?v=")
				#m="plugin://plugin.video.youtube/?action=play_video&videoid="+m.split("/v/")[-1].split("&")[0]
				m="plugin://plugin.video.youtube/?path=/root/video&action=play_video&videoid="+m.split("/v/")[-1].split("&")[0]
			###
			cMI=[]; labs={'title':m}; 
			pars={'mode':'PlayFromHost','url':m,'studio':stitle+' - '+str(enumber)+' - '+etitle,'title':title,'etitle':etitle,'stitle':title,'imdb_id':imdb_id,'img':img,'fimg':fimg,'site':site,'section':section,'wwT':wwT,'MarkAsWatched':'true'}; 
			destfile=str(stitle)+' - s'+str(snumber)+'e'+str(enumber)+' - '+str(enumber)+' - '+str(etitle)+'.mp4'
			if (int(snumber) > 1) and (int(enumber) is not enumber2):
				destfile=str(stitle)+' - s'+str(snumber)+'e'+str(enumber2)+' - '+str(enumber)+' - '+str(etitle)+'.mp4'
			destfile=destfile.replace(':','').replace('"','').replace("'","").replace("?","")
			Clabs={'title':title,'year':'','url':m,'destfile':destfile,'img':img,'fanart':fimg,'plot':'','todoparams':_addon.build_plugin_url(pars),'site':site,'section':section}; 
			cMI=ContextMenu_Hosts(Clabs); 
			if urlresolver.HostedMediaFile(m).valid_url(): labs[u'title']=cFL(m,'blue'); 
			else: labs[u'title']=cFL(m,'red'); 
			try: _addon.add_directory(pars,labs,is_folder=False,fanart=fimg,img=img,contextmenu_items=cMI,total_items=iC)
			except: pass
	# <iframe id="video" src="
	#html=messupText(nURL('http://metaframe.digitalsmiths.tv/v2/WBtv/assets/'+VideoID+'/partner/11?format=json'),True)
	#s='"length": (\d+), "bitrate": "(.+?)", "uri": "(.+?://.+?)"'; matches=re.compile(s).findall(nolines(html)); deb('# of matches found',str(len(matches))); #debob(matches)
	#for (_length,_name,_url) in matches:
	#	labs={'title':title+' - ['+_name+']'}
	#	try: _addon.add_directory({'mode':'PlayVideo','img':img,'studio':'['+_name+']','url':_url,'title':title,'site':site},labs,is_folder=False,fanart=fanartSite,img=img)
	#	except: pass
	###
	s='<div\s+class="video-show[0-9\s]*">\s*<div\s+class="vid-thumb">\s*<a\s+href="(.*?)">\s*<div\s+class="gg">\s*'; 
	s+='<div style="background-image:url\((.+?)\);width:\d+px;height:\d+px;opacity:.\d*">\s*</div>\s*</div>'; 
	s+='\s*<span class="vid-play">\s*</span>'; 
	s+='\s*<span class="vid-info[d]*">\s*(.*?)\s*</span>'; 
	s+='\s*<span class="vid-hd">\s*(.*?)\s*</span>'; 
	s+='\s*<div class="titlel">\s*(.*?)\s*</div>\s*</a>\s*</div>'; 
	### vUrl,vImg,vLangType,vMirror,vHost
	try: matchesC=re.compile(s).findall(html); deb('# of matches found for mirrors',str(len(matchesC))); debob(matchesC)
	except: matchesC=''; 
	if len(matchesC) > 0:
		iC=iC+len(matchesC); 
		UrlPre=re.compile('('+mainSite+'/[a-zA-Z0-9\-_]+/)').findall(Url)[0]
		UrlTest=(Url+"/000").replace("http://","").split("/")
		UrlPre="http://"+UrlTest[0]+"/"+UrlTest[1]+"/"
		for vUrl,vImg,vLangType,vMirror,vHost in matchesC:
			if "-episode-" not in vUrl: vUrl=UrlPre+''+vUrl
			cMI=[]; labs={}; pars={'mode':'GetMedia','img':img,'fimg':fimg,'title':title,'wwT':wwT,'e':enumber,'s':snumber,'e2':enumber2,'etitle':etitle,'stitle':stitle,'imdb_id':imdb_id}; 
			## Url,title,imdb_id,img,fimg,stitle,etitle,enumber,snumber,enumber2,wwT
			## GetMedia(url,addpr('title',''),addpr('imdb_id',''),addpr('img',''),addpr('fimg',''),addpr('stitle',''),addpr('etitle',''),addpr('e',''),addpr('s',''),addpr('e2',''),addpr('wwT',''))
			pars[u'url']=vUrl
			labs[u'title']=vMirror+': '+vLangType+' - '+vHost+'[CR]'+cFL(vUrl,'firebrick')+''
			try: _addon.add_directory(pars,labs,is_folder=True,fanart=fimg,img=img,contextmenu_items=cMI,total_items=iC)
			except: pass
	###
	set_view('list',view_mode=addst('links-view')); eod()

def ListEpisodes(Url,title,imdb_id,img,fimg):
	debob([Url,title,imdb_id,img,fimg])
	if len(Url)==0: return
	if mainSite not in Url: Url=mainSite+Url; 
	deb('imdb_id',imdb_id); deb('title',title); deb('Url',Url); html=messupText(nolines(nURL(Url)),True,True); deb('length of html',str(len(html))); #debob(html); 
	if imdb_id=='0': imdb_id=''; 
	if len(html)==0: return
	if (len(title)==0) or (title=="Random Anime") or (title=="Anime Movies"): 
		try: title=re.compile('<h2 class="sip-list-title">(.*?)\s+Anime Episodes</h2>').findall(html)[0]
		except: pass
	try: sipList=re.compile('<ul class="sip-list">(.*?)</ul>').findall(html)[0]
	except: sipList=''+html
	#=re.compile('').findall(html)[0]
	
	###
	_addon.addon.setSetting(id="LastShowListedURL", value=Url)
	_addon.addon.setSetting(id="LastShowListedNAME", value=title)
	_addon.addon.setSetting(id="LastShowListedIMG", value=img)
	_addon.addon.setSetting(id="LastShowListedFANART", value=fimg)
	_addon.addon.setSetting(id="LastShowListedIMDBID", value=imdb_id)
	###
	s='<li><a\s+href="(.+?)"\s+title="(.+?)">(.+?)</a>\s*<span\s+style="float:\D+;margin-\D+:\d+px">(.*?)</span>(.*?)</li>'; 
	try: 
		#matches=re.compile(s).findall(html); 
		matches=re.compile(s).findall(sipList); 
		deb('# of matches found',str(len(matches))); #debob(matches)
	except: matches=''; 
	###
	cMI=[]; pars={}; labs={}; 
	cMI.append(('Show Info',ps('cMI.showinfo.url')))
	try: 		
		pageImage=re.compile('<div class="sip-thumb">\s*<img src="(.+?)" width="\d+px" alt="thumb" pagespeed_url_hash=".*?"/>').findall(html)[0]; 
		if len(img)==0: _addon.addon.setSetting(id="LastShowListedIMG", value=pageImage); img=''+pageImage
	except: pageImage=img
	if (mainSite not in pageImage) and (mainSiteI not in pageImage) and (mainSiteI2 not in pageImage): pageImage=mainSite+pageImage; 
	if mainSiteI2 in pageImage: pageImage.replace(mainSiteI2,mainSiteI)
	try: 		pageTitle=re.compile('<div class="cat-title"><h1>(.*?)</h1>').findall(html)[0]; 
	except: pageTitle=''+title
	try: 		pageYear=re.compile('<p><span>Year:</span>\s*(.*?)\s*</p>').findall(html)[0]; 
	except: pageYear=''
	try: 		pageType=re.compile('<p><span>Type:</span>\s*(.*?)\s*</p>').findall(html)[0]; 
	except: pageType=''
	try: 		
		pageGenres1=re.compile('<p><span>Genres:</span>\s*(.*?)\s*</p>').findall(html)[0]; 
		pageGenres=re.compile("<a href='/.genre=.*?'>\s*(.*?)\s*</a>").findall(pageGenres1)[0]; 
	except: pageGenres=[]
	try: 		pagePlot=re.compile('<strong>Description:</strong></span></p>\s*<p>(.*?)</p>').findall(html)[0]; 
	except: pagePlot=''
	pagePlot=pagePlot.replace('<br/>','[CR]').replace('<br>','[CR]').replace('<BR/>','[CR]').replace('<BR>','[CR]').replace('<I>','[I]').replace('</I>','[/I]').replace('<i>','[I]').replace('</i>','[/I]').replace('<span style="text=decoration:underline">','').replace('</span>','')
	pagePlot=messupText(pagePlot,True,True,True)
	labs[u'title']=pageTitle; pars[u'title']=pageTitle; pars[u'img']=pageImage; pars[u'fimg']=fimg; 
	labs[u'plot']=cFL(pagePlot,'tan'); 
	debob(labs); 
	nTitles=[]
	if len(pageTitle) > 0: nTitles.append(pageTitle)
	if len(pageType) > 0: nTitles.append(pageType)
	if len(pageYear) > 0: nTitles.append(pageYear)
	for nTitle in nTitles:
		labs[u'title']=nTitle
		try: _addon.add_directory(pars,labs,is_folder=True,fanart=fimg,img=pageImage,contextmenu_items=cMI,total_items=1)
		except: pass
	###
	if len(matches) > 0:
		s='1'; enMeta=tfalse(addst("enableMeta","false")); iC=len(matches); n=False; e3='0'; 
		if enMeta==True:
			try: from metahandler import metahandlers; grab=metahandlers.MetaData(preparezip=False); 
			except: debob("filed to import metahandler"); 
		if len(imdb_id)==0:
			try:
				ShowLabs=grab.get_meta('tvshow',title)
				imdb_id=ShowLabs['imdb_id']
				_addon.addon.setSetting(id="LastShowListedIMDBID", value=imdb_id)
			except: pass
		
		if 'Movie ' in title: s='0'; enMeta=False; 
		for (url,nameTitle,name,datestamp,OtherStuff) in matches[::-1]:
			debob([url,nameTitle,name,datestamp,OtherStuff]); 
			if ' ~Final~' in name: name=name.replace(' ~Final~','')
			cMI=[]; labs={}; #labs['plot']=''; labs['plotoutline']=''; labs['showtitle']=''; labs['episodetitle']=''; labs['videoid']=''; 
			if "Episode " in name: 
				try: e=re.compile("Episode\s*(\d+)").findall(name)[0]; 
				except: e=""; 
				if len(str(e))==0:
					try: e=re.compile("Movie\s*(\d+)").findall(name)[0]; 
					except: e=""; 
			else: e=""; 
			name=name.replace(title,''); e2=copy.deepcopy(e); e4=''+str(e); 
			wwT=title+" ~~ "+name
			try:
				if visited_check(wwT)==True: ww=7
				else: ww=6
			except: ww=6
			if (enMeta==True) and (len(imdb_id) > 1):
				if len(e) > 0:
					if int(s) > 1:
						e2=str(int(e)-int(e3))
					try: labs=grab.get_episode_meta(tvshowtitle=title,imdb_id=imdb_id,season=s,episode=e2,air_date='',episode_title='',overlay=6); 
					except: n=True;
					#debob(labs); 
					try:
						if (len(labs['title'])==0) and (len(labs['plot'])==0) and (len(labs['episode_id'])==0):
							s=str(int(s)+1); e3=str(int(e)-1)
							e2=str(int(e)-int(e3))
							try: labs=grab.get_episode_meta(tvshowtitle=title,imdb_id=imdb_id,season=s,episode=e2,air_date='',episode_title='',overlay=6); 
							except: n=True;
					except: pass
					try:
						if len(labs[u'cover_url']) > 0: img=labs[u'cover_url']; 
					except: pass
					try:
						if len(labs[u'backdrop_url']) > 0: fimg=labs[u'backdrop_url']; 
					except: pass
				else: n=True; 
			else: n=True; 
			if n==True: labs[u'plot']=''; labs[u'imdb_id']=''; labs[u'title']=name; labs[u'year']=''; 
			if len(labs[u'title'])==0: labs[u'title']=name; 
			if len(labs[u'title'])==0: labs[u'title']=title; 
			etitle=labs[u'title']; 
			if len(e) > 0: labs[u'title']=cFL(str(e4)+') ','blue')+AFColoring(labs[u'title']); 
			else: labs[u'title']=AFColoring(labs[u'title'])
			labs[u'plot']=CR+cFL(labs[u'plot'],'mediumpurple'); 
			if len(datestamp) > 0: labs[u'title']+=CR+cFL("["+datestamp+"]",colors['13']); 
			labs[u'plot']+=CR+cFL(str(e)+")",'blue')+cFL(" Season "+cFL(str(s),colors['13'])+" Episode "+cFL(str(e2),colors['13'])+"",'mediumpurple')
			labs[u'title']=wwA(labs[u'title'],ww); 
			debob(labs); 
			pars={'mode':'GetMedia','url':url,'title':name,'etitle':etitle,'stitle':title,'imdb_id':labs[u'imdb_id'],'img':img,'fimg':fimg,'site':site,'section':section,'e':str(e),'s':str(s),'e2':str(e2),'e3':str(e3),'wwT':wwT}; 
			Clabs={'title':name,'year':'','url':url,'img':img,'fanart':fimg,'plot':labs[u'plot'],'todoparams':_addon.build_plugin_url(pars),'site':site,'section':section}; 
			if ">HOT</span>" in OtherStuff: labs[u'title']=labs[u'title']+'  '+cFL('[HOT]','deeppink'); 
			try: cMI=ContextMenu_Episodes(Clabs); 
			except: pass
			try: cMI=wwCMI(cMI,ww,wwT); 
			except: pass
			try: _addon.add_directory(pars,labs,is_folder=True,fanart=fimg,img=img,contextmenu_items=cMI,total_items=iC)
			except: pass
	if '">&gt;</a></li>' in html:
		#try: 		NextPageUrl=re.compile('<li><a href="(.*?/page/.*?)">&gt;</a></li>').findall(html)[0]; 
		#except: NextPageUrl=''
		NextPageUrl=html.split('">&gt;</a></li>')[0].split('<li><a href="')[-1]
		#if '/page/' in URL
		if '/anime/' in NextPageUrl: NextPageUrl=mainSite+NextPageUrl
		elif '/page/' not in Url: NextPageUrl=Url+NextPageUrl
		pars={'mode':'ListEpisodes','url':NextPageUrl,'fimg':fimg,'img':img,'imdb_id':imdb_id,'title':title}
		labs={u'title':'Next Page'+'[CR]'+cFL(NextPageUrl,'redbrick')}
		try: _addon.add_directory(pars,labs,is_folder=True,fanart=fimg,img=img,contextmenu_items=cMI,total_items=iC)
		except: pass
	set_view('episodes',view_mode=addst('episode-view')); eod()

### ############################################################################################################
### ############################################################################################################

def ListShows_HotThisSeason(Url):
	if len(Url)==0: Url=mainSite+Url
	if mainSite not in Url: Url=mainSite+Url
	deb('Url',Url); html=messupText(nolines(nURL(Url)),True,True); deb('length of html',str(len(html))); #debob(html); 
	if len(html) > 0:
		try:		html2=re.compile('<div class="hotanime"><ul>(.*?)</ul></div>').findall(html)[0]; 
		except: html2=''
		if len(html2) > 0:
			try:		matches=re.compile('<li>\s*<a\s+href="(anime/.*?)">\s*(.*?)\s*</a>\s*</li>').findall(html2); 
			except: matches=''
			if len(matches) > 0:
				iC=len(matches); enMeta=tfalse(addst("enableMeta","false")); 
				if enMeta==True:
					try: from metahandler import metahandlers; grab=metahandlers.MetaData(preparezip=False); 
					except: debob("filed to import metahandler"); 
				for (url,name) in matches:
					tag1="anime/"
					if len(url) > len(tag1):
						if url[0:len(tag1)]==tag1: url="/"+url
					cMI=[]; plot=""; labs={}; fimg=fanartSite; img=iconSite;
					if enMeta==True:
						try: labs=grab.get_meta('tvshow',name); debob(labs); 
						except: pass
						try:
							if len(labs[u'cover_url']) > 0: img=labs[u'cover_url']; 
						except: pass
						try:
							if len(labs[u'backdrop_url']) > 0: fimg=labs[u'backdrop_url']; 
						except: pass
					else: labs[u'plot']=''; labs[u'imdb_id']=''; labs[u'title']=name; labs[u'year']=''; 
					pars={'mode':'ListEpisodes','url':url,'title':name,'imdb_id':labs[u'imdb_id'],'img':img,'fimg':fimg,'site':site,'section':section}; 
					labs[u'title']=AFColoring(name); 
					Clabs={'title':name,'year':labs[u'year'],'url':url,'commonid':labs[u'imdb_id'],'img':img,'fanart':fimg,'plot':labs[u'plot'],'todoparams':_addon.build_plugin_url(pars),'site':site,'section':section}; 
					try: cMI=ContextMenu_Series(Clabs); 
					except: pass
					try: _addon.add_directory(pars,labs,is_folder=True,fanart=fimg,img=img,contextmenu_items=cMI,total_items=iC,context_replace=False)
					except: pass
	set_view('tvshows',view_mode=addst('tvshows-view')); eod()




### ############################################################################################################
### ############################################################################################################

def ListShows(Url,Letter=''): ## For Browsing: text-lists, ...
	if len(Url)==0: return
	if mainSite not in Url: Url=mainSite+Url; 
	deb('Url',Url); html=messupText(nolines(nURL(Url)),True,True); deb('length of html',str(len(html))); #debob(html); 
	if len(html) > 0:
		if len(Letter)==0: s9='<div id="content">(.*?)<div class="\D+-sidebar">'
		else: s9='<h3 class="postlist-title"><a name="'+Letter+'"></a><p class="sep">'+Letter+'</p></h3><ul class="postlist">(.*?)</ul>'
		try:		html2=re.compile(s9).findall(html)[0]; 
		except: html2=''
		if len(html2) > 0:
			s1 ='<li>\s*<a href="(.+?)">\s*(.+?)\s*</a>\s*</li'; 
			try:		matches=re.compile(s1).findall(html2); 
			except: matches=''
			if len(matches) > 0:
				iC=len(matches); enMeta=tfalse(addst("enableMeta","false")); 
				if enMeta==True:
					try: from metahandler import metahandlers; grab=metahandlers.MetaData(preparezip=False); 
					except: debob("filed to import metahandler"); 
				for (url,name) in matches:
					tag1="anime/"
					if len(url) > len(tag1):
						if url[0:len(tag1)]==tag1: url="/"+url
					#if len(img)==0: img=iconSite;
					#if ("http://i.imgur.com/" not in img) and (iconSite not in img) and (mainSite not in img) and (mainSiteI not in img) and (mainSiteI2 not in img): img=mainSite+img; 
					cMI=[]; plot=""; labs={}; fimg=fanartSite; img=iconSite; 
					if enMeta==True:
						try: labs=grab.get_meta('tvshow',name); debob(labs); 
						except: pass
						try:
							if len(labs[u'cover_url']) > 0: img=labs[u'cover_url']; 
						except: pass
						try:
							if len(labs[u'backdrop_url']) > 0: fimg=labs[u'backdrop_url']; 
						except: pass
					else: labs[u'plot']=''; labs[u'imdb_id']=''; labs[u'title']=name; labs[u'year']=''; 
					#if len(plot)==0: plot="[COLOR "+clr2+"]"+sType+" - [[COLOR "+clr1+"]"+sAirDate+"[/COLOR]][/COLOR]"; 
					#else: plot="[COLOR "+clr2+"]"+sType+" - [[COLOR "+clr1+"]"+sAirDate+"[/COLOR]][/COLOR]"+CR+"[COLOR "+clr2+"]"+plot+"[/COLOR]"; 
					try: labs[u'plot']=plot+CR+CRlabs['plot']
					except: labs[u'plot']=plot
					#plot+=CR+"Genres:  [COLOR purple]"+Genres2+"[/COLOR]"; 
					#labs[u'plot']=plot+CR+CR+cFL(labs[u'plot'],'tan'); 
					pars={'mode':'ListEpisodes','url':url,'title':name,'imdb_id':labs[u'imdb_id'],'img':img,'fimg':fimg,'site':site,'section':section}; 
					labs[u'title']=AFColoring(name); 
					Clabs={'title':name,'year':labs[u'year'],'url':url,'commonid':labs[u'imdb_id'],'img':img,'fanart':fimg,'plot':labs[u'plot'],'todoparams':_addon.build_plugin_url(pars),'site':site,'section':section}; 
					try: cMI=ContextMenu_Series(Clabs); 
					except: pass
					try: _addon.add_directory(pars,labs,is_folder=True,fanart=fimg,img=img,contextmenu_items=cMI,total_items=iC,context_replace=False)
					except: pass
			s2='<div class="pagging">(.*?)</div>'; 
			try:		html3=re.compile(s2).findall(html)[0]; 
			except: html3=''
			if len(html3) > 0:
				s3='<span(.*?)><a href="(.+?)">(.+?)</a></span>'; 
				try:		matches=re.compile(s3).findall(html3); 
				except: matches=''
				if len(matches) > 0:
					iC=iC+len(matches); 
					for (current,url,name) in matches:
						tname=cFL('>> Page:','green')+'  '+cFL(name,clr1)
						if "current" in current: tname+=' '+cFL('['+cFL('current',clr1)+']',clr2)
						try: _addon.add_directory({'mode':'ListShows','url':url,'site':site,'section':section},{'title':tname},is_folder=True,total_items=iC,fanart=fanartSite,img=psgn('img_next'))
						except: pass
	set_view('tvshows',view_mode=addst('tvshows-view')); eod()

def ListShows2(Url): ## For Browsing: Years, ...
	if len(Url)==0: return
	if mainSite not in Url: Url=mainSite+Url; 
	deb('Url',Url); html=messupText(nolines(nURL(Url)),True,True); deb('length of html',str(len(html))); #debob(html); 
	if len(html) > 0:
		try:		html2=re.compile('<div id="content">(.*?)<div class="\D+-sidebar">').findall(html)[0]; 
		except: html2=''
		if len(html2) > 0:
			s1 ='<div class="entry-\D+">\s*<div.*?>\s*<a href="(.+?)">\s*<img src="(.+?)" width="\d+px" height="\d+px" pagespeed_url_hash="(.*?)"/>\s*</a>'; 
			s1+='</div><div.*?><p><span>Series[\:]+\s*</span>\s*<a href="(.+?)">\s*(.+?)\s*</a>\s*</p>\s*'; 
			s1+='<p><span>Air Date[\:]+\s*</span>\s*(.*?)\s*</p>\s*'; 
			s1+='<p><span>Type[\:]+\s*</span>\s*(.*?)\s*</p>\s*'; 
			s1+='<p><span>Genres[\:]+\s*(.*?)\s*</span>\s*(.*?)\s*</p>\s*</div>'; 
			try:		matches=re.compile(s1).findall(html2); 
			except: matches=''
			if len(matches) > 0:
				iC=len(matches); enMeta=tfalse(addst("enableMeta","false")); 
				if enMeta==True:
					try: from metahandler import metahandlers; grab=metahandlers.MetaData(preparezip=False); 
					except: debob("filed to import metahandler"); 
				for (url1,img,pagespeed_url_hash,url,name,sAirDate,sType,sGenres1,sGenres2) in matches:
					tag1="anime/"
					if len(url) > len(tag1):
						if url[0:len(tag1)]==tag1: url="/"+url
					if len(img)==0: img=iconSite;
					if ("http://i.imgur.com/" not in img) and (iconSite not in img) and (mainSite not in img) and (mainSiteI not in img) and (mainSiteI2 not in img): img=mainSite+img; 
					cMI=[]; plot=""; labs={}; fimg=fanartSite; 
					if enMeta==True:
						try: labs=grab.get_meta('tvshow',name); debob(labs); 
						except: pass
						try:
							if len(labs[u'cover_url']) > 0: img=labs[u'cover_url']; 
						except: pass
						try:
							if len(labs[u'backdrop_url']) > 0: fimg=labs[u'backdrop_url']; 
						except: pass
					else: labs[u'plot']=''; labs[u'imdb_id']=''; labs[u'title']=name; labs[u'year']=''; 
					if len(plot)==0: plot="[COLOR "+clr2+"]"+sType+" - [[COLOR "+clr1+"]"+sAirDate+"[/COLOR]][/COLOR]"; 
					else: plot="[COLOR "+clr2+"]"+sType+" - [[COLOR "+clr1+"]"+sAirDate+"[/COLOR]][/COLOR]"+CR+"[COLOR "+clr2+"]"+plot+"[/COLOR]"; 
					try: labs[u'plot']=plot+CR+CRlabs['plot']
					except: labs[u'plot']=plot
					#plot+=CR+"Genres:  [COLOR purple]"+Genres2+"[/COLOR]"; 
					#labs[u'plot']=plot+CR+CR+cFL(labs[u'plot'],'tan'); 
					pars={'mode':'ListEpisodes','url':url,'title':name,'imdb_id':labs[u'imdb_id'],'img':img,'fimg':fimg,'site':site,'section':section}; 
					labs[u'title']=AFColoring(name); 
					Clabs={'title':name,'year':labs[u'year'],'url':url,'commonid':labs[u'imdb_id'],'img':img,'fanart':fimg,'plot':labs[u'plot'],'todoparams':_addon.build_plugin_url(pars),'site':site,'section':section}; 
					try: cMI=ContextMenu_Series(Clabs); 
					except: pass
					try: _addon.add_directory(pars,labs,is_folder=True,fanart=fimg,img=img,contextmenu_items=cMI,total_items=iC,context_replace=False)
					except: pass
	set_view('tvshows',view_mode=addst('tvshows-view')); eod()

def ListShows3(Url): ## For Browsing: Genres, ...
	if len(Url)==0: return
	if mainSite not in Url: Url=mainSite+Url; 
	deb('Url',Url); html=messupText(nolines(nURL(Url)),True,True); deb('length of html',str(len(html))); #debob(html); 
	if len(html) > 0:
		try:		html2=re.compile('<div id="content">(.*?)<div class="\D+-sidebar">').findall(html)[0]; 
		except: html2=''
		if len(html2) > 0:
			s1 ='<div.*?>\s*<div.*?>\s*<a href=\'(.+?)\'>\s*<img width="\d+px" height="\d+px" src="(.+?)" pagespeed_url_hash="(.*?)">\s*</a>\s*'; 
			s1+='<div.*?>\s*<img.*?>\s*<script .*?>.*?</script>\s*<a href=".*?">\s*Add To Favourites\s*</a>\s*</div>\s*</div>\s*<div.*?><br/>\s*'; 
			s1+="<p>\s*<span>\s*Series[\:]+\s*</span>\s*<a href='(.+?)'>\s*(.+?)\s*</a>\s*</p>\s*"; 
			s1+='<p>\s*<span>\s*Type[\:]+\s*</span>\s*(.*?)\s*</p>\s*<p>\s*<span>\s*Year[\:]+\s*</span>\s*(.*?)\s*</p>\s*'; 
			s1+='<p>\s*<span>\s*Genres[\:]+\s*(.*?)\s*</span>\s*(.*?)\s*</p>\s*</div>'; 
			try:		matches=re.compile(s1).findall(html2); 
			except: matches=''
			if len(matches) > 0:
				iC=len(matches); enMeta=tfalse(addst("enableMeta","false")); 
				if enMeta==True:
					try: from metahandler import metahandlers; grab=metahandlers.MetaData(preparezip=False); 
					except: debob("filed to import metahandler"); 
				for (url1,img,pagespeed_url_hash,url,name,sType,sAirDate,sGenres1,sGenres2) in matches:
					tag1="anime/"
					if len(url) > len(tag1):
						if url[0:len(tag1)]==tag1: url="/"+url
					if len(img)==0: img=iconSite;
					if ("http://i.imgur.com/" not in img) and (iconSite not in img) and (mainSite not in img) and (mainSiteI not in img) and (mainSiteI2 not in img): img=mainSite+img; 
					cMI=[]; plot=""; labs={}; fimg=fanartSite; 
					if enMeta==True:
						try: labs=grab.get_meta('tvshow',name); debob(labs); 
						except: pass
						try:
							if len(labs[u'cover_url']) > 0: img=labs[u'cover_url']; 
						except: pass
						try:
							if len(labs[u'backdrop_url']) > 0: fimg=labs[u'backdrop_url']; 
						except: pass
					else: labs[u'plot']=''; labs[u'imdb_id']=''; labs[u'title']=name; labs[u'year']=''; 
					if len(plot)==0: plot="[COLOR "+clr2+"]"+sType+" - [[COLOR "+clr1+"]"+sAirDate+"[/COLOR]][/COLOR]"; 
					else: plot="[COLOR "+clr2+"]"+sType+" - [[COLOR "+clr1+"]"+sAirDate+"[/COLOR]][/COLOR]"+CR+"[COLOR "+clr2+"]"+plot+"[/COLOR]"; 
					try: labs[u'plot']=plot+CR+CRlabs['plot']
					except: labs[u'plot']=plot
					#plot+=CR+"Genres:  [COLOR purple]"+Genres2+"[/COLOR]"; 
					#labs[u'plot']=plot+CR+CR+cFL(labs[u'plot'],'tan'); 
					pars={'mode':'ListEpisodes','url':url,'title':name,'imdb_id':labs[u'imdb_id'],'img':img,'fimg':fimg,'site':site,'section':section}; 
					labs[u'title']=AFColoring(name); 
					Clabs={'title':name,'year':labs[u'year'],'url':url,'commonid':labs[u'imdb_id'],'img':img,'fanart':fimg,'plot':labs[u'plot'],'todoparams':_addon.build_plugin_url(pars),'site':site,'section':section}; 
					try: cMI=ContextMenu_Series(Clabs); 
					except: pass
					try: _addon.add_directory(pars,labs,is_folder=True,fanart=fimg,img=img,contextmenu_items=cMI,total_items=iC,context_replace=False)
					except: pass
			s2='<div class="pagging">(.*?)</div>'; 
			try:		html3=re.compile(s2).findall(html)[0]; 
			except: html3=''
			if len(html3) > 0:
				s3='<span(.*?)><a href="(.+?)">(.+?)</a></span>'; 
				try:		matches=re.compile(s3).findall(html3); 
				except: matches=''
				if len(matches) > 0:
					iC=iC+len(matches); 
					for (current,url,name) in matches:
						tname=cFL('>> Page:','green')+'  '+cFL(name,clr1)
						if "current" in current: tname+=' '+cFL('['+cFL('current',clr1)+']',clr2)
						try: _addon.add_directory({'mode':'ListShows3','url':url,'site':site,'section':section},{'title':tname},is_folder=True,total_items=iC,fanart=fanartSite,img=psgn('img_next'))
						except: pass
	set_view('tvshows',view_mode=addst('tvshows-view')); eod()



### ############################################################################################################
### ############################################################################################################
def MenuYear():
	EarliestYear=(2011-1); RangeBy=0-1; 
	try: thisyear=int(datetime.date.today().strftime("%Y"))
	except: thisyear=2014
	#browsebyImg=checkImgLocal(art('year','.gif'))
	ItemCount=len(range(thisyear,EarliestYear,RangeBy)) * 12 - 12 + 3 # ,total_items=ItemCount
	for year in range(thisyear,EarliestYear,RangeBy):
		_addon.add_directory({'mode':'ListLatestEpisodes2','url':'/'+str(year)+'/','site':site,'section':section},{'title':('/'+cFL(str(year),'mediumpurple')+'/')},is_folder=True,fanart=fanartSite,img=iconSite,total_items=ItemCount); 
		if year==2011: EarliestMonth=10
		else: EarliestMonth=1
		for month in range(12,(EarliestMonth-1),-1):
			_addon.add_directory({'mode':'ListLatestEpisodes2','url':'/'+str(year)+'/'+str(month)+'/','site':site,'section':section},{'title':('/'+str(year)+'/'+cFL(str(month),'firebrick')+'/')},is_folder=True,fanart=fanartSite,img=iconSite,total_items=ItemCount); 
	set_view('list',view_mode=addst('default-view')); eod()

def MenuAZ():
	##_addon.add_directory({'mode':'ListShows','url':'/anime-index/','site':site,'section':section},{'title':AFColoring('ALL')},is_folder=True,fanart=fanartSite,img=psgn('all')); 
	##_addon.add_directory({'mode':'ListShows','url':'/anime-index/','site':site,'section':section},{'title':AFColoring('#')},is_folder=True,fanart=fanartSite,img=psgn('0')); 
	az='.'; _addon.add_directory({'mode':'ListShows','letter':az,'url':'/anime-index/','site':site,'section':section},{'title':AFColoring(az)},is_folder=True,fanart=fanartSite,img=psgn('0')); 
	az='_'; _addon.add_directory({'mode':'ListShows','letter':az,'url':'/anime-index/','site':site,'section':section},{'title':AFColoring(az)},is_folder=True,fanart=fanartSite,img=psgn('0')); 
	for az in MyAlphabet:
		az=az.upper(); _addon.add_directory({'mode':'ListShows','letter':az,'url':'/anime-index/','site':site,'section':section},{'title':AFColoring(az)},is_folder=True,fanart=fanartSite,img=psgn(az.lower())); 
	###
	###
	set_view('list',view_mode=addst('default-view')); eod()

def MenuGenre():
	for az in MyGenres: 
		i=psgn(az.lower())
		if len(i)==0: i=iconSite
		_addon.add_directory({'mode':'ListShows3','url':'/?genre='+az.replace(' ','%20'),'site':site,'section':section},{'title':AFColoring(az)},is_folder=True,fanart=fanartSite,img=i); 
		_addon.add_directory({'mode':'ListShows3','url':'/?genre='+az.replace(' ','%20').lower(),'site':site,'section':section},{'title':AFColoring(az.lower())},is_folder=True,fanart=fanartSite,img=i); 
	###
	# http://www.animefate.com/?genre=Slice%20of%20Life
	###
	set_view('list',view_mode=addst('default-view')); eod()

### ############################################################################################################
### ############################################################################################################
def SectionMenu():
	#_addon.add_directory({'mode':'ListLatestEpisodes','site':site},{'title':AFColoring('Latest Episodes')},is_folder=True,fanart=fanartSite,img=psgn('latest episodes'))
	#_addon.add_directory({'mode':'ListLatestShows','site':site},{'title':AFColoring('Latest Series')},is_folder=True,fanart=fanartSite,img=psgn('new anime'))
	#_addon.add_directory({'mode':'ListPopularShows','site':site},{'title':AFColoring('Popular Anime Series')},is_folder=True,fanart=fanartSite,img=psgn('most popular'))
	#_addon.add_directory({'mode':'MenuYear','site':site},{'title':AFColoring('Archived By Date')},is_folder=True,fanart=fanartSite,img=psgn('icon'))
	
	#
	
	## Form-Post
	## http://www.animefate.com/search_anime.php search_string=
	
	Tt="Latest Episodes"; _addon.add_directory({'mode':'ListEpisodes','url':'/latest-anime-episodes/','title':Tt,'site':site},{'title':AFColoring(Tt)},is_folder=True,fanart=fanartSite,img=psgn('latest episodes'))
	Tt="Hot This Season"; _addon.add_directory({'mode':'LS_HotThisSeason','url':'','title':Tt,'site':site},{'title':AFColoring(Tt)},is_folder=True,fanart=fanartSite,img=psgn('hot this season'))
	Tt="Movies"; _addon.add_directory({'mode':'ListEpisodes','url':'/anime/anime-movies/','title':Tt,'site':site},{'title':AFColoring(Tt)},is_folder=True,fanart=fanartSite,img=psgn('movies')) #img="http://images1.waoanime.tv/images/225xNx12332122.jpg.pagespeed.ic.gHvo9hKHqX.jpg")
	_addon.add_directory({'mode':'MenuAZ','site':site},{'title':AFColoring('Anime List')},is_folder=True,fanart=fanartSite,img=psgn('anime list'))
	_addon.add_directory({'mode':'MenuGenre','site':site},{'title':AFColoring('Genre List')},is_folder=True,fanart=fanartSite,img=psgn('genre'))
	Tt="Random Anime"; _addon.add_directory({'mode':'ListEpisodes','url':'/random/','title':Tt,'site':site},{'title':AFColoring(Tt)},is_folder=True,fanart=fanartSite,img=psgn('random anime'))
	thisyear=int(datetime.date.today().strftime("%Y"))
	if thisyear > (2017): Tt="2018 Anime Series"; _addon.add_directory({'mode':'ListShows2','url':'/anime-2018/','title':Tt,'site':site},{'title':AFColoring(Tt)},is_folder=True,fanart=fanartSite,img=psgn('anime 2018'))
	if thisyear > (2016): Tt="2017 Anime Series"; _addon.add_directory({'mode':'ListShows2','url':'/anime-2017/','title':Tt,'site':site},{'title':AFColoring(Tt)},is_folder=True,fanart=fanartSite,img=psgn('anime 2017'))
	if thisyear > (2015): Tt="2016 Anime Series"; _addon.add_directory({'mode':'ListShows2','url':'/anime-2016/','title':Tt,'site':site},{'title':AFColoring(Tt)},is_folder=True,fanart=fanartSite,img=psgn('anime 2016'))
	if thisyear > (2014): Tt="2015 Anime Series"; _addon.add_directory({'mode':'ListShows2','url':'/anime-2015/','title':Tt,'site':site},{'title':AFColoring(Tt)},is_folder=True,fanart=fanartSite,img=psgn('anime 2015'))
	Tt="2014 Anime Series"; _addon.add_directory({'mode':'ListShows2','url':'/anime-2014/','title':Tt,'site':site},{'title':AFColoring(Tt)},is_folder=True,fanart=fanartSite,img=psgn('anime 2014'))
	Tt="2013 Anime Series"; _addon.add_directory({'mode':'ListShows2','url':'/anime-2013/','title':Tt,'site':site},{'title':AFColoring(Tt)},is_folder=True,fanart=fanartSite,img=psgn('anime 2013'))
	#Tt="Kokurikozaka Kara Movie"; _addon.add_directory({'mode':'GetMedia','url':'http://www.waoanime.tv/anime-movies-episode-10/','title':Tt,'site':site},{'title':AFColoring(Tt)},is_folder=True,fanart=fanartSite,img=iconSite)
	
	
	# ## ## Things to do later 					## 
	# ## Latest Added Series						## http://www.waoanime.tv/
	# ## Currently Airing Anime					## http://www.waoanime.tv/
	# ## 
	# ## 
	# ## 
	
	#http://www.waoanime.tv/anime-movies-episode-10/
	# ## 
	# ## Anime Series Index
	# ## Anime Movies
	# ## Popular Animes
	# ## Latest Added
	# ## Release Times (Updated)
	# ## Ongoing Series
	# ## 2013 Anime
	# ## 2014 Anime
	# ## Random
	# ## 
	# ## 
	# ## 
	# ## 
	# ## 
	# ## 
	# ## 
	# ## 
	# ## 
	# ## 
	# ## 
	# ## 
	# ## 
	#urllib.unquote_plus()
	#s="%3c%69%66%72%61%6d%65%20%74%69%74%6c%65%3d%22%4d%50%34%55%70%6c%6f%61%64%22%20%74%79%70%65%3d%22%74%65%78%74%2f%68%74%6d%6c%22%20%66%72%61%6d%65%62%6f%72%64%65%72%3d%22%30%22%20%73%63%72%6f%6c%6c%69%6e%67%3d%22%6e%6f%22%20%77%69%64%74%68%3d%22%37%35%30%22%20%68%65%69%67%68%74%3d%22%34%31%30%22%20%73%72%63%3d%22%68%74%74%70%3a%2f%2f%6d%70%34%75%70%6c%6f%61%64%2e%63%6f%6d%2f%65%6d%62%65%64%2d%34%78%62%37%65%39%64%64%38%67%6e%68%2d%37%35%30%78%34%31%30%2e%68%74%6d%6c%22%3e%3c%2f%69%66%72%61%6d%65%3e"
	#debob(urllib.unquote_plus(s))
	
	
	#
	_addon.add_directory({'mode':'FavoritesList','site':site,'section':section             },{'title':cFL(ps('WhatRFavsCalled'),clr1)+cFL(addst('fav.tv.1.name'),clr2)},fanart=fanartSite,img=psgn('favorites 1'))
	_addon.add_directory({'mode':'FavoritesList','site':site,'section':section,'subfav':'2'},{'title':cFL(ps('WhatRFavsCalled'),clr1)+cFL(addst('fav.tv.2.name'),clr2)},fanart=fanartSite,img=psgn('favorites 2'))
	_addon.add_directory({'mode':'FavoritesList','site':site,'section':section,'subfav':'3'},{'title':cFL(ps('WhatRFavsCalled'),clr1)+cFL(addst('fav.tv.3.name'),clr2)},fanart=fanartSite,img=psgn('favorites 3'))
	_addon.add_directory({'mode':'FavoritesList','site':site,'section':section,'subfav':'4'},{'title':cFL(ps('WhatRFavsCalled'),clr1)+cFL(addst('fav.tv.4.name'),clr2)},fanart=fanartSite,img=psgn('favorites 4'))
	_addon.add_directory({'mode':'FavoritesList','site':site,'section':section,'subfav':'5'},{'title':cFL(ps('WhatRFavsCalled'),clr1)+cFL(addst('fav.tv.5.name'),clr2)},fanart=fanartSite,img=psgn('favorites 5'))
	_addon.add_directory({'mode':'FavoritesList','site':site,'section':section,'subfav':'6'},{'title':cFL(ps('WhatRFavsCalled'),clr1)+cFL(addst('fav.tv.6.name'),clr2)},fanart=fanartSite,img=psgn('favorites 6'))
	_addon.add_directory({'mode':'FavoritesList','site':site,'section':section,'subfav':'7'},{'title':cFL(ps('WhatRFavsCalled'),clr1)+cFL(addst('fav.tv.7.name'),clr2)},fanart=fanartSite,img=psgn('favorites 7'))
	###
	if (len(addst("LastShowListedURL")) > 0): 
		pars={'site':site,'section':section,'mode':'ListEpisodes','url':addst("LastShowListedURL"),'title':addst("LastShowListedNAME"),'imdb_id':addst("LastShowListedIMDBID"),'img':addst("LastShowListedIMG"),'fimg':addst("LastShowListedFANART")}; 
		title=AFColoring(addst("LastShowListedNAME"))+CR+cFL('[Last Show]',clr1); 
		_addon.add_directory(pars,{'title':title},fanart=addst("LastShowListedFANART"),img=addst("LastShowListedIMG"),is_folder=True); 
	if (len(addst("LastEpisodeListedURL")) > 0): 
		pars={'site':site,'section':section,'mode':'GetMedia','url':addst("LastEpisodeListedURL"),'title':addst("LastEpisodeListedNAME"),'imdb_id':addst("LastEpisodeListedIMDBID"),'img':addst("LastEpisodeListedIMG"),'fimg':addst("LastEpisodeListedFANART"),'stitle':addst("LastEpisodeListedSTITLE"),'etitle':addst("LastEpisodeListedETITLE"),'e':addst("LastEpisodeListedEpNo"),'s':addst("LastEpisodeListedSNo"),'e2':addst("LastEpisodeListedEpNo2")}; 
		title=AFColoring(addst("LastEpisodeListedNAME"))+CR+cFL('[Last Episode]',clr1); 
		_addon.add_directory(pars,{'title':title},fanart=addst("LastEpisodeListedFANART"),img=addst("LastEpisodeListedIMG"),is_folder=True); 
	###
	_addon.add_directory({'mode':'About','site':site,'section':section},{'title':AFColoring('About')},is_folder=True,fanart=fanartSite,img='http://i.imgur.com/0h78x5V.png') # iconSite
	###
	set_view('list',view_mode=addst('default-view')); eod()
### ############################################################################################################
### ############################################################################################################
def mode_subcheck(mode='',site='',section='',url=''):
	if (mode=='SectionMenu'): 		SectionMenu()
	elif (mode=='') or (mode=='main') or (mode=='MainMenu'): SectionMenu()
	elif (mode=='SubMenu'): 			SubMenu()
	elif (mode=='ListShows'): 		ListShows(url,addpr('letter',''))
	elif (mode=='ListShows2'): 		ListShows2(url)
	elif (mode=='ListShows3'): 		ListShows3(url)
	elif (mode=='ListEpisodes'): 	ListEpisodes(url,addpr('title',''),addpr('imdb_id',''),addpr('img',''),addpr('fimg',''))
	elif (mode=='ListLatestEpisodes'): ListLatestEpisodes()
	elif (mode=='ListLatestEpisodes2'): ListLatestEpisodes(url)
	elif (mode=='ListLatestShows'): ListLatestShows()
	elif (mode=='ListPopularShows'): ListPopularShows()
	
	elif (mode=='LS_HotThisSeason'): 		ListShows_HotThisSeason(url)
	
	
	elif (mode=='GetMedia'): 			GetMedia(url,addpr('title',''),addpr('imdb_id',''),addpr('img',''),addpr('fimg',''),addpr('stitle',''),addpr('etitle',''),addpr('e',''),addpr('s',''),addpr('e2',''),addpr('wwT',''))
	#elif (mode=='Hosts'): 				Browse_Hosts(url)
	#elif (mode=='Search'): 			Search_Site(title=addpr('title',''),url=url,page=page,metamethod=addpr('metamethod','')) #(site,section)
	#elif (mode=='SearchLast'): 	Search_Site(title=addst('LastSearchTitle'+SiteTag),url=url,page=page,metamethod=addpr('metamethod',''),endit=tfalse(addpr('endit','true'))) #(site,section)
	elif (mode=='About'): 				eod(); DoA('Back'); About()
	#elif (mode=='FavoritesList'): Fav_List(site=site,section=section,subfav=addpr('subfav',''))
	elif (mode=='MenuAZ'): 				MenuAZ()
	elif (mode=='MenuGenre'): 		MenuGenre()
	elif (mode=='FavoritesList'): Fav_List(site=site,section=section,subfav=addpr('subfav',''))
	elif (mode=='PlayURL'): 						PlayURL(url)
	elif (mode=='PlayURLs'): 						PlayURLs(url)
	elif (mode=='PlayURLstrm'): 				PlayURLstrm(url)
	elif (mode=='PlayFromHost'): 				PlayFromHost(url)
	elif (mode=='PlayVideo'): 					PlayVideo(url)
	elif (mode=='PlayItCustom'): 				PlayItCustom(url,addpr('streamurl',''),addpr('img',''),addpr('title',''))
	elif (mode=='PlayItCustomL2A'): 		PlayItCustomL2A(url,addpr('streamurl',''),addpr('img',''),addpr('title',''))
	elif (mode=='Settings'): 						_addon.addon.openSettings() # Another method: _plugin.openSettings() ## Settings for this addon.
	elif (mode=='ResolverSettings'): 		import urlresolver; urlresolver.display_settings()  ## Settings for UrlResolver script.module.
	elif (mode=='ResolverUpdateHostFiles'):	import urlresolver; urlresolver.display_settings()  ## Settings for UrlResolver script.module.
	elif (mode=='TextBoxFile'): 				TextBox2().load_file(url,addpr('title','')); #eod()
	elif (mode=='TextBoxUrl'):  				TextBox2().load_url(url,addpr('title','')); #eod()
	elif (mode=='MenuYear'): 						MenuYear()
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
	elif (mode=='refresh_meta'):			refresh_meta(addpr('video_type',''),addpr('title',''),addpr('imdb_id',''),addpr('alt_id',''),addpr('year',''))
	else: myNote(header='Site:  "'+site+'"',msg=mode+' (mode) not found.'); import mMain
mode_subcheck(addpr('mode',''),addpr('site',''),addpr('section',''),addpr('url',''))
### ############################################################################################################
### ############################################################################################################
