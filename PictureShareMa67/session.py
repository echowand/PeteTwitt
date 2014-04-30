#!/usr/bin/python

# Import the CGI, string, sys modules
import cgi, string, sys, os, re, random

import cgitb; cgitb.enable()  # for troubleshooting


def create_session(user):
    n=20
    char_set = string.ascii_uppercase + string.digits
    session = ''.join(random.sample(char_set,n)) 

    #store random string as session number
    session_file = open("users/"+user+"/session.txt", 'w')
    session_file.write(session)
    session_file.close()
    return session

def check_session(form):
    #print("Checking session")
    if "user" in form and "session" in form:
	#print("User here")
        username=form["user"].value
        session=form["session"].value
        #print("user=",username," session=",session)
        session_stored=read_session_string(username)
        #print(" session_stored="+session_stored)
        if session_stored==session:
           return "passed"
    
    return "failed"


def read_session_string(user):
    session_file = open("users/"+user+"/session.txt", 'r')
    session = session_file.readline().strip()
    session_file.close()
    return session