######################################################################
## Igralec človek

class Clovek():
    def __init__(self, gui):
        self.gui = gui

    def igraj(self):
        # Na potezi je uporabnik. Čakamo, da bo kliknil na ploščo.
        # Ko se bo to zgodilo, nas bo Gui obvestil preko metode klik.
        pass

    def prekini(self):
        # Metoda, ki jo kliče gui, če je treba prekiniti razmišljanje.
        pass

    def klik(self, p):
        # Povlečemo potezo. Če ni veljavna, se ne zgodi nič.
        self.gui.naredi_potezo(p)
