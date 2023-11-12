import settings
from bird import Bird
from obstacle import Obstacle
from settings import HEIGHT, FONTS, WIDTH
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
                 how_to_play_image):
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
        self.bird = pygame.sprite.GroupSingle()
        self.obstacles = pygame.sprite.Group()
        self.bird.add(Bird(self, int(self.app.dimensions[0] / 2), int(self.app.dimensions[1]) / 2, bird_sprites))
        self.generate_first_objects()
        self.try_again = TryAgain(try_again_image, self.restart)

    def add_obstacles(self):
        if len(self.obstacles.sprites()) <= 4:
            bottom, top = Obstacle.generate_positions_of_objects()

            distance = self.obstacles.sprites()[len(self.obstacles.sprites()) - 1].rect.x + Obstacle.distance_between_pair

            bottom_obstacle = Obstacle(self.obstacle_images[0], topleft=(distance, bottom))
            top_obstacle = Obstacle(self.obstacle_images[1], bottomleft=(distance, top))

            self.obstacles.add(bottom_obstacle, top_obstacle)

    def generate_first_objects(self):
        bottom, top = Obstacle.generate_positions_of_objects()
        x = 400
        bottom_obstacle = Obstacle(self.obstacle_images[0], topleft=(x, bottom))
        top_obstacle = Obstacle(self.obstacle_images[1], bottomleft=(x, top))
        self.obstacles.add(bottom_obstacle, top_obstacle)

    def is_game_over_checker(self):
        self.is_game_over = bool(len(pygame.sprite.spritecollide(self.bird.sprite, self.obstacles, False)) >= 1 or pygame.sprite.spritecollideany(self.bird.sprite, self.ground))
        self.is_active = not self.is_game_over and self.is_active

    def handle_score(self):
        position = self.bird.sprite.rect.x
        if position == self.obstacles.sprites()[0].rect.x + 1 or (len(self.obstacles) > 2 and position == self.obstacles.sprites()[2].rect.x + 1):
            self.score += 1
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

    def move_objects(self):
        for obstacle in self.obstacles:
            obstacle.update()

    def draw(self):
        self.app.screen.blit(self.background, self.background.get_rect())
        if self.is_active:
            self.move_objects()
            self.ground.update()
        self.obstacles.draw(self.app.screen)

    def controls(self):
        keys = pygame.mouse.get_pressed()
        # print(self.try_again.active)
        if keys[0] and not self.is_game_over and not self.bird.sprite.is_jumping and not self.try_again.is_active:
            self.active_game()

    def active_game(self):
        self.is_active = True
        self.bird.sprite.active()

    def update(self):
        self.draw()
        self.handle_score()
        self.controls()
        self.ground.draw(self.app.screen)
        self.bird.update()
        self.bird.draw(self.app.screen)
        if not self.is_game_over:
            self.try_again.disable()
            if not self.is_active:
                self.app.screen.blit(self.how_to_play, self.how_to_play.get_rect(center=(int(WIDTH / 2), int(HEIGHT / 2) + 100)))
            self.is_game_over_checker()
        else:
            self.game_over()
        self.add_obstacles()


class Score:
    def __init__(self):
        self.value = 0
        self.font = pygame.font.Font(FONTS["bold"], 24)

    def draw(self, screen):
        text = self.font.render(str(self.value), False, "Black")
        rect = text.get_rect(center=(int(WIDTH / 2), 100))
        screen.blit(text, rect)

    def set_score(self, score):
        self.value = score


class TryAgain:
    def __init__(self, image, fn):
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
        self.is_active = False

    def click(self):
        if pygame.mouse.get_pressed()[0] and self.rect.collidepoint(pygame.mouse.get_pos()):
            self.fn()
            self.rect = self.image.get_rect(center=(int(settings.WIDTH / 2), settings.HEIGHT + 200))
            self.is_active = False

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
        self.rect.x -= 2
        if self.rect.x <= -100:
            self.rect.x = 0

    def update(self):
        self.apply_velocity()