import pygame


class Poketer:
    def __init__(self, name, mood, color, health, attack, catchword, img_name):
        self.name = name
        self.mood = mood
        self.health = health
        self.attack = attack
        self.color = color
        self.catchword = catchword
        self.image = pygame.image.load(img_name).convert_alpha()

    def add_health(self, health_score):
        self.health += health_score
        if self.health < 0:
            self.health = 0
