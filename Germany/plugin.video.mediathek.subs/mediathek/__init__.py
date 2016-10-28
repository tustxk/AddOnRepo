# -*- coding: utf-8 -*-
#-------------LicenseHeader--------------
# plugin.video.Mediathek - Gives acces to the most video-platforms from german public service broadcaster
# Copyright (C) 2010  Raptor 2101 [raptor2101@gmx.de]
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>. 
import sys, urllib2,urllib, time, os, re, htmlentitydefs;
import socket
socket.setdefaulttimeout(1);

class SimpleLink(object):
  def __init__(self, basePath, size):
    self.basePath = basePath;
    self.size = size;
    
class ComplexLink(object):
  def __init__(self, basePath, playPath, size):
    self.basePath = basePath;
    self.playPath = playPath;
    self.size = size;

class TreeNode(object):
  def __init__(self,path,name,link,displayElements,childNodes = []):
     self.name = name;
     self.path = path;
     self.link = link;
     self.displayElements = displayElements;
     self.childNodes = childNodes;
     
class DisplayObject(object):
  def __init__(self,title,subTitle,picture,description,link=[],isPlayable = True, date = None, duration = None, subUrl = None):
    self.title = title
    self.subTitle = subTitle
    self.link = link
    self.picture = picture
    self.isPlayable = isPlayable
    self.description = description
    self.date = date;
    self.duration = duration;
    self.subUrl = subUrl;

class Mediathek(object):
  
  def loadPage(self,url, values = None, maxTimeout = None):
    try:
      safe_url = url.replace( " ", "%20" ).replace("&amp;","&")
      
      if(values is not None): 
        data = urllib.urlencode(values)
        req = urllib2.Request(safe_url, data)
      else:
        req = urllib2.Request(safe_url)
      req.add_header('User-Agent', 'Mozilla/5.0')
      req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
      req.add_header('Accept-Language', 'de-de,de;q=0.8,en-us;q=0.5,en;q=0.3')
      req.add_header('Accept-Charset', 'utf-8')
      
      if maxTimeout == None:
        maxTimeout = 60;
      
      waittime = 0;
      doc = False;
      while not doc and waittime < maxTimeout:
        try:
          if waittime > 0: 
            time.sleep(waittime);
          self.gui.log("download %s %d"%(safe_url,waittime));
          sock = urllib2.urlopen( req )
          doc = sock.read();
          sock.close()
        except urllib2.HTTPError, e:
          #handle http error like 404
          print "HTTP error :%s:"%e.code;
          if(e.code == 404): 
              return '';
          if(waittime == 0):
            waittime = 1;
          else:
            waittime *= 2;
        except Exception as e:
          if(waittime == 0):
            waittime = 1;
          else:
            waittime *= 2;
            
      if doc:
        try:
          return doc.encode('utf-8');
        except:
          return doc;
      else:
        return ''
    except:
      return ''
      
  def buildMenu(self, path, treeNode = None):
    if(type(path) in (str,unicode)):
      path = path.split('.');
    if(len(path) > 0):
      index = int(path.pop(0));
    
      if(treeNode == None):
        treeNode = self.menuTree[index];
      else:
        treeNode = treeNode.childNodes[index];
      self.buildMenu(path,treeNode);
    else:
      if(treeNode == None):
        treeNode = self.menuTree[0];
      self.gui.log(treeNode.name);
      for childNode in treeNode.childNodes:
        self.gui.buildMenuLink(childNode,self, len(treeNode.childNodes));
      if(treeNode.displayElements):
        self.buildPageMenu(treeNode.link,len(treeNode.childNodes));
        
  def displayCategories(self):
    if(len(self.menuTree)>1 or not self.menuTree[0].displayElements):
      for treeNode in self.menuTree:
        self.gui.buildMenuLink(treeNode,self,len(self.menuTree)) 
    else:
      self.buildPageMenu(self.menuTree[0].link, 0);
      
     
  def download_subtitles(self, url):
    #from https://code.google.com/p/xbmc-iplayerv2/
    # Download and Convert the TTAF format to srt
    outfile = os.path.join(self.gui.SUBTITLES_DIR, 'mediathek.srt')
    fw = open(outfile, 'w')
    
    txt = self.loadPage(url)
    if txt == '': txt = None;
       
    if not url or txt is None:
        print ("cannot download subtitle")
        fw.write("1\n0:00:00,001 --> 0:01:00,001\nNo subtitles available\n\n".encode('utf-8'))
        fw.close() 
        return outfile
    
           
    else:
        p= re.compile('^\s*<p.*?.*begin=\"(.*?)\.([0-9]+)\"\s+.*?end=\"(.*?)\.([0-9]+)\"[^>]*\s*>(.*?)</p>')
    
        i=0
        prev = None

        # some of the subtitles are a bit rubbish in particular for live tv
        # with lots of needless repeats. The follow code will collapse sequences
        # of repeated subtitles into a single subtitles that covers the total time
        # period. The downside of this is that it would mess up in the rare case
        # where a subtitle actually needs to be repeated 
        for line in txt.split('\n'):
            entry = None
            m = p.match(line)
            if m:
                start_mil = "%s000" % m.group(2) # pad out to ensure 3 digits
                end_mil   = "%s000" % m.group(4)
                
                ma = {'start'     : m.group(1), 
                      'start_mil' : start_mil[:3], 
                      'end'       : m.group(3), 
                      'end_mil'   : end_mil[:3], 
                      'text'      : self.unescape(m.group(5))}
        
                
                
                ma['text'] = ma['text'].replace('&amp;', '&')
                ma['text'] = ma['text'].replace('&gt;', '>')
                ma['text'] = ma['text'].replace('&lt;', '<')
                ma['text'] = ma['text'].replace('<br />', '\n')
                ma['text'] = ma['text'].replace('<br/>', '\n')
                ma['text'] = ma['text'].replace('&apos;', "'")
                
                ma['text'] = re.sub('<.*?>', '', ma['text'])
                ma['text'] = re.sub('&#[0-9]+;', '', ma['text'])
                
                ma=self.tidy(ma);
                if not prev:
                    # first match - do nothing wait till next line
                    prev = ma
                    continue
                
                if prev['text'] == ma['text']:
                    # current line = previous line then start a sequence to be collapsed
                    prev['end'] = ma['end']
                    prev['end_mil'] = ma['end_mil']
                else:
                    i += 1
                    entry = "%d\n%s,%s --> %s,%s\n%s\n\n" % (i, prev['start'], prev['start_mil'], prev['end'], prev['end_mil'], prev['text'])
                    prev = ma
            elif prev:
                i += 1
                entry = "%d\n%s,%s --> %s,%s\n%s\n\n" % (i, prev['start'], prev['start_mil'], prev['end'], prev['end_mil'], prev['text'])
                
            if entry: 
                fw.write(entry)
        
        fw.close()    
        return outfile

  def check_subtitles(self, url):
    try:
      safe_url = url.replace( " ", "%20" ).replace("&amp;","&")
      req = urllib2.Request(safe_url)
      req.get_method = lambda : 'HEAD'
      req.add_header('User-Agent', 'Mozilla/5.0')
      req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
      req.add_header('Accept-Language', 'de-de,de;q=0.8,en-us;q=0.5,en;q=0.3')
      req.add_header('Accept-Charset', 'utf-8')
      res = urllib2.urlopen(req)
      return True
      
    except Exception as e:
      return False
  

  def tidy(self, entry):
    return entry;
  ##
  # Removes HTML or XML character references and entities from a text string.
  # from Fredrik Lundh
  #
  # @param text The HTML (or XML) source text.
  # @return The plain text, as a Unicode string, if necessary.
  #
  def unescape(self,text):
    def fixup(m):
        text = m.group(0)
        if text[:2] == "&#":
            # character reference
            try:
                if text[:3] == "&#x":
                    return unichr(int(text[3:-1], 16)).encode("UTF-8")
                else:
                    return unichr(int(text[2:-1])).encode("UTF-8")
            except ValueError:
                pass
        else:
            # named entity
            try:
                text = unichr(htmlentitydefs.name2codepoint[text[1:-1]]).encode("UTF-8")
            except KeyError:
                pass
        return text # leave as is
    return re.sub("&#?\w+;", fixup, text)
