#!/usr/bin/python

import sqlite3
conn = sqlite3.connect('picture_share.db')

c = conn.cursor()

# Turn on foreign key support
c.execute("PRAGMA foreign_keys = ON")

# Create users table, 
c.execute('''CREATE TABLE users
	     (login TEXT NOT NULL,
          email TEXT NOT NULL, 
          displayName TEXT NOT NULL,
          password TEXT NOT NULL,
          activated TEXT NOT NULL,
          description TEXT NOT NULL,
	      PRIMARY KEY(email, login))''')

# Create table avatars
c.execute('''CREATE TABLE avatars
             (login TEXT NOT NULL,
              path TEXT NOT NULL,
              FOREIGN KEY(login) REFERENCES users(login),
              PRIMARY KEY(path))''')

# Create pictures table
c.execute('''CREATE TABLE pictures
	      (picID INGEGER NOT NULL,
          login TEXT NOT NULL,
          path TEXT NOT NULL,
	      FOREIGN KEY(login) REFERENCES users(login),
	      PRIMARY KEY(path, picID))''')

# Create sessions table
c.execute('''CREATE TABLE sessions
	     (user TEXT NOT NULL,
	      session TEXT NOT NULL,
	      FOREIGN KEY(user) REFERENCES users(email),
	      PRIMARY KEY(session))''')

# Create follows table
c.execute('''CREATE TABLE follows
          (followerLogin TEXT NOT NULL,
           followingLogin TEXT NOT NULL,
           PRIMARY KEY(followerLogin, followingLogin)
          )''')


# Create tweets table
c.execute('''CREATE TABLE tweets
          (tweetID INTEGER NOT NULL,
           login TEXT NOT NULL,
           content TEXT NOT NULL,
           picID INTEGER NOT NULL,
           timeStamp TEXT NOT NULL,
           PRIMARY KEY(tweetID))''')
           




# Save the changes
conn.commit()

# Close the connection
conn.close()
