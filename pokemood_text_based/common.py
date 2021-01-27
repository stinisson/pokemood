import random

from pokemood_text_based.cards_helper import take_integer_input


def choose_poketer(available_poketers, is_cpu):
    if is_cpu:
        cpu_pokemon = random.choice(available_poketers)
        available_poketers.remove(cpu_pokemon)
        return cpu_pokemon
    else:
        print("Du ska nu få välja en Poketer. Dessa Pokteter är tillgängliga:")
        if len(available_poketers) > 0:
            for idx, poketer in enumerate(available_poketers):
                print(idx + 1, poketer.name)

            poketer_choice = take_integer_input(f"Vilken Poketer väljer du? (1-{len(available_poketers)}): ",
                                                len(available_poketers) + 1,
                                                f"Ogiltligt val! Ange en siffra 1-{len(available_poketers)}.")

            user_pokemon = available_poketers[poketer_choice - 1]
            available_poketers.remove(user_pokemon)
            return user_pokemon
        else:
            print("Tyvärr, det finns inga Poketerer kvar att välja bland.")
            return None
