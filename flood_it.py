import tkinter

class Gui():
    # Velikost polja
    VELIKOST_POLJA = 1
    SEZNAM_BARV = ['red', 'blue', 'black', 'yellow', 'green', 'white']

    def __init__(self, master):
        #igralna plošča
        self.okno = tkinter.Canvas(master)
        self.okno.pack(fill=tkinter.BOTH, expand=1)
        #ustvarimo okvir v katerm bodo gumbi
        gumbi = tkinter.Frame(master)
        gumbi.pack()
        #nariše gumbe
        for barva in Gui.SEZNAM_BARV:
            tkinter.Button(gumbi, width=5*Gui.VELIKOST_POLJA, height=2*Gui.VELIKOST_POLJA,
                           background=barva, command=self.barva_klik(barva)).pack(side=tkinter.LEFT, padx=10, pady=5)


        #nariše igralno polje
        self.narisi_polje()

    def narisi_polje(self):
        #TODO
        pass

    def barva_klik(self, barva):
        def pomozna():
            #TODO
            print(barva)
        return pomozna

root = tkinter.Tk()
aplikacija = Gui(root)
root.mainloop()