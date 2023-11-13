import pygame.mouse


class Menu:
    def __init__(self, app, background_image, logo_image, play_button_image):
        self.app = app
        self.background = background_image
        self.logo = logo_image
        self.play_button_surf = play_button_image
        self.play_button_rect = self.play_button_surf.get_rect(center=(int(self.app.dimensions[0] / 2),
                                                                       int(self.app.dimensions[1] / 2 + 100)))

    def draw(self):
        self.app.screen.blit(self.background, self.background.get_rect(topleft=(0, 0)))
        self.app.screen.blit(self.logo, self.logo.get_rect(center=(int(self.app.dimensions[0] / 2), 150)))
        self.app.screen.blit(self.play_button_surf, self.play_button_rect)
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
        pygame.time.delay(100)
        self.app.is_loading = False
