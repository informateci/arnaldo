import sqlite3
import time

def db():
    if not hasattr(db, "db"):
        db.db = sqlite3.connect('db.arnaldo')
        c = db.db.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS
                     quotes
                     (
                        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                        author,
                        quote,
                        date
                     )''')
        db.db.commit()
    
    return db.db

def add_quote(author, quote):
    db().execute('INSERT INTO quotes (author, quote, date) VALUES (?, ?, ?)',
                 (author, quote, time.time()))
    db().commit()

def random_quote():
    c = db().cursor()
    c.execute('SELECT * FROM quotes ORDER BY RANDOM() LIMIT 1')
    print c.fetchone()


if __name__ == '__main__':
    random_quote()
    
