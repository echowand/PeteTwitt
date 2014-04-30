#!/usr/bin/python

import sqlite3

conn = sqlite3.connect('picture_share.db')
c = conn.cursor()

c.execute('''CREATE TABLE users (user_id INTEGER PRIMARY KEY AUTOINCREMENT, username VARCHAR(255),password VARCHAR(255), active INT);''')
c.execute('''CREATE TABLE albums (id INTEGER PRIMARY KEY AUTOINCREMENT, album VARCHAR(255),user_id INT,public INT);''')
c.execute('''CREATE TABLE session (user_id INTEGER,session VARCHAR(1024));''')



conn.commit()
conn.close()
