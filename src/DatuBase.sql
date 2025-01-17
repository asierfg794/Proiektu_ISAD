create table Erabiltzailea (
    NAN varchar(9) primary key,
    izena varchar(50),
    abizena varchar(50),
    pasahitza varchar(50),
    rol varchar(50),
    ezabatuta boolean
);

create table Film(
    id_pelikula int primary key,
    izena varchar(50),
    deskribapena varchar(500),
    alokairuKopurua int,
    iruzkinKopurua int,
);

create table Alokairua (
    id_alokairua int primary key,
    NAN varchar(9) primary key,
    id_pelikula int primary key,
    hasieraData date primary key,
    amaieraData date ,
    foreign key (NAN) references Erabiltzailea(NAN),
    foreign key (id_pelikula) references Film(id_pelikula)
);