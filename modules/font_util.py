import pygame


def outline(img, loc, display, alpha = 255):
    mask = pygame.mask.from_surface(img)
    mask_surf = mask.to_surface(setcolor=(1,1,1))
    mask_surf.set_alpha(alpha)
    line = 2
    mask_surf.set_colorkey((0, 0, 0))
    display.blit(mask_surf, (loc[0] - line, loc[1]))
    display.blit(mask_surf, (loc[0] + line, loc[1]))
    display.blit(mask_surf, (loc[0], loc[1] - line))
    display.blit(mask_surf, (loc[0], loc[1] + line))
    display.blit(img, loc)
