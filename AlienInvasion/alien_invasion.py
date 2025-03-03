import sys
import pygame

class AlienInvasion:
    def __init__(self):
        pygame.init()
        self.bgcolor = pygame.Color(230,230,230)
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(800,600)
        pygame.display.set_caption('Alien Invasion')
    def run_game(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            pygame.display.flip()
            self.clock.tick(60)
            self.screen.fill(self.bgcolor)
