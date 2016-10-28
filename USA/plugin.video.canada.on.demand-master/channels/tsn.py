import xml.etree.ElementTree as ET, urlparse
from theplatform import *
from BeautifulSoup import BeautifulStoneSoup

try:
    from pyamf import remoting
    has_pyamf = True
except ImportError:
    has_pyamf = False

try:
    from sqlite3 import dbapi2 as sqlite

except:
    from pysqlite2 import dbapi2 as sqlite


class TSN(BaseChannel):
    short_name = 'tsn'
    long_name = 'The Sports Network'
    base_url = 'http://video.tsn.ca/'
    default_action = 'root'

    def action_play_clip(self):
        urltemplate = 'http://esi.ctv.ca/datafeed/urlgenjs.aspx?vid=%s'
        url = urltemplate % self.args['clip_id']
        logging.debug('play_clip: %s' % url)

        data = self.plugin.fetch(url, max_age=self.cache_timeout).read()

        remote_url = data.split("'")[1]
        o = urlparse.urlparse(remote_url)
        logging.debug(o)

        vidquality = self.plugin.get_setting('vidquality')
        # adding 1 to the video quality because I don't use zero as the lowest quality
        # I use 1 as the lowest quality.
        vidquality=int(vidquality)+1
        logging.debug('vidquality: %r' % vidquality)

        if o.netloc == 'tsn.fcod.llnwd.net':
                firstpart = 'rtmpe://tsn.fcod.llnwd.net/a5504'
                secondpart = re.compile('a5504/(.+?)\'').findall(data)
                #playpath = re.compile('ondemand/(.+?).mp4').findall(remote_url)
                url = firstpart + ' playpath=mp4:' + secondpart[0]
        elif o.netloc == 'ctvmms.rd.llnwd.net':
                firstpart = 'http://ctvmms.vo.llnwd.net/kip0/_pxn=1+_pxI0=Ripod-h264+_pxL0=undefined+_pxM0=+_pxK=19321+_pxE=mp4/'
                secondpart = re.compile('ctvmms.rd.llnwd.net/(.+?).mp4').findall(remote_url)
                url = firstpart + secondpart[0] + '.mp4'
        elif o.netloc == 'tsnpmd.akamaihd.edgesuite.net':
                url = remote_url
                #starting in version 0.1.5 (March 19 2013) tsn started using adaptive quality in their http streams
                #the quality now goes up to 720p (adaptive_08)
                url = url.replace('Adaptive_04','Adaptive_0' + str(vidquality))
        else:
                #break that down into 3 parts so that we can build the final url and playpath
                firstpart = re.compile('rtmpe(.+?)ondemand/').findall(remote_url)
                firstpart = 'rtmpe' + firstpart[0] + 'ondemand?'
                secondpart = re.compile('\?(.+?)\'').findall(data)
                thirdpart = re.compile('ondemand/(.+?)\?').findall(remote_url)
                playpath = ' playpath=mp4:' + thirdpart[0]

                #the tsn site adaptivly figures out what quality it should show you
                #(maybe based on your bandwidth somehow?).  We can set the quality outselves in the settings of this plugin
                playpath = playpath.replace('Adaptive_05','Adaptive_0' + str(vidquality))
                playpath = playpath.replace('Adaptive_04','Adaptive_0' + str(vidquality))
                playpath = playpath.replace('Adaptive_03','Adaptive_0' + str(vidquality))
                playpath = playpath.replace('Adaptive_02','Adaptive_0' + str(vidquality))
                playpath = playpath.replace('Adaptive_01','Adaptive_0' + str(vidquality))
                url = firstpart + secondpart[0] + playpath
        return self.plugin.set_stream_url(url)


    def action_play_ondemand(self):
        # this section is for the "on demand" games.  As of creating this plugin (version 0.1.2) there is only
        # hockey canada games on demand, cfl games on demand, and curling matches on demand
        url = self.args['remote_url']
        clipid = str(self.args['clip_id'])

        logging.debug('play_ondemand: %s' % url)
        logging.debug('clip: %s' % clipid)

        data = self.plugin.fetch(url, max_age=self.cache_timeout)

        tree = ET.parse(data)
        root = tree.getroot()

        for menuitem in root.findall('channel/item'):
            allclipids = menuitem.find('id').text
            logging.debug(allclipids)

            if allclipids == clipid:
                for cliplist in menuitem.findall('clipList/item'):
                    clipid = cliplist.find('id').text
                    title = cliplist.find('title').text
                    description = cliplist.find('description').text
                    image = cliplist.find('imgUrl').text

                    data = {}
                    #data.update(self.args)
                    data.update({
                        'Title': title,
                        'action': 'play_clip',
                        'clip_id': clipid,
                        'channel': self.short_name,
                        'Thumb': image,
                        'Plot': description
                    })
                    logging.debug(data)

                    self.plugin.add_list_item(data, is_folder=False)
                break
        self.plugin.end_list()


    def action_browse_channel(self):
        numclips = self.plugin.get_setting('numclips')
        numclips = (int(numclips) + 1) * 10

        url = self.args['remote_url'] + '&pageSize=' + str(numclips)
        logging.debug('browse_channel: %s' % url)

        data = self.plugin.fetch(url, max_age=self.cache_timeout)

        tree = ET.parse(data)
        root = tree.getroot()

        for menuitem in root.findall('channel/item'):
            title = menuitem.find('title').text
            description = menuitem.find('description').text
            image = menuitem.find('imgUrl').text
            clipid = menuitem.find('id').text
            vidtype = menuitem.find('type').text

            if (vidtype == 'video'):
                action = 'play_ondemand'
            else:
                action = 'play_clip'

            data = {}
            data.update(self.args)
            data.update({
                'Title': title,
                'action': action,
                'clip_id': clipid,
                'channel': self.short_name,
                'Thumb': image,
                'Plot': description
            })
            self.plugin.add_list_item(data, is_folder=(vidtype == 'video'))
        self.plugin.end_list()

    # recursive category builder (NHL, NFL, etc)
    def get_categories(self, item, title):
        children = item.findall('item')

        for child in children:
            t = child.find('text').text
            separator = '-' if len(title) > 0 else ''
            name = title + separator + t

            if (self.get_categories(child, name)):
                url = child.find('urlLatest').text

                data = {}
                data.update(self.args)
                data.update({
                    'Title': name.decode('unicode_escape'),
                    'action': 'browse_channel',
                    'remote_url': url,
                    'channel': self.short_name,
                })
                self.plugin.add_list_item(data)

        return len(children) == 0 # has children?

    def action_root(self):
        url = 'http://www.tsn.ca/config/videoHubMenu.xml'
        data = self.plugin.fetch(url, max_age=self.cache_timeout)

        tree = ET.parse(data)
        root = tree.getroot()

        # build categories list
        self.get_categories(root, '')
        self.plugin.end_list()
