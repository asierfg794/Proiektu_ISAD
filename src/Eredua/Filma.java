package Eredua;

public class Filma {
    private int id;
    private String izena;
    private String deskribapena;
    private double puntuazioa;
    private int alokairuKop;
    private int iruzkinKop;
    
    public Filma(String pIzena, String pDeskribapena){
        this.id = 0; //ponerle un id distinto a cada film
        this.izena = pIzena;
        this.deskribapena = pDeskribapena;
        this.puntuazioa = 0;
        this.alokairuKop = 0;
        this.iruzkinKop = 0;
    }
}
