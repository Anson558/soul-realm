import pygame
import random
from tools import *
from enemies import *

class EnemySpawner():
    def __init__(self, main):
        self.main = main
        self.most_spawn_rate = 150
        self.spawn_rate = self.most_spawn_rate
        self.least_spawn_rate = 50
        self.time_since_spawn = 0

    def update(self):
        self.time_since_spawn += 1
        if self.spawn_rate > self.least_spawn_rate:
                self.spawn_rate -= 0.015
        print(self.spawn_rate)

        if self.time_since_spawn > self.spawn_rate:
            self.time_since_spawn = 0
            self.main.spawn_points.append(SpawnPoint(self.main, pygame.math.Vector2(
                random.randrange(150, 750),
                random.randrange(150, 350)
            )))

class SpawnPoint():
    def __init__(self, main, pos):
        self.main = main
        self.image = load_cut_image('enemies/spawn_point.png')[0]
        self.rect = pygame.FRect(pos.x, pos.y, self.image.get_width(), self.image.get_height())
        self.anim = Animation(load_cut_image('enemies/spawn_point.png'), 15)

        self.time_alive = 0
        self.spawn_time = 150

    def update(self):
        self.animate()

        self.time_alive += 1
        if self.time_alive > self.spawn_time:
            self.main.entities.append(
                random.choice([
                    FollowingEnemy, 
                    FollowingEnemy, 
                    FollowingEnemy,
                    FollowingEnemy,
                    TankEnemy, 
                    TankEnemy, 
                    TankEnemy,
                    ShootingEnemy,
                    ShootingEnemy, 
                    ShootingEnemy, 
                    ShootingEnemy,
                    ShootingEnemy,
                    SnipingEnemy,
                    SnipingEnemy, 
                    FastEnemy, 
                    FastEnemy, 
                    FastEnemy,
                    ]
                )(self.main, pygame.math.Vector2(self.rect.x, self.rect.y)))
            self.main.spawn_points.remove(self)
            
    def draw(self, display):
        display.blit(self.image, self.rect.topleft - self.main.scroll)

    def animate(self):
        self.anim.play()
        self.image = self.anim.image
