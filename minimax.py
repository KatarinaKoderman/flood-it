#########################################################################
#                                                                       #
#                                  Minimax                              #
#                                                                       #
#########################################################################

import logging
import random
import logika
from flood_it import VELIKOST_IGRALNE_PLOSCE

## Algoritem minimax

class Minimax():
    # Algoritem minimax predstavimo z objektom, ki hrani stanje igre in algoritma.

    def __init__(self, globina, velikost):
        self.globina = globina  # Do katere globine iščemo.
        self.prekinitev = False  # Ali moramo končati?
        self.jaz = None  # Katerega igralca igramo (podatek dobimo kasneje).
        self.poteza = None  # Sem napišemo potezo, ko jo najdemo.
        self.logika = None

    def prekini(self):
        """Metoda, ki jo pokliče GUI, če je treba nehati razmišljati, ker
           je uporabnik zaprl okno ali izbral novo igro."""
        self.prekinitev = True

    def izracunaj_potezo(self, logika):
        """Izračunaj potezo za trenutno stanje dane igre."""
        # To metodo pokličemo iz vzporednega vlakna.
        self.logika = logika
        self.prekinitev = False  # Glavno vlakno bo to nastavilo na True, če moramo nehati.
        self.jaz = self.logika.na_potezi
        self.poteza = None  # Sem napišemo potezo, ko jo najdemo.

        # Poženemo minimax
        (poteza, vrednost) = self.izberi_potezo(self.globina, True)
        self.jaz = None
        self.logika = None
        if not self.prekinitev:
            # Potezo izvedemo v primeru, da nismo bili prekinjeni.
            logging.debug("minimax: poteza {0}, vrednost {1}".format(poteza, vrednost))
            self.poteza = poteza

    # Vrednosti igre
    # TODO konstant VREDNOST_POLJA in ZMAGA ne uporabljava
    VREDNOST_POLJA = 1
    ZMAGA = VELIKOST_IGRALNE_PLOSCE * VELIKOST_IGRALNE_PLOSCE - 1
    NESKONCNO = 100 * VELIKOST_IGRALNE_PLOSCE * VELIKOST_IGRALNE_PLOSCE  # Več kot zmaga

    def vrednost_pozicije(self):
        """Oceni vrednost pozicije. Vrne razliko med rezultatoma igralcev."""
        (prvi_igralec, drugi_igralec) = self.logika.get_rezultat()
        if self.jaz == logika.IGRALEC1:
            return (prvi_igralec - drugi_igralec)
        elif self.jaz == logika.IGRALEC2:
            return (drugi_igralec - prvi_igralec)
        else:
            assert False

    def minimax(self, globina, maksimiziramo):
        """Glavna metoda minimax."""
        if self.prekinitev:
            # Sporočili so nam, da moramo prekiniti.
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
                # Naredimo eno stopnjo minimax:
                if maksimiziramo:
                    # Maksimiziramo
                    vrednost_najboljse = -Minimax.NESKONCNO
                    najboljse_poteze = set()
                    for p in self.logika.veljavne_poteze():
                        self.logika.naredi_potezo(p)
                        vrednost = self.minimax(globina-1, False)[1]
                        self.logika.razveljavi()
                        if vrednost == vrednost_najboljse:
                            najboljse_poteze.add(p)
                        elif vrednost > vrednost_najboljse:
                            najboljse_poteze.clear()
                            vrednost_najboljse = vrednost
                            najboljse_poteze.add(p)

                else:
                    # Minimiziramo
                    vrednost_najboljse = Minimax.NESKONCNO
                    najboljse_poteze = set()
                    for p in self.logika.veljavne_poteze():
                        self.logika.naredi_potezo(p)
                        vrednost = self.minimax(globina-1, True)[1]
                        self.logika.razveljavi()
                        if vrednost == vrednost_najboljse:
                            najboljse_poteze.add(p)
                        elif vrednost < vrednost_najboljse:
                            najboljse_poteze.clear()
                            vrednost_najboljse = vrednost
                            najboljse_poteze.add(p)

                assert (len(najboljse_poteze) > 0), "minimax: množica najboljših potez je prazna"
                return (najboljse_poteze, vrednost_najboljse)
        else:
            assert False, "minimax: nedefinirano stanje igre"

    def izberi_potezo(self, globina, maksimiziramo):
        """Iz množice najboljših potez izbere tisto, ki nam v naslednji potezi prinese največ točk."""
        (najboljse_poteze, vrednost_najboljsih) = self.minimax(globina, maksimiziramo)
        if len(najboljse_poteze) == 1:
            # Našli smo le eno najboljšo potezo, jo izberemo:
            najboljsa_poteza = najboljse_poteze.pop()
            return (najboljsa_poteza, vrednost_najboljsih)
        else:
            najboljsa_vrednost = -Minimax.NESKONCNO
            for poteza in najboljse_poteze:
                self.logika.naredi_potezo(poteza)
                vrednost = self.vrednost_pozicije()
                if vrednost > najboljsa_vrednost:
                    najboljsa_vrednost = vrednost
                    najboljsa_poteza = poteza
                self.logika.razveljavi()
            return (najboljsa_poteza, vrednost_najboljsih)

