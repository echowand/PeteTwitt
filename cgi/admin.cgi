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

def display_admin_options(user, session):
    html="""
        <H1> Picture Share Admin Options</H1>
        <ul>
        <li> <a href="admin.cgi?action=new-album&user={user}&session={session}">Create new album</a>
        <li> <a href="admin.cgi?action=upload&user={user}&session={session}">Upload Picture</a>
        <li> <a href="admin.cgi?action=show_image&user={user}&session={session}">Show Image</a>
        <li> Delete album
        <li> Make album public
        <li> Change pasword
        </ul>
        """
        #Also set a session number in a hidden field so the
        #cgi can check that the user has been authenticated

    print_html_content_type()
    print(html.format(user=user,session=session))


def main():
    display_admin_options()
