import pygame
from modules import BaseState, Bird, Ground, Obstacle, Score, SpriteSheet


class Gameplay(BaseState):
    def __init__(self):
        super(Gameplay, self).__init__()
        self.background = None
        self.ground_image = None
        self.obstacle_images = None
        self.pause_button = None
        self.how_to_play = None
        self.load_images()
        self.pause_button_rect = self.pause_button.get_rect(topleft=(20, 20))
        self.ground = pygame.sprite.GroupSingle(Ground(self.ground_image))
        self.bird = None
        self.score = 0
        self.scoreElement = Score()
        self.obstacles = pygame.sprite.Group()
        self.generate_first_objects()
        self.is_active = False
        self.is_game_over = False
        self.point_channel = pygame.mixer.Channel(2)
        self.point_sound = pygame.mixer.Sound("./assets/sounds/point.mp3")
        self.next_state = "GAMEOVER"

    def startup(self, persistent):
        self.persist = persistent
        self.restart()

    def generate_first_objects(self):
        bottom, top = Obstacle.generate_positions_of_objects()
        x = 800
        bottom_obstacle = Obstacle(self.obstacle_images[0], topleft=(x, bottom))
        top_obstacle = Obstacle(self.obstacle_images[1], bottomleft=(x, top))
        self.obstacles.add(bottom_obstacle, top_obstacle)

    def is_game_over_checker(self):
        self.is_game_over = bool(len(pygame.sprite.spritecollide(self.bird.sprite, self.obstacles, False)) >= 1 or
                                 pygame.sprite.spritecollideany(self.bird.sprite, self.ground)) or self.is_game_over

        self.is_active = not self.is_game_over and self.is_active

    def handle_score(self):
        position = self.bird.sprite.rect.x
        obstacles = self.obstacles.sprites()
        first_obstacle = obstacles[0]
        second_obstacle = {}

        if len(obstacles) > 6:
            second_obstacle = obstacles[2]

        added = False
        if position >= first_obstacle.rect.x and not first_obstacle.scored:
            added = True
            first_obstacle.scored = True
        elif second_obstacle and position >= second_obstacle.rect.x and not second_obstacle.scored:
            added = True
            second_obstacle.scored = True

        if added:
            if self.bird.sprite.rect.bottom <= 0:
                self.is_game_over = True
                self.is_active = False
                return
            self.score += 1
            self.point_channel.play(self.point_sound)
        self.scoreElement.set_score(self.score)

    def move_objects(self):
        for obstacle in self.obstacles:
            obstacle.update()

    def add_obstacles(self):
        if len(self.obstacles.sprites()) <= 4:
            bottom, top = Obstacle.generate_positions_of_objects()

            distance = (self.obstacles.sprites()[len(self.obstacles.sprites()) - 1].rect.x +
                        Obstacle.distance_between_pair)

            bottom_obstacle = Obstacle(self.obstacle_images[0], topleft=(distance, bottom))
            top_obstacle = Obstacle(self.obstacle_images[1], bottomleft=(distance, top))

            self.obstacles.add(bottom_obstacle, top_obstacle)

    def load_images(self):
        ss = SpriteSheet("./assets/sprites/sprites.png")
        self.background = pygame.transform.scale(ss.image_at((0, 0, 143, 255)), self.screen_rect.size)
        self.ground_image = pygame.transform.scale(ss.image_at((292, 0, 67, 56)), (self.screen_rect.size[0] + 150, 150))
        self.obstacle_images = [
            pygame.transform.scale_by(ss.image_at((84, 323, 26, 160)), 3.5),
            pygame.transform.scale_by(ss.image_at((56, 323, 26, 160)), 3.5)
        ]
        for image in self.obstacle_images:
            image.set_colorkey("Black")
        self.pause_button = pygame.transform.scale_by(ss.image_at((462, 26, 40, 14)), 2.5)
        self.pause_button.set_colorkey("Black")
        self.how_to_play = pygame.transform.scale_by(ss.image_at((292, 91, 57, 49)), 2.5)
        self.how_to_play.set_colorkey("Black")

    def restart(self):
        self.is_active = False
        self.is_game_over = False
        self.bird = None
        self.obstacles.empty()
        self.generate_first_objects()
        self.score = 0

    def get_event(self, event):
        mouse_position = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN and self.pause_button_rect.collidepoint(mouse_position):
            self.restart()
            self.next_state = "MENU"
            self.done = True
        elif ((event.type == pygame.MOUSEBUTTONDOWN or (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE)) and
                not self.is_game_over):
            self.is_active = True
            self.bird.sprites()[0].jump()

    def draw(self, surface):
        surface.blit(self.background, self.background.get_rect())
        self.obstacles.draw(surface)
        self.ground.draw(surface)
        surface.blit(self.pause_button, self.pause_button_rect)
        self.bird.draw(surface)
        self.scoreElement.draw(surface)
        if not self.is_active and not self.is_game_over:
            surface.blit(self.how_to_play, self.how_to_play.get_rect(
                center=(self.screen_rect.centerx, self.screen_rect.centery + 100)))

    def update(self, dt):
        if not self.bird:
            self.bird = pygame.sprite.GroupSingle(
                Bird(self.screen_rect.centerx, self.screen_rect.centery, self.persist["skin"]))
        self.is_game_over_checker()
        self.handle_score()
        if self.is_game_over:
            self.bird.sprite.death()
            self.bird.update()
            if self.bird.sprite.rect.bottom >= 551:
                self.next_state = "GAMEOVER"
                self.persist["score"] = self.score
                self.done = True
        if self.is_active:
            self.bird.update()
            self.ground.update()
            self.move_objects()
            self.add_obstacles()
