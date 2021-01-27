"""
The player gets to search for a particular city and guess from a list of moods, which mood the inhabitants
in the city are in right now based on their twitter content.
If the player guess right, the Pokemon gets rewarded an attack bonus. If the guess is wrong,
the pokemon gets punished and looses attack strength.
"""

from twitter_search import get_tweets
import string
from pathlib import Path

# import nltk
# nltk.download("stopwords")
from nltk.corpus import stopwords

import matplotlib.pyplot as plt
import operator

text_emotions = {"arg": 0, "glad": 0, "ledsen": 0, "kärleksfull": 0}

def clean_tweets(tweets):
    """ Make tweets lowercase, remove punctuations, newlines and @username calls. Tokenize the tweet content. """

    # Characters to be removed from tweets
    tweet_punctuation = string.punctuation.replace('@', '') + '”' + '“'
    stop_words = stopwords.words("swedish")

    cleaned_tweets = []
    for tweet in tweets:
        tweet_lower = tweet.lower().replace('\n', ' ')
        table = tweet_lower.maketrans('', '', tweet_punctuation)
        cleaned_tweet = tweet_lower.translate(table)
        tokens = cleaned_tweet.split(' ')

        for token in tokens:
            if "https" in token or '@' in token or token in stop_words or len(token) < 1:
                # Exclude links, username calls in tweets and stopwords
                continue
            cleaned_tweets.append(token)

    return cleaned_tweets


def mood_analysis(city, live=False):

    city_lower = city.lower()
    file_name_city = city_lower.replace("å", "a").replace("ä", "a").replace("ö", "o")

    tweets = get_tweets(city=city, load_from_file=True, live=live, file_name=f'tweets_{file_name_city}.p', file_path='fallback-tweets')

    if not tweets:
        return None

    cleaned_tweets = clean_tweets(tweets)

    """ Read emotion categories and emotion words from file """
    try:
        p = Path('keywords/emotions.txt')
        file = p.read_text(encoding='utf8')
        file = file.split('\n')
        emotions = {}
        for line in file:
            clean_line = line.replace(',', '').replace("'", '').strip()
            emotion_category, emotion_word = clean_line.split(':')
            emotion_word = emotion_word.strip()
            if emotion_category in emotions:
                emotions[emotion_category].append(emotion_word)
            else:
                emotions[emotion_category] = [emotion_word]
    except:
        return None

    # Count number of occurrences of emotion words in the text
    # If "vivacious" is in the text two times - make sure it counts as two
    #text_emotions = {"arg": 0, "glad": 0, "ledsen": 0, "kärleksfull": 0}
    for word in cleaned_tweets:
        for emotion_category in emotions:
            if word in emotions[emotion_category]:
                #print(word)
                text_emotions[emotion_category] += 1

    most_frequent_emotion_value = max(text_emotions.items(), key=operator.itemgetter(1))[1]
    most_frequent_emotions = [emotion for emotion in text_emotions if text_emotions[emotion] == most_frequent_emotion_value]

    """ Plot the result as a bar graph displaying the mood of the people in the city """
    plt.figure()
    plt.xlabel("Twitter-känslor\n\n #Carpe diem #YOLO #😦!?! #born to be freeeeee ❤")
    moods = []
    score = []
    for emotion in text_emotions.keys():
        moods.append(emotion)
        score.append(text_emotions[emotion])
    colors = {'angry': (0.0, 0.0, 0.0, 0.8), 'happy': (0.9, 0.9, 0.0, 0.5),
              'sad': (0.0, 0.0, 0.9, 0.5), 'loving': (1.0, 0.0, 0.0, 0.5)}
    plt.bar(moods, score, color=(colors['angry'], colors['happy'], colors['sad'], colors['loving']))
    plt.suptitle(f"Vad är invånarna i {city.capitalize()} på för humör?")
    plt.show()

    return most_frequent_emotions

if __name__ == '__main__':
    mood_analysis(city="östersund", live=False)
