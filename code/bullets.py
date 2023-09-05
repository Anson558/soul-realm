import pygame
from tools import load_image, load_cut_image
from entities import Entity
import random

class Bullet(Entity):
    def __init__(self, main, pos : pygame.math.Vector2, images : list):
        super().__init__(main, pos, pygame.math.Vector2(5, 5), images)
        self.damage = 1

    def update(self):
        super().update()

        if self.colliding == True:
            self.die()

class PlayerBullet(Bullet):
    def __init__(self, main, pos : pygame.math.Vector2):
        super().__init__(main, pos, [load_image('player_bullet.png')])
        self.global_mouse_pos = pygame.math.Vector2((pygame.mouse.get_pos()[0] / self.main.game.display_multiplier) + self.main.scroll.x, (pygame.mouse.get_pos()[1] / self.main.game.display_multiplier) + self.main.scroll.y)
        self.type = 'player_bullet'
        self.speed = 6
        self.damage = 1
        self.velocity = self.get_direction_to_target(self.global_mouse_pos)

class ShootingBullet(Bullet):
    def __init__(self, main, pos : pygame.math.Vector2):
        super().__init__(main, pos, [load_image('enemy_bullet.png')])
        self.type = 'enemy_bullet'
        self.speed = 1.5
        self.damage = 1
        self.velocity = pygame.math.Vector2(random.uniform(-1, 1), random.uniform(-1, 1))
        if self.velocity == pygame.math.Vector2(0, 0):
            self.velocity = pygame.math.Vector2(1, 1)
        else:
            self.velocity.normalize()

class SnipingBullet(Bullet):
    def __init__(self, main, pos : pygame.math.Vector2):
        super().__init__(main, pos, [load_image('enemy_bullet.png')])
        self.type = 'enemy_bullet'
        self.speed = 1.5
        self.damage = 1
        for entity in self.main.entities:
            if entity.type == 'player':
                self.velocity = self.get_direction_to_target(entity.rect.center)