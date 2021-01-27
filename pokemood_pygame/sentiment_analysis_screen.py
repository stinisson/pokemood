import sys
import pygame

from constants import *
from common import TextBox, Button, InputBox, periodic_movement, rel_to_pix, Screen
from twitter.sentiment_analysis import sentiment_analysis

bg = pygame.image.load("media/images/Background_forest.jpg")
background = pygame.transform.scale(bg, SCREEN_SIZE)
screen = pygame.display.set_mode(SCREEN_SIZE)


class SentimentAnalysisScreen(Screen):
    def __init__(self, poketer, return_screen):
        self.return_screen = return_screen
        self.poketer = poketer
        health_bonus = 10
        self.info_text = f"""Twitter betting! Do you know what's trending on social media?
Write a phrase you want to search Twitter for. Guess if the latest tweets that contain this phrase are mostly positive,
mostly negative or neutral. If your guess is correct, you will be rewarded with {health_bonus} p in increased health.
If your guess is wrong, you will be punished with {health_bonus} p in reduced health. Good luck!"""
        self.text = TextBox((0.5, 0.1), 22, False, WHITE, self.info_text, line_width=65)
        self.text_keyword = TextBox((0.5, 0.52), 20, False, WHITE, "Enter a keyword:", line_width=65)

        self.input_field_keyword = InputBox((0.5, 0.6), (0.35, 0.1), QUIZ_TRANSP_GREEN_HIGHL, QUIZ_TRANSP_GREEN_HIGHL,
                                            20, WHITE)

        self.button_positions = [(0.3, 0.75), (0.5, 0.75), (0.7, 0.75)]
        self.sentiment_buttons = []
        self.attitude_options = ["Positive", "Neutral", "Negative"]
        for idx in range(len(self.button_positions)):
            self.sentiment_button = Button(self.button_positions[idx], (0.2, 0.1), QUIZ_TRANSP_GREEN_HIGHL,
                                           QUIZ_TRANSP_GREEN_LIGHT, 20, WHITE, self.attitude_options[idx])
            self.sentiment_buttons.append(self.sentiment_button)
        self.continue_button = Button((0.5, 0.9), (0.2, 0.1), QUIZ_TRANSP_GREEN_HIGHL,
                                      QUIZ_TRANSP_GREEN_LIGHT, 20, WHITE, "CONTINUE")
        self.chosen_sentiment = ""

    def handle_keydown(self, key):
        self.input_field_keyword.handle_keydown(key)
        return self

    def handle_mouse_button(self, button):
        mx, my = pygame.mouse.get_pos()
        quit_button_rect = pygame.Rect(650, 30, 140, 40)
        self.input_field_keyword.handle_mouse_button(button)
        if button == 1:
            if quit_button_rect.collidepoint((mx, my)):
                sys.exit()

            for idx, sentiment_button in enumerate(self.sentiment_buttons):
                if sentiment_button.handle_mouse_button(button):
                    sentiment_button.color = QUIZ_TRANSP_GREEN_LIGHT
                    self.chosen_sentiment = self.attitude_options[idx]
                    self.input_field_keyword.finished = True

                    # Disable buttons when a choice is made TODO UGLY TEMP FIX, FIX THIS!
                    for sentiment_button in self.sentiment_buttons:
                        sentiment_button.enabled = False

            if self.continue_button.handle_mouse_button(button):
                self.continue_button.color = QUIZ_TRANSP_GREEN_LIGHT
                return SentimentGraphScreen(keyword=self.input_field_keyword.text, attitude=self.chosen_sentiment,
                                            poketer=self.poketer, return_screen=self.return_screen)
        return self

    def handle_timer(self):
        self.input_field_keyword.handle_timer()
        return self

    def render(self, screen):
        screen.fill(WHITE)
        screen.blit(background, (0, 0))
        self.text.render(screen)
        self.text_keyword.render(screen)
        self.input_field_keyword.render(screen)
        for button in self.sentiment_buttons:
            button.render(screen)
        self.continue_button.render(screen)


class SentimentGraphScreen(Screen):
    def __init__(self, keyword, attitude, poketer, return_screen):
        self.return_screen = return_screen
        self.poketer = poketer
        self.keyword = keyword
        self.attitude = attitude.lower()
        self.result = sentiment_analysis(keyword=self.keyword, language='english',
                                         file_name="", live=True)
        self.continue_button = Button((0.5, 0.9), (0.2, 0.1), QUIZ_TRANSP_GREEN_HIGHL,
                                      QUIZ_TRANSP_GREEN_LIGHT, 20, WHITE, "CONTINUE")

        res = pygame.image.load("./twitter/sentiment_analysis.png")
        self.graph = pygame.transform.smoothscale(res, (800, 480))

    def handle_mouse_button(self, button):
        mx, my = pygame.mouse.get_pos()
        quit_button_rect = pygame.Rect(650, 30, 140, 40)
        if button == 1:
            if quit_button_rect.collidepoint((mx, my)):
                sys.exit()

            if self.continue_button.handle_mouse_button(button):
                self.continue_button.color = QUIZ_DARKGREEN
                return SentimentResultScreen(keyword=self.keyword, attitude=self.attitude, result=self.result,
                                             poketer=self.poketer, return_screen=self.return_screen)
        return self

    def handle_timer(self):
        if self.result == "too_few_results":
            return SentimentResultScreen(keyword=self.keyword, attitude=self.attitude, result=self.result,
                                         poketer=self.poketer, return_screen=self.return_screen)
        elif self.result == "connection_error":
            SentimentResultScreen(keyword=self.keyword, attitude=self.attitude, result=self.result,
                                  poketer=self.poketer, return_screen=self.return_screen)
        return self

    def render(self, screen):
        screen.fill(WHITE)
        screen.blit(self.graph, (0, 0))
        self.continue_button.render(screen)


class SentimentResultScreen(Screen):
    def __init__(self, keyword, attitude, result, poketer, return_screen):
        self.return_screen = return_screen
        self.poketer = poketer
        self.keyword = keyword
        self.attitude = attitude.lower()
        self.result = result
        if self.attitude == self.result:
            self.result_text = f"That was correct! {self.keyword} has mostly {self.result} content on Twitter. " \
                               f"You get a 10 p increase in attack strength as an award."
            self.poketer.attack += 10
        elif self.result == "too_few_results":
            self.result_text = f"Found too few tweets containing {keyword}. One tip is to search for something " \
                               f"that is more relevant in the public debate. "
        elif self.result == "connection_error":
            self.result_text = f"It is not possible to connect to Twitter right now. Try again later!"
        else:
            self.result_text = f"That was incorrect! {self.keyword} has mostly {self.result} content on Twitter. " \
                               f"You get a 10 p decrease in attack strength as a penalty."
            self.poketer.attack -= 10

        self.text = TextBox((0.5, 0.1), 22, False, WHITE, self.result_text, line_width=65)
        self.continue_button = Button((0.5, 0.9), (0.2, 0.1), QUIZ_TRANSP_GREEN_HIGHL,
                                      QUIZ_TRANSP_GREEN_LIGHT, 20, WHITE, "CONTINUE")

        self.poketer_image = pygame.image.load("media/images/Green_monster_resized.png").convert_alpha()
        self.poketer_image = pygame.transform.smoothscale(self.poketer_image, (207, 207))

    def handle_mouse_button(self, button):
        mx, my = pygame.mouse.get_pos()
        quit_button_rect = pygame.Rect(650, 30, 140, 40)
        if button == 1:
            if quit_button_rect.collidepoint((mx, my)):
                sys.exit()
            if self.continue_button.handle_mouse_button(button):
                if self.result == "too_few_results":
                    return SentimentAnalysisScreen(self.poketer, return_screen=self.return_screen)
                return self.return_screen
        return self

    def render(self, screen):
        screen.fill(WHITE)
        screen.blit(background, (0, 0))
        self.text.render(screen)
        self.continue_button.render(screen)

        x_off, y_off = periodic_movement(1, 5)
        pixel_pos = rel_to_pix((0.5, 0.55))
        poketer_image_rect = self.poketer_image.get_rect()
        poketer_image_rect.center = pixel_pos[0], pixel_pos[1] + y_off
        screen.blit(self.poketer_image, poketer_image_rect)


def mainloop(screen):
    clock = pygame.time.Clock()
    while True:
        # Event handling
        ev = pygame.event.poll()

        if ev.type == pygame.KEYDOWN:
            state = state.handle_keydown(ev.key)

        if ev.type == pygame.MOUSEBUTTONDOWN:
            temp_state = state.handle_mouse_button(ev.button)
            if temp_state is not None:
                state = temp_state

        elif ev.type == pygame.QUIT:
            break

        state = state.handle_timer()
        state.render(screen)

        pygame.display.update()
        clock.tick(30)


if __name__ == '__main__':
    pygame.init()
    mainloop(screen)
