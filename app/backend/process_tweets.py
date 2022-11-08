import pandas as pd 

def read_csv_file(input_path: str):
    df = pd.read_csv(input_path) 
    print(df)

def punctuation():
    pass 

read_csv_file("unprocessed_tweets.csv")