import tkinter
import random

# TODO velikost polja se mora spremeniti, če se spremeni velikost okna

VELIKOST_IGRALNE_PLOSCE = 12

class Gui():
    # Vpeljemo konstante:
    VELIKOST_POLJA = 1
    SEZNAM_BARV = ['deep sky blue', 'yellow', 'chocolate1', 'lawn green', 'maroon1', 'navy']

    # Vpeljemo parametre:
    levi_rezultat = 0
    desni_rezultat = 0
    matrika = []

    def __init__(self, master):
        #ustvarimo objekt
        self.logika = Logika()

        # narišemo igralno okno
        self.okno = tkinter.Canvas(master)
        self.okno.grid(row=0, column=1)

        # ustvarimo okvir, v katerem bodo gumbi
        gumbi = tkinter.Frame(master)
        gumbi.grid(row=1, column=1)
        # nariše gumbe
        for barva in Gui.SEZNAM_BARV:
            tkinter.Button(gumbi, width=5 * Gui.VELIKOST_POLJA, height=2 * Gui.VELIKOST_POLJA,
                           background=barva, command=self.barva_klik(barva)).pack(side=tkinter.LEFT, padx=10, pady=5)

        # levo in desno postavimo label-a z vmesnim rezultatom
        self.leva_vrednost = tkinter.Label(master, text=self.levi_rezultat, font=("Comic Sans", 16)).grid(row=0, column=0, padx=20)
        self.desna_vrednost = tkinter.Label(master, text=self.desni_rezultat, font=("Comic Sans", 16)).grid(row=0, column=2, padx=20)

        # okvir za igralno polje:
        self.plosca = tkinter.Frame(master)
        self.plosca.grid(row=0, column=1)

        # nariše igralno polje
        self.narisi_polje()

        # naredimo glavni menu:
        menu = tkinter.Menu(master)
        master.config(menu=menu)
        # in podmenu z izbiro vrste igre
        menu_igra = tkinter.Menu(menu, tearoff=0)
        menu.add_cascade(label="Nova igra", menu=menu_igra)
        menu_igra.add_command(label="Proti računalniku", command=lambda: self.narisi_polje())#zaenkrat samo narišeta novo polje
        menu_igra.add_command(label="Proti človeku", command=lambda: self.narisi_polje())

    # funkcija, ki nastavi matriko z vrednostmi
    def set_matrika(self, matrika):
        self.matrika = matrika

    # funkcija, ki nam vrne trenutno matriko vrednosti
    def get_matrika(self):
        return self.matrika

    # funkcija, ki nastavi rezultate:
    def set_rezultat(self, levi_rezultat, desni_rezultat):
        self.levi_rezultat = levi_rezultat
        self.desni_rezultat = desni_rezultat

    # funkcija, ki nam vrne trenutni rezultat
    def get_rezultat(self):
        return (self.levi_rezultat, self.desni_rezultat)

    # funkcija, ki po potezi popravi igralno ploščo
    def posodobi(self):
        for vrstica in range(VELIKOST_IGRALNE_PLOSCE):
            for stolpec in range(VELIKOST_IGRALNE_PLOSCE):
                self.matrika_polj[vrstica][stolpec].config(bg=Gui.SEZNAM_BARV[self.matrika[vrstica][stolpec]])
        self.leva_vrednost.config(text=self.levi_rezultat)
        self.desna_vrednost.config(text=self.desni_rezultat)

    # funkcija, ki ob začetku nove igre nariše novo igralno ploščo.
    # Ustvarimo dve matriki:
        # self.matrika je matrika vrednosti [0,5],
        # matrika_polj pa je matrika objektov (labelov):
    def narisi_polje(self):
        vrstice = VELIKOST_IGRALNE_PLOSCE
        stolpci = VELIKOST_IGRALNE_PLOSCE
        self.logika.narisi_polje()
        self.matrika_polj = [] #matrika kvadratov
        self.matrika = self.logika.get_polje()
        self.levi_rezultat = self.logika.get_rezultat()[0]
        self.desni_rezultat = self.logika.get_rezultat()[1]
        for vrstica in range(vrstice):
            trenutna_vrstica = [] # vrstica matrike matrika_polj
            vrstica_matrike = self.matrika[vrstica]  # vrstica matrike matrika
            for stolpec in range(stolpci):
                vrednost = vrstica_matrike[stolpec]
                polje = tkinter.Label(self.plosca, borderwidth=Gui.VELIKOST_POLJA, width=2 * Gui.VELIKOST_POLJA,
                                      bg=Gui.SEZNAM_BARV[vrednost])
                polje.grid(row=vrstica, column=stolpec, padx=0.5, pady=0.5)
                trenutna_vrstica.append(polje)
            self.matrika_polj.append(trenutna_vrstica)

    def barva_klik(self, barva):
        def pomozna():
            #TODO
            print(barva)
        return pomozna

#igralec, ki začne v zgornjem levem kotu
IGRALEC_1 = "1"
#igralec, ki začne v spodnjem desnem kotu
IGRALEC_2 = "2"
NEODLOCENO = "neodločeno"
NI_KONEC = "ni konec"

def nasprotnik(igralec):
    """Vrni nasprotnika od igralca."""
    if igralec == IGRALEC_1:
        return IGRALEC_2
    elif igralec == IGRALEC_2:
        return IGRALEC_1
    else:
        assert False, "neveljaven nasprotnik"

class Logika():
    def __init__(self):
        self.plosca = None
        self.na_potezi = IGRALEC_1
        self.zgodovina = []
        self.rezultat = (0, 0)

    # funkcija, ki ob začetku nove igre nariše novo igralno ploščo.
    # Ustvarimo matriko vrednosti self.matrika
    def narisi_polje(self):
        vrstice = VELIKOST_IGRALNE_PLOSCE
        stolpci = VELIKOST_IGRALNE_PLOSCE
        self.plosca = []
        self.levi_rezultat = 0
        self.desni_rezultat = 0
        for vrstica in range(vrstice):
            vrstica_matrike = []  # vrstica matrike matrika
            for stolpec in range(stolpci):
                vrednost = random.randint(0, 5)
                vrstica_matrike.append(vrednost)
            self.plosca.append(vrstica_matrike)

    def get_polje(self):
        '''Vrne matriko polja.'''
        return self.plosca

    def shrani_pozicijo(self):
        '''Shrani trenutno pozicijo, da se bomo lahko kasneje vrnili vanjo
           z metodo razveljavi.'''
        p = self.plosca
        self.zgodovina.append((p, self.na_potezi))

    def razveljavi(self):
        """Razveljavi potezo in se vrni v prejšnje stanje."""
        (self.plosca, self.na_potezi) = self.zgodovina.pop()

    def veljavne_poteze(self):
        """Vrni seznam veljavnih potez."""
        barva_1 = self.plosca[0][0]
        barva_2 = self.plosca[VELIKOST_IGRALNE_PLOSCE][VELIKOST_IGRALNE_PLOSCE]
        mozne_poteze = [0, 1, 2, 3, 4, 5].remove(barva_1, barva_2)
        return mozne_poteze

    def get_rezultat(self):
        '''Vrne vmesni rezultat.'''
        return self.rezultat

    def naredi_potezo(self, p):
        """Povleci potezo p, ne naredi nič, če je neveljavna.
           Vrne stanje_igre() po potezi ali None, ce je poteza neveljavna."""
        izbrana_barva = p
        if izbrana_barva not in self.veljavne_poteze():
            print("Izberi drugo barvo!")
        else:
            pass
            #
            #
            # self.shrani_pozicijo()
            # self.plosca[i][j] = self.na_potezi
            # (zmagovalec, trojka) = self.stanje_igre()
            # if zmagovalec == NI_KONEC:
            #     # Igre ni konec, zdaj je na potezi nasprotnik
            #     self.na_potezi = nasprotnik(self.na_potezi)
            # else:
            #     # Igre je konec
            #     self.na_potezi = None
            # return (zmagovalec, trojka)


root = tkinter.Tk()
root.title("Color Flood")
aplikacija = Gui(root)
root.mainloop()