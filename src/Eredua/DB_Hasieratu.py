import sqlite3
import os.path
from werkzeug.security import generate_password_hash
import json

def init_db():

    fitx = os.path.dirname(__file__)
    db_path = os.path.join(fitx, "..", "datubase.db")

    #if not os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS erabiltzailea")
    c.execute("DROP TABLE IF EXISTS pelikula")
    c.execute("DROP TABLE IF EXISTS alokairua")
    c.execute("""
            CREATE TABLE IF NOT EXISTS erabiltzailea(
                nan varchar(9) PRIMARY KEY,
                izena varchar(50),
                abizena varchar(50),
                pasahitza varchar(50),
                rol boolean,
                onartu boolean,
                onartuID varchar(9)
            )
            """)
    
    c.execute("""
                CREATE TABLE IF NOT EXISTS pelikula(
                id_pelikula int primary key,
                izena varchar(50),
                deskribapena varchar(500),
                puntuazioa int,
                alokairuKopurua int,
                iruzkinKopurua int
            )
            """)
    
    c.execute("""
                CREATE TABLE IF NOT EXISTS alokairua(
                id_alokairua INTEGER primary key autoincrement,
                nan varchar(9) ,
                id_pelikula int ,
                hasieraData date ,
                amaieraData date ,
                foreign key (nan) references erabiltzailea(nan),
                foreign key (id_pelikula) references pelikula(id_pelikula)
                unique (nan, id_pelikula, hasieraData)
            )
            """)
    
    c.execute("""
                CREATE TABLE IF NOT EXISTS balorazioa(
                id_pelikula int,
                nan varchar(9) ,
                puntuazioa int,
                iruzkina varchar(500),
                primary key (id_pelikula, nan),
                foreign key (id_pelikula) references pelikula(id_pelikula),
                foreign key (nan) references erabiltzailea(nan),
                unique (id_pelikula, nan),
                check (puntuazioa >= 0 and puntuazioa <= 10)
            )
            """)
    
    json_path = os.path.join(fitx,"..","..", "jsons","erabiltzaileak.json")
    with open(json_path, 'r') as f:
        erabiltzaileak = json.load(f)['erabiltzaileak']

    for user in erabiltzaileak:
        db_password = user['pasahitza']
        hashed = generate_password_hash(db_password)
        db_password = hashed
        c.execute(f"""INSERT OR REPLACE INTO erabiltzailea VALUES ('{user['nan']}','{user['izena']}', '{user['abizena']}', '{db_password}','{user['rol']}',{user['onartu']}, '{user['onartuID']}')""")
        conn.commit()
      
    json_path = os.path.join(fitx,"..","..", "jsons","pelikulak.json")
    with open(json_path, 'r') as f:
        pelikulak = json.load(f)['pelikulak']

    for pelikula in pelikulak:
        c.execute(f"""INSERT OR REPLACE INTO pelikula VALUES ('{pelikula['id_pelikula']}','{pelikula['izena']}', '{pelikula['deskribapena']}', '{pelikula['puntuazioa']}','{pelikula['alokairuKopurua']}', '{pelikula['iruzkinKopurua']}')""")
        conn.commit()

    conn.commit()
    conn.close()