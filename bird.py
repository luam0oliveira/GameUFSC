import pygame


class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y, sprites):
        super().__init__()
        self.initial_position = (x, y)
        self.sprites = sprites
        self.num_sprites = len(sprites)
        self.index_image = 0
        self.angle = 0
        self.image = self.sprites[self.index_image]
        self.rect = self.image.get_rect(center=self.initial_position)
        self.gravity = 0
        self.jump_channel = pygame.mixer.Channel(0)
        self.jump_channel.set_volume(0.1)
        self.jump_sound = pygame.mixer.Sound("./assets/sounds/flap.mp3")
        self.played_death = False
        self.die_channel = pygame.mixer.Channel(1)
        self.die_channel.set_volume(0.35)
        self.die_sound = pygame.mixer.Sound("./assets/sounds/die.mp3")
        self.hit_channel = pygame.mixer.Channel(3)
        self.die_channel.set_volume(0.2)
        self.hit_sound = pygame.mixer.Sound("./assets/sounds/hit.mp3")

    def jump(self):
        self.gravity = -13
        self.jump_channel.play(self.jump_sound)

    def reset(self):
        self.index_image = 0
        self.angle = 0
        self.played_death = False
        self.image = self.sprites[self.index_image]
        self.rect = self.image.get_rect(center=self.initial_position)
        self.gravity = 0

    def apply_gravity(self):
        if self.rect.bottom + self.gravity >= 551:
            self.rect.bottom = 551
            return
        self.gravity += 1
        self.rect.bottom += self.gravity

    def animation(self):
        if pygame.time.get_ticks() % 5 == 0:
            self.index_image = (self.index_image + 1) % self.num_sprites
        self.angle = -self.gravity
        self.image = pygame.transform.rotate((self.sprites[self.index_image]), self.angle)
        self.image.set_colorkey("Black")

    def death(self):
        if not self.played_death:
            self.hit_channel.play(self.hit_sound)
            pygame.time.delay(100)
            self.die_channel.play(self.die_sound)
            self.played_death = True
        if self.rect.bottom <= 550:
            self.rect.bottom += 10
        if self.angle >= -90:
            self.angle -= 3
        self.image = pygame.transform.rotate((self.sprites[2]), self.angle)
        self.image.set_colorkey("Black")

    def verify(self):
        self.death()

    def update(self):
        if not self.played_death:
            self.animation()
        self.apply_gravity()
