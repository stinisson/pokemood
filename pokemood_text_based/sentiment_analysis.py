"""
The player gets to search for a specific keyword in a chosen language (Swedish/English) and guess whether the
the 1000 most recent tweets associated with that keyword has a positive or negative sentiment.
If the player guess right, the active Pokemon gets rewarded an attack bonus. If the guess is wrong,
the pokemon gets punished and looses attack strength.
"""

from twitter_search import get_tweets
import textwrap

import nltk
from nltk.corpus import stopwords
#nltk.download("stopwords")
#nltk.download('punkt')
#nltk.download('vader_lexicon')

from nltk.sentiment.vader import SentimentIntensityAnalyzer as SentimentIntensityAnalyzerEnglish
from vaderSentimentSwedish.vaderSentimentSwedish import SentimentIntensityAnalyzerSwedish
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties


def wrap_text(text, width):
    new_text = "\n".join(textwrap.wrap(text, width))
    return new_text


def sentiment_analysis(keyword, language, file_name='', live=False):
    """ Perform sentiment analysis on Twitter data. Visualize the result as a bar graph and
        print the most positive and the most negative tweet on screen.
        If the negative sentiment is greater than the positive, return 'negative'.
        If the positive sentiment is greater than the negative return 'positive'.
        If the sentiment is equally positive and negative return 'neutral'.
        If something went wrong and it wasn't possible to retrieve tweets return None. """

    if file_name:
        load_from_file = True
    else:
        load_from_file = False

    tweets = get_tweets(keyword=keyword, language=language, load_from_file=load_from_file, live=live, file_name=file_name, file_path='demo-tweets')

    if tweets is None:
        return 'connection_error'
    if len(tweets) < 2:
        return 'too_few_results'

    tweet_blob = "\n\n".join(tweets)

    most_positive_tweet, most_negative_tweet = get_tweets_with_highest_sentiment_score(tweets, language)
    if len(most_positive_tweet) < 1 or len(most_negative_tweet) < 1:
        # Ugly fix - handle if all tweets have a compound score of 0. So not really too few results,
        # but due to time limitations - this will have to do. Future improvement - if all tweets have a compound
        # score of 0 - display the bar graph with one selected tweet and print - "all tweets are neutral".
        return 'too_few_results'

    sentiment_score = 0
    if language == "english":
        sentiment_score = SentimentIntensityAnalyzerEnglish().polarity_scores(tweet_blob)

        """ Run to demo how the sentiment is calculated """
        # sent = {'neg': 0, 'neu': 0, 'pos': 0, 'compound_pos': 0, 'compound_neg': 0}
        # number_of_tweets = 0
        # for idx, tweet in enumerate(tweets):
        #     sentiment_score = SentimentIntensityAnalyzerEnglish().polarity_scores(tweet)
        #     print("\n", idx,  tweet, str(sentiment_score))
        #     num += 1
        #     #print(sentiment_score)
        #     sent['neg'] += sentiment_score['neg']
        #     sent['neu'] += sentiment_score['neu']
        #     sent['pos'] += sentiment_score['pos']
        #     if sentiment_score['compound'] > 0:
        #         sent['compound_pos'] += sentiment_score['compound']
        #     elif sentiment_score['compound'] < 0:
        #         sent['compound_neg'] += sentiment_score['compound']
        # print("----")
        # print(sent)
        # print(number_of_tweets)

    elif language == "swedish":
        sentiment_score = SentimentIntensityAnalyzerSwedish().polarity_scores(tweet_blob)

    """ Visualize the result as a bar graph """
    negative_score = sentiment_score['neg']
    positive_score = sentiment_score['pos']
    score = [negative_score, positive_score]
    sentiment = ["Negativt", "Positivt"]

    plot1 = plt.subplot(211)
    plot1.set_xlabel("Sentiment")
    plot1.bar(sentiment, score, color=((0.8, 0.3, 0.3, 0.8), (0.3, 0.8, 0.3, 0.8)))
    plot1.set_title(f"Är folk på Twitter positivt eller negativt inställda till {keyword}?")

    plot2 = plt.subplot(212)
    plot2.axis('off')
    plot2.set_xlim(0, 1)
    plot2.set_ylim(0, 10)
    font = FontProperties()
    font.set_size('small')
    plot2.text(0, 6, f"Negativaste tweet:\n{wrap_text(most_negative_tweet, 150)}", fontproperties=font)
    plot2.text(0, 0, f"Positivaste tweet:\n{wrap_text(most_positive_tweet, 150)}", fontproperties=font)
    plt.show()

    if positive_score > negative_score:
        return "positivt"
    elif positive_score < negative_score:
        return "negativt"
    else:
        return "neutralt"


def get_tweets_with_highest_sentiment_score(tweets, language):
    """ Return the tweet with the highest positive sentiment score and the tweet with lowest negative score """

    most_pos = {'tweet': "", 'compound_score': 0}
    most_neg = {'tweet': "", 'compound_score': 0}
    sia = ""
    if language == "english":
        sia = SentimentIntensityAnalyzerEnglish()
    elif language == "swedish":
        sia = SentimentIntensityAnalyzerSwedish()

    for idx, tweet in enumerate(tweets):
        sentiment_score = sia.polarity_scores(tweet)
        #print("\n", idx, tweet, str(sentiment_score))

        if sentiment_score['compound'] > most_pos['compound_score']:
            most_pos['compound_score'] = sentiment_score['compound']
            most_pos['tweet'] = tweet
        if sentiment_score['compound'] < most_neg['compound_score']:
            most_neg['compound_score'] = sentiment_score['compound']
            most_neg['tweet'] = tweet

    return most_pos['tweet'], most_neg['tweet']


if __name__ == '__main__':
    sentiment_analysis(keyword="covid", language="english", file_name='demo_tweets_english_covid.p', live=False)
