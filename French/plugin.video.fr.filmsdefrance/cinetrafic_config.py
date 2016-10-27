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
			'__plugin__': 					"Cine Trafic"
			,'__authors__': 				"[COLOR white]The[COLOR tan]Highway[/COLOR][/COLOR]"
			,'__credits__': 				""
			,'_domain_url': 				""
			,'UsedLanguages':				['French','English']
			,'mainSite': 						'http://cinetrafic.fr'
			,'mainSite2': 					'http://www.cinetrafic.fr'
			,'colorA': 							"FFFFFFFF"
			,'colorB': 							"FFB7C411"
			#,'MyGenres':						[['Seriale','Seriale','Series'],['Filme-Vechi','Filme Vechi','Old Movies'],['Animatie','Animatie','Animation'],['Aventura','Aventura','Adventure'],['Biografic','Biografic','Biographical'],['Comedie','Comedie','Comedy'],['Dragoste','Dragoste','Love'],['Drama','Drama','Drama'],['Familie','Familie','Family'],['Fantezie','Fantezie','Fantasy'],['Horror','Horror','Horror'],['Istoric','Istoric','Historical'],['Mister','Mister','Mystery'],['Muzica','Muzica','Music'],['Psihologic','Psihologic','Psychological'],['Razboi','Razboi','War'],['Romantic','Romantic','Romance'],['Science-Fiction','Science Fiction','Sci-Fi'],['Sport','Sport','Sports'],['Thriller','Thriller','Thriller'],['Western','Western','Western'],['Filme-Documentare-Online','Filme Documentare Online','Documentary Film Online'],['Film-Noir','Film Noir','Film Noir'],['despre/filme-indiene','Filme Indiene','Indian Movies'],['despre/filme-nominalizate-la-oscar','Filme Nominalizate la Oscar','Nominated for Oscar'],['despre/filme-oscar','Filme Oscar','Oscar Movies'],['despre/nominalizari-globul-de-aur','Nominalizari Globul de Aur','Golden Globe Nominations']]
			#,'MyGenres':						[ ['action','Action','Action'],['animation','Animation','Animation'],['arts-martiaux','Arts Martiaux','Martial Arts'],['aventure','Aventure','Adventure'],['biopic','Biopic','Biopic'],['bollywood','Bollywood','Bollywood'],['comedie','Comedie','Comedy'],['comedie-dramatique','Comedie Dramatique','Comedy Drama'],['comedie-musicale','Comedie Musicale','Comedy Musical'],['crime','Crime','Crime'],['divers','Divers','Misc. Others'],['documentaire','Documentaire','Documentary'],['drame','Drame','Drama'],['epouvante-horreur','Epouvante Horreur','Fright Horror'],['espionnage','Espionnage','Espionnage'],['famille','Famille','Family'],['fantastique','Fantastique','Fantastic'] ,['guerre','Guerre','War'] ,['historique','Historique','Historical'] ,['musical','Musical','Musical'] ,['mystere','Mystere','Mystery'] ,['policier','Policier','Police'] ,['romance-2','Romance','Romance'] ,['science-fiction','Science-Fiction','Sci-Fi'] ,['show','Show','Show'] ,['sport-2','Sport','Sport'] ,['thriller','Thriller','Thriller'] ,['western','Western','Western'] ]
			#,'MyGenres':						[ ['film-comique','Film comique','Comedy Movies'],['film-d-action',"Film d'action","Action Movies"],['film-d-amour',"Film d'amour","Love Movies"],['film-romantique','Film romantique','Romantic Movies'],['film-d-horreur',"Film d'horreur","Horror Movies"],['film-fantastique','Film fantastique','Fantasy Movies'],['film-science-fiction','Film science fiction','Sci-Fi Movies'],['thriller','Thriller','Thriller'],['dessin-anime','Dessin anime','Cartoon'],['film-policier','Film policier','Police Movies'],['film-de-guerre','Film de guerre','War Movies'],['film-gay','Film gay','Gay Movies'],['documentaire','Documentaire','Documentary'],['film-arabe','Film arabe','Arab Movies'],['film-marocain','Film marocain','Moroccan Movies'],['film-francais','Film francais','French Movies'],['serie-tv','Serie tv','TV Series'],['film-2014','Film 2014','Movies in 2014'],['film-2013','Film 2013','Movies in 2013'],['film-2012','Film 2012','Movies in 2012'],['film-2011','Film 2011','Movies in 2011'],['film-2010','Film 2010','Movies in 2010'],['nouveau-film','Nouveau film','New Movies'],['film-recent','Film recent','Recent Movies'],['sortie-cinema','Sortie Cinema','Cinema Releases'],['bande-annonce','Bande Annonce','Trailers'],['dernier-bon-film','Bon film','Good Movies'],['film-a-voir','Film a voir','Films to see'],['video-extrait/extrait-film','Extrait de film','Film Clip'],['top-film','Top film','Top Films'],['super-film','Super film','Super films'],['liste-film','Liste de film','Movie List'] ]
			,'MyGenres':						[ ['nouveau-film','Nouveau film','New Movies'],['film-recent','Film recent','Recent Movies'],['sortie-cinema','Sortie Cinema','Cinema Releases'],['dernier-bon-film','Bon film','Good Movies'],['film-a-voir','Film a voir','Movies to view'],['top-film','Top film','Top Movies'],['super-film','Super film','Super Movies'],['film-comique','Film comique','Comedy Movies'],['film-d-action',"Film d'action","Action Movies"],['film-d-amour',"Film d'amour","Love Movies"],['film-romantique','Film romantique','Romantic Movies'],['film-d-horreur',"Film d'horreur","Horror Movies"],['film-fantastique','Film fantastique','Fantasy Movies'],['film-science-fiction','Film science fiction','Sci-Fi Movies'],['thriller','Thriller','Thriller'],['dessin-anime','Dessin anime','Cartoon'],['film-policier','Film policier','Police Movies'],['film-de-guerre','Film de guerre','War Movies'],['film-gay','Film gay','Gay Movies'],['documentaire','Documentaire','Documentary'],['film-arabe','Film arabe','Arab Movies'],['film-marocain','Film marocain','Moroccan Movies'],['film-francais','Film francais','French Movies'],['serie-tv','Serie tv','TV Series'],['meilleures-series','Meilleures Series','Best TV Series'],['film-2014','Film 2014','Movies in 2014'],['film-2013','Film 2013','Movies in 2013'],['film-2012','Film 2012','Movies in 2012'],['film-2011','Film 2011','Movies in 2011'],['film-2010','Film 2010','Movies in 2010'] ]
			## 
			## ,['bande-annonce','Bande Annonce','Trailers'],['video-extrait/extrait-film','Extrait de film','Film Clip'],['liste-film','Liste de film','Movie List']
			# ,['u','f','e']
			,'MyYears':							['2014','2013','2012','2011','2010','2009','2008','2007','2006','2005','2004','2003','2002','2001','2000','1999','1998','1997','1996','1995','1994','1993','1992','1991','1990','1980','1970']
			,'MyAlphabet':					['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
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
