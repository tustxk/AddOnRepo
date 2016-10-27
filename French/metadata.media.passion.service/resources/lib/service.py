
# Modules General
import os
import sys
import time
import urllib
from traceback import print_exc
from xml.dom.minidom import parseString

# Modules XBMC
import xbmc
import xbmcgui
try:
    import xbmcvfs
except: 
    import shutil as xbmcvfs
    xbmcvfs.delete = os.remove
    xbmcvfs.rename = os.rename


# addon constants
Addon    = sys.modules[ "__main__" ].Addon
Service  = sys.modules[ "__main__" ].Service
Language = sys.modules[ "__main__" ].Language


def notification( header="", message="", sleep=5000, icon=Addon.getAddonInfo( "icon" ) ):
    """ Will display a notification dialog with the specified header and message,
        in addition you can set the length of time it displays in milliseconds and a icon image.
    """
    import os.path
    icon = ( Addon.getAddonInfo( "icon" ), icon )[ os.path.isfile( icon ) ]
    icon = ( "DefaultIconInfo.png", icon )[ os.path.isfile( icon ) ]
    xbmc.executebuiltin( "Notification(%s,%s,%i,%s)" % ( header.encode( "utf-8" ), message.encode( "utf-8" ), sleep, icon.encode( "utf-8" ) ) )


class _urlopener( urllib.URLopener ):
    #version = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; fr; rv:1.9.2.16) Gecko/20110319 Firefox/3.6.16'
    USER_AGENT = "Media-Passion Service/Demo"
    try:
        from xbmc import getInfoLabel
        USER_AGENT = USER_AGENT.replace( "Demo", Service.getAddonInfo( "version" ), 1 )
        USER_AGENT += " (XBMC for %s %s; %s" % ( os.environ.get( "OS", "XBox" ), getInfoLabel( "System.BuildVersion" ), getInfoLabel( "System.BuildDate" ) )
    except ImportError:
        USER_AGENT += " (Python %s on %s" % ( sys.version, sys.platform )
    USER_AGENT += ")"
    version = USER_AGENT

# set for user agent
urllib._urlopener = _urlopener()

def getText( node ):
    try: return node[ 0 ].childNodes[0].nodeValue
    except: return ""

def getAttr( node, id ):
    try: return node[ 0 ].getAttribute( id )
    except: return ""


url = "http://passion-xbmc.org/scraper%(debug)s/API/1/User.GetInfos/%(b64)s/%(token)s/%(lang)s/%(format)s/%(project)s"

class User:
    params = { "lang": "fr", "format": "XML", "project": "705f2172834666788607efbfca35afb3" }

    def __init__( self, b64="", token="", debug="" ):
        self.params.update( { "b64": b64, "token": token, "debug": debug } )

        self.error    = ""
        self.nickname = ""
        self.quota    = "0"
        self.country  = ""
        self.messages = "0"
        self.avatar   = ""

    def GetInfos( self ):
        # get and parse source
        dom = parseString( urllib.urlopen( url % self.params ).read() )

        self.error = getText( dom.getElementsByTagName( "error" ) )
        if not self.error:
            self.nickname = getText( dom.getElementsByTagName( "nickname" ) )
            self.quota    = getText( dom.getElementsByTagName( "quota" ) )
            self.messages = getText( dom.getElementsByTagName( "messages" ) )

            self.getCountry( getText( dom.getElementsByTagName( "country" ) ) )

            avatar = dom.getElementsByTagName( "avatar" )
            self.getAvatar( getAttr( avatar, "url" ), getAttr( avatar, "file" ) )

        #cleanup
        dom.unlink()

    def getCountry( self, country ):
        countries = "Argentina|Australia|Austria|Belgium|Brazil|Canada|Chile|China|Colombia|Cyprus|Czech Republic|Denmark|East Germany|Egypt|Finland|France|Germany|Greece|Hong Kong|Hungary|Iceland|India|Indonesia|Iran|Iraq|Ireland|Israel|Italy|Japan|Kuwait|Lebanon|Luxembourg|Malaysia|Malta|Mexico|Netherlands|New Zealand|Norway|Peru|Philippines|Poland|Portugal|Puerto Rico|Romania|Singapore|Slovakia|South Africa|South Korea|Soviet Union|Spain|Sweden|Switzerland|Taiwan|Thailand|Turkey|UK|USA|Ukraine|Venezuela|Vietnam|West Germany"
        try:
            #if countries.lower().count( country.lower() ):
            if country.lower() in countries.lower().split( "|" ):
                i = countries.lower().split( "|" ).index( country.lower() )
                # set real country for cine-passion
                self.country = countries.split( "|" )[ i ]
        except:
            print_exc()

    def getAvatar( self, url, filename ):
        try:
            try:
                CACHEDIR = os.path.join( Service.getAddonInfo( "profile" ), "~" )
                CACHEDIR  = xbmc.translatePath( CACHEDIR )
            except:
                CACHEDIR = ""
            if not os.path.isdir( CACHEDIR ):
                os.makedirs( CACHEDIR )
            avatar_cached = os.path.join( CACHEDIR, filename )
            if not os.path.exists( avatar_cached ):
                fp, h = urllib.urlretrieve( url, avatar_cached )
                print fp, "\n" + str( h ).replace( "\r", "" )

            if os.path.exists( avatar_cached ):
                self.avatar = avatar_cached
        except:
            print_exc()


def Main():
    user = None
    try:
        if Service.getSetting( "delcookies" ) == "true":
            CACHEDIR = os.path.join( Service.getAddonInfo( "profile" ), "~" )
            if os.path.isdir( CACHEDIR ):
                for file in os.listdir( CACHEDIR ):
                    try: xbmcvfs.delete( os.path.join( CACHEDIR, file ) )
                    except: print_exc()
            Service.setSetting( "delcookies", "false" )
            
        # get our settings
        token    = Addon.getSetting( "token" )
        tokenb64 = Addon.getSetting( "tokenb64" )
        username = Addon.getSetting( "username" )
        password = Addon.getSetting( "password" )

        user = User( tokenb64 or username, token or password, Addon.getSetting( "debug" ) )
        user.GetInfos()

        if user.error:
            if tokenb64 or token or username or password:
                xbmcgui.Dialog().ok( Language[ 33000 ], user.error )
            if not xbmcgui.Dialog().yesno( Language[ 33051 ], Language[ 33052 ], Language[ 33053 ], Language[ 33054 ], Language[ 24021 ], Language[ 24022 ] ):
                xbmcgui.Dialog().ok( Language[ 33000 ], Language[ 33055 ], Language[ 33056 ], Language[ 33057 ] )
                Service.setSetting( "updatetime", "0" )
            else:
                user.error = "SetUserAccount"

        if ( Service.getSetting( "updatetime" ) != "0" ):
            # set our user subclass
            #user = Passion.user
            # set our date and time based on region of user
            DATE_TIME_FORMAT = "%s %s" % ( xbmc.getRegion( "dateshort" ), xbmc.getRegion( "time" ) )
            # set our last updated
            updated = time.strftime( DATE_TIME_FORMAT, time.localtime( time.time() ) )
            # get and set our credits
            credits = "[B][%i][/B]" % int( user.quota )
            usercredits = Language[ 33008 ] % ( credits, updated )

            # set add-on setting
            Addon.setSetting( "usercredits", usercredits )
            Service.setSetting( "usercredits", usercredits )

            # set country - user.country
            if bool( user.country ) and str( Service.getSetting( "country" ) ) == str( Language[ 24022 ] ):
                Addon.setSetting( "enablempaa", "true" )
                if user.country != Addon.getSetting( "mpaa" ):
                    Addon.setSetting( "mpaa", user.country )
            #
            elif Addon.getSetting( "enablempaa" ) == "true":
                Addon.setSetting( "enablempaa", "false" )

    except:
        user = None
        print_exc()

    return user, notification
