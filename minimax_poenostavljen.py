import logging
import random
import logika
# from flood_it import VELIKOST_IGRALNE_PLOSCE
VELIKOST_IGRALNE_PLOSCE = 12
## Algoritem minimax

class Minimax_poenostavljen():
    # Algoritem minimax predstavimo z objektom, ki hrani stanje igre in
    # algoritma, nima pa dostopa do GUI (ker ga ne sme uporabljati, saj deluje
    # v drugem vlaknu kot tkinter).

    def __init__(self, globina, velikost):
        self.globina = globina  # do katere globine iščemo
        self.prekinitev = False  # ali moramo končati?
        self.jaz = None  # katerega igralca igramo (podatek dobimo kasneje)
        self.poteza = None  # sem napišemo potezo, ko jo najdemo
        #self.logika = logika.Logika(velikost)
        self.logika = None

    def prekini(self):
        """Metoda, ki jo pokliče GUI, če je treba nehati razmišljati, ker
           je uporabnik zaprl okno ali izbral novo igro."""
        self.prekinitev = True

    def izracunaj_potezo(self, logika):
        """Izračunaj potezo za trenutno stanje dane igre."""
        # To metodo pokličemo iz vzporednega vlakna
        self.logika = logika
        self.prekinitev = False  # Glavno vlakno bo to nastavilo na True, če moramo nehati
        self.jaz = self.logika.na_potezi
        self.poteza = None  # Sem napišemo potezo, ko jo najdemo

        # Poženemo minimax
        (poteza, vrednost) = self.minimax(self.globina, True)
        self.jaz = None
        self.logika = None
        if not self.prekinitev:
            # Potezo izvedemo v primeru, da nismo bili prekinjeni
            logging.debug("minimax: poteza {0}, vrednost {1}".format(poteza, vrednost))
            self.poteza = poteza


    # Vrednosti igre
    VREDNOST_POLJA = 1
    ZMAGA = VELIKOST_IGRALNE_PLOSCE * VELIKOST_IGRALNE_PLOSCE - 1
    NESKONCNO = 100 * VELIKOST_IGRALNE_PLOSCE * VELIKOST_IGRALNE_PLOSCE  # Več kot zmaga

    def vrednost_pozicije(self):
        (prvi_igralec, drugi_igralec) = self.logika.get_rezultat()
        if self.jaz == logika.IGRALEC1:
            return prvi_igralec
        elif self.jaz == logika.IGRALEC2:
            return drugi_igralec
        else:
            assert False

    def minimax(self, globina, maksimiziramo):
        """Glavna metoda minimax."""
        if self.prekinitev:
            # Sporočili so nam, da moramo prekiniti
            logging.debug("Minimax prekinja, globina = {0}".format(globina))
            return (None, 0)
        zmagovalec = self.logika.stanje_igre()
        if zmagovalec in (logika.IGRALEC1, logika.IGRALEC2, logika.NEODLOCENO):
            # Igre je konec, vrnemo njeno vrednost.
            return (None, (self.vrednost_pozicije()))
        elif zmagovalec == logika.NI_KONEC:
            # Igre ni konec
            if globina == 0:
                return (None, self.vrednost_pozicije())
            else:
                # Naredimo eno stopnjo minimax
                if maksimiziramo:
                    # Maksimiziramo
                    najboljsa_poteza = None
                    vrednost_najboljse = -Minimax_poenostavljen.NESKONCNO
                    for p in self.logika.veljavne_poteze():
                        self.logika.naredi_potezo(p)
                        vrednost = self.minimax(globina-1, False)[1]
                        self.logika.razveljavi()
                        if vrednost > vrednost_najboljse:
                            vrednost_najboljse = vrednost
                            najboljsa_poteza = p
                    if najboljsa_poteza == None:
                        najboljsa_poteza = poteza
                else:
                    # Minimiziramo
                    najboljsa_poteza = None
                    vrednost_najboljse = Minimax_poenostavljen.NESKONCNO
                    for p in self.logika.veljavne_poteze():
                        self.logika.naredi_potezo(p)
                        vrednost = self.minimax(globina-1, True)[1]
                        self.logika.razveljavi()
                        if vrednost < vrednost_najboljse:
                            vrednost_najboljse = vrednost
                            najboljsa_poteza = p
                    if najboljsa_poteza == None:
                        najboljsa_poteza = poteza
                assert (najboljsa_poteza is not None), "minimax: izračunana poteza je None"
                return (najboljsa_poteza, vrednost_najboljse)
        else:
            assert False, "minimax: nedefinirano stanje igre"