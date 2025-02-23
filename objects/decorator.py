"""
objects/decorator.py
    Definiranje dekoratora za dodavanje power-upova balonu.
    Koristi se dekorator obrazac za dinamičko proširivanje funkcionalnosti balona
    bez promjene same Balloon klase.
"""

class PowerUpDecorator:
    """ 
    Bazni dekorator za power-upove, dodaju se efekti balonu. 
    Apstraktna klasa, osnova za sve dekoratore.
    Omogućuje primjenu dodatnih funkcionalnosti - povećanje goriva, aktivacija štita.
    """
    def __init__(self,balloon):
        # spremanje reference na balon koji se dekorira
        self._balloon = balloon

    def apply(self):
        """ 
        Apstraktna metoda za primjenu power-up efekta na balon.
        Implementira se u podklasama.
        """
        raise NotImplementedError()

class FuelPowerUpDecorator(PowerUpDecorator):
    """ 
    Povećavanje dostupne količine goriva za neki postotak.
    Ako se pokupi small_fuel 30% goriva će se dodati maksimalnom postotku goriva.
    """
    def __init__(self, balloon, fuel_increase):
        super().__init__(balloon) # postavljanje reference na balon
        self.fuel_increase = fuel_increase # spremanje postotka goriva koji se dodaje

    def apply(self):
        """Primjenjuje efekt povećanja goriva."""
        max_fuel = self._balloon.stats.settings.initial_fuel # maksimalna količina goriva iz postavki
        added_fuel = max_fuel * (self.fuel_increase/100) # izračun dodatnog goriva
        self._balloon.stats.fuel = min(self._balloon.stats.fuel + added_fuel, max_fuel) # povećavanje trenutnog goriva, ne može ići više od maksimalnog
        print(f"Fuel increased by {self.fuel_increase}%. Current fuel: {self._balloon.stats.fuel}")

class ShieldPowerUpDecorator(PowerUpDecorator):
    """
    Aktiviranje štita na balonu za određeno vrijeme (ovisno koji je štit pokupljen).
    Omogućava koliziju balona sa preprekama bez gubitka života.
    """
    def __init__(self, balloon, shield_duration):
        super().__init__(balloon) # postavljanje reference na balon
        self.shield_duration = shield_duration # spremanje trajanja štita u sekundama

    def apply(self):
        """Aktivira štit."""
        self._balloon.shield_active = True
        self._balloon.shield_timer = self.shield_duration
        
