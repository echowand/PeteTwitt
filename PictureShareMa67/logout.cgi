#!/usr/bin/python

# Import the CGI, string, sys modules
import cgi, string, sys, os, re, random, sqlite3

import cgitb; cgitb.enable()  # for troubleshooting
import session;

# Define function to generate HTML form.

form = cgi.FieldStorage()
conn = sqlite3.connect('picture_share.db')
c = conn.cursor()
c.execute("DELETE FROM session WHERE user_id="+form['user_id'].value+";")
conn.commit()

print("Content-Type: text/html\n\n")
print """<html>
    <head>
    <script type="text/javascript">
    <!--
    function delayer(){
        window.location = "main.cgi"
    }
    -->
    </script>
    </head>
    <body onLoad="setTimeout('delayer()', 3000)">
    <p>You have securely log out. If the webpage does not redirect automatically, click <a href="login.cgi">here</a> to visit homepage.</p>

    </body>
    </html>
"""
