import pygame as pg

from constants import *
from intro_screens import FirstScreen
from mood_analysis_screen import ChooseCityMoodScreen


def mainloop(screen):
    state = FirstScreen()
    #state = ChooseCityMoodScreen()
    clock = pg.time.Clock()

    while True:
        ev = pg.event.poll()

        if ev.type == pg.KEYDOWN:
            state = state.handle_keydown(ev.key)

        if ev.type == pg.MOUSEBUTTONDOWN:
            temp_state = state.handle_mouse_button(ev.button)
            if temp_state is not None:
                state = temp_state

        elif ev.type == pg.QUIT:
            break

        state = state.handle_timer()
        state.render(screen)

        pg.display.update()
        clock.tick(30)


if __name__ == '__main__':
    pg.init()
    screen = pg.display.set_mode(SCREEN_SIZE)
    pg.display.set_caption("PokeMood")
    programIcon = pg.image.load('media/images/icon.png')
    icon = pg.transform.smoothscale(programIcon, (32, 32))
    pg.display.set_icon(icon)
    mainloop(screen)
    pg.quit()
