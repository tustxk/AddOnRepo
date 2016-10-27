
# Modules General
import sys

# Modules XBMC
import xbmc
from xbmcaddon import Addon


# addon constants
ServiceId  = "metadata.cine.passion.service"
Service    = Addon( ServiceId )
AddonId    = "metadata.cine.passion-xbmc.org"
Addon      = Addon( AddonId )
RunService = "RunScript(%s)" % ServiceId

from resources.lib.Language import Language
Language = Language( Addon, Service, xbmc )


class _Info:
    """ Parse sys.argv : (ServiceId [Action,AddonId,OPT1,OPT2]) """
    def __init__( self, keys=[ "Action", "AddonId", "Option1", "Option2" ] ):
        self.__info__ = dict( zip( keys, sys.argv[ 1: ] ) )
        print "[%s] params: %r" % ( ServiceId, self.__info__ )

    def __getattr__( self, namespace ):
        return self[ namespace ]

    def __getitem__( self, namespace ):
        return self.get( namespace )

    def __setitem__( self, key, default="" ):
        self.__info__[ key ] = default

    def get( self, key, default="" ):
        return self.__info__.get( key, default ).lower()

    def isempty( self ):
        return not bool( self.__info__ )

    def IsTrue( self, key, default="false" ):
        return ( self.get( key, default ) == "true" )


class Main:
    def __init__( self, *args, **kwargs ):
        try:
            # parse args
            self.args = _Info()

            if self.args.isempty() or self.args.Action == "updatecredits":
                updatetime = ( -1, 0, 1, 6, 12, 18, 24 )[ int( Service.getSetting( "updatetime" ) ) ]
                if ( updatetime >= 0 ):
                    if self.args.isempty():
                        self.check_settings_compatibility()

                    self.update_credits( updatetime )
                else:
                    # no service
                    print "%s : Disabled!" % ServiceId

            elif self.args.Action == "webbrowser":
                import resources.lib.xbmcwebbrowser as webbrowser
                webbrowser.Main( self.args.Option1, Addon )

            elif self.args.Action == "opensettings":
                self.open_settings( self.args.AddonId )

            elif self.args.Action == "togglesettings":
                AddonInfoIsVisible = xbmc.getCondVisibility( "Window.IsVisible(addoninformation)" )
                if AddonInfoIsVisible: xbmc.executebuiltin( "Dialog.Close(addoninformation)" )

                toggle = ( "true", "false" )[ Addon.getSetting( self.args.Option1 ) == "true" ]
                statut = ( Language[ 24021 ], Language[ 24022 ] )[ toggle == "true" ]
                Service.setSetting( self.args.Option2, statut )
                Addon.setSetting( self.args.Option2, statut )
                Addon.setSetting( self.args.Option1, toggle )

                if AddonInfoIsVisible:
                    xbmc.sleep( 200 )
                    self.open_info()

                self.open_settings( self.args.AddonId )

                # update user infos
                if toggle == "true":
                    self.args[ "Option1" ] = "false"
                    self.args[ "Option2" ] = "true"
                    updatetime = ( -1, 0, 1, 6, 12, 18, 24 )[ int( Service.getSetting( "updatetime" ) ) ]
                    self.update_credits( updatetime )

            elif self.args.Action == "exportlibrary":
                AddonInfoIsVisible = xbmc.getCondVisibility( "Window.IsVisible(addoninformation)" )
                if AddonInfoIsVisible: xbmc.executebuiltin( "Dialog.Close(addoninformation)" )

                overwrite = Addon.getSetting( "el_overwrite" )
                popup = ( "false", "true" )[ overwrite == "false" ]
                if Addon.getSetting( "el_single" ) == "true":
                    filepath = Addon.getSetting( "el_path" )
                    params = "%s,%s" % ( popup, filepath )
                else:
                    thumbs = Addon.getSetting( "el_thumbs" )
                    actors = Addon.getSetting( "el_actors" )
                    params = "%s,%s,%s,%s" % ( popup, thumbs, overwrite, actors )

                if AddonInfoIsVisible:
                    xbmc.sleep( 200 )
                    self.open_info()

                self.open_settings( self.args.AddonId )
                xbmc.executebuiltin( "ExportLibrary(video,%s)" % params )
        except:
            from traceback import print_exc
            print_exc()

    def open_info( self ):
        xbmc.sleep( 100 )
        xbmc.executebuiltin( "SetFocus(50)" )
        xbmc.sleep( 100 )
        xbmc.executebuiltin( "Action(Info)" )
        xbmc.sleep( 100 )

    def open_settings( self, addonId, setFocus=True ):
        xbmc.sleep( 100 )
        xbmc.executebuiltin( "Addon.OpenSettings(%s)" % addonId )
        xbmc.sleep( 100 )
        if setFocus:
            xbmc.executebuiltin( "SetFocus(200)" )

    def update_credits( self, updatetime ):
        AddonInfoIsVisible = xbmc.getCondVisibility( "Window.IsVisible(addoninformation)" )
        AddonSettingsIsVisible = xbmc.getCondVisibility( "Window.IsVisible(addonsettings)" )

        # don't active busy or close/open dialog
        silent = self.args.IsTrue( "Option1", "true" )
        if not silent:
            xbmc.executebuiltin( "ActivateWindow(busydialog)" )
            if AddonInfoIsVisible:
                xbmc.executebuiltin( "Dialog.Close(addoninformation)" )
                xbmc.sleep( 200 )

        # # retrieve infos
        from resources.lib.service import Main
        user, notification = Main()

        if ( Service.getSetting( "updatetime" ) == "0" ):
            if AddonInfoIsVisible:
                xbmc.executebuiltin( "Dialog.Close(busydialog)" )
                xbmc.executebuiltin( "Dialog.Close(addoninformation)" )
                xbmc.sleep( 200 )
                self.open_info()
            return

        # close busy
        if not silent and xbmc.getCondVisibility( "Window.IsVisible(busydialog)" ):
            xbmc.executebuiltin( "Dialog.Close(busydialog)" )

        # cancel any auto update credits Cine-Passion
        if xbmc.getCondVisibility( "System.HasAlarm(UpdateCreditsCinePassion)" ):
            xbmc.executebuiltin( "XBMC.CancelAlarm(UpdateCreditsCinePassion,true)" )

        if updatetime > 0:
            # setup auto update credits Cine-Passion
            command = "%s,%i,true" % ( RunService, updatetime * 60 )
            xbmc.executebuiltin( "XBMC.AlarmClock(UpdateCreditsCinePassion,%s)" % command )

        if not silent:
            if AddonSettingsIsVisible:
                xbmc.executebuiltin( "Dialog.Close(addonsettings)" )
                xbmc.sleep( 200 )

            # open addon info
            if AddonInfoIsVisible:
                self.open_info()

            # open addon settings
            if AddonSettingsIsVisible and user.error != "SetUserAccount":
                self.open_settings( ( self.args.AddonId, ServiceId )[ self.args.AddonId == ServiceId ], False )

        # notify user
        if not user.error and self.args.IsTrue( "Option2", Service.getSetting( "notify" ) ):
            msg = Language[ 33102 ] % str( user.messages )
            notification( Language[ 33101 ] % user.nickname, msg, 3000, user.avatar )
            xbmc.sleep( 2000 )
            msg = "[B][%i][/B] %s %s" % ( int( user.quota ), Language[ 33104 ], user.country )
            notification( Language[ 33103 ], msg, icon=user.avatar )

        elif user.error == "SetUserAccount":
            xbmc.executebuiltin( "RunScript(%s,opensettings,%s)" % ( ServiceId, AddonId ) )

    def update_globals( self ):
        from xbmcaddon import Addon
        globals().update( { "Addon": Addon( AddonId ) } )
        from resources.lib.Language import Language
        globals().update( { "Language": Language( Addon, Service, xbmc ) } )

    def check_settings_compatibility( self ):
        try:
            # fisrt check version of xbmc is 11.0 check settings
            OK = xbmc.getCondVisibility( "SubString(System.BuildVersion,PRE-11.0)" )
            if not OK:
                import time
                # is not xbmc 11.0 ! check for minimal date (Mar 10 2011)
                bdate = xbmc.getInfoLabel( "System.BuildDate" ).replace( "  ", " " )
                OK = time.mktime( time.strptime( bdate, "%b %d %Y" ) ) > 1299733200.0
            # check scraper minimal version 1.1.7
            OK = OK and ( Addon.getAddonInfo( "version" ) >= "1.1.7" )
            if OK:
                import os
                from filecmp import cmp
                # ok now check if scraper has service settings
                service_settings = os.path.join( Addon.getAddonInfo( "path" ), "resources", "service_settings.xml" )
                def_settings = os.path.join( Addon.getAddonInfo( "path" ), "resources", "settings.xml" )
                # is not same, change settings
                if not cmp( service_settings, def_settings ):
                    # create backup
                    try: os.rename( def_settings, def_settings + ".default" )
                    except: pass
                    # update settings
                    f = open( def_settings, "w" )
                    f.write( open( service_settings ).read() )
                    f.close()
                    # update globals
                    self.update_globals()
            else:
                print "[%s] Not Compatible!" % ServiceId
                print "[%s] Scraper Version: %s" % ( ServiceId, Addon.getAddonInfo( "version" ) )
                print "[%s] XBMC: %s compiled: %s" % ( ServiceId, xbmc.getInfoLabel( "System.BuildVersion" ), xbmc.getInfoLabel( "System.BuildDate" ) )
        except:
            from traceback import print_exc
            print_exc()



if ( __name__ == "__main__" ):
    Main()
    xbmc.executebuiltin( "Dialog.Close(busydialog)" )
