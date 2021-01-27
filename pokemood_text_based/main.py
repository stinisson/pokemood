"""Pokemon Battle GO!"""

from pokemood_text_based.cards import card_attack, card_block, chance_card_attack, chance_card_health, quiz_card, \
    show_stats_card, intro_card
from pokemood_text_based.cards_helper import take_integer_input
from pokemood_text_based.common import choose_poketer
from pokemood_text_based.user import User
from pokemood_text_based.poketer import Poketer
import random
from termcolor import colored
import colorama
import sys

colorama.init()
from pokemood_text_based.print_module import print_frame, draw_welcome_screen, poketer_mood_explanation_text, draw_end_screen


def cpu_make_move(user, user_pokemon, cpu, cpu_pokemon, live):
    cpu_extra_s = (colored("s", cpu_pokemon.color))
    print(f"\nNu är det {cpu.name}{cpu_extra_s} tur!")

    # TODO implement cpu make quiz move
    #moves = ["attack", "block", "chance_card_attack", "chance_card_health", 'quiz']
    moves = ["attack", "block", "chance_card_attack", "chance_card_health"]

    move = random.choice(moves)

    if move == "attack":
        card_attack(user_pokemon=user.team[0], cpu=cpu, cpu_pokemon=cpu_pokemon, is_cpu=True)

    elif move == "block":
        card_block(user=user, user_pokemon=user.team[0], cpu=cpu, cpu_pokemon=cpu_pokemon, is_cpu=True)

    elif move == "chance_card_attack":
        chance_card_attack(player=cpu, poketer=cpu_pokemon, is_cpu=True, live=live)

    elif move == "chance_card_health":
        chance_card_health(player=cpu, poketer=cpu_pokemon, is_cpu=True)

    # elif move == "quiz":
    #     quiz_card(player=cpu, poketer=cpu_pokemon, is_cpu=True)


def check_is_winner(user, cpu):
    for poketer in user.team:
        if poketer.get_health() <= 0:
            user.team.remove(poketer)

    for poketer in cpu.team:
        if poketer.get_health() <= 0:
            cpu.team.remove(poketer)

    if len(user.team) == 0:
        return "cpu"
    elif len(cpu.team) == 0:
        return "user"
    else:
        return None


def game_loop(user, user_pokemon, cpu, cpu_pokemon, live, available_poketers):
    while True:
        print("\nVad vill du göra?")
        choices = {1: "Attackera", 2: "Blockera", 3: "Chanskort - attack", 4: "Chanskort - hälsa",
                   5: "Quiz - vinn en ny Poketer", 6: "Visa status", 7: "Avsluta spelet"}

        for choice in choices:
            print(choice, choices[choice])

        user_choice = take_integer_input(f">> ", len(choices) + 1, f"Ange en siffra 1-{len(choices)}.")

        if user_choice == 1:
            card_attack(user_pokemon=user.team[0], cpu=cpu, cpu_pokemon=cpu_pokemon, is_cpu=False)

        elif user_choice == 2:
            card_block(user=user, user_pokemon=user.team[0], cpu=cpu, cpu_pokemon=cpu_pokemon, is_cpu=False)

        elif user_choice == 3:
            chance_card_attack(player=user, poketer=user.team[0], is_cpu=False, live=live)

        elif user_choice == 4:
            chance_card_health(player=user, poketer=user.team[0], is_cpu=False)

        elif user_choice == 5:
            quiz_card(player=user, poketer=user.team[0], is_cpu=False, available_poketers=available_poketers)

        elif user_choice == 6:
            show_stats_card(user=user, cpu=cpu)
            continue

        elif user_choice == 7:
            print("Avslutar spelet..")
            sys.exit(0)

        is_winner = check_is_winner(user=user, cpu=cpu)
        if is_winner is None:
            pass
        else:
            return is_winner

        cpu_make_move(user=user, user_pokemon=user_pokemon, cpu=cpu, cpu_pokemon=cpu_pokemon, live=live)

        is_winner = check_is_winner(user=user, cpu=cpu)
        if is_winner is None:
            pass
        else:
            return is_winner


def start_game(live):
    draw_welcome_screen()
    username = input("Vänligen ange ditt namn: ")
    poketer_mood_explanation_text(username)
    input("\nTryck enter för att fortsätta\n")

    gunnar = Poketer(colored("Glada Gunnar", 'yellow'), 'happy', 'yellow', 50, 50, 45, catchword="#YOLO")
    ada = Poketer(colored("Aggressiva Ada", 'red'), 'angry', 'red', 50, 50, 45, catchword="#FTW")
    louise = Poketer(colored("Ledsna Louise", 'blue'), 'sad', 'blue', 50, 50, 45, catchword="#TGIF")
    kalle = Poketer(colored("Kärleksfulla Kalle", 'magenta'), 'loving', 'magenta', 50, 50, 45, catchword="#XOXO")
    available_poketers = [gunnar, ada, louise, kalle]

    user_pokemon = choose_poketer(available_poketers, is_cpu=False)
    cpu_pokemon = choose_poketer(available_poketers, is_cpu=True)

    user = User(colored(username, user_pokemon.color))
    user.add_team(user_pokemon)

    cpu = User(colored("Olof", cpu_pokemon.color))
    cpu.add_team(cpu_pokemon)

    x = f"\n{user.name}, din Poketer är {user_pokemon.name}."
    y = user_pokemon.get_stats()
    print_frame([x, y], user_pokemon.color, 15)

    x = f"Din motståndare är {cpu.name}. {cpu.name} valde poketer {cpu_pokemon.name}. {cpu_pokemon.get_stats()}"
    print_frame([x], cpu_pokemon.color, 15)

    input("\nTryck enter för att fortsätta")

    intro_card(poketer=user_pokemon, is_cpu=False, live=live)
    intro_card(poketer=cpu_pokemon, is_cpu=True, live=live)

    is_winner = game_loop(user=user, user_pokemon=user_pokemon, cpu=cpu, cpu_pokemon=cpu_pokemon, live=live, available_poketers=available_poketers)

    if is_winner == "user":
        x = "Grattis! Du vann! Lejon jämför sig inte med människor - Ibrahimovic."
        draw_end_screen(x, user_pokemon.color, 15)
    else:
        x = "Du förlorade! Du kan inte vinna om du inte lär dig hur man förlorar - Abdul-Jabbar."
        draw_end_screen(x, user_pokemon.color, 15)


if __name__ == '__main__':
    start_game(live=False)
