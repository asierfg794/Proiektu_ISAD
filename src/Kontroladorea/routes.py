
from flask import Flask, render_template, request, redirect, url_for, flash, session

from ..Eredua.Balorazioa import Balorazioa
from ..Eredua.Pelikula import Pelikula
from ..Eredua.Erabiltzailea import Erabiltzailea
from ..Eredua.Alokatu import Alokatu
from ..Eredua.api import api
from ..Eredua.DB_Hasieratu import init_db
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from ..Eredua.Konexioa import Konexioa
from datetime import datetime

app = Flask(__name__, template_folder='../Bista')
app.secret_key = 'secret_key'

init_db()

db = Konexioa()

@app.route("/")
def index():
    return render_template("login.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    nan = request.form['nan']
    password = request.form['password']

    user = db.select("SELECT * FROM erabiltzailea WHERE nan = ?", (nan,))
    if len(user) == 0:
        flash("Erabiltzailea ez da existitzen1!")
        return redirect('/login')
    
    if user[0][5] == 0:
        flash("Ez da onartu zure kontua oraindik. Itxaron mesedez!")
        return redirect('/login')
    if user and check_password_hash(user[0][3], password):  
        session["nan"] = user[0][0]  
        session["is_admin"] = bool(user[0][4]) 
        return redirect('/pelikulak')
    else:
        flash("Erabiltzailea ez da existitzen!")

    return redirect('/login')

@app.route('/logout')
def logout():
    session.clear()
    flash("Sesioa itxi duzu.")
    return redirect('/login')

@app.route("/erregistratu", methods=["GET", "POST"])
def erregistratu():
    if request.method == 'GET':
        return render_template('erregistratu.html')
    nan = request.form['nan']
    name = request.form['name']
    surname = request.form['surname']
    password = request.form['password']
    confirm_password = request.form['confirm_password']

    if password != confirm_password:
        flash("Pasahitzak ez dira berdinak!")
        return redirect('/erregistratu')

    hashed_password = generate_password_hash(password)
    try:
        db.insert(
            """
            INSERT INTO erabiltzailea (nan, izena, abizena, pasahitza, rol, onartu, onartuID)
            VALUES (?, ?, ?, ?, ?, ?,?)
            """,
            (nan, name, surname, hashed_password, False, False, "")
        )
        flash("Erabiltzailea erregistratu da!")
        return redirect('/')
    except Exception as e:
        flash(f"Errorea: {str(e)}")
        return redirect('/erregistratu')


@app.route("/admin/ezabErabiltzaile", methods=["GET", "POST"])
def delete_user():
    
    if "nan" not in session or not session.get("is_admin", False):
        return redirect(url_for("login"))

    if request.method == "POST":
        nan_to_delete = request.form.get("nan")

        user = db.select("SELECT * FROM erabiltzailea WHERE nan = ?", (nan_to_delete,))
        if not user:
            return render_template("ezabErabiltzaile.html", error="Erabiltzailea ez da aurkitu.")

        if user[0][4]:
            return render_template("ezabErabiltzaile.html", error="Ezin dira administradoreak ezabatu.")

        rows_deleted = db.delete("DELETE FROM erabiltzailea WHERE nan = ?", (nan_to_delete,))
        if rows_deleted > 0:
            return render_template("ezabErabiltzaile.html", message="Erabiltzailea ezabatu da.")
        else:
            return render_template("ezabErabiltzaile.html", error="Ezin izan da ezabatu.")

    return render_template("ezabErabiltzaile.html")


@app.route('/datuakAldatu', methods=['GET', 'POST'])
def update_user():
    if 'nan' not in session:
        return redirect('/login')  
    
    if session.get('is_admin', False) is False:
        if request.method == 'POST':
            izena = request.form['izena']
            abizena = request.form['abizena']
            pasahitza = request.form['pasahitza']
            hashed_pass= generate_password_hash(pasahitza)
            
            db.update("""
                UPDATE erabiltzailea 
                SET izena = ?, abizena = ?, pasahitza = ? 
                WHERE nan = ?
            """, (izena, abizena, hashed_pass, session['nan']))
            
            return flash("Datuak eguneratu dira.")
        
        return render_template('datuakAldErab.html') 
    
    elif session.get('is_admin', False):
        if request.method == 'POST':
            nan = request.form['nan']
            izena = request.form['izena']
            abizena = request.form['abizena']
            pasahitza = request.form['pasahitza']
            hashed_pass= generate_password_hash(pasahitza)
            
            usuario = db.select("SELECT * FROM erabiltzailea WHERE nan = ?", (nan,))
            if not usuario or usuario[0][4]==1:
                return flash("")

            db.update("""
                UPDATE erabiltzailea 
                SET izena = ?, abizena = ?, pasahitza = ? 
                WHERE nan = ?
            """, (izena, abizena, hashed_pass, nan))
            
            return flash(f" {nan} Nan-a duen erabiltzailearen datuak eguneratu dira.")
        
        return render_template('datuakAldAdmin.html')

@app.route('/eskaerak')
def ver_solicitudes():
    if 'nan' not in session or not session.get('is_admin', False):
        return redirect('/login')
    
    usuarios_pendientes = db.select("SELECT * FROM erabiltzailea WHERE onartu = FALSE")
    
    return render_template('erabiltzaileEsk.html', usuarios=usuarios_pendientes)

@app.route('/eskaerak/<nan>', methods=['POST'])
def aceptar_usuario(nan):
    if 'nan' not in session or not session.get('is_admin', False):
        return redirect('/login')
    
    db.update("""
        UPDATE erabiltzailea
        SET onartu = TRUE, onartuID = ?
        WHERE nan = ?
    """, (session["nan"] , nan))
    
    flash(f"Erabiltzailea {nan} onartu da.")
    return redirect('/eskaerak')


@app.route("/pelikulak")
def pelikulak_erakutsi():
    pelikulak = Pelikula().pelikulak_lortu()
    return render_template("pelikulak.html", pelikulak=pelikulak)

@app.route("/pelikulak/iruzkinak/<int:id_pelikula>", methods=["GET"])
def pelikula_iruzkinak(id_pelikula):
    pelikula = Pelikula().pelikula_lortu(id_pelikula)
    iruzkinak = Balorazioa().iruzkinak_lortu(id_pelikula)
    return render_template("iruzkinak.html", pelikula=pelikula, balorazioak=iruzkinak)

@app.route("/pelikulak/iruzkinak/<int:id_pelikula>/baloratu", methods=["GET","POST"])
def baloratu(id_pelikula):
    #if request.method == "GET":
    if request.method == "POST":
        puntuazioa = request.form["puntuazioa"]
        iruzkina = request.form["iruzkina"]
        Balorazioa().balorazioa_gorde(id_pelikula, session["nan"], puntuazioa, iruzkina)
        return redirect(f"/pelikulak/iruzkinak/{id_pelikula}")
    pelikula = Pelikula().pelikula_lortu(id_pelikula)
    return render_template("baloratu.html", pelikula=pelikula)

@app.route("/pelikulak/alokatu/<int:id_pelikula>", methods=["POST"])
def pelikula_alokatu(id_pelikula):
    Alokatu().pelikulak_alokatu(id_pelikula,session["nan"])
    return redirect("/pelikulak")

@app.route("/alokatuak")
def alokatuak_erakutsi():
    pelikulak = Alokatu().pelikula_alokatuak_lortu(session["nan"])
    pelikulak = [list(pelikula) for pelikula in pelikulak]
    for pelikula in pelikulak:
        pelikula[2] = datetime.strptime(pelikula[2], '%Y-%m-%d %H:%M:%S.%f')
    return render_template("alokatuak.html", pelikulak=pelikulak, datetime=datetime)

@app.route('/eskaerak', methods=['GET'])
def listar_solicitudes():
    # Verificar si el usuario está logueado y es administrador
    if 'nan' not in session or not session.get('is_admin', False):
        return redirect('/login')
    
    # Obtener todas las solicitudes pendientes
    solicitudes = db.select("SELECT * FROM eskaerak WHERE estado = 'pendiente'")
    
    # Renderizar la página HTML con las solicitudes
    return render_template("eskaerak.html", solicitudes=solicitudes)


@app.route('/eskaera/aceptar/<int:id>', methods=['POST'])
def aceptar_solicitud(id):
    # Verificar si el usuario es administrador
    if 'nan' not in session or not session.get('is_admin', False):
        return redirect('/login')
    
    # Obtener la película solicitada
    solicitud = db.select("SELECT * FROM eskaerak WHERE id = ?", (id,))
    if solicitud:
        # Insertar la película en el catálogo de películas
        pelicula = solicitud[0]
        db.insert("""
            INSERT INTO pelikula (id_pelikula, izena, deskribapena, puntuazioa, alokairuKopurua, iruzkinKopurua)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (pelicula['id'], pelicula['izena'], pelicula['deskribapena'], pelicula['puntuazioa'], 
              pelicula['alokairuKopurua'], pelicula['iruzkinKopurua']))
        
        # Marcar la solicitud como aceptada
        db.update("UPDATE eskaerak SET estado = 'aceptada' WHERE id = ?", (id,))
        flash("Película aceptada y añadida al catálogo.")
    else:
        flash("La solicitud no fue encontrada.")
    
    return redirect('/eskaerak')


@app.route('/eskaera/rechazar/<int:id>', methods=['POST'])
def rechazar_solicitud(id):
    # Verificar si el usuario es administrador
    if 'nan' not in session or not session.get('is_admin', False):
        return redirect('/login')
    
    # Eliminar la solicitud o marcarla como rechazada
    db.update("UPDATE eskaerak SET estado = 'rechazada' WHERE id = ?", (id,))
    flash("La solicitud ha sido rechazada.")
    
    return redirect('/eskaerak')


if __name__ == "__main__":
    app.run(debug=True)