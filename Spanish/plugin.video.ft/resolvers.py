#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2, re
import urlresolver

def allmyvideos(url):
        url_id = url.replace("http://allmyvideos.net/", "")
        url_embed = "http://allmyvideos.net/embed-" + url_id + ".html"
        req = urllib2.Request(url_embed)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link = response.read()
        response.close()
        url_direc = re.compile('"file" : "(.+?)",\n               "default" : true,\n').findall(link)
        #print url_direc
        return url_direc


def played(url):
        url_id = url.replace("http://played.to/", "")
        url_embed = "http://played.to/embed-" + url_id + "-640x360.html"
        req = urllib2.Request(url_embed)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link = response.read()
        response.close()
        url_direc = re.compile('\n    file: "(.+?)",\n').findall(link)
        #print url_direc
        return url_direc
        

def vidspot(url):
        url_id = url.replace("http://www.vidspot.net/", "")
        url_embed = "http://www.vidspot.net/embed-" + url_id + ".html"
        req = urllib2.Request(url_embed)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link = response.read()
        response.close()
        url_direc = re.compile('"file" : "(.+?)",\n               "default" : true,\n').findall(link)
        #print url_direc
        return url_direc
        

def vodlocker(url):
        url_id = url.replace("http://vodlocker.com/", "")
        url_embed = "http://vodlocker.com/embed-" + url_id + "-640x272.html"
        req = urllib2.Request(url_embed)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link = response.read()
        response.close()
        url_direc = re.compile('\n    file: "(.+?)",\n').findall(link)
        #print url_direc
        return url_direc
    

def get_resolved(url):
        url_direc = urlresolver.resolve(url)
        # print url_direc
        return url_direc


