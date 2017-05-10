# FLOOD IT
Barbara Robba, Katarina Koderman
## Projektna naloga pri predmetu Programiranje 2

### Delovni načrt
* izdelava GUI: do 29. 3.
* logika igre: do 12. 4. 
* igra med dvema človekoma: do 12. 4.
* računalnik kot igralec: do 18. 4.
* testiranje in odprava napak: sproti

### Navodila za igranje

Igra 'Flood Wars' je igra za 2 igralca. Na začetku igre igralcu 1 pripada levi zgornji kot, 
igralcu 2 pa desni spodnji kot tabele, katere polja so (naključno) pobarvana s šestimi barvami. 
Igralec, ki je na potezi, s pritiskom na gumb izbere barvo, s katero želi pobarvati svoja polja
(pri tem ne sme izbrati barv, s katerima sta pobarvana levi zgornji in desni spodnji kot). 
Igra se konča, ko vsako polje pripada bodisi enemu bodisi drugemu igralcu, ali pa ko sta igralca 
naredila več potez, kot je polj. Cilj igre je zavzeti čimveč polj. 
Ob zagonu se začne igra človeka proti računalniku. Drug način igre lahko izberemo v menuju.
 
### Opis programa 

Program deluje s pomočjo več datotek:
* flood_it.py - glavni program, ki ga je potrebno zagnati, če želimo igrati igro.
* logika.py - nadzoruje potek igre, stanja igre, dogajanja na plošči...
* minimax.py - algoritem za računanje potez računalnika.
* racunalnik.py - vsebuje funkcije, ki jih potrebuje računalniški igralec.
* clovek.py - vsebuje funkcije za potek igre s človeškim igralcem.

V datoteki flood_it.py dopuščamo nekaj sprememb za prilagajanje igre:
* S spreminjanjem konstante VELIKOST_IGRALNE_PLOSCE spreminjamo velikost tabele, na kateri igramo.
  Smiselne vrednosti so med 5 in 20. Brez sprememb je velikost igralnega polja enaka 12×12. 
* Spreminjamo lahko globino delovanja minimaxa tako, da nastavimo konstanto MINIMAX_GLOBINA. 
  Vstavljena vrednost mora biti pozitivna in celoštevilska. Pri večjih vrednostih računalnik deluje počasneje. 
  Za dobro in zmerno hitro igranje računalnika priporočava globine med 3 in 7.
* S spreminjenjem seznama SEZNAM_BARV lahko spremenimo 6 barv, s katerimi igramo.
