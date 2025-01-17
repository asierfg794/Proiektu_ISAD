class Filma:
    def Filma(self, id, izena, deskribapena, puntuazioa, alokairuKop, iruzkinKop):
        self.id = id
        self.izena = izena
        self.deskribapena = deskribapena
        self.puntuazioa = puntuazioa
        self.alokairuKop = alokairuKop
        self.iruzkinKop = iruzkinKop

    def inf_lortu(self):
        return f"{self.id} - {self.izena} - {self.deskribapena} - {self.puntuazioa} - {self.alokairuKop} - {self.iruzkinKop}"
    
    