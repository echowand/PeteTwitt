#!/usr/bin/python

# Import the CGI, string, sys modules
import cgi, string, sys, os, re, random

import cgitb; cgitb.enable()  # for troubleshooting

import login
import session
import albums

# Required header that tells the browser how to render the HTML.
print("Content-Type: text/html\n\n")

form = cgi.FieldStorage()
html="""
<HTML>
<HEAD>
<TITLE>Info Form</TITLE>
</HEAD>

<BODY BGCOLOR = white>

<center><H2>PictureShare User Administration</H2></center>

<H3>Modify User and Password:</H3>

<TABLE BORDER = 0>
<FORM METHOD=post ACTION="admin.cgi">
<TR><TH>New Password:</TH><TD><INPUT TYPE=password NAME="password"></TD></TR>
</TABLE>

<INPUT TYPE=hidden NAME="action" VALUE="changing_pass">
<INPUT TYPE=hidden NAME="user" VALUE="""+form['user'].value+""">
<INPUT TYPE=hidden NAME="user_id" VALUE="""+form['user_id'].value+""">
<INPUT TYPE=hidden NAME="session" VALUE="""+form['session'].value+""">
<INPUT TYPE=submit VALUE="Enter">
</FORM>
</BODY>
</HTML>
"""
print(html)