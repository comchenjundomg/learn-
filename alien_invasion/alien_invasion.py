import sys
import pygame
from time import sleep
from Settings import Settings
from game_stats import GameStats
from ship import Ship
from bullet import Bullet
from alien import Alien
from button import Button
from scoreboard import Scoreboard
class AiNInvasion:
    def __init__(self):
        pygame.init()
        self.game_active = False
        self.clock = pygame.time.Clock()
        self.settings = Settings()


        self.screen = pygame.display.set_mode((self.settings.screen_width,self.settings.screen_height))
        #全屏模式为：
        #self.screen = pygame.display,set_mode(0,0),pygame.FULLSCREEN
        #self.settings.screen_width = self.screen.get_rect().width
        #self.setting.screen_height = self.screen.get_rect().height
        pygame.display.set_caption('Alien Invasion')
        self.ship = Ship(self)
        self.stats = GameStats(self)
        self.scoreboard = Scoreboard(self)
        self.bullet = pygame.sprite.Group()
        self.alien = pygame.sprite.Group()
        self._create_fleet()
        self.play_button = Button(self, "Play")

    def run_game(self):
         while True:
             self._check_events()

             if  self.game_active:
                 self.ship.update()
                 self.bullet.update()
                 self._update_bullet()
                 self._update_aliens()

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
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
    def _check_play_button(self, mouse_pos):
        button_clicked =self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active :
            self.settings.initialize_dynamic_settings()
            self.stats.reset_starts()
            self.scoreboard.prep_score()
            self.scoreboard.prep_level()
            self.game_active = True
            pygame.mouse.set_visible(False)

            self.bullet.empty()
            self.alien.empty()

            self._create_fleet()
            self.ship.center_ship()
            self.scoreboard.prep_ships()

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
        self.scoreboard.show_score()
        if not self.game_active:
            self.play_button.draw_button()

        pygame.display.flip()
    def _fire_bullet(self):
        new_bullet = Bullet(self)
        self.bullet.add(new_bullet)
    def _update_bullet(self):
        self.bullet.update()
        for bullet in self.bullet.copy():
            if bullet.rect.bottom <= 0:
                self.bullet.remove(bullet)
        self._check_aliens_bullet_collisions()
    def _check_aliens_bullet_collisions(self):
        collisions = pygame.sprite.groupcollide(self.alien, self.bullet, True, True)
        if collisions:
            for alien in collisions.values():
                self.stats.score += self.settings.alien_points * len(alien)
            self.scoreboard.prep_score()
            self.scoreboard.check_high_score()
        if not self.alien:
            self.bullet.empty()
            self._create_fleet()
            self.settings.increase_speed()
            self.stats.level += 1
            self.scoreboard.prep_level()

    def _create_fleet(self):
        alien = Alien(self)
        alien_width,alien_height = alien.rect.size
        current_x,current_y = alien_width,alien_height
        while current_y <(self.settings.screen_height-3*alien_height):
            while current_x < (self.settings.screen_width-2*alien_width):
                self._create_alien(current_x,current_y)
                current_x += 2*alien_width
            current_x = alien_width
            current_y += 2*alien_height
    def _create_alien(self,x_position,y_position):
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.alien.add(new_alien)
    def _check_fleet_edges(self):
        for alien in self.alien.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
    def _change_fleet_direction(self):
        for alien in self.alien.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1
    def _update_aliens(self):
        self._check_fleet_edges()
        self.alien.update()
        if pygame.sprite.spritecollideany(self.ship,self.alien):
            self._ship_hit()
        self._check_alien_bottom()
    def _ship_hit(self):
        if self.stats.ship_left>0:

            self.stats.ship_left -=1
            self.scoreboard.prep_ships()
            self.bullet.empty()
            self.alien.empty()

            self._create_fleet()
            self.ship.center_ship()
            sleep(5)
        else:
            self.game_active = False
            pygame.mouse.set_visible(True)
    def _check_alien_bottom(self):
        for alien in self.alien.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                self._ship_hit()
                break


if __name__ == '__main__':
    ai = AiNInvasion()
    ai.run_game()