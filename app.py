import spritesheet
import pygame
import sys
from spritesheet_skins import get_skins
from flappybird import FlappyBird
from settings import DIMENSIONS, WIDTH, HEIGHT, FPS, SKINS
from menu import Menu


class App:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Flappy Bird")
        pygame.font.init()
        pygame.mixer.init()
        self.dimensions = (WIDTH, HEIGHT)
        self.screen = pygame.display.set_mode(self.dimensions)
        self.clock = pygame.time.Clock()
        self.state = 0
        self.images = {}
        self.skins = {}
        self.is_loading = False
        self.selected_skin = "default"
        self.load_images()
        self.flappy_bird = FlappyBird(self,
                                      0, self.images["obstacle_images"],
                                      self.images["background_image"],
                                      self.images["ground_image"],
                                      self.images["bird_sprites"],
                                      self.images["try_again_image"],
                                      self.images["how_to_play"],
                                      self.images["pause_button"],
                                      self.images["board_score_image"]
                                      )

        self.menu = Menu(self,
                         self.images["background_image"],
                         self.images["logo"],
                         self.images["play"],
                         self.skins,
                         self.images["next"],
                         self.images["previous"],
                         self.change_skin,)

    def load_skins(self):
        data = SKINS
        for i in data:
            self.skins[i] = {
                "name": data[i]["name"],
                "sprites": get_skins(data[i]["path"], 17, 12, 3)
            }

    def change_skin(self, selected):
        self.selected_skin = selected
        self.flappy_bird.bird.sprite.set_sprites(self.skins[self.selected_skin]["sprites"])
        print(self.flappy_bird.bird.sprite.sprites)


    def load_images(self):
        # Load SpriteSheet
        ss = spritesheet.SpriteSheet("assets/sprites/sprites.png")

        # Obstacle images
        self.images["obstacle_images"] = [
            pygame.transform.scale_by(ss.image_at((84, 323, 26, 160)), 3.5),
            pygame.transform.scale_by(ss.image_at((56, 323, 26, 160)), 3.5)
        ]

        # Load skins
        self.load_skins()

        self.images["bird_sprites"] = self.skins[self.selected_skin]["sprites"]

        # Load how to play
        self.images["how_to_play"] = pygame.transform.scale_by(ss.image_at((292, 91, 57, 49)), 2.5)
        self.images["how_to_play"].set_colorkey("Black")

        # Load scenario images
        self.images["background_image"] = pygame.transform.scale(ss.image_at((0, 0, 143, 255)), DIMENSIONS)
        self.images["ground_image"] = pygame.transform.scale(ss.image_at((292, 0, 67, 56)),
                                                             (self.dimensions[0] + 150, 150))

        # Load board_score image
        self.images["board_score_image"] = pygame.transform.scale_by(ss.image_at((3, 259, 113, 57)), 2.75)
        self.images["board_score_image"].set_colorkey("Black")

        # Load try again image
        self.images["try_again_image"] = pygame.transform.scale_by(ss.image_at((354, 118, 52, 29)), 2)

        # Load logo image
        self.images["logo"] = pygame.transform.scale_by(ss.image_at((351, 91, 89, 24)), 3)
        self.images["logo"].set_colorkey("Black")

        # Load skin changer button images
        self.images["next"] = pygame.transform.scale_by(ss.image_at((334, 142, 13, 14)), 2)
        self.images["previous"] = pygame.transform.flip(self.images["next"], True, False)

        # Load play image
        self.images["play"] = pygame.transform.scale_by(ss.image_at((354, 118, 52, 29)), 2.5)
        self.images["play"].set_colorkey("Black")

        # Load pause button image
        self.images["pause_button"] = pygame.transform.scale_by(ss.image_at((462, 26, 40, 14)), 2.5)
        self.images["pause_button"].set_colorkey("Black")

        # Removing black background
        for image in self.images["obstacle_images"]:
            image.set_colorkey("Black")

    def update(self):
        pygame.display.update()
        match self.state:
            case 0:
                self.menu.draw()
            case 1:
                self.flappy_bird.update()
            case _:
                print("Hahaha")

        self.clock.tick(FPS)

    @staticmethod
    def check_events():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def run(self):
        while True:
            self.check_events()
            self.update()
