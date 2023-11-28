import pygame.mouse
from settings import WIDTH, HEIGHT, FONTS
from font_util import outline

class Menu:
    def __init__(self,
                 app,
                 background_image,
                 logo_image,
                 play_button_image,
                 skins,
                 next_image,
                 previous_image,
                 skin_changer_fn):
        self.app = app
        self.background = background_image
        self.logo = logo_image
        self.skins = skins
        self.play_button_surf = play_button_image
        self.skin_changer = SkinChanger(app, self.skins, next_image, previous_image, skin_changer_fn)
        self.play_button_rect = self.play_button_surf.get_rect(
            center=(int(WIDTH / 2) + 1, int(HEIGHT / 2 + 200)))

    def draw(self):
        self.app.screen.blit(self.background, self.background.get_rect(topleft=(0, 0)))
        self.app.screen.blit(self.logo, self.logo.get_rect(center=(int(self.app.dimensions[0] / 2), 150)))
        self.app.screen.blit(self.play_button_surf, self.play_button_rect)
        self.skin_changer.draw(self.app.screen)
        self.get_commands()

    def get_commands(self):
        mouse_click = pygame.mouse.get_pressed()[0]
        on_button_play = self.play_button_rect.collidepoint(pygame.mouse.get_pos())

        if self.app.state == 0 and mouse_click and on_button_play:
            self.start_game()

    def start_game(self):
        self.app.state = 1
        self.app.is_loading = True
        self.app.flappy_bird.is_loading = False
        pygame.time.delay(150)
        self.app.is_loading = False

class SkinChanger:
    def __init__(self, app, skins, next_image, previous_image, change_skin_fn):
        self.app = app
        self.fn = change_skin_fn
        self.skins = skins
        self.skins_names = list(skins.keys())
        self.num_skins = len(self.skins_names)
        self.index_selected = 0
        self.selected = self.skins[self.skins_names[self.index_selected]]["sprites"][1]
        self.selected_rect = self.selected.get_rect(center=(int(WIDTH / 2), int(HEIGHT / 2)))
        self.font = pygame.font.Font(FONTS["bold"], 16)
        self.text = self.font.render(self.skins[self.skins_names[self.index_selected]]["name"], False, "Black")
        self.text_rect = self.text.get_rect(center=(int(WIDTH / 2), int(HEIGHT / 2) + 40))
        self.next_button_surf = next_image
        self.next_button_rect = self.next_button_surf.get_rect(
            center=(self.selected_rect.topright[0] + 50, self.selected_rect.center[1]))
        self.previous_button_surf = previous_image
        self.previous_button_rect = self.previous_button_surf.get_rect(
            center=(self.selected_rect.topleft[0] - 50, self.selected_rect.center[1]))

    def draw(self, screen):
        screen.blit(self.selected, self.selected_rect)
        screen.blit(self.next_button_surf, self.next_button_rect)
        screen.blit(self.previous_button_surf, self.previous_button_rect)
        outline(self.text, self.text_rect, screen)
        screen.blit(self.text, self.text_rect)
        self.controls()

    def update_text(self):
        self.text = self.font.render(self.skins[self.skins_names[self.index_selected]]["name"], False, "Black")
        self.text_rect = self.text.get_rect(center=(int(WIDTH / 2), int(HEIGHT / 2) + 40))

    def controls(self):
        mouse_click = pygame.mouse.get_pressed()[0]
        mouse_pos = pygame.mouse.get_pos()

        on_next_button = self.next_button_rect.collidepoint(mouse_pos)
        on_previous_button = self.previous_button_rect.collidepoint(mouse_pos)

        if self.app.state == 0 and mouse_click and (on_previous_button or on_next_button):
            if on_next_button:
                self.next_skin()
            elif on_previous_button:
                self.previous_skin()

            pygame.time.delay(100)
            self.fn(self.skins_names[self.index_selected])
            self.update_text()

    def next_skin(self):
        self.index_selected = (self.index_selected + 1) % self.num_skins
        self.selected = self.skins[self.skins_names[self.index_selected]]["sprites"][1]

    def previous_skin(self):
        self.index_selected = (self.index_selected - 1) % self.num_skins
        self.selected = self.skins[self.skins_names[self.index_selected]]["sprites"][1]
