import logging
import random
import logika
from flood_it import VELIKOST_IGRALNE_PLOSCE

## Algoritem minimax

class Minimax():
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
        spremenljivka = self.izberi_potezo(self.globina, True)
        poteza, vrednost = spremenljivka
        self.jaz = None
        self.logika = None
        if not self.prekinitev:
            #Potezo izvedemo v primeru, da nismo bili prekinjeni
            logging.debug("minimax: poteza {0}, vrednost {1}".format(poteza, vrednost))
            self.poteza = poteza


    # Vrednosti igre
    VREDNOST_POLJA = 1
    ZMAGA = VELIKOST_IGRALNE_PLOSCE * VELIKOST_IGRALNE_PLOSCE - 1
    NESKONCNO = 100 * VELIKOST_IGRALNE_PLOSCE * VELIKOST_IGRALNE_PLOSCE  # Več kot zmaga

    def vrednost_pozicije(self):
        # TODO
        (prvi_igralec, drugi_igralec) = self.logika.get_rezultat()
        if self.jaz == logika.IGRALEC1:
            # return (prvi_igralec - drugi_igralec, prvi_igralec, - len(self.logika.zgodovina))
            return (prvi_igralec - drugi_igralec)
        elif self.jaz == logika.IGRALEC2:
            # return (drugi_igralec - prvi_igralec, drugi_igralec,  -len(self.logika.zgodovina))
            return (drugi_igralec - prvi_igralec)
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
                #print("Globina je 0. Vrednost pozicije je {}".format(self.vrednost_pozicije()))
                return (None, self.vrednost_pozicije())
            else:
                # Naredimo eno stopnjo minimax
                if maksimiziramo:
                    # Maksimiziramo
                    najboljsa_poteza = None
                    vrednost_najboljse = -Minimax.NESKONCNO
                    # print(str(self.logika.veljavne_poteze()))
                    najboljse_poteze = set()
                    for p in self.logika.veljavne_poteze():
                        self.logika.naredi_potezo(p)
                        vrednost = self.minimax(globina-1, False)[1]
                        self.logika.razveljavi()
                        #print("max: globina = {}, poteza = {}".format(globina, p))
                        #print("{0}max ({1}): best = {2}, current = {3}".format("  " * (6 - globina), self.jaz, (vrednost_najboljse, najboljsa_poteza), (vrednost, p)))
                        if vrednost == vrednost_najboljse:
                            najboljse_poteze.add(p)
                            #print ("max: našel sem enako dobro potezo. Množica najboljših potez je {}".format(najboljse_poteze))
                        elif vrednost > vrednost_najboljse:
                            najboljse_poteze.clear()
                            vrednost_najboljse = vrednost
                            najboljse_poteze.add(p)
                            #print("max: našel sem boljšo potezo. Množica najboljših potez je {}".format(najboljse_poteze))
                        else:
                            pass

                else:
                    # Minimiziramo
                    najboljsa_poteza = None
                    vrednost_najboljse = Minimax.NESKONCNO
                    # print(str(self.logika.veljavne_poteze()))
                    najboljse_poteze = set()
                    for p in self.logika.veljavne_poteze():
                        self.logika.naredi_potezo(p)
                        vrednost = self.minimax(globina-1, True)[1]
                        self.logika.razveljavi()
                        #print("{0}min ({1}): best = {2}, current = {3}".format("  " * (6 - globina), self.jaz, (vrednost_najboljse, najboljsa_poteza), (vrednost, p)))
                        if vrednost == vrednost_najboljse:
                            najboljse_poteze.add(p)
                            #print ("min: našel sem enako dobro potezo. Množica najboljših potez je {}".format(najboljse_poteze))
                            #print("min Našli smo enakovredno potezo. Množica potez = {}".format(najboljse_poteze))
                        elif vrednost < vrednost_najboljse:
                            #print("min Našli smo boljšo potezo.")
                            najboljse_poteze.clear()
                            vrednost_najboljse = vrednost
                            najboljse_poteze.add(p)
                            #print("max: našel sem boljšo potezo. Množica najboljših potez je {}".format(najboljse_poteze))
                    #else:
                        #print("min Ni najboljših potez.")
                #print("končal sem z minimaksom, najboljse poteze so {}, njihova vrednost je {}.".format(najboljse_poteze,vrednost_najboljse))
                #assert (len(najboljse_poteze) <= 0), "minimax: izračunana poteza je None"
                return (najboljse_poteze, vrednost_najboljse)
        else:
            assert False, "minimax: nedefinirano stanje igre"

    def izberi_potezo(self, globina, maksimiziramo):
        (najboljse_poteze, vrednost_najboljsih) = self.minimax(globina, maksimiziramo)
        #print ("izberi: najboljse poteze so {}".format(najboljse_poteze))
        if len(najboljse_poteze) == 1:
            #print ("izberi: najboljša poteza je samo ena: {}".format(najboljse_poteze))
            najboljsa_poteza = najboljse_poteze.pop()
            return (najboljsa_poteza, vrednost_najboljsih)
        else:
            #print("izberi: našli smo več najboljših potez {}.".format(najboljse_poteze))
            if globina == 1:
                najboljsa_poteza = random.choice(tuple(najboljse_poteze))
                #print("izberi: globina je 1, izbrali smo {}".format(najboljsa_poteza))
                return (najboljsa_poteza, vrednost_najboljsih)
            najboljse_poteze_manjsa_globina = self.minimax(globina-1, maksimiziramo)[0]
            #print("izberi: najboljse poteze na manjsi globini so {}".format(najboljse_poteze_manjsa_globina))
            presek = set()
            for poteza in najboljse_poteze:
                if poteza in najboljse_poteze_manjsa_globina:
                    presek.add(poteza)
            #print("izber: presek je {}".format(presek))
            if len(presek) == 0:
                najboljsa_poteza = random.choice(tuple(najboljse_poteze))
                #print ("presek je bil prazen, izbrali smo {}".format(najboljsa_poteza))
                return (najboljsa_poteza, vrednost_najboljsih)
            elif len(presek) == 1:
                najboljsa_poteza = presek.pop()
                #print ("v preseku je bil en element. Torej vracamo {},{}".format(najboljsa_poteza, vrednost_najboljsih))
                return (najboljsa_poteza, vrednost_najboljsih)
            else:
                return self.izberi_potezo(globina-1, maksimiziramo)
