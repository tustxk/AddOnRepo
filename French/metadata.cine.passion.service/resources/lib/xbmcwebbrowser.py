""" Display url using the default browser.
    by frost (passion-xbmc.org)
"""

# Modules General
import webbrowser
from traceback import print_exc

# Modules XBMC
import xbmc


def notification( header="", message="", sleep=5000, icon="DefaultIconInfo.png" ):
    """ Will display a notification dialog with the specified header and message,
        in addition you can set the length of time it displays in milliseconds and a icon image.
    """
    xbmc.executebuiltin( "XBMC.Notification(%s,%s,%i,%s)" % ( header, message, sleep, icon ) )


def launchUrl( url ):
    try: webbrowser.open( url )
    except: print_exc()


def Main( url, Addon ):
    try:
        # notify user
        notification( Addon.getAddonInfo( "name" ), url, icon=Addon.getAddonInfo( "icon" ) )
        # launch url
        launchUrl( url )
    except:
        print_exc()



if ( __name__ == "__main__" ):
    import sys
    #print sys.argv
    from xbmcaddon import Addon
    Main( sys.argv[ 3 ], Addon( sys.argv[ 2 ] ) )
