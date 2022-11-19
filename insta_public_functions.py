# -*- coding: utf-8 -*-
"""
Created on Aug 5 2021
@author: Gal Vekselman
"""

import instaloader
from datetime import date
import pandas as pd
import os
from pathlib import Path


class GetInstagramProfile():
    def __init__(self) -> None:
        self.L = instaloader.Instaloader()

    def scrape_users_post_likes(self, user_name, un, psw):
        '''Note: login required to get a profile's followers.'''
        self.L.login(un, psw)
        profile = instaloader.Profile.from_username(self.L.context, user_name)

        '''Build: Folder structure for follower and followees'''
        today = date.today()
        year = today.strftime("%Y")
        month = today.strftime("%m")
        day = today.strftime("%d")
        directory_post = "Instagram\Data\posts\{y}\{m}\{d}".format(y=year, m=month, d=day)
        directory_posts = "Instagram\Data\posts_likes\{y}\{m}\{d}".format(y=year, m=month, d=day)
        Path(directory_post).mkdir(parents=True, exist_ok=True)
        Path(directory_posts).mkdir(parents=True, exist_ok=True)

        '''Scrape: post'''
        postsdf = pd.DataFrame(columns=['post_url'
            , 'caption'
            , 'shortcode'
            , 'mediaid'
            , 'title'
            , 'date_local'
            , 'typename'
            , 'mediacount'
            , 'caption_hashtags'
            , 'caption_mentions'
            , 'tagged_users'
            , 'likes'
            , 'comments'
                                        ])

        '''Scrape: post likes'''
        fdf = pd.DataFrame(columns=['shortcode'
            , 'liker_username'
                                    ])

        for post in profile.get_posts():
            post_url = post.url
            post_caption = post.caption
            post_shortcode = post.shortcode
            post_mediaid = post.mediaid
            post_title = post.title
            post_date_time = post.date_local
            post_typename = post.typename
            post_mediacount = post.mediacount
            post_caption_hashtags = post.caption_hashtags
            post_caption_mentions = post.caption_mentions
            post_tagged_users = post.tagged_users
            post_likes = post.likes
            post_comments = post.comments
            postsdf.loc[len(postsdf.index)] = [post_url, post_caption, post_shortcode, post_mediaid, post_title,
                                               post_date_time, post_typename, post_mediacount, post_caption_hashtags,
                                               post_caption_mentions, post_tagged_users, post_likes, post_comments]
            for like in post.get_likes():
                like_full_name = like.username
                fdf.loc[len(fdf.index)] = [post_shortcode, like_full_name]
                print(like_full_name)

        postsdf.to_csv(os.path.join(directory_post, user_name + '.csv'))
        fdf.to_csv(os.path.join(directory_posts, user_name + '.csv'))

    def scrape_users_followers_followings(self, user_name, un, psw):
        '''Note: login required to get a profile's followers.'''
        self.L.login(un, psw)
        profile = instaloader.Profile.from_username(self.L.context, user_name)

        '''Build: Folder structure for follower and followees'''
        today = date.today()
        year = today.strftime("%Y")
        month = today.strftime("%m")
        day = today.strftime("%d")
        directory_followees = "Instagram\Data\Followees\{y}\{m}\{d}".format(y=year, m=month, d=day)
        directory_followers = "Instagram\Data\Followers\{y}\{m}\{d}".format(y=year, m=month, d=day)
        Path(directory_followees).mkdir(parents=True, exist_ok=True)
        Path(directory_followers).mkdir(parents=True, exist_ok=True)

        '''Scrape: followees'''
        fdf = pd.DataFrame(columns=['account_name'
            , 'followee_username'
            , 'followee_full_name'
                                    ])

        for followee in profile.get_followees():
            username = followee.username
            full_name = followee.full_name
            fdf.loc[len(fdf.index)] = [user_name, username, full_name]
            print(full_name)

        fdf.to_csv(os.path.join(directory_followees, user_name + '.csv'))

        '''Scrape: followers'''
        fldf = pd.DataFrame(columns=['account_name'
            , 'followers_username'
            , 'followers_full_name'
                                     ])

        for followers in profile.get_followers():
            username = followers.username
            full_name = followers.full_name
            fldf.loc[len(fldf.index)] = [user_name, username, full_name]

        fldf.to_csv(os.path.join(directory_followers, user_name + '.csv'))

    def scrape_users_info(self, user_name, un, psw):
        '''Note: login required to get a profile's followers.'''
        self.L.login(un, psw)
        profile = instaloader.Profile.from_username(self.L.context, user_name)

        '''Build: Folder structure for follower and followees'''
        today = date.today()
        year = today.strftime("%Y")
        month = today.strftime("%m")
        day = today.strftime("%d")
        directory_profile = "Instagram\Data\Profiles"
        Path(directory_profile).mkdir(parents=True, exist_ok=True)

        '''Scrape: followees'''
        fdf = pd.DataFrame(columns=['userid'
            , 'username'
            , 'full_name'
            , 'followers_count'
            , 'followees_count'
            , 'mediacount'
            , 'profile_pic_url'
            , 'is_private'
            , 'as_of_date'
                                    ])

        userid = profile.userid
        username = profile.username
        full_name = profile.full_name
        followers_count = profile.followers
        followees_count = profile.followees
        mediacount = profile.mediacount
        profile_pic_url = profile.profile_pic_url
        is_private = profile.is_private
        as_of_date = today.strftime("%d/%m/%Y")
        fdf.loc[len(fdf.index)] = [userid, username, full_name, followers_count, followees_count, mediacount,
                                   profile_pic_url, is_private, as_of_date]
        print(fdf)
        fdf.to_csv(os.path.join(directory_profile, user_name + '.csv'))

    def get_users_followers(self, user_name, un, psw):
        '''Note: login required to get a profile's followers.'''
        self.L.login(un, psw)
        #  directory_profile = "Data\Politician"
        profile = instaloader.Profile.from_username(self.L.context, user_name)
        fdf = pd.DataFrame(columns=['account_name'
            , 'followee_username'
            , 'followee_full_name'
                                    ])

        for followee in profile.get_followers():
            username = followee.username
            full_name = followee.full_name
            fdf.loc[len(fdf.index)] = [user_name, username, full_name]
            print(fdf)

        #  fdf.to_csv(os.path.join(directory_profile,user_name+'.csv'))
        return fdf

    def get_users_followings(self, user_name, un, psw):
        """Note: login required to get a profile's followings."""
        self.L.login(un, psw)
        profile = instaloader.Profile.from_username(self.L.context, user_name)
        fdf = pd.DataFrame(columns=['account_name'
            , 'followee_username'
            , 'followee_full_name'
                                    ])

        for followee in profile.get_followees():
            username = followee.username
            full_name = followee.full_name
            fdf.loc[len(fdf.index)] = [user_name, username, full_name]
            print(fdf)

        #  fdf.to_csv(os.path.join(directory_profile,user_name+'.csv'))
        return fdf


