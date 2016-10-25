import sys
import sha
import zlib
import math as Math
from utils.Common import Common
from binascii import hexlify, unhexlify
from crypto.cipher.aes_cbc import AES_CBC
from utils.Base64Decoder import Base64Decoder
from crypto.cipher.base import noPadding, padWithPadLen
from utils.BeautifulSoup import BeautifulSoup, BeautifulSoup

__settings__ = sys.modules[ "__main__" ].__settings__

class crunchyDec:
	def __init__(self):
		pass
		
	def returnSubs(self, xml):
		useSRT = __settings__.getSetting("useSRTSubs") == "true"
		useSRT = bool(useSRT)
		print useSRT
		_id, _iv, _data = self.strainSoup(xml)
		print "CRUNCHYROLL: --> Attempting to decrypt subtitles..."
		decryptedSubs = self.decodeSubtitles(_id, _iv, _data)
		formattedSubs = self.convertToASS(decryptedSubs)
		if(useSRT):
			print "CRUNCHYROLL: --> Converting to SRT..."
			formattedSubs = self.convertToSRT(formattedSubs.split('\n'))
		print "CRUNCHYROLL: --> Success!  Subtitles decrypted."
		return formattedSubs, useSRT
		
	def strainSoup(self, xml):
		soup = BeautifulSoup(xml)
		subtitle = soup.find('subtitle', attrs={'link': None})
		if subtitle:
			_id = int(subtitle['id'])
			_iv = subtitle.find('iv').contents[0]
			_data = subtitle.data.string
			return _id, _iv, _data
		else:
			print "CRUNCHYROLL: --> Couldn't parse XML file."
			
	def convertToASS(self, script):
		soup = BeautifulSoup(script, convertEntities=BeautifulSoup.HTML_ENTITIES)
		header = soup.find('subtitle_script')
		header = "[Script Info]\nTitle: "+header['title']+"\nScriptType: v4.00+\nWrapStyle: "+header['wrap_style']+"\nPlayResX: 624\nPlayResY: 366\n\n";
		styles = "[V4 Styles]\nFormat: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n";
		events = "[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n";
		stylelist = soup.findAll('style')
		eventlist = soup.findAll('event')
		
		for style in stylelist:
			styles += "Style: " + style['name'] + ", " + style['font_name'] + ", " + style['font_size'] + ", " + style['primary_colour'] + ", " + style['secondary_colour'] + ", " + style['outline_colour'] + ", " + style['back_colour'] + ", " + style['bold'] + ", " + style['italic'] + ", " + style['underline'] + ", " + style['strikeout'] + ", " + style['scale_x'] + ", " + style['scale_y'] + ", " + style['spacing'] + ", " + style['angle'] + ", " + style['border_style'] + ", " + style['outline'] + ", " + style['shadow'] + ", " + style['alignment'] + ", " + style['margin_l'] + ", " + style['margin_r'] + ", " + style['margin_v'] + ", " + style['encoding'] + "\n"
		
		for event in eventlist:
			events += "Dialogue: 0,"+event['start']+","+event['end']+","+event['style']+","+event['name']+","+event['margin_l']+","+event['margin_r']+","+event['margin_v']+","+event['effect']+","+event['text']+"\n"
	
		formattedSubs = header+styles+events
		return formattedSubs
		
	def convertToSRT(self, script):
		offset = script.index('[Events]')
		events = []
		for i in range(offset, len(script)):
			line = script[i]
			try:
				fields = line.split(': ', 1)
				lineType = fields[0]
				payload = fields[1].split(',', 9)
				if lineType != 'Dialogue':
				    continue
				startTime = payload[1]
				endTime = payload[2]
				text = payload[-1]
				startTime = self.convert_timecode(startTime)
				endTime = self.convert_timecode(endTime)
				text = self.parse_override_tags(text)
			except:
				continue
			events.append((startTime, endTime, text))
		index = 1
		srtOutput = ''
		print events
		for i in events:
			srtOutput += str(index) + '\n'
			srtOutput += i[0] + ' --> ' + i[1] + '\n'
			srtOutput += i[2] + '\n\n'
			index += 1
		return srtOutput

	def convert_timecode(self, time):
		fields = time.split(':')
		hh = '0' + fields[0]
		mm = fields[1]
		ss = fields[2].replace('.', ',') + '0'
		return ':'.join([hh, mm, ss])

	def parse_override_tags(self, text):
		equivs = {'i1':'<i>', 'i0':'</i>', 'b1':'<b>', 'b0':'</b>', 'u1':'<u>', 'u0':'</u>', 's1':'<s>', 's0':'</s>'}
		parsed = []
		currentTag = []
		tagIsOpen = False
		for i in text:
			if not tagIsOpen:
				if i != '{':
				    parsed.append(i)
				else:
				    tagIsOpen = True
			else:
				if i != '}':
				    currentTag.append(i)
				else:
					tagIsOpen = False
					override = ''.join(currentTag)
					tags = override.split('\\')
					for j in tags:
						if j in equivs:
							parsed.append(equivs[j])
					currentTag = []
					fields = []
		line = ''.join(parsed)
		line = line.replace('\\N', '\n').replace('\\n', '\n').replace('\\h', ' ')
		return line

		
	# ---- CRYPTO -----

	def generateKey(self, mediaid, size = 32):
		# Below: Do some black magic
		eq1 = int(int(Math.floor(Math.sqrt(6.9) * Math.pow(2, 25))) ^ mediaid)
		eq2 = int(Math.floor(Math.sqrt(6.9) * Math.pow(2, 25)))
		eq3 = (mediaid ^ eq2) ^ (mediaid ^ eq2) >> 3 ^ eq1 * 32
		# Below: Creates a 160-bit SHA1 hash 
		shaHash = sha.new(self.createString([20, 97, 1, 2]) + str(eq3)) 
		finalHash = shaHash.digest()
		hashArray = Common().createByteArray(finalHash)
		# Below: Pads the 160-bit hash to 256-bit using zeroes, incase a 256-bit key is requested
		padding = [0]*4*3
		hashArray.extend(padding)
		keyArray = [0]*size
		# Below: Create a string of the requested key size
		for i, item in enumerate(hashArray[:size]):
			keyArray[i] = item
		return Common().ByteArrayToString(keyArray)
	
	def createString(self, args):
		i = 0
		argArray = [args[2], args[3]]
		while(i < args[0]):
			argArray.append(argArray[-1] + argArray[-2])
			i = i + 1
		finalString = ""
		for arg in argArray[2:]:
			finalString += chr(arg % args[1] + 33)
		return finalString

	def decodeSubtitles(self, id, iv, data):
		compressed = True
		key = self.generateKey(id)
		iv = Common().ByteArrayToString(Base64Decoder().decode(iv))
		data = Common().ByteArrayToString(Base64Decoder().decode(data))
		data = iv+data
		cipher = AES_CBC(key, padding=noPadding(), keySize=32)
		decryptedData = cipher.decrypt(data)
		if compressed:
			return zlib.decompress(decryptedData)
		else:
			return decryptedData