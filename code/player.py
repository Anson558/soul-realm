import pygame
from entities import Character
from tools import Animation, load_cut_image, load_image
from bullets import PlayerBullet

class Player(Character):
    def __init__(self, main, pos):
        super().__init__(main, pos, pygame.math.Vector2(10, 13), load_cut_image('player/idle.png'))
        self.main = main
        self.idle_anim = Animation(load_cut_image('player/idle.png'), 12)
        self.run_anim = Animation(load_cut_image('player/run.png'), 8)
        self.type = 'player'
        self.damagers = ['enemy', 'enemy_bullet']
        self.speed = 1.8
        self.health = 1
        self.damage = 0
        self.shoot_cooldown = 15
        self.shoot_sound = pygame.mixer.Sound('audio/shoot.wav')
        self.shoot_sound.set_volume(0.15)

    def update(self):
        super().update()
        self.move()
        self.shoot()
        self.animate()

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_d]:
            self.velocity.x = self.speed
        elif keys[pygame.K_a]:
            self.velocity.x = -self.speed
        else:
            self.velocity.x = 0

        if keys[pygame.K_s]:
            self.velocity.y = self.speed
        elif keys[pygame.K_w]:
            self.velocity.y = -self.speed
        else:
            self.velocity.y = 0

    def shoot(self):
        mouse = pygame.mouse
        self.time_since_shot += 1

        if mouse.get_pressed()[0]:
            if self.time_since_shot > self.shoot_cooldown:
                self.shoot_sound.play()
                self.time_since_shot = 0
                self.main.entities.append(PlayerBullet(self.main, pygame.math.Vector2(self.rect.centerx, self.rect.centery)))

    def animate(self):
        self.idle_anim.play()
        self.run_anim.play()

        if self.velocity.x > 0:
            self.image = self.run_anim.image
            self.flip = False
        elif self.velocity.x < 0:
            self.image = self.run_anim.image
            self.flip = True
        elif self.velocity.y > 0:
            self.image = self.run_anim.image
        elif self.velocity.y < 0:
            self.image = self.run_anim.image
        else:
            self.image = self.idle_anim.image

    def die(self):
        self.main.set_menu()
