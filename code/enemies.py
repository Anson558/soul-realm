import pygame
from entities import Character
from bullets import ShootingBullet, SnipingBullet
from tools import *

class Enemy(Character):
    def __init__(self, main, pos : pygame.math.Vector2, size : pygame.math.Vector2, images : list):
        super().__init__(main, pos, size, images)
        self.images = images
        self.type = 'enemy'
        self.damagers = ['player_bullet']
        self.anim = Animation(self.images, 15)
        self.speed = 1
        self.health = 3
        self.damage = 1
        self.die_sound = pygame.mixer.Sound('audio/die.wav')

    def update(self):
        super().update()
        self.animate()

    def animate(self):
        self.anim.play()
        self.image = self.anim.image

    def follow(self):
        for entity in self.main.entities:
            if entity.type == 'player':
                self.velocity = self.get_direction_to_target(entity.rect.center)

    def shoot(self, bullet_type):
        self.time_since_shot += 1

        if self.time_since_shot > self.shoot_cooldown:
            self.time_since_shot = 0
            self.main.entities.append(bullet_type(self.main, pygame.math.Vector2(self.rect.centerx, self.rect.centery)))

    def die(self):
        self.die_sound.play()
        super().die()

class FollowingEnemy(Enemy):
    def __init__(self, main, pos : pygame.math.Vector2):
        super().__init__(main, pos, pygame.math.Vector2(12, 15), load_cut_image('enemies/following_enemy.png'))
        self.type = 'enemy'
        self.anim = Animation(self.images, 15)
        self.speed = 1
        self.health = 4
        self.damage = 1

    def update(self):
        super().update()
        self.follow()
        self.animate()

class TankEnemy(Enemy):
    def __init__(self, main, pos : pygame.math.Vector2):
        super().__init__(main, pos, pygame.math.Vector2(25, 22), load_cut_image('enemies/tank_enemy.png', 32))
        self.type = 'enemy'
        self.anim = Animation(self.images, 25)
        self.speed = 0.25
        self.health = 10
        self.damage = 1

    def update(self):
        super().update()
        self.follow()
        self.animate()

class ShootingEnemy(Enemy):
    def __init__(self, main, pos : pygame.math.Vector2):
        super().__init__(main, pos, pygame.math.Vector2(12, 15), load_cut_image('enemies/shooting_enemy.png'))
        self.type = 'enemy'
        self.anim = Animation(self.images, 15)
        self.speed = 0.5
        self.health = 4
        self.damage = 1
        self.follow_radius = 120
        self.shoot_cooldown = 25

    def update(self):
        super().update()
        for entity in self.main.entities:
            if entity.type == 'player':
                if pygame.math.Vector2(self.rect.centerx, self.rect.centery).distance_to(pygame.math.Vector2(entity.rect.centerx, entity.rect.centery)) > self.follow_radius:
                    self.follow()
                else:
                    self.velocity = pygame.math.Vector2(0, 0)

        self.shoot(ShootingBullet)
        self.animate()

class SnipingEnemy(Enemy):
    def __init__(self, main, pos : pygame.math.Vector2):
        super().__init__(main, pos, pygame.math.Vector2(12, 15), load_cut_image('enemies/sniping_enemy.png'))
        self.type = 'enemy'
        self.anim = Animation(self.images, 15)
        self.speed = 0.5
        self.health = 4
        self.damage = 1
        self.follow_radius = 150
        self.shoot_cooldown = 35

    def update(self):
        super().update()
        for entity in self.main.entities:
            if entity.type == 'player':
                if pygame.math.Vector2(self.rect.centerx, self.rect.centery).distance_to(pygame.math.Vector2(entity.rect.centerx, entity.rect.centery)) > self.follow_radius:
                    self.follow()
                else:
                    self.velocity = pygame.math.Vector2(0, 0)

        self.shoot(SnipingBullet)
        self.animate()

class FastEnemy(Enemy):
    def __init__(self, main, pos : pygame.math.Vector2):
        super().__init__(main, pos, pygame.math.Vector2(8, 8), load_cut_image('enemies/fast_enemy.png'))
        self.type = 'enemy'
        self.anim = Animation(self.images, 15)
        self.speed = 2
        self.health = 2
        self.damage = 1

    def update(self):
        super().update()
        self.follow()
        self.animate()