import math
import sys
import pygame

from common import music, Button, start_bg, logo, Screen
from constants import *
from game_screen import PoketerIntroScreen
from poketer import Poketer

"""
def linearTransformation(start_coord, end_coord, motion_time):


    time_now = pygame.time.get_ticks()
    if time_now - self.next_question_timeout > 2000 and self.next_question_timeout != 0:

    pygame.time.set_timer(first_move, 5000)
    pygame.time.set_time(first_move, 0)

    start_x, start_y = start_coord
    end_x, end_y = end_coord

    x = start_x + (end_x - start_x) * step_count / total_steps
    y = start_y + (end_y - start_y) * step_count / total_steps

    for i in range(100):
        steps()

    def steps(start_coord, end_coord, motion_time, fps=30):
        distance = pygame.math.abs(end_coord - start_coord)
        period = motion_time * (60 / 30)
        number_of_steps = distance / period
        return number_of_steps

    return (x, y)

    start_coord, end_coord, start_t, end_t
    i varje loop kör step
    en funktion step som tar ett steg
    utöver start coord och end coord ska ha parameter hur länge rörelsen ska ske
    hur många 30dels sekunder
    tar varje step räknar upp med ett och får ha en step_count
    var du beginnfer dig nu är step_count / tiden du angett
    och ekvationen
    pos x = start pos x + (slut pos x - start pos x) * step count / total antal steps
    samma för y
    x, y
    return x, y pos på skärmen
    """


def animation(step_count, screen):
    #screen.blit("media/images/Pink_dragon_01.png", (580, 200))

    start_x = 0
    end_x = 200
    motion_time = 10

    distance = abs(end_x - start_x)
    period = motion_time / 3
    total_steps = 300
    x = start_x + (end_x - start_x) * step_count/total_steps

    image = pygame.image.load("media/images/Green_monster_resized.png").convert_alpha()
    img = pygame.transform.smoothscale(image, (220, 220))
    screen.blit(img, (x, 200))


def steps(start_coord, end_coord, motion_time, fps=30):

    distance = abs(end_coord - start_coord)
    period = motion_time * (60 / fps)
    number_of_steps = distance / motion_time
    print(number_of_steps)
    return number_of_steps


class FirstScreen(Screen):
    def __init__(self):
        self.frame_start_time = pygame.time.get_ticks()
        self.current_frame = "first"
        self.x_hasse = 0
        self.y_hasse = 200
        self.x_ada = 780
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

    def movement(self, x_start, x_end, t_start, t_end, frame_time):
        return x_start + (x_end - x_start) * (frame_time - t_start) / (t_end - t_start)

    def animation(self, time_now):

        frame_time = time_now - self.frame_start_time
        frame_time_max = 7000

        print(self.current_frame)
        if self.current_frame == "first":
            """Hasse -> <-Ada"""
            x_start_h = -20
            x_end_h = 350
            t_start_h = 0
            t_end_h = 6000

            x_start_a = 780
            x_end_a = 580
            t_start_a = 4000
            t_end_a = 6000

            if t_start_h < frame_time < t_end_h:
                print("hasse:", self.x_hasse)
                self.x_hasse = self.movement(x_start_h, x_end_h, t_start_h, t_end_h, frame_time)

            if t_start_a < frame_time < t_end_a:
                print("ada:", self.x_ada)
                self.x_ada = self.movement(x_start_a, x_end_a, t_start_a, t_end_a, frame_time)

            if frame_time > frame_time_max:
                print("FIRST RESET FRAME TIME")
                self.current_frame = "second"
                self.frame_start_time = pygame.time.get_ticks()

        elif self.current_frame == "second":
            """<-Hasse <-Ada"""
            frame_time_max = 7500

            x_start_h = 350
            x_end_h = -210
            t_start_h = 0
            t_end_h = 5000

            x_start_a = 580
            x_end_a = -210
            t_start_a = 1000
            t_end_a = 6500

            if t_start_h < frame_time < t_end_h:
                print("hasse:", self.x_hasse)
                self.x_hasse = self.movement(x_start_h, x_end_h, t_start_h, t_end_h, frame_time)

            if t_start_a < frame_time < t_end_a:
                print("ada:", self.x_ada)
                self.x_ada = self.movement(x_start_a, x_end_a, t_start_a, t_end_a, frame_time)

            if frame_time > frame_time_max:
                self.current_frame = "third"
                self.frame_start_time = pygame.time.get_ticks()

        elif self.current_frame == "third":
            """Hasse->"""
            frame_time_max = 5000
            x_start_h = 0
            x_end_h = 290
            t_start_h = 0
            t_end_h = 4000

            if t_start_h < frame_time < t_end_h:
                print("hasse:", self.x_hasse)
                self.x_hasse = self.movement(x_start_h, x_end_h, t_start_h, t_end_h, frame_time)

            if frame_time > frame_time_max:
                self.current_frame = "fourth"
                self.frame_start_time = pygame.time.get_ticks()

        elif self.current_frame == "fourth":
            print("in fourth")
            """Hasse"""
            frame_time_max = 6000
            x_start_h = 290
            x_end_h = 290
            t_start_h = 0
            t_end_h = 6000

            if t_start_h < frame_time < t_end_h:
                print("hasse:", self.x_hasse)
                y_off = 1 * math.sin(1 * frame_time * math.pi / 1000)
                self.y_hasse += y_off

            if frame_time > frame_time_max:
                self.current_frame = "fifth"
                self.frame_start_time = pygame.time.get_ticks()

        elif self.current_frame == "fifth":
            """Hasse->"""
            frame_time_max = 9000
            x_start_h = 290
            x_end_h = 850
            t_start_h = 0
            t_end_h = 5000

            if t_start_h < frame_time < t_end_h:
                print("hasse:", self.x_hasse)
                self.x_hasse = self.movement(x_start_h, x_end_h, t_start_h, t_end_h, frame_time)

            if frame_time > frame_time_max:
                self.current_frame = "first"
                self.frame_start_time = pygame.time.get_ticks()


    def handle_timer(self):
        time_now = pygame.time.get_ticks()
        self.animation(time_now)
        return self

    def render(self, screen):
        screen.fill(WHITE)
        screen.blit(start_bg, (0, 0))
        screen.blit(logo, (73, -45))
        screen.blit(self.gunnar.image, (self.x_hasse, self.y_hasse))
        screen.blit(self.ada.image, (self.x_ada, 200))
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
        screen.blit(start_bg, (0, 0))
        screen.blit(logo, (73, -45))
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
        screen.blit(start_bg, (0, 0))
        screen.blit(self.instructions_frame, (75, 75))
        self.back_button.render(screen)
        self.quit_button.render(screen)
