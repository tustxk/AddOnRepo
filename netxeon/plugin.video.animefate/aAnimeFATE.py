### ############################################################################################################
###	#	
### # Site: 				#		Anime FATE - http://www.animefate.com/
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
SiteName='A[COLOR firebrick][I]nime[/I][/COLOR] F[COLOR mediumpurple]ate[/COLOR]  [v0.0.8]  [Anime]'
SiteTag='animefate.com'
mainSite='http://www.animefate.com'
mainSite2='http://www.animefate.com'
iconSite='http://i.imgur.com/aG3GkmR.png' #_artIcon #'http://i.imgur.com/aG3GkmR.png' #'http://www.animefate.com/wp-content/uploads/2012/09/animefate_logo.png'
fanartSite='http://i.imgur.com/PcZjx2D.jpg' #_artFanart #'http://www.animefate.com/wp-content/themes/MagMan/i/footer-overlay.png'
colors={'0':'white','1':'red','2':'blue','3':'green','4':'yellow','5':'orange','6':'lime','7':'','8':'cornflowerblue','9':'blueviolet','10':'hotpink','11':'pink','12':'tan','13':'firebrick','14':'mediumpurple'}

CR='[CR]'
MyAlphabet=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
MyGenres=[' Action','Action','Adventure','Animation','Cars','Comedy','Dementia','Demons','Drama','Ecchi','Fantasy','Game','Harem','Historical','Horror','Josei','Kids','Magic','Martial Arts','Mecha','Military','Movie','Music','Mutants','Mystery','Parody','Police','Psychological','Romance','Samurai','School','Sci-Fi','Seinen','Shoujo','Shoujo Ai','Shounen','Shounen Ai','Slice of Life','Space','Sports','Super Power','Supernatural','Thriller','Vampire']
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
		m+=CR+'* TrollVid'
		m+=CR+'* UploadCrazy'
		m+=CR+CR+'Features:  '
		m+=CR+'* Browse Shows'
		m+=CR+'* Browse Episodes'
		m+=CR+'* Browse Host Links'
		m+=CR+'* Play Videos with UrlResolver'
		m+=CR+'* Download Videos with UrlResolver'
		m+=CR+'* MetaData for Shows and 1st Season Episodes where data is available.'
		m+=CR+'* MetaData auto-disabled for Anime List - ALL.  This is to prevent hammering with the huge list of nearly 400 shows.'
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
			,'ongoing': 									s+"EUak0Sg"+t
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
			,'icon': 											s+"aG3GkmR"+t
			,'last': 											s+"3g6S9UH"+t
			,'latest episodes': 					s+"r19ycox"+t
			,'latest updates': 						s+"E86Rnq5"+t
			,'most popular': 							s+"N69lo3G"+t
			,'new anime': 								s+"wZN1olE"+t
			,'search': 										s+"MTnRQJ3"+t
			,'fanart': 										s+"PcZjx2D"+t
#			,'': 								s+""+t
#			,'': 								s+""+t
#			,'': 								s+""+t
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
	s='<iframe\s+id="video"\s+src="(http[s]*://.+?)"'; 
	try: matches=re.compile(s).findall(html); deb('# of matches found',str(len(matches))); debob(matches)
	except: matches=''; 
	if len(matches) > 0:
		#for (url,img,name,genres,status,NoEps,year) in matches:
		iC=len(matches); 
		try: import urlresolver
		except: pass
		for m in matches:
			###
			if "http://animeonair.com/" in m: m=m.replace("http://animeonair.com/","http://videoboxone.com/")
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
	set_view('list',view_mode=addst('links-view')); eod()

def ListPopularShows(Url=mainSite):
	#if len(Url)==0: return
	if mainSite not in Url: Url=mainSite+Url; 
	deb('Url',Url); html=messupText(nolines(nURL(Url)),True,True); deb('length of html',str(len(html))); #debob(html); 
	if len(html)==0: return
	##s='</div><div class=\'pop_img_list\'>\s*<div class="img_hor_strip">\s*<a href="(http://www.animefate.com/series/.+?/)" title=".+? English Dubbed Anime">\s*'; 
	##s+='<img src="(http://www.animefate.com/images/.+?-\d+x\d+.[jpg|png|gif]+)" alt=".+?" title=".+?" />\s*</div>\s*<p class="pop_anime_name">(.+?)</p>\s*</a>'; 
	s='class=\'pop_img_list\'>\s*<div class="img_hor_strip">\s*'; 
	s+='<a href="(http://www.animefate.com/series/.+?/)" title=".+? English Dubbed Anime">\s*'; 
	s+='<img src="(http://www.animefate.com/images/.+?-\d+x\d+\.(?:jpg|png|gif)?)" alt=".+?" title=".+?"\s*/>\s*'; 
	s+='(?:</div>\s*)?<p class="pop_anime_name">\s*(.+?)\s*</p'; 
	html=str(html).replace("<div class='pop_img_list'>","<div\n\r class='pop_img_list'>")
	try: matches=re.compile(s).findall(html); deb('# of matches found',str(len(matches))); #debob(matches)
	except: matches=''; 
	if len(matches) > 0:
		iC=len(matches); enMeta=tfalse(addst("enableMeta","false")); 
		if enMeta==True:
			try: from metahandler import metahandlers; grab=metahandlers.MetaData(preparezip=False); 
			except: debob("filed to import metahandler"); 
		for (img,url,name) in matches:
			img=FixImage(img); cMI=[]; img=img.replace(' ','%20'); fimg=fanartSite; deb('img',img); Genres2=""; g="<a href='http://www.animefate.com/.genre=.+?'>\s*(.+?)\s*</a>"; plot=""; labs={}; 
			#try: Genres1=re.compile(g).findall(genres); debob(Genres1); 
			#except: Genres1=""; 
			#for g in Genres1: Genres2+="["+g+"] "; 
			if enMeta==True: 
				try: labs=grab.get_meta('tvshow',name); 
				except: pass
				try:
					if len(labs[u'cover_url']) > 0: img=labs[u'cover_url']; 
				except: pass
				try:
					if len(labs[u'backdrop_url']) > 0: fimg=labs[u'backdrop_url']; 
				except: pass
			else: labs[u'plot']=''; labs[u'imdb_id']=''; labs[u'title']=name; labs[u'year']=''; 
			debob(labs); 
			#labs[u'plot']=''; labs[u'imdb_id']=''; labs[u'title']=name; labs[u'year']=''; 
			#
			#plot+=CR+"Genres:  [COLOR purple]"+Genres2+"[/COLOR]"; #plot+="[CR]Year: [COLOR purple]"+year+"[/COLOR]"; plot+=" [COLOR black]|[/COLOR] Status: [COLOR purple]"+status+"[/COLOR]"; plot+=" [COLOR black]|[/COLOR] Episodes: [COLOR purple]"+NoEps+"[/COLOR]"; 
			pars={'mode':'ListEpisodes','url':url,'title':name,'imdb_id':labs[u'imdb_id'],'img':img,'fimg':fimg,'site':site,'section':section}; 
			labs[u'plot']=plot+CR+CR+cFL(labs[u'plot'],'mediumpurple'); labs[u'title']=AFColoring(name); 
			labs[u'plot']=messupText(labs[u'plot'],True,True,True); labs[u'title']=messupText(labs[u'title'],True,True,True); 
			#Clabs=labs; 
			Clabs={'title':name,'year':labs[u'year'],'url':url,'commonid':labs[u'imdb_id'],'img':img,'fanart':fimg,'plot':labs[u'plot'],'todoparams':_addon.build_plugin_url(pars),'site':site,'section':section}; 
			try: cMI=ContextMenu_Series(Clabs); 
			#try: cMI=ContextMenu_Episodes(Clabs); 
			except: pass
			#labs[u'title']+=cFL(' ('+cFL(year,'mediumpurple')+') ['+cFL(NoEps,'blue')+']'+CR+'['+status+']','purple')
			try: _addon.add_directory(pars,labs,is_folder=True,fanart=fimg,img=img,contextmenu_items=cMI,total_items=iC)
			except: pass
	set_view('tvshows',view_mode=addst('tvshows-view')); eod()
	#set_view('episodes',view_mode=addst('episode-view')); eod()

def ListLatestShows(Url=mainSite):
	#if len(Url)==0: return
	if mainSite not in Url: Url=mainSite+Url; 
	deb('Url',Url); html=messupText(nolines(nURL(Url)),True,True); deb('length of html',str(len(html))); #debob(html); 
	if len(html)==0: return
	s='<div class=\'index_img_list\'><img src="(http://www.animefate.com/images/.+?-\d+x\d+.[jpg|png|gif]+)" alt=".+?" title=".+?"\s*/>\s*'; 
	s+='</div>\s*<div class="blog-title">\s*'; 
	s+='<h2>\s*<a href="(http://www.animefate.com/series/.+?/)" title=".+? English Dubbed Anime">\s*'; 
	s+='<strong>\s*(.+?)\s*</strong>\s*</a>\s*</h2>\s*'; 
	s+='<p class="small_post_info">\s*Genres:\s*(.+?)\s*</p>\s*</div>'; 
	html=str(html).replace('<div class="clear"></div>','<div class="clear">\n</div>')
	try: matches=re.compile(s).findall(html); deb('# of matches found',str(len(matches))); #debob(matches)
	except: matches=''; 
	if len(matches) > 0:
		iC=len(matches); enMeta=tfalse(addst("enableMeta","false")); 
		if enMeta==True:
			try: from metahandler import metahandlers; grab=metahandlers.MetaData(preparezip=False); 
			except: debob("filed to import metahandler"); 
		for (img,url,name,genres) in matches:
			img=FixImage(img); cMI=[]; img=img.replace(' ','%20'); fimg=fanartSite; deb('img',img); Genres2=""; g="<a href='http://www.animefate.com/.genre=.+?'>\s*(.+?)\s*</a>"; plot=""; labs={}; 
			try: Genres1=re.compile(g).findall(genres); debob(Genres1); 
			except: Genres1=""; 
			for g in Genres1: Genres2+="["+g+"] "; 
			if enMeta==True: 
				try: labs=grab.get_meta('tvshow',name); 
				except: pass
				try:
					if len(labs[u'cover_url']) > 0: img=labs[u'cover_url']; 
				except: pass
				try:
					if len(labs[u'backdrop_url']) > 0: fimg=labs[u'backdrop_url']; 
				except: pass
			else: labs[u'plot']=''; labs[u'imdb_id']=''; labs[u'title']=name; labs[u'year']=''; 
			#labs[u'plot']=''; labs[u'imdb_id']=''; labs[u'title']=name; labs[u'year']=''; 
			#
			plot+=CR+"Genres:  [COLOR purple]"+Genres2+"[/COLOR]"; #plot+="[CR]Year: [COLOR purple]"+year+"[/COLOR]"; plot+=" [COLOR black]|[/COLOR] Status: [COLOR purple]"+status+"[/COLOR]"; plot+=" [COLOR black]|[/COLOR] Episodes: [COLOR purple]"+NoEps+"[/COLOR]"; 
			pars={'mode':'ListEpisodes','url':url,'title':name,'imdb_id':labs[u'imdb_id'],'img':img,'fimg':fimg,'site':site,'section':section}; 
			labs[u'plot']=plot+CR+CR+cFL(labs[u'plot'],'mediumpurple'); labs[u'title']=AFColoring(name); 
			labs[u'plot']=messupText(labs[u'plot'],True,True,True); labs[u'title']=messupText(labs[u'title'],True,True,True); 
			#Clabs=labs; 
			Clabs={'title':name,'year':labs[u'year'],'url':url,'commonid':labs[u'imdb_id'],'img':img,'fanart':fimg,'plot':labs[u'plot'],'todoparams':_addon.build_plugin_url(pars),'site':site,'section':section}; 
			try: cMI=ContextMenu_Series(Clabs); 
			#try: cMI=ContextMenu_Episodes(Clabs); 
			except: pass
			#labs[u'title']+=cFL(' ('+cFL(year,'mediumpurple')+') ['+cFL(NoEps,'blue')+']'+CR+'['+status+']','purple')
			try: _addon.add_directory(pars,labs,is_folder=True,fanart=fimg,img=img,contextmenu_items=cMI,total_items=iC)
			except: pass
	set_view('tvshows',view_mode=addst('tvshows-view')); eod()
	#set_view('episodes',view_mode=addst('episode-view')); eod()

def ListLatestEpisodes(Url=mainSite):
	#if len(Url)==0: return
	if mainSite not in Url: Url=mainSite+Url; 
	deb('Url',Url); html=messupText(nolines(nURL(Url)),True,True); deb('length of html',str(len(html))); #debob(html); 
	if len(html)==0: return
	s=''
	s='<div class="blog-title">\s*<div class=\'index_img_list\'>'; 
	s+='<img src="(http://www.animefate.com/images/.+?-\d+x\d+\.(?:jpg|png|gif)?)" alt=".+?" title=".+?"\s*/>\s*'; 
	s+='</div>\s*<h2>\s*<a href="(http://www.animefate.com/.+?/)">\s*<strong>\s*(.+?)\s*</strong>\s*</a>\s*</h2>\s*'; 
	s+='<p class="small_post_info">Posted on:\s+(.+?)\s*</p>\s*'; 
	s+='<p class="small_post_info">Full Episodes List:\s+'; 
	s+='<a href="(http://www.animefate.com/series/.+?/)" (?:title="View all posts in .+?" )?rel="category tag">(.+?)</a'; 
	##s+='>\s*</p>\s*</div>\s*<div class="clear"></div>'; 
	html=str(html).replace('<div class="clear"></div>','<div class="clear">\n</div>')
	#try: 
	matches=re.compile(s).findall(html); deb('# of matches found',str(len(matches))); debob(matches)
	#except: matches=''; 
	if len(matches) > 0:
		iC=len(matches) * 2; enMeta=tfalse(addst("enableMeta","false")); 
		if enMeta==True:
			try: from metahandler import metahandlers; grab=metahandlers.MetaData(preparezip=False); 
			except: debob("filed to import metahandler"); 
		for (img,url,name,datestamp,showUrl,showName) in matches:
			img=FixImage(img); cMI=[]; img=img.replace(' ','%20'); fimg=fanartSite; deb('img',img); Genres2=""; g="<a href='http://www.animefate.com/.genre=.+?'>\s*(.+?)\s*</a>"; plot=""; labs={}; 
			if "Episode " in showName: 
				try: e=re.compile("Episode\s*(\d+)").findall(showName)[0]; 
				except: e=""; 
			else: e=""; 
			#try: Genres1=re.compile(g).findall(genres); debob(Genres1); 
			#except: Genres1=""; 
			#for g in Genres1: Genres2+="["+g+"] "; 
			#Genres2=str(Genres1); 
			if enMeta==True: 
				try: labs=grab.get_meta('tvshow',showName); 
				except: pass
				try:
					if len(labs[u'cover_url']) > 0: img=labs[u'cover_url']; 
				except: pass
				try:
					if len(labs[u'backdrop_url']) > 0: fimg=labs[u'backdrop_url']; 
				except: pass
			else: labs[u'plot']=''; labs[u'imdb_id']=''; labs[u'title']=name; labs[u'year']=''; 
			#labs[u'plot']=''; labs[u'imdb_id']=''; labs[u'title']=name; labs[u'year']=''; 
			labs[u'title']=name; 
			#
			#plot+=CR+"Genres:  [COLOR purple]"+Genres2+"[/COLOR]"; plot+="[CR]Year: [COLOR purple]"+year+"[/COLOR]"; plot+=" [COLOR black]|[/COLOR] Status: [COLOR purple]"+status+"[/COLOR]"; plot+=" [COLOR black]|[/COLOR] Episodes: [COLOR purple]"+NoEps+"[/COLOR]"; 
			pars={'mode':'GetMedia','url':url,'title':name,'imdb_id':labs[u'imdb_id'],'img':img,'fimg':fimg,'site':site,'section':section,'e':str(e),'s':str(1),'e2':str(e),'e3':str(0)}; 
			labs[u'plot']=plot+CR+CR+cFL(labs[u'plot'],'mediumpurple'); labs[u'title']=cFL(name,'blue'); 
			labs[u'plot']=messupText(labs[u'plot'],True,True,True); labs[u'title']=messupText(labs[u'title'],True,True,True); 
			Clabs={'title':name,'year':labs[u'year'],'url':url,'img':img,'fanart':fimg,'plot':labs[u'plot'],'todoparams':_addon.build_plugin_url(pars),'site':site,'section':section}; 
			try: cMI=ContextMenu_Episodes(Clabs); 
			except: pass
			#labs[u'title']+=cFL(' ('+cFL(year,'mediumpurple')+') ['+cFL(NoEps,'blue')+']'+CR+'['+status+']','purple')
			labs[u'title']+=CR+cFL('['+datestamp+']',colors['13']); 
			### Episode
			try: labs2=copy.deepcopy(labs); 
			except: labs2=labs; 
			labs2[u'title']=showName; 
			pars2={'mode':'ListEpisodes','url':showUrl,'title':name,'imdb_id':labs[u'imdb_id'],'img':img,'fimg':fimg,'site':site,'section':section}; 
			labs2[u'title']=AFColoring(showName); 
			Clabs2={'title':name,'year':labs[u'year'],'url':url,'commonid':labs[u'imdb_id'],'img':img,'fanart':fimg,'plot':labs[u'plot'],'todoparams':_addon.build_plugin_url(pars2),'site':site,'section':section}; 
			try: cMI2=ContextMenu_Series(Clabs2); 
			except: pass
			try: _addon.add_directory(pars2,labs2,is_folder=True,fanart=fimg,img=img,contextmenu_items=cMI2,total_items=iC)
			except: pass
			### Show
			try: _addon.add_directory(pars,labs,is_folder=True,fanart=fimg,img=img,contextmenu_items=cMI,total_items=iC)
			except: pass
	#set_view('tvshows',view_mode=addst('tvshows-view')); eod()
	set_view('episodes',view_mode=addst('episode-view')); eod()

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
	##s='<li>\s*<a href="(http://www.animefate.com/.+?/)" rel="bookmark" title=".+?">\s*<p class="episode_number">\s*(.+?)\s*</p>\s*<p title="Added on .+?" class="date_published">(.+?)</p>\s*</a>\s*<div class="clear"></div>\s*</li>'; 
	s='<li>\s*<a href="(http://www.animefate.com/.+?/)" rel="bookmark" title=".+?">\s*<p class="episode_number">\s*(.+?)\s*</p>\s*<p title="Added on .+?" class="date_published">(.+?)</p>\s*</a'; 
	
	html=str(html).replace('<div class="clear"></div>','<div class="clear">\n</div>')
	try: matches=re.compile(s).findall(html); deb('# of matches found',str(len(matches))); #debob(matches)
	except: matches=''; 
	if len(matches) > 0:
		s='1'; enMeta=tfalse(addst("enableMeta","false")); 
		#for (url,img,name,genres,status,NoEps,year) in matches:
		iC=len(matches); n=False; e3='0'
		if enMeta==True:
			try: from metahandler import metahandlers; grab=metahandlers.MetaData(preparezip=False); 
			except: debob("filed to import metahandler"); 
			#ShowLabs=grab.get_seasons(tvshowtitle=title,imdb_id=imdb_id,seasons=s,overlay=6); debob(ShowLabs); 
			#labsZ=grab.get_episode_meta(tvshowtitle=title,imdb_id=imdb_id,season=s,episode='1',air_date='',episode_title='',overlay=6); debob(labsZ); 
		#matches=sorted(matches,key=lambda nn: (nn[1]),reverse=True)
		if 'Movie ' in title: s='0'; enMeta=False; 
		for (url,name,datestamp) in matches[::-1]:
			debob([url,name,datestamp]); 
			cMI=[]; labs={}; #labs['plot']=''; labs['plotoutline']=''; labs['showtitle']=''; labs['episodetitle']=''; labs['videoid']=''; 
			if "Episode " in name: 
				try: e=re.compile("Episode\s*(\d+)").findall(name)[0]; 
				except: e=""; 
				if len(str(e))==0:
					try: e=re.compile("Movie\s*(\d+)").findall(name)[0]; 
					except: e=""; 
			else: e=""; 
			name=name.replace(title,''); e2=copy.deepcopy(e); e4=''+str(e); 
			#name=name.replace(title+" Episode","Episode")
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
					try: labs=grab.get_episode_meta(tvshowtitle=title,imdb_id=imdb_id,season=s,episode=e2,air_date='',episode_title='',overlay=6); 
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
			if n==True: labs[u'plot']=''; labs[u'imdb_id']=''; labs[u'title']=name; labs[u'year']=''; 
			if len(labs[u'title'])==0: labs[u'title']=name; 
			if len(labs[u'title'])==0: labs[u'title']=title; 
			#elif labs[u'title']==" ": labs[u'title']=name; 
			#labs[u'title']=labs[u'title'].replace(title+" Episode","Episode")
			etitle=labs[u'title']; 
			#labs[u'title']=cFL(str(e)+') ','blue')+AFColoring(labs[u'title']); 
			if len(e) > 0: labs[u'title']=cFL(str(e4)+') ','blue')+AFColoring(labs[u'title']); 
			else: labs[u'title']=AFColoring(labs[u'title'])
			labs[u'plot']=CR+cFL(labs[u'plot'],'mediumpurple'); labs[u'title']+=CR+cFL("["+datestamp+"]",colors['13']); 
			labs[u'plot']+=CR+cFL(str(e)+")",'blue')+cFL(" Season "+cFL(str(s),colors['13'])+" Episode "+cFL(str(e2),colors['13'])+"",'mediumpurple')
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

def ListShows(Url):
	if len(Url)==0: return
	if mainSite not in Url: Url=mainSite+Url; 
	deb('Url',Url); html=messupText(nolines(nURL(Url)),True,True); deb('length of html',str(len(html))); #debob(html); 
	if len(html)==0: return
	##s='<div class=\'anime_list_info\'>\s*<a href="(http://www.animefate.com/series/.+?/)" title=".+? English Dubbed Anime">\s*<div class="info_list_cover">\s*'; #s+='<img src="(http://www.animefate.com/images/.+?-\d+x\d+.[jpg|png|gif]+)" alt=".+?" title=".+?" />\s*</div>\s*<div class="info_list_description">\s*'; #s+='<p class=\'anime_list_title\'><strong>(.+?)</strong></p></a><p><strong>Genres: </strong>(.+?)</p>'; #s+='<p><strong>Status: </strong><span class=\'.+?\'>\s*(\D+)\s*</span></p>'; #s+='<p><strong>No. of Episodes: </strong>\s*(\d*)\s*</p><p><strong>Released: </strong>\s*(\d*)\s*</p>\s*</div>\s*</div>'; 
	#s="<div class='index_img_list\s*[clear]*'>"+'<img src="(http://www.animefate.com/images/.+?)" alt=".+?" title=".+?" /></div>'; s+='<li><div class="listupdate">'; s+="<h2><a href='(http://www.animefate.com/series/.+?/)'>(.+?)</a></h2>"; s+="<span><em>Genres: </em>(.+?)</span>"; s+='<div class="clear"></div></div></li>'; 
	s="class='index_img_list\s*[clear]*'>"+'<img src="(http://www.animefate.com/images/.+?)" alt=".+?" title=".+?" /></div>'; s+='<li><div class="listupdate">'; s+="<h2><a href='(http://www.animefate.com/series/.+?/)'>(.+?)</a></h2>"; s+="<span><em>Genres: </em>(.+?)</span>"; s+='<div class="clear"></div></div></li>'; 
	
	html=str(html).replace("<div class='anime_list_info'>","<div\n\r class='anime_list_info'>")
	html=str(html).replace("<div class='index_img_list'>","<div\n\r class='index_img_list'>")
	try: matches=re.compile(s).findall(html); deb('# of matches found',str(len(matches))); #debob(matches)
	except: matches=''; 
	if len(matches) > 0:
		#for (url,img,name,genres,status,NoEps,year) in matches:
		iC=len(matches); enMeta=tfalse(addst("enableMeta","false")); 
		if enMeta==True:
			try: from metahandler import metahandlers; grab=metahandlers.MetaData(preparezip=False); 
			except: debob("filed to import metahandler"); 
		for (img,url,name,genres) in matches:
			img=FixImage(img); cMI=[]; img=img.replace(' ','%20'); fimg=fanartSite; deb('img',img); Genres2=""; g="<a href='http://www.animefate.com/.genre=.+?'>\s*(.+?)\s*</a>"; plot=""; labs={}; 
			try: Genres1=re.compile(g).findall(genres); debob(Genres1); 
			except: Genres1=""; 
			for g in Genres1: Genres2+="["+g+"] "; 
			#Genres2=str(Genres1); 
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
			plot+=CR+"Genres:  [COLOR purple]"+Genres2+"[/COLOR]"; #plot+="[CR]Year: [COLOR purple]"+year+"[/COLOR]"; #plot+="[CR]Status: [COLOR purple]"+status+"[/COLOR]"; #plot+="[CR]Number of Episodes: [COLOR purple]"+NoEps+"[/COLOR]"; 
			pars={'mode':'ListEpisodes','url':url,'title':name,'imdb_id':labs[u'imdb_id'],'img':img,'fimg':fimg,'site':site,'section':section}; 
			labs[u'plot']=plot+CR+CR+cFL(labs[u'plot'],'mediumpurple'); labs[u'title']=AFColoring(name); 
			#Clabs=labs; 
			Clabs={'title':name,'year':labs[u'year'],'url':url,'commonid':labs[u'imdb_id'],'img':img,'fanart':fimg,'plot':labs[u'plot'],'todoparams':_addon.build_plugin_url(pars),'site':site,'section':section}; 
			try: cMI=ContextMenu_Series(Clabs); 
			except: pass
			try: _addon.add_directory(pars,labs,is_folder=True,fanart=fimg,img=img,contextmenu_items=cMI,total_items=iC,context_replace=False)
			except: pass
	set_view('tvshows',view_mode=addst('tvshows-view')); eod()

def ListShows2(Url):
	if len(Url)==0: return
	if mainSite not in Url: Url=mainSite+Url; 
	deb('Url',Url); html=messupText(nolines(nURL(Url)),True,True); deb('length of html',str(len(html))); #debob(html); 
	if len(html)==0: return
	##s='<div class=\'anime_list_info\s*[clear]*\'>\s*<a href="(http://www.animefate.com/series/.+?/)" title=".+? English Dubbed Anime">\s*<div class="info_list_cover">\s*'; s+='<img src="(http://www.animefate.com/images/.+?-\d+x\d+.[jpg|png|gif]+)" alt=".+?" title=".+?" />\s*</div>\s*<div class="info_list_description">\s*'; s+='<p class=\'anime_list_title\'><strong>(.+?)</strong></p></a><p><strong>Genres: </strong>(.+?)'; s+='<p><strong>Status: </strong><span class=\'.+?\'>\s*(\D+)\s*</span></p>'; s+='<p><strong>No. of Episodes: </strong>\s*(\d*)\s*</p><p><strong>Released: </strong>\s*(\d*)\s*</p>\s*</div>\s*</div>'; 
	s='class=\'anime_list_info\s*(?:clear)?\'>\s*'; 
	s+='<a href="(http://www.animefate.com/series/.+?/)" title=".+? English Dubbed Anime">\s*'; 
	s+='<div class="info_list_cover">\s*'; 
	s+='<img src="(http://www.animefate.com/images/.+?-\d+x\d+\.(?:jpg|png|gif)?)" alt=".+?" title=".+?" />\s*'; 
	s+='</div>\s*<div class="info_list_description">\s*'; 
	s+='<p class=\'anime_list_title\'><strong>(.+?)</strong></p></a>'; 
	s+='<p><strong>Genres: </strong>(.+?)'; 
	s+='<p><strong>Status: </strong><span class=\'.+?\'>\s*(\D+)\s*</span></p>'; 
	s+='<p><strong>No. of Episodes: </strong>\s*(\d*)\s*</p>'; 
	s+='<p><strong>Released: </strong>\s*(\d*)\s*</p>\s*</div>\s*</div'; 
	
	html=str(html).replace("<div class='anime_list_info'>","<div\n\r class='anime_list_info'>")
	try: matches=re.compile(s).findall(html); deb('# of matches found',str(len(matches))); debob(matches)
	except: matches=''; 
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
	_addon.add_directory({'mode':'ListShows2','url':'/anime-list/?starting_char=all','site':site,'section':section},{'title':AFColoring('ALL')},is_folder=True,fanart=fanartSite,img=psgn('all')); 
	_addon.add_directory({'mode':'ListShows2','url':'/anime-list/','site':site,'section':section},{'title':AFColoring('#')},is_folder=True,fanart=fanartSite,img=psgn('0')); 
	for az in MyAlphabet:
		az=az.upper(); _addon.add_directory({'mode':'ListShows2','url':'/anime-list/?starting_char='+az,'site':site,'section':section},{'title':AFColoring(az)},is_folder=True,fanart=fanartSite,img=psgn(az.lower())); 
	###
	# http://www.animefate.com/anime-list/?starting_char=all
	# http://www.animefate.com/anime-list/
	# http://www.animefate.com/anime-list/?starting_char=A
	###
	set_view('list',view_mode=addst('default-view')); eod()

def MenuGenre():
	for az in MyGenres: 
		i=psgn(az.lower())
		if len(i)==0: i=iconSite
		_addon.add_directory({'mode':'ListShows','url':'/?genre='+az.replace(' ','%20'),'site':site,'section':section},{'title':AFColoring(az)},is_folder=True,fanart=fanartSite,img=i); 
	###
	# http://www.animefate.com/?genre=Slice%20of%20Life
	###
	set_view('list',view_mode=addst('default-view')); eod()

def SectionMenu():
	_addon.add_directory({'mode':'ListLatestEpisodes','site':site},{'title':AFColoring('Latest Episodes')},is_folder=True,fanart=fanartSite,img=psgn('latest episodes'))
	_addon.add_directory({'mode':'ListLatestShows','site':site},{'title':AFColoring('Latest Series')},is_folder=True,fanart=fanartSite,img=psgn('new anime'))
	_addon.add_directory({'mode':'ListPopularShows','site':site},{'title':AFColoring('Popular Anime Series')},is_folder=True,fanart=fanartSite,img=psgn('most popular'))
	_addon.add_directory({'mode':'MenuAZ','site':site},{'title':AFColoring('Anime List')},is_folder=True,fanart=fanartSite,img=psgn('alphabetical'))
	_addon.add_directory({'mode':'MenuYear','site':site},{'title':AFColoring('Archived By Date')},is_folder=True,fanart=fanartSite,img=psgn('icon'))
	_addon.add_directory({'mode':'MenuGenre','site':site},{'title':AFColoring('Genre List')},is_folder=True,fanart=fanartSite,img=psgn('genre'))
	#
	
	## Form-Post
	## http://www.animefate.com/search_anime.php search_string=
	
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
	if (mode=='SectionMenu'): 		SectionMenu()
	elif (mode=='') or (mode=='main') or (mode=='MainMenu'): SectionMenu()
	elif (mode=='SubMenu'): 			SubMenu()
	elif (mode=='ListShows'): 		ListShows(url)
	elif (mode=='ListShows2'): 		ListShows2(url)
	elif (mode=='ListEpisodes'): 	ListEpisodes(url,addpr('title',''),addpr('imdb_id',''),addpr('img',''),addpr('fimg',''))
	elif (mode=='ListLatestEpisodes'): ListLatestEpisodes()
	elif (mode=='ListLatestEpisodes2'): ListLatestEpisodes(url)
	elif (mode=='ListLatestShows'): ListLatestShows()
	elif (mode=='ListPopularShows'): ListPopularShows()
	elif (mode=='GetMedia'): 			GetMedia(url,addpr('title',''),addpr('imdb_id',''),addpr('img',''),addpr('fimg',''),addpr('stitle',''),addpr('etitle',''),addpr('e',''),addpr('s',''),addpr('e2',''),addpr('wwT',''))
	#elif (mode=='Hosts'): 				Browse_Hosts(url)
	#elif (mode=='Search'): 			Search_Site(title=addpr('title',''),url=url,page=page,metamethod=addpr('metamethod','')) #(site,section)
	#elif (mode=='SearchLast'): 	Search_Site(title=addst('LastSearchTitle'+SiteTag),url=url,page=page,metamethod=addpr('metamethod',''),endit=tfalse(addpr('endit','true'))) #(site,section)
	elif (mode=='About'): 				eod(); About()
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
