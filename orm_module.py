import sqlite3

def execute_query(query):
    conn = sqlite3.connect("gimnazija.db")
    conn.execute(query)
    conn.commit()
    conn.close()

def execute_select_query(query):
    conn = sqlite3.connect("gimnazija.db")
    c = conn.cursor()
    c.execute(query)
    podaci = c.fetchall()
    c.close()
    conn.close()
    return podaci


def set_tables():
    conn = sqlite3.connect("gimnazija.db")
    
    conn.execute('''
    CREATE TABLE IF NOT EXISTS profesori(
        jmbg char(13) primary key,
        ime varchar(20) not null,
        prezime varchar(20) not null,
        predmet varchar(50) not null
    );
    ''')

    conn.execute('''
    CREATE TABLE IF NOT EXISTS odjeljenja(
        razred int not null,
        odjeljenje int not null,
        razredni_starjesina char(13) not null,
        primary key (razred, odjeljenje),
        foreign key (razredni_starjesina) references profesori(jmbg)
    );
    ''')

    conn.execute('''
    CREATE TABLE IF NOT EXISTS ucenici(
        jmbg char(13) primary key,
        ime varchar(20) not null,
        prezime varchar(20) not null,
        razred int not null,
        odjeljenje int not null,
        foreign key (razred, odjeljenje) references odjeljenja(razred, odjeljenje)
    );
    ''')

    conn.execute('''
    CREATE TABLE IF NOT EXISTS kabineti(
        broj int primary key,
        broj_mjesta int not null
    );
    ''')

    conn.close()

class Ucenik:
    def __init__(self, jmbg, ime, prezime, razred, odjeljenje):
        self.jmbg = jmbg
        self.ime = ime
        self.prezime = prezime
        self.razred = razred
        self.odjeljenje = odjeljenje
    
    def sacuvaj(self):
        execute_query(f"INSERT INTO ucenici (jmbg, ime, prezime, razred, odjeljenje) VALUES ('{self.jmbg}', '{self.ime}', '{self.prezime}', {self.razred}, {self.odjeljenje})")
    
    def sacuvaj_promjene(self):
        execute_query(f"UPDATE ucenici SET ime = '{self.ime}', prezime = '{self.prezime}', razred = {self.razred}, odjeljenje = {self.odjeljenje} WHERE jmbg = '{self.jmbg}'")

    def izbrisi(self):
        execute_query(f"DELETE FROM ucenici WHERE jmbg = '{self.jmbg}'")
    
    @staticmethod
    def uzmi(jmbg):
        podaci = execute_select_query(f"SELECT * FROM ucenici WHERE jmbg = '{jmbg}'")
        return Ucenik(podaci[0][0], podaci[0][1], podaci[0][2], podaci[0][3], podaci[0][4])
    
    @staticmethod
    def izbrisi_sve():
        execute_query("DELETE FROM ucenici")


class Odjeljenje:
    def __init__(self, razred, odjeljenje, razredni_starjesina):
        self.razred = razred
        self.odjeljenje = odjeljenje
        self.razredni_starjesina = razredni_starjesina
    
    def sacuvaj(self):
        execute_query(f"INSERT INTO odjeljenja (razred, odjeljenje, razredni_starjesina) VALUES ({self.razred}, {self.odjeljenje}, '{self.razredni_starjesina}')")
    
    def sacuvaj_promjene(self):
        execute_query(f"UPDATE odjeljenja SET razredni_starjesina = '{self.razredni_starjesina}' WHERE razred = {self.razred} AND odjeljenje = {self.odjeljenje}")

    def izbrisi(self):
        execute_query(f"DELETE FROM odjeljenja WHERE razred = {self.razred} AND odjeljenje = {self.odjeljenje}")
    
    @staticmethod
    def uzmi(razred, odjeljenje):
        podaci = execute_select_query(f"SELECT * FROM odjeljenja WHERE razred = {razred} AND odjeljenje = {odjeljenje}")
        return Odjeljenje(podaci[0][0], podaci[0][1], podaci[0][2])
    
    @staticmethod
    def izbrisi_sve():
        execute_query("DELETE FROM odjeljenja")


class Profesor:
    def __init__(self, jmbg, ime, prezime, predmet):
        self.jmbg = jmbg
        self.ime = ime
        self.prezime = prezime
        self.predmet = predmet
    
    def sacuvaj(self):
        execute_query(f"INSERT INTO profesori (jmbg, ime, prezime, predmet) VALUES ('{self.jmbg}', '{self.ime}', '{self.prezime}', '{self.predmet}')")
    
    def sacuvaj_promjene(self):
        execute_query(f"UPDATE profesori SET ime = '{self.ime}', prezime = '{self.prezime}', predmet = '{self.predmet}' WHERE jmbg = '{self.jmbg}'")
        
    def izbrisi(self):
        execute_query(f"DELETE FROM profesori WHERE jmbg = '{self.jmbg}'")
    
    @staticmethod
    def uzmi(jmbg):
        podaci = execute_select_query(f"SELECT * FROM profesori WHERE jmbg = '{jmbg}'")
        return Profesor(podaci[0][0], podaci[0][1], podaci[0][2], podaci[0][3])
    
    @staticmethod
    def izbrisi_sve():
        execute_query("DELETE FROM profesori")


class Kabinet:
    def __init__(self, broj, broj_mjesta):
        self.broj = broj
        self.broj_mjesta = broj_mjesta
    
    def sacuvaj(self):
        execute_query(f"INSERT INTO kabineti (broj, broj_mjesta) VALUES ({self.broj}, {self.broj_mjesta})")
    
    def sacuvaj_promjene(self):
        execute_query(f"UPDATE kabineti SET broj_mjesta = {self.broj_mjesta} WHERE broj = {self.broj_mjesta}")

    def izbrisi(self):
        execute_query(f"DELETE FROM kabineti WHERE broj = {self.broj}")
    
    @staticmethod
    def uzmi(broj):
        podaci = execute_select_query(f"SELECT * FROM kabineti WHERE broj = {broj}")
        return Kabinet(podaci[0][0], podaci[0][1])
    
    @staticmethod
    def izbrisi_sve():
        execute_query("DELETE FROM kabineti")