import sqlite3
import os.path

def init_db():

    fitx = os.path.dirname(__file__)
    db_path = os.path.join(fitx, "..", "datubase.db")

    if not os.path.exists(db_path):
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute("""
                CREATE TABLE IF NOT EXISTS erabiltzailea(
                    nan varchar(9) PRIMARY KEY,
                    izena varchar(50),
                    abizena varchar(50),
                    pasahitza varchar(50),
                    rol boolean,
                    ezabatua boolean
                )
                """)
        
        c.execute("""
                    CREATE TABLE IF NOT EXISTS film(
                    id_pelikula int primary key,
                    izena varchar(50),
                    deskribapena varchar(500),
                    alokairuKopurua int,
                    iruzkinKopurua int,
                )
                """)
        
        c.execute("""
                    CREATE TABLE IF NOT EXISTS alokairua(
                    id_alokairua int primary key,
                    nan varchar(9) primary key,
                    id_pelikula int primary key,
                    hasieraData date primary key,
                    amaieraData date ,
                    foreign key (nan) references erabiltzailea(nan),
                    foreign key (id_pelikula) references film(id_pelikula)
                )
                """)
        
        conn.commit()
        conn.close()