from tweepy import OAuthHandler, API, Cursor, TweepError
from pathlib import Path
import pickle


def twitter_connect():
    p = Path('keys.txt')
    keys = p.read_text().split('\n')
    consumer_key = keys[0]
    consumer_secret = keys[1]
    access_token = keys[2]
    access_token_secret = keys[3]

    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = API(auth, wait_on_rate_limit=False)

    # test authentication
    try:
        api.verify_credentials()
        # print("Authentication OK")
    except TweepError:
        # print("Error during authentication")
        return None

    return api


# def tweet_search(api, city, number_of_tweets, keyword='', language='sv'):
#     geocodes = {"göteborg": "57.71085,11.98261,20km",
#                 "kiruna": "67.84779,20.24009,20km",
#                 "malmö": "55.60984,13.00267,20km",
#                 "stockholm": "59.33100,18.06441,30km",
#                 "uppsala": "59.85829,17.64660,20km",
#                 "västerås": "59.60745,16.55205,20km",
#                 "östersund": "63.16976,14.66004,20km",
#                 "": ""}
#
#     tweets = []
#     for idx, tweet in enumerate(Cursor(api.search,
#                                        q=f'{keyword} -filter:retweets',
#                                        result_type='recent',
#                                        geocode=geocodes[city.lower()],
#                                        lang=language,
#                                        count=100,
#                                        tweet_mode='extended').items(number_of_tweets)):
#         tweets.append(tweet.full_text)
#         print(idx, tweet.full_text)
#     return tweets


# TODO For sprint 1
# twitter_api = twitter_connect()
# tweets = tweet_search(twitter_api, 'västerås', 1000)
# with open("fallback-tweets/tweets_vasteras.p", "wb") as f:
#     pickle.dump(tweets, f)

# twitter_api = twitter_connect()
# tweets = tweet_search(api=twitter_api, city="", keyword="Puppies", number_of_tweets=1000, language='en')
# with open("fallback-tweets/tweets_puppies.p", "wb") as f:
#     pickle.dump(tweets, f)
