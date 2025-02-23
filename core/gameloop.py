"""
core/gameloop.py
    Rukovanje glavnom petljom igre. Procesiranje evenata (pritisci na tipke ili pritisak miša),
    ažuriranje objekata, skrolanje svijeta, detekcija kolizija, bodovanje, prikazivanje
    objekata na ekranu.
"""

from time import sleep
import pygame
import sys
import random
from core.factory import ObstacleFactory, PowerUpFactory
from core.gamestats import GameStats
from objects.scoreboard import Scoreboard
from objects.powerup import FuelPowerUp, ShieldPowerUp, PowerUpComposite
from objects.decorator import FuelPowerUpDecorator, ShieldPowerUpDecorator
from objects.obstacle import Bird 

class GameLoop:
    """
    Rukovanje glavnom petljom igre.
    
    Metode:     
        check_events() - procesira ulazne evente
        start_new_game() - resetira stanje igre za pokretanje nove
        display_message() - postavlja statusnu poruku ili obavijest o prikupljenom power-upu
        reset_position() - resetira poziciju balona na startnu
        update_game() - ažurira objekte u igri, skrolanje, kolizije i bodovanje
        spawn_obstacles() - spawning prepreka korištenjem ObstacleFactory
        spawn_powerups() - spawning power-upova korištenjem PowerUpFactory
        update_screen() - renderira sve objekte i poruke
        run_game() - pokreće glavnu petlju igre
    """
    def __init__(self, settings, screen, balloon, obstacles, powerups, play_button, scoreboard, stats):
        # inicijalizacija referenci na postavke i druge objekte u igri
        self.settings = settings 
        self.screen = screen
        self.balloon = balloon
        self.obstacles = obstacles # kompozit prepreka
        self.powerups = powerups # kompozit power-upova
        self.play_button = play_button
        self.scoreboard = scoreboard
        self.stats = stats # gorivo, životi, bodovi ...

        # čisti prikaz poruke
        self.scoreboard.status_message = ""
        self.scoreboard.status_expiration = 0

        # prati prethodni status štita za detekciju isteka
        self.prev_shield_active = self.balloon.shield_active

        self.game_over_shown = False # prikazivanje poruke da je igra završila

    def check_events(self):
        """ Procesiranje pritisaka tipki na tipkovnici ili pritisak miša. """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    self.balloon.moving_left = True # pritisnuta tipka A - pomicanje ulijevo
                elif event.key == pygame.K_d:
                    self.balloon.moving_right = True # pritisnuta tipka D - pomicanje udesno

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    self.balloon.moving_left = False
                elif event.key == pygame.K_d:
                    self.balloon.moving_right = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                # ako je igra neaktivna i pritisnut je Play gumb pokreće se nova igra
                if not self.stats.game_active and self.play_button.rect.collidepoint(mouse_x, mouse_y):
                    self.start_new_game()

    def start_new_game(self):
        """ 
        Resetira se stanje igre i pokreće se nova.
        Resetira se statistika, pozicija balona, čiste se poruke,
        prepreke i power-upovi 
        """
        self.stats.reset_stats()
        self.stats.game_active = True
        self.reset_position()
        self.balloon.shield_active = False
        self.balloon.shield_timer = 0
        self.obstacles.children.clear()
        self.powerups.children.clear()
        self.scoreboard.active_powerup = ""
        self.scoreboard.status_message = ""
        self.prev_shield_active = False
        self.game_over_shown = False

    def display_message(self, message, duration, message_type="status"):
        """ 
        Postavljanje poruke za prikazivanje na ekranu. Status poruke se
        prikazuju na sredini ekrana, a powerup poruke ispod prikaza 
        statusa života. 

            message - tekst poruke za prikaz na ekranu
            duration -  trajanje prikaza poruke
            message_type -  status: centralne poruke (Life lost! ...)
                            power-up: poruke za aktivirane power-upove
        """
        if message_type == "status":
            self.scoreboard.set_status_message(message, duration)
        elif message_type == "powerup":
            self.scoreboard.set_active_powerup(message, duration // 1000)
    
    def reset_position(self):
        """ Resetira poziciju balona na donji centar ekrana. """
        self.balloon.rect.centerx = self.screen.get_rect().centerx
        self.balloon.rect.bottom = self.screen.get_rect().bottom - 50

    def update_game(self, dt):
        """ 
        Ažurira igrine objekte, skrolanje svijeta, rukuje kolizijama i bodovanjem.
            dt - vrijeme od posljednjeg frejma u sekundama 
        """
        if self.stats.game_active:
            # ažurira balon i timer štita
            self.balloon.update(dt)
            self.balloon.update_shield(dt)
            
            # ažurira prepreke i power-upove
            self.obstacles.update(dt)
            self.powerups.update(dt)
            
            """ Balon se podiže do zadane maksimalne visine te kada ju dostigne
            ostaje na njoj, a prepreke se skrolaju prema dolje. """
            max_up =  350 # maksimalna visina ekrana do koje se balon podiže
            if self.balloon.rect.y < max_up:
                #scroll_offset = max_up - self.balloon.rect.y
                scroll_offset = self.settings.balloon_rise_speed * dt * 0.35
                #scroll_offset = min(scroll_offset, self.settings.balloon_rise_speed * dt * 0.5)
                self.balloon.rect.y = max_up # y koordinata se postavlja na maksimalnu visinu ekrana do koje se balon podiže

                # prepreke i power-upovi se skrolaju za scroll_offset
                for o in self.obstacles.children:
                    o.rect.y += scroll_offset
                for pu in self.powerups.children:
                    pu.rect.y += scroll_offset

                self.stats.score += scroll_offset * 0.005 # bodovi za postizanje visine

            # Povećavanje bodova bazirano na proteklom vremenu
            self.stats.score += self.settings.score_increment * dt

            # Ažurira high_score ako je trenutni broj bodova veći od njega
            if self.stats.score > self.stats.high_score:
                self.stats.high_score = self.stats.score

            # Ažuriranje prikazivanja bodova, goriva, života
            self.scoreboard.prep_score()
            self.scoreboard.prep_high_score()
            self.scoreboard.prep_fuel()
            self.scoreboard.prep_lives()

            # Kolizija s preprekama, ako je štit neaktivan gubi se život
            for o in self.obstacles.children[:]:
                if self.balloon.rect.colliderect(o.rect):
                    if not self.balloon.shield_active:
                        self.stats.lives -= 1 # umanjuje broj života za 1
                        self.display_message("Collision! Life lost!", duration = 2000, message_type="status")
                        print("Life lost - collision")
                        self.obstacles.remove(o)
                        self.reset_position()
                        self.stats.fuel = self.settings.initial_fuel # resetira stanje goriva nakon gubitka života
                        self.scoreboard.prep_lives()
                        if self.stats.lives <= 0: 
                            self.stats.lives = 0
                            self.scoreboard.prep_lives()
                            #self.display_message("No more lives! Game Over!", duration = 2000, message_type="status")
                            print("Game Over!")
                            pygame.time.delay(2000)
                            self.stats.game_active = False # igra završava kad su svi životi izgubljeni
                            return
                    else: # ako je štit aktivan kolizije su ignorirane, a prepreka se briše
                        print("Active Shield - Collision ignored")
                        self.obstacles.remove(o)
            
            # Kolizija s power-upovima
            for pu in self.powerups.children[:]:
                if self.balloon.rect.colliderect(pu.rect):
                    if isinstance(pu, FuelPowerUp):
                        FuelPowerUpDecorator(self.balloon, pu.effect).apply() # dodaje se gorivo
                        self.display_message(f"Fuel + {pu.effect}%", duration = 1500, message_type="powerup")
                        self.powerups.remove(pu)
                    elif isinstance(pu, ShieldPowerUp):
                        ShieldPowerUpDecorator(self.balloon, pu.effect).apply() # aktivira se štit
                        duration_sec = pu.effect
                        self.display_message(f"Shield: {duration_sec:.1f}s", duration=1500, message_type="powerup")
                        self.scoreboard.set_active_powerup("Shield", duration_sec)
                        self.powerups.remove(pu)
            
            # Poruka koja obaviještava igrača da je trajanje štita isteklo
            if self.prev_shield_active and not self.balloon.shield_active:
                 self.display_message("Shield expired", duration = 1500, message_type="status")
            self.prev_shield_active = self.balloon.shield_active
            
            # Gorivo se smanjuje tijekom vremena
            self.stats.fuel -= self.settings.fuel_decrease_rate * dt
            
            # Provjera goriva, ako ga nestane gubi se život
            if self.stats.fuel <=0:
                self.stats.lives -= 1 # umanjuje broj života za 1
                print("No more fuel. Life lost!")
                if self.stats.lives > 0:
                    self.stats.fuel = self.settings.initial_fuel
                    self.reset_position()
                    self.scoreboard.prep_lives()
                    self.display_message("Out of fuel! Life lost!", duration = 2000)
                else:
                    self.stats.lives = 0
                    self.scoreboard.prep_lives()
                    #self.display_message("No more lives! Game Over!", duration = 2000)
                    print("Game Over! No more lives!")
                    pygame.time.delay(2000)
                    self.stats.game_active = False
                    return


    def spawn_obstacles(self, obstacle_factory):
        """ 
        Nasumično pojavljivanje prepreka.
        Koristi ObstacleFactory.
        """
        # povećavanje pojavljivanja s dostignutom visinom
        current_spawn_rate = min(self.settings.obstacle_spawn_rate * (1+ self.stats.score / 1000), 0.02)
        if random.random() < current_spawn_rate:
            # nasumično kreiranje ptice ili oblaka
            new_o = obstacle_factory.create_obstacle(self.screen, random.choice(["bird", "cloud"]), self.settings)
            self.obstacles.add(new_o)

    def spawn_powerups(self, powerup_factory):
        """ 
        Nasumično pojavljivanje power-upova. 
        Koristi PowerUpFactory.
        """
        available_powerups = ["fuel_small", "fuel_large", "shield_short", "shield_long"] # svi dostupni power-upovi
        if random.random() < self.settings.powerup_spawn_rate:
            chosen = random.choice(available_powerups)
            new_pu = powerup_factory.create_powerup(self.screen, chosen, self.settings)
            #print(f"Spawned {chosen} at {new_pu.rect.x}, {new_pu.rect.y}")
            self.powerups.add(new_pu)
    
    def update_screen(self):
        """ Renderiranje svih elemenata igre na ekranu. """
        self.screen.fill(self.settings.bg_color)
        self.balloon.blitme()
        self.obstacles.draw(self.screen)
        self.powerups.draw(self.screen)
        self.scoreboard.show_score()

        # Ako je igra završena pojavljuje se tekst Game Over! prije prikazivanja Play gumba
        if not self.stats.game_active and self.stats.lives == 0 and not self.game_over_shown:
            font = pygame.font.SysFont(None, 80)
            text_surface = font.render("GAME OVER!", True, (255, 0, 0))
            text_rect = text_surface.get_rect(center=(self.screen.get_rect().centerx, self.screen.get_rect().centery - 50))
            self.screen.blit(text_surface, text_rect)
            pygame.display.flip()
            pygame.time.delay(2000)
            self.game_over_shown = True
            
        # Ako je igra neaktivna pojavljuje se Play button za pokretanje nove
        if not self.stats.game_active:
            self.play_button.draw_button()

        pygame.display.flip()

    def run_game(self):
        """ 
        Glavna petlja igre. 
        Kontinuirano obrađuje evente, ažurira objekte, ubacuje nove prepreke i
        power-upove, renderira ekran.
        Koristi se clock za izračun delta vremena (dt) za kretanje neovisno o frame rate-u.
        """
        clock = pygame.time.Clock()
        obstacle_factory = ObstacleFactory()
        powerup_factory = PowerUpFactory()

        while True:
            dt = clock.tick(60) / 1000 # dt - vrijeme u sekundama od posljednjeg frejma
            self.check_events()
            if self.stats.game_active:
                self.update_game(dt)
                self.spawn_obstacles(obstacle_factory)
                self.spawn_powerups(powerup_factory)
            self.update_screen()
