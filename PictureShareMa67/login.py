#!/usr/bin/python

# Import the CGI, string, sys modules
import cgi, string, sys, os, re, random,sqlite3

import cgitb; cgitb.enable()  # for troubleshooting

# Define function to generate HTML form.
def login_form():
    html="""
<HTML>
<HEAD>
<TITLE>Info Form</TITLE>
</HEAD>

<BODY BGCOLOR = white>

<center><H2>PictureShare User Administration</H2></center>

<H3>Type User and Password:</H3>

<TABLE BORDER = 0>
<FORM METHOD=post ACTION="login.cgi">
<TR><TH>Email Address:</TH><TD><INPUT TYPE=text NAME="username"></TD><TR>
<TR><TH>Password:</TH><TD><INPUT TYPE=password NAME="password"></TD></TR>
</TABLE>

<INPUT TYPE=hidden NAME="action" VALUE="login">
<INPUT TYPE=submit VALUE="Enter">
</FORM>
</BODY>
</HTML>
"""
    print(html)
    
# Define function to test the password.
def check_password(user, passwd):
    conn = sqlite3.connect('picture_share.db')
    c = conn.cursor()
    
    try:
        list = c.execute("SELECT * FROM users WHERE username='"+user+"';")
        conn.commit()
        row = list.fetchone()
        stored_password = row[2]
    except:
        #No user"
        return "failed"
    
    if (stored_password==passwd): 
        return "passed"
    else:
        return "failed"

def delete(user, user_id) :
    conn = sqlite3.connect('picture_share.db')
    c = conn.cursor()
    c.execute("DELETE FROM albums WHERE user_id="+user_id+";")
    c.execute("DELETE FROM session WHERE user_id="+user_id+";")
    c.execute("DELETE FROM users WHERE username='"+user+"';")
    conn.commit()
    shutil.rmtree('users/'+user+'/')
    
def change_passwd(user,password):
    conn = sqlite3.connect('picture_share.db')
    c = conn.cursor()
    c.execute("UPDATE users SET password='"+password+"' where username='"+user+"';")
    conn.commit()

