import random
import pygame

from common import TextBox, Button, battle_bg, Screen
from constants import *
from battle_screens import BattleScreen
from poketer import Poketer
from twitter.twitter_search import geocodes
from twitter.mood_score import calc_mood_score


class PoketerIntroScreen(Screen):
    def __init__(self):
        self.gunnar = Poketer("Happy Hasse", 'happy', 'yellow', 100, 50, catchword="#YOLO",
                              img_name="media/images/Green_monster_resized.png")

        self.ada = Poketer("Aggressive Ada", 'angry', 'red', 100, 50, catchword="#FTW",
                           img_name="media/images/Pink_dragon_01.png")
        self.ada.image = pygame.transform.flip(self.ada.image, True, False)

        self.continue_button = Button((0.5, 0.5), (0.2, 0.1), PURPLE_1, PURPLE_5, 22, WHITE, "CONTINUE", frame=PURPLE_4)
        self.p1_text = "This is your Poketer Happy Hasse. Hasse thrives in merry environments with a lot of laughter and joy. " \
                       "He feeds on peoples' positive energy and cheerfulness. #YOLO"
        self.p2_text = "This is your opponent's Poketer Aggressvive Ada. She feels at home in hostile situations " \
                       "with a lot of swearing and controversy. #FTW"
        self.p1_pres = TextBox((0.35, 0.08), 22, False, WHITE, self.p1_text, line_width=35)
        self.p2_pres = TextBox((0.64, 0.62), 22, False, WHITE, self.p2_text, line_width=40)

        self.p1_stats = TextBox((0.8, 0.48), 18, False, WHITE,
                                f"Attack: {self.gunnar.attack} Health: {self.gunnar.health}")
        self.p2_stats = TextBox((0.22, 0.92), 18, False, WHITE,
                                f"Attack: {self.ada.attack} Health: {self.ada.health}")

    def handle_mouse_button(self, button):
        if button == 1:
            if self.continue_button.handle_mouse_button(button):
                self.ada.image = pygame.transform.flip(self.ada.image, True, False)
                return ChooseCityScreen(self.gunnar, self.ada)
        return self

    def render(self, screen):
        screen.fill(WHITE)
        screen.blit(battle_bg, (0, 0))
        screen.blit(self.gunnar.image, (500, 0))
        screen.blit(self.ada.image, (20, 270))
        self.p1_pres.render(screen)
        self.p2_pres.render(screen)
        self.p1_stats.render(screen)
        self.p2_stats.render(screen)
        self.continue_button.render(screen)


class ChooseCityScreen(Screen):
    def __init__(self, poketer, cpu_poketer):
        self.poketer = poketer
        self.cpu_poketer = cpu_poketer
        self.text = """Twitter-mood score! Your Poketer has a certain mood. You now have the opportunity to increase your Poketer's health
by searching for a city in Sweden where you think the inhabitants are in the same mood as your Poketer.
The residents' mood is based on what they tweet. The more emotional they are, the more they increase
your Poketer's health. Good luck!"""
        self.title = TextBox((0.5, 0.08), 20, False, WHITE, self.text, line_width=68)
        self.button_positions = [(0.3, 0.5), (0.7, 0.5),
                                 (0.3, 0.65), (0.7, 0.65),
                                 (0.3, 0.8), (0.7, 0.8)]
        self.city_buttons = []

        self.attitude_options = geocodes  # 8 st
        self.cities = list(self.attitude_options.keys())
        self.cities = self.cities[:-1]
        self.button_colors = [PASTEL_1, PASTEL_2, PASTEL_3, PASTEL_4, PASTEL_5, PASTEL_6, PASTEL_1]
        for idx in range(len(self.button_positions)):
            self.city_button = Button(self.button_positions[idx], (0.3, 0.12), self.button_colors[idx],
                                      PASTEL_7, 27, WHITE, self.cities[idx].capitalize(),
                                      frame=self.button_colors[idx + 1])
            self.city_buttons.append(self.city_button)

        self.cpu_city = random.choice(self.cities)

    def handle_mouse_button(self, button):
        if button == 1:
            for idx, city_button in enumerate(self.city_buttons):
                if city_button.handle_mouse_button(button):
                    return MoodScoreScreen(self.cities[idx], self.poketer, self.cpu_city, self.cpu_poketer)
        return self

    def render(self, screen):
        screen.fill(WHITE)
        screen.blit(battle_bg, (0, 0))
        self.title.render(screen)

        for button in self.city_buttons:
            button.render(screen)


class MoodScoreScreen(Screen):
    def __init__(self, city, poketer, cpu_city, cpu_poketer):
        self.poketer = poketer
        self.cpu_poketer = cpu_poketer
        self.city = city
        self.cpu_city = cpu_city

        self.p1_text = f"... Tweet, tweet! Calculates how {self.poketer.mood} the inhabitants of {self.city.capitalize()} are ..."
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
        screen.blit(battle_bg, (0, 0))
        self.row1.render(screen)
        self.row2.render(screen)
        self.line.render(screen)
        self.row3.render(screen)
        self.continue_button.render(screen)
