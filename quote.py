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
    r = c.fetchone()
    return r[0], r[1]

def search_quote(pattern):
    pattern = '%' + pattern.lower() + '%'
    c = db().cursor()
    c.execute('SELECT * FROM quotes WHERE LOWER(author) LIKE ?', (pattern,))
    r = c.fetchone()
    
    if r is None:
        return None
    else:
        return r[0], r[1]
    
if __name__ == '__main__':
    random_quote()
    
