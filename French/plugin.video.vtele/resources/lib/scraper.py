
import os
import re
import sys
import time
import urllib
from traceback import print_exc

from vteleapiservice import *

vteleapi = vTeleApi()

def getVideo( PID, refresh=True ):
    return vteleapi.theplatform( PID, refresh=refresh )


def getDate( jsondate ):
    #not really used
    try:
        d = jsondate.replace( "-62", "", 1 )
        d = float( "".join( re.findall( '(\\d{10})', d ) ) )
        return time.strftime( "%d-%m-%Y", time.localtime( d ) )
    except:
        pass
    return ""

def getCollections():
    collections = vteleapi.GetCollections()
    return collections


def getPageRepertoire( cat='Emissions', refresh=False ):
    # cat : string 'Pays', 'Genres', 'Emissions'
    repertoire = vteleapi.GetPageRepertoire( refresh=refresh ) or {}
    return repertoire
    
def getPageRepertoireEmission( cat='Emissions', refresh=False ):
    # cat : string 'Pays', 'Genres', 'Emissions'
    repertoire = vteleapi.GetPageRepertoireEmission( refresh=refresh ) or {}
    return repertoire


def getEmissions():
    emissions = vteleapi.GetEmissions() or []
    return emissions
    
    
def getAllEpisodesId( emissionId ):
    try:
        episodes = getPageEmission( emissionId )[ "Episodes" ]
        return [ str( e[ "uid" ] ) for e in episodes ]
    except:
        print_exc()
    return []

    
def getEmissionsWithFullDescription():
    t = time.time()
    #emissions up to date
    up_emissions = getPageRepertoire()

    emissions = []
    #emissions uptodate, set with max infos
    for e in up_emissions:
        if not(e["vod"] == "0"):
            emissions.append( e )

    full_emissions = {}
    full_emissions[ "Emissions" ] = emissions

    return full_emissions

    print len( emissions )
    #print len( full_emissions[ "Outdated" ] )
    print time_took( t )
    #json_dumps( full_emissions )
    print time_took( t )

def getPageEmission( emissionId, cat='Episodes', uselocal=False, refresh=False ):
    emission = vteleapi.GetPageEmission( emissionId=emissionId, uselocal=uselocal, refresh=refresh ) or {}
    print emission
    return emission#.get( cat )
    
#Utilisé
def getSaisons( emissionId, cat='Episodes', uselocal=False, refresh=False ):
    emission = vteleapi.GetSaisons( emissionId=emissionId, uselocal=uselocal, refresh=refresh ) or {}
    print emission
    return emission
    
def getLive( emissionId, cat='Episodes', uselocal=False, refresh=False ):
    emission = vteleapi.GetLive( emissionId=emissionId, uselocal=uselocal, refresh=refresh ) or {}
    print emission
    return emission
    
#Utilisé
def getSaison( emissionId, saisonId, cat='Episodes', uselocal=False, refresh=False ):
    emission = vteleapi.GetSaison( emissionId=emissionId, saisonId=saisonId, uselocal=uselocal, refresh=refresh ) or {}
    return emission


def getPageEpisode( episodeId ):
    episodes = vteleapi.GetPageEpisode( episodeId=episodeId )
    return episodes.get( lol )


def refreshAllEmissions( dialog_update=None ):
    t = time.time()

    emissions = getPageRepertoire( refresh=True )
    totals = float( len( emissions ) or 1 )
    for count, emission in enumerate( emissions ):
        pct = int( ( float( count+1 ) / totals ) * 100.0 )
        if hasattr( dialog_update, 'update' ):
            if dialog_update.iscanceled(): break
            dialog_update.update( pct, "Refresh emission %i of %i" % ( count+1, int( totals ) ), emission[ "Titre" ], "Please wait..." )
        else:
            print "%i%%" % pct, emission[ "Titre" ]
        getPageEmission( emission[ "uid" ], refresh=True )

    print "[TouTV] Refresh all emissions took %s" % time_took( t )


def vteledb( refresh=False ):
    #not used in features
    t = time.time()
    vtele_db = os.path.join( os.path.dirname( ADDON_CACHE ), "vtele.json" )
    if not refresh and os.path.exists( vtele_db ):
        if not is_expired( os.path.getmtime( vtele_db ) ):
            try:
                data = json.loads( open( vtele_db ).read() )
                print time_took( t )
                return data
            except: pass
    #create db
    all = {}
    full_emissions = getEmissionsWithFullDescription()

    for emission in full_emissions[ "Emissions" ]:
        #emission[ "AirDateLongString" ] = getPremiered( emission[ "Id" ] )
        all[ emission[ "uid" ] ] = emission

    str_all = json_dumps( all, debug=False )
    #print str_all
    try: file( vtele_db, "wb" ).write( str_all )
    except: print_exc()

    data = json.loads( str_all )
    print time_took( t )
    return data


#if ( __name__ == "__main__" ):
    #setDebug( True )
    #print vteledb().keys()

    #getEmissionsWithFullDescription()
    #refreshAllEmissions()

    #emissions, episodes = getFavourites()
    #print emissions

    #getPageAccueil()
    #searchTerms( "vie de quartier" )
    #getPageGenre( "animation" )
    #getGenres()
    #getCollections()
    #getCarrousel( "carrousel-animation" )
    #getPageRepertoire()
    #getPageRepertoire('Pays')
    #getPageRepertoire('Genres')
    #getPageEmission( 1852377904 )#, 'Emission' )
    #getPageEpisode( 2060099162 )

    #print getDate( '/Date(-62135578800000-0500)/' )


