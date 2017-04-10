import random

# uvedemo parametre:
IGRALEC_1 = "1"  # igralec, ki začne v zgornjem levem kotu
IGRALEC_2 = "2"  # igralec, ki začne v spodnjem desnem kotu
NEODLOCENO = "neodločeno"
NI_KONEC = "ni konec"
# VELIKOST_IGRALNE_PLOŠČE lahko spreminjamo v Gui-ju.


class Logika():
    def __init__(self, VELIKOST_IGRALNE_PLOSCE):
        self.plosca = None
        self.na_potezi = None
        self.zgodovina = []
        self.rezultat = (0, 0)
        self.VELIKOST_IGRALNE_PLOSCE = VELIKOST_IGRALNE_PLOSCE
        self.polja_igralec1 = [(0, 0)]
        self.polja_igralec2 = [(self.VELIKOST_IGRALNE_PLOSCE - 1, self.VELIKOST_IGRALNE_PLOSCE - 1)]


    def nasprotnik(self, igralec):
        """Vrni nasprotnika igralca."""
        if igralec == self.igralec1:
            print("1 -> 2")
            return self.igralec2
        elif igralec == self.igralec2:
            print('2 -> 1')
            return self.igralec1
        else:
            assert False, "neveljaven nasprotnik"

    # funkcija, ki ob začetku nove igre nariše novo igralno ploščo.
    # Ustvarimo matriko vrednosti self.matrika
    def narisi_polje(self, igralec1, igralec2):
        vrstice = self.VELIKOST_IGRALNE_PLOSCE
        stolpci = self.VELIKOST_IGRALNE_PLOSCE
        self.zgodovina = []
        self.plosca = []
        self.levi_rezultat = 0
        self.desni_rezultat = 0
        self.igralec1 = igralec1
        self.igralec2 = igralec2
        for vrstica in range(vrstice):
            vrstica_matrike = []  # vrstica matrike matrika
            for stolpec in range(stolpci):
                vrednost = random.randint(0, 5)
                vrstica_matrike.append(vrednost)
            self.plosca.append(vrstica_matrike)
        self.skeniraj_matriko(self.plosca[0][0], igralec1)
        self.skeniraj_matriko(self.plosca[self.VELIKOST_IGRALNE_PLOSCE - 1][self.VELIKOST_IGRALNE_PLOSCE - 1], igralec2)
        self.na_potezi = igralec1
        self.shrani_pozicijo() #shrani pozicijo v zgodovino


    def get_polje(self):
        '''Vrne matriko polja.'''
        return self.plosca

    def shrani_pozicijo(self):
        '''Shrani trenutno pozicijo, da se bomo lahko kasneje vrnili vanjo
           z metodo razveljavi.'''
        p = [] #naredimo kopijo matrike, sicer zgodovina vsebuje samo kazalce na isto matriko
        for vrstica in range(self.VELIKOST_IGRALNE_PLOSCE):
            p.append(self.plosca[vrstica][:])
        self.zgodovina.append((p, self.na_potezi, self.polja_igralec1, self.polja_igralec2))

    def razveljavi(self):
        """Razveljavi potezo in se vrni v prejšnje stanje."""
        if len(self.zgodovina) < 1: #ko pridemo do začetnega stanja, funkcija razveljavi ne dela ničesar
            return (self.plosca, self.na_potezi)
        (self.plosca, self.na_potezi, self.polja_igralec1, self.polja_igralec2) = self.zgodovina.pop()#nastavimo vrednosti iz zgodovine
        self.izracunaj_rezultat()
        return (self.plosca, self.na_potezi)

    def veljavne_poteze(self):
        """Vrni seznam veljavnih potez."""
        barva_1 = self.plosca[0][0]
        barva_2 = self.plosca[self.VELIKOST_IGRALNE_PLOSCE - 1][self.VELIKOST_IGRALNE_PLOSCE - 1]
        vse_poteze = [0, 1, 2, 3, 4, 5]
        vse_poteze.remove(barva_1)
        if barva_1 != barva_2: #s tem se izognemo napaki, če imata igralca na začetku enako barvo
            vse_poteze.remove(barva_2)
        return vse_poteze

    def get_rezultat(self):
        '''Vrne vmesni rezultat.'''
        return self.rezultat

    def izracunaj_rezultat(self):
        self.rezultat = (len(self.polja_igralec1), len(self.polja_igralec2))

    def naredi_potezo(self, izbrana_barva, igralec):
        '''Povleci potezo p, ne naredi nič, če je neveljavna.
           Vrne stanje_igre() po potezi ali None, ce je poteza neveljavna.'''
        if izbrana_barva not in self.veljavne_poteze():
            print("Izberi drugo barvo!")
        else:
            self.shrani_pozicijo() #shranimo staro pozicijo v zgodovino
            self.spremeni_matriko(izbrana_barva)
            self.izracunaj_rezultat()
            if self.stanje_igre() == NI_KONEC:
                #Igre ni konec, na potezi je nasprotnik.
                self.na_potezi = self.nasprotnik(igralec)
            else:
                self.na_potezi = None

    def spremeni_matriko(self, p):
        '''Vrne stanje igre po potezi.'''
        igralec = self.na_potezi
        if igralec == IGRALEC_1:
            for (vrstica, stolpec) in self.polja_igralec1:
                self.plosca[vrstica][stolpec] = p
        else:
            for (vrstica, stolpec) in self.polja_igralec2:
                self.plosca[vrstica][stolpec] = p
        self.skeniraj_matriko(p, igralec)

    def skeniraj_matriko(self, p, igralec):
        '''Pregleda matriko in jo glede na potezo in igralca spremeni.'''
        if igralec == IGRALEC_1:
            polje = (0, 0)
            self.polja_igralec1 = self.preglej_sosednja_polja(polje, p, [])
        else:
            polje = (self.VELIKOST_IGRALNE_PLOSCE - 1, self.VELIKOST_IGRALNE_PLOSCE - 1)
            self.polja_igralec2 = self.preglej_sosednja_polja(polje, p, [])

    def preglej_sosednja_polja(self, polje, p, polja):
        '''Pregleda sosednja polja, če so iste barve kot poteza. Če se barva ujema, polje dodajo k poljem igralca, ki je bil na potezi.'''
        (i, j) = polje
        if self.plosca[i][j] == p and polje not in polja:
            polja.append(polje)
            #desno
            if j < self.VELIKOST_IGRALNE_PLOSCE - 1:
                self.preglej_sosednja_polja((i, j + 1), p, polja)
            #dol
            if i < self.VELIKOST_IGRALNE_PLOSCE - 1:
                self.preglej_sosednja_polja((i + 1, j), p, polja)
            #levo
            if j > 0:
                self.preglej_sosednja_polja((i, j - 1), p, polja)
            #gor
            if i > 0:
                self.preglej_sosednja_polja((i - 1, j), p, polja)
        return polja

    def stanje_igre(self):
        '''Ugotovi, kakšno je trenutno stanje igre. Vrne:
            - igralec1, če je igre konec in je zmagal igralec1,
            - igralec2, če je igre konec in je zmagal igralec2,
            - neodločeno, če je igre konec in imata igralca enak rezulat,
            - NI_KONEC, če igre še ni konec.'''
        rezultat_igr1 = self.rezultat[0]
        rezultat_igr2 = self.rezultat[1]
        if rezultat_igr1 + rezultat_igr2 == self.VELIKOST_IGRALNE_PLOSCE * self.VELIKOST_IGRALNE_PLOSCE:
            if rezultat_igr1 > rezultat_igr2:
                return IGRALEC_1
            elif rezultat_igr1 < rezultat_igr2:
                return IGRALEC_2
            else:
                return NEODLOCENO
        return NI_KONEC


