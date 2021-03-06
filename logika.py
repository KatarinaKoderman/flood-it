
#########################################################################
#                                                                       #
#                                Logika igre                            #
#                                                                       #
#########################################################################

import random

# Uvedemo parametre:
IGRALEC1 = "IGRALEC1"  # igralec, ki začne v zgornjem levem kotu
IGRALEC2 = "IGRALEC2"  # igralec, ki začne v spodnjem desnem kotu
NEODLOCENO = "neodločeno"
NI_KONEC = "ni konec"

# VELIKOST_IGRALNE_PLOŠČE lahko spreminjamo v Gui-ju v datoteki flood_it.py


class Logika():
    def __init__(self, velikost):
        self.plosca = None
        self.na_potezi = None
        self.zgodovina = []
        self.velikost = velikost
        self.polja_igralec1 = [(0, 0)]
        self.polja_igralec2 = [(self.velikost - 1, self.velikost - 1)]
        self.stevec_potez = 0  # Število potez je omejeno na število polj.

    def nasprotnik(self, igralec):
        """Vrne nasprotnika igralca."""
        if igralec == IGRALEC1:
            return IGRALEC2
        elif igralec == IGRALEC2:
            return IGRALEC1
        else:
            assert False, "neveljaven nasprotnik"

    def narisi_polje(self):
        """Ob začetku nove igre nariše novo igralno ploščo."""
        # Ustvarimo matriko self.plosca z vrednostmi barv
        vrstice = self.velikost
        stolpci = self.velikost
        self.zgodovina = []
        self.plosca = []
        for vrstica in range(vrstice):
            vrstica_plosce = []
            for stolpec in range(stolpci):
                vrednosti = []
                for i in range(6):
                    vrednosti.append(i)
                if vrstica > 0:
                    vrednosti.remove(self.plosca[vrstica - 1][stolpec])
                if len(vrstica_plosce) > 1:
                    vrednost_na_levi = vrstica_plosce[-1]
                    if stolpec > 0 and vrednost_na_levi in vrednosti:
                        vrednosti.remove(vrednost_na_levi)
                vrednost = random.choice(vrednosti)
                vrstica_plosce.append(vrednost)
            self.plosca.append(vrstica_plosce)
        self.skeniraj_plosco(self.plosca[0][0], IGRALEC1)
        self.skeniraj_plosco(self.plosca[self.velikost - 1][self.velikost - 1], IGRALEC2)
        self.na_potezi = IGRALEC1
        self.shrani_pozicijo()  # Pozicijo shranimo v zgodovino.

    def get_polje(self):
        """Vrne matriko igralne plošče."""
        return self.plosca

    def shrani_pozicijo(self):
        """Shrani trenutno pozicijo, da se bomo lahko kasneje vrnili nanjo z metodo razveljavi."""
        # Naredimo kopijo matrike, sicer zgodovina vsebuje samo kazalce na isto matriko:
        p = []
        for vrstica in range(self.velikost):
            p.append(self.plosca[vrstica][:])

        self.zgodovina.append((p, self.na_potezi, self.polja_igralec1, self.polja_igralec2))

    def razveljavi(self):
        """Razveljavi potezo in se vrni v prejšnje stanje."""
        if len(self.zgodovina) < 1:  # Ko pridemo do začetnega stanja, funkcija razveljavi ne naredi ničesar.
            return (self.plosca, self.na_potezi)
        # Nastavimo vrednosti iz zgodovine:
        self.stevec_potez -= 1
        (self.plosca, self.na_potezi, self.polja_igralec1, self.polja_igralec2) = self.zgodovina.pop()
        return (self.plosca, self.na_potezi)

    def kopija(self):
        """Ustvari kopijo trenutnega stanja."""
        k = Logika(self.velikost)
        k.plosca = [self.plosca[i][:] for i in range(self.velikost)]
        k.na_potezi = self.na_potezi
        k.polja_igralec1 = self.polja_igralec1
        k.polja_igralec2 = self.polja_igralec2
        return k

    def veljavne_poteze(self):
        """Vrne seznam veljavnih potez."""
        barva_1 = self.plosca[0][0]
        barva_2 = self.plosca[self.velikost - 1][self.velikost - 1]
        vse_poteze = [0, 1, 2, 3, 4, 5]
        vse_poteze.remove(barva_1)
        if barva_1 != barva_2:  # S tem se izognemo napaki, če imata igralca na začetku enako barvo.
            vse_poteze.remove(barva_2)
        return vse_poteze

    def get_rezultat(self):
        """Vrne vmesni rezultat."""
        return (len(self.polja_igralec1), len(self.polja_igralec2))

    def naredi_potezo(self, izbrana_barva):
        """Povleče potezo p in vrne stanje_igre() po potezi.
            Če je poteza neveljavna, ne naredi nič in vrne None."""
        if izbrana_barva not in self.veljavne_poteze():
            return None  # neveljavna poteza
        else:
            self.shrani_pozicijo()  # Staro pozicijo shranimo v zgodovino.
            self.spremeni_matriko(izbrana_barva)
            self.stevec_potez += 1
            r = self.stanje_igre()
            if r == NI_KONEC:
                # Igre ni konec, na potezi je nasprotnik.
                self.na_potezi = self.nasprotnik(self.na_potezi)
            else:
                self.na_potezi = None
            return r

    def spremeni_matriko(self, p):
        """Nastavi stanje igre na stanje po potezi."""
        igralec = self.na_potezi
        if igralec == IGRALEC1:
            for (vrstica, stolpec) in self.polja_igralec1:
                self.plosca[vrstica][stolpec] = p
        elif igralec == IGRALEC2:
            for (vrstica, stolpec) in self.polja_igralec2:
                self.plosca[vrstica][stolpec] = p
        else:
            assert False
        self.skeniraj_plosco(p, igralec)

    def skeniraj_plosco(self, p, igralec):
        """Pregleda matriko in jo glede na potezo in igralca spremeni."""
        if igralec == IGRALEC1:
            polje = (0, 0)
            self.polja_igralec1 = self.preglej_sosednja_polja(polje, p, [])
        elif igralec == IGRALEC2:
            polje = (self.velikost - 1, self.velikost - 1)
            self.polja_igralec2 = self.preglej_sosednja_polja(polje, p, [])
        else:
            assert False

    def preglej_sosednja_polja(self, polje, p, polja):
        """Pregleda sosednja polja, če so iste barve kot poteza.
            Če se barva ujema, polje dodajo k poljem igralca, ki je bil na potezi."""
        (i, j) = polje
        if self.plosca[i][j] == p and polje not in polja:
            polja.append(polje)
            # desno
            if j < self.velikost - 1:
                self.preglej_sosednja_polja((i, j + 1), p, polja)
            # dol
            if i < self.velikost - 1:
                self.preglej_sosednja_polja((i + 1, j), p, polja)
            # levo
            if j > 0:
                self.preglej_sosednja_polja((i, j - 1), p, polja)
            # gor
            if i > 0:
                self.preglej_sosednja_polja((i - 1, j), p, polja)
        return polja

    def stanje_igre(self):
        """Ugotovi, kakšno je trenutno stanje igre. Vrne:
            - igralec1, če je igre konec in je zmagal igralec1,
            - igralec2, če je igre konec in je zmagal igralec2,
            - neodločeno, če je igre konec in imata igralca enak rezulat,
            - NI_KONEC, če igre še ni konec."""
        (rezultat_igr1, rezultat_igr2) = self.get_rezultat()
        if rezultat_igr1 + rezultat_igr2 == self.velikost * self.velikost \
                or self.stevec_potez >= self.velikost ** 2:
            if rezultat_igr1 > rezultat_igr2:
                return IGRALEC1
            elif rezultat_igr1 < rezultat_igr2:
                return IGRALEC2
            else:
                return NEODLOCENO
        return NI_KONEC
