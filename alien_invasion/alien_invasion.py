import sys
import pygame
from Settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
class AiNInvasion:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((self.settings.screen_width,self.settings.screen_height))
        #全屏模式为：
        #self.screen = pygame.display,set_mode(0,0),pygame.FULLSCREEN
        #self.settings.screen_width = self.screen.get_rect().width
        #self.setting.screen_height = self.screen.get_rect().height
        pygame.display.set_caption('Alien Invasion')
        self.ship = Ship(self)
        self.bullet = pygame.sprite.Group()
        self.alien = pygame.sprite.Group()
        self._create_alien()

    def run_game(self):
         while True:
             self._check_events()
             self.ship.update()
             self.bullet.update()
             self._update_bullet()
             self._update_screen()
             self.clock.tick(60)

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_events_keydown(event)

            elif event.type == pygame.KEYUP:
                self._check_events_keyup(event)

    def _check_events_keydown(self,event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_ESCAPE:
            sys.exit()
    def _check_events_keyup(self,event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        if event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _update_screen(self):
        pygame.display.flip()
        self.screen.fill(self.settings.bg_color)
        for bullet in self.bullet.sprites():
          bullet.draw_bullet()
        self.ship.blitme()
        self.alien.draw(self.screen)
        pygame.display.flip()
    def _fire_bullet(self):
        new_bullet = Bullet(self)
        self.bullet.add(new_bullet)
    def _update_bullet(self):
        self.bullet.update()
        for bullet in self.bullet.copy():
            if bullet.rect.bottom <= 0:
                self.bullet.remove(bullet)


    def _create_alien(self):
        alien = Alien(self)
        alien.width = alien.rect.width
        current_x = alien.width
        while current_x < (self.settings.screen_width-2*alien.width):
            new_alien = Alien(self)
            new_alien.x = current_x
            new_alien.rect.x = current_x
            self.alien.add(new_alien)
            current_x += 2*alien.width

if __name__ == '__main__':
    ai = AiNInvasion()
    ai.run_game()