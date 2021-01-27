import pickle
from twitter.twitter_connect import twitter_connect
from tweepy import Cursor
import warnings

geocodes = {"göteborg": "57.71085,11.98261,20km",
            "kiruna": "67.84779,20.24009,20km",
            "malmö": "55.60984,13.00267,20km",
            "stockholm": "59.33100,18.06441,30km",
            "uppsala": "59.85829,17.64660,20km",
            "västerås": "59.60745,16.55205,20km",
            "östersund": "63.16976,14.66004,20km",
            "": ""}


def twitter_search(city='', keyword='', language='swedish'):
    """ Search Twitter for English or Swedish tweets made from a specific city that contain a keyword
        specified by the user. Return an empty list if it is not possible to retrieve tweets live. """

    api = twitter_connect()

    if language == "english":
        language = 'en'
    elif language == "swedish":
        language = 'sv'

    tweets = []
    try:
        for idx, tweet in enumerate(Cursor(api.search,
                                           q=f'{keyword} -filter:retweets',
                                           result_type='recent',
                                           geocode=geocodes[city.lower()],
                                           lang=language,
                                           count=100,
                                           tweet_mode='extended').items(250)):
            tweets.append(tweet.full_text)
            #print(idx, tweet.full_text)
    except:
        return None
    return tweets


def load_tweets_from_file(file_name='', file_path=''):
    """ Load pickled tweets from file and return tweets as a list. The pickled files must be placed
    in a directory called fallback-tweets and be named tweets_city.p"""

    try:
        with open(f"{file_path}/{file_name}", "rb") as f:
            tweets = pickle.load(f)
            return tweets
    except FileNotFoundError:
        return []


def get_tweets(city='', keyword='', language='swedish', load_from_file=True, live=False, file_name='', file_path=''):
    """ If it is a live run - try to retrieve tweets live. If it is not possible,
    load fallback tweets. If it is a test run - load tweets from file and avoid Twitter rate limit exceeded. """

    if live:
        tweets = twitter_search(city=city, keyword=keyword, language=language)
        warnings.filterwarnings("ignore")
        if not tweets:
            # For sentiment analysis - if not possible to retrieve live - do not try to load from file during live run
            if not load_from_file:
                return tweets  # Can be None or []. None - if not possible to get tweets live, [] - if no tweets found
            try:
                tweets = load_tweets_from_file(file_name=file_name, file_path=file_path)
            except:
                return None

    else:
        tweets = load_tweets_from_file(file_name=file_name, file_path=file_path)
        # For test run and debugging
        if not tweets:
            tweets = twitter_search(city=city, keyword=keyword, language=language)
            if tweets:
                pickle.dump(tweets, open(f'{file_path}/{file_name}', 'wb'))
                print("Saved pickle")
            else:
                return None
    return tweets
