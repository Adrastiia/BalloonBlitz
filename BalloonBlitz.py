import pygame
from core.settings import Settings
from core.gameloop import GameLoop
from core.gamestats import GameStats
from core.factory import BalloonFactory, ObstacleFactory, PowerUpFactory
from objects.button import Button
from objects.scoreboard import Scoreboard
from objects.obstacle import ObstacleComposite
from objects.powerup import PowerUpComposite

def main():
    """ 
    Glavna funkcija za pokretanje igre.
    Inicijalizira pygame, kreira instancu postavki (Settings) koja sadrži konfiguraciju igre,
    stvara glavni prozor prema dimenzijama iz postavki, inicijalizira GameStats (objekt statistike)
    koji prati bodove, high score, živote i gorivo, kreira također Scoreboard za prikazivanje
    statistike na ekranu. Kreira i Play gumb koji omogućava ponovno pokretanje igre te balon objekt
    koristeći BalloonFactory. Kreira kompozite za prepreke i power-upove te inicijalizira glavnu petlju
    igre (GameLoop).
    """
    pygame.init() # inicijalizacija pygame modula

    settings = Settings() # kreiranje instanci postavki
    screen = pygame.display.set_mode((settings.screen_width, settings.screen_height)) # stvara glavni prozor
    pygame.display.set_caption("Balloon Blitz") # naslov prozora

    stats = GameStats(settings) # inicijalizacija statistike
    scoreboard = Scoreboard(settings,screen,stats) # kreiranje Scoreboard-a za prikaz statistike
    play_button = Button(settings,screen,"Play") # kreiranje Play gumva


    balloon = BalloonFactory.create_balloon(screen, stats) # kreiranje balona
    obstacles = ObstacleComposite() # kreiranje kompozita za prepreke
    powerups = PowerUpComposite() # kreiranje kompozita za power-upove
   
    
    game_loop = GameLoop(settings, screen, balloon, obstacles, powerups, play_button, scoreboard, stats) #inicijalizacija game loop-a
    stats.game_active = False # postavlja igru na status neaktivna (postaje aktivna pritiskom na Play gumb)
    game_loop.run_game() # pokreće glavnu petlju igre

if __name__ == "__main__":
    main()
