import tkinter    # za uporabniški vmesnik
import argparse   # za argumente iz ukazne vrstice
import logging    # za odpravljanje napak

# Privzeta minimax globina
MINIMAX_GLOBINA = 4

import logika
import clovek
import racunalnik
import minimax

# TODO velikost polja se mora spremeniti, če se spremeni velikost okna

# uvedemo parameter:
VELIKOST_IGRALNE_PLOSCE = 12


class Gui():
    # Vpeljemo konstante:
    VELIKOST_POLJA = 1
    SEZNAM_BARV = ['deep sky blue', 'yellow', 'snow4', 'lawn green', 'maroon1', 'navy']

    def __init__(self, master, globina):
        self.logika = None  # Tu bo spravljena logika igre, ko se bo igra dejansko začela
        self.igralec1 = None
        self.igralec2 = None

        # narišemo igralno okno
        self.okno = tkinter.Canvas(master)
        self.okno.grid(row=1, column=1)

        #ustvarimo label z opozorili
        self.opozorila = tkinter.Label(master, text="", font=("Comic Sans", 16))
        self.opozorila.grid(row=0, column=1, pady=0, padx=0)

        # ustvarimo okvir, v katerem bodo gumbi
        gumbi = tkinter.Frame(master)
        gumbi.grid(row=3, column=1)
        # nariše gumbe
        self.seznam_gumbov = []
        for i in range(len(Gui.SEZNAM_BARV)):
            gumb_v_nastajanju = tkinter.Button(gumbi, width=5 * Gui.VELIKOST_POLJA, height=2 * Gui.VELIKOST_POLJA,
                           text=Gui.SEZNAM_BARV[i],
                           background=Gui.SEZNAM_BARV[i], command=lambda i=i: self.barva_klik(i))
            gumb_v_nastajanju.pack(side=tkinter.LEFT, padx=10, pady=5)
            self.seznam_gumbov.append(gumb_v_nastajanju)

        # levo in desno postavimo label-a z vmesnim rezultatom
        levi_okvir = tkinter.Frame(master)#okvir v katem bosta levo ime in levi rezultat
        levi_okvir.grid(row=1, column=0, padx=20, sticky="S")
        self.leva_vrednost = tkinter.Label(levi_okvir, text="0", font=("Comic Sans", 16), borderwidth=20)
        self.leva_vrednost.pack(side=tkinter.BOTTOM)

        desni_okvir = tkinter.Frame(master) #okvir v katerem bosta desno ime in desni rezultat
        desni_okvir.grid(row=1, column=2, padx=20, sticky="S")
        self.desna_vrednost = tkinter.Label(desni_okvir, text="0", font=("Comic Sans", 16), borderwidth=20)
        self.desna_vrednost.pack(side=tkinter.BOTTOM)

        def omejitev_stevila_znakov(event):
            "funkcija dopušča vnos v Entry do dolžine 15, daljše nize pa skrajša na dožino 15"
            if len(self.ime_igralca1.get()) > 15:
                skrajsano_ime = self.ime_igralca1.get()[:15]
                self.ime_igralca1.delete(0, len(self.ime_igralca1.get()))
                self.ime_igralca1.insert(0, skrajsano_ime)
            elif len(self.ime_igralca2.get()) > 15:
                skrajsano_ime = self.ime_igralca2.get()[:15]
                self.ime_igralca2.delete(0, len(self.ime_igralca2.get()))
                self.ime_igralca2.insert(0, skrajsano_ime)

        # pod vmesnim rezultatom ustvarimo polje za vnos imen igralcev
        self.ime_igralca1 = tkinter.Entry(master, justify="center")
        self.ime_igralca1.insert(0, "Igralec 1")
        self.ime_igralca1.grid(row=2, column=0, padx=20, sticky="N")
        self.ime_igralca1.bind(sequence='<KeyRelease>', func=omejitev_stevila_znakov)

        self.ime_igralca2 = tkinter.Entry(master, justify="center")
        self.ime_igralca2.insert(0, "Igralec 2")
        self.ime_igralca2.grid(row=2, column=2, padx=20, sticky="N")
        self.ime_igralca2.bind(sequence='<KeyRelease>', func=omejitev_stevila_znakov)

        #  Nastavimo minimalno širino prvega in zadnjega stolpca.
        root.grid_columnconfigure(0, minsize=150)
        root.grid_columnconfigure(2, minsize=150)

        # okvir za igralno polje:
        self.plosca = tkinter.Frame(master)
        self.plosca.grid(row=1, column=1, rowspan=2)

        # nariše igralno polje
        # privzeto: zagnana igra je igra človek proti računalniku
        self.narisi_polje(clovek.Clovek(self), racunalnik.Racunalnik(self, minimax.Minimax(globina, VELIKOST_IGRALNE_PLOSCE)))

        # naredimo glavni menu:
        menu = tkinter.Menu(master)
        master.config(menu=menu)
        # in podmenu z izbiro vrste igre
        menu_igra = tkinter.Menu(menu, tearoff=0)
        menu.add_cascade(label="Nova igra", menu=menu_igra)
        menu_igra.add_command(label="Človek proti računalniku",
                              command=lambda: self.narisi_polje(clovek.Clovek(self),
                                                                racunalnik.Racunalnik(self, minimax.Minimax(globina, VELIKOST_IGRALNE_PLOSCE))))
        menu_igra.add_command(label="Človek proti človeku", command=lambda: self.narisi_polje(clovek.Clovek(self),
                                                                                              clovek.Clovek(self)))
        menu_igra.add_command(label="Računalnik proti računalniku",
                              command=lambda: self.narisi_polje(racunalnik.Racunalnik(self, minimax.Minimax(globina, VELIKOST_IGRALNE_PLOSCE)),
                                                                racunalnik.Racunalnik(self, minimax.Minimax(globina, VELIKOST_IGRALNE_PLOSCE))))
        # naredimo menu z gumbom razveljavi
        moznosti = tkinter.Menu(menu, tearoff=0)
        menu.add_cascade(label="Možnosti", menu=moznosti)
        moznosti.add_command(label="Razveljavi eno potezo", command=lambda: self.razveljavi_eno_potezo())
        moznosti.add_command(label="Razveljavi dve potezi", command=lambda: self.razveljavi_dve_potezi())

    # funkcija, ki po potezi popravi igralno ploščo
    def posodobi(self):
        #prilagodi izpise na zaslonu
        for vrstica in range(VELIKOST_IGRALNE_PLOSCE):
            for stolpec in range(VELIKOST_IGRALNE_PLOSCE):
                self.matrika_polj[vrstica][stolpec].config(bg=Gui.SEZNAM_BARV[self.matrika[vrstica][stolpec]])
        (levi_rezultat, desni_rezultat) = self.logika.get_rezultat()
        self.leva_vrednost.config(text=levi_rezultat)
        self.desna_vrednost.config(text=desni_rezultat)
        #prilagodimo izpis v opozorilni vrstici:
        if self.logika.stanje_igre() == logika.NI_KONEC:
            if self.logika.na_potezi == logika.IGRALEC1:
                self.opozorila.config(text="Na potezi je {}.".format(self.ime_igralca1.get()))
                self.leva_vrednost.config(font=("Comic Sans", 20, "bold"))
                self.desna_vrednost.config(font=("Comic Sans", 16))
            elif self.logika.na_potezi == logika.IGRALEC2:
                self.opozorila.config(text="Na potezi je {}.".format(self.ime_igralca2.get()))
                self.desna_vrednost.config(font=("Comic Sans", 20, "bold"))
                self.leva_vrednost.config(font=("Comic Sans", 16))
            else:
                assert False
            #  Vključimo/izključimo gumbe.
            for poteza in range(len(Gui.SEZNAM_BARV)):
                if poteza in self.logika.veljavne_poteze():
                    #  Gumb vključimo
                    self.seznam_gumbov[poteza].config(state="normal", background="{}".format(Gui.SEZNAM_BARV[poteza]))
                else:
                    #  Gumb izključimo
                    defaultbg = root.cget("bg")
                    self.seznam_gumbov[poteza].config(state="disabled", background=defaultbg)
        else:
            # Igre je konec, metoda naredi_potezo bo s klicanjem drugih metod končala igro.
            pass

    # Funkcija, ki ob začetku nove igre nariše novo igralno ploščo.
    def narisi_polje(self, igralec1, igralec2):
        self.prekini_igralce()
        self.logika = logika.Logika(VELIKOST_IGRALNE_PLOSCE)
        vrstice = VELIKOST_IGRALNE_PLOSCE
        stolpci = VELIKOST_IGRALNE_PLOSCE
        self.opozorila.config(text="Na potezi je {}.".format(self.ime_igralca1.get()))
        self.logika.narisi_polje()
        self.matrika_polj = [] #matrika kvadratov
        self.matrika = self.logika.get_polje()
        self.igralec1 = igralec1
        self.igralec2 = igralec2
        (levi_rezultat, desni_rezultat) = self.logika.get_rezultat()
        self.leva_vrednost.config(text=levi_rezultat)
        self.desna_vrednost.config(text=desni_rezultat)
        for vrstica in range(vrstice):
            trenutna_vrstica = [] # vrstica matrike matrika_polj
            vrstica_matrike = self.matrika[vrstica]  # vrstica matrike matrika
            for stolpec in range(stolpci):
                vrednost = vrstica_matrike[stolpec]
                polje = tkinter.Label(self.plosca, borderwidth=Gui.VELIKOST_POLJA,
                                      height=2 * Gui.VELIKOST_POLJA,
                                      width=4 * Gui.VELIKOST_POLJA,
                                      bg=Gui.SEZNAM_BARV[vrednost])
                polje.grid(row=vrstica, column=stolpec, padx=0.5, pady=0.5)
                trenutna_vrstica.append(polje)
            self.matrika_polj.append(trenutna_vrstica)

        for barva in range(len(Gui.SEZNAM_BARV)):
            if barva not in self.logika.veljavne_poteze():
                #  Gumb izključimo
                defaultbg = root.cget("bg")
                self.seznam_gumbov[barva].config(state="disabled", background=defaultbg)
            else:
                #  Gumb izključimo
                defaultbg = root.cget("bg")
                self.seznam_gumbov[barva].config(state="normal", background="{}".format(Gui.SEZNAM_BARV[barva]))
        self.igralec1.igraj()

    def barva_klik(self, indeks_barve):
        if self.logika.na_potezi == None:
            pass
        else:
            if self.logika.na_potezi == logika.IGRALEC1:
                self.igralec1.klik(indeks_barve)
            else:
                self.igralec2.klik(indeks_barve)

    def naredi_potezo(self, p):
        "Naredi potezo, če je ta veljavna."
        r = self.logika.naredi_potezo(p)
        if r is None:
            # Poteza ni bila veljavna, nič se ni spremenilo
            pass
        else:
            # Poteza je bila veljavna, narišemo jo na zaslon
            self.posodobi()
            # Ugotovimo, kako nadaljevati
            if r == logika.NI_KONEC:
                # Igra se nadaljuje
                if self.logika.na_potezi == logika.IGRALEC1:
                    self.igralec1.igraj()
                elif self.logika.na_potezi == logika.IGRALEC2:
                    self.igralec2.igraj()
                else:
                    assert False
            else:
                # Igre je konec, končaj.
                self.koncaj_igro(r)

    def koncaj_igro(self, zmagovalec):
        "Nastavi stanje igre na konec igre."
        if zmagovalec == logika.IGRALEC1:
            self.opozorila.config(text="Bravo {}! Zmaga je tvoja!".format(self.ime_igralca1.get()))
            self.leva_vrednost.config(font=("Comic Sans", 20, "bold"))
        elif zmagovalec == logika.IGRALEC2:
            self.opozorila.config(text="Bravo {}! Zmaga je tvoja!".format(self.ime_igralca2.get()))
            self.desna_vrednost.config(font=("Comic Sans", 20, "bold"))
        else:
            self.opozorila.config(text="Igre je konec, rezultat pa neodločen.")
            self.leva_vrednost.config(font=("Comic Sans", 20, "bold"))
            self.desna_vrednost.config(font=("Comic Sans", 20, "bold"))

    def prekini_igralce(self):
        "Igralcem sporoči, da nehajo razmišljati."
        logging.debug("prekinjam igralce")
        if self.igralec1:
            self.igralec1.prekini()
        if self.igralec2:
            self.igralec2.prekini()

    def zapri_okno(self, master):
        "Metoda se pokliče, ko  uporabnik zapre aplikacijo."
        # vporedna vlakna se morajo končati
        self.prekini_igralce()
        master.destroy()

############################################################################################

    def razveljavi_eno_potezo(self): #uporabno pri igri proti človeku
        (pozicija, na_potezi) = self.logika.razveljavi() #iz zgodovine dobimo zadnjo pozicijo in kdo je bil takrat na potezi
        self.matrika = pozicija
        self.posodobi()

    def razveljavi_dve_potezi(self): #uporabno pri igri proti računalniku
        self.razveljavi_eno_potezo()
        self.razveljavi_eno_potezo()

######################################################################
## Glavni program

# Glavnemu oknu rečemo "root" (koren), ker so grafični elementi
# organizirani v drevo, glavno okno pa je koren tega drevesa

# Ta pogojni stavek preveri, ali smo datoteko pognali kot glavni program in v tem primeru
# izvede kodo. (Načeloma bi lahko datoteko naložili z "import" iz kakšne druge in v tem
# primeru ne bi želeli pognati glavne kode. To je standardni idiom v Pythonu.)

if __name__ == "__main__":
    # Iz ukazne vrstice poberemo globino za minimax, uporabimo
    # modul argparse, glej https://docs.python.org/3.4/library/argparse.html

    # Opišemo argumente, ki jih sprejmemo iz ukazne vrstice
    parser = argparse.ArgumentParser(description="Igrica color flood")
    # Argument --globina n, s privzeto vrednostjo MINIMAX_GLOBINA
    parser.add_argument('--globina',
                        default=MINIMAX_GLOBINA,
                        type=int,
                        help='globina iskanja za minimax algoritem')
    # Argument --debug, ki vklopi sporočila o tem, kaj se dogaja
    parser.add_argument('--debug',
                        action='store_true',
                        help='vklopi sporočila o dogajanju')

    # Obdelamo argumente iz ukazne vrstice
    args = parser.parse_args()

    # Vklopimo sporočila, če je uporabnik podal --debug
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)

    # Naredimo glavno okno in nastavimo ime
    root = tkinter.Tk()
    root.title("Color Flood")

    # Naredimo objekt razreda Gui in ga spravimo v spremenljivko,
    # sicer bo Python mislil, da je objekt neuporabljen in ga bo pobrisal
    # iz pomnilnika.
    globina = args.globina
    aplikacija = Gui(root, globina)

    # Kontrolo prepustimo glavnemu oknu. Funkcija mainloop neha delovati, ko okno zapremo.
    root.mainloop()