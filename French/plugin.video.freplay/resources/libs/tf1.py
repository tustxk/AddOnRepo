import urllib2
import json

url_categories={'tf1':'http://api.tf1.fr/tf1-genders/ipad/',
             'tmc':'http://api.tmc.tv/tmc-genres/android-smartphone/',
             'nt1':'http://api.nt1.tv/nt1-genres/android-smartphone/'
            }
url_shows={'tf1':'http://api.tf1.fr/tf1-programs/ipad/',
             'tmc':'http://api.tmc.tv/tmc-programs/android-smartphone/',
             'nt1':'http://api.nt1.tv/nt1-programs/android-smartphone/'
            }
url_videos={'tf1':'http://api.tf1.fr/tf1-vods/ipad/integral/0/program_id/',
             'tmc':'http://api.tmc.tv/tmc-vods/ipad/integral/0/program_id/',
             'nt1':'http://api.nt1.tv/nt1-vods/ipad/integral/0/program_id/'
            }
url_integ={'tf1':'http://api.tf1.fr/tf1-homepage-news/ipad/',
             'tmc':'http://api.tmc.tv/tmc-homepage-news/ipad/',
             'nt1':'http://api.nt1.tv/nt1-homepage-news/ipad/'
            }

def list_shows(channel,folder):
    shows=[]
    if folder=='none':
    	shows.append( [channel,'integ','Accueil (Integrales)','','shows'] )
        filPrgm=urllib2.urlopen(url_categories[channel]).read()
        jsoncat     = json.loads(filPrgm)
        for prtCat in jsoncat :
            childs  = prtCat['childs']
            for child in childs :
                shows.append( [channel,str(childs[child]['id']), childs[child]['name'].encode('utf-8'),'','folder'] )
    
    else:
        filPrgm=urllib2.urlopen(url_shows[channel]).read()
        jsoncat     = json.loads(filPrgm)
        #TMC...
        if channel=='tmc' or channel=='nt1':
            folder='999'
        for prgm in jsoncat :
            #print prgm
            if str(prgm['genderId'])==folder:
                if prgm['images']:
                    img=prgm['images'][0]['url']
                shows.append( [channel,prgm['id'], prgm['shortTitle'].encode('utf-8'),img,'shows'] )
    
    return shows

def getVideoURL(channel,idVideo):
    return 'http://wat.tv/get/ipad/'+idVideo+'.m3u8'

def list_videos(channel,show_title):
    videos=[]
    print show_title
    if show_title=='integ':
        fileVideos=urllib2.urlopen(url_integ[channel]).read()
        jsonvid     = json.loads(fileVideos)
        for video in jsonvid : 
            video_url=''
            video_url=str(video['linkAttributes']['watId'])
            name=video['title'].encode('utf-8')
            image_url=video['picture'].encode('utf-8')
            date=''
            duration=''
            views=''
            desc=''
            rating=''

            infoLabels={ "Title": name,"Plot":desc,"Aired":date,"Duration": duration, "Year":date[:4]}
            videos.append( [channel, video_url, name, image_url,infoLabels,'play'] )
    else:
        fileVideos=urllib2.urlopen(url_videos[channel] + str(show_title)).read()
        jsonvid     = json.loads(fileVideos)
        for video in jsonvid : 
            video_url=''
            if 'watid' in video:
                video_url=str(video['watId'])
            name=video['shortTitle'].encode('utf-8')
            image_url=video['images'][0]['url']
            date=video['publicationDate'][:10]
            duration=video['duration']
            views=''
            desc=video['longTitle']
            rating=''

            infoLabels={ "Title": name,"Plot":desc,"Aired":date,"Duration": duration, "Year":date[:4]}
            videos.append( [channel, video_url, name, image_url,infoLabels,'play'] )
    return videos