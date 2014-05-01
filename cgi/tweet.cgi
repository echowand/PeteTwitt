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


#print "Content-Type: text/html\n\n"

MYLOGIN=getpass.getuser()
portNum = "7111"

if MYLOGIN == "jin75":
    portNum = "61111"


host="http://data.cs.purdue.edu:"+portNum+"/PeteTwitt"
DATABASE="/homes/"+MYLOGIN+"/PeteTwitt/picture_share.db"
IMAGEPATH="/homes/"+MYLOGIN+"/PeteTwitt/images"
HOMEPATH="/homes/"+MYLOGIN+"/PeteTwitt"

########################################################################
def displayTweets(login):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    t = (login,)
    
    followingList = []
    for following in c.execute('SELECT * FROM follows WHERE followerLogin=?', t):
        followingList.append(following)
    
    #print "follwingList: "
    #print followingList
    
    
    tweetList = []
    ###### add current user 
    for row in c.execute('SELECT * FROM tweets WHERE login=?', t):
        tweetList.append(row)
    
    ###### add current user's following accounts. 
    t = (login,)
    for following in followingList:
        u = (following[1], )
        for row in c.execute('SELECT * FROM tweets WHERE login=?', u):
            tweetList.append(row)
    
    conn.commit()
    
    #print "tweetList"
    #print len(tweetList)
    
    
#####################################################################
def displayFollowing(login):    
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    t = (login,)
    followingList = []
    for following in c.execute('SELECT * FROM follows WHERE followerLogin=?', t):
        followingList.append(following)
    
    #print "follwingList: "
    #print followingList
    conn.commit()
    

######################################################################
def displayFollowers(login):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    t = (login,)
    followersList = []
    for follower in c.execute('SELECT * FROM follows WHERE followingLogin=?', t):
        followersList.append(follower)
    conn.commit()
    #print followersList
    
    
displayTweets('jin')
displayFollowing('mgq')
displayFollowers('mm')

