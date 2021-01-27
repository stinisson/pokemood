from twitter_search import geocodes
from mood_score import calc_mood_score
from mood_analysis import mood_analysis, text_emotions
from sentiment_analysis import sentiment_analysis


def twitter_demo():
    x = """Din Pokemon har ett visst humör. Du har nu möjligheten att öka din pokemons hälsa genom
        att söka efter en stad i Sverige där du tror att invånarna är på samma humör som din pokemon.
        Invånarnas humör baseras på vad de twittrar. Ju mer känslosamma de är desto mer ökar 
        din Pokemons hälsa. Lycka till!"""
    print(f"""\n
    ----------------------------------------------------------------------------------------------------
    *                                                                                                  *
        {x}                                         
    *                                                                                                  *
    ----------------------------------------------------------------------------------------------------
    """)
    for idx, city in enumerate(geocodes):
        if city:
            print(idx + 1, city.capitalize())
    city_choice = int(input(f"Vilken stad väljer du? (1-{len(geocodes) - 1}): "))
    city_list = list(geocodes)
    city = city_list[city_choice - 1]

    print("Det här kan ta en liten stund... Vänligen vänta. :)")

    mood_score = calc_mood_score("happy", city, live=False)

    x = f" ... Beräknar humör för invånarna i {city.capitalize()} ..."
    y = f"Happy-Hasse fick {mood_score} i ökad hälsa! #YOLO"
    print(f"""
    ----------------------------------------------------------------------------------------------------
    *                                                                                                  *
                     {x}
                       {y}
    *                                                                                                  *
    ----------------------------------------------------------------------------------------------------
    """)

    input("Tryck enter för att fortsätta")

    x = f" *-*-* Nu är det dags för battle! *-*-*"
    y = f"""Boom! Smack! Boom!"""
    print(f"""
    ----------------------------------------------------------------------------------------------------
    *                                                                                                  *
                     {x}
                               {y}
    *                                                                                                  *
    ----------------------------------------------------------------------------------------------------
    """)

    input("Tryck enter för att fortsätta")

    x = """ Attack-bonus! Du har nu chansen att öka din pokemons attack-styrka. 
         Välj en stad och gissa vilket humör som är mest förekommande 
         bland invånarna. Lycka till! """
    print(f"""\n
    ----------------------------------------------------------------------------------------------------
    *                                                                                                  *
        {x}                                         
    *                                                                                                  *
    ----------------------------------------------------------------------------------------------------
    """)

    for idx, city in enumerate(geocodes):
        if city:
            print(idx + 1, city.capitalize())
    city_choice = int(input(f"Vilken stad väljer du? (1-{len(geocodes) - 1}): "))
    city_list = list(geocodes)
    city = city_list[city_choice - 1]

    for idx, emotion in enumerate(text_emotions):
        print(idx + 1, emotion.capitalize())
    emotion_choice = int(input(f"Vilken känsla är mest förekommande i {city.capitalize()}? (1-{len(text_emotions)}): "))
    emotion_list = list(text_emotions)
    emotion = emotion_list[emotion_choice - 1]

    print("Det här kan ta en liten stund... Vänligen vänta. :)")

    most_frequent_emotions = mood_analysis(city=city, live=False)

    if emotion in most_frequent_emotions:
        x = f"""Rätt! Vanligast är att man är {emotion} i {city.capitalize()}.
                Din pokemon belönas med 50 poäng i ökad attack-styrka!"""
    else:
        x = f"""Tyvärr! I {city.capitalize()} är man {most_frequent_emotions[0]}, inte {emotion}!
                     Du får ingen attack-bonus."""

    print(f"""
    ----------------------------------------------------------------------------------------------------
    *                                                                                                  *
                     {x}
    *                                                                                                  *
    ----------------------------------------------------------------------------------------------------
    """)

    input("Tryck enter för att fortsätta")


    x = """    Twitter-vadslagning! Har du koll på vad som trendar på sociala medier? 
            Skriv in ett ord och på vilket språk du vill använda i sökningen. Gissa om 
            de senaste tweetsen som innehåller detta ord är mest positiva, mest negativa
            eller neutrala. Om du gissar rätt belönas du med 20 p i ökad hälsa.
            Om du gissar fel bestraffas du med 20 p minskad hälsa. Lycka till! """

    print(f"""\n
    ----------------------------------------------------------------------------------------------------
    *                                                                                                  *
        {x}                                         
    *                                                                                                  *
    ----------------------------------------------------------------------------------------------------
    """)

    print("Skriv in ett nyckelord att söka efter på Twitter. Exempel: COVID, Donald Trump, Estonia.")
    keyword_choice = input(">> ")

    language_choice = input("Vilket språk vill du söka efter? [S]venska eller [E]ngelska? ")
    if language_choice.lower() == "s":
        language_choice = "swedish"
    elif language_choice.lower() == "e":
        language_choice = "english"

    print(f"Tror du folket på Twitter är mest positivt, mest negativt eller neutralt inställda till {keyword_choice}? ")
    attitude_choice = input("[P]ostiva - [N]egativa - ne[U]trala? ")
    if attitude_choice.lower() == "p":
        attitude_choice = "positivt"
    elif attitude_choice.lower() == "n":
        attitude_choice = "negativt"
    elif attitude_choice.lower() == "u":
        attitude_choice = "neutralt"

    print("Det här kan ta en liten stund... Vänligen vänta. :)")

    # Ni får testköra genom att söka efter covid på engelska
    result = sentiment_analysis(keyword=keyword_choice, language=language_choice, file_name='demo_tweets_english_covid.p', live=False)

    if attitude_choice == result:
        x = f"""Rätt! {keyword_choice} har mest {result} innehåll på Twitter.
                     Din pokemon belönas med 20 poäng i ökad hälsa!"""
    else:
        x = f"""Tyvärr, {keyword_choice} har mest {result} innehåll på Twitter!
                     Din pokemon bestraffas med 20 p i minskad hälsa."""

    print(f"""
    ----------------------------------------------------------------------------------------------------
    *                                                                                                  *
                     {x}
    *                                                                                                  *
    ----------------------------------------------------------------------------------------------------
    """)


if __name__ == '__main__':
    twitter_demo()
