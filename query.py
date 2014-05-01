#!/usr/bin/python

import sqlite3
conn = sqlite3.connect('picture_share.db')
c = conn.cursor()

print
print 'Print all users'
for row in c.execute('SELECT * FROM users'):
  print row

#print
#print "Print peter's password"
#t = ('peter@gmail.com',)
#c.execute('SELECT * FROM users WHERE email=?', t)
#print c.fetchone()[1]


user=('mgq', 'guanqunmao@me.com', 'MGQ', '123', 'true', 'Nothing')
#c.execute('INSERT INTO users VALUES (?,?,?,?,?,?)', user)


#name = ('guanqunmao@me.com',)
#c.execute('DELETE FROM users WHERE email=?', name)
#print c.fetchone()


#user = ('jin', 'mm')
#c.execute('INSERT INTO follows VALUES (?,?)', user)


for i in range(3):
    tt=(i+15, 'x', str(i)+'xxxxxxxx', '0', 'time')
    #c.execute('INSERT INTO tweets VALUES (?,?,?,?,?)', tt)


conn.commit()
