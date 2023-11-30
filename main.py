import sys
import pygame
from modules import DIMENSIONS, Game, ICON
from modules.states import GameOver, Gameplay, Menu

pygame.init()
pygame.display.set_caption("Flappy Bird")
pygame.display.set_icon(pygame.image.load(ICON))
screen = pygame.display.set_mode(DIMENSIONS)


states = {
    "MENU": Menu(),
    "GAMEPLAY": Gameplay(),
    "GAMEOVER": GameOver()
}

game = Game(screen, states, "MENU")
game.run()

pygame.quit()
sys.exit()
