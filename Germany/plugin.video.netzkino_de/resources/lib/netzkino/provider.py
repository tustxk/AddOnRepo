from resources.lib.kodion.items import DirectoryItem, VideoItem

__author__ = 'bromix'

from resources.lib import kodion
from resources.lib.kodion import constants, iso8601
from resources.lib.kodion.utils import FunctionCache, build_in_functions


class Provider(kodion.AbstractProvider):
    def __init__(self):
        kodion.AbstractProvider.__init__(self)

        from . import Client

        self._client = Client()
        pass

    def _create_video_item_from_post(self, post, context):
        def _read_custom_fields(_post, field_name):
            custom_fields = post.get('custom_fields', {})
            field = custom_fields.get(field_name, [])
            if len(field) >= 1:
                return field[0]
            return u''

        stream_id = _read_custom_fields(post, 'Streaming')
        movie_item = VideoItem(post['title'],
                               context.create_uri('play', {'stream_id': stream_id}),
                               image=post['thumbnail'])

        # stars
        stars = _read_custom_fields(post, 'Stars')
        if stars:
            stars = stars.split(',')
            for star in stars:
                movie_item.add_cast(star.strip())
                pass
            pass

        # director
        director = _read_custom_fields(post, 'Regisseur')
        if director:
            movie_item.set_director(director.strip())
            pass

        # imdb
        imdb = _read_custom_fields(post, 'IMDb-Link')
        if imdb:
            movie_item.set_imdb_id(imdb)
            pass

        # rating
        rating = _read_custom_fields(post, 'IMDb-Bewertung')
        if rating:
            rating = rating.replace(',', '.')
            movie_item.set_rating(rating)
            pass

        # year
        year = _read_custom_fields(post, 'Jahr')
        if year:
            # There was one case with '2006/2012' as a result. Therefore we split every year.
            year = year.split('/')[0]
            movie_item.set_year(year)
            pass

        # fanart
        movie_item.set_fanart(_read_custom_fields(post, 'featured_img_all'))

        # plot
        plot = kodion.utils.strip_html_from_text(post['content'])
        movie_item.set_plot(plot)

        # date added - in this case date modified (why?!?!)
        date = iso8601.parse(post['modified'])
        movie_item.set_date(date.year, date.month, date.day)

        # context menu
        ctx_menu = [(context.localize(constants.localize.WATCH_LATER_ADD),
                    build_in_functions.run_plugin_add_to_watch_later(context, movie_item))]
        movie_item.set_context_menu(ctx_menu)
        return movie_item

    def _set_content_and_sort(self, context):
        context.set_content_type(constants.content_type.MOVIES)
        context.add_sort_method(constants.sort_method.LABEL_IGNORE_THE,
                                constants.sort_method.VIDEO_YEAR,
                                constants.sort_method.VIDEO_RATING,
                                constants.sort_method.DATE)
        pass

    def on_search(self, search_text, context, re_match):
        self._set_content_and_sort(context)

        result = []

        json_data = context.get_function_cache().get(FunctionCache.ONE_MINUTE, self._client.search, search_text)
        posts = json_data['posts']
        for post in posts:
            result.append(self._create_video_item_from_post(post, context))
            pass

        return result, {self.RESULT_CACHE_TO_DISC: False}

    def on_watch_later(self, context, re_match):
        self._set_content_and_sort(context)
        pass

    @kodion.RegisterProviderPath('^/play/?$')
    def _on_play(self, context, re_match):
        params = context.get_params()
        stream_id = params['stream_id']

        stream_url = self._client.get_video_url(stream_id)
        movie_item = VideoItem(stream_id,
                               stream_url)
        return movie_item

    @kodion.RegisterProviderPath('^/category/(?P<categoryid>\d+)/?$')
    def _on_category(self, context, re_match):
        self._set_content_and_sort(context)

        result = []
        category_id = re_match.group('categoryid')

        json_data = context.get_function_cache().get(FunctionCache.ONE_DAY, self._client.get_category_content,
                                                     category_id)
        posts = json_data['posts']
        for post in posts:
            result.append(self._create_video_item_from_post(post, context))
            pass

        return result

    def on_root(self, context, re_match):
        result = []

        # watch later
        if len(context.get_watch_later_list().list()) > 0:
            watch_later_item = DirectoryItem('[B]' + context.localize(constants.localize.WATCH_LATER) + '[/B]',
                                             context.create_uri([constants.paths.WATCH_LATER, 'list']),
                                             image=context.create_resource_path('media', 'watch_later.png'))
            watch_later_item.set_fanart(self.get_fanart(context))
            result.append(watch_later_item)
            pass

        # search
        search_item = DirectoryItem('[B]' + context.localize(constants.localize.SEARCH) + '[/B]',
                                    context.create_uri([constants.paths.SEARCH, 'list']),
                                    image=context.create_resource_path('media', 'search.png')
        )
        search_item.set_fanart(self.get_fanart(context))
        result.append(search_item)

        # "Neu bei Netzkino"
        category_id = '81'
        image = 'http://dyn.netzkino.de/wp-content/themes/netzkino/imgs/categories/%s.png' % category_id
        category_item = DirectoryItem(u'[B]Neu bei Netzkino[/B]',
                                      context.create_uri(['category', category_id]),
                                      image=image)
        category_item.set_fanart(self.get_fanart(context))
        result.append(category_item)

        # categories
        categories = context.get_function_cache().get(FunctionCache.ONE_DAY, self._client.get_categories)
        for category in categories:
            category_id = str(category['id'])
            image = 'http://dyn.netzkino.de/wp-content/themes/netzkino/imgs/categories/%s.png' % category_id
            category_item = DirectoryItem(category['title'],
                                          context.create_uri(['category', category_id]),
                                          image=image)
            category_item.set_fanart(self.get_fanart(context))
            result.append(category_item)
            pass

        return result, {self.RESULT_CACHE_TO_DISC: False}

    def get_alternative_fanart(self, context):
        return self.get_fanart(context)

    def get_fanart(self, context):
        return context.create_resource_path('media', 'fanart.jpg')

    pass