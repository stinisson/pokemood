from pokemood_text_based.mood_analysis import text_emotions
from twitter_search import geocodes


def take_integer_input(input_text, end_range, error_text):
    while True:
        try:
            user_choice = int(input(input_text))
            if user_choice in range(1, end_range):
                break
        except ValueError:
            pass
        print(error_text)
    return user_choice


def choose_city():
    for idx, city in enumerate(geocodes):
        if city:
            print(idx + 1, city.capitalize())

    city_choice = take_integer_input(f"Vilken stad väljer du? (1-{len(geocodes) - 1}): ",
                                     len(geocodes), f"Ogiltligt val! Ange en siffra 1-{len(geocodes) - 1}.")

    # One of the elements in geocodes is an empty placeholder
    temp_city_list = list(geocodes)
    city_list = [x for x in temp_city_list if x != '']
    city = city_list[city_choice - 1]
    return city


def get_cities():
    temp_city_list = list(geocodes)
    cities = [x for x in temp_city_list if x != '']
    return cities


def choose_emotion(city):
    for idx, emotion in enumerate(text_emotions):
        print(idx + 1, emotion.capitalize())

    emotion_choice = take_integer_input(
        f"Vilken känsla är mest förekommande i {city.capitalize()}? (1-{len(text_emotions)}): ",
        len(text_emotions) + 1,
        f"Ogiltligt val! Ange en siffra 1-{len(text_emotions)}.")

    emotion_list = list(text_emotions)
    emotion = emotion_list[emotion_choice - 1]
    return emotion


def get_emotions():
    emotions = list(text_emotions)
    return emotions
