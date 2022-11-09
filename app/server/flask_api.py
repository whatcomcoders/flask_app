import sys 
sys.path.append("..")

import json 

import collections
import collections.abc
collections.Iterable = collections.abc.Iterable

from flask import Flask 
from flask_cors import CORS, cross_origin 
from backend import auth, get_tweets_from_api, prune_tweet_data, convert_pruned_tweet_data_to_pandas


api = Flask(__name__)
api.config['CORS_HEADERS'] = 'Content-Type'
cors = CORS(api)

@api.route('/')
@cross_origin()
def main():
    auth()

@api.route('/collect_data')
@cross_origin()
def get_twitter_data():
    auth_details = auth()
    print(auth_details)
    tweets = get_tweets_from_api(auth_details, "youngboy", 1, 1)

    responses = {}
    for i, tweet in enumerate(tweets):
        tweet_json = json.dumps(tweet._json)
        responses["tweet: " + str(i)] = tweet_json
    return responses

@api.route('/data_to_csv')
@cross_origin()
def data_to_csv():
    auth_details = auth()
    tweets = get_tweets_from_api(auth_details, "youngboy", 1, 1)
    prune_tweet = prune_tweet_data(tweets)
    df = convert_pruned_tweet_data_to_pandas(prune_tweet, ["username", "tweet_text", "created_at", "retweet_count", "favorite_count"])
    df.to_csv("output.csv", index=False)



if __name__=='__main__':
    api.run(host='localhost', port=8080)