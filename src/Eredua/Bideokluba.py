from Filma import Filma

class Bideokluba:
    def Bideokluba(self):
        self.filmak = []
        self.erabiltzaileak = []

    def filmaGehitu(self, bideoa):
        self.filmak.append(bideoa)

    def erabiltzaileaGehitu(self, bazkidea):
        self.erabiltzaileak.append(bazkidea)