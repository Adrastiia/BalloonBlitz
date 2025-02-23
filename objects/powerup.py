"""
objects/powerup.py
    Definiraju se power-up bazne klase i specifične klase - gorivo i štit, kao i kompozit za grupiranje istih
"""

import pygame
import random
from pygame.sprite import Sprite

class PowerUp(Sprite):
    """ 
    Bazna klasa za power-upove.
        effect - Za gorivo je postotak dodanog goriva, a za štit je trajanje štita.
    """
    def __init__(self, screen, image_path, effect, settings):
        """ 
        Inicijalizacija powerup objekta.
        Učitava se slika power-upa, postavlja mu se veličina i početna x
        pozicija te se sprema efekt.
        """
        super().__init__()
        self.screen = screen
    	# učitavanje slike power-upa
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        # postavljanje početne x pozicije nasumično unutar ekrana
        self.rect.x = random.randint(0, screen.get_rect().width - self.rect.width)
        self.effect = effect #Kod goriva je postotak, kod štita trajanje
        self.speed = settings.powerup_speed # vertikalna brzina

    def update(self, dt):
        """ 
        Ažurira vertikalnu poziciju power-upa.
        Spušta se prema dolje, a kada izađe iz ekrana briše se
        """
        self.rect.y += self.speed * dt
        # ako je ispod donjeg dijela ekrana briše se iz igre
        if self.rect.top > self.screen.get_rect().height:
            self.kill()

class FuelPowerUp(PowerUp):
    """ Power-up koji povećava količinu dostupnog goriva. """
    def __init__(self, screen, amount, settings):
        """
        Inicijalizira FuelPowerUp.
            amount -  postotak goriva koji se dodaje
        """
        super().__init__(screen, "assets/fuel.png", amount, settings)

class ShieldPowerUp(PowerUp):
    """ Power-up koji daje štit balonu kako bi bio imun na prepreke. """
    def __init__(self, screen, duration, settings):
        """ 
        Inicijalizira ShieldPowerUp.
            duration - trajanje štita u sekundama.
        """
        super().__init__(screen, "assets/shield.png", duration, settings)

# Kompozit za power-upove
class PowerUpComposite:
    """ Grupiranje power-upova i upravljanje istima.
    Koristi se kompozit obrazac kako bi se sa više power-upova upravljalo
    kao cjelinom. Omogućuje dodavanje, uklanjanje, ažuriranje i crtanje
    svih power-upova. """
    def __init__(self):
        """ Inicijalizira prazan popis power-upova. """
        self.children = []

    def add(self, powerup):
        """ Dodaje power-up u kompozit. """
        self.children.append(powerup)

    def remove(self, powerup):
        """ Uklanja power-up iz kompozita (ako postoji)"""
        if powerup in self.children:
            self.children.remove(powerup)

    def update(self, dt):
        """ Ažurira sve power-upove unutar kompozita"""
        for pu in self.children[:]:
            pu.update(dt)

    def draw(self, screen):
        """ Crta sve power-upove na ekranu. """
        for pu in self.children:
            screen.blit(pu.image, pu.rect)