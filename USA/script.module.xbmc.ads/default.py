import sys
import xbmc
import xbmcaddon
import xbmcplugin
import xbmcgui

addon_id = 'script.module.xbmc.ads'
ADDON = xbmcaddon.Addon(id = addon_id)

from xbmcads import ads

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


def addDir(mode, client, id, sno, type, details, t, p):
    u=sys.argv[0]+"?mode="+str(mode)+"&client="+str(client)+"&id="+str(id)+"&sno="+str(sno)+"&type="+str(type)+"&details="+str(details)+"&p="+str(p)
    
    img=''
    if type == 'IMAGE':
        img = details
    elif type == 'YOUTUBE':
        img =  'http://i.ytimg.com/vi/%s/0.jpg' % details
    
    ok=True
    
    liz=xbmcgui.ListItem(t, iconImage=img, thumbnailImage=img)

    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)

    return ok

params=get_params()

mode=None
try:
    mode=params["mode"]
except:
    pass
    
client=None
try:
    client=params["client"]
except:
    pass
    
id=None
try:
    id=params["id"]
except:
    pass
    
sno=None
try:
    sno=params["sno"]
except:
    pass
    
type=None
try:
    type=params["type"]
except:
    pass
    
details=None
try:
    details=params["details"]
except:
    pass
    
p=None
try:
    p=params["p"]
except:
    pass

if mode == None:

    try:
        import simplejson as json
    except:
        import json
        
    ads_list = json.loads( ads.ALL() )
    
    for ad in ads_list:
        addDir('AD', ad['ClientId'], ad['AdId'], ad['AdNum'], ad['AdType'], ad['Ad'], ad['AdTitle'], ad['priority'])
        
    xbmcplugin.endOfDirectory(int(sys.argv[1]))
    
elif mode == 'AD':
    ads.POP_ADVERTISE(client, id, sno, type, details, p)