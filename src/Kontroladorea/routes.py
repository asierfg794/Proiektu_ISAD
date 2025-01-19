
from flask import Flask, render_template, request, redirect, url_for, flash, session
from ..Eredua.Pelikula import Pelikula
from ..Eredua.Erabiltzailea import Erabiltzailea
from ..Eredua.Alokatu import Alokatu
from ..Eredua.api import api
from ..Eredua.DB_Hasieratu import init_db
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from ..Eredua.Konexioa import Konexioa

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

    # Obtener datos del formulario
    nan = request.form['nan']
    password = request.form['password']
    """
    # Consultar la base de datos para obtener el usuario
    user = db.select(
        "SELECT nan, pasahitza FROM erabiltzailea WHERE nan = ? AND ezabatua = 0",
        (nan,)
    )
    """

    user = db.select("SELECT * FROM erabiltzailea WHERE nan = ?", (nan,))
    if user[0][5] == 0:
        flash("Ez da onartu zure kontua oraindik. Itxaron mesedez!")
        return redirect('/login')
    if user and check_password_hash(user[0][3], password):  # Assuming password is at index 3
        session["nan"] = user[0][0]  # Save NAN in session
        session["is_admin"] = bool(user[0][4])  # Save role (True if admin)
        return redirect('/pelikulak')
    else:
        flash("User not found!")
    """
    if user:
        # Verificar la contraseña (hasheada en el registro)
        stored_password = user[0][1]
        if check_password_hash(stored_password, password):
            # Iniciar sesión: guardar usuario en la sesión
            session['user'] = nan
            flash("Login successful!")
            return redirect('/pelikulak')  # Cambia esta ruta según tu página principal
        else:
            flash("Invalid password!")
    
    else:
        flash("User not found!")
    """

    return redirect('/login')

# Ruta para cerrar sesión
@app.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out.")
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
        flash("Passwords do not match!")
        return redirect('/erregistratu')

    hashed_password = generate_password_hash(password)
    try:
        db.insert(
            """
            INSERT INTO erabiltzailea (nan, izena, abizena, pasahitza, rol, ezabatua)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (nan, name, surname, hashed_password, False, False)
        )
        flash("User registered successfully!")
        return redirect('/')
    except Exception as e:
        flash(f"Error during registration: {str(e)}")
        return redirect('/erregistratu')


@app.route("/admin/ezabErabiltzaile", methods=["GET", "POST"])
def delete_user():
    # Check if the user is logged in and is an administrator
    if "nan" not in session or not session.get("is_admin", False):
        return redirect(url_for("login"))

    if request.method == "POST":
        nan_to_delete = request.form.get("nan")

        # Check if the NAN exists in the database
        user = db.select("SELECT * FROM erabiltzailea WHERE nan = ?", (nan_to_delete,))
        if not user:
            return render_template("ezabErabiltzaile.html", error="User not found.")

        # Ensure the user to delete is not an administrator
        if user[0][4]:  # Assuming 'rol' is at index 4 in the table
            return render_template("ezabErabiltzaile.html", error="Cannot delete an administrator.")

        # Delete the user
        rows_deleted = db.delete("DELETE FROM erabiltzailea WHERE nan = ?", (nan_to_delete,))
        if rows_deleted > 0:
            return render_template("ezabErabiltzaile.html", message="User deleted successfully.")
        else:
            return render_template("ezabErabiltzaile.html", error="Failed to delete user.")

    # Render the deletion form
    return render_template("ezabErabiltzaile.html")


@app.route('/datuakAldatu', methods=['GET', 'POST'])
def update_user():
    # Verifica si el usuario está logueado
    if 'nan' not in session:
        return redirect('/login')  # Redirige al login si no está logueado
    
    # Usuario normal: No necesita introducir su NAN (ya lo tiene en sesión)
    if session.get('is_admin', False) is False:
        if request.method == 'POST':
            izena = request.form['izena']
            abizena = request.form['abizena']
            pasahitza = request.form['pasahitza']
            hashed_pass= generate_password_hash(pasahitza)
            
            # Actualiza datos en la base de datos
            db.update("""
                UPDATE erabiltzailea 
                SET izena = ?, abizena = ?, pasahitza = ? 
                WHERE nan = ?
            """, (izena, abizena, hashed_pass, session['nan']))
            
            return "Tus datos han sido actualizados correctamente."
        
        return render_template('datuakAldErab.html')  # Página para usuarios normales
    
    # Administrador: Necesita introducir el NAN de quien quiere actualizar
    elif session.get('is_admin', False):
        if request.method == 'POST':
            nan = request.form['nan']
            izena = request.form['izena']
            abizena = request.form['abizena']
            pasahitza = request.form['pasahitza']
            hashed_pass= generate_password_hash(pasahitza)
            
            # Asegúrate de que no se puedan editar otros administradores
            usuario = db.select("SELECT * FROM erabiltzailea WHERE nan = ?", (nan,))
            if not usuario or usuario[0][4]==1:  # usuario[0][4] = rol (True = admin)
                return "No puedes editar administradores."
            
            # Actualiza datos en la base de datos
            db.update("""
                UPDATE erabiltzailea 
                SET izena = ?, abizena = ?, pasahitza = ? 
                WHERE nan = ?
            """, (izena, abizena, hashed_pass, nan))
            
            return f"Los datos del usuario con NAN {nan} han sido actualizados correctamente."
        
        return render_template('datuakAldAdmin.html')

@app.route('/eskaerak')
def ver_solicitudes():
    # Verificar si el usuario está logueado y es administrador
    if 'nan' not in session or not session.get('is_admin', False):
        return redirect('/login')
    
    # Obtener todos los usuarios pendientes de aceptación (onartu = False)
    usuarios_pendientes = db.select("SELECT * FROM erabiltzailea WHERE onartu = FALSE")
    
    return render_template('erabiltzaileEsk.html', usuarios=usuarios_pendientes)

@app.route('/eskaerak/<nan>', methods=['POST'])
def aceptar_usuario(nan):
    # Verificar si el usuario está logueado y es administrador
    if 'nan' not in session or not session.get('is_admin', False):
        return redirect('/login')
    
    # Cambiar el valor de 'onartu' a True
    db.update("""
        UPDATE erabiltzailea
        SET onartu = TRUE, onartuID = ?
        WHERE nan = ?
    """, (session["nan"] , nan))
    
    flash(f"El usuario con NAN {nan} ha sido aceptado.")
    return redirect('/eskaerak')


@app.route("/pelikulak")
def pelikulak_erakutsi():
    pelikulak = Pelikula().pelikulak_lortu()
    return render_template("pelikulak.html", pelikulak=pelikulak)

@app.route("/pelikulak/alokatu/<int:id_pelikula>", methods=["POST"])
def pelikula_alokatu(id_pelikula):
    Alokatu().pelikulak_alokatu(id_pelikula,session["nan"])
    return redirect("/pelikulak")

@app.route("/alokatuak")
def alokatuak_erakutsi():
    pelikulak = Alokatu().pelikula_alokatuak_lortu(session["nan"])
    return render_template("alokatuak.html", pelikulak=pelikulak)

@app.route("/eskaerak")
def eskaera_egin(titulo,api_key):
    eskaerak = api().eskaera_egin(titulo,api_key)
    return render_template("eskaerak.html", eskaerak=eskaerak)

if __name__ == "__main__":
    app.run(debug=True)