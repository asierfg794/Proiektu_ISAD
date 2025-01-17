from Filma import Filma

class Balorazioa:
    def Balorazioa(self, erabiltzailea, filma, puntuazioa, iruzkina):
        self.erabiltzailea = erabiltzailea
        self.filma = filma
        self.puntuazioa = puntuazioa
        self.iruzkina = iruzkina

    def inf_lortu(self):
        return f"{self.erabiltzailea} - {self.filma} - {self.puntuazioa} - {self.iruzkina}"