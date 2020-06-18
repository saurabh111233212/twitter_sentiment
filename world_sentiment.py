import tweepy
from textblob import TextBlob
import preprocessor as p
import statistics
from typing import List

api_key = "JwqA8hwrCXN9rMWu4RNxDNydB"
api_secret_key = "b00hrPqTjhggFmRDPRBeRculAKW3CJdFpEh6DU4ZdZQ59EcXI8"

auth = tweepy.AppAuthHandler(api_key, api_secret_key)
api = tweepy.API(auth)

def get_tweets(keyword: str) -> List[str]:
    all_tweets = []
    for tweet in tweepy.Cursor(api.search, q=keyword, tweet_mode='extended', lang='en').items(10):
        all_tweets.append(tweet.full_text)
    return all_tweets


def clean_tweet(all_tweets: List[str]) -> List[str]:
    tweets_clean = []
    for tweet in all_tweets:
        tweets_clean.append(p.clean(tweet))
    return tweets_clean


def get_sentiment(clean_tweets: List[str]) -> List[float]:
    sentiment_scores = []
    for tweet in clean_tweets:
        blob = TextBlob(tweet)
        sentiment_scores.append(blob.sentiment.polarity)
    return sentiment_scores


def generate_average_sentiment_score(keyword : str) -> int :
    tweets = get_tweets(keyword)
    tweets_clean = clean_tweet(tweets)
    sentiment_scores = get_sentiment(tweets_clean)
    average_score = statistics.mean(sentiment_scores);
    return average_score


if __name__ == "__main__":
    print("Which does twitter prefer?")
    word1 = input()
    print("--or--")
    word2 = input()
    print('\n')
    first_score = generate_average_sentiment_score(word1)
    second_score = generate_average_sentiment_score(word2)
    preferred_word = "";
    if (first_score > second_score) :
        preferred_word = word1
        loser = word2
    else :
        preferred_word = word2
        loser = word1
    print('Looks like people prefer ' + preferred_word + ' to ' + loser)