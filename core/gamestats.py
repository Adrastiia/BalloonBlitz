"""
core/gamestats.py
    Prati statistiku igre - životi, bodovi (visina), high score
    (najveća postignuta visina), gorivo, status igre (aktivna/neaktivna)
"""

class Singleton(type):
    """ Metaklasa koja osigurava postojanje samo jedne GameStats instance. """
    _instances = {} 

    def __call__(cls, *args, **kwargs):
        # ako ne postoji instanca klase kreira se i sprema u _instances
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, *kwargs)
        # vraća se spremljena klasa čime se osigurava postojanje samo jedne instance
        return cls._instances[cls]

class GameStats(metaclass=Singleton):
    """ 
    Klasa za praćenje statistike igre.
        fuel - trenutna količina goriva
        score - trenutni broj bodova, odnosno postignuta visina
        high_score - najveći postignuti broj bodova, odnosno najveća postignuta visina
        lives - količina preostalih života
        game_active - true ako je trenutna igra aktivna, false ako nije
    """
    def __init__(self, settings):
        """
        Inicijalizacija statistike.
        Ako GameStats već nije inicijaliziran postavljaju se vrijednosti.
        """
        # provjera je li instanca već inicijalizirana
        if not hasattr(self, "initialized"):
            self.settings = settings
            self.reset_stats() # postavlja bodove, gorivo i živote na inicijalne vrijednosti
            self.game_active = False # započinje u neaktivnom stanju
            self.high_score = 0
            self.initialized = True # izbjegava se reinicijalizacija

    def reset_stats(self):
        """ 
        Resetira statistiku koja se mijenja - gorivo, životi i bodovi, ali ne i high score 
        (najveću postignutu visinu)
        """
        self.fuel = self.settings.initial_fuel # postavlja gorivo na inicijalnu vrijednost iz postavki
        self.score = 0 # resetira bodove na 0
        self.lives = self.settings.balloon_limit # postavlja živote na inicijalnu vrijednost iz postavki

        