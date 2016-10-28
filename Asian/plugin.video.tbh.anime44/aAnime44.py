### ############################################################################################################
###	#	
### # Site: 				#		Anime44 - http://www.anime44.com/
### # Author: 			#		The Highway
### # Description: 	#		
###	#	
### ############################################################################################################
### ############################################################################################################
### Imports ###
import xbmc
import os,sys,string,StringIO,logging,random,array,time,datetime,re

from common import *
from common import (_addon,_artIcon,_artFanart,fav__COMMON__list_fetcher)

### ############################################################################################################
### ############################################################################################################
SiteName='[COLOR white]Anime[COLOR red]44[/COLOR][/COLOR]  [v0.1.3]  [Anime]'
SiteTag='anime44.com'
mainSite='http://www.anime44.com/'
iconSite='http://i.imgur.com/AJvEUN4.png' #'http://www.anime44.com/images/site/front/logo.png'
fanartSite='https://fbcdn-sphotos-a-a.akamaihd.net/hphotos-ak-ash3/578135_265333103556365_294501254_n.jpg'
colors={'0':'white','1':'red','2':'blue','3':'green','4':'yellow','5':'orange','6':'lime','7':'','8':'cornflowerblue','9':'blueviolet','10':'hotpink','11':'pink','12':'tan'}

CR='[CR]'
MyAlphabet=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
MyBrowser=['User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3']
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
		m+=CR+'videofun.me | video44.net | novamov.com | yourupload.com' # | play44.net | vidzur.com'
		m+=CR+CR+'Features:  '
		m+=CR+'* Browse Items on Pages'
		m+=CR+'* Browse Url/Name-only Items on Pages'
		m+=CR+'* Browse Episodes - Browse Episodes, Movies and other such Items.'
		m+=CR+'* Browse Hosts.'
		m+=CR+'* Uses urlResolver().'
		m+=CR+'* Play Videos via Handled Hosts.'
		m+=CR+'* Browse Genres and A-Z - Browse Item Pages by A-Z/Others or by Genres (fetched from the site with item count for each genre.'
		m+=CR+'* Search - Just a normal Title Search was available for this site, though it uses a Post-method and their site search seems to have some problems at times.'
		m+=CR+'* Repeat Last Search - Like it says, this shows up once you\'ve done a Search for the first time and allows you to repeat the last search term you used for this Site.  Yes, it\'s setup to save the setting for each site seperately.'
		m+=CR+CR+'Notes:  '
		m+=CR+'* This site doesn\'t seem to have as many methods to browse Movies.  About all there seemed to be was a single long Url/Name-ONLY list.'
		#m+=CR+'* '
		#m+=CR+'* '
		m+=CR+''
		m+=CR+ps('ReferalMsg')
		m+=CR+''
		m+=CR+''
		m+=CR+''
	String2TextBox(message=cFL(m,'cornflowerblue'),HeaderMessage=head)
	#RefreshList()

### ############################################################################################################
### ############################################################################################################

def Search_Site(title='',url='',page='',metamethod='',endit=True):
	if url=='': url=mainSite+'anime/search'
	if len(page) > 0: page='1'
	deb('url',url)
	if (title==''): title=showkeyboard(txtMessage=title,txtHeader="Search:  ("+site+")")
	if (title=='') or (title=='none') or (title==None) or (title==False): return
	deb('Searching for',title)
	title=title.replace('+','%2B').replace('&','%26').replace('?','%3F').replace(':','%3A').replace(',','%2C').replace('/','%2F').replace('=','%3D').replace('@','%40').replace(' ','+')
	#title=title.replace(' ','+')
	if len(page) > 0: npage=str(int(page)+1); #p='&page='+page; 
	else: npage='2'; #p=''; 
	deb('url and page',url+'?key='+title+'&search_submit=Go&page='+page)
	html=nURL(url+'?key='+title+'&search_submit=Go&page='+page,headers={'Referer':mainSite})
	#html=nURL(url,method='get',form_data={'key':title,'search_submit':'Go','page':page},headers={'Referer':mainSite})
	if (len(html)==0): myNote('Search:  '+title,'No page found.'); return
	##if '">Next</a></li>' in html: _addon.add_directory({'mode':'Page','site':site,'section':section,'url':url,'page':npage},{'title':cFL_('  .Next Page > '+npage,colors['2'])},is_folder=True,fanart=fanartSite,img=iconSite)
	addstv('LastSearchTitle'+SiteTag,title) ## Save Setting ##
	Browse_Items(html,metamethod)
	if endit==True: eod()





def Browse_Page(url,page='',metamethod=''):
	if url=='': return
	if len(page) > 0: p='/'+page; npage=str(int(page)+1)
	else: p=''; npage='2'
	deb('url and page',url+p)
	html=nURL(url+p)
	if (len(html)==0): return
	if '">Next</a></li>' in html: _addon.add_directory({'mode':'Page','site':site,'section':section,'url':url,'page':npage},{'title':cFL_('  .Next Page > '+npage,colors['2'])},is_folder=True,fanart=fanartSite,img=iconSite)
	Browse_Items(html,metamethod)
	eod()

def Browse_Items(html,metamethod='',content='tvshows',view='515'):
	if (len(html)==0): return
	s='<a href="(.+?)"><img src="(.+?)" width="120" height="168" alt="Watch (.+?) online"'; html=messupText(html,True,True); matches=re.compile(s).findall(html) #,re.DOTALL
	ItemCount=len(matches)
	if ItemCount > 0:
		#debob(matches)
		for _url,_img,_name in matches:
			labs={}; _NameTag='alt="Watch '+_name+' online"'; SN1S='<span class="small">'; SN1B='<span class="bold">'; SN2='</span>'
			img =''+_img; fimg=''+_img ##img=_artIcon; fimg=_artFanart
			try: 
				labs['plot']=html.split(_NameTag)[1].split('<div class="descr">')[1].split('</div>')[0].strip()
				if ('[<a href' in labs['plot']): labs['plot']=labs['plot'].split('[<a href')[0].strip()
				labs['plot']+='...'
				labs['plot']=cFL(labs['plot'],colors['12'])
			except: labs['plot']=''
			try: labs['year']=html.split(_NameTag)[1].split(SN1S+'Released:'+SN2)[1].split(SN1B)[1].split(SN2)[0].strip()
			except: labs['year']=''
			if len(labs['year']) > 0: labs['plot']+=CR+cFL('Year:  ',colors['11'])+cFL(labs['year'],colors['10'])
			try: labs['type']=html.split(_NameTag)[1].split('<span class="type_indic">')[1].split(SN2)[0].strip()
			except: labs['type']=''
			if len(labs['type']) > 0: labs['plot']+=CR+cFL('Video Type:  ',colors['11'])+cFL(labs['type'],colors['10'])
			try: labs['status']=html.split(_NameTag)[1].split(SN1S+'Status:'+SN2)[1].split(SN1B)[1].split(SN2)[0].strip()
			except: labs['status']=''
			if len(labs['status']) > 0: labs['plot']+=CR+cFL('Status:  ',colors['11'])+cFL(labs['status'],colors['10'])
			try: labs['rating']=html.split(_NameTag)[1].split(SN1S+'Rating:'+SN2)[1].split(SN1B)[1].split(SN2)[0].strip()
			except: labs['rating']=''
			if len(labs['rating']) > 0: labs['plot']+=CR+cFL('Rating:  ',colors['11'])+cFL(labs['rating'],colors['10'])
			if   'movie' in labs['type'].lower(): section='movie'
			elif 'show'  in labs['type'].lower(): section='series'
			else: section='series'
			#
			pars={'mode':'Episodes','site':site,'section':section,'title':_name,'url':_url,'img':img,'fanart':fimg,'year':labs['year']}
			contextLabs={'title':_name,'year':labs['year'],'url':_url,'img':img,'fanart':fimg,'todoparams':_addon.build_plugin_url(pars),'site':site,'section':section,'plot':labs['plot']}
			if   section=='movie':  contextMenuItems=ContextMenu_Movies(contextLabs)
			elif section=='series': contextMenuItems=ContextMenu_Series(contextLabs)
			else: contextMenuItems=[]
			labs['title']=cFL_(_name,'white')
			_addon.add_directory(pars,labs,is_folder=True,fanart=fimg,img=img,contextmenu_items=contextMenuItems,total_items=ItemCount)
	set_view(content,view_mode=addst('tvshows-view')); #set_view(content,int(view)); 
	#eod()

def spAfterSplit(t,ss):
	if ss in t: t=t.split(ss)[1]
	return t
def spBeforeSplit(t,ss):
	if ss in t: t=t.split(ss)[0]
	return t

def Browse_Episodes(url,page='',content='episodes',view='515'):
	if url=='': return
	if page=='': npage='2'; p=''
	else: npage=str(int(page)+1); p='/page/'+page
	deb('url and npage',url+'/page/'+npage)
	deb('url and page',url+p)
	
	html=nURL(url+p); html=messupText(html,True,True)
	if '">Next</a></li>' in html: _addon.add_directory({'mode':'Episodes','site':site,'section':section,'url':url,'page':npage},{'title':cFL_('  .Next Page > '+npage,colors['2'])},is_folder=True,fanart=fanartSite,img=iconSite)
	html=spAfterSplit(html,'<div id="videos_link">'); html=spAfterSplit(html,'<div id="videos">'); html=spBeforeSplit(html,'<ul class="pagination">')
	s='<li>\s*\n*\s*<a href="(.+?)">\s*\n*\s*(.+?)\s*\n*\s*</a>\s*\n*\s*</li>'
	matches=re.compile(s).findall(html)
	ItemCount=len(matches)
	if ItemCount > 0:
		for _url,_name in matches:
			labs={}; labs['plot']=''
			img=''+thumbnail; fimg=''+fanart ##img=_artIcon; fimg=_artFanart
			_title=''+cFL_(_name,'pink')
			#
			contextLabs={'title':_name,'year':'0000','url':_url,'img':img,'fanart':fimg,'DateAdded':''}; contextMenuItems=ContextMenu_Episodes(labs=contextLabs)
			pars={'mode':'Hosts','site':site,'section':section,'title':_name,'url':_url,'img':img,'fanart':fimg}
			labs['title']=_title
			_addon.add_directory(pars,labs,is_folder=True,fanart=fimg,img=img,contextmenu_items=contextMenuItems,total_items=ItemCount)
	set_view(content,int(addst('episode-view'))); eod()

def Browse_List(url,page='',content='tvshows',view='515'):
	if url=='': return
	html=nURL(url); html=messupText(html,True,True)
	html=spAfterSplit(html,'<div id="videos_link">'); html=spAfterSplit(html,'<div id="videos">'); html=spBeforeSplit(html,'<ul class="pagination">')
	s='<li>\s*\n*\s*<a href="(.+?)">\s*\n*\s*(.+?)\s*\n*\s*</a>\s*\n*\s*</li>'
	matches=re.compile(s).findall(html)
	ItemCount=len(matches)
	if ItemCount > 0:
		for _url,_name in matches:
			labs={}; labs['plot']=''
			img=''+thumbnail; fimg=''+fanart ##img=_artIcon; fimg=_artFanart
			_title=''+cFL_(_name,'white')
			#
			if section=='movies': pars={'mode':'Hosts'   ,'site':site,'section':section,'title':_name,'url':_url,'img':img,'fanart':fimg}
			else:                pars={'mode':'Episodes','site':site,'section':section,'title':_name,'url':_url,'img':img,'fanart':fimg}
			contextLabs={'title':_name,'year':'0000','url':_url,'img':img,'fanart':fimg,'DateAdded':'','todoparams':_addon.build_plugin_url(pars),'site':site,'section':section}
			if   section=='movies':  contextMenuItems=ContextMenu_Movies(contextLabs)
			elif section=='series': contextMenuItems=ContextMenu_Series(contextLabs)
			else: contextMenuItems=[]
			labs['title']=_title
			_addon.add_directory(pars,labs,is_folder=True,fanart=fimg,img=img,contextmenu_items=contextMenuItems,total_items=ItemCount)
	set_view(content,int(addst('episode-view'))); eod()


def Browse_Hosts(url,page='',content='list',view='50'):
	if url=='': return
	#if page=='': page='1'
	deb('url',url)
	#npage=str(int(page)+1); deb('url and npage',url+'?page='+npage)
	html=nURL(url); html=messupText(html,True,True)
	if '">Next</a></li>' in html: _addon.add_directory({'mode':'Episodes','site':site,'section':section,'url':url,'page':npage},{'title':cFL_('  .Next Page > '+npage,colors['2'])},is_folder=True,fanart=fanartSite,img=iconSite)
	s='<iframe.*?src="((http://[www|embed]*[\.]*([A-Za-z0-9\.\-_]*))/.+?)"'; matches=re.compile(s).findall(html); ItemCount=len(matches)
	if ItemCount > 0:
		debob(matches)
		for _url,_hostdomain,_hostname in matches:
			if ('/ads/' not in _url) and ('facebook' not in _url):
				img=''+thumbnail; fimg=''+fanart; _title=''+cFL_(_hostname,'blueviolet')
				if checkHostProblems(_url)==True: _title+=cFL_('  *','blueviolet')
				contextLabs={'title':addpr('title',''),'year':'0000','url':_url,'img':img,'fanart':fimg,'hostname':_hostname,'hostdomain':_hostdomain,'destfile':addpr('title','')+'.flv'}; contextMenuItems=ContextMenu_Hosts(labs=contextLabs)
				pars={'mode':'PlayFromHost','site':site,'section':section,'title':addpr('title',''),'hostname':_hostname,'hostdomain':_hostdomain,'url':_url,'img':img,'fanart':fimg}
				labs={'title':_title}
				_addon.add_directory(pars,labs,is_folder=False,fanart=fimg,img=img,contextmenu_items=contextMenuItems,total_items=ItemCount)
	set_view(content,view_mode=addst('links-view'))
	eod()

def Browse_AZ():
	if section=='movies':
		tUrl=mainSite+'alpha-movies/'
		scolor=colors['1']
		_addon.add_directory({'mode':'Page','site':site,'section':section,'url':tUrl+'others'},{'title':cFL_('#',scolor)},is_folder=True,fanart=fanartSite,img=iconSite)
		for az in MyAlphabet:
			_addon.add_directory({'mode':'Page','site':site,'section':section,'url':tUrl+az},{'title':cFL_(az.upper(),scolor)},is_folder=True,fanart=fanartSite,img=iconSite)
	if section=='series':
		tUrl=mainSite+'alpha-anime/'
		scolor=colors['2']
		_addon.add_directory({'mode':'Page','site':site,'section':section,'url':tUrl+'others'},{'title':cFL_('#',scolor)},is_folder=True,fanart=fanartSite,img=iconSite)
		for az in MyAlphabet:
			_addon.add_directory({'mode':'Page','site':site,'section':section,'url':tUrl+az},{'title':cFL_(az.upper(),scolor)},is_folder=True,fanart=fanartSite,img=iconSite)
	set_view('list',view_mode=addst('default-view'))
	eod()


def Browse_Genres(url=''):
	if section=='movies':
		url=mainSite+'anime-movie-genres'
		scolor=colors['1']
	if section=='series':
		url=mainSite+'anime-genres'
		scolor=colors['2']
	if url=='': return
	deb('url',url)
	html=nURL(url)
	html=messupText(html,True,True)
	s='<tr>\s*\n*\s*<td>\s*\n*\s*<a href="(http://[A-Za-z0-9\.]*/\D+-genre/.+?)">(.+?)</a>\s*\n*\s*</td>\s*\n*\s*<td>(\d*)</td>\s*\n*\s*</tr>\s*\n*\s*'
	matches=re.compile(s).findall(html)
	ItemCount=len(matches)
	if ItemCount > 0:
		for _url,_name,_count in matches:
			img=thumbnail
			fimg=fanart
			pars={'mode':'Page','site':site,'section':section,'url':_url}
			_addon.add_directory(pars,{'title':cFL_(_name+'  [COLOR '+scolor+'][[COLOR white]'+_count+'[/COLOR]][/COLOR]',scolor)},is_folder=True,fanart=fimg,img=img,total_items=ItemCount)
	#	
	set_view('list',view_mode=addst('default-view'))
	eod()

def Fav_List(site='',section='',subfav=''):
	debob(['test1',site,section,subfav])
	favs=fav__COMMON__list_fetcher(site=site,section=section,subfav=subfav)
	ItemCount=len(favs)
	debob('test2 - '+str(ItemCount))
	if len(favs)==0: myNote('Favorites','None Found'); eod(); return
	debob(favs)
	for (_name,_year,_img,_fanart,_Country,_Url,_plot,_Genres,_site,_subfav,_section,_ToDoParams,_commonID,_commonID2) in favs:
		if _img > 0: img=_img
		else: img=iconSite
		if _fanart > 0: fimg=_fanart
		else: fimg=fanartSite
		debob('_ToDoParams'); debob(_ToDoParams)
		pars=_addon.parse_query(_ToDoParams)
		debob('pars'); debob(pars)
		_title=cFL_(_name,'white')
		if (len(_year) > 0) and (not _year=='0000'): _title+=cFL('  ('+cFL(_year,'deeppink')+')','pink')
		if len(_Country) > 0: _title+=cFL('  ['+cFL(_Country,'deeppink')+']','pink')
		
		contextLabs={'title':_name,'year':_year,'img':_img,'fanart':_fanart,'country':_Country,'url':_Url,'plot':_plot,'genres':_Genres,'site':_site,'subfav':_subfav,'section':_section,'todoparams':_ToDoParams,'commonid':_commonID,'commonid2':_commonID2}
		##contextLabs={'title':_name,'year':'0000','url':_url,'img':img,'fanart':fimg,'DateAdded':'','todoparams':_addon.build_plugin_url(pars),'site':site,'section':section}
		contextMenuItems=ContextMenu_Favorites(contextLabs)
		#contextMenuItems=[]
		_addon.add_directory(pars,{'title':_title,'plot':_plot},is_folder=True,fanart=fimg,img=img,total_items=ItemCount,contextmenu_items=contextMenuItems)
		#
	#
	if 'movie' in section.lower(): content='movies'
	else: content='tvshows'
	set_view(content,view_mode=int(addst('tvshows-view'))); eod()



### ############################################################################################################
### ############################################################################################################
def SubMenu(): #(site,section=''):
	if section=='movies':
		scolor=colors['1']
		_addon.add_directory({'mode':'List','site':site,'section':section,'url':mainSite+'category/anime-movies'},{'title':cFL_('Anime Movies',colors['1'])},is_folder=True,fanart=fanartSite,img=iconSite)
		### Favorites
		_addon.add_directory({'mode':'FavoritesList','site':site,'section':section},{'title':cFL_(ps('WhatRFavsCalled')+addst('fav.movies.1.name'),ps('cFL_color3'))},fanart=fanartSite,img=iconSite)
		_addon.add_directory({'mode':'FavoritesList','site':site,'section':section,'subfav':'2'},{'title':cFL_(ps('WhatRFavsCalled')+addst('fav.movies.2.name'),ps('cFL_color3'))},fanart=fanartSite,img=iconSite)
		_addon.add_directory({'mode':'FavoritesList','site':site,'section':section,'subfav':'3'},{'title':cFL_(ps('WhatRFavsCalled')+addst('fav.movies.3.name'),ps('cFL_color3'))},fanart=fanartSite,img=iconSite)
		_addon.add_directory({'mode':'FavoritesList','site':site,'section':section,'subfav':'4'},{'title':cFL_(ps('WhatRFavsCalled')+addst('fav.movies.4.name'),ps('cFL_color3'))},fanart=fanartSite,img=iconSite)
		_addon.add_directory({'mode':'FavoritesList','site':site,'section':section,'subfav':'5'},{'title':cFL_(ps('WhatRFavsCalled')+addst('fav.movies.5.name'),ps('cFL_color3'))},fanart=fanartSite,img=iconSite)
		_addon.add_directory({'mode':'FavoritesList','site':site,'section':section,'subfav':'6'},{'title':cFL_(ps('WhatRFavsCalled')+addst('fav.movies.6.name'),ps('cFL_color3'))},fanart=fanartSite,img=iconSite)
		_addon.add_directory({'mode':'FavoritesList','site':site,'section':section,'subfav':'7'},{'title':cFL_(ps('WhatRFavsCalled')+addst('fav.movies.7.name'),ps('cFL_color3'))},fanart=fanartSite,img=iconSite)
		### Advanced Users - used to clean-up Favorites folders.
		#_addon.add_directory({'mode':'cFavoritesEmpty','site':site,'section':section,'subfav':'' },{'title':cFL_('Clear '+ps('WhatRFavsCalled')+addst('fav.movies.1.name'),ps('cFL_color3'))},fanart=fanartSite,img=iconSite)
		#_addon.add_directory({'mode':'cFavoritesEmpty','site':site,'section':section,'subfav':'2'},{'title':cFL_('Clear '+ps('WhatRFavsCalled')+addst('fav.movies.2.name'),ps('cFL_color3'))},fanart=fanartSite,img=iconSite)
		#_addon.add_directory({'mode':'cFavoritesEmpty','site':site,'section':section,'subfav':'3'},{'title':cFL_('Clear '+ps('WhatRFavsCalled')+addst('fav.movies.3.name'),ps('cFL_color3'))},fanart=fanartSite,img=iconSite)
		#_addon.add_directory({'mode':'cFavoritesEmpty','site':site,'section':section,'subfav':'4'},{'title':cFL_('Clear '+ps('WhatRFavsCalled')+addst('fav.movies.4.name'),ps('cFL_color3'))},fanart=fanartSite,img=iconSite)
		#_addon.add_directory({'mode':'cFavoritesEmpty','site':site,'section':section,'subfav':'5'},{'title':cFL_('Clear '+ps('WhatRFavsCalled')+addst('fav.movies.5.name'),ps('cFL_color3'))},fanart=fanartSite,img=iconSite)
		#_addon.add_directory({'mode':'cFavoritesEmpty','site':site,'section':section,'subfav':'6'},{'title':cFL_('Clear '+ps('WhatRFavsCalled')+addst('fav.movies.6.name'),ps('cFL_color3'))},fanart=fanartSite,img=iconSite)
		#_addon.add_directory({'mode':'cFavoritesEmpty','site':site,'section':section,'subfav':'7'},{'title':cFL_('Clear '+ps('WhatRFavsCalled')+addst('fav.movies.7.name'),ps('cFL_color3'))},fanart=fanartSite,img=iconSite)
		
		
		#
		#_addon.add_directory({'mode':'Page','site':site,'section':section,'url':mainSite+'popular-movies'},{'title':cFL_('Popular',scolor)},is_folder=True,fanart=fanartSite,img=iconSite)
		#_addon.add_directory({'mode':'Page','site':site,'section':section,'url':mainSite+'new-movies'},{'title':cFL_('New Series',scolor)},is_folder=True,fanart=fanartSite,img=iconSite)
		#_addon.add_directory({'mode':'Page','site':site,'section':section,'url':mainSite+'recent-movies'},{'title':cFL_('Recent',scolor)},is_folder=True,fanart=fanartSite,img=iconSite)
		#_addon.add_directory({'mode':'AZ','site':site,'section':section},{'title':cFL_('A-Z',scolor)},is_folder=True,fanart=fanartSite,img=iconSite)
		#_addon.add_directory({'mode':'Genres','site':site,'section':section},{'title':cFL_('Genres',scolor)},is_folder=True,fanart=fanartSite,img=iconSite)
	if section=='series':
		scolor=colors['2']
		_addon.add_directory({'mode':'Page','site':site,'section':section,'url':mainSite+'popular-anime'},{'title':cFL_('Popular',scolor)},is_folder=True,fanart=fanartSite,img=iconSite)
		_addon.add_directory({'mode':'Page','site':site,'section':section,'url':mainSite+'new-anime'},{'title':cFL_('New Series',scolor)},is_folder=True,fanart=fanartSite,img=iconSite)
		_addon.add_directory({'mode':'Page','site':site,'section':section,'url':mainSite+'recent-anime'},{'title':cFL_('Recent',scolor)},is_folder=True,fanart=fanartSite,img=iconSite)
		_addon.add_directory({'mode':'Page','site':site,'section':section,'url':mainSite+'ongoing-anime'},{'title':cFL_('Ongoing Series',scolor)},is_folder=True,fanart=fanartSite,img=iconSite)
		_addon.add_directory({'mode':'Page','site':site,'section':section,'url':mainSite+'completed-anime'},{'title':cFL_('Completed',scolor)},is_folder=True,fanart=fanartSite,img=iconSite)
		_addon.add_directory({'mode':'AZ','site':site,'section':section},{'title':cFL_('A-Z',scolor)},is_folder=True,fanart=fanartSite,img=iconSite)
		_addon.add_directory({'mode':'Genres','site':site,'section':section},{'title':cFL_('Genres',scolor)},is_folder=True,fanart=fanartSite,img=iconSite)
		### Favorites
		_addon.add_directory({'mode':'FavoritesList','site':site,'section':section             },{'title':cFL_(ps('WhatRFavsCalled')+addst('fav.tv.1.name'),ps('cFL_color3'))},fanart=fanartSite,img=iconSite)
		_addon.add_directory({'mode':'FavoritesList','site':site,'section':section,'subfav':'2'},{'title':cFL_(ps('WhatRFavsCalled')+addst('fav.tv.2.name'),ps('cFL_color3'))},fanart=fanartSite,img=iconSite)
		_addon.add_directory({'mode':'FavoritesList','site':site,'section':section,'subfav':'3'},{'title':cFL_(ps('WhatRFavsCalled')+addst('fav.tv.3.name'),ps('cFL_color3'))},fanart=fanartSite,img=iconSite)
		_addon.add_directory({'mode':'FavoritesList','site':site,'section':section,'subfav':'4'},{'title':cFL_(ps('WhatRFavsCalled')+addst('fav.tv.4.name'),ps('cFL_color3'))},fanart=fanartSite,img=iconSite)
		_addon.add_directory({'mode':'FavoritesList','site':site,'section':section,'subfav':'5'},{'title':cFL_(ps('WhatRFavsCalled')+addst('fav.tv.5.name'),ps('cFL_color3'))},fanart=fanartSite,img=iconSite)
		_addon.add_directory({'mode':'FavoritesList','site':site,'section':section,'subfav':'6'},{'title':cFL_(ps('WhatRFavsCalled')+addst('fav.tv.6.name'),ps('cFL_color3'))},fanart=fanartSite,img=iconSite)
		_addon.add_directory({'mode':'FavoritesList','site':site,'section':section,'subfav':'7'},{'title':cFL_(ps('WhatRFavsCalled')+addst('fav.tv.7.name'),ps('cFL_color3'))},fanart=fanartSite,img=iconSite)
		### Advanced Users - used to clean-up Favorites folders.
		#_addon.add_directory({'mode':'cFavoritesEmpty','site':site,'section':section,'subfav':'' },{'title':cFL_('Clear '+ps('WhatRFavsCalled')+addst('fav.tv.1.name'),ps('cFL_color3'))},fanart=fanartSite,img=iconSite)
		#_addon.add_directory({'mode':'cFavoritesEmpty','site':site,'section':section,'subfav':'2'},{'title':cFL_('Clear '+ps('WhatRFavsCalled')+addst('fav.tv.2.name'),ps('cFL_color3'))},fanart=fanartSite,img=iconSite)
		#_addon.add_directory({'mode':'cFavoritesEmpty','site':site,'section':section,'subfav':'3'},{'title':cFL_('Clear '+ps('WhatRFavsCalled')+addst('fav.tv.3.name'),ps('cFL_color3'))},fanart=fanartSite,img=iconSite)
		#_addon.add_directory({'mode':'cFavoritesEmpty','site':site,'section':section,'subfav':'4'},{'title':cFL_('Clear '+ps('WhatRFavsCalled')+addst('fav.tv.4.name'),ps('cFL_color3'))},fanart=fanartSite,img=iconSite)
		#_addon.add_directory({'mode':'cFavoritesEmpty','site':site,'section':section,'subfav':'5'},{'title':cFL_('Clear '+ps('WhatRFavsCalled')+addst('fav.tv.5.name'),ps('cFL_color3'))},fanart=fanartSite,img=iconSite)
		#_addon.add_directory({'mode':'cFavoritesEmpty','site':site,'section':section,'subfav':'6'},{'title':cFL_('Clear '+ps('WhatRFavsCalled')+addst('fav.tv.6.name'),ps('cFL_color3'))},fanart=fanartSite,img=iconSite)
		#_addon.add_directory({'mode':'cFavoritesEmpty','site':site,'section':section,'subfav':'7'},{'title':cFL_('Clear '+ps('WhatRFavsCalled')+addst('fav.tv.7.name'),ps('cFL_color3'))},fanart=fanartSite,img=iconSite)
	set_view('list',view_mode=addst('default-view')); eod()
	#

def SectionMenu():
	_addon.add_directory({'mode':'SubMenu','site':site,'section':'movies'},{'title':cFL_('Anime Movies',colors['1'])},is_folder=True,fanart=fanartSite,img=iconSite)
	#_addon.add_directory({'mode':'List','site':site,'section':'movies','url':mainSite+'category/anime-movies'},{'title':cFL_('Anime Movies',colors['1'])},is_folder=True,fanart=fanartSite,img=iconSite)
	_addon.add_directory({'mode':'SubMenu','site':site,'section':'series'},{'title':cFL_('Anime Series',colors['2'])},is_folder=True,fanart=fanartSite,img=iconSite)
	_addon.add_directory({'mode':'Page','site':site,'section':'series','url':mainSite+'ongoing-anime'},{'title':cFL_('Ongoing Series',colors['2'])},is_folder=True,fanart=fanartSite,img=iconSite)
	_addon.add_directory({'mode':'Page','site':site,'section':'series','url':mainSite+'new-anime'},{'title':cFL_('New Series',colors['2'])},is_folder=True,fanart=fanartSite,img=iconSite)
	#_addon.add_directory({'mode':'Episodes','site':site,'section':'series','url':mainSite+'surprise'},{'title':cFL_('Suprise Me',colors['0'])},is_folder=True,fanart=fanartSite,img=iconSite)
	#_addon.add_directory({'mode':'Search','site':site,'section':'series'},{'title':cFL_('Search',colors['0'])},is_folder=True,fanart=fanartSite,img=iconSite)
	
	_addon.add_directory({'mode':'Search','site':site},{'title':cFL_('Search',colors['0'])},is_folder=True,fanart=fanartSite,img=iconSite)
	if (len(addst('LastSearchTitle'+SiteTag)) > 0): _addon.add_directory({'mode':'SearchLast','site':site},{'title':cFL_('Repeat Last Search',colors['0'])},is_folder=True,fanart=fanartSite,img=iconSite)
	_addon.add_directory({'mode':'About','site':site},{'title':cFL_('About',colors['9'])},is_folder=False,fanart=fanartSite,img='http://i.imgur.com/0h78x5V.png') # iconSite
	
	set_view('list',view_mode=addst('default-view')); eod()










### ############################################################################################################
### ############################################################################################################
def mode_subcheck(mode='',site='',section='',url=''):
	deb('mode',mode); 
	if (mode=='SectionMenu'): 		SectionMenu()
	elif (mode=='') or (mode=='main') or (mode=='MainMenu'): SectionMenu()
	elif (mode=='SubMenu'): 			SubMenu()
	elif (mode=='Page'): 					Browse_Page(url=url,page=page,metamethod=addpr('metamethod','')) #(site,section)
	elif (mode=='Episodes'): 			Browse_Episodes(url,page)
	elif (mode=='List'): 					Browse_List(url,page)
	elif (mode=='Hosts'): 				Browse_Hosts(url)
	elif (mode=='AZ'): 						Browse_AZ()
	elif (mode=='Genres'): 				Browse_Genres()
	elif (mode=='PlayFromHost'): 	PlayFromHost(url)
	elif (mode=='Search'): 				Search_Site(title=addpr('title',''),url=url,page=page,metamethod=addpr('metamethod','')) #(site,section)
	elif (mode=='SearchLast'): 		Search_Site(title=addst('LastSearchTitle'+SiteTag),url=url,page=page,metamethod=addpr('metamethod',''),endit=tfalse(addpr('endit','true'))) #(site,section)
	elif (mode=='About'): 				About()
	elif (mode=='FavoritesList'): Fav_List(site=site,section=section,subfav=addpr('subfav',''))
	##
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
	#

mode_subcheck(addpr('mode',''),addpr('site',''),addpr('section',''),addpr('url',''))
### ############################################################################################################
### ############################################################################################################
