""" The player has a pokemon with a particular mood. The player tries to guess in which city the inhabitants
 have high levels of the same mood based on their Twitter content. The Pokemon gets awarded an amount of increased
 health based on the mood level. """

from pathlib import Path
import os
from twitter_search import get_tweets


def calc_mood_score(mood, city, live=False):
    """ Calculate mood score for a city chosen by the user. The mood score represent what mood
    the inhabitants of a particular city are in and is calculated by counting how many of the
    recent tweets that have any keyword associated with a particular mood in them.
    The keyword files must be placed in a folder called 'keywords' and be named mood_keywords.csv.
    The content of the keyword files must a single comma separated line without any spaces.
    The mood score is returned as an integer. If something goes wrong and no tweets are retrieved or the
    keyword files are unable to be located None is returned. """

    keywords = {}
    try:
        for file in os.listdir('keywords'):
            if '_keywords.csv' in file:
                keywords[file.replace(file[-13:], "")] = set(Path(f'keywords/{file}').read_text(encoding='utf8').split(','))
    except FileNotFoundError:
        return None

    city_lower = city.lower()
    file_name_city = city_lower.replace("å", "a").replace("ä", "a").replace("ö", "o")

    tweets = get_tweets(city=city, load_from_file=True, live=live, file_name=f'tweets_{file_name_city}.p', file_path='fallback-tweets')

    if not tweets:
        return None

    tweets_with_mood_content = 0
    for idx, tweet in enumerate(tweets):
        for keyword in keywords.get(mood):
            if keyword in tweet:
                tweets_with_mood_content += 1
                #print(idx, keyword, '-->', tweet)

    #print("number of tweets with mood content:", tweets_with_mood_content)
    #print(len(tweets))

    # TODO change how mood score is used in update_max_health_by_city_mood!
    x = tweets_with_mood_content / len(tweets)
    if x < 0.15:
        k = 150 / 0.15
        mood_score = k * x
    else:
        k = (200 - 150) / (1 - 0.15)
        m = 150
        mood_score = k * (x - 0.15) + m
    return int(mood_score)


if __name__ == '__main__':
    calc_mood_score(mood="happy", city="göteborg", live=False)
