import sys
from random import randint
import pygame

from constants import *
from common import music, battle_bg, TextBox, Button, periodic_movement, Screen
from sentiment_analysis_screen import SentimentAnalysisScreen
from quiz.quiz import QuizStartScreen
from quiz.quiz_api import quiz_categories
from end_screens import WinnerScreen


class BattleScreen(Screen):
    def __init__(self, poketer, cpu_poketer):
        self.poketer = poketer
        self.cpu_poketer = cpu_poketer

        self.attack_button = Button((0.14, 0.8), (0.2, 0.1), PURPLE_1, PURPLE_5, 22, WHITE, "Attack", frame=PURPLE_2)
        self.special_button = Button((0.38, 0.8), (0.2, 0.1), PURPLE_2, PURPLE_5, 22, WHITE, "Special", frame=PURPLE_3)
        self.sentiment_button = Button((0.62, 0.8), (0.2, 0.1), PURPLE_3, PURPLE_5, 22, WHITE, "Sentiment",
                                       frame=PURPLE_4)
        self.quiz_button = Button((0.86, 0.8), (0.2, 0.1), PURPLE_4, PURPLE_5, 22, WHITE, "Quiz", frame=PURPLE_1)
        self.quit_button = Button((0.7, 0.1), (0.2, 0.1), LIGHT_GREEN_UNSELECTED, LIGHT_GREEN_SELECTED, 22, WHITE,
                                  "QUIT")

        vs_sign = pygame.image.load("media/images/VS.PNG")
        self.vs_sign = pygame.transform.smoothscale(vs_sign, (270, 343))

        self.poketer_name = TextBox((0.22, 0.05), 20, False, LIGHT_GREEN, f"{self.poketer.name}")
        self.poketer_stats = TextBox((0.22, 0.1), 20, False, WHITE, '')

        self.cpu_poketer_name = TextBox((0.79, 0.05), 20, False, LIGHT_PINK, f"{self.cpu_poketer.name}")
        self.cpu_poketer_stats = TextBox((0.78, 0.1), 20, False, WHITE, '')

    def handle_mouse_button(self, button):
        if button == 1:
            if self.attack_button.handle_mouse_button(button):
                return AttackScreen("user", self.poketer, self.cpu_poketer)
            if self.special_button.handle_mouse_button(button):
                return SpecialAttackScreen("user", self.poketer, self.cpu_poketer)
            if self.sentiment_button.handle_mouse_button(button):
                return SentimentAnalysisScreen(self.poketer, self)
            if self.quiz_button.handle_mouse_button(button):
                return QuizStartScreen(5, quiz_categories, self, self.poketer)
            if self.quit_button.handle_mouse_button(button):
                print("The End! :)")
                sys.exit()
        return self

    def render(self, screen):
        screen.fill(WHITE)
        screen.blit(battle_bg, (0, 0))

        x_off, y_off = periodic_movement(1, 5)
        screen.blit(self.poketer.image, (24, 123 + y_off))
        screen.blit(self.cpu_poketer.image, (504, 135))

        self.poketer_name.render(screen)
        self.poketer_stats.set_text(f"Attack: {self.poketer.attack} Health: {self.poketer.health}")
        self.poketer_stats.render(screen)

        self.cpu_poketer_name.render(screen)
        self.cpu_poketer_stats.set_text(f"Attack: {self.cpu_poketer.attack} Health: {self.cpu_poketer.health}")
        self.cpu_poketer_stats.render(screen)

        self.attack_button.render(screen)
        self.special_button.render(screen)
        self.sentiment_button.render(screen)

        self.quiz_button.render(screen)

        screen.blit(self.vs_sign, (265, 135))
        textbox_gunnar = TextBox((0.5, 0.2), 30, False, WHITE, "It's your turn!")
        textbox_gunnar.render(screen)


class AttackScreen(Screen):
    def __init__(self, turn, poketer, cpu_poketer):
        self.turn = turn
        self.poketer = poketer
        self.cpu_poketer = cpu_poketer
        self.timeout = pygame.time.get_ticks()

        if self.turn == "user":
            attack_score = attack_function(self.poketer, self.cpu_poketer)
            self.text_poketer = f"{self.poketer.name} attacked {self.cpu_poketer.name}! {self.cpu_poketer.name} took {attack_score} in damage!"
            self.text_cpu_poketer = ""
        else:
            attack_score = attack_function(self.cpu_poketer, self.poketer)
            self.text_cpu_poketer = f"{self.cpu_poketer.name} attacked {self.poketer.name}! You took {attack_score} in damage!"
            self.text_poketer = ""

        self.textbox_poketer = TextBox((0.5, 0.2), 20, False, LIGHT_GREEN, self.text_poketer)
        self.textbox_cpu_poketer = TextBox((0.5, 0.2), 20, False, LIGHT_PINK, self.text_cpu_poketer)

        self.poketer_name = TextBox((0.22, 0.05), 20, False, LIGHT_GREEN, f"{self.poketer.name}")
        self.poketer_stats = TextBox((0.22, 0.1), 20, False, WHITE,
                                     f"Attack: {self.poketer.attack} Health: {self.poketer.health}")

        self.cpu_poketer_name = TextBox((0.79, 0.05), 20, False, LIGHT_PINK, f"{self.cpu_poketer.name}")
        self.cpu_poketer_stats = TextBox((0.78, 0.1), 20, False, WHITE,
                                         f"Attack: {self.cpu_poketer.attack} Health: {self.cpu_poketer.health}")

    def handle_mouse_button(self, button):
        mx, my = pygame.mouse.get_pos()
        quit_button_rect = pygame.Rect(650, 30, 140, 40)
        back_button_rect = pygame.Rect(30, 540, 140, 40)

        if button == 1:
            if back_button_rect.collidepoint((mx, my)):
                return BattleScreen(self.poketer, self.cpu_poketer)
            if quit_button_rect.collidepoint((mx, my)):
                sys.exit()
            return self

    def handle_timer(self):
        time_now = pygame.time.get_ticks()
        if time_now - self.timeout > 3000 and self.timeout != 0:
            self.timeout = 0

            if self.cpu_poketer.health <= 0:
                return WinnerScreen(self.poketer, won=True)
            if self.poketer.health <= 0:
                return WinnerScreen(self.poketer, won=False)

            # when the users attack is finished - let cpu make a move
            if self.turn == "user":
                if cpu_random_attack():
                    return AttackScreen("cpu", self.poketer, self.cpu_poketer)
                else:
                    return SpecialAttackScreen("cpu", self.poketer, self.cpu_poketer)

            # when the cpu's attack is finished - return to Battlescreen
            if self.turn == "cpu":
                return BattleScreen(self.poketer, self.cpu_poketer)
        return self

    def render(self, screen):
        screen.fill(WHITE)
        screen.blit(battle_bg, (0, 0))

        self.textbox_poketer.render(screen)
        self.textbox_cpu_poketer.render(screen)

        x_off, y_off = periodic_movement(1, 5)
        if self.turn == "user":
            screen.blit(self.poketer.image, (24, 123 + y_off))
            screen.blit(self.cpu_poketer.image, (504, 135))

        else:
            screen.blit(self.poketer.image, (24, 123))
            screen.blit(self.cpu_poketer.image, (504, 135 + y_off))

        self.poketer_name.render(screen)
        self.poketer_stats.render(screen)
        self.cpu_poketer_name.render(screen)
        self.cpu_poketer_stats.render(screen)

        # Rotate sword depending on whose turn it is
        sword(self.turn, screen)


class SpecialAttackScreen(Screen):
    def __init__(self, turn, poketer, cpu_poketer):
        self.turn = turn
        self.poketer = poketer
        self.cpu_poketer = cpu_poketer
        self.timeout = pygame.time.get_ticks()

        if self.turn == "user":
            attack_score = special_attack(self.poketer, self.cpu_poketer)
            self.text_poketer = f"{self.poketer.name} special attacked {self.cpu_poketer.name}! {self.cpu_poketer.name} took {attack_score} in damage!"
            self.text_cpu_poketer = ""
        else:
            attack_score = special_attack(self.cpu_poketer, self.poketer)
            self.text_cpu_poketer = f"{self.cpu_poketer.name} special attacked {self.poketer.name}! You took {attack_score} in damage!"
            self.text_poketer = ""

        self.textbox_poketer = TextBox((0.5, 0.2), 20, False, LIGHT_GREEN, self.text_poketer)
        self.textbox_cpu_poketer = TextBox((0.5, 0.2), 20, False, LIGHT_PINK, self.text_cpu_poketer)

        self.poketer_name = TextBox((0.22, 0.05), 20, False, LIGHT_GREEN, f"{self.poketer.name}")
        self.poketer_stats = TextBox((0.22, 0.1), 20, False, WHITE,
                                     f"Attack: {self.poketer.attack} Health: {self.poketer.health}")

        self.cpu_poketer_name = TextBox((0.79, 0.05), 20, False, LIGHT_PINK, f"{self.cpu_poketer.name}")
        self.cpu_poketer_stats = TextBox((0.78, 0.1), 20, False, WHITE,
                                         f"Attack: {self.cpu_poketer.attack} Health: {self.cpu_poketer.health}")

    def handle_mouse_button(self, button):
        mx, my = pygame.mouse.get_pos()
        quit_button_rect = pygame.Rect(650, 30, 140, 40)
        back_button_rect = pygame.Rect(30, 540, 140, 40)

        if button == 1:
            if back_button_rect.collidepoint((mx, my)):
                return BattleScreen(self.poketer, self.cpu_poketer)
            if quit_button_rect.collidepoint((mx, my)):
                print("The End! :)")
                sys.exit()
        return self

    def handle_timer(self):
        time_now = pygame.time.get_ticks()
        if time_now - self.timeout > 3000 and self.timeout != 0:
            self.timeout = 0

            if self.cpu_poketer.health <= 0:
                return WinnerScreen(self.poketer, won=True)
            if self.poketer.health <= 0:
                return WinnerScreen(self.poketer, won=False)

            # when the users attack is finished - let cpu make a move
            if self.turn == "user":
                if cpu_random_attack():
                    return AttackScreen("cpu", self.poketer, self.cpu_poketer)
                else:
                    return SpecialAttackScreen("cpu", self.poketer, self.cpu_poketer)

            # when the cpu's attack is finished - return to Battlescreen
            if self.turn == "cpu":
                return BattleScreen(self.poketer, self.cpu_poketer)
        return self

    def render(self, screen):
        screen.fill(WHITE)
        screen.blit(battle_bg, (0, 0))

        self.textbox_poketer.render(screen)
        self.textbox_cpu_poketer.render(screen)

        x_off, y_off = periodic_movement(1, 5)
        if self.turn == "user":
            screen.blit(self.poketer.image, (24, 123 + y_off))
            screen.blit(self.cpu_poketer.image, (504, 135))

        else:
            screen.blit(self.poketer.image, (24, 123))
            screen.blit(self.cpu_poketer.image, (504, 135 + y_off))

        self.poketer_name.render(screen)
        self.poketer_stats.render(screen)
        self.cpu_poketer_name.render(screen)
        self.cpu_poketer_stats.render(screen)
        crossed_sword(screen)


def attack_function(attacker, defender):
    defender.add_health(-attacker.attack)
    return attacker.attack


def special_attack(attacker, defender):
    misschans = randint(1, 6)
    if misschans <= 2:
        defender.add_health(-attacker.attack * 2)
        return attacker.attack * 2
    return 0


def cpu_random_attack():
    random_number = randint(1, 11)
    if random_number <= 7:
        return True
    return False


def sword(turn, screen):
    sword_img = pygame.image.load("media/images/sword_resized.png")
    x_off, y_off = periodic_movement(1, 5)
    if turn == "user":
        rotated_image = pygame.transform.rotozoom(sword_img, 0 + x_off, 1)
    else:
        rotated_image = pygame.transform.rotozoom(sword_img, 70 + x_off, 1)
    rotated_rect = rotated_image.get_rect(center=(400, 300))
    screen.blit(rotated_image, rotated_rect)


def crossed_sword(screen):
    crossed_sword_img = pygame.image.load("media/images/Sword_crossed_01.PNG")
    crossed_sword_img = pygame.transform.smoothscale(crossed_sword_img, (230, 230))
    rect = crossed_sword_img.get_rect()
    x_off, y_off = periodic_movement(1, 7)
    scaled_image = pygame.transform.smoothscale(crossed_sword_img, (rect.width + int(x_off), rect.height + int(x_off)))
    scaled_rect = scaled_image.get_rect()
    scaled_rect.center = (420, 280)
    screen.blit(scaled_image, scaled_rect)
