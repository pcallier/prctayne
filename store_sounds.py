import sqlite3

dbname='sounds.db'

def store(sound_path, name, attribute):
    conn = sqlite3.connect(dbname)
    c = conn.cursor()
    c.execute("INSERT INTO sounds VALUES (?, ?, ?)", (name, sound_path, attribute))
    conn.commit()
    conn.close()

def init_db():
    conn = sqlite3.connect(dbname)
    c = conn.cursor()
    c.execute('''CREATE TABLE sounds
    (name text, path text, attribute text)''')
    conn.commit()
    conn.close()

def get_all():
    conn = sqlite3.connect(dbname)
    c = conn.cursor()
    records = c.execute("SELECT * FROM sounds")
    records = list(records)
    conn.close()
    return records
