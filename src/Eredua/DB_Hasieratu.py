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
                alokairuKopurua int,
                iruzkinKopurua int
            )
            """)
    
    c.execute("""
                CREATE TABLE IF NOT EXISTS alokairua(
                id_alokairua int primary key,
                nan varchar(9) ,
                id_pelikula int ,
                hasieraData date ,
                amaieraData date ,
                foreign key (nan) references erabiltzailea(nan),
                foreign key (id_pelikula) references pelikula(id_pelikula)
                unique (nan, id_pelikula, hasieraData)
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
      

    conn.commit()
    conn.close()