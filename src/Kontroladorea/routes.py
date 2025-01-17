
from flask import Flask, render_template, request, redirect, url_for, flash
from Eredua.Filma import Filma
from Eredua.Erabiltzailea import Erabiltzailea
from Eredua.Alokatu import Alokatu
from Eredua.api import api

app = Flask(__name__)

@app.route("/pelikulak")
def pelikulak_erakutsi():
    pelikulak = Filma().pelikulak_lortu()
    return render_template("pelikulak.html", pelikulak=pelikulak)

@app.route("/pelikulak/alokatu/<int:id_pelikula>", methods=["POST"])
def pelikula_alokatu(id_pelikula):
    Alokatu().pelikulak_alokatu(id_pelikula,Erabiltzailea().nan)
    return redirect("/pelikulak")

@app.route("/alokatuak")
def alokatuak_erakutsi():
    pelikulak = Alokatu().alokatuak_lortu(Erabiltzailea().nan)
    return render_template("alokatuak.html", pelikulak=pelikulak)

@app.route("/eskaerak")
def eskaera_egin(titulo,api_key):
    eskaerak = api().eskaera_egin(titulo,api_key)
    return render_template("eskaerak.html", eskaerak=eskaerak)

