from entertainment.filestore import FileStore
fs = FileStore()
if fs.check_file_store('http://xty.me/xunitytalk'):
    fs.remove_file_store('http://xty.me/xunitytalk' )

if not fs.check_file_store('https://bitbucket.org/xnty/drplxnty/raw/78f81df18608bf3f472427d69a40e2d0c456ff15/_MAIN/xunity_pl_dir.plx'):
    fs.add_file_store('[B][COLOR steelblue]X[/COLOR][COLOR white]UNITYTALK[/COLOR][/B] [COLOR gray]PLAYLIST DIRECTORY[/COLOR]', '', 'https://raw.githubusercontent.com/Coolwavexunitytalk/images/2f125e294033cc32ccdc867a60ca249d4e30f76c/xunitytalk%20playlist.png', 'playlist', 'xbmcplx', 'XBMC PLX', 'https://bitbucket.org/xnty/drplxnty/raw/78f81df18608bf3f472427d69a40e2d0c456ff15/_MAIN/xunity_pl_dir.plx' )



def OPEN_URL(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    return link


try:
    import urllib2,xbmc,xbmcaddon,os
    ADDON = xbmcaddon.Addon(id='script.icechannel')
    cartoon = xbmc.translatePath(os.path.join(ADDON.getAddonInfo('profile'),'databases','cartoon2'))
    xunity='http://gearscenter.com/cartoon_control/gapi-ios/index.php?op_select=catalog&os=ios&param_10=AIzaSyBsxsynyeeRczZJbxE8tZjnWl_3ALYmODs&param_7=1.0.0&param_8=com.appmovies.gears&type_film=Movie'
    response=OPEN_URL(xunity)    
    f = open(cartoon, mode='w')
    f.write(response)
    f.close()
except:pass
