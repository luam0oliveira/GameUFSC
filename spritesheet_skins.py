import pygame


def get_skins(file, sprite_width, sprite_height, number_of_sprites):
    sprites = []

    sprite_sheet = pygame.image.load(file).convert_alpha()

    for i in range(number_of_sprites):
        rect = pygame.Rect((sprite_width * i,
                            0,
                            sprite_width, sprite_height))
        image = pygame.Surface(rect.size).convert_alpha()
        image.blit(sprite_sheet, (0, 0), rect)
        image = pygame.transform.scale_by(image, 2.5)
        image.set_colorkey("Black")
        sprites.append(image)

    return sprites
