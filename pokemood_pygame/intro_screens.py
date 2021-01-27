import sys
import pygame

from common import music, Button, start_background, logo, Screen
from constants import *
from game_screen import PoketerIntroScreen
from poketer import Poketer


class FirstScreen(Screen):
    def __init__(self):
        music("media/music/intro_song_1.mp3", 0.0)
        self.gunnar = Poketer("Happy Hasse", 'happy', 'yellow', 100, 50, catchword="#YOLO",
                              img_name="media/images/Green_monster_resized.png")
        self.gunnar.image = pygame.transform.smoothscale(self.gunnar.image, (220, 220))

        self.ada = Poketer("Aggressive Ada", 'angry', 'red', 100, 50, catchword="#FTW",
                           img_name="media/images/Pink_dragon_01.png")
        self.ada.image = pygame.transform.flip(self.ada.image, True, False)

        self.ada.image = pygame.transform.flip(self.ada.image, True, False)
        self.ada.image = pygame.transform.smoothscale(self.ada.image, (225, 218))

        self.start_button = Button((0.5, 0.8), (0.3, 0.12), PASTEL_3,
                                   PASTEL_6, 27, WHITE, "Let's begin!", frame=PASTEL_4)

    def handle_mouse_button(self, button):
        if button == 1:
            if self.start_button.handle_mouse_button(button):
                return MenuScreen()

    def render(self, screen):
        screen.fill(WHITE)
        screen.blit(start_background, (0, 0))
        screen.blit(logo, (215, -55))
        screen.blit(self.gunnar.image, (0, 200))
        screen.blit(self.ada.image, (580, 200))
        self.start_button.render(screen)


class MenuScreen(Screen):
    def __init__(self):
        music("media/music/intro_song_1.mp3", 0.0)
        self.button_positions = [(0.5, 0.35), (0.5, 0.5), (0.5, 0.65), (0.5, 0.8)]
        self.option_buttons = []
        self.attitude_options = ["Start game", "How to play", "Settings", "Quit"]
        self.button_colors = [PASTEL_1, PASTEL_2, PASTEL_3, PASTEL_4, PASTEL_5]
        for idx in range(len(self.button_positions)):
            self.option_button = Button(self.button_positions[idx], (0.3, 0.12), self.button_colors[idx],
                                        PASTEL_6, 27, WHITE, self.attitude_options[idx],
                                        frame=self.button_colors[idx + 1])
            self.option_buttons.append(self.option_button)

    def handle_mouse_button(self, button):
        if button == 1:
            if self.option_buttons[0].handle_mouse_button(button):
                return PoketerIntroScreen()
            if self.option_buttons[1].handle_mouse_button(button):
                return InstructionsScreen()
            if self.option_buttons[2].handle_mouse_button(button):
                pass
            if self.option_buttons[3].handle_mouse_button(button):
                print("The End! :)")
                sys.exit()

    def render(self, screen):
        screen.fill(WHITE)
        screen.blit(start_background, (0, 0))
        screen.blit(logo, (215, -55))
        for button in self.option_buttons:
            button.render(screen)


class InstructionsScreen(Screen):
    def __init__(self):
        instructions_frame = pygame.image.load("media/images/Frame_background.PNG")
        self.instructions_frame = pygame.transform.smoothscale(instructions_frame, (650, 450))
        self.back_button = Button((0.15, 0.92), (0.25, 0.1), PASTEL_3,
                                  PASTEL_6, 27, WHITE, "Return", frame=PASTEL_4)

        self.quit_button = Button((0.85, 0.08), (0.25, 0.1), PASTEL_3,
                                  PASTEL_6, 27, WHITE, "Quit", frame=PASTEL_4)

    def handle_mouse_button(self, button):
        if button == 1:
            if self.back_button.handle_mouse_button(button):
                return MenuScreen()
            if self.quit_button.handle_mouse_button(button):
                print("The End! :)")
                sys.exit()

    def render(self, screen):
        screen.fill(WHITE)
        screen.blit(start_background, (0, 0))
        screen.blit(self.instructions_frame, (75, 75))
        self.back_button.render(screen)
        self.quit_button.render(screen)
