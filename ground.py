import pygame
from settings import HEIGHT


class Ground(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(bottomleft=(0, HEIGHT))

    def apply_velocity(self):
        self.rect.x -= 3
        if self.rect.x <= -100:
            self.rect.x = 0

    def update(self):
        self.apply_velocity()
