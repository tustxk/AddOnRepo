#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Released under GPLv3

""" Parse playlist.m3u from freebox """

import re
import urllib, urllib2

PLAYLISTURL="http://mafreebox.freebox.fr/freeboxtv/playlist.m3u"

def getUrl(url):
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    return link

class Service:
	def __init__(self, serviceid):
		self.id = serviceid
		self.audiotracks = list()

	def add(self, audiotrackid):
		self.audiotracks.append(audiotrackid)

	def __settle(self):
		self.audiotracks.sort()
		self.relativetracks = dict()
		index = 1
		for id in self.audiotracks:
			self.relativetracks[id] = index
			index += 1

	def get_relative_audio_track(self, audiotrackid):
		self.__settle()
		return self.relativetracks[audiotrackid]
	

class ServiceList:
	def __init__(self):
		self.services = dict()

	def add(self, serviceid, audiotrackid):
		if serviceid not in self.services:
			self.services[serviceid] = Service(serviceid)
		self.services[serviceid].add(audiotrackid)

	def get(self, serviceid):
		if serviceid in self.services:
			return self.services[serviceid]
		else:
			return None

	def get_relative_audio_track(self, serviceid, audiotrackid):
		service = self.get(serviceid)
		if service != None:
			return service.get_relative_audio_track(audiotrackid)
		else:
			return None

class ChannelFlavour:

	def __init__(self, spec, service_list):
		self.spec = spec
		self.id = spec['id']
		self.name = spec['name']
		self.url = spec['url']
		self.audiotrack = spec['audiotrack']
		self.flavour = spec['flavour']
		self.service = spec['service']
		self.service_list = service_list
		service_list.add(self.service, self.audiotrack)

	def get_relative_audio_track(self):
		sl = self.service_list
		s = self.service
		a = self.audiotrack
		return sl.get_relative_audio_track(s, a)

	def __str__(self):
		return '(%i ,%s)<%s,"%s">, <%s, %s>' % (self.id, self.flavour, self.service, self.name, self.url, self.audiotrack)


class Channel:	

	def __init__(self, id, service_list):
		self.id = id
		self.flavours = dict()
		self.service_list = service_list

	def add_flavour(self, flavourspec):
		assert(self.id == int(flavourspec['id']))
		self.flavours[flavourspec['flavour']] = ChannelFlavour(flavourspec, self.service_list)

	def is_radio(self):
		return 'radio' in self.flavours

	def is_tv(self):
		return 'radio' not in self.flavours

	def get_flavour(self, flavour):
		if self.has_flavour(flavour):
			return self.flavours[flavour]
		else:
			return None

	def has_flavour(self, flavour):
		return flavour in self.flavours

	def __str__(self):
		s = "Channel(%s\n" % self.id
		for flavour in self.flavours:
			s += "  %s\n" % self.flavours[flavour]
		s += ")"
		return s


class ChannelList:

	def __init__(self):
		self.list = dict()
		self.service_list = ServiceList()

	def get(self, id):
		if id not in self.list :
			self.list[id] = Channel(id, self.service_list)
		return self.list[id]

	def all(self, flavour='sd'):
		result = []
		for id in self.list:
			f = self.list[id].get_flavour(flavour)			
			if f != None:
				result.append(f)
		return result

	def __str__(self):
		s = "ChannelList(\n"
		for k in self.list:
			s += "%s\n" % self.list[k]
		s += ")"
		return s


class ChannelListReader:
		
	def __init__(self):
		pass

	def get_instance(self):
		instance  = ChannelList()
		playlist_content = getUrl(PLAYLISTURL)
		globalregex = re.compile(r'#EXTINF:\d+,(?P<id>\d+) - (?P<name>.*)\n(?:#EXTVLCOPT:(audio-track-id=(?P<audiotrack>\d+)|.*)\n)*(?P<url>rtsp://.*)\n', re.MULTILINE)
		flavourregex = re.compile(r'flavour=(\w+)')
		serviceregex = re.compile(r'service=(\w+)')
		for match in globalregex.finditer(playlist_content):
			channelflavour = match.groupdict()
			mo = flavourregex.search(channelflavour['url'])
			if mo == None:
				flavour = 'radio'
			else:
				flavour = mo.group(1)
			mo = serviceregex.search(channelflavour['url'])
			if mo == None:
				service = None
			else:
				service = mo.group(1)

			channelflavour['flavour'] = flavour
			channelflavour['id'] = int(channelflavour['id'])
			channelflavour['service'] = service
		
			channel = instance.get(channelflavour['id'])
			channel.add_flavour(channelflavour)
		return instance

if __name__ == "__main__":
	cl  = ChannelListReader().get_instance()
	# print cl

	def cfs(a,b):
		return cmp(a.name, b.name)

	z = cl.all(flavour='radio')
	z.sort(cfs)
	for cf in z:	
		print "%s %s " % (cf.get_relative_audio_track(), cf)

	zz = "%(a)s - %(b)s"
	print zz % { "a":"a", "b":"b" }


