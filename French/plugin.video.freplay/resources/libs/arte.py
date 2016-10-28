import urllib2
import CommonFunctions
common = CommonFunctions
from xml.dom import minidom
import globalvar

url_base='http://www.arte.tv/papi/tvguide-flow/sitemap/feeds/videos/F.xml' 

def fix_text(text):
    print
    return text.replace('&amp;','&').encode('utf-8').replace('&#039;',' ')

def list_shows(channel,folder):
    shows=[]
    d=dict()
    
    if folder=='none':
        xml = open(globalvar.CATALOG_ARTE).read()
        url=common.parseDOM(xml, "url")
        for i in range(0, len(url)):
            categoryTab=common.parseDOM(url[i], "video:category")
            if len(categoryTab)>0:
                category=fix_text(categoryTab[0])
                if category not in d:
                    shows.append( [channel,category,category,'','folder'] )
                    d[category]=category
    else:
        xml = open(globalvar.CATALOG_ARTE).read()
        url=common.parseDOM(xml, "url")
        for i in range(0, len(url)):
            titleTab=common.parseDOM(url[i], "video:title")
            if len(titleTab)>0:
                title=fix_text(titleTab[0])
            categoryTab=common.parseDOM(url[i], "video:category")
            if len(categoryTab)>0:
                if(fix_text(categoryTab[0])==folder and title not in d):                   
                    shows.append( [channel,title,title,'','shows'] )
                    d[title]=title
    return shows

def getVideoURL(channel,url):
    print url
    url=urllib2.unquote(url[url.index('videorefFileUrl')+16:]).decode('utf8')
    xml = urllib2.urlopen(url).read()
    xmldoc = minidom.parseString(xml)
    itemlist = xmldoc.getElementsByTagName('video') 
    for s in itemlist :
        if s.attributes['lang'].value==globalvar.LANG:
            url=s.attributes['ref'].value
    xml = urllib2.urlopen(url).read()   
    xmldoc = minidom.parseString(xml)     
    urlslist = xmldoc.getElementsByTagName('urls')
    for urls in urlslist :
        itemlist = urls.getElementsByTagName('url') 
        for s in itemlist :
            if s.attributes['quality'].value==globalvar.QLTY:
                url=s.firstChild.data
    return url
    
def list_videos(channel,show_title):
    videos=[]
    xml = open(globalvar.CATALOG_ARTE).read()	
    url=common.parseDOM(xml, "url")
    for i in range(0, len(url)):      
        video_url=''
        name=''
        image_url=''
        date=''
        duration=''
        views=''
        desc=''
        rating=''
        tmpTab=common.parseDOM(url[i], "video:publication_date")
        if len(tmpTab)>0:
            date=tmpTab[0][:10]
        tmpTab=common.parseDOM(url[i], "video:duration")
        if len(tmpTab)>0:
            duration=tmpTab[0]
        tmpTab=common.parseDOM(url[i], "video:view_count")
        if len(tmpTab)>0:
            views=tmpTab[0]
        tmpTab=common.parseDOM(url[i], "video:rating")
        if len(tmpTab)>0:
            rating=tmpTab[0]
        tmptab=common.parseDOM(url[i], 'video:player_loc allow_embed="yes"')
        if len(tmpTab)>0:
            print 'hi' + len(tmptab)
            video_url=tmpTab[0]
        start=video_url.find('MasterPlugin.feedurl=')
        print start
        print video_url
        #video_url.decode('utf-8')
        descriptionTab=common.parseDOM(url[i], "video:description")
        if len(descriptionTab)>0:
            name=fix_text(descriptionTab[0])
            desc=fix_text(descriptionTab[0])
        picTab=common.parseDOM(url[i], "video:thumbnail_loc")
        if len(picTab)>0:
            image_url=picTab[0]
        titleTab=common.parseDOM(url[i], "video:title")
        if len(titleTab)>0:
            title=fix_text(titleTab[0])
        if(title==show_title):       
            infoLabels={ "Title": name,"Plot":desc,"Aired":date,"Duration": duration, "Year":date[:4]}   
            videos.append( [channel, video_url, name, image_url,infoLabels,'play'] )
    return videos