### ############################################################################################################
###	#	
### # Site: 				#		
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
from streamcomplet_common import *
from streamcomplet_common import (_addon,_artIcon,_artFanart,_addonPath,_debugging)
### ############################################################################################################
### ############################################################################################################
SiteName=ps('__plugin__'); SiteTag=ps('__plugin__').replace(' ',''); mainSite=ps('mainSite'); mainSite2=ps('mainSite2'); 
iconSite=_artIcon #
fanartSite=_artFanart #
colors=ps('colors'); CR='[CR]'; MyAlphabet=ps('MyAlphabet'); MyGenres=ps('MyGenres'); MyYears=ps('MyYears'); 
MyBrowser=['User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3']
ww6='[COLOR black]@[/COLOR]'; ww7='[COLOR FF0098BD]@[/COLOR]'; 
colorA=ps('colorA'); colorB=ps('colorB'); UsedLanguages=ps('UsedLanguages'); 
prox=''; #prox='http://#.#.#.#:#'; 
workingUrl=mainSite+''
### ############################################################################################################
### ############################################################################################################
site=addpr('site',''); section=addpr('section',''); url=addpr('url',''); sections={'series':'series','movies':'movies'}; thumbnail=addpr('img',''); fanart=addpr('fanart',''); page=addpr('page',''); 
if isFile(artj(site+'_fanart'))==True:  fanartSite=artj(site+'_fanart')
if isFile(artp(site+'_icon'))==True: iconSite=artp(site+'_icon')
### ############################################################################################################
### ############################################################################################################
def About(head=''+cFL(SiteName,'blueviolet')+'',m=''):
	m=''
	if len(m)==0:
		m+='IRC Chat:  '+cFL('#XBMCHUB','blueviolet')+' @ '+cFL('irc.Freenode.net','blueviolet')
		m+=CR+'Site Name:  '+SiteName
		#m+=CR+'Site Tag:  '+SiteTag
		#m+=CR+'Site Domain:  '+mainSite+CR+'Site Icon:  '+iconSite+CR+'Site Fanart:  '+fanartSite
		m+=CR+'Age:  Please make sure you are of a valid age to watch the material shown.'
		m+=CR+CR+'Known Hosts for Videos:  '
		m+=CR+'* [vk.com]'
		m+=CR+CR+'Known Hosts for Videos (Not Supported):  '
		m+=CR+'* [vimple.ru]'
		m+=CR+CR+'Features:  '
		m+=CR+'* Browse Movies, Host Links'
		m+=CR+'* Play Videos with UrlResolver where available'
		m+=CR+'* Play Videos without UrlResolver where supported'
		m+=CR+'* MetaData for Shows and Movies where available'
		m+=CR+'* Favorites, AutoView'
		m+=CR+'* Core Player Selector'
		m+=CR+'* Search'
		##m+=CR+'* Download Videos with UrlResolver'
		#m+=CR+'* '
		m+=CR+CR+'Notes:  '
		#m+=CR+'* Thanks to: ..., Eleazar, and TheHighway.'
		#m+=CR+'* '+ps('ReferalMsg')
		m+=CR+'* At the time this addon was made, Vimple.ru (host source for some videos) was not supported.  Hopefully a Host Plugin for UrlResolver can be created in time.'
		m+=CR+'* For now, Videos from the host source VK should play (internally handled as well as through urlresolver), as well as any other sources added to the site that have are handled by host plugins via UrlResolver.'
		m+=CR+''
		m+=CR+''
	try: DoA('Back'); 
	except: pass
	xbmc.sleep(20); 
	try: String2TextBox(message=cFL(m,'cornflowerblue'),HeaderMessage=head)
	except: pass
	#RefreshList()
def spAfterSplit(t,ss):
	if ss in t: t=t.split(ss)[1]
	return t
def spBeforeSplit(t,ss):
	if ss in t: t=t.split(ss)[0]
	return t
def FixImage(img):
	if len(img)==0: return img
	if ('http://' not in img) and ('https://' not in img): img=mainSite+img; 
	return img
def AFColoring(t): 
	if len(t)==0: return t
	elif len(t)==1: return cFL(t,colorA) #colorA)
	else: return cFL(cFL_(t,colorA),colorB) #colorA),colorB)
def RoAFColoring(t,t2): 
	if addst('mylanguage1',UsedLanguages[0]).lower()==UsedLanguages[0].lower(): return AFColoring(t)
	else: return AFColoring(t2)
def wwA(t,ww): #for Watched State Display
	#if   ww==7: t=ww7+t
	#elif ww==6: t=ww6+t
	return t

### ############################################################################################################
### ############################################################################################################

def psgnR(x,t=".png"): ## French
	s="http://i.imgur.com/"; 
	try:
		return {
			'search': 										ROartp('button_search')
			,'all': 											ROartp('button_all')
			,'about': 										ROartp('button_about')
			,'genre': 										ROartp('button_genres')
			,'year': 											ROartp('button_years')
			#,'latest': 										ROartp('button_latest')
			,'favorites': 								ROartp('button_favorites')
			,'favorites 1': 							ROartp('button_favorites')
			,'favorites 2': 							ROartp('button_favorites')
			,'favorites 3': 							ROartp('button_favorites')
			,'favorites 4': 							ROartp('button_favorites')
			,'favorites 5': 							ROartp('button_favorites')
			,'favorites 6': 							ROartp('button_favorites')
			,'favorites 7': 							ROartp('button_favorites')
			,'img_next':									ROartp('button_next')
			,'img_prev':									ROartp('button_prev')
			,'img_last':									ROartp('button_last')
		}[x]
	except: print 'failed to find graphc for %s' % (x); return ''

def psgn(x,t=".png"): ## English
	s="http://i.imgur.com/"; 
	return psgnR(x,t)
	if addst('mylanguage1',UsedLanguages[0]).lower()==UsedLanguages[0].lower(): return psgnR(x,t)
	try:
		return {
			'search': 										artp('button_search')
			,'all': 											artp('button_all')
			,'about': 										artp('button_about')
			,'genre': 										artp('button_genres')
			,'year': 											artp('button_years')
			#,'latest': 										artp('button_latest')
			,'favorites': 								artp('button_favorites')
			,'favorites 1': 							artp('button_favorites')
			,'favorites 2': 							artp('button_favorites')
			,'favorites 3': 							artp('button_favorites')
			,'favorites 4': 							artp('button_favorites')
			,'favorites 5': 							artp('button_favorites')
			,'favorites 6': 							artp('button_favorites')
			,'favorites 7': 							artp('button_favorites')
			,'img_next':									artp('button_next')
			,'img_prev':									artp('button_prev')
			,'img_last':									artp('button_last')
#			,'': 								s+""+t
#			,'': 								s+""+t
#			,'': 								s+""+t
#			,'': 								s+""+t
		}[x]
	except: print 'failed to find graphc for %s' % (x); return ''
if len(site) > 0: iconSite=artp(site+'_icon'); 
### ############################################################################################################
### ############################################################################################################
def PlayFromCHost(Url):
	if len(Url)==0: return
	if (mainSite not in Url) and (mainSite2 not in Url): Url=mainSite+Url; 
	deb('Url',Url); html=messupText(nolines(nURL(Url)),True,True); deb('length of html',str(len(html))); #debob(html); 
	#s='<center>\s*(Partea .*?)</center>\s*<iframe .*?src="(\D+://(.+?)/.+?)"'; 
	#try: results=re.compile(s).findall(html);
	
	
	return
	##

def GetMedia(Url,title,imdb_id,img,fimg,stitle,etitle,enumber,snumber,enumber2,wwT=''):
	if len(snumber)==0: snumber='0'; 
	if len(Url)==0: return
	if (mainSite not in Url) and (mainSite2 not in Url): Url=mainSite+Url; 
	###
	_addon.addon.setSetting(id=site+"_LastShowListedURL", value=Url)
	_addon.addon.setSetting(id=site+"_LastShowListedNAME", value=title)
	_addon.addon.setSetting(id=site+"_LastShowListedIMG", value=img)
	_addon.addon.setSetting(id=site+"_LastShowListedFANART", value=fimg)
	_addon.addon.setSetting(id=site+"_LastShowListedIMDBID", value=imdb_id)
	_addon.addon.setSetting(id=site+"_LastShowListedwwT", value=wwT)
	###
	deb('imdb_id',imdb_id); deb('title',title); deb('Url',Url); html=messupText(nolines(nURL(Url)),True,True); deb('length of html',str(len(html))); #debob(html); 
	if len(html)==0: return
	s='<iframe .*?src="(\D*[\:]*//(.+?)/.+?)".*?>\s*</iframe>'; 
	#s='<iframe .*?src="(*.?//(.+?)/.+?)".*?>\s*</iframe>'; 
	## <p> <iframe width="607" height="360" src="//www.youtube.com/embed/2a_4EKLBs9M" frameborder="0" allowfullscreen></iframe></p>
	## <p><iframe src="http://vk.com/video_ext.php?oid=211766911&#038;id=166762789&#038;hash=314520241af139b7" width="607" height="360" frameborder="0"></iframe></p>
	try: html2p1=re.compile(s).findall(html);
	except: 
		html2p1=''
		try: debob(html); 
		except: pass
	iC=len(html2p1); debob(html2p1); 
	s="<iframe .*?src='(\D*[\:]*//(.+?)/.+?)'.*?>\s*</iframe>"; 
	try: html2p1b=re.compile(s).findall(html);
	except: 
		html2p1b=[]
	for p1b in html2p1b: html2p1.append(p1b)
	if iC > 0:
		aSortMeth(xbmcplugin.SORT_METHOD_TITLE); 
		phtml2p=""; CentA=''; #html2p1=sorted(html2p1); 
		for (url1,domain) in html2p1:
			name=title; domain=domain.replace('www.',''); #url1=url1.replace('&#038;','&'); 
			if phtml2p==url1: next
			else:
					if ' ~~ ' in wwT: wwT+=domain
					else: wwT=title+' ~~ '+domain
					try: URIed=True; import urlresolver; 
					except: URIed=False
					#if 'vk.com' in url1: url1=url1.replace('&',';;').replace(';;','&amp;'); deb('vk.com',url1); 
					if (tfalse(addst('internal-vk.com','false'))==True) and (domain.lower() in ['vk.com','vk.me']):
						#quality=str(addst("quality-vk.com","720")); 
						if (URIed==True) and (urlresolver.HostedMediaFile(url1).valid_url()): 
							cMI=[]; labs={}; pars={'site':site,'mode':'PlayFromHost','url':url1,'title':title,'studio':''+name+' - ['+domain+']'+' [UrlResolver]','img':img,'fimg':fimg,'wwT':wwT,'imdb_id':imdb_id }
							#labs['title']=cFL(''+CentA+''+name+' - '+domain,'blue'); 
							labs['title']=''+name+' - ['+domain+']'+' [UrlResolver]'; 
							#Clabs={'title':title,'year':'','url':m,'destfile':destfile,'img':img,'fanart':fimg,'plot':'','todoparams':_addon.build_plugin_url(pars),'site':site,'section':section}; 
							#cMI=ContextMenu_Hosts(Clabs); 
							try: _addon.add_directory(pars,labs,is_folder=False,contextmenu_items=cMI,total_items=iC,fanart=fimg,img=img)
							except: pass
						if '&amp;' in url1: url1=url1.replace('&amp;','&')
						if '&#038;' in url1: url1=url1.replace('&#038;','&')
						#if '&#038;' in url1: url1=url1.replace('&#038;','&amp;')
						if 'http://' in url1: url1=url1.replace('http://','https://')
						#if 'https://' in url1: url1=url1.replace('https://','http://')
						prox=''; 
						htmlVK=messupText(nolines(nURL(url1,headers={'Referer':Url},proxy=prox)),True,True); deb('length of htmlVK',str(len(htmlVK))); #debob(htmlVK); 
						s='"(\D\D\D+)(\d\d\d+)"\s*:\s*"(\D+:.+?)"'; #deb('s',s); 
						htmlVK=htmlVK.replace('&amp;','&'); 
						htmlVK=htmlVK.replace('\\/','\/').replace('\/','/'); #debob(htmlVK); 
						try: rLink=re.compile(s).findall(htmlVK);
						except: rLink=''
						#if len(rLink) > 0:
						if len(rLink)==0:
							try: debob(htmlVK); 
							except: pass
						else:
							pLink=""; debob(rLink); 
							rLink=sorted(rLink,key=lambda item: (item[1],item[0]),reverse=False)
							rLink=sorted(rLink,key=lambda item: (item[0]),reverse=True)
							for rW,rQ,rL in rLink:
								if (rW in ['url','cache']) and (not pLink==rL):
									quality=rW+' '+rQ; 
									cMI=[]; labs={}; pars={'site':site,'mode':'PlayURL','url':rL,'title':title,'studio':''+name+' - ['+domain+']'+' ['+quality+']','img':img,'fimg':fimg,'wwT':wwT,'imdb_id':imdb_id }
									#labs['title']=cFL(''+CentA+''+name+' - '+domain+' ['+quality+']','green'); 
									labs['title']=''+name+' - ['+domain+']'+' ['+quality+']'; 
									try: _addon.add_directory(pars,labs,is_folder=False,contextmenu_items=cMI,total_items=(iC+len(rLink)),fanart=fimg,img=img)
									except: pass
									pLink=""+rL
					elif (URIed==True) and (urlresolver.HostedMediaFile(url1).valid_url()): 
						cMI=[]; labs={}; pars={'site':site,'mode':'PlayFromHost','url':url1,'title':title,'studio':''+name+' - ['+domain+']','img':img,'fimg':fimg,'wwT':wwT,'imdb_id':imdb_id }
						labs['title']=''+name+' - ['+domain+']'; 
						#Clabs={'title':title,'year':'','url':m,'destfile':destfile,'img':img,'fanart':fimg,'plot':'','todoparams':_addon.build_plugin_url(pars),'site':site,'section':section}; 
						#cMI=ContextMenu_Hosts(Clabs); 
						#try: 
						_addon.add_directory(pars,labs,is_folder=False,contextmenu_items=cMI,total_items=iC,fanart=fimg,img=img)
						#except: pass
					else:
						#cMI=[]; labs={}; pars={'site':site,'mode':'PlayFromCHost','url':url1,'title':title,'studio':CentA+''+name,'img':img,'fimg':fimg,'wwT':title+" ~~ "+name}
						##cMI=[]; labs={}; pars={'site':site,'mode':'PlayURL','url':url1,'title':title,'studio':name,'img':img,'fimg':fimg}
						#labs['title']=cFL(''+CentA+''+name+' - '+domain,'red'); 
						debob('Host domain not currently supported.'); debob([name,url1,domain]); 
						#try: _addon.add_directory(pars,labs,is_folder=False,contextmenu_items=cMI,total_items=iC)
						#except: pass
			phtml2p=""+url1; 
	set_view('list',view_mode=addst('links-view')); eod()

def TagAnimeName(animename):
	#return animename
	try:
		return animename
	except: return animename

def ListShows(Url):
	if len(Url)==0: return
	if (mainSite not in Url) and (mainSite2 not in Url): Url=mainSite+Url; 
	deb('Url',Url); html=messupText(nolines(nURL(Url)),True,True); deb('length of html',str(len(html))); #debob(html); 
	if len(html)==0: return
	s ='<div class="moviefilm">\s*<a href=".+?">\s*'; 
	s+='<img src="(.+?)" alt=".*?" height="\d+px" width="\d+px" /></a>\s*'; 
	s+='<div class="movief"><a href="(.+?)">\s*(.+?)\s*</a></div>\s*'; 
	s+='<div class="movies"><small>\s*(.*?)\s*</small></div>\s*</div'; 
	### img,url,title
	### url,img,name,plot
	try: matches=re.compile(s).findall(html); deb('# of matches found',str(len(matches))); #debob(matches)
	except: matches=''; 
	if len(matches) > 0:
		iC=len(matches); enMeta=tfalse(addst("enableMeta","false")); 
		if '<a class="previouspostslink" href="' in html:
			try: PrEVIOUS= html.split('<a class="previouspostslink" href="')[-1].split('"')[0]; #re.compile("<a href='(.+?)' class='previouspostslink'>").findall(html)[0]; 
			except: PrEVIOUS=Url; 
			deb('previous',PrEVIOUS); _addon.add_directory({'mode':'ListShows','url':PrEVIOUS,'site':site,'section':section},{'title':cFL('<< Precedent','green')+'  '+PrEVIOUS.replace(mainSite,'').replace(mainSite2,'').replace('/category','')},is_folder=True,fanart=fanartSite,img=psgn('img_prev'))
		if enMeta==True:
			try: from metahandler import metahandlers; grab=metahandlers.MetaData(preparezip=False); 
			except: debob("filed to import metahandler"); 
		#for (url,name,img) in matches: #for (url,img,name) in matches:
		for (img,url,name,sitePlot) in matches: #for (url,img,name) in matches:
			name1=''+name; 
			#if 'filme online' in name: TyP='movie'
			#elif 'Serial TV' in name: TyP='tv'
			#else: TyP='movie'
			TyP='movie'
			name=name.replace(') - filme online',')').replace(') Serial TV - ',') - ')
			name2=""+name; 
			if '(' in name2: 
				try: Year=name2.split('(')[1].split(')')[0]
				except: Year=''
				name2=name2.split('(')[0]
			else:
				Year=''
			if ' - ' in name2: name2=name2.split(' - ')[0]
			#img=FixImage(img); 
			cMI=[]; img=img.replace(' ','%20'); fimg=fanartSite; deb('img',img); Genres2=""; g="<a href='http://www.animefate.com/.genre=.+?'>\s*(.+?)\s*</a>"; plot=""; labs={}; 
			genres=""; 
			#try: Genres1=re.compile(g).findall(genres); debob(Genres1); 
			#except: Genres1=""; 
			#for g in Genres1: Genres2+="["+g+"] "; 
			#Genres2=str(Genres1); 
			wwT=name+" ~~ "; 
			#wwT=name2+" ~~ "; 
			try:
				if visited_check(wwT)==True: ww=7
				#if visited_check2(wwT)==True: ww=7
				else: ww=6
			except: ww=6
			#enMeta=False
			if enMeta==True: 
				if 'filme online' in name1:
					#try: labs=grab.get_meta('movie',TagAnimeName(name2),overlay=ww); debob(labs); 
					try: labs=grab.get_meta('movie',TagAnimeName(name2)); debob(labs); 
					except: pass
				else:
					#try: labs=grab.get_meta('tvshow',TagAnimeName(name2),overlay=ww); debob(labs); 
					try: labs=grab.get_meta('tvshow',TagAnimeName(name2)); debob(labs); 
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
			#pars={'site':site,'mode':'ListEpisodes','url':url,'title':name,'imdb_id':labs[u'imdb_id'],'img':img,'fimg':fimg,'site':site,'section':section}; 
			pars={'mode':'GetMedia','url':url,'title':name,'imdb_id':labs[u'imdb_id'],'img':img,'fimg':fimg,'site':site,'section':section,'wwT':wwT}; 
			labs[u'title']=AFColoring(name); 
			try: 
				if not labs[u'plot']: labs[u'plot']=''; 
			except: labs[u'plot']=''; 
			labs[u'plot']=labs['plot'].encode('utf8','strict'); 
			labs[u'plot']=plot+CR+cFL(labs['plot'],'mediumpurple'); 
			#Clabs=labs; 
			#sitePlot=sitePlot.encode('utf8','ignore'); 
			#sitePlot=sitePlot.encode('utf8','xmlcharrefreplace'); 
			#sitePlot=sitePlot.encode('utf8','strict'); 
			#sitePlot=sitePlot.encode('utf8','replace'); 
			
			#zz=[ [0xc3,0x80,'A'],[0xc3,0x81,'A'],[0xc3,0x82,'A'],[0xc3,0x83,'A'],[0xc3,0x84,'A'],[0xc3,0x85,'A'],[0xc3,0x86,'AE'],[0xc3,0x87,'C'],[0xc3,0x88,'E'],[0xc3,0x89,'E'],[0xc3,0x8A,'E'],[0xc3,0x8B,'E'],[0xc3,0xa9,'e'],[0xc3,0xa0,'a'] ]
			#for z,z2,z3 in zz: sitePlot=sitePlot.replace(chr(int(z))+chr(int(z2)),z3); 
			#zz=[0xc3,0xa9,0xaa,0xa7,0xa0,0xa8,0xe2,0x99,0xae,0x80]
			#for z in zz: sitePlot=sitePlot.replace(chr(int(z)),''); 
			
			#sitePlot=sitePlot.encode('utf8','ignore'); 
			#sitePlot=sitePlot.encode('ascii','ignore'); 
			try: labs[u'plot']=''+cFL(str(sitePlot),'grey')+'[CR]'+labs['plot']; 
			except: pass
			labs[u'plot']=messupText(labs['plot'],True,True); 
			labs[u'title']=wwA(messupText(labs[u'title'],True,True),ww); 
			Clabs={'title':name,'year':labs[u'year'],'url':url,'commonid':labs[u'imdb_id'],'img':img,'fanart':fimg,'plot':labs[u'plot'],'todoparams':_addon.build_plugin_url(pars),'site':site,'section':section}; 
			try: cMI=ContextMenu_Series(Clabs,TyP); 
			except: pass
			try: _addon.add_directory(pars,labs,is_folder=True,fanart=fimg,img=img,contextmenu_items=cMI,total_items=iC,context_replace=True)
			except: pass
		if '<a class="nextpostslink" href="' in html:
			try: NeXT=html.split('<a class="nextpostslink" href="')[-1].split('"')[0]; #re.compile("</span><a href='("+mainSite+"/.+?/)' class='nextpostslink'>").findall(html)[0]; 
			except: NeXT=Url; 
			deb('next',NeXT); _addon.add_directory({'mode':'ListShows','url':NeXT,'site':site,'section':section},{'title':cFL('>> Suivant','green')+'  '+NeXT.replace(mainSite,'').replace(mainSite2,'').replace('/category','')},is_folder=True,fanart=fanartSite,img=psgn('img_next'))
		if '<a class="last" href="' in html:
			try: LaST=html.split('<a class="last" href="')[-1].split('"')[0]; #re.compile("<a href='("+mainSite+"/.+?/)' class='last'>Last ").findall(html)[0]; 
			except: LaST=Url; 
			deb('last',LaST); _addon.add_directory({'mode':'ListShows','url':LaST,'site':site,'section':section},{'title':cFL('>> >> Dernier','green')+'  '+LaST.replace(mainSite,'').replace(mainSite2,'').replace('/category','')},is_folder=True,fanart=fanartSite,img=psgn('img_last'))
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
		if (len(_year) > 0) and (not _year=='0000'): _title+=cFL('  ('+cFL(_year,'mediumpurple')+')',colorA)
		if len(_Country) > 0: _title+=cFL('  ['+cFL(_Country,'mediumpurple')+']',colorA)
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
	for aL,azRo,azEn in sorted(MyGenres,key=lambda item: (item[1]),reverse=False): 
		if addst('mylanguage1',UsedLanguages[0]).lower()==UsedLanguages[0].lower(): az=azRo
		else: az=azEn
		i='' #psgn(az.lower())
		if len(i)==0: i=iconSite
		_addon.add_directory({'mode':'ListShows','url':'/film/'+aL.lower().replace(' ','-')+'/','site':site,'section':section},{'title':AFColoring(az)},is_folder=True,fanart=fanartSite,img=i); 
	set_view('list',view_mode=addst('list-view')); eod()

def MenuYear():
	for az in MyYears: 
		i='' #psgn(az.lower())
		if len(i)==0: i=iconSite
		_addon.add_directory({'mode':'ListShows','url':'/despre/filme-'+az.lower().replace(' ','-')+'/','site':site,'section':section},{'title':AFColoring(az)},is_folder=True,fanart=fanartSite,img=i); 
	set_view('list',view_mode=addst('list-view')); eod()
def SectionMenu():
	##addstv('firstrun','') ## To reset first-run value for testing ##
	#if len(addst('firstrun',''))==0: 
	#	L=popYN(title=ps('__plugin__'),line1='                                     Selection de la langue',line2='                                       Language Selection',line3='',n=UsedLanguages[1],y=UsedLanguages[0]); #deb("L",str(L)); 
	#	if str(L)=='1': addstv('mylanguage1',UsedLanguages[0]); 
	#	else: addstv('mylanguage1',UsedLanguages[1]); 
	#	addstv('firstrun','no'); 
	
	#_addon.add_directory({'mode':'GetMedia','site':site,'url':'/transmorphers-fall-of-man/'},{'title':AFColoring('Testing')},is_folder=True,fanart=fanartSite,img=iconSite)
	
	_addon.add_directory({'mode':'ListShows','site':site,'url':'/page/1'},{'title':RoAFColoring('Tous','ALL')},is_folder=True,fanart=fanartSite,img=psgn('all')) #iconSite)
	_addon.add_directory({'mode':'MenuGenre','site':site},{'title':RoAFColoring('Categories','Genres')},is_folder=True,fanart=fanartSite,img=psgn('genre'))
	#_addon.add_directory({'mode':'MenuYear','site':site},{'title':RoAFColoring('Annees','Years')},is_folder=True,fanart=fanartSite,img=psgn('year'))
	_addon.add_directory({'mode':'Search','site':site,'url':'/?s='},{'title':RoAFColoring('Rechercher','Search')},is_folder=True,fanart=fanartSite,img=psgn('search'))
	
	_addon.add_directory({'mode':'FavoritesList','site':site,'section':section             },{'title':cFL(ps('WhatRFavsCalled'),colorA)+cFL('Films - Movies',colorB)},fanart=fanartSite,img=psgn('favorites 1'))
	#_addon.add_directory({'mode':'FavoritesList','site':site,'section':section,'subfav':'2'},{'title':cFL(ps('WhatRFavsCalled'),colorA)+cFL('Seriale - TV Shows',colorB)},fanart=fanartSite,img=psgn('favorites 2'))
	
	#_addon.add_directory({'mode':'FavoritesList','site':site,'section':section             },{'title':cFL(ps('WhatRFavsCalled'),colorA)+cFL(addst('fav.tv.1.name'),colorB)},fanart=fanartSite,img=psgn('favorites 1'))
	#_addon.add_directory({'mode':'FavoritesList','site':site,'section':section,'subfav':'2'},{'title':cFL(ps('WhatRFavsCalled'),colorA)+cFL(addst('fav.tv.2.name'),colorB)},fanart=fanartSite,img=psgn('favorites 2'))
	#_addon.add_directory({'mode':'FavoritesList','site':site,'section':section,'subfav':'3'},{'title':cFL(ps('WhatRFavsCalled'),colorA)+cFL(addst('fav.tv.3.name'),colorB)},fanart=fanartSite,img=psgn('favorites 3'))
	#_addon.add_directory({'mode':'FavoritesList','site':site,'section':section,'subfav':'4'},{'title':cFL(ps('WhatRFavsCalled'),colorA)+cFL(addst('fav.tv.4.name'),colorB)},fanart=fanartSite,img=psgn('favorites 4'))
	#_addon.add_directory({'mode':'FavoritesList','site':site,'section':section,'subfav':'5'},{'title':cFL(ps('WhatRFavsCalled'),colorA)+cFL(addst('fav.tv.5.name'),colorB)},fanart=fanartSite,img=psgn('favorites 5'))
	#_addon.add_directory({'mode':'FavoritesList','site':site,'section':section,'subfav':'6'},{'title':cFL(ps('WhatRFavsCalled'),colorA)+cFL(addst('fav.tv.6.name'),colorB)},fanart=fanartSite,img=psgn('favorites 6'))
	#_addon.add_directory({'mode':'FavoritesList','site':site,'section':section,'subfav':'7'},{'title':cFL(ps('WhatRFavsCalled'),colorA)+cFL(addst('fav.tv.7.name'),colorB)},fanart=fanartSite,img=psgn('favorites 7'))
	###
	if (len(addst(site+"_LastShowListedURL")) > 0): 
		pars={'site':site,'section':section,'mode':'GetMedia','url':addst(site+"_LastShowListedURL"),'title':addst(site+"_LastShowListedNAME"),'imdb_id':addst(site+"_LastShowListedIMDBID"),'img':addst(site+"_LastShowListedIMG"),'fimg':addst(site+"_LastShowListedFANART"),'wwT':addst(site+"_LastShowListedwwT")}; 
		#title=AFColoring(addst(site+"_LastShowListedNAME"))+CR+cFL('[Last Show]',colorA); 
		title=AFColoring(addst(site+"_LastShowListedNAME"))+CR+RoAFColoring('[Dernier]','[Last]').replace(colorB,colorA); #cFL(' [Last Show]',colorA); 
		_addon.add_directory(pars,{'title':title},fanart=addst(site+"_LastShowListedFANART"),img=addst(site+"_LastShowListedIMG"),is_folder=True); 
	#if (len(addst("LastEpisodeListedURL")) > 0): 
	#	pars={'site':site,'section':section,'mode':'GetMedia','url':addst("LastEpisodeListedURL"),'title':addst("LastEpisodeListedNAME"),'imdb_id':addst("LastEpisodeListedIMDBID"),'img':addst("LastEpisodeListedIMG"),'fimg':addst("LastEpisodeListedFANART"),'stitle':addst("LastEpisodeListedSTITLE"),'etitle':addst("LastEpisodeListedETITLE"),'e':addst("LastEpisodeListedEpNo"),'s':addst("LastEpisodeListedSNo"),'e2':addst("LastEpisodeListedEpNo2")}; 
	#	title=AFColoring(addst("LastEpisodeListedNAME"))+CR+cFL('[Last Episode]',colorA); 
	#	_addon.add_directory(pars,{'title':title},fanart=addst("LastEpisodeListedFANART"),img=addst("LastEpisodeListedIMG"),is_folder=True); 
	###
	_addon.add_directory({'mode':'About','site':site,'section':section},{'title':RoAFColoring('A propos','About')},is_folder=True,fanart=fanartSite,img=psgn('about')) #'http://i.imgur.com/0h78x5V.png') # iconSite
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
	elif (mode=='GetMedia'): 			GetMedia(url,addpr('title',''),addpr('imdb_id',''),addpr('img',''),addpr('fimg',''),addpr('stitle',''),addpr('etitle',''),addpr('e',''),addpr('s',''),addpr('e2',''),addpr('wwT',''))
	elif (mode=='Search'):				DoSearch(addpr('title',''),url)
	#elif (mode=='Hosts'): 				Browse_Hosts(url)
	#elif (mode=='Search'): 			Search_Site(title=addpr('title',''),url=url,page=page,metamethod=addpr('metamethod','')) #(site,section)
	#elif (mode=='SearchLast'): 	Search_Site(title=addst('LastSearchTitle'+SiteTag),url=url,page=page,metamethod=addpr('metamethod',''),endit=tfalse(addpr('endit','true'))) #(site,section)
	elif (mode=='About'): 				eod(); About()
	#elif (mode=='FavoritesList'): Fav_List(site=site,section=section,subfav=addpr('subfav',''))
	elif (mode=='MenuAZ'): 				MenuAZ(url)
	elif (mode=='MenuGenre'): 		MenuGenre()
	elif (mode=='MenuYear'): 		MenuYear()
	elif (mode=='FavoritesList'): Fav_List(site=site,section=section,subfav=addpr('subfav',''))
	elif (mode=='PlayFromCHost'): 			PlayFromCHost(url)
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
