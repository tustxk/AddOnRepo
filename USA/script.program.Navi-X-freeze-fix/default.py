import os
import shutil
import fileinput
import xbmc, xbmcgui
	
Addon_NAME='Navi-X freeze fix'

class Main:
	#set main variables
	#andriod_path = ('//storage/sdcard0/Android/data/org.xbmc.xbmc/files/.xbmc/addons')
	#droid = xbmc.validatePath('//storage/sdcard0/Download/navix.py')
	directory_NaviX = (xbmc.translatePath('special://home/addons/Navi-X'))
	directory_navi_src = (xbmc.translatePath('special://home/addons/Navi-X/src' ))
	fix_dir = (xbmc.translatePath('special://home/addons/script.program.Navi-X-freeze-fix/src' ))
	addon_xml = os.path.join((xbmc.translatePath('special://home/addons/Navi-X')), 'addon.xml')
	
	fix_navix = os.path.join(fix_dir,'navix.py')	
	navix = os.path.join(directory_navi_src,'navix.py')
	navix_old = os.path.join(directory_navi_src,'navix.old')
	
	fix_fileloader = os.path.join(fix_dir,'CFileLoader.py')
	fileloader = os.path.join(directory_navi_src,'CFileLoader.py')
	fileloader_old = os.path.join(directory_navi_src,'CFileLoader.old')
	
	fix_playlist = os.path.join(fix_dir,'CPlayList.py')
	playlist = os.path.join(directory_navi_src,'CPlayList.py')
	playlist_old = os.path.join(directory_navi_src,'CPlayList.old')
	
	status = 'failed'
	version = 'invalid'

class Background(xbmcgui.Window):
    def __init__(self	):
    	self.background = (xbmc.translatePath('special://home/addons/script.program.Navi-X-freeze-fix/fanart.jpg'))
    	self.addControl(xbmcgui.ControlImage(0,0,1280,720, self.background, aspectRatio=1)) 
    		
class Display(xbmcgui.Window):
	#background and four input dialog buttons
	ACTION_PREVIOUS_MENU = 10
	ACTION_NAV_BACK = 92 
	def __init__(self):
		self.background = (xbmc.translatePath('special://home/addons/script.program.Navi-X-freeze-fix/fanart.jpg'))
		self.addControl(xbmcgui.ControlImage(0,0,1280,720, self.background, aspectRatio=1))
		self.strActionInfo = xbmcgui.ControlLabel(520, 300, 300, 300, '', 'font30', '0xFFFF00FF')
		self.addControl(self.strActionInfo)
		self.strActionInfo.setLabel(Addon_NAME)
		self.button0 = xbmcgui.ControlButton(385, 380, 135, 30, "  Freeze Fix")
		self.addControl(self.button0)
		self.button1 = xbmcgui.ControlButton(575, 380, 135, 30, "Freeze Undo")
		self.addControl(self.button1)
		self.button2 = xbmcgui.ControlButton(785, 380, 135, 30, "      Exit")
		self.addControl(self.button2)
		self.button3 = xbmcgui.ControlButton(575, 430, 135, 30, " Gotham Fix")
		self.addControl(self.button3)
		
		self.setFocus(self.button2)	
			
		self.button0.controlRight(self.button1)
		self.button0.controlLeft(self.button3)
		self.button0.controlUp(self.button3)
		self.button0.controlDown(self.button3)
		
		self.button1.controlRight(self.button2)
		self.button1.controlLeft(self.button0)
		self.button1.controlUp(self.button3)
		self.button1.controlDown(self.button3)
		
		self.button2.controlRight(self.button3)
		self.button2.controlLeft(self.button1)
		self.button2.controlUp(self.button3)
		self.button2.controlDown(self.button3)
		
		self.button3.controlRight(self.button0)
		self.button3.controlLeft(self.button2)
		self.button3.controlUp(self.button0)
		self.button3.controlDown(self.button0)
		
		
	def onAction(self, action):
		#non Display Button control
		if action == self.ACTION_PREVIOUS_MENU:
			self.close()
		if action == self.ACTION_NAV_BACK:
			self.close()

	def onControl(self, control):
		#Display Button control
		if control == self.button0:
			freeze_install(Main)
			
		if control == self.button1:
			freeze_uninstall(Main)
		
		if control == self.button3:
			xml_mod(Main)
			
		if control == self.button2:
			self.close()
			
		
def freeze_install(Main):    
	#install freeze fix
	LoG("hello. install.")
	if Main.version == ('valid'):
		if (not os.path.exists(Main.navix)) or (not os.path.exists(Main.fileloader)) or (not os.path.exists(Main.fileloader)):
			message("Error", "You do not appear to have Navi-X installed.")
			#notification("Error", "You do not appear to have Navi-X installed.")
			LoG("Error. You do not appear to have Navi-X installed.")
		else:
			###### navix
			if os.path.exists(Main.navix):
				if os.path.exists(Main.navix_old):
					os.remove(Main.navix)
					#devicelog(freezelog," removed navix.\n")
				else:
					os.rename(Main.navix, Main.navix_old)
					#devicelog(freezelog," renamed to navixold.\n") 
			try:
				#devicelog(freezelog," do shutil.copy2.\n")
				shutil.copy2(Main.fix_navix, Main.navix) 
				Main.status = 'success'			
			except :
				if os.path.exists(Main.navix):  # need this for android. it will copy but fault
					Main.status = 'success'
					#devicelog(freezelog," copied navix.\n")
					#message("Notice", "the fix has moved the files")
					'''try:    # for checking files for android
						shutil.copy2(Main.navix, Main.droid)					
					except :    # need this for android. it will copy but fault
						pass'''									
				else:
					LoG("Error. Could not do shutil.copy for navix.")
					#devicelog(freezelog," Could not do navx shutil.copy.\n")			
										
			######  CFileLoader
			if os.path.exists(Main.fileloader):
				if os.path.exists(Main.fileloader_old):
					os.remove(Main.fileloader)
				else:
					os.rename(Main.fileloader, Main.fileloader_old)
					#devicelog(freezelog," renamed to Cfileloaderold\n")
			try:
				#devicelog(freezelog," do shutil.copy2.\n")
				shutil.copy2(Main.fix_fileloader, Main.fileloader)
				Main.status = 'success'	
			except:
				if os.path.exists(Main.fileloader):   # need this for android. it will copy but fault
					Main.status = 'success'
					LoG("copied. fileloader.")
					#devicelog(freezelog,"  copied. Cfileloader.\n")
					#message("Notice", "the fix has moved the files")
					'''try:    # for checking files for android
						shutil.copy2(Main.fileloader, Main.droid)					
					except :    # need this for android. it will copy but fault
						pass'''										
				else:
					LoG("Error. Could not do shutil.copy for fileloader.")
					#devicelog(freezelog," Could not do fileloader shutil.copy.\n")
		
			######  CPlayList
			if os.path.exists(Main.playlist):
				if os.path.exists(Main.playlist_old):
					os.remove(Main.playlist)
				else:
					os.rename(Main.playlist, Main.playlist_old)
					#devicelog(freezelog," renamed to CPlayList\n")
			try:
				#devicelog(freezelog," do shutil.copy2.\n")
				shutil.copy2(Main.fix_playlist, Main.playlist)
				Main.status = 'success'	
			except:
				if os.path.exists(Main.playlist):   # need this for android. it will copy but fault
					Main.status = 'success'
					LoG("copied. CPlayList.")
					#devicelog(freezelog,"  copied. CPlayList.\n")
					#message("Notice", "the fix has moved the files")
					'''try:    # for checking files for android
						shutil.copy2(Main.playlist, Main.droid)					
					except :    # need this for android. it will copy but fault
						pass'''										
				else:
					LoG("Error. Could not do shutil.copy2 for playlist.")
					#devicelog(freezelog," Could not do playlist shutil.copy2.\n")
								
			if Main.status == 'success':
				message("Success", "The fix has been installed.")
				#notification("Success", "The fix has been installed.")
				LoG("fix. installed.")
			else:
				message("Error", "The fix installarion has failed.")
				
	elif Main.version == ('invalid'):
		message("Notice", "You need Navi-X version 3.7.8 to run this fix.")
								
def freeze_uninstall(Main):    
	#uninstall freeze fix
	LoG("hello. uninstall.")
	if Main.version == ('valid'):
		if (not os.path.exists(Main.navix)) or (not os.path.exists(Main.fileloader)) or (not os.path.exists(Main.playlist)):
			message("Error", "You do not appear to have Navi-X installed.")
			LoG("error. You do not appear to have Navi-X installed.") 
		elif (not os.path.exists(Main.navix_old)) or (not os.path.exists(Main.fileloader_old)) or (not os.path.exists(Main.playlist_old)):
			message("Error", "You do not appear to have original files to restore from. \nOr have not run this fix before")
			#notification("Error", "You do not appear to have Navi-X freeze fix installed."); 
		else:
			if os.path.exists(Main.navix):
				os.remove(Main.navix)
				os.rename(Main.navix_old, Main.navix)
		
			if os.path.exists(Main.fileloader):
				os.remove(Main.fileloader)
				os.rename(Main.fileloader_old,Main.fileloader)
				
			if os.path.exists(Main.playlist):
				os.remove(Main.playlist)
				os.rename(Main.playlist_old,Main.playlist)
					
			message("Success", "The fix has been removed.")
			#notification("Success", "The fix has been removed.") 
			LoG("fix. removed.")
			#devicelog(freezelog," The fix has been removed.\n")
	elif Main.version == ('invalid') :
		message("Notice", "You need Navi-X version 3.7.8 to run this fix.")

def xml_mod(Main):    
	#modify addon.xml for use with Gotham
	success = 0
	with open(Main.addon_xml, 'r+') as xml:
		for line in fileinput.input((Main.addon_xml), inplace=1):
			if ('"xbmc.python" version="1.0"') in line:
				line = line.replace('1.0' , '2.1.0')
				success = 1
			elif ('"xbmc.python" version="2.1.0"') in line:
				success = 2				
			print(line),			
	if success == 1:				
		message("Success","Navi-X is now all setup to run on Gotham")								
	elif success == 2:
			message("Notice","Navi-X was already setup to run on Gotham")								
	elif success == 0:
			message("Error","Could not find Python version number")
	xml.close()	
		
def version_chk(Main):    
	#check for Navi-X version 3.7.8 in line 4 of addon.xml
	with open(Main.addon_xml, 'r') as xml:
		for line in xml:
			if ('"3.7.8"') in line:
				print (Addon_NAME+ ": Navi-X " +line)
				LoG("Main.version. valid.")
				Main.version = ('valid')
				break
	xml.close()	
	
def message(title, message):
	#### Output display box
	dialog = xbmcgui.Dialog()
	dialog.ok(title, message)	
			
###### Error reporting
#create an accessable log for debugging android
#freezelog = xbmc.validatePath('//storage/sdcard0/Download/Navi-x-freeze.log')
#open(freezelog, 'w+').close()
def devicelog(path,text='',var=''):    
	with open(path, 'a+') as log:
		log.write(text)
		log.write(var)
	log.close()
#XBMC log	
def LoG(t=''): print Addon_NAME+": "+t
#on screen
def notification(header="", message="", sleep=5000 ): xbmc.executebuiltin( "XBMC.Notification(%s,%s,%i)" % ( header, message, sleep ) )

		
#### Start of program
if os.path.exists(Main.directory_NaviX):	
	version_chk(Main)		
	fix_display = Display()
	fix_display.doModal()
	del fix_display							
else:
	display = Background()
	display.show()
	message(Addon_NAME, "Can not find the Navi-X folder. \nPlease install the official Navi-X addon.")
	display.close()
	del display		
    	
#EOF			
