#########################################################################
#                                                                       #
#                          Minimax posodobljen                          #
#                                                                       #
#########################################################################

import logging
import logika
# from flood_it import VELIKOST_IGRALNE_PLOSCE
VELIKOST_IGRALNE_PLOSCE = 12

## Algoritem minimax

class Minimax():
    # Algoritem minimax predstavimo z objektom, ki hrani stanje igre in algoritma.

    def __init__(self, globina, velikost, zgodovina):
        self.globina = globina  # Do katere globine iščemo.
        self.prekinitev = False  # Ali moramo končati?
        self.jaz = None  # Katerega igralca igramo (podatek dobimo kasneje).
        self.poteza = None  # Sem napišemo potezo, ko jo najdemo.
        self.logika = None
        self.koncno_stanje = None
        self.zgodovina = zgodovina

    def prekini(self):
        """Metoda, ki jo pokliče GUI, če je treba nehati razmišljati, ker
           je uporabnik zaprl okno ali izbral novo igro."""
        self.prekinitev = True

    def izracunaj_potezo(self, logika, zgodovina):
        """Izračunaj potezo za trenutno stanje dane igre."""
        # To metodo pokličemo iz vzporednega vlakna.
        self.logika = logika
        self.prekinitev = False  # Glavno vlakno bo to nastavilo na True, če moramo nehati.
        self.jaz = self.logika.na_potezi
        self.poteza = None  # Sem napišemo potezo, ko jo najdemo.
        self.zgodovina = zgodovina

        # Poženemo minimax
        (poteza, vrednost) = self.minimax(self.globina, True, zgodovina)
        self.jaz = None
        self.logika = None
        self.zgodovina = None
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

    def minimax(self, globina, maksimiziramo, zgodovina):
        """Glavna metoda minimax. Vrne tuple najboljša poteza, vrednost te poteze.
        Če je igra prekinjena, vrne (None, 0).
        Če je igre konec, vrne (None, vrednost pozicije)."""
        if self.prekinitev:
            # Sporočili so nam, da moramo prekiniti.
            logging.debug("Minimax prekinja, globina = {0}".format(globina))
            return (None, 0)

        zmagovalec = self.logika.stanje_igre()
        if zmagovalec in (logika.IGRALEC1, logika.IGRALEC2, logika.NEODLOCENO):
            # Igre je konec, vrnemo njeno vrednost.
            if zmagovalec == self.jaz:
                return (None, Minimax.ZMAGA - (len(self.logika.zgodovina) / self.globina))
            elif zmagovalec == self.logika.nasprotnik(self.jaz):
                return (None, Minimax.ZMAGA + (len(self.logika.zgodovina) / self.globina))
            else:
                return (None, 0)

        elif zmagovalec == logika.NI_KONEC:
            # Igre ni konec
            if globina == 0:
                self.koncno_stanje = self.logika.zgodovina[-1]
                print("dolžina zgodovine = {}".format(len(self.zgodovina)))

                # Naslednjih 6 vrstic ne rabimo. Če jih ni, program teče nekaj potez dlje.
                # if self.koncno_stanje in self.logika.zgodovina[:-1]:
                #     print("Končno stanje je bilo narejeno v zadnjih {} potezah.".format(self.globina))
                #     if maksimiziramo:
                #         return (None, Minimax.NESKONCNO)
                #     else:
                #         return (None, -Minimax.NESKONCNO)

                if self.koncno_stanje in self.zgodovina:
                    print("Končno stanje je bilo narejeno že prej.")
                    if maksimiziramo:
                        return (None, Minimax.NESKONCNO)
                    else:
                        return (None, -Minimax.NESKONCNO)

                return (None, self.vrednost_pozicije())
            else:
                # Naredimo eno stopnjo minimax:
                if maksimiziramo:
                    # Maksimiziramo
                    najboljsa_poteza = (None, -Minimax.NESKONCNO - 1)
                    for p in self.logika.veljavne_poteze():
                        self.logika.naredi_potezo(p)
                        vrednost = self.minimax(globina-1, False, zgodovina)[1]
                        self.logika.razveljavi()

                        if vrednost > najboljsa_poteza[1]:
                            najboljsa_poteza = (p, vrednost)

                else:
                    # Minimiziramo
                    najboljsa_poteza = (None, Minimax.NESKONCNO + 1)
                    for p in self.logika.veljavne_poteze():
                        self.logika.naredi_potezo(p)
                        vrednost = self.minimax(globina-1, True, zgodovina)[1]
                        self.logika.razveljavi()

                        if vrednost < najboljsa_poteza[1]:
                            najboljsa_poteza = (p, vrednost)

                assert (najboljsa_poteza[0] is not None), "minimax: izračunana poteza je None"
                return najboljsa_poteza
        else:
            assert False, "minimax: nedefinirano stanje igre"