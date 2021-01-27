import textwrap
import sys
import time
from termcolor import colored, cprint
from colorama import init
init()



def draw_welcome_screen():
    print("")
    cprint(f'    Varmt välkomna till PokéMood!', 'cyan')
    cprint(f'    Ett textbaserat spel med humörstyrda Poketerer!', 'cyan')
    cprint(f'    Med hjälp av Twitter kommer du få en chans att \n    påverka din Poketers pokemör!', 'cyan')
    cprint(f'    Men passa dig, är du fel ute kan det också bli minus!\n', 'cyan')

    cprint(colored("""    ⢀⣠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
    ⣿⣿⣿⣿⣿⡏⠉⠛⢿⣿⣿Pik'a'mood-⣿⣿⣿⣿⣿⣿⣿⡿⣿
    ⣿⣿⣿⣿⣿⣿⠀⠀⠀⠈⠛⢿⣿⣿⣿-trollet⣿⣿⠿⠛⠉⠁⠀⢸
    ⣿⣿⣿⣿⣿⣿⣧⡀⠀⠀⠀⠀⠙⠿⠿⠿⠻⠿⠿⠟⠿⠛⠉⠀⠀⠀⠀⠀⣸⣿
    ⣿⣿⣿⣿⣿⣿⣿⣷⣄⠀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⣿⣿
    ⣿⣿⣿⣿⣿⣿⣿⣿⣿⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⣴⣿⣿⣿⣿
    ⣿⣿⣿⣿⣿⣿⣿⣿⡟⠀⠀⢰⣹⡆⠀⠀⠀⠀⠀⠀⣭⣷⠀⠀⠀⠸⣿⣿⣿⣿
    ⣿⣿⣿⣿⣿⣿⣿⣿⠃⠀⠀⠈⠉⠀⠀⠤⠄⠀⠀⠀⠉⠁⠀⠀⠀⠀⢿⣿⣿⣿
    ⣿⣿⣿⣿⣿⣿⣿⣿⢾⣿⣷⠀⠀⠀⠀⡠⠤⢄⠀⠀⠀⠠⣿⣿⣷⠀⢸⣿⣿⣿
    ⣿⣿⣿⣿⣿⣿⣿⣿⡀⠉⠀⠀⠀⠀⠀⢄⠀⢀⠀⠀⠀⠀⠉⠉⠁⠀⠀⣿⣿⣿
    ⣿⣿⣿⣿⣿⣿⣿⣿⣧⠀⠀⠀⠀⠀⠀⠀⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⣿⣿
    ⣿⣿⣿⣿⣿⣿⣿⣿⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿""", "yellow"))
    cprint(f'    Nu kör vi!! \n', 'yellow')


def poketer_mood_explanation_text(username):
    row1 = f"Hej {username}!"
    row2 = f"""Alla Poketerer har ett visst grundhumör. De kan vara {colored('glada', 'yellow')}, {colored('arga', 'red')}, {colored('ledsna', 'blue')} eller {colored('kärleksfulla', 'magenta')}."""
    row3 = f"{colored('Glada Poketerer trivs bäst i omgivningar med glada tillrop, skratt och uppsluppen stämning. Livet är en fest!', 'yellow')}"
    row4 = f"{colored('Arga Poketerer växer i styrka under kontroverser och fientliga förhållanden. Skjut, gräv, tig!', 'red')}"
    row5 = f"{colored('Ledsna Poketerer mår som bäst omgivna av nedstämdhet, sorg och ledsamheter. Saliga äro de som sörja!', 'blue')}"
    row6 = f"{colored('Kärleksfulla Poketerer frodas i miljöer med mycket värme, kramar och omtänksamhet. Man kan aldrig få för många kramar!', 'magenta')}"
    print_frame_with_newline([row1, row2, row3, row4, row5, row6], 'white', 15)


def delay_print(intro_text, s, a):
    print(intro_text)
    for i in s:
        sys.stdout.write(i)
        sys.stdout.flush()
        time.sleep(0.3)
    print(a)
    time.sleep(0.5)


def atk_txt(attacker, reciver, text):
    print(f"{attacker} attacks {reciver} ")
    for i in text:
        sys.stdout.write(i)
        sys.stdout.flush()
        time.sleep(0.3)
    print('''
          |
O=========|>>>>>>>>>>>>>>>>>>>>>>>>>>
          |
    ''')
    time.sleep(0.5)


def successful_block(blocker):
    print(f"{blocker} försöker blockera")
    text = "Lyckad block!"
    for i in text:
        sys.stdout.write(i)
        sys.stdout.flush()
        time.sleep(0.1)
    print('''
      |`-._/\_.-`|
      |    ||    |
      |___o()o___|
      |__((<>))__|
      \   o\/o   /
       \   ||   /
        \  ||  /
         '.||.'
    ''')


def unsuccessful_block(blocker):
    print(f"{blocker} försöker blockera")
    text = "Misslyckad block!"
    for i in text:
        sys.stdout.write(i)
        sys.stdout.flush()
        time.sleep(0.1)
    print('''
      |`-._/<    <\_.-`|
      |    |>    >|    |
      |___o(<    <)o___|
      |__((<>    >>))__|
      \   o\>   > /o   /
       \   |<    <|   /
        \  |>    <|  /
          '.|>   <|.'
    ''')


def print_frame(rows, table_color, indentation):
    print(colored("""
        ----------------------------------------------------------------------------------------------------
        *                                                                                                  *"""
                  , table_color))

    line_width = 85
    for row in rows:
        dedented_row = textwrap.dedent(row).strip()
        chopped_lines = textwrap.fill(dedented_row, line_width)
        print(textwrap.indent(chopped_lines, ' ' * indentation))

    print(colored(
        """        *                                                                                                  *
        ----------------------------------------------------------------------------------------------------"""
        , table_color))


def print_frame_with_newline(rows, table_color, indentation):
    print(colored("""
        ----------------------------------------------------------------------------------------------------
        *                                                                                                  *"""
                  , table_color))

    line_width = 85
    for row in rows:
        chopped_lines = textwrap.fill(row, line_width)
        print(textwrap.indent(chopped_lines, ' ' * indentation))
        print("")

    print(colored(
        """        *                                                                                                  *
        ----------------------------------------------------------------------------------------------------"""
        , table_color))


def draw_end_screen(text, table_color, indentation):
    print(colored("""
        ----------------------------------------------------------------------------------------------------
        ----------------------------------------------------------------------------------------------------
        *                                                                                                  *"""
                  , table_color, attrs=['blink']))

    line_width = 85
    dedented_row = textwrap.dedent(text).strip()
    chopped_lines = textwrap.fill(dedented_row, line_width)
    print(textwrap.indent(chopped_lines, ' ' * indentation))

    print(colored(
        """        *                                                                                                  *
        ----------------------------------------------------------------------------------------------------
        ----------------------------------------------------------------------------------------------------"""
        , table_color, attrs=['blink']))

def draw_loser_screen():
    pass