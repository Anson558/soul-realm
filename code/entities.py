import pygame
from tools import load_cut_image, load_image, Animation

class Entity():
    def __init__(self, main, pos : pygame.math.Vector2, size : pygame.math.Vector2, images : pygame.Surface):
        self.type = ''
        self.main = main
        self.image = images[0]
        self.flip = False
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = pygame.FRect(pos.x, pos.y, size.x, size.y)
        self.speed = 1
        self.velocity = pygame.math.Vector2(0, 0)
        self.colliding = False

    def update(self):
        if self.velocity != pygame.math.Vector2(0, 0):
            self.velocity = self.velocity.normalize()
        else:
            self.velocity = self.velocity

        self.colliding = False

        self.rect.x += self.velocity.x * self.speed
        for tile in self.main.walls:
            if self.rect.colliderect(tile):
                self.colliding = True
                if self.velocity.x > 0:
                    self.rect.right = tile.rect.left
                elif self.velocity.x < 0:
                    self.rect.left = tile.rect.right

        self.rect.y += self.velocity.y * self.speed
        for tile in self.main.walls:
            if self.rect.colliderect(tile):
                self.colliding = True
                if self.velocity.y > 0:
                    self.rect.bottom = tile.rect.top
                    self.velocity.y = 0
                elif self.velocity.y < 0:
                    self.rect.top = tile.rect.bottom
                    self.velocity.y = 0

    def draw(self, display : pygame.Surface):
        display.blit(pygame.transform.flip(self.image, self.flip, False), (self.rect.centerx - self.image.get_width()/2, self.rect.bottom - self.image.get_height()) - self.main.scroll)

    def die(self):
        self.main.entities.remove(self)

    def get_direction_to_target(self, target : pygame.math.Vector2):
        if target != NotImplemented:
            return pygame.math.Vector2(target - pygame.math.Vector2(self.rect.centerx, self.rect.centery)).normalize()
        return pygame.math.Vector2(0, 0)

class Character(Entity):
    def __init__(self, main, pos : pygame.math.Vector2, size : pygame.math.Vector2, images : pygame.Surface):
        super().__init__(main, pos, size, images)
        self.damagers = ['']
        self.health = 3
        self.damage = 1
        self.iframes = 7
        self.time_since_hit = 0
        self.shoot_cooldown = 40
        self.time_since_shot = 0

    def update(self):
        super().update()
        self.time_since_hit += 1

        for damager in self.damagers:
            for entity in self.main.entities:
                if entity.type == damager:
                    if self.rect.colliderect(entity.rect):
                        if self.time_since_hit > self.iframes:
                            self.time_since_hit = 0
                            self.health -= 1

        if self.health <= 0:
            self.health = 0
            self.die()