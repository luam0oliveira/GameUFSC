import pygame
import random
from settings import DISTANCE_BETWEEN_OBJECTS, DISTANCE_BETWEEN_PAIR_OBJECTS


class Obstacle(pygame.sprite.Sprite):
    distance_between_obstacle = DISTANCE_BETWEEN_OBJECTS
    distance_between_pair = DISTANCE_BETWEEN_PAIR_OBJECTS

    def __init__(self, image, **kwargs):
        super().__init__()
        self.image = image
        self.scored = False
        self.image.set_colorkey("Black")
        if kwargs.get("bottomleft"):
            bottomleft = kwargs.get("bottomleft")
            self.rect = self.image.get_rect(bottomleft=bottomleft)
        elif kwargs.get("topleft"):
            topleft = kwargs.get("topleft")
            self.rect = self.image.get_rect(topleft=topleft)
        self.is_active = True
        self.velocity = -3

    def apply_velocity(self):
        self.rect.x += self.velocity

    @staticmethod
    def generate_positions_of_objects():
        bottom_position = random.randint(250, 500)
        top_position = bottom_position - DISTANCE_BETWEEN_OBJECTS
        return bottom_position, top_position

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

    def update(self):
        if self.is_active:
            self.destroy()
            self.apply_velocity()
