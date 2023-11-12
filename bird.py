import pygame

class Bird(pygame.sprite.Sprite):
    def __init__(self, flappy, x, y, sprites):
        super().__init__()
        self.initial_position = (x,y)
        self.flappy = flappy
        self.sprites = sprites
        self.num_sprites = len(sprites)
        self.index_image = 0
        self.angle = 0
        self.image = self.sprites[self.index_image]
        self.rect = self.image.get_rect(center=self.initial_position)
        self.is_active = False
        self.gravity = 0
        self.is_jumping = False

    def jump(self):
        self.gravity = -13

    def reset(self):
        self.index_image = 0
        self.angle = 0
        self.image = self.sprites[self.index_image]
        self.rect = self.image.get_rect(center=self.initial_position)
        self.is_active = False
        self.gravity = 0
        self.is_jumping = False

    def apply_gravity(self):
        if self.rect.bottom + self.gravity >= 551:
            self.rect.bottom = 551
            return
        self.gravity += 1
        self.rect.bottom += self.gravity

    def animation(self):
        self.index_image = (self.index_image + 1) % self.num_sprites
        self.angle = -self.gravity
        self.image = pygame.transform.rotate((self.sprites[self.index_image]), -self.angle)
        self.image.set_colorkey("Black")

    def death(self):
        self.is_jumping = False
        if self.rect.bottom <= 550:
            self.rect.bottom += 10
        if self.angle >= -90:
            self.angle -= 3
        self.image = pygame.transform.rotate((self.sprites[2]), self.angle)
        self.image.set_colorkey("Black")

    def active(self):
        self.is_active = True

    def controls(self):
        keys = pygame.mouse.get_pressed()

        if not self.flappy.is_game_over:
            if keys[0] and not self.is_jumping:
                self.is_jumping = True
                self.jump()

            if not keys[0]:
                self.is_jumping = False

    def verify(self):
        self.is_active = False
        self.death()

    def update(self):
        self.controls()
        if self.is_active:
            self.animation()
            self.apply_gravity()

