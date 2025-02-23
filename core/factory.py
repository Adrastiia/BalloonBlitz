"""
core/factory.py
    Sadrži factory klase koje kreiraju objekte igre.
    Osigurava laganu izmjenu kreacija objekata bez promjene logike u gameloop-u.
"""

import pygame
from objects.balloon import Balloon
from objects.obstacle import Bird, Cloud
from objects.powerup import FuelPowerUp, ShieldPowerUp
import random

class BalloonFactory:
    """ 
    Tvornica za kreiranje balon objekta.
    Ostali moduli ne moraju znati pojedinosti oko inicijalizacije balona.
    """
    @staticmethod
    def create_balloon(screen, stats):
        """
        Kreira i vraća novi Balloon objekt
            screen - pygame Surface na kojem se crta balon
            stats - GameStats objekt koji sadrži gorivo, bodovanje i sl.
        """
        return Balloon(screen, stats) # vraća instancu balona
    
class ObstacleFactory:
    """ 
    Tvornica za kreiranje prepreka - ptice i oblaci. Mogu se
    generirati ili na lijevoj ili na desnoj strani ekrana i 
    kreiraju se nasumično. 
    """
    @staticmethod
    def create_obstacle(screen, obstacle_type, settings):
        """
        Kreira i vraća novu prepreku ovisno o tipu.
            obtacle_type - označava vrstu prepreke, može biti ptica ili oblak
            settings - Settings objekt koji sasdržava konfiguracijske vrijednosti
        """
        spawn_side = random.choice(["left", "right"]) # mogući izbor strana na kojima će se stvarati prepreke
        if obstacle_type == "bird":
            return Bird(screen, settings, spawn_side) # vraća prepreku pticu sa nasumično odabranom stranom stvaranja
        elif obstacle_type == "cloud":
            return Cloud(screen, settings, spawn_side) # vraća prepreku oblak sa nasumično odabranom stranom stvaranja
        raise ValueError(f"Nepoznati tip prepreke: {obstacle_type}") # vraća grešku ako je dan nepoznat tip prepreke
    
class PowerUpFactory:
    """ 
    Tvornica za kreiranje power-upova. Mogu biti varijante goriva ili štita.
    """
    @staticmethod
    def create_powerup(screen, powerup_type, settings):
        """ Kreira i vraća novi power_up.       
                powerup_type - tip power-upa (fuel_small, fuel_large, shield_short, shield_long)
        """
        if powerup_type == "fuel_small":
            return FuelPowerUp(screen, 30, settings) # 30% dodanog goriva
        elif powerup_type == "fuel_large":
            return FuelPowerUp(screen, 70, settings) # 70% dodanog goriva
        elif powerup_type == "shield_short":
            return ShieldPowerUp(screen, 10, settings) # štit od 10 sekundi
        elif powerup_type == "shield_long":
            return ShieldPowerUp(screen, 20, settings) # štit od 20 sekundi
        raise ValueError(f"Nepoznati tip powerupa: {powerup_type}") # vraća grešku ako je dan nepoznat tip power-upa
