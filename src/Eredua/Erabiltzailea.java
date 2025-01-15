package Eredua;

public class Erabiltzailea{
    private String NAN;
    private String izena;
    private String abizena;
    private String pasahitza;
    private String rol;
    private boolean ezabatuta;

    public Erabiltzailea(String pNAN, String pIzena, String pAbizena, String pPasahitza, String pRol){
        this.NAN = pNAN;
        this.izena = pIzena;
        this.abizena = pAbizena;
        this.pasahitza = pPasahitza;
        this.rol = pRol;
        this.ezabatuta = false;
    }
}