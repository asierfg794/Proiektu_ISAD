package Eredua;

public class Balorazioa {
    private Erabiltzailea erabiltzailea;
    private Filma filma;
    private double puntuazioa;
    private String iruzkina;

    public Balorazioa(Erabiltzailea pErabiltzailea, Filma pFilma, double pPuntuazioa, String pIruzkin){
        this.erabiltzailea = pErabiltzailea;
        this.filma = pFilma;
        this.puntuazioa = pPuntuazioa;
        this.iruzkina = pIruzkin;
    }
}
