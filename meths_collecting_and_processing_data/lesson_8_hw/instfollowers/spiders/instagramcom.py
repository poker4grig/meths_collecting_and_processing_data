import json
import re
from urllib.parse import urlencode
from copy import deepcopy

import scrapy
from scrapy.http import HtmlResponse
from lesson_8_hw.instfollowers.items import InstfollowersItem


class InstagramcomSpider(scrapy.Spider):
    name = 'instagramcom'
    allowed_domains = ['instagram.com']
    start_urls = ['https://www.instagram.com/']
    inst_login_link = 'https://www.instagram.com/accounts/login/ajax/'
    inst_login = 'Onliskill_udm'
    inst_passwd = '#PWD_INSTAGRAM_BROWSER:10:1651766168:Af1QAEPVT2wMo5ZoBmtI9yaUUSRZ7N2mmqws6aHcVluAGOhHqcHqbcu0wuClcnfkLzdE/wJs5EBFd472ZfAHj83FvVddlWg+HfWctat5Fgiv/q2381qqkGAA7M/6AoWAgqJ8U7sxZhP9Yaijd98='
    parse_users = ['poker4grig', 'vsy_ksy']
    inst_friendships_link = 'https://i.instagram.com/api/v1/friendships'

    def parse(self, response: HtmlResponse, **kwargs):
        csrf = self.fetch_csrf_token(response.text)
        yield scrapy.FormRequest(
            self.inst_login_link,
            method='POST',
            callback=self.login,
            formdata={
                'username': self.inst_login,
                'enc_password': self.inst_passwd},
            headers={'X-CSRFToken': csrf}
        )

    def login(self, response: HtmlResponse):
        print()
        j_body = response.json()
        if j_body.get('authenticated'):
            for user in self.parse_users:
                yield response.follow(
                    f'/{user}',
                    callback=self.user_data_parse,
                    cb_kwargs={'username': user}
                )

    def user_data_parse(self, response: HtmlResponse, username):
        user_id = self.fetch_user_id(response.text, username)
        variables = {'count': 12}
        url_followers = f'{self.inst_friendships_link}/{user_id}/followers/?{urlencode(variables)}&search_surface=follow_list_page'
        yield response.follow(url_followers,
                              callback=self.user_followers_parse,
                              cb_kwargs={'username': username,
                                         'user_id': user_id,
                                         'variables': deepcopy(variables)},
                              headers={
                                  'User-Agent': 'Instagram 155.0.0.37.107'})

        url_followings = f'{self.inst_friendships_link}/{user_id}/followings/?{urlencode(variables)}&search_surface=follow_list_page'
        yield response.follow(url_followings,
                              callback=self.user_followings_parse,
                              cb_kwargs={'username': username,
                                         'user_id': user_id,
                                         'variables': deepcopy(variables)},
                              headers={'User-Agent': 'Instagram 155.0.0.37.107'})

    def user_followers_parse(self, response: HtmlResponse, username, user_id, variables):
        j_data = response.json()
        if j_data.get('next_max_id'):
            variables['max_id'] = j_data.get('next_max_id')
            url_posts = f'{self.inst_friendships_link}/{user_id}/followers/?{urlencode(variables)}&search_surface=follow_list_page'
            yield response.follow(url_posts,
                                  callback=self.user_followers_parse,
                                  cb_kwargs={'username': username,
                                             'user_id': user_id,
                                             'variables': deepcopy(variables)},
                                  headers={'User-Agent': 'Instagram 155.0.0.37.107'})

        followers = j_data.get('users')
        for follower in followers:
            item = InstfollowersItem(
                user_id=follower.get('pk'),
                username=follower.get('username'),
                fullname=follower.get('full_name'),
                photo=follower.get('profile_pic_url'),
                post_data=follower)
            yield item

    def user_followings_parse(self, response: HtmlResponse, username, user_id, variables):
        j_data = response.json()
        if j_data.get('next_max_id'):
            variables['max_id'] = j_data.get('next_max_id')
            url_followings = f'{self.inst_friendships_link}/{user_id}/followings/?{urlencode(variables)}&search_surface=follow_list_page'
            yield response.follow(url_followings,
                                  callback=self.user_following_parse,
                                  cb_kwargs={'username': username,
                                             'user_id': user_id,
                                             'variables': deepcopy(variables)},
                                  headers={'User-Agent': 'Instagram 155.0.0.37.107'})
        followings = j_data.get('users')
        for following in followings:
            item = InstfollowersItem(
                user_id=following.get('pk'),
                username=following.get('username'),
                fullname=following.get('full_name'),
                photo=following.get('profile_pic_url'),
                post_data=following)

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
