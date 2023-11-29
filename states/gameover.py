import pygame
import spritesheet
from base import BaseState
from font_util import outline
from save_game import save_score


class GameOver(BaseState):
    def __init__(self):
        super(GameOver, self).__init__()
        self.font = pygame.font.Font("./assets/fonts/PixeloidSansBold.ttf", 20)
        self.scoreboard = None
        self.play_again = None
        self.pause_button = None
        self.medals = []
        self.alpha = 0
        self.load_images()
        self.pause_button_rect = self.pause_button.get_rect(topleft=(20, 20))
        self.scoreboard.set_alpha(self.alpha)
        self.scoreboard_rect = self.scoreboard.get_rect(
            center=(self.screen_rect.centerx, self.screen_rect.centery - 50))
        self.score = 0
        self.selected = 0
        self.score_surf = self.font.render(str(self.score), False, "White")
        self.score_surf.set_alpha(self.alpha)
        self.score_rect = self.score_surf.get_rect(
            topright=(self.scoreboard_rect.topright[0] - 30, self.scoreboard_rect.topright[1] + 45))
        self.best_score = 0
        self.best_score_surf = self.font.render(str(self.best_score), False, "White")
        self.best_score_surf.set_alpha(self.alpha)
        self.best_score_rect = self.best_score_surf.get_rect(
            topright=(self.scoreboard_rect.topright[0] - 30, self.scoreboard_rect.topright[1] + 105))
        self.play_again.set_alpha(self.alpha)
        self.play_again_rect = self.play_again.get_rect(
            center=(self.screen_rect.centerx, self.scoreboard_rect.bottom + 50))

    def startup(self, persistent):
        self.persist = persistent
        self.score = self.persist["score"]
        self.best_score = self.persist["best_score"]
        self.alpha = 0
        self.score_surf = self.font.render(str(self.score), False, "White")
        if self.score > self.best_score:
            save_score(self.score)
            self.persist["best_score"] = self.score
            self.best_score = self.score
        if self.score >= 50:
            self.selected = 2
        elif self.score >= 25:
            self.selected = 1
        elif self.score >= 10:
            self.selected = 0
        else:
            self.selected = -1
        self.best_score_surf = self.font.render(str(self.best_score), False, "White")
        self.best_score_rect = self.best_score_surf.get_rect(
            topright=(self.scoreboard_rect.topright[0] - 30, self.scoreboard_rect.topright[1] + 105))

    def get_event(self, event):
        mouse_pos = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.pause_button_rect.collidepoint(mouse_pos):
                self.next_state = "MENU"
                self.done = True
            elif self.play_again_rect.collidepoint(mouse_pos):
                self.next_state = "GAMEPLAY"
                self.done = True

    def load_images(self):
        ss = spritesheet.SpriteSheet("./assets/sprites/sprites.png")
        self.scoreboard = pygame.transform.scale_by(ss.image_at((3, 259, 113, 57)), 2.9)
        self.scoreboard.set_colorkey("Black")
        self.play_again = pygame.transform.scale_by(ss.image_at((354, 118, 52, 29)), 2.5)
        self.play_again.set_colorkey("Black")
        self.pause_button = pygame.transform.scale_by(ss.image_at((462, 26, 40, 14)), 2.5)
        self.pause_button.set_colorkey("Black")
        self.medals.append(pygame.transform.scale_by(ss.image_at((112, 477, 22, 22)), 2.9))
        self.medals.append(pygame.transform.scale_by(ss.image_at((121, 258, 22, 22)), 2.9))
        self.medals.append(pygame.transform.scale_by(ss.image_at((121, 282, 22, 22)), 2.9))
        for medal in self.medals:
            medal.set_colorkey("Black")
            medal.set_alpha(self.alpha)

    def draw(self, surface):
        surface.blit(self.scoreboard, self.scoreboard_rect)
        outline(self.score_surf, self.score_rect, surface, self.alpha)
        outline(self.best_score_surf, self.best_score_rect, surface, self.alpha)
        surface.blit(self.play_again, self.play_again_rect)
        surface.blit(self.pause_button, self.pause_button_rect)
        if self.selected != -1:
            surface.blit(self.medals[self.selected], self.medals[self.selected].get_rect(
                topleft=(self.scoreboard_rect.topleft[0] + 38, self.scoreboard_rect.topleft[1] + 62)))

    def update(self, dt):
        if self.alpha < 255:
            self.alpha += 5
            self.play_again.set_alpha(self.alpha)
            self.scoreboard.set_alpha(self.alpha)
            self.score_surf.set_alpha(self.alpha*4)
            self.best_score_surf.set_alpha(self.alpha*4)
            self.medals[self.selected].set_alpha(self.alpha*2)
