from Eredua.Pelikula import Filma

class Bideokluba:
    __instance = None

    def __new__(cls): #Singleton
        if cls._instance is None:
            cls._instance = super().__new__(cls)  
        return cls._instance

    def Bideokluba(self):
        self.filmak = []
        self.erabiltzaileak = []

    def filmaGehitu(self, filma):
        self.filmak.append(filma)

    def erabiltzaileaGehitu(self, erabiltzailea):
        self.erabiltzaileak.append(erabiltzailea)

    def filmaAlokatu(self, filma, erabiltzailea):
        pass