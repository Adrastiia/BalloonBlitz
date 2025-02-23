"""
core/settings.py
    Definira sve postavke igre Balloon Blitz. 
    Vremena su izražena u sekundama.
    Brzine su izražene u pikselima po sekundi.
"""

class Settings:
    """
    Klasa koja sadrži sve statičke i dinamičke postavke za Balloon Blitz igru.
        screen_width - širina ekrana igre
        screen_height - visina ekrana igre
        bg_color - boja pozadine
        balloon_speed - horizontalna brzina balona
        balloon_rise_speed - vertikalna brzina balona
        initial_fuel - početna količina goriva
        fuel_deacrease_rate - potrošnja goriva po sekundi
        obstacle_speed_x - horizontalna brzina prepreka
        obstacle_spawn_rate - vjerojatnost pojave prepreke
        powerup_speed - vertikalna brzina power-upova
        powerup_spawn_rate - vjerojatnost pojave power-upova
        score_increment - dodani bodovi po sekundi
        balloon_limit - broj života 
    """
    def __init__(self):
        """Inicijalizacija statičkih postavki."""
        # Postavke ekrana.
        self.screen_width = 1400
        self.screen_height = 1000
        self.bg_color = (219, 208, 255) # ljubičasta pozadinska boja

        # Postavke balona.
        self.balloon_speed = 500 # brzina kretanja balona lijevo - desno
        self.balloon_rise_speed = 90 # brzina pomicanje balona prema gore
        
        self.initial_fuel = 100 # početna količina goriva
        self.fuel_decrease_rate = 0.5 # brzina potrošnje goriva

        # Postavke prepreka.
        self.obstacle_speed_x = 40 # brzina pomicanja prepreka - horizontalno (ptice i oblaci)
        self.obstacle_speed_y = 0 # prepreke nemaju vertikalnu brzinu
        self.obstacle_spawn_rate = 0.004 # koliko često se prepreke pojavljuju

        # Postavke poweer-upova.
        self.powerup_speed = 80 # brzina pomicanja, odnosno spuštanja
        self.powerup_spawn_rate = 0.0008 # koliko se često power-upovi stvaraju
        
        # Povećavanje bodova (po sekundi)
        self.score_increment = 1 

        # Broj života/balona
        self.balloon_limit = 3

        # Inicijalizacija dinamičkih postavki
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Inicijalizacija postavki koje se mijenjaju tijekom igre."""
        self.dynamic_obstacle_speed = self.obstacle_speed_x
        self.dynamic_fuel = self.initial_fuel # dinamička količina goriva - ažurira se tijekom igre
        self.dynamic_balloon_speed = self.balloon_speed

