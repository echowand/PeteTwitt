#!/usr/bin/python

# Import the CGI, string, sys modules
import cgi, string, sys, os, re, random
import cgitb; cgitb.enable()  # for troubleshooting
import sqlite3
import session
import getpass
import smtplib
import admin

from email.mime.text import MIMEText


#Get Databasedir
#MYLOGIN="maog"
#print "Content-Type: text/html\n\n"

MYLOGIN=getpass.getuser()
portNum = "7111"
# print MYLOGIN
if MYLOGIN == "jin75":
    portNum = "61111"


host="http://data.cs.purdue.edu:"+portNum+"/PeteTwitt"
DATABASE="/homes/"+MYLOGIN+"/PeteTwitt/picture_share.db"
IMAGEPATH="/homes/"+MYLOGIN+"/PeteTwitt/images"
HOMEPATH="/homes/"+MYLOGIN+"/PeteTwitt"


def search_user(form):
    print_html_content_type()
    jump = """
    <meta http-equiv="refresh" content="0; url=login.cgi?action=Search&user={user}&session={session}" />
    """
    # print(jump.format(user=form["user"].value, session=form["session"].value))
    generate_search(form)
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()

    user=(form["user"].value)
    c.execute('SELECT * FROM users');
    rows = c.fetchall()
    conn.close()
    user=form["user"].value
    # html = "<h3>" + user +"</h3>" 
    # print(html)
    flag = 0
    for row in rows:
        if user in row[2]:
            flag = 1
            html = "<h3>"
            html += row[2]
            html += " "+"@"+row[0]+"</h3>"
            print(html)
    # if flag == 0:
    #     print(jump.format(user=form["user"].value, session=form["session"].value))