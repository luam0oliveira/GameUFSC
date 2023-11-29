import sys
import pygame
from settings import DIMENSIONS
from states.menu import Menu
from game import Game
from states.gameplay import Gameplay
from states.gameover import GameOver

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
