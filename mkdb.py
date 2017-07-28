# https://docs.python.org/2/library/sqlite3.html
# https://www.sqlite.org/docs.html
# https://www.tutorialspoint.com/sqlite/index.htm

import sqlite3

def build_person(c):
    c.execute('''
        CREATE TABLE person(
            uuid INTEGER PRIMARY KEY AUTOINCREMENT,
            ccid TEXT,
            name TEXT
        );
    ''')

def build_class(c):
    c.execute('''
        CREATE TABLE class(
            cid     INTEGER PRIMARY KEY AUTOINCREMENT,
            name    text
        );
    ''')

def build_solution(c):
    c.execute('''
        CREATE TABLE solution(
            soid    INTEGER PRIMARY KEY AUTOINCREMENT
        );
    ''')

def build_assignment(c):
    c.execute('''
        CREATE TABLE assignment(
            aid     INTEGER PRIMARY KEY AUTOINCREMENT,
            name    TEXT
        );
    ''')

def build_source(c):
    c.execute('''
        CREATE TABLE source(
            scid        INTEGER PRIMARY KEY AUTOINCREMENT,
            filename    TEXT
        );
    ''')

def build_belongs_to(c):
    c.execute('''
        CREATE TABLE belongs_to(
            student INTEGER,
            class   INTEGER,
            FOREIGN KEY(student) REFERENCES person(uuid),
            FOREIGN KEY(class) REFERENCES class(cid)
        );
    ''')

def build_TAs_for(c):
    c.execute('''
        CREATE TABLE tas_for(
            ta      INTEGER,
            class   INTEGER,
            FOREIGN KEY(ta) REFERENCES person(uuid),
            FOREIGN KEY(class) REFERENCES class(cid)
        );
    ''')

def build_teaches(c):
    c.execute('''
        CREATE TABLE teaches(
            prof    INTEGER,
            class   INTEGER,
            FOREIGN KEY(prof) REFERENCES person(uuid),
            FOREIGN KEY(class) REFERENCES class(cid)
        );
    ''')

def build_submits(c):
    c.execute('''
        CREATE TABLE submits(
            student     INTEGER,
            solution    INTEGER,
            assignment  INTEGER,
            date        DATE,
            FOREIGN KEY(student) REFERENCES person(uuid),
            FOREIGN KEY(assignment) REFERENCES assignment(aid),
            FOREIGN KEY(solution) REFERENCES solution(soid)
        );
    ''')

def build_provides(c):
    c.execute('''
        CREATE TABLE provides(
            assignment  INTEGER,
            file        INTEGER,
            FOREIGN KEY(assignment) REFERENCES assignment(aid),
            FOREIGN KEY(file) REFERENCES source(scid)
        );
    ''')

def build_contains(c):
    c.execute('''
        CREATE TABLE contains(
            solution    INTEGER,
            file        INTEGER,
            FOREIGN KEY(solution) REFERENCES solution(soid),
            FOREIGN KEY(file) REFERENCES source(scid)
        );
    ''')

def build_database(name='database.db'):
    conn = sqlite3.connect(name)
    c = conn.cursor()

    # BUILD TABLES
    build_person(c)
    build_class(c)
    build_assignment(c)
    build_solution(c)
    build_source(c)
    build_belongs_to(c)
    build_TAs_for(c)
    build_teaches(c)
    build_submits(c)
    build_provides(c)
    build_contains(c)
    
    conn.commit()
    conn.close()

def clear_database(tables, name='database.db'):
    conn = sqlite3.connect(name)
    c = conn.cursor()

    for t in tables:
        try:
            c.execute("drop table {}".format(t))
        except:
            pass

    conn.commit()
    conn.close()

def pop_database(name='database.db'):
    conn = sqlite3.connect(name)
    c = conn.cursor()

    conn.execute("PRAGMA foreign_keys=on;")
    conn.commit()

    print("ATTEMPTING TO POPULATE DB WITH SIMPLE VALUES TO TEST.")
    c.execute("INSERT INTO person values(1, 's1', 'John Doe');")      # student1
    c.execute("INSERT INTO person values(2, 's2', 'Jane Doe');")      # student2
    c.execute("INSERT INTO person values(3, 't1', 'Joe Blow');")      # ta1
    c.execute("INSERT INTO person values(4, 't2', 'Jack Shmo');")      # ta2
    c.execute("INSERT INTO person values(5, 'p1', 'Joan Grow');")      # prof1
    
    c.execute("INSERT INTO class values(1, 'cmput0')")          # class1
    c.execute("INSERT INTO class values(2, 'cmput1')")          # class2

    c.execute("INSERT INTO belongs_to values(1, 1)")            # student1 in class1
    c.execute("INSERT INTO belongs_to values(2, 1)")            # student2 in class1
    c.execute("INSERT INTO belongs_to values(2, 2)")            # student2 in class2

    c.execute("INSERT INTO tas_for values(3, 1)")               # ta1 TAs class1
    c.execute("INSERT INTO tas_for values(4, 2)")               # ta2 TAs class2

    c.execute("INSERT INTO teaches values(5, 1)")               # prof1 teaches class1
    c.execute("INSERT INTO teaches values(5, 2)")               # prof1 teaches class2

    c.execute("INSERT INTO source values(1, 'base code')")      # source1 is base code
    c.execute("INSERT INTO source values(2, 'base code')")      # source2 is base code
    c.execute("INSERT INTO source values(3, 'f1')")             # source3 is submitted
    c.execute("INSERT INTO source values(4, 'f2')")             # source4 is submitted

    c.execute("INSERT INTO assignment values(1, 'asgn1')")      # assignment 11

    c.execute("INSERT INTO provides values(1, 1)")              # asgn1 provides source1
    c.execute("INSERT INTO provides values(1, 2)")              # asgn1 provides source2

    c.execute("INSERT INTO solution values(1)")                 # solution 1
    c.execute("INSERT INTO solution values(2)")                 # solution 2

    c.execute("INSERT INTO contains values(1, 1)")              # sol1 contains source1
    c.execute("INSERT INTO contains values(1, 2)")              # sol1 contains source2
    c.execute("INSERT INTO contains values(1, 3)")              # sol1 contains source3

    c.execute("INSERT INTO contains values(2, 1)")              # sol2 contains source1
    c.execute("INSERT INTO contains values(2, 2)")              # sol2 contains source2
    c.execute("INSERT INTO contains values(2, 4)")              # sol3 contains source3

    c.execute("INSERT INTO submits values(1, 1, 1, '2017-07-28')") # student1 submits sol1 for a1 on date
    c.execute("INSERT INTO submits values(2, 2, 1, '2017-07-29')") # student2 submits sol2 for a1 on date
    
    print("FINISHED POPULATING DATABASE WITH SIMPLE VALUES.")

    print("TESTING FOREIGN KEY CONSTRAINT.")
    try:
        c.execute("INSERT INTO belongs_to values(1, 9999)")
    except:
        print("ATTEMPT TO VIOLATE FOREIGN KEY CONSTRAINT FAILED.  TEST PASSED.")
        pass

    conn.commit()
    conn.close()

def main():
    tables = [  'person', 'class', 'solution', 'assignment', 'source',
                'belongs_to', 'tas_for', 'teaches', 'submits', 'provides', 'contains']
    try:
        build_database()
    except:
        clear_database(tables)
        build_database()
    pop_database()

if __name__ == "__main__":
    main()

