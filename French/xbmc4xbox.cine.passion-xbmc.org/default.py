
import re
import os
import urllib
from traceback import print_exc
from shutil import copyfile, rmtree

try:
    import xbmc
    import xbmcgui
except:
    xbmc = None
    xbmcgui = None


addonId = "xbmc4xbox.cine.passion-xbmc.org"
url_xml = "http://passion-xbmc.org/addons/addons.php"
url_dl  = "http://passion-xbmc.org/addons/Download.php/%s/" % ( addonId )

home_dir    = os.getcwd()
addon_xml   = os.path.join( home_dir, "addon.xml" )
scraper_xml = os.path.join( "scrapers", "video", "cine-passion.xml" )
icon        = os.path.join( "scrapers", "video", "cine-passion.png" )

# "special://xbmc/system" is same as "Q:\\system"
if xbmc is None: xbmc_system = "C:\\Program Files\\XBMC\\system"
else: xbmc_system = xbmc.translatePath( "special://xbmc/system" )


def check_version( new_xml=None ):
    # return new version greater of old
    try:
        regexp = '<addon.*?id="%s".*?version="(.*?)".*?>' % addonId
        if new_xml is not None: new_ver = re.search( regexp, open( new_xml ).read(), re.S ).group( 1 )
        else: new_ver = re.search( regexp, urllib.urlopen( url_xml ).read(), re.S ).group( 1 )
        old_ver = re.search( regexp, open( os.path.join( os.getcwd(), "addon.xml" ) ).read(), re.S ).group( 1 )
        if new_ver > old_ver:
            return new_ver
    except:
        print_exc()


def unzip( filename, dpath ):
    from zipfile import ZipFile
    OK = False
    try:
        zip = ZipFile( filename, "r" )
        namelist = zip.namelist()
        try:
            d = os.path.join( dpath, namelist[ 0 ].strip( "/" ) )
            if os.path.exists( d ): rmtree( d )
        except:
            print_exc()
        for item in namelist:
            if not item.endswith( "/" ):
                root, name = os.path.split( item )
                directory = os.path.normpath( os.path.join( dpath, root ) )
                if not os.path.isdir( directory ): os.makedirs( directory )
                file( os.path.join( directory, name ), "wb" ).write( zip.read( item ) )
        zip.close()
        del zip
        OK = True
    except:
        print_exc()
    return OK


def filecopy( src, dst ):
    copyfile( src, dst )
    print "Copy: " + src + " to " + dst
    print


def Main():
    OK = True
    try:
        new_ver = check_version()
        if new_ver:
            filename = "%s-%s.zip" % ( addonId, new_ver )
            dpath = os.path.join( os.getcwd(), "packages" )
            if not os.path.isdir( dpath ): os.makedirs( dpath )
            fp, h = os.path.join( dpath, filename ), "Already downloaded!\n"
            # download new version, if not exists
            if not os.path.exists( fp ):
                fp, h = urllib.urlretrieve( url_dl + filename, fp )
            print fp
            print h

            if unzip( fp, dpath ):
                # check is realy new
                new_xml = os.path.join( os.getcwd(), "packages", addonId, "addon.xml" )
                new_ver = check_version( new_xml )
                if new_ver:
                    source_dir = os.path.join( os.getcwd(), "packages", addonId )
                    # overwrite current cine-passion.xml
                    filecopy( os.path.join( source_dir, scraper_xml ), os.path.join( home_dir, scraper_xml ) )
                    # overwrite current cine-passion.png
                    filecopy( os.path.join( source_dir, icon ), os.path.join( home_dir, icon ) )
                    # overwrite current addon.xml
                    filecopy( new_xml, addon_xml )

        # is new or not, overwrite scraper.
        # xbmc system overwrite current cine-passion.xml
        filecopy( os.path.join( home_dir, scraper_xml ), os.path.join( xbmc_system, scraper_xml ) )
        # xbmc system overwrite current cine-passion.png
        filecopy( os.path.join( home_dir, icon ), os.path.join( xbmc_system, icon ) )
    except:
        print_exc()
        OK = False

    if OK:
        if not new_ver:  msg = "Scraper Ciné-Passion up to date."
        else: msg = "Scraper Ciné-Passion updated to version %s." % new_ver
        return msg, "", ""
    else:
        return ( "Error: Scraper Ciné-Passion Not Updated!",
                 "Copy your [B]'Q:\\xbmc.log'[/B] to [B]'http://pastebin.com/'[/B]",
                 "And send your pastebin url to [B]'passion-xbmc.org'[/B]"
                 )


if ( __name__ == "__main__" ):
    msg, msg2, msg3 = Main()
    if xbmcgui is None:
        print msg
        print msg2
        print msg3
    else:
        xbmcgui.Dialog().ok( "Ciné-Passion (XBMC4XBox)", msg, msg2, msg3 )
        # paste xbmc.log for xbox
        logfile = "Q:\\xbmc.log"
        if msg2 and os.path.exists( logfile ):
            kb = xbmc.Keyboard( "", "Pastebin.com : Enter your e-mail address", False )
            kb.doModal()
            if kb.isConfirmed():
                e_mail = kb.getText()
                if e_mail and "@" in e_mail:
                    from pastebin import Pastebin
                    data = open( logfile, "rb" ).read()
                    # Submit a code snippet to Pastebin
                    url = Pastebin().submit( data, "Ciné-Passion (XBMC4XBox)", e_mail, None, 1, "1M", None )
                    file( os.path.join( os.getcwd(), "pastebin.txt" ), "w" ).write( url )
                    xbmcgui.Dialog().ok( "Pastebin submit success", "Url: [B]%s[/B]" % url, "File: pastebin.txt", "Dir: %s" % os.getcwd() )
