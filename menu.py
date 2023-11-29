import pygame.mouse
import spritesheet
from base import BaseState
from settings import SKINS
from spritesheet_skins import get_skins
from save_game import get_best_score
from font_util import outline


class Menu(BaseState):
    def __init__(self):
        super(Menu, self).__init__()
        self.background = None
        self.logo = None
        self.start_button = None
        self.start_button_rect = None
        self.next_skin_button = None
        self.next_skin_button_rect = None
        self.previous_skin_button = None
        self.previous_skin_button_rect = None
        self.selected_skin = None
        self.selected_skin_rect = None
        self.selected_index = 0
        self.skins = {}
        self.load_images()
        self.load_rect()
        self.font = pygame.font.Font("./assets/fonts/PixeloidSansBold.ttf", 18)
        self.skin_name = self.font.render(
            self.skins[list(self.skins.keys())[self.selected_index]]["name"], True, "White")
        self.skin_name_rect = self.skin_name.get_rect(
            center=(self.screen_rect.centerx, self.selected_skin_rect.bottom + 20))
        self.next_state = "GAMEPLAY"
        self.persist["best_score"] = get_best_score()

    def load_images(self):
        ss = spritesheet.SpriteSheet("assets/sprites/sprites.png")
        self.background = pygame.transform.scale(ss.image_at((0, 0, 143, 255)), self.screen_rect.size)
        self.logo = pygame.transform.scale_by(ss.image_at((351, 91, 89, 24)), 3)
        self.logo.set_colorkey("Black")
        self.start_button = pygame.transform.scale_by(ss.image_at((354, 118, 52, 29)), 2.5)
        self.start_button.set_colorkey("Black")
        self.next_skin_button = pygame.transform.scale_by(ss.image_at((334, 142, 13, 14)), 2)
        self.previous_skin_button = pygame.transform.flip(self.next_skin_button, True, False)
        self.load_skins()
        self.selected_skin = self.skins[list(self.skins.keys())[self.selected_index]]["sprites"][1]

    def load_skins(self):
        data = SKINS
        for i in data:
            self.skins[i] = {
                "name": data[i]["name"],
                "sprites": get_skins(data[i]["path"], 17, 12, 3)
            }

    def load_rect(self):
        self.start_button_rect = self.start_button.get_rect(center=(
            self.screen_rect.center[0], self.screen_rect.center[1] + 150))
        self.selected_skin_rect = self.selected_skin.get_rect(center=self.screen_rect.center)
        self.next_skin_button_rect = self.next_skin_button.get_rect(center=(
            self.selected_skin_rect.topright[0] + 50, self.selected_skin_rect.center[1]))
        self.previous_skin_button_rect = self.previous_skin_button.get_rect(center=(
            self.selected_skin_rect.topleft[0] - 50, self.selected_skin_rect.center[1]))

    def update(self, dt):
        self.selected_skin = self.skins[list(self.skins.keys())[self.selected_index]]["sprites"][1]
        self.persist["skin"] = self.skins[list(self.skins.keys())[self.selected_index]]["sprites"]
        self.skin_name = self.font.render(
            self.skins[list(self.skins.keys())[self.selected_index]]["name"], True, "White")
        self.skin_name_rect = self.skin_name.get_rect(
            center=(self.screen_rect.centerx, self.selected_skin_rect.bottom + 20))

    def get_event(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_position = pygame.mouse.get_pos()
            if self.start_button_rect.collidepoint(mouse_position):
                self.done = True
            elif self.next_skin_button_rect.collidepoint(mouse_position):
                self.change_skin(1)
            elif self.previous_skin_button_rect.collidepoint(mouse_position):
                self.change_skin(-1)

    def change_skin(self, direction):
        length = len(self.skins)
        self.selected_index = (self.selected_index + direction) % length

    def draw(self, surface):
        surface.fill("Black")
        surface.blit(self.background, self.background.get_rect(topleft=(0, 0)))
        surface.blit(self.logo, self.logo.get_rect(
                        center=(self.screen_rect.center[0], self.screen_rect.center[1] - 200)))
        surface.blit(self.start_button, self.start_button_rect)
        surface.blit(self.selected_skin, self.selected_skin_rect)
        surface.blit(self.previous_skin_button, self.previous_skin_button_rect)
        surface.blit(self.next_skin_button, self.next_skin_button_rect)
        outline(self.skin_name, self.skin_name_rect, surface)
