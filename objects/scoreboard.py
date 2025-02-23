"""
objects/scoreboard.py
    Prikazuje statistiku igre - bodove (visinu), najveće osvojene bodove (visinu),
    postotak dostupnog goriva i živote, power-up poruke (koji power-up je aktivan)
    i status poruke iz GameLoop-a.
"""
import pygame.font

class Scoreboard:
    """ Upravlja prikazom statistike i poruka. """
    def __init__(self,settings,screen,stats):
        """ 
        Inicijalizira Scoreboard objekt. 
        Postavlja reference na ekran, postavke i statistiku te inicijalizira
        boju teksta, font i početne vrijednosti poruka. Priprema početne prikaze
        bodova, najviše osvojenih bodova, goriva i života.
        """
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.settings = settings
        self.stats = stats

        self.text_color = (18,0,36) # tamno ljubičasta boja teksta
        self.font = pygame.font.SysFont(None,48)

        # Inicijalno prazna poruka za aktivni power-up
        self.active_powerup = ""
        self.powerup_expiration = 0

        # Statusne poruke (na sredini ekrana)
        self.status_message = ""
        self.status_expiration = 0

        # Priprema početnih prikaza statistike
        self.prep_score()
        self.prep_high_score()
        self.prep_fuel()
        self.prep_lives()

    def prep_score(self):
        """ 
        Renderira trenutne bodove (visinu).
        Kreiranje tekstualnog prikaza trenutnog broja bodova i prikaz u gornjem
        lijevom kutu ekrana. 
        """
        score_str = f"Altitude: {int(self.stats.score)}"
        self.score_image = self.font.render(score_str, True, self.text_color)
        self.score_rect = self.score_image.get_rect()
        self.score_rect.left = 20
        self.score_rect.top = 20

    def prep_high_score(self):
        """ 
        Renderira najveće osvojene bodove (visinu).
        Kreiranje tekstualnog prikaza  najviše osvojenih broja bodova i prikaz 
        ispod prikaza bodova.
        """
        high_score_str = f"Highest altitude: {int(self.stats.high_score)}"
        self.high_score_image = self.font.render(high_score_str, True, self.text_color)
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = 20

    def prep_fuel(self):
        """ 
        Renderira trenutnu količinu dostupnog goriva.
        Kreiranje tekstualnog prikaza postotka dostupnog goriva i prikaz ispod
        prikaza bodova. 
        """
        fuel_str = f"Fuel: {int(self.stats.fuel)}%"
        self.fuel_image = self.font.render(fuel_str, True, self.text_color)
        self.fuel_rect = self.fuel_image.get_rect()
        self.fuel_rect.left = 20
        self.fuel_rect.top = self.score_rect.bottom + 10

    def prep_lives(self):
        """ 
        Renderira dostupan broj života. 
        Kreiranje tekstualnog prikaza dostupnog broja života i prikaz ispod
        prikaza goriva.
        """
        lives_str = f"Lives: {max(self.stats.lives, 0)}"
        self.lives_image = self.font.render(lives_str, True, self.text_color)
        self.lives_rect = self.lives_image.get_rect()
        self.lives_rect.top = self.fuel_rect.bottom + 10
        self.lives_rect.left = 20

    def set_active_powerup(self, name, duration):
        """ 
        Postavlja poruku za trenutno aktivni power-up.
            name - naziv power-upa
            duration - duljina trajanja poruke
        """
        self.active_powerup = name
        self.powerup_expiration = pygame.time.get_ticks() + (duration*1000) # u milisekundama

    def set_status_message(self, message, duration):
        """
        Postavlja statusnu poruku
            message - text poruke (npr. Game Over!, Life Lost!)
        """
        self.status_message = message
        self.status_expiration = pygame.time.get_ticks() + duration

    def show_score(self):
        """ Crta bodove, najveće osvojene bodove, živote i poruku koji je power-up aktivan na ekranu"""
        # Prikaz statistike
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.fuel_image, self.fuel_rect)
        self.screen.blit(self.lives_image, self.lives_rect)

        # Crta poruku koji je power-up aktivan ispod dostupnih života
        if self.active_powerup and pygame.time.get_ticks() < self.powerup_expiration:
            powerup_str = f"Power-Up: {self.active_powerup}"
            powerup_image = self.font.render(powerup_str, True, (0, 143, 90))
            powerup_rect = powerup_image.get_rect()
            powerup_rect.top = self.lives_rect.bottom + 10
            powerup_rect.left = 20
            self.screen.blit(powerup_image,powerup_rect)
        
        # Prikaz centralne poruka ako je još aktivna
        if self.status_message and pygame.time.get_ticks() < self.status_expiration:
            font = pygame.font.SysFont(None,80)
            text_surface = font.render(self.status_message, True, (255,0,0))
            text_rect = text_surface.get_rect(center = self.screen_rect.center)
            self.screen.blit(text_surface, text_rect)