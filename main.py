import sys
import pygame
from settings import DIMENSIONS
from menu import Menu
from game import Game
from gameplay import Gameplay
from gameover import GameOver

pygame.init()
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
