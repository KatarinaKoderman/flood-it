import logging
import logika
# TODO v logika.py imamo funkcijo, ki določa nasprotnika + ostalo
from flood_it import VELIKOST_IGRALNE_PLOSCE

# TODO parametre vzamemo iz igre (flood_it)
# uvedemo parametre:
IGRALEC_1 = "1"  # igralec, ki začne v zgornjem levem kotu
IGRALEC_2 = "2"  # igralec, ki začne v spodnjem desnem kotu
NEODLOCENO = "neodločeno"
NI_KONEC = "ni konec"
# VELIKOST_IGRALNE_PLOSCE lahko spreminjamo v Gui-ju.  # TODO zaenkrat

## Algoritem minimax

class Minimax:
    # Algoritem minimax predstavimo z objektom, ki hrani stanje igre in
    # algoritma, nima pa dostopa do GUI (ker ga ne sme uporabljati, saj deluje
    # v drugem vlaknu kot tkinter).

    def __init__(self, globina, velikost):
        self.globina_racunanja = globina
        self.globina = globina  # do katere globine iščemo?
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
        (poteza, vrednost) = self.minimax(self.globina_racunanja, True)
        self.jaz = None
        self.logika = None
        if not self.prekinitev:
            # Potezo izvedemo v primeru, da nismo bili prekinjeni
            logging.debug("minimax: poteza {0}, vrednost {1}".format(poteza, vrednost))
            self.poteza = poteza

    # Vrednosti igre
    VREDNOST_POLJA = 1  # Mora biti vsaj 10^5
    NESKONCNO = VELIKOST_IGRALNE_PLOSCE * VELIKOST_IGRALNE_PLOSCE  # Več kot zmaga

    def vrednost_pozicije(self):
        # TODO
        """Ocena vrednosti pozicije: sešteje vrednosti vseh trojk na plošči."""
        # Slovar, ki pove, koliko so vredne posamezne trojke, kjer "(x,y) : v" pomeni:
        # če imamo v trojki x znakov igralca in y znakov nasprotnika (in 3-x-y praznih polj),
        # potem je taka trojka za self.jaz vredna v.
        # Trojke, ki se ne pojavljajo v slovarju, so vredne 0.
        (prvi_igralec, drugi_igralec) = self.logika.rezultat
        return drugi_igralec - prvi_igralec

    def minimax(self, globina, maksimiziramo):
        """Glavna metoda minimax."""
        if self.prekinitev:
            # Sporočili so nam, da moramo prekiniti
            logging.debug("Minimax prekinja, globina = {0}".format(globina))
            return None, 0
        zmagovalec = self.logika.stanje_igre()
        if zmagovalec in (IGRALEC_1, IGRALEC_2, NEODLOCENO):
            # Igre je konec, vrnemo njeno vrednost
            if zmagovalec == self.jaz:
                return (None, Minimax.ZMAGA)
            elif zmagovalec == self.logika.nasprotnik(self.jaz):
                return (None, -Minimax.ZMAGA)
            else:
                return (None, 0)
        elif zmagovalec == NI_KONEC:
            # Igre ni konec
            if globina == 0:
                return (None, self.vrednost_pozicije())
            else:
                # Naredimo eno stopnjo minimax
                if maksimiziramo:
                    print("maksimiziramo")
                    # Maksimiziramo
                    najboljsa_poteza = None
                    vrednost_najboljse = -Minimax.NESKONCNO
                    for p in self.logika.veljavne_poteze():
                        self.logika.naredi_potezo(p)
                        vrednost = self.minimax(globina-1, False)[1]
                        self.logika.razveljavi()
                        if vrednost > vrednost_najboljse:
                            vrednost_najboljse = vrednost
                            najboljsa_poteza = p
                else:
                    # Minimiziramo
                    print("minimiziramo")
                    najboljsa_poteza = None
                    vrednost_najboljse = Minimax.NESKONCNO
                    for p in self.logika.veljavne_poteze():
                        self.logika.naredi_potezo(p)
                        vrednost = self.minimax(globina-1, True)[1]
                        self.logika.razveljavi()
                        if vrednost < vrednost_najboljse:
                            vrednost_najboljse = vrednost
                            najboljsa_poteza = p

                assert (najboljsa_poteza is not None), "minimax: izračunana poteza je None"
                return (najboljsa_poteza, vrednost_najboljse)
        else:
            assert False, "minimax: nedefinirano stanje igre"