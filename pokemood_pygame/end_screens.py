import sys

import pygame

from common import periodic_movement, music, TextBox, Button, logo, Screen
from constants import SCREEN_SIZE, WHITE, PINK, YELLOW_LIGHT, LIGHT_GREEN, LIGHT_PINK


class WinnerScreen(Screen):
    def __init__(self, gunnar, won):
        background_win = pygame.image.load("media/images/winning_pic.jpg")
        self.background_win = pygame.transform.smoothscale(background_win, SCREEN_SIZE)
        if won:
            music("media/music/vinnar_låt_utkast.mp3", 0.0)
        else:
            music("media/music/lose_game_melody.mp3", 0.0)

        self.quit_button = Button((0.85, 0.9), (0.2, 0.1), LIGHT_GREEN, LIGHT_PINK, 22, WHITE, "QUIT", frame=YELLOW_LIGHT)
        self.gunnar = gunnar
        self.won = won

    def handle_mouse_button(self, button):
        if button == 1:
            if self.quit_button.handle_mouse_button(button):
                print("The End! :)")
                sys.exit()
        return self

    def render(self, screen):
        screen.fill(WHITE)
        screen.blit(self.background_win, (0, 0))

        if self.won:
            x_off, y_off = periodic_movement(1, 5)
            gunnar_bigger = pygame.transform.scale(self.gunnar.image, (350, 350))
            screen.blit(gunnar_bigger, (220, 235 + y_off))
            winning_crown_hasse_moving(screen)
            pink_dragon_sad = pygame.image.load("media/images/Pink_dragon_05.png")
            pink_dragon_sad = pygame.transform.scale(pink_dragon_sad, (204, 235))
            screen.blit(pink_dragon_sad, (25, 340))
            tear_drop = pygame.image.load("media/images/tear-png-20.png")
            tear_drop = pygame.transform.scale(tear_drop, (25, 25))
            screen.blit(tear_drop, (120, 410))
            game_won = TextBox((0.5, 0.2), 35, False, YELLOW_LIGHT, f"Congratulations, {self.gunnar.name} won!")
            game_won.render(screen)
        else:
            ada_win_pic = pygame.image.load("media/images/Pink_dragon_08.png")
            ada_win_pic = pygame.transform.scale(ada_win_pic, (350, 350))
            screen.blit(ada_win_pic, (205, 285))
            winning_crown_ada_moving(screen)
            gunnar_lose = pygame.transform.scale(self.gunnar.image, (200, 200))
            screen.blit(gunnar_lose, (25, 355))
            tear_drop = pygame.image.load("media/images/tear-png-20.png")
            tear_drop = pygame.transform.scale(tear_drop, (25, 25))
            screen.blit(tear_drop, (90, 430))
            game_lost = TextBox((0.5, 0.2), 35, False, PINK, "Better luck next time!")
            game_lost.render(screen)

        screen.blit(logo, (213, -55))
        self.quit_button.render(screen)


def winning_crown_hasse_moving(screen):
    winning_crown = pygame.image.load("media/images/crown.png")
    winning_crown = pygame.transform.scale(winning_crown, (170, 140))
    x_off, y_off = periodic_movement(1, 5)
    screen.blit(winning_crown, (270, 180 + y_off))


def winning_crown_ada_moving(screen):
    winning_crown = pygame.image.load("media/images/crown.png")
    winning_crown = pygame.transform.scale(winning_crown, (151, 124))
    x_off, y_off = periodic_movement(1, 5)
    screen.blit(winning_crown, (340, 245 + y_off))
