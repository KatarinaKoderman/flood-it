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

    def minimax(self, globina, maksimiziramo, poteze={0, 1, 2, 3, 4, 5}):
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
                print("Globina je 0.")
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
                        if p in poteze:
                            self.logika.naredi_potezo(p)
                            vrednost = self.minimax(globina-1, False)[1]
                            self.logika.razveljavi()
                            print("max: globina = {}, poteza = {}".format(globina, p))
                            #print("{0}max ({1}): best = {2}, current = {3}".format("  " * (6 - globina), self.jaz, (vrednost_najboljse, najboljsa_poteza), (vrednost, p)))
                            if vrednost == vrednost_najboljse:
                                najboljse_poteze.add(p)
                            elif vrednost > vrednost_najboljse:
                                najboljse_poteze.clear()
                                vrednost_najboljse = vrednost
                                najboljse_poteze.add(p)
                        else:
                            pass
                    if len(najboljse_poteze) > 1:
                        if globina > 1:
                            print("max globina = {}, najboljše poteze = {}".format(globina, najboljse_poteze))
                            self.minimax(globina-1, True, najboljse_poteze)
                        else:
                            najboljsa_poteza = random.choice(tuple(najboljse_poteze))
                    if len(najboljse_poteze) == 1:
                        print("Najboljše poteze = {}.".format(najboljse_poteze))
                        najboljsa_poteza = najboljse_poteze.pop()
                        print("Najboljša poteza je samo ena = {}".format(najboljsa_poteza))
                    else:
                        print("max Ni najboljših potez.")

                else:
                    # Minimiziramo
                    najboljsa_poteza = None
                    vrednost_najboljse = Minimax.NESKONCNO
                    # print(str(self.logika.veljavne_poteze()))
                    najboljse_poteze = set()
                    for p in self.logika.veljavne_poteze():
                        if p in poteze:
                            self.logika.naredi_potezo(p)
                            vrednost = self.minimax(globina-1, True)[1]
                            self.logika.razveljavi()
                            #print("{0}min ({1}): best = {2}, current = {3}".format("  " * (6 - globina), self.jaz, (vrednost_najboljse, najboljsa_poteza), (vrednost, p)))
                            if vrednost == vrednost_najboljse:
                                najboljse_poteze.add(p)
                                print("min Našli smo enakovredno potezo. Množica potez = {}".format(najboljse_poteze))
                            elif vrednost < vrednost_najboljse:
                                print("min Našli smo boljšo potezo.")
                                najboljse_poteze.clear()
                                vrednost_najboljse = vrednost
                                najboljse_poteze.add(p)
                    if len(najboljse_poteze) > 1:
                        if globina > 1:
                            print("min globina = {}, najboljše poteze = {}".format(globina, najboljse_poteze))
                            self.minimax(globina - 1, True, najboljse_poteze)
                        else:
                            najboljsa_poteza = random.choice(tuple(najboljse_poteze))
                    if len(najboljse_poteze) == 1:
                        print("min Najboljše poteze = {}.".format(najboljse_poteze))
                        najboljsa_poteza = najboljse_poteze.pop()
                        print("min Najboljša poteza je samo ena = {}".format(najboljsa_poteza))

                    else:
                        print("min Ni najboljših potez.")
                assert (najboljsa_poteza is not None), "minimax: izračunana poteza je None"
                return (najboljsa_poteza, vrednost_najboljse)
        else:
            assert False, "minimax: nedefinirano stanje igre"