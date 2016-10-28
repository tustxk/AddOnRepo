import urllib,urllib2,sys,re,xbmcplugin,xbmcgui,xbmcaddon,xbmc,os
import datetime
import time
import extract
import downloader

ADDON = xbmcaddon.Addon(id='script.userdatainstaller')



def INSTALL_URL(url):
    dialog = xbmcgui.Dialog()
    dp = xbmcgui.DialogProgress()
    dp.create("UserData Installer","Downloading ",'', 'Please Wait')
    import time
    path         =  xbmc.translatePath(os.path.join('special://home/addons','packages'))
    lib          =  os.path.join(path, 'my_userdata_installer.zip')
    addonfolder  =  xbmc.translatePath(os.path.join('special://home/userdata/addon_data',''))
    dp.update(0,"Downloading ",'', 'Please Wait')
    downloader.download(url, lib, dp)
    time.sleep(4)
    dp.update(0, "Extracting ",'',"Please Wait")
    extract.all(lib,addonfolder,dp)
    time.sleep(2)
    dialog.ok("UserData Installer", "","All Done Enjoy !!", "")
	        
    
    
    
    
def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                                
        return param

        
               
params=get_params()
url=None
mode=None


try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:        
        mode=int(params["mode"])
except:
        pass
   
        
#these are the modes which tells the plugin where to go
INSTALL_URL(url)
        
       
#xbmcplugin.endOfDirectory(int(sys.argv[1]))
