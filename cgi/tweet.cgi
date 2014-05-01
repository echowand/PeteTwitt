#!/usr/bin/python

def displayTweets(login):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    t = (login,)
    for row in c.execute('SELECT * FROM tweets WHERE login=?', t):
        row[0]
    conn.commit()
