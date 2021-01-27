import random

from common import TextBox, Button, background, Screen
from constants import *
from battle_screens import BattleScreen
from twitter.twitter_search import geocodes
from twitter.mood_score import calc_mood_score
from poketer import Poketer


class ChooseCityMoodScreen(Screen):
    #def __init__(self, poketer, cpu_poketer):
        # self.poketer = poketer
        # self.cpu_poketer = cpu_poketer
    def __init__(self):

        self.poketer = Poketer("Happy Hasse", 'happy', 'yellow', 100, 50, catchword="#YOLO",
                              img_name="media/images/Green_monster_resized.png")
        self.cpu_poketer = Poketer("Aggressive Ada", 'angry', 'red', 100, 50, catchword="#FTW",
                           img_name="media/images/Pink_dragon_01.png")
        self.attack_score = 10
        self.text = f"""Mood analysis! Choose a city and guess which mood is most prevalent among the inhabitants.
If you guess correctly, your Poketer will be rewarded with {self.attack_score} attack points. If you guess wrong, 
your Poketer will be punished and lose {self.attack_score} p in attack strength. Good luck!"""
        self.title = TextBox((0.5, 0.08), 20, False, WHITE, self.text, line_width=68)

        self.city_button_positions = [(0.2, 0.45), (0.5, 0.45), (0.8, 0.45),
                                  (0.2, 0.6), (0.5, 0.6), (0.8, 0.6)]
        self.city_buttons = []
        self.attitude_options = geocodes  # 8 st
        self.cities = list(self.attitude_options.keys())
        self.cities = self.cities[:-1]


        #self.button_colors = [PASTEL_1, PASTEL_2, PASTEL_3, PASTEL_4, PASTEL_5, PASTEL_6, PASTEL_1]


        self.button_colors = [BLUE_1, BLUE_2, BLUE_3, BLUE_4, BLUE_5, BLUE_6, BLUE_7]

        # 254, 109, 115

        for idx in range(len(self.city_button_positions)):
            self.city_button = Button(self.city_button_positions[idx], (0.25, 0.12), (53, 90, 105, 150),
                                      (127, 180, 192, 200), 27, WHITE, self.cities[idx].capitalize(),
                                      frame=(37, 50, 55))
            self.city_buttons.append(self.city_button)

        self.button_colors = [HAPPY, SAD, ANGRY, LOVING]
        self.frame_colors = [HAPPY_F, SAD_F, ANGRY_F, LOVING_F]
        self.mood_button_positions = [(0.146, 0.8), (0.382, 0.8), (0.618, 0.8), (0.854, 0.8)]
        self.mood_buttons = []
        self.mood_options = ["happy", "sad", "angry", "loving"]
        for idx in range(len(self.mood_button_positions)):
            self.mood_button = Button(self.mood_button_positions[idx], (0.18, 0.1), self.button_colors[idx],
                                      (188, 231, 132, 200), 22, WHITE, self.mood_options[idx].capitalize(),
                                      frame=self.frame_colors[idx])
            self.mood_buttons.append(self.mood_button)

        self.cpu_city = random.choice(self.cities)
        self.cpu_mood = random.choice(self.mood_options)

        self.chosen_city = ""
        self.chosen_mood = ""
        self.city_is_chosen = False
        self.mood_is_chosen = False

    def handle_mouse_button(self, button):
        if button == 1:
            for idx, city_button in enumerate(self.city_buttons):
                if city_button.handle_mouse_button(button):
                    self.chosen_city = self.cities[idx]
                    self.city_is_chosen = True
                    print("chose:", self.chosen_city)
                    break
            for idx, mood_button in enumerate(self.mood_buttons):
                if mood_button.handle_mouse_button(button):
                    self.chosen_mood = self.mood_options[idx]
                    self.mood_is_chosen = True
                    print("chose:", self.chosen_mood)
                    break
        if self.city_is_chosen and self.mood_is_chosen:
            return MoodAnalysisScreen(self.chosen_city, self.chosen_mood, self.poketer, self.cpu_city, self.cpu_mood, self.cpu_poketer)
        return self

    def render(self, screen):
        screen.fill(WHITE)
        screen.blit(background, (0, 0))
        self.title.render(screen)

        for button in self.city_buttons:
            button.render(screen)

        for button in self.mood_buttons:
            button.render(screen)


class MoodAnalysisScreen(Screen):
    def __init__(self, city, mood, poketer, cpu_city, cpu_mood, cpu_poketer):
        self.city = city
        self.mood = mood
        self.poketer = poketer

        self.cpu_city = cpu_city
        self.cpu_mood = cpu_mood
        self.cpu_poketer = cpu_poketer

        self.p1_text = f"... Tweet, tweet! Calculates how {self.mood} the inhabitants of {self.city.capitalize()} are ..."
        self.row1 = TextBox((0.5, 0.1), 28, False, WHITE, self.p1_text, line_width=45)


        # TODO HORRIBLE - FIX THIS!
        self.p1_moodscore = calc_mood_score(self.poketer.mood, self.city, True)
        if self.p1_moodscore is None:
            self.p1_moodscore = calc_mood_score(self.poketer.mood, self.city, False)
            self.p1_text2 = f"{poketer.name} got {self.p1_moodscore} p in increased health. {poketer.name} now has {poketer.health} in total health."
            self.poketer.add_health(self.p1_moodscore)
            if self.p1_moodscore is None:
                self.poketer.add_health(10)
                self.p1_text2 = f"Something went wrong, but {poketer.name} get 10 extra health points anyway. {poketer.name} now has {poketer.health} in total health."
        else:
            self.poketer.add_health(self.p1_moodscore)
            self.p1_text2 = f"{poketer.name} got {self.p1_moodscore} p in increased health. {poketer.name} now has {poketer.health} p in total health."
        self.row2 = TextBox((0.5, 0.3), 25, False, WHITE, self.p1_text2, line_width=45)

        self.line = TextBox((0.5, 0.48), 25, False, WHITE, "* " * 35, line_width=70)

        # TODO HORRIBLE - FIX THIS!
        self.p2_moodscore = calc_mood_score(self.cpu_poketer.mood, self.cpu_city, True)
        if self.p2_moodscore is None:
            self.p2_moodscore = calc_mood_score(self.cpu_poketer.mood, self.cpu_city, False)
            self.p2_text2 = f"Your opponent chose {cpu_city.capitalize()} and {cpu_poketer.name} got {self.p2_moodscore} p in increased health. {cpu_poketer.name} now has {cpu_poketer.health} p in total health."
            self.cpu_poketer.add_health(self.p2_moodscore)
            if self.p2_moodscore is None:
                self.cpu_poketer.add_health(10)
                self.p2_text2 = f"Something went wrong, but {cpu_poketer.name} get 10 extra health points anyway. {cpu_poketer.name} now has {cpu_poketer.health} p in total health."
        else:
            self.cpu_poketer.add_health(self.p2_moodscore)
            self.p2_text2 = f"Your opponent chose {cpu_city.capitalize()} and {cpu_poketer.name} got {self.p2_moodscore} p in increased health. {cpu_poketer.name} now has {cpu_poketer.health} p in total health."
        self.row3 = TextBox((0.5, 0.57), 25, False, WHITE, self.p2_text2, line_width=50)

        self.continue_button = Button((0.5, 0.85), (0.2, 0.1), PASTEL_3, PASTEL_6, 22, WHITE, "Begin battle!",
                                      frame=PASTEL_4)

    def handle_mouse_button(self, button):
        if button == 1:
            if self.continue_button.handle_mouse_button(button):
                return BattleScreen(self.poketer, self.cpu_poketer)
        return self

    def render(self, screen):
        screen.fill(WHITE)
        screen.blit(background, (0, 0))
        self.row1.render(screen)
        self.row2.render(screen)
        self.line.render(screen)
        self.row3.render(screen)
        self.continue_button.render(screen)
