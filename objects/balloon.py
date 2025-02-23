"""
objects/balloon.py
    Definiranje klase Balloon koja predstavlja objekt kojim upravlja igrač.
"""

import pygame
from pygame.sprite import Sprite

class Balloon(Sprite):
    """ klasa koja predstavlja igračev balon """
    def __init__(self, screen, stats):
        """ 
        Inicijalizacija balon objekta.
        Učitava sliku balona, skalira ju i postavlja inicijalnu poziciju 
        balona na ekranu te postavlja status štita.

        """
        super().__init__()
        self.screen = screen
        self.stats = stats # referenca na statistiku

        # Učitavanje i skaliranje slike balona
        self.image = pygame.image.load("assets/balloon.png")
        self.image = pygame.transform.scale(self.image, (80, 120))

        self.rect = self.image.get_rect()
        self.screen_rect = self.screen.get_rect()

        # Početna pozicija balona, centriran horizontalno
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom - 50
        self.initial_y = self.rect.y

        # Kontrola horizontalnog kretanja
        self.moving_left = False
        self.moving_right = False

        # Status štit power-upa 
        self.shield_active = False
        self.shield_timer = 0

    def update(self,dt):
        """ 
        Ažurira poziciju balona ovisno o kretanju i količinu goriva. 
        Ako se balon kreće lijevo ili desno ažurira se x koordinata i osigurava se
        da balon ne izađe izvan granica ekrana.
        Ako ima dostupnog goriva balon se kreće vertikalno, a gorivo se smanjuje tijekom vremena.
        """
        # Ažuriranje horizontalne pozicije
        if self.moving_left:
            # pomicanje u lijevo, x koordinata ne ide ispod 0, odnosno lijevog ruba ekrana
            self.rect.x = max(self.rect.x - self.stats.settings.balloon_speed * dt, 0 )
        
        if self.moving_right:
            # pomicanje u desno, balon ostaje unutar granica ekrana
            self.rect.x = min(self.rect.x + self.stats.settings.balloon_speed * dt, self.screen_rect.width - self.rect.width )

        # ažuriranje vertikalne pozicije ukoliko ima goriva
        if self.stats.fuel > 0:
            self.rect.y -= self.stats.settings.balloon_rise_speed * dt
            self.stats.fuel -= self.stats.settings.fuel_decrease_rate * dt
            # gorivo ne može pasti ispod 0
            self.stats.fuel = max(self.stats.fuel, 0)

    def update_shield(self, dt):
        """ Ažuriranje timer-a štita, kada vrijeme istekne štit se deaktivira"""
        if self.shield_active and self.shield_timer > 0:
            self.shield_timer -= dt
        if self.shield_timer <= 0:
            if self.shield_active:
                print("Shield expired.")
            self.shield_active = False
            
    def blitme(self):
        """ Crta balon na ekranu. """
        self.screen.blit(self.image, self.rect)