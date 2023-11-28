import settings
from bird import Bird
from obstacle import Obstacle
from settings import HEIGHT, FONTS, WIDTH
from font_util import outline
import pygame


class FlappyBird:
    def __init__(self,
                 app,
                 max_score,
                 obstacle_sprites,
                 background_image,
                 ground_image,
                 bird_sprites,
                 try_again_image,
                 how_to_play_image,
                 pause_image,
                 boardscore_image):
        self.app = app
        self.score = 0
        self.scoreElement = Score()
        self.max_score = max_score
        self.is_active = False
        self.how_to_play = how_to_play_image
        self.is_game_over = False
        self.obstacle_images = obstacle_sprites
        self.background = background_image
        self.ground = pygame.sprite.GroupSingle()
        self.ground.add(Ground(ground_image))
        self.is_loading = False
        self.bird = pygame.sprite.GroupSingle()
        self.obstacles = pygame.sprite.Group()
        self.bird.add(Bird(self,
                           int(self.app.dimensions[0] / 2),
                           int(self.app.dimensions[1]) / 2,
                           bird_sprites))
        self.generate_first_objects()
        self.try_again = TryAgain(try_again_image,boardscore_image, self.restart)
        self.menu_button = MenuButton(pause_image, self.click_menu_button)
        self.point_channel = pygame.mixer.Channel(2)
        self.point_sound = pygame.mixer.Sound("./assets/sounds/point.mp3")

    def click_menu_button(self):
        self.restart()
        self.app.state = 0

    def add_obstacles(self):
        if len(self.obstacles.sprites()) <= 4:
            bottom, top = Obstacle.generate_positions_of_objects()

            distance = (self.obstacles.sprites()[len(self.obstacles.sprites()) - 1].rect.x +
                        Obstacle.distance_between_pair)

            bottom_obstacle = Obstacle(self.obstacle_images[0], topleft=(distance, bottom))
            top_obstacle = Obstacle(self.obstacle_images[1], bottomleft=(distance, top))

            self.obstacles.add(bottom_obstacle, top_obstacle)

    def generate_first_objects(self):
        bottom, top = Obstacle.generate_positions_of_objects()
        x = 800
        bottom_obstacle = Obstacle(self.obstacle_images[0], topleft=(x, bottom))
        top_obstacle = Obstacle(self.obstacle_images[1], bottomleft=(x, top))
        self.obstacles.add(bottom_obstacle, top_obstacle)

    def is_game_over_checker(self):
        self.is_game_over = bool(len(pygame.sprite.spritecollide(self.bird.sprite, self.obstacles, False)) >= 1 or
                                 pygame.sprite.spritecollideany(self.bird.sprite, self.ground))
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
                self.game_over()
                return
            self.score += 1
            self.point_channel.play(self.point_sound)
        self.scoreElement.set_score(self.score)
        self.scoreElement.draw(self.app.screen)

    def game_over(self):
        if self.is_game_over:
            self.bird.sprite.verify()
            self.try_again.update()
            self.try_again.draw(self.app.screen)

    def restart(self):
        self.is_active = False
        self.is_game_over = False
        self.bird.sprite.reset()
        self.obstacles.empty()
        self.generate_first_objects()
        self.score = 0
        self.try_again.disable()
        pygame.time.delay(90)
        self.is_loading = False

    def move_objects(self):
        for obstacle in self.obstacles:
            obstacle.update()

    def draw(self):
        self.app.screen.blit(self.background, self.background.get_rect())
        if self.is_active:
            self.move_objects()
            self.ground.update()
        self.obstacles.draw(self.app.screen)
        self.menu_button.draw(self.app.screen)

    def controls(self):
        keys = pygame.mouse.get_pressed()
        if keys[0] and self.menu_button.rect.collidepoint(pygame.mouse.get_pos()):
            self.is_loading = True
            return

        space = pygame.key.get_pressed()[pygame.K_SPACE]
        if (keys[0] or space) and not self.is_game_over and not self.bird.sprite.is_jumping and not self.try_again.is_active:
            self.active_game()

    def active_game(self):
        self.is_active = True
        self.bird.sprite.active()

    def update(self):
        self.draw()
        if not self.app.is_loading:
            self.controls()
        self.ground.draw(self.app.screen)
        self.bird.update()
        self.bird.draw(self.app.screen)
        self.handle_score()
        if not self.is_game_over:
            self.try_again.disable()
            if not self.is_active:
                self.app.screen.blit(self.how_to_play, self.how_to_play.get_rect(center=(int(WIDTH / 2),
                                                                                         int(HEIGHT / 2) + 100)))
            self.is_game_over_checker()
        else:
            self.game_over()
        self.add_obstacles()

class Score:
    def __init__(self):
        self.value = 0
        self.font = pygame.font.Font(FONTS["bold"], 32)

    def draw(self, screen):
        text = self.font.render(str(self.value), False, "Black")
        rect = text.get_rect(center=(int(WIDTH / 2), 40))

        outline(text, rect, screen)
        screen.blit(text, rect)

    def set_score(self, score):
        self.value = score


class TryAgain:
    def __init__(self, image, score_board_image, fn):
        super().__init__()
        self.image = image
        self.image.set_colorkey("Black")
        self.fn = fn
        self.is_active = False
        self.rect = self.image.get_rect(center=(int(settings.WIDTH / 2), settings.HEIGHT + 200))

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        self.is_active = True

    def disable(self):
        self.rect = self.image.get_rect(center=(int(settings.WIDTH / 2), settings.HEIGHT + 200))
        self.is_active = False

    def click(self):
        if pygame.mouse.get_pressed()[0] and self.rect.collidepoint(pygame.mouse.get_pos()):
            self.fn()
            self.disable()

    def update(self):
        if self.rect.y > int(settings.HEIGHT / 2):
            self.rect.y -= 5
        self.click()


class Ground(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(bottomleft=(0, HEIGHT))

    def apply_velocity(self):
        self.rect.x -= 3
        if self.rect.x <= -100:
            self.rect.x = 0

    def update(self):
        self.apply_velocity()


class MenuButton:
    def __init__(self, pause_image, fn):
        self.image = pause_image
        self.rect = pause_image.get_rect(topleft=(20, 20))
        self.fn = fn

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        self.click()

    def click(self):
        pressed = pygame.mouse.get_pressed()[0]
        position = pygame.mouse.get_pos()

        if pressed and self.rect.collidepoint(position):
            self.fn()
