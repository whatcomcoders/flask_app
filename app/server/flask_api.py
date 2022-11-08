import sys 
sys.path.append("..")

import json 

import collections
import collections.abc
collections.Iterable = collections.abc.Iterable

from flask import Flask 
from flask_cors import CORS, cross_origin 
from backend import auth, get_tweets_from_api

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
    tweets = get_tweets_from_api(auth_details, "youngboy", 1, 1)
    print(tweets)

    responses = {}
    for i, tweet in enumerate(tweets):
        tweet_json = json.dumps(tweet._json)
        responses["tweet: " + str(i)] = tweet_json
    return responses


if __name__=='__main__':
    api.run(host='localhost', port=8080)