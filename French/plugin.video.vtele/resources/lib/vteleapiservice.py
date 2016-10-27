####################################################
#
#   Service qui gère la connexion à l'API de vtele
#
####################################################
import os
import re
import urllib
import base64
import urllib2

try:
    import json
except ImportError:
    import simplejson as json

from utilities import *

DEBUG = True

API_SERVICE_URL         = "http://apps.vtele.ca/api/"
THEPLATFORM_CONTENT_URL = "http://api.brightcove.com/services/library?command=find_video_by_id&token=2sgr1KCsKKJXcqUFQdti_mXZAhdNB-wCFwCbGW6lz5atwI1QTrElxQ..&media_delivery=http&video_id=" #+"&mbr=true"

HTTP_USER_AGENT         = "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.1.1) Gecko/20090715 Firefox/3.5.1"

def setDebug( yesno ):
    global DEBUG
    DEBUG = yesno


def _print( msg, debug=False ):
    if DEBUG or debug:
        print msg


def json_dumps( data, sort_keys=True, indent=2, debug=False ):
    try:
        str_dump = json.dumps( data, sort_keys=sort_keys, indent=indent )
        if DEBUG or debug:
            _print( str_dump, debug )
            _print( "-"*100, debug )
        return str_dump
    except:
        return "%r" % data


def get_html_source( url, refresh=False, uselocal=False ):
    """ fetch the html source """
    source = ""
    try:
        # set cached filename
        source, sock, c_filename = get_cached_source( url, refresh, uselocal, debug=_print )

        if not source or sock is None:
            _print( "Reading online source: %r" % url )
            query_args = { 'timestamp':'1' }
            encoded_args = urllib.urlencode(query_args)
            #sock = urllib.urlopen( url, encoded_args )
            
            
            request = urllib2.Request(url,encoded_args)
            base64string = base64.encodestring('%s:%s' % ("mirego", "RiOnV/24_8WC-jS-@%9%Q8RIb!d#rwSE")).replace('\n', '')
            request.add_header("Authorization", "Basic %s" % base64string)   
            sock = urllib2.urlopen(request)
            
            
            source = sock.read()
            if c_filename:
                try: file( c_filename, "w" ).write( source )
                except: print_exc()
            sock.close()
    except:
        print_exc()
    return source
    
def get_html_source_nopost( url, refresh=False, uselocal=False ):
    """ fetch the html source """
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:11.0) Gecko/20100101 Firefox/13.0')
    response = urllib2.urlopen(req,timeout=30)
    link=response.read()
    response.close()
    return link


class _urlopener( urllib.FancyURLopener ):
    version = os.environ.get( "HTTP_USER_AGENT" ) or HTTP_USER_AGENT
urllib._urlopener = _urlopener()


class vTeleApi:
    def __init__( self ):
        self.__handler_cache = {}

    def __getattr__( self, method ):
        if method in self.__handler_cache:
            return self.__handler_cache[ method ]

        def handler( *args, **kwargs ):
            if method.lower() == "theplatform":
                return self.content_select( args[ 0 ], kwargs.get( "refresh", True ) )
            else:
                return self.getRepertoire( method, **kwargs )

        handler.method = method
        self.__handler_cache[ method ] = handler
        return handler

    def getRepertoire( self, method, **kwargs ):
        start_time = time.time()
        url_end = "shows/"
        # get params
        refresh = False
        if kwargs.has_key( "refresh" ):
            refresh = kwargs[ "refresh" ]
            kwargs.pop( "refresh" )
        uselocal = False
        if kwargs.has_key( "uselocal" ):
            uselocal = kwargs[ "uselocal" ]
            kwargs.pop( "uselocal" )
        #
        if method == "GetPageEmission":
          url_end = "shows/" + kwargs["emissionId"] + "/videos"
            #url_end = "shows/" + kwargs["emissionId"] + "/videos"
        elif method == "GetSaisons":
            url_end = "shows/" + kwargs["emissionId"] + "/saisons"
        elif method == "GetSaison":
            url_end = "shows/" + kwargs["emissionId"] + "/videos/saisons/" + kwargs["saisonId"]
        
        url = API_SERVICE_URL + url_end
        
        if method == "GetLive":
            url = "http://vtele.ca/en-direct/includes/retreiveEmiV3.inc.php"
        
        query = urllib.urlencode( kwargs )
        if query: url += "?" + query
        #
        if method == "GetLive":
            content = get_html_source_nopost( url )
            data = json.loads( content )
        else:
            content = get_html_source( url, refresh, uselocal )
            data = json.loads( content ).get( "data" )

        _print( "[vTeleApi] %s took %s" % ( method, time_took( start_time ) ))
        _print(content)
        #json_dumps( data )

        return data

    def content_select( self, PID, refresh=True ):
        start_time = time.time()
        content = get_html_source_nopost( THEPLATFORM_CONTENT_URL + PID, refresh )
        data = json.loads( content )
        _print( "[vTeleApi] thePlatform took %s" % time_took( start_time ) )
        json_dumps( data )
        return data

if ( __name__ == "__main__" ):
    setDebug( True )
    vteleapi = vTeleApi()
    
    vteleapi.GetPays()

    #vteleapi.GetPageRepertoire()
    #vteleapi.GetPageAccueil()
    #vteleapi.GetGenres()
    #vteleapi.GetCollections()
    #vteleapi.GetEmissions()
    #vteleapi.GetPageGenre( genre="animation" )
    #vteleapi.GetPageEmission( emissionId=2041271036 ) # digit
    #vteleapi.GetPageEpisode( episodeId=2060099162 ) # digit
    #vteleapi.GetCarrousel( playlistName="carrousel-animation" )
    #vteleapi.SearchTerms( query="vie de quartier"  )

    #print vteleapi.theplatform( '2S7KnmMzf3qdFokIL61ORofYT7vh73Am', refresh=True )

    # not supported on xbmc is m3u8 file type
    #vteleapi.validation( idMedia='2S7KnmMzf3qdFokIL61ORofYT7vh73Am', refresh=True )
