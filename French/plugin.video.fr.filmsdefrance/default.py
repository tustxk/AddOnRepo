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
from common import *
from common import (_addon,_artIcon,_artFanart,_addonPath,_debugging)
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
		m+=CR+"Attention: Assurez vous d'avoir l'age requis pour visionner les titres selectioners."
		#m+=CR+CR+'Known Hosts for Videos:  '
		#m+=CR+'* [vk.com]'
		#m+=CR+CR+'Known Hosts for Videos (Not Supported):  '
		#m+=CR+'* [vimple.ru]'
		#m+=CR+CR+'Features:  '
		#m+=CR+'* Browse Movies, Host Links'
		#m+=CR+'* Play Videos with UrlResolver where available'
		#m+=CR+'* Play Videos without UrlResolver where supported'
		#m+=CR+'* MetaData for Shows and Movies where available'
		#m+=CR+'* Favorites, AutoView'
		#m+=CR+'* Core Player Selector'
		##m+=CR+'* Download Videos with UrlResolver'
		#m+=CR+'* '
		m+=CR+CR+'Notes:  '
		#m+=CR+'* Thanks to: ..., Eleazar, and TheHighway.'
		#m+=CR+'* '+ps('ReferalMsg')
		#m+=CR+'* At the time this addon was made, Vimple.ru (host source for some videos) was not supported.  Hopefully a Host Plugin for UrlResolver can be created in time.'
		#m+=CR+'* For now, Videos from the host source VK should play (internally handled as well as through urlresolver), as well as any other sources added to the site that have are handled by host plugins via UrlResolver.'
		m+=CR+'* This add-on handles a collection of many sites that handled French videos.'
		m+=CR+'* Films et emissions de television provenant de diverses sites Web de streaming francais.'
		m+=CR+''
		m+=CR+'* The development of this add-on was sponsored by KewlTV.'
		m+=CR+''
		m+=CR+'* Developpement commanditer par KewlTV.'
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
### ############################################################################################################
### ############################################################################################################
def GetMedia(Url,title,imdb_id,img,fimg,stitle,etitle,enumber,snumber,enumber2,wwT=''):
	if len(snumber)==0: snumber='0'; 
	if len(Url)==0: return
	if (mainSite not in Url) and (mainSite2 not in Url): Url=mainSite+Url; 
	###
	_addon.addon.setSetting(id="LastShowListedURL", value=Url)
	_addon.addon.setSetting(id="LastShowListedNAME", value=title)
	_addon.addon.setSetting(id="LastShowListedIMG", value=img)
	_addon.addon.setSetting(id="LastShowListedFANART", value=fimg)
	_addon.addon.setSetting(id="LastShowListedIMDBID", value=imdb_id)
	_addon.addon.setSetting(id="LastShowListedwwT", value=wwT)
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
#def DoSearch(title='',Url='/?s='):
#	if len(Url)==0: return
#	if mainSite not in Url: Url=mainSite+Url; 
#	if len(title)==0: title=showkeyboard(txtMessage=title,txtHeader="Search:  ("+site+")")
#	if (title=='') or (title=='none') or (title==None) or (title==False): return
#	deb('Searching for',title); title=title.replace('+','%2B').replace('&','%26').replace('?','%3F').replace(':','%3A').replace(',','%2C').replace('/','%2F').replace('=','%3D').replace('@','%40').replace(' ','+'); 
#	deb('Searching for',title); ListShows( Url+( title.replace(' ','+') ) ); 

def SectionMenu():
	##addstv('firstrun','') ## To reset first-run value for testing ##
	#if len(addst('firstrun',''))==0: 
	#	L=popYN(title=ps('__plugin__'),line1='                                     Selection de la langue',line2='                                       Language Selection',line3='',n=UsedLanguages[1],y=UsedLanguages[0]); #deb("L",str(L)); 
	#	if str(L)=='1': addstv('mylanguage1',UsedLanguages[0]); 
	#	else: addstv('mylanguage1',UsedLanguages[1]); 
	#	addstv('firstrun','no'); 
	### ## ### 
	oStar=cFL(' *','orange'); 
	zz=[ 
			['seriesddl','Series DDL']
			,['sokrostream','Sokro Stream']
			,['kstreaming','K Streaming']
			,['streamizfilmze','StreamIZ Filmze']
			,['filmcomplet','Film Complet']
			,['streamcomplet','Stream Complet']
			,['mamzouka','Mamzouka']
			,['videoscourtesclic','Videos Courtes Clic'] #Short Videos Click
			,['cinetrafic','Cine Trafic']
			#,['streamiz','StreamIZ'+oStar]
			##,['streamingp','Streaming P'+oStar]
			##,['delicast','Deli Cast'+oStar]
			#,['','']
			#,['','']
			#,['','']
			#,['','']
			 ]; 
	for nm,nm2 in zz: 
		if isFile(artj(nm+'_fanart'))==True:  nmF=artj(nm+'_fanart')
		else: nmF=''+fanartSite
		_addon.add_directory({'mode':'SectionMenu','site':nm+''},{'title':AFColoring(nm2)},is_folder=True,fanart=nmF,img=artp(nm+'_icon'))
	### ## ### 
	#if (len(addst("LastShowListedURL")) > 0): 
	#	pars={'site':site,'section':section,'mode':'GetMedia','url':addst("LastShowListedURL"),'title':addst("LastShowListedNAME"),'imdb_id':addst("LastShowListedIMDBID"),'img':addst("LastShowListedIMG"),'fimg':addst("LastShowListedFANART"),'wwT':addst("LastShowListedwwT")}; 
	#	title=AFColoring(addst("LastShowListedNAME"))+CR+cFL('[Last Show]',colorA); 
	#	_addon.add_directory(pars,{'title':title},fanart=addst("LastShowListedFANART"),img=addst("LastShowListedIMG"),is_folder=True); 
	##if (len(addst("LastEpisodeListedURL")) > 0): 
	##	pars={'site':site,'section':section,'mode':'GetMedia','url':addst("LastEpisodeListedURL"),'title':addst("LastEpisodeListedNAME"),'imdb_id':addst("LastEpisodeListedIMDBID"),'img':addst("LastEpisodeListedIMG"),'fimg':addst("LastEpisodeListedFANART"),'stitle':addst("LastEpisodeListedSTITLE"),'etitle':addst("LastEpisodeListedETITLE"),'e':addst("LastEpisodeListedEpNo"),'s':addst("LastEpisodeListedSNo"),'e2':addst("LastEpisodeListedEpNo2")}; 
	##	title=AFColoring(addst("LastEpisodeListedNAME"))+CR+cFL('[Last Episode]',colorA); 
	##	_addon.add_directory(pars,{'title':title},fanart=addst("LastEpisodeListedFANART"),img=addst("LastEpisodeListedIMG"),is_folder=True); 
	###
	_addon.add_directory({'mode':'About','site':site,'section':section},{'title':RoAFColoring('A propos','About')},is_folder=True,fanart=fanartSite,img=psgn('about')) #'http://i.imgur.com/0h78x5V.png') # iconSite
	###
	set_view('list',view_mode=addst('default-view')); eod()
### ############################################################################################################
### ############################################################################################################
def mode_subcheck(mode='',site='',section='',url=''):
	deb('mode',mode); 
	if (len(site) > 0): 		
		sFn=site+'_default'; sFilename=xbmc.translatePath(os.path.join(_addonPath,sFn+'.py')); 
		if isFile(sFilename)==True:
			__import__(sFn); 
			return
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
