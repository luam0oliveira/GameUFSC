import pygame
from modules.settings import FONTS, WIDTH
from modules.font_util import outline


class Score:
    def __init__(self):
        self.value = 0
        self.font = pygame.font.Font(FONTS["bold"], 32)

    def draw(self, screen):
        text = self.font.render(str(self.value), False, "White").convert_alpha()
        rect = text.get_rect(center=(int(WIDTH / 2), 40))
        outline(text, rect, screen)

    def set_score(self, score):
        self.value = score
