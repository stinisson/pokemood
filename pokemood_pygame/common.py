import math
import textwrap
import pygame
from pygame import mixer

from constants import *

bg = pygame.image.load("media/images/Background_forest.jpg")
background = pygame.transform.smoothscale(bg, SCREEN_SIZE)

logo = pygame.image.load("media/images/LOGO.PNG")
logo = pygame.transform.smoothscale(logo, (360, 222))

start_background = pygame.image.load("media/images/background_start.png")
start_background = pygame.transform.scale(start_background, SCREEN_SIZE)


class TextBox:
    def __init__(self, rel_pos, font_size, font_bold, color, text, font_name=FONT_ROBOTO, line_width=100):
        self.position = (SCREEN_SIZE[0] * rel_pos[0], SCREEN_SIZE[1] * rel_pos[1])
        self.font_size = font_size
        self.font = pygame.font.Font(font_name, font_size)
        self.font.set_bold(font_bold)
        self.color = color
        self.text_lines = []
        self.text_lines_shadow = []
        self.line_width = line_width
        self.set_text(text)

    def set_text(self, text):
        lines_specified_width = textwrap.fill(text, self.line_width)
        chopped_lines = lines_specified_width.split('\n')
        self.text_lines = []
        self.text_lines_shadow = []
        for line in chopped_lines:
            line_surface = self.font.render(line, True, self.color)
            self.text_lines.append(line_surface)
            line_surface_shadow = self.font.render(line, True, BLACK)
            self.text_lines_shadow.append(line_surface_shadow)

    def render(self, screen):
        # shadow
        for idx, text_surface_shadow in enumerate(self.text_lines_shadow):
            text_rect_shadow = text_surface_shadow.get_rect()
            text_rect_shadow.center = self.position[0] + 1, self.position[1] + 2 + idx * (self.font_size + 15)
            screen.blit(text_surface_shadow, text_rect_shadow)

        for idx, text_surface in enumerate(self.text_lines):
            text_rect = text_surface.get_rect()
            text_rect.center = self.position[0], self.position[1] + idx * (self.font_size + 15)
            screen.blit(text_surface, text_rect)


class Button:
    def __init__(self, rel_pos, rel_size, color, highlight, font_size, font_color, text, frame=QUIZ_DARKGREEN):
        self.position = (SCREEN_SIZE[0] * rel_pos[0], SCREEN_SIZE[1] * rel_pos[1])
        self.size = (SCREEN_SIZE[0] * rel_size[0], SCREEN_SIZE[1] * rel_size[1])
        self.color = color
        self.highlight = highlight
        self.text = TextBox(rel_pos=rel_pos, font_name=FONT_ROBOTO,
                            font_size=font_size, font_bold=False, color=font_color, text=text, line_width=28)
        self.button_rect = pygame.Rect(self.position[0], self.position[1], self.size[0] - 3, self.size[1] - 3)
        self.button_rect.center = self.position[0], self.position[1]
        self.button_frame_rect = pygame.Rect(0, 0, self.size[0], self.size[1])  # x, y, width, height
        self.button_frame_rect.center = self.position[0], self.position[1]
        self.enabled = True
        self.frame = frame

    def handle_mouse_button(self, mouse_button):
        mouse_pos = pygame.mouse.get_pos()
        if self.button_rect.collidepoint(mouse_pos) and mouse_button == 1 and self.enabled:
            return True
        else:
            return False

    def render(self, screen):
        pygame.draw.rect(screen, self.frame, self.button_frame_rect, 4)  # button frame

        mouse_pos = pygame.mouse.get_pos()
        if self.button_rect.collidepoint(mouse_pos) and self.enabled:  # If mouse on button - highlight button
            if len(self.highlight) == 4:
                s = pygame.Surface((self.button_rect.width, self.button_rect.height),
                                   pygame.SRCALPHA)  # per-pixel alpha
                s.fill(self.highlight)  # notice the alpha value in the color
                screen.blit(s, self.button_rect)
            else:
                pygame.draw.rect(screen, self.highlight, self.button_rect)
        else:
            if len(self.color) == 4:
                s = pygame.Surface((self.button_rect.width, self.button_rect.height),
                                   pygame.SRCALPHA)  # per-pixel alpha
                s.fill(self.color)  # notice the alpha value in the color
                screen.blit(s, self.button_rect)
            else:
                pygame.draw.rect(screen, self.color, self.button_rect)

        self.text.render(screen)


class InputBox:
    def __init__(self, rel_pos, rel_size, color, highlight, font_size, font_color):
        self.cursor = ""
        self.timeout = 0
        self.button = Button(rel_pos, rel_size, color, highlight, font_size, font_color, self.cursor)
        self.active = False
        self.text = ""
        self.finished = False

    def handle_keydown(self, key):
        alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ "

        if not self.finished:
            mods = pygame.key.get_mods()
            if key == pygame.K_RETURN:
                print(self.text)
                print("managed return")
                self.finished = True
            elif key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif key == pygame.K_SPACE:
                if len(self.text) < 15:
                    self.text += " "
            elif mods & pygame.KMOD_LSHIFT:
                if pygame.key.name(key) in alphabet:
                    if mods & pygame.KMOD_LSHIFT:
                        self.text += pygame.key.name(key).upper()
            elif pygame.key.name(key) in alphabet:
                if len(self.text) < 15:
                    self.text += pygame.key.name(key)
        return self

    def handle_mouse_button(self, button):
        if button == 1:
            self.button.handle_mouse_button(button)
        return self

    def handle_timer(self):
        if self.finished:
            self.button.text.set_text(self.text)
        else:
            self.button.text.set_text(self.text)
            time_now = pygame.time.get_ticks()
            if (time_now - self.timeout) % 2000 < 1000:
                if self.text:
                    self.button.text.set_text(self.text + "|")
                else:
                    self.button.text.set_text("|")
        return self

    def render(self, screen):
        self.button.render(screen)


class Screen:
    def __init__(self):
        pass

    def handle_keydown(self, key):
        return self

    def handle_mouse_button(self, button):
        return self

    def handle_timer(self):
        return self

    def render(self, screen):
        return self


def periodic_movement(frequency, amplitude):
    time = pygame.time.get_ticks()
    x_off = amplitude * math.cos(frequency * time * math.pi / 1000)
    y_off = amplitude * math.sin(frequency * time * math.pi / 1000)
    return x_off, y_off


def rel_to_pix(rel_pos):
    x = rel_pos[0] * SCREEN_SIZE[0]
    y = rel_pos[1] * SCREEN_SIZE[1]
    pix_pos = (x, y)
    return pix_pos


def music(filename, volume):
    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(volume)


def sound(filename):
    sound = mixer.Sound(filename)
    sound.play()
    sound.set_volume(0.0)
