import tkinter
import random

class Gui():
    # Vpeljemo konstante:
    VELIKOST_POLJA = 1
    SEZNAM_BARV = ['red', 'blue', 'black', 'yellow', 'green', 'white']
    VELIKOST_IGRALNE_PLOSCE = 12
    # Vpeljemo parametre:
    levi_rezultat = 0
    desni_rezultat = 0
    matrika = []

    def __init__(self, master):

        #narišemo igralno okno
        self.okno = tkinter.Canvas(master)
        self.okno.grid(row=0, column=1)

        #ustvarimo okvir v katerm bodo gumbi
        gumbi = tkinter.Frame(master)
        gumbi.grid(row=1, column=1)
        #nariše gumbe
        for barva in Gui.SEZNAM_BARV:
            tkinter.Button(gumbi, width=5*Gui.VELIKOST_POLJA, height=2*Gui.VELIKOST_POLJA,
                           background=barva, command=self.barva_klik(barva)).pack(side=tkinter.LEFT, padx=10, pady=5)

        #levo in desno postavimo label-a z umesnim rezultatom
        self.leva_vrednost = tkinter.Label(master, text=self.levi_rezultat).grid(row=0, column=0) #dodati fond
        self.desna_vrednost = tkinter.Label(master, text=self.desni_rezultat).grid(row=0, column=2)

        #okvir za igralno polje:
        self.plosca = tkinter.Frame(master)
        self.plosca.grid(row=0, column=1)

        #nariše igralno polje
        self.narisi_polje()

        #naredimo glevni menu:
        menu = tkinter.Menu(master)
        master.config(menu=menu)
        #in podmenu z izbiro vrste igre
        menu_igra = tkinter.Menu(menu)
        menu.add_cascade(label="Nova igra", menu=menu_igra)
        menu_igra.add_command(label="Proti računalniku",command=lambda: self.narisi_polje())#zaenkrat samo narišeta novo polje
        menu_igra.add_command(label="Proti človeku",command=lambda: self.narisi_polje())

    #funkcija, ki nastavi matriko z vrednostmi
    def set_matrika(self, matrika):
        self.matrika = matrika

    #funkcija, ki nam vrne trenutno matriko vrednosti
    def get_matrika (self):
        return self.matrika

    #funskcija, ki nastavi rezultate:
    def set_rezultat(self, levi_rezultat, desni_rezultat):
        self.levi_rezultat = levi_rezultat
        self.desni_rezultat = desni_rezultat

    #funkcija, ki nam vrne trenutni rezultat
    def get_rezultat(self):
        return (self.levi_rezultat, self.desni_rezultat)

    #funkcija, ki po potezi popravi igralno ploščo
    def posodobi(self):
        for vrstica in range(Gui.VELIKOST_IGRALNE_PLOSCE):
            for stolpec in  range(Gui.VELIKOST_IGRALNE_PLOSCE):
                self.matrika_polj[vrstica][stolpec].config(bg=Gui.SEZNAM_BARV[self.matrika[vrstica][stolpec]])
        self.leva_vrednost.config(text=self.levi_rezultat)
        self.desna_vrednost.config(text=self.desni_rezultat)

    #funkcija, ki ob začetku nove igre nariše novo igralno ploščo. Ustvarimo dve matriki: self.matrika je matrika vrednosti [0,5],
    #matrika_polj pa je matrika objektov (labelov):
    def narisi_polje(self):
        vrstice = Gui.VELIKOST_IGRALNE_PLOSCE
        stolpci = Gui.VELIKOST_IGRALNE_PLOSCE
        self.matrika_polj = []
        self.matrika = []
        self.levi_rezultat = 0
        self.desni_rezultat = 0
        for vrstica in range(vrstice):
            trenutna_vrstica = [] #vrstica matrike matrika_polj
            vrstica_matrike = []  #vrstica matrike matrika
            for stolpec in range(stolpci):
                vrednost = random.randint(0,5)
                polje = tkinter.Label(self.plosca, borderwidth=Gui.VELIKOST_POLJA, width=2*Gui.VELIKOST_POLJA,
                                      bg=Gui.SEZNAM_BARV[vrednost])
                polje.grid(row=vrstica, column=stolpec, padx=1, pady=1)
                vrstica_matrike.append(vrednost)
                trenutna_vrstica.append(polje)
            self.matrika_polj.append(trenutna_vrstica)
            self.matrika.append(vrstica_matrike)

    def barva_klik(self, barva):
        def pomozna():
            #TODO
            #print(barva)
        return pomozna

root = tkinter.Tk()
aplikacija = Gui(root)
root.mainloop()