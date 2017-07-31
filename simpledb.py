import sqlite3

def build(name="simple.db"):
    conn = sqlite3.connect(name)
    c = conn.cursor()

    c.execute('''
        CREATE TABLE metadata(
            uuid        INTEGER PRIMARY KEY AUTOINCREMENT,
            assignment  TEXT,
            date        TEXT,
            name        TEXT,
            unixid      TEXT,
            lecture     TEXT,
            instructor  TEXT,
            lab         TEXT,
            ta          TEXT
        )
    ''')
    
    conn.commit()
    conn.close()

def clear_db(name="simple.db"):
    conn = sqlite3.connect(name)
    c = conn.cursor()
    c.execute("DROP TABLE metadata")
    conn.commit()
    conn.close()

def pop_db(name="simple.db"):
    conn = sqlite3.connect(name)
    c = conn.cursor()
    values = [(None, "1", "2017, 29-07", "NAME1", "UID1", "LECTURE B1", "TEACHER1", "LAB SECT 1", "TA1"),
              (None, "1", "2017, 29-07", "NAME1", "UID1", "LECTURE B1", "TEACHER1", "LAB SECT 1", "TA1")
             ]
    c.executemany("INSERT INTO metadata VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", values)
    conn.commit()

def main():
    try:
        build()
    except:
        clear_db()
        build()
    pop_db()
    
main()
