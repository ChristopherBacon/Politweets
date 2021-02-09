"""
Politweets Python Project
Using Twitter API to scrape tweets then sentiment analysis with Textblob, finally present using Streamlit
This is the twitter api data scrape
"""

import tweepy
import webbrowser
import time
import pandas as pd
import numpy as np
from twitter_handles_list import new_handles_list
import os


def twitter_api_access():
    """access twitter api, have already used the hashed below to obtain keys"""
    consumer_key = os.environ.get('TWTR_CK')
    consumer_secret = os.environ.get('TWTR_CS')
    key = os.environ.get('TWTR_K')
    secret = os.environ.get('TWTR_S')
    # callback_uri = 'oob'
    # auth = tweepy.OAuthHandler(consumer_key, consumer_secret, callback_uri)
    # redirect_url = auth.get_authorization_url()
    # webbrowser.open(redirect_url)
    # user_pint_input = input("What's the pin value? ")
    # auth.get_access_token(user_pint_input)
    # print(auth.access_token, auth.access_token_secret)
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(key, secret)
    api = tweepy.API(auth)
    return api


def get_twitter_data(api):
    """scrape twitter using the mp list"""
    api_data = []
    for handle in new_handles_list:
        try:
            timeline = api.user_timeline(screen_name=handle, count=20)
            tweet_data = {}
            for status in timeline:
                tweet_data['name'] = status.user.name
                tweet_data['screen_name'] = status.user.screen_name
                tweet_data['description'] = status.user.description
                tweet_data['created_date'] = status.created_at
                tweet_data['tweet'] = status.text
                tweet_data['retweet_count'] = status.retweet_count
                tweet_data['favourite_count'] = status.favorite_count
                api_data.append(tweet_data)
                tweet_data = {}
        except tweepy.TweepError:
            print(f"Failed to run the command on {handle}, Skipping...")
    return api_data


def save_twitter_data(data):
    """take the scraped data and save it"""
    politweets = pd.DataFrame(data)
    politweets.to_csv('politweets.csv')

def main():
    print('Connecting to api')
    api = twitter_api_access()
    print('scraping data')
    data = get_twitter_data(api)
    print('saving data')
    save_twitter_data(data)
    print('finishing')


if __name__ == "__main__":
    main()


