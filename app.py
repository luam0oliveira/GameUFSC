import spritesheet
import pygame
import sys
from flappybird import FlappyBird
from settings import DIMENSIONS, WIDTH, HEIGHT, FPS
from menu import Menu

class App:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Flappy Bird")
        pygame.font.init()
        self.dimensions = (WIDTH, HEIGHT)
        self.screen = pygame.display.set_mode(self.dimensions)
        self.clock = pygame.time.Clock()
        self.state = 0
        self.images = {}
        self.is_loading = False
        self.load_images()
        self.flappy_bird = FlappyBird(self,
                                      0, self.images["obstacle_images"],
                                      self.images["background_image"],
                                      self.images["ground_image"],
                                      self.images["bird_sprites"],
                                      self.images["try_again_image"],
                                      self.images["how_to_play"]
                                      )
        self.menu = Menu(self, self.images["background_image"], self.images["logo"], self.images["play"])

    def load_images(self):
        # Load SpriteSheet
        ss = spritesheet.SpriteSheet("assets/sprits/sprits.png")

        # Obstacle images
        self.images["obstacle_images"] = [
            pygame.transform.scale_by(ss.image_at((84, 323, 26, 160)), 3.5),
            pygame.transform.scale_by(ss.image_at((56, 323, 26, 160)), 3.5)
        ]

        # Load sprites from bird
        self.images["bird_sprites"] = [
            ss.image_at((3, 491, 17, 12)),
            ss.image_at((31, 491, 17, 12)),
            ss.image_at((59, 491, 17, 12))
        ]

        # Load how to play
        self.images["how_to_play"] = pygame.transform.scale_by(ss.image_at((292, 91, 57, 49)), 2.5)
        self.images["how_to_play"].set_colorkey("Black")

        # Re-scaling images
        for i in range(len(self.images["bird_sprites"])):
            self.images["bird_sprites"][i] = pygame.transform.scale_by(self.images["bird_sprites"][i], 2.5)

        # Load scenario images
        self.images["background_image"] = pygame.transform.scale(ss.image_at((0, 0, 143, 255)), DIMENSIONS)
        self.images["ground_image"] = pygame.transform.scale(ss.image_at((292, 0, 67, 56)), (self.dimensions[0] + 150, 150))

        # Load try again image
        self.images["try_again_image"] = pygame.transform.scale_by(ss.image_at((354, 118, 52, 29)), 2)

        # Load logo image
        self.images["logo"] = pygame.transform.scale_by(ss.image_at((351, 91, 89, 24)), 3)
        self.images["logo"].set_colorkey("Black")

        # Load play image
        self.images["play"] = pygame.transform.scale_by(ss.image_at((354, 118, 52, 29)), 2.5)
        self.images["play"].set_colorkey("Black")

        # Removing black background
        for image in self.images["obstacle_images"]:
            image.set_colorkey("Black")

        for image in self.images["bird_sprites"]:
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