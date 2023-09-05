import pygame

class Tile():
    def __init__(self, main, pos, image):
        self.main = main
        self.image = image
        self.rect = pygame.FRect(pos.x, pos.y, self.image.get_width(), self.image.get_height())

    def draw(self, display):
        display.blit(self.image, self.rect.topleft - self.main.scroll)