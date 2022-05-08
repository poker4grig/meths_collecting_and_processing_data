import json
import re
from urllib.parse import urlencode
from copy import deepcopy
import scrapy
from scrapy.http import HtmlResponse
from lesson_8_inst_study.instagram.items import InstagramItem


class InstagramstudySpider(scrapy.Spider):
    name = 'instagramStudy'
    allowed_domains = ['instagram.com']
    start_urls = ['https://www.instagram.com/']
    inst_login_link = 'https://www.instagram.com/accounts/login/ajax/'
    inst_login = 'Onliskill_udm'
    inst_passwd = '#PWD_INSTAGRAM_BROWSER:10:1651766168:Af1QAEPVT2wMo5ZoBmtI9yaUUSRZ7N2mmqws6aHcVluAGOhHqcHqbcu0wuClcnfkLzdE/wJs5EBFd472ZfAHj83FvVddlWg+HfWctat5Fgiv/q2381qqkGAA7M/6AoWAgqJ8U7sxZhP9Yaijd98='
    parse_user = 'polina.s.s'
    inst_graphql_link = 'https://www.instagram.com/graphql/query/?'
    posts_hash = '69cba40317214236af40e7efa697781d'
    followers = 'https://i.instagram.com/api/v1/friendships/549181358/followers/'

    def parse(self, response: HtmlResponse, **kwargs):
        csrf = self.fetch_csrf_token(response.text)
        yield scrapy.FormRequest(
            self.inst_login_link,
            method='POST',
            callback=self.login,
            formdata={'username': self.inst_login,
                      'enc_password': self.inst_passwd},
            headers={'X-CSRFToken': csrf}
        )

    def login(self, response: HtmlResponse):
        print()
        j_body = response.json()
        if j_body.get('authenticated'):
            yield response.follow(
                f'/{self.parse_user}',
                callback=self.user_data_parse,
                cb_kwargs={'username': self.parse_user}
            )

    def user_data_parse(self, response: HtmlResponse, username):
        user_id = self.fetch_user_id(response.text, username)
        variables = {'id': user_id,
                     'first': 12}
        url_posts = f'{self.inst_graphql_link}query_hash={self.posts_hash}&{urlencode(variables)}'
        yield response.follow(url_posts,
                              callback=self.user_post_parse,
                              cb_kwargs={'username': username,
                                         'user_id': user_id,
                                         'variables': deepcopy(variables)})

    def user_post_parse(self, response: HtmlResponse, username, user_id, variables):
        j_data = response.json()
        page_info = j_data.get('data').get('user').get('edge_owner_to_timeline_media').get('page_info')
        if page_info.get('has_next_page'):
            variables['after'] = page_info.get('end_cursor')
            url_posts = f'{self.inst_graphql_link}query_hash={self.posts_hash}&{urlencode(variables)}'
            yield response.follow(url_posts,
                                  callback=self.user_post_parse,
                                  cb_kwargs={'username': username,
                                             'user_id': user_id,
                                             'variables': deepcopy(variables)},
                                  headers={'User-Agent': 'Instagram 155.0.0.37.107'})

        posts = j_data.get('data').get('user').get('edge_owner_to_timeline_media').get('edges')
        for post in posts:
            item = InstagramItem(
                user_id=user_id,
                username=username,
                photo=post.get('node').get('display_url'),
                likes=post.get('node').get('edge_media_preview_like').get('count'),
                post_data=post.get('node')
            )
            yield item

    def user_followers_parse(self, response: HtmlResponse, username, user_id, variables):
        print()
        j_data = response.json()
        page_info = j_data.get('data').get('user').get(
            'edge_owner_to_timeline_media').get('page_info')
        if page_info.get('has_next_page'):
            variables['after'] = page_info.get('end_cursor')
            url_posts = f'{self.inst_graphql_link}query_hash={self.posts_hash}&{urlencode(variables)}'
            yield response.follow(url_posts,
                                  callback=self.user_post_parse,
                                  cb_kwargs={'username': username,
                                             'user_id': user_id,
                                             'variables': deepcopy(variables)},
                                  headers={
                                      'User-Agent': 'Instagram 155.0.0.37.107'})


    def fetch_csrf_token(self, text):
        """ Get csrf-token for auth """
        matched = re.search('\"csrf_token\":\"\\w+\"', text).group()
        return matched.split(':').pop().replace(r'"', '')

    def fetch_user_id(self, text, username):
        try:
            matched = re.search(
                '{\"id\":\"\\d+\",\"username\":\"%s\"}' % username, text
            ).group()
            return json.loads(matched).get('id')
        except:
            return re.findall('\"id\":\"\\d+\"', text)[-1].split('"')[-2]
