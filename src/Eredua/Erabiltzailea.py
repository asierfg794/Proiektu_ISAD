

class Erabiltzailea:
    def __init__(self, nan, izena, abizena, pasahitza,):
        self.nan = nan
        self.izena = izena
        self.abizena = abizena
        self.pasahitza = pasahitza
        self.rol = False #Erabiltzailea (True=Admin)
        self.onartu = False
        self.onartuID = None

    