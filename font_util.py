import pygame


def outline(img, loc, display):
    mask = pygame.mask.from_surface(img)
    mask_surf = mask.to_surface()
    line = 2
    mask_surf.set_colorkey((0, 0, 0))
    display.blit(mask_surf, (loc[0] - line, loc[1]))
    display.blit(mask_surf, (loc[0] + line, loc[1]))
    display.blit(mask_surf, (loc[0], loc[1] - line))
    display.blit(mask_surf, (loc[0], loc[1] + line))
