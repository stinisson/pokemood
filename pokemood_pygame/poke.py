import random


class Poke:
    def __init__(self, speed, attack, defence, hp, dodge, type, moves, evolution):
        self.speed = speed
        self.attk = attack
        self.defence = defence
        self.hp = hp
        self.dodge = dodge
        self.type = type
        self.moves = moves
        self.evolution = evolution

    def attack(self):
        pass


class Move:
    def __init__(self, damage, accuracy, type, priority):
        self.damage = damage
        self.accuracy = accuracy
        self.type = type
        self.priority = priority


class Type:
    def __init__(self, resistance, weakness):
        self.resistance = resistance
        self.weakness = weakness


class Happy(Type):
    def __init__(self):
        super().__init__(resistance=["Happy", "Angry"], weakness=["Sad"])


class Confetti(Move):
    def __init__(self):
        super().__init__(damage=65, accuracy=100, type="Happy", priority=80)

    def __repr__(self):
        return "confetti"


class Jokes(Move):
    def __init__(self):
        super().__init__(damage=90, accuracy=100, type="Happy", priority=20)

    def __repr__(self):
        return "jokes"


class Angry(Type):
    def __init__(self):
        super().__init__(resistance=["Angry", "Happy"], weakness=["Loving"])


class Growl(Move):
    def __init__(self):
        super().__init__(damage=65, accuracy=100, type="Angry", priority=70)

    def __repr__(self):
        return "growl"


class Curse(Move):
    def __init__(self):
        super().__init__(damage=90, accuracy=100, type="Angry", priority=30)

    def __repr__(self):
        return "curse"


class Hasse(Poke):
    def __init__(self):
        super().__init__(speed=95, attack=55, defence=40, hp=140, dodge=10, type="Happy",
                         moves=[Confetti(), Jokes()], evolution="HasseBasse")

    def __repr__(self):
        return "Hasse"


class Ada(Poke):
    def __init__(self):
        super().__init__(speed=95, attack=70, defence=30, hp=140, dodge=5, type="Angry",
                         moves=[Growl(), Curse()], evolution="Adasaur")

    def __repr__(self):
        return "Ada"


def fight_order(poke, opponent):
    if poke.speed > opponent.speed:
        print("Poke is the fastest and will make the first move")
        return [poke, opponent]
    elif opponent.speed > poke.speed:
        print("Opponent is the fastest and will make the first move")
        return [opponent, poke]
    else:
        print("Same speed, first move will be decided randomly")
        pokes = [poke, opponent]
        moves_first = random.choice(pokes)
        pokes.remove(moves_first)
        moves_last = pokes[0]
        print("Makes first move: " + str(moves_first))
        return [moves_first, moves_last]


def hit_or_miss(poke, opponent):

    probability_to_hit = poke.move.accuracy - opponent.dodge

    return probability_to_hit


def choose_move(poke):

    for i in range(len(poke.moves)):
        print(poke.moves[i], poke.moves[i].priority)


def fight(poke, opponent):
    """
    random attack of a poke to the opponent. select a move randomly with the probability given by the priority of each
    attack. the poke with the highest speed will hit first, if both pokes have the same speed it is decided randomly.
    when a poke use a Move it can't miss.
    Hit or miss:
    accuracy - opponent dodge = % to hit
    """
    choose_move(poke)
    order = fight_order(poke, opponent)
    print(order)


def main():
    hasse = Hasse()
    ada = Ada()
    fight(hasse, ada)


if __name__ == '__main__':
    main()
