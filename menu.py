import pygame.mouse
import spritesheet
from base import BaseState
from settings import SKINS
from spritesheet_skins import get_skins


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
        self.next_state = "GAMEPLAY"

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
        self.persist = {
            "skin": self.skins[list(self.skins.keys())[self.selected_index]]["sprites"]
        }

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

# class Menu:
#     def __init__(self,
#                  app,
#                  background_image,
#                  logo_image,
#                  play_button_image,
#                  skins,
#                  next_image,
#                  previous_image,
#                  skin_changer_fn):
#         self.app = app
#         self.background = background_image
#         self.logo = logo_image
#         self.skins = skins
#         self.play_button_surf = play_button_image
#         self.skin_changer = SkinChanger(app, self.skins, next_image, previous_image, skin_changer_fn)
#         self.play_button_rect = self.play_button_surf.get_rect(
#             center=(int(WIDTH / 2) + 1, int(HEIGHT / 2 + 200)))
#
#     def draw(self):
#         self.app.screen.blit(self.background, self.background.get_rect(topleft=(0, 0)))
#         self.app.screen.blit(self.logo, self.logo.get_rect(center=(int(self.app.dimensions[0] / 2), 150)))
#         self.app.screen.blit(self.play_button_surf, self.play_button_rect)
#         self.skin_changer.draw(self.app.screen)
#         self.get_commands()
#
#     def get_commands(self):
#         mouse_click = pygame.mouse.get_pressed()[0]
#         on_button_play = self.play_button_rect.collidepoint(pygame.mouse.get_pos())
#
#         if self.app.state == 0 and mouse_click and on_button_play:
#             self.start_game()
#
#     def start_game(self):
#         self.app.state = 1
#         self.app.is_loading = True
#         self.app.flappy_bird.is_loading = False
#         pygame.time.delay(150)
#         self.app.is_loading = False
#
# class SkinChanger:
#     def __init__(self, app, skins, next_image, previous_image, change_skin_fn):
#         self.app = app
#         self.fn = change_skin_fn
#         self.skins = skins
#         self.skins_names = list(skins.keys())
#         self.num_skins = len(self.skins_names)
#         self.index_selected = 0
#         self.selected = self.skins[self.skins_names[self.index_selected]]["sprites"][1]
#         self.selected_rect = self.selected.get_rect(center=(int(WIDTH / 2), int(HEIGHT / 2)))
#         self.font = pygame.font.Font(FONTS["bold"], 16)
#         self.text = self.font.render(self.skins[self.skins_names[self.index_selected]]["name"], False, "Black")
#         self.text_rect = self.text.get_rect(center=(int(WIDTH / 2), int(HEIGHT / 2) + 40))
#         self.next_button_surf = next_image
#         self.next_button_rect = self.next_button_surf.get_rect(
#             center=(self.selected_rect.topright[0] + 50, self.selected_rect.center[1]))
#         self.previous_button_surf = previous_image
#         self.previous_button_rect = self.previous_button_surf.get_rect(
#             center=(self.selected_rect.topleft[0] - 50, self.selected_rect.center[1]))
#
#     def draw(self, screen):
#         screen.blit(self.selected, self.selected_rect)
#         screen.blit(self.next_button_surf, self.next_button_rect)
#         screen.blit(self.previous_button_surf, self.previous_button_rect)
#         outline(self.text, self.text_rect, screen)
#         screen.blit(self.text, self.text_rect)
#         self.controls()
#
#     def update_text(self):
#         self.text = self.font.render(self.skins[self.skins_names[self.index_selected]]["name"], False, "Black")
#         self.text_rect = self.text.get_rect(center=(int(WIDTH / 2), int(HEIGHT / 2) + 40))
#
#     def controls(self):
#         mouse_click = pygame.mouse.get_pressed()[0]
#         mouse_pos = pygame.mouse.get_pos()
#
#         on_next_button = self.next_button_rect.collidepoint(mouse_pos)
#         on_previous_button = self.previous_button_rect.collidepoint(mouse_pos)
#
#         if self.app.state == 0 and mouse_click and (on_previous_button or on_next_button):
#             if on_next_button:
#                 self.next_skin()
#             elif on_previous_button:
#                 self.previous_skin()
#
#             pygame.time.delay(100)
#             self.fn(self.skins_names[self.index_selected])
#             self.update_text()
#
#     def next_skin(self):
#         self.index_selected = (self.index_selected + 1) % self.num_skins
#         self.selected = self.skins[self.skins_names[self.index_selected]]["sprites"][1]
#
#     def previous_skin(self):
#         self.index_selected = (self.index_selected - 1) % self.num_skins
#         self.selected = self.skins[self.skins_names[self.index_selected]]["sprites"][1]
