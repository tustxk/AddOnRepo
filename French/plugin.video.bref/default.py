import xbmcaddon, xbmcgui, xbmcplugin
import sys, os, urllib
from xml.dom.minidom import parse

URL_XML_FEED = 'http://service.canal-plus.com/video/rest/search/cplus/bref'

__settings__ = xbmcaddon.Addon(id='plugin.video.bref')
__language__ = __settings__.getLocalizedString
type_flux = __settings__.getSetting('type_flux')

if __name__ == '__main__' :
	doc = parse(urllib.urlopen(URL_XML_FEED))
	
	for node_video in doc.getElementsByTagName('VIDEO') :
		# verifier que qu'on est dans node VIDEO de BREF
		if node_video.getElementsByTagName('RUBRIQUE')[0].childNodes[0].data == 'BREF' :
			# titre episode
			try :
				name = node_video.getElementsByTagName('TITRE')[0].childNodes[0].data
			except IndexError :
				name = 'Inconnu'
			if name == 'Bref' :
				name = 'Bref. '+node_video.getElementsByTagName('SOUS_TITRE')[0].childNodes[0].data
			try :
				date = node_video.getElementsByTagName('DATE')[0].childNodes[0].data
			except IndexError :
				date = 'Inconnu'
			try :
				urlImg = node_video.getElementsByTagName('PETIT')[0].childNodes[0].data
			except IndexError :
				urlImg = ''
			
			# url
			if type_flux == 30002 : # HD
				try :
					url = node_video.getElementsByTagName('HD')[0].childNodes[0].data
				except IndexError :
					url = ''
					name = name + ' - Flux indisponible en HD.'
			elif type_flux == 30001 : # haut debit
				try :
					url = node_video.getElementsByTagName('HAUT_DEBIT')[0].childNodes[0].data
				except IndexError :
					url = ''
					name = name + ' - Flux indisponible en haut debit.'
			else : # bas debit
				try :
					url = node_video.getElementsByTagName('BAS_DEBIT')[0].childNodes[0].data
				except IndexError :
					url = ''
					name = name + ' - Flux indisponible en bas debit.'
		
			liz=xbmcgui.ListItem(name+' ('+date+')', iconImage=urlImg)
			liz.setInfo(type="Video", infoLabels={"Title": name})
			liz.setProperty('IsPlayable', 'true')
			xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz,totalItems=20)
	
	xbmcplugin.endOfDirectory(handle=int(sys.argv[1]))
