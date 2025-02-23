"""
objects/obstacle.py
    Definiraju se bazna klasa za prepreke i specifične prepreke - ptice i oblaci, kao i kompozit za grupiranje istih
"""

import pygame
import random
from pygame.sprite import Sprite

class Obstacle(Sprite):
    """ 
    Bazna klasa za prepreke. 
    Generička prepreka koja se pojavljuje na ekranu i kreće horizontalno.
    Prepreke se pojavljuju na lijevoj ili desnoj strani ekrana i odbijaju se 
    od rubova istog te mijenjaju smjer kretanja. Ukoliko izađu iz ekrana brišu se.
    """
    def __init__(self, screen, image_path, settings, size, spawn_side="left"):
        """ 
        Inicijalizira prepreku. 
        Učitava se slika prepreke, postavlja joj se veličina i postavlja početna
        pozicija ovisno o odabranoj strani.
        """
        super().__init__()
        self.screen = screen
        self.screen_rect = self.screen.get_rect()

        # učitavanje i skaliranje slike
        self.image = pygame.image.load(image_path) 
        #print(f"Loaded image: {image_path}")
        self.image = pygame.transform.scale(self.image,size)
        self.rect = self.image.get_rect()

        # postavljanje x pozicije pojavljivanja prepreki ovisno o strani pojavljivanja
        if spawn_side == "left":
            self.rect.x = random.randint(-self.rect.width - 20,-10)
        else:
            self.rect.x = random.randint(self.screen_rect.width + 10, self.screen_rect.width + self.rect.width + 20)
        # postavljanje početne y pozicije unutar gornjeg dijela ekrana
        self.rect.y = random.randint(20, self.screen_rect.height//6)

        # postavljanje brzine prepreke
        self.speed_x = settings.obstacle_speed_x # horizontalna brzina
        self.speed_y = settings.obstacle_speed_y # vertikalna brzina koja je 0

    def update(self, dt):
        """ Pomicanje prepreki horizontalno, kad dođu do kraja ekrana odbijaju se i 
            kreću u suprotnu stranu. Kada izađu iz ekrana brišu se iz igre. """
        
        # ažuriranje x koordinate prema horizontalnoj brzini i vremenu
        self.rect.x += self.speed_x * dt 

        # ako prepreka dođe do desnog ruba ekrana odbija se i mijenja smjer u lijevo
        if self.rect.right >= self.screen_rect.width:
            self.rect_right = self.screen_rect.width
            self.speed_x = -abs(self.speed_x) # odbijanje od ruba ekrana
            self.speed_x -= 5 # pogura prepreke prema unutrašnjosti ekrana kako ne bi zapele na rubovima
        
        # ako prepreka dođe do lijvog ruba ekrana odbija se i mijenja smjer u desno
        elif self.rect.left <= 0:
            self.rect_left = 0
            self.speed_x = abs(self.speed_x) # odbijanje od ruba ekrana
            self.speed_x += 5  # pogura prepreke prema unutrašnjosti ekrana kako ne bi zapele na rubovima
        
        # ako prepreka izađe iz donjeg dijela ekrana briše se iz igre
        if self.rect.top > self.screen_rect.height:
            self.kill() #Brisanje iz igre


class Bird(Obstacle):
    """
    Konkretna prepreka - ptica.
    Kreće se horizontalno i slika se zrcali ovisno o strani na koju ide.
    Ako se odbije od ruba ekrana slika se zrcali kako bi uvijek bila okrenuta
    u smjeru kretanja.
    """
    def __init__(self,screen, settings, spawn_side = "left"):
        """ Inicijalizira prepreku pticu. """
        super().__init__(screen, "assets/pigeon.png", settings,(50,30),spawn_side)
        self.original_image = pygame.image.load("assets/pigeon.png") # učitavanje originalne slike ptice
        self.original_image = pygame.transform.flip(self.original_image, True, False) # koristi se zrcaljena slike zbog ispravne orijentacije

        # postavljanje početne slike ovisno o strani na kojoj se pojavljuje ptica
        if spawn_side == "right":
            # ako se pojavljuje na desnoj strani slika se odmah zrcali
            self.image = pygame.transform.flip(self.original_image, True, False)
        else:
            # inače se koristi kopija originalne slike
            self.image = self.original_image.copy()


    def update(self, dt):
        """ 
        Ažurira kretanje ptice i mijenja orijentaciju slike u slučaju
        promjene smjera.
        """
        prev_speed = self.speed_x # sprema prethodnu horizontalnu brzinu zbog detekcije promjene smjera
        super().update(dt) # pozivanje bazne metode update za kretanje i odbijanje

        # ako je došlo do promjene smjera, odnosno odbijanja slika se ažurira
        if prev_speed != self.speed_x:
            if self.speed_x < 0:
                # ako se ptica kreće ulijevo koristi se originalna slika
                self.image = self.original_image.copy()
            else:
                # ako se kreće udesno zrcali se originalna slika
                self.image = pygame.transform.flip(self.original_image, True, False)

class Cloud(Obstacle):
    """
    Konkretna prepreka - oblak.
    Kreće se horizontalno.
    """
    def __init__(self,screen, settings, spawn_side = "left"):
        """ Inicijalizira prepreku oblak. """
        super().__init__(screen, "assets/cloud.png", settings,(120,80), spawn_side)

# Kompozit za prepreke
class ObstacleComposite:
    """ 
    Grupiranje prepreka i upravljanje istima.
    Koristi se kompozit obrazac kako bi se sa više prepreka upravljalo
    kao cjelinom. Omogućuje dodavanje, uklanjanje, ažuriranje i crtanje
    svih prepreka.
    """
    def __init__(self):
        """ Inicijalizira prazan popis prepreka"""
        self.children = []

    def add(self, obstacle):
        """ Dodaje prepreku u kompozit"""
        self.children.append(obstacle)
    
    def remove(self, obstacle):
        """ 
        Ukoliko postoji uklanja prepreku iz kompozita.
            obstacle - instanca prepreke koju treba ukloniti 
        """
        if obstacle in self.children:
            self.children.remove(obstacle)

    def update(self, dt):
        """ Ažurira sve prepreke unutar kompozita. """
        for o in self.children[:]:
            o.update(dt)

    def draw(self, screen):
        """ Crta sve prepreke na ekranu. """
        for o in self.children:
            screen.blit(o.image, o.rect)