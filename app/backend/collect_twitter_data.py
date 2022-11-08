import os 
import tweepy
import json
import pandas as pd 
from dotenv import load_dotenv
from typing import List


def auth():
    load_dotenv()
    consumer_key = os.getenv("API_KEY")
    consumer_secret = os.getenv("API_KEY_SECRETS")
    access_token = os.getenv("ACCESS_TOKEN")
    access_token_secret = os.getenv("ACCESS_TOKEN_SECRETS")

    auth = tweepy.OAuth1UserHandler(
        consumer_key,
        consumer_secret,
        access_token, 
        access_token_secret
    )
    return auth 

def get_tweets_from_api(auth, keyword: str, num_of_tweets_per_page: int, num_of_pages: int) -> List:
    api = tweepy.API(auth)
    extracted_page = []
    for page in tweepy.Cursor(api.search_tweets, keyword, lang="en", 
                count=num_of_tweets_per_page).pages(num_of_pages):
        extracted_page.append(page)

    extracted_tweets_from_pages = []
    for page in extracted_page:
        extracted_tweets_from_pages += page
    return extracted_tweets_from_pages

def prune_tweet_data(tweepy_status_tweets: List) -> List[List]:
    pruned_tweet_data = []
    for tweet_status_tweet in tweepy_status_tweets:
        tweet_json = json.dumps(tweet_status_tweet._json)
        tweet_data = json.loads(tweet_json)
        pruned_tweet_data.append([tweet_data['user']['screen_name'], tweet_data['text'], 
        tweet_data['created_at'], tweet_data['retweet_count'], tweet_data['favorite_count']])
    return pruned_tweet_data

def convert_pruned_tweet_data_to_pandas(pruned_tweet_data: List[List], headers: List):
    df = pd.DataFrame(pruned_tweet_data, columns=headers)
    return df 
     

def convert_pandas_to_csv(df, output_path: str) -> None:
    df.to_csv(output_path, index=False) 

def main():
    authentication = auth()
    keyword, tweets_per_page, pages = "NBA Youngboy", 20, 5
    tweepy_status_tweets = get_tweets_from_api(authentication, keyword, tweets_per_page, pages)
    pruned_tweet_data = prune_tweet_data(tweepy_status_tweets)
    df = convert_pruned_tweet_data_to_pandas(pruned_tweet_data, ["username", "tweet_text", "created_at", "retweet_count", "favorite_count"])
    convert_pandas_to_csv(df, "unprocessed_tweets.csv")