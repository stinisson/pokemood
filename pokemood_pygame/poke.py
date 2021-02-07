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


class Hasse(Poke):
    def __init__(self):
        super().__init__(speed=90, attack=55, defence=40, hp=140, dodge=5, type="Happy",
                         moves=["Confetti", "Joke"], evolution="Hasselito")


class Confetti(Move):
    def __init__(self):
        super().__init__(damage=65, accuracy=100, type="Happy", priority=80)


class Jokes(Move):
    def __init__(self):
        super().__init__(damage=90, accuracy=100, type="Happy", priority=20)


class Happy(Type):
    def __init__(self):
        super().__init__(resistance=["Happy", "Angry"], weakness=["Sad"])


def fight(poke, opponent):
    """
    random attack of a poke to the opponent. select a move randomly with the probability given by the priority of each
    attack. the poke with the highest speed will hit first, if both pokes have the same speed it is decided randomly.
    when a poke use a Move it can't miss.
    Hit or miss:
    accuracy - opponent dodge = % to hit
    """