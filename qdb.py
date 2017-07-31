# This script's purpose is to take a set of numbers associated with anonymised files
# returned by MOSS and match those numbers with the metadata associated with them.
# It will do this by matching the list of numbers against an sqlite database.

# https://docs.python.org/2/library/sqlite3.html
# https://www.sqlite.org/docs.html
# https://www.tutorialspoint.com/sqlite/index.htm
# https://stackoverflow.com/questions/22506153/how-to-rename-a-table-in-sql-with-join

import sqlite3

# MOSS returns pairs of files that are similar, each titled with a unique identifier.
# These IDs can be used to lookup the metadata for the files.
# pairs is expected to be [[ID1, ID2], [ID3, ID4], ... ] or some other iterable.

'''
            SELECT  
                person.name AS student,
                assignment.name AS assignment,
                class.name AS class,
                teacher.name AS prof,
                submits.date AS date,
                contains.file
            FROM person
            INNER JOIN submits ON person.uuid=submits.student
            INNER JOIN solution ON solution.soid=submits.solution
            INNER JOIN assignment ON submits.assignment=assignment.aid
            INNER JOIN assigns ON assigns.assignment=assignment.aid
            INNER JOIN person AS teacher ON teacher.uuid=assigns.prof
            INNER JOIN belongs_to ON person.uuid=belongs_to.student
            INNER JOIN class ON class.cid=belongs_to.class
            INNER JOIN contains ON contains.solution=solution.soid
            INNER JOIN source ON source.scid=contains.file
            WHERE class.name="cmput0" 
                AND assignment.aid=1
                AND (source.scid={} OR source.scid={})
        '''

def match(connection, pairs):
    results = []
    for pair in pairs:
        c = connection.cursor()
        c.execute('''
            SELECT
                source.filename,
                student.name,
                assignment.name,
                class.name,
                professor.name,
                submits.date
            FROM
                source,
                contains,
                solution,
                submits,
                person student,
                assignment,
                assigns,
                person professor,
                class, 
                belongs_to
            WHERE 
                (scid={} OR scid={}) AND
                source.scid==contains.file AND
                contains.solution==solution.soid AND
                solution.soid==submits.solution AND
                submits.student==student.uuid AND
                student.uuid==belongs_to.student AND
                belongs_to.class==class.cid AND
                submits.assignment==assignment.aid AND
                assignment.aid==assigns.assignment AND
                assigns.prof==professor.uuid AND
                assigns.class==class.cid
                  
        '''.format(pair[0], pair[1])
        )
        
        for row in c:
            print row

    for r in c:
        print r
    


def setup(name="database.db"):
    pairs = []                      # NB: This ought to be read from MOSS's output in the real world
    return sqlite3.connect(name), pairs

def main():
    db, pairs = setup()
    print "SIMPLE PAIR TEST."
    pairs = [[3, 4]]        # Source file 3 matches source file 4.  Student for file 4 in multiple lectures
    match(db, pairs)
    print "TESTING ACROSS LECTURE SECTIONS"
    pairs = [[3, 5]]        # Files 3 & 5 match.  Students are in separate lectures.
    match(db, pairs)
    print "LARGER TEST"
    pairs = [[3,4], [3, 5]] # Combined test.  files match across sections
    match(db, pairs)

    

main()
