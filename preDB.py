#!/usr/bin/env python

# https://docs.python.org/2/library/sqlite3.html
import os, sys, sqlite3

class prepDB:
    conn=None
    arxivsql="arXivdb.sql"
    def __init__(self, dbname):
        self.open(dbname)

    def createTables(self):
        print "creating database",
        sql=open(self.arxivsql).readlines()
        for line in sql:
            self.conn.execute(line.strip())
            print ".",
        self.conn.commit()
        print "done"
    
    def open(self, dbname):
        dbexists = os.path.basename(dbname) in os.listdir(os.path.dirname(dbname))
        try:
            self.conn = sqlite3.connect(dbname)
            cur = self.conn.cursor()    
            cur.execute('SELECT SQLITE_VERSION()')
            data = cur.fetchone()
            print "SQLite version: %s" % data                
        except sqlite3.Error, e:
            print "Error %s:" % e.args[0]
        if not dbexists: self.createTables()
        
    def getPreprints(self):
        try:
            for row in con.execute("select * from preprints"):
                print row
        except sqlite3.OperationalError, e:
            if "no such table" in e: # table doesn't exist
                pass
    #code

if __name__ == "__main__":
    dbname="./arxiv.db"
    mydb=prepDB(dbname)
    #mydb.createTables()
    #print conn, c
    