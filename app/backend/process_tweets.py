import preprocessor as p
import nltk 
from nltk import word_tokenize, FreqDist
from nltk.corpus import stopwords
from nltk.tokenize import TweetTokenizer
import pandas as pd 
import re 

from typing import List, Dict

tweetTokenizer = TweetTokenizer()
stopwords_set = set(stopwords.words('english'))

def read_csv_file(input_path: str):
    return pd.read_csv(input_path) 

#todo - add a flag to trigger this function
def download_nltk_modules(download_flag: bool) -> None:
    if download_flag:
        nltk.download()
        nltk.download('wordnet')
        nltk.download('stopwords')

def extract_hashtags(tweet):
    extracted_hashtags = re.findall(r"#(\w+)", tweet)
    if extracted_hashtags:
        print(extracted_hashtags)
    return extracted_hashtags

def extract_hyperlinks(tweet):
    extracted_hyperlinks = re.findall(r'https?:\/\/.*[\r\n]*', tweet) 
    return extracted_hyperlinks

def extract_retweets(tweet):
    extracted_retweets = re.findall(r'^RT[\s]+', tweet)
    return extracted_retweets 

def clean_tweets(tweet):
    clean_tweet = p.clean(tweet)
    return clean_tweet


def standardize_casing(tweet):
    tweet = tweet.lower() 
    return tweet

def remove_punctuation(tweets: List):
    new_words = []
    for word in tweets:
        new_word = re.sub(r'[^\w\s]', '', (word))
        if new_word != '':
            new_words.append(new_word)
    return new_words 

def twitter_tokenizer(tweet):
    return [word for word in tweetTokenizer.tokenize(tweet)]


def remove_stopwords(stopwords_set, tweet):
    return [word for word in tweet if word not in stopwords_set]

def run_pipeline(df, output_path=None):
    df['hashtags'] = df['tweet_text'].apply(extract_hashtags)
    df['hyperlinks'] = df['tweet_text'].apply(extract_hyperlinks)
    df['retweets'] = df['tweet_text'].apply(extract_retweets)

    df['clean_tweet'] = df['tweet_text'].apply(clean_tweets)
    df['clean_tweet'] = df['clean_tweet'].apply(standardize_casing)
    
    df['tokenized_tweet'] = df['clean_tweet'].apply(twitter_tokenizer)

    df['clean_tokenized_tweet'] = df['tokenized_tweet'].apply(remove_punctuation)
    df['clean_tokenized_tweet'] = df['clean_tokenized_tweet'].apply(lambda tweet: [word for word in tweet if word not in stopwords_set])

    if output_path:
        df.to_csv(output_path, index=False)
    
PATH_TO_TWEETS_CSV = "unprocessed_tweets.csv"
DOWNLOAD_FLAG = False 
OUTPUT_PATH = "processed_tweets.csv"

download_nltk_modules(DOWNLOAD_FLAG)

df = read_csv_file(PATH_TO_TWEETS_CSV)
run_pipeline(df, OUTPUT_PATH)

