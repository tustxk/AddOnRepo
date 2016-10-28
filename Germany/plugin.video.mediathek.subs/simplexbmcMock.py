# -*- coding: utf-8 -*-
#-------------LicenseHeader--------------
# plugin.video.mediathek - display german mediathekes
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
import sys, urllib, os, time, re 
from xml.dom import minidom

regex_findLink = re.compile("mms://[^\"]*wmv");

__plugin__ = "Mediathek"
__plugin_handle__ = 0

translation = "en";

class SimpleXbmcGui(object):
  def __init__(self):
    self.settings = None
    self.quality = 3
    self.preferedStreamTyp = 30021;
    
    self.enableSubs = True;
    self.SUBTITLES_DIR  = "/tmp/"
    
  def log(self, msg):
    if type(msg) not in (str, unicode):
      print("[%s]: %s" % (__plugin__, type(msg)))
    else:
      print("[%s]: %s" % (__plugin__, msg.encode('utf8')))
      
  def buildVideoLink(self, displayObject, mediathek, objectCount):
      print "buildVideoLink %s"%(displayObject.subUrl)
   
  def buildMenuLink(self,menuObject,mediathek,objectCount):
      print "buildMenuLink"

  def listAvaibleMediathekes(self, mediathekNames):
      print "listAvaibleMediathekes"
  
  def openMenuContext(self):
      print "openMenuContext"
  
  def closeMenuContext(self):
      print "closeMenuContext"
  
  def getHomeDir(self):
      print "getHomeDir"
  
  def back(self):
      print "back"
    
  def keyboardInput(self):
      print "keyboardInput"
    
  def addSearchButton(self,mediathek):
      print "addSearchButton"
  
  def readText(self,node,textNode):
      print "readText"
      
  def playPlaylist(self, remotePlaylist):
      print "playPlaylist"
      
  def errorOK(self,title="", msg=""):
      print "errorOK"
