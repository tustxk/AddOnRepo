### ############################################################################################################
###	#	
### # Author: 			#		The Highway
### # Description: 	#		Config File
###	#	
### ############################################################################################################
### ############################################################################################################
### Imports ###
import xbmc,xbmcplugin,xbmcgui,xbmcaddon,xbmcvfs
import os,sys,string,StringIO,logging,random,array,time,datetime,re
#from t0mm0.common.addon import Addon
#try: 		from t0mm0.common.addon 				import Addon
#except: 
#	try: from c_t0mm0_common_addon 				import Addon
#	except: pass
try: 			from addon.common.addon 				import Addon
except:
	try: 		from t0mm0.common.addon 				import Addon
	except: 
		try: from c_t0mm0_common_addon 				import Addon
		except: pass
### Plugin Settings ###
def ps(x):
	if (x=='_addon_id') or (x=='addon_id') or (x=='_plugin_id') or (x=='plugin_id'): return 'plugin.video.fr.filmsdefrance'
	try: 
		return {
			'__plugin__': 					"Mamzouka"
			,'__authors__': 				"[COLOR white]The[COLOR tan]Highway[/COLOR][/COLOR]"
			,'__credits__': 				""
			,'_domain_url': 				""
			,'UsedLanguages':				['French','English']
			,'mainSite': 						'http://mamzouka.com'
			,'mainSite2': 					'http://www.mamzouka.com'
			,'colorA': 							"FFFFFFFF"
			,'colorB': 							"FFB7C411"
			#,'MyGenres':						[['Seriale','Seriale','Series'],['Filme-Vechi','Filme Vechi','Old Movies'],['Animatie','Animatie','Animation'],['Aventura','Aventura','Adventure'],['Biografic','Biografic','Biographical'],['Comedie','Comedie','Comedy'],['Dragoste','Dragoste','Love'],['Drama','Drama','Drama'],['Familie','Familie','Family'],['Fantezie','Fantezie','Fantasy'],['Horror','Horror','Horror'],['Istoric','Istoric','Historical'],['Mister','Mister','Mystery'],['Muzica','Muzica','Music'],['Psihologic','Psihologic','Psychological'],['Razboi','Razboi','War'],['Romantic','Romantic','Romance'],['Science-Fiction','Science Fiction','Sci-Fi'],['Sport','Sport','Sports'],['Thriller','Thriller','Thriller'],['Western','Western','Western'],['Filme-Documentare-Online','Filme Documentare Online','Documentary Film Online'],['Film-Noir','Film Noir','Film Noir'],['despre/filme-indiene','Filme Indiene','Indian Movies'],['despre/filme-nominalizate-la-oscar','Filme Nominalizate la Oscar','Nominated for Oscar'],['despre/filme-oscar','Filme Oscar','Oscar Movies'],['despre/nominalizari-globul-de-aur','Nominalizari Globul de Aur','Golden Globe Nominations']]
			,'MyGenres':						[ 
				#['2014','Annees: 2014','Year: 2014'],['2013','Annees: 2013','Year: 2013'],['2012','Annees: 2012','Year: 2012'] #,['annees/2011','Annees: 2011','Year: 2011'],['annees/2010','Annees: 2010','Year: 2010']
				#,['langues/french','Langue: French','Language: French'],['langues/vostfr','Langue: VOSTFR','Language: VOSTFR']
				#,['qualites/bdrip','Qualite: BDRip','Quality: BDRip'],['qualites/brrip','Qualite: BRRip','Quality: BRRip'],['qualites/camrip','Qualite: DVDRip','Quality: DVDRip'],['qualites/dvdrip','Qualite: DVDRip','Quality: DVDRip'],['qualites/dvdscr','Qualite: DVDSCR','Quality: DVDSCR'],['qualites/hdcam','Qualite: HDCam','Quality: HDCam'],['qualites/hdrip','Qualite: HDRip','Quality: HDRip'],['qualites/hdtv','Qualite: HDTV','Quality: HDTV'],['qualites/pdtv','Qualite: PDTV','Quality: PDTV'],['qualites/r5','Qualite: R5','Quality: R5'],['qualites/ts','Qualite: TS','Quality: TS'],['qualites/tvrip','Qualite: TVRip','Quality: TVRip'],['qualites/webrip','Qualite: WEBRiP','Quality: WEBRiP']
				#,
				['hd','HD Films','HD Movies']
				,['top-films','Top Films','Top Movies']
				,['action-film','Action','Action']
				,['animation-manga','Animation','Animation']
				,['aventure','Aventure','Adventure']
				,['arts-martiaux','Arts Martiaux','Martial Arts']
				#,['biographie','Biographie','Biography']
				,['biopic','Biopic','Biopic']
				#,['catastrophe','Catastrophe','Disaster']
				,['comedie','Comedie','Comedy']
				#,['comedie-dramatique','Comedie Dramatique','Comedy Drama']
				#,['comedie-musicale','Comedie musicale','Music Comedy']
				,['crime','Crime','Crime']
				,['divers','Divers','Misc. Others']
				,['documentaire','Documentaire','Documentary']
				,['drame','Drame','Drama']
				#,['drame-psychologique','Drame Psychologique','Psychological Drama']
				#,['emotion','Emotion','Emotional']
				#,['epouvante-horreur','Epouvante Horreur','Fright Horror']
				#,['erotique','Erotique','Erotic']
				,['espionnage','Espionnage','Espionage']
				,['famille','Famille','Family']
				,['fantastique','Fantastique','Fantasy']
				#,['film-noir','Film Noir','Film Noir']
				,['guerre','Guerre','War']
				#,['historie','Historie','History']
				,['historique','Historique','Historical']
				,['horreur','Horreur','Horror']
				#,['judiciaire','Judiciaire','Judicial']
				#,['medical','Medical','Medical']
				,['musical','Musical','Musical']
				#,['mystere','Mystere','Mystery']
				,['peplum','Peplum','Peplum']
				,['policier','Policier','Police']
				#,['politique','Politique','Policy']
				,['romance','Romance','Romance']
				,['science-fiction','Science-Fiction','Sci-Fi']
				#,['serie','Serie','Series']
				#,['spectacles','Spectacles','Shows']
				#,['sport','Sport','Sport']
				,['thriller','Thriller','Thriller']
				,['western','Western','Western']
				#
				,['americain','Americain','American']
				,['francais','Francais','French']
				,['canadien','Canadien','Canadian']
				,['belge','Belge','Belgian']
				,['allemand','Allemand','German']
				,['espagnole','Espagnole','Spanish']
				,['suisse','Suisse','Switzerland']
				,['italien','Italien','Italian']
				,['chinois','Chinois','Chinese']
				 ]
			# ,['u','f','e']
			,'MyYears':							['2014','2013','2012','2011','2010','2009','2008','2007','2006'] #,'2005','2004','2003','2002','2001','2000','1999','1998','1997','1996','1995','1994','1993','1992','1991','1990','1980','1970']
			,'MyAlphabet':					['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','0','1','2','3','4','5','6','7','8','9']
			,'colors':							{'0':'white','1':'red','2':'blue','3':'green','4':'yellow','5':'orange','6':'lime','7':'','8':'cornflowerblue','9':'blueviolet','10':'hotpink','11':'pink','12':'tan','13':'firebrick','14':'mediumpurple'}
			,'word': 								""
			,'word0': 							""
			,'word1': 							""
			,'word2': 							""
			,'word3': 							""
			,'word4': 							""
			,'word5': 							""
			,'word6': 							""
			,'word7': 							""
			,'word8': 							""
			,'word9': 							""
			,'content_movies': 			"movies"
			,'content_tvshows': 		"tvshows"
			,'content_seasons': 		"seasons"
			,'content_episodes': 		"episodes"
			,'content_links': 			"list"
			,'default_section': 					'anime'
			,'section.wallpaper':					'wallpapers'
			,'section.tv': 								'tv'
			,'section.movies': 						'movies'
			,'section.anime': 						'anime'
			,'section.animesub': 					''
			,'section.animedub': 					''
			,'section.animesubmovies': 		''
			,'section.animesubseries': 		''
			,'section.animedubmovies': 		''
			,'section.animedubseries': 		''
			,'section.anime': 						''
			,'sep': 								os.sep
			,'special.home': 				'special:'+os.sep+os.sep+'home'
			,'special.home.addons': 'special:'+os.sep+os.sep+'home'+os.sep+'addons'+os.sep
			,'_addon_path_art': 		"art_test"
			,'_database_name': 			"notused"
			,'default_art_ext': 		'.png'
			,'default_cFL_color': 	'cornflowerblue'
			,'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
			,'cMI.showinfo.url': 							'XBMC.Action(Info)'
			,'cMI.jDownloader.addlink.url':		'XBMC.RunPlugin(plugin://plugin.program.jdownloader/?action=addlink&url=%s)'
			,'filemarker': ''
			#,'': ''
			,'ReferalMsg': 'My XBMC-HUB Refferal Code - http://www.xbmchub.com/forums/register.php?referrerid=15468  [CR]Please use it to register if you don\'t have an account.  It not\'s not much but it can help me out.  '
			,'WhatRFavsCalled': 'Favoris: '
		}[x]
	except: return ''







### ############################################################################################################
### ############################################################################################################
