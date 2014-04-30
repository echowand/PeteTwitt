#!/usr/bin/python

# Import the CGI, string, sys modules
import cgi, string, sys, os, re, random, glob

import cgitb; cgitb.enable()  # for troubleshooting
import sqlite3
# import the db library

import login
import session
import admin
import albums

# Required header that tells the browser how to render the HTML.
print("Content-Type: text/html\n\n")




database='picture_share.db'


conn =  sqlite3.connect(database)
c = conn.cursor()



def home_page(form):
    list = c.execute("SELECT username FROM users WHERE active=1")
    print "<h3>Come check out others' pictures!<br/>Select any of the following member of our website</h3>"
    print "<table>"
    for row in list :
	owner=row[0]
        html = "<tr>"
        if session.check_session(form)=="passed":
	    user = form["user"].value
            s = form["session"].value
            html +="<td><a href='main.cgi?action=albums_of_user&owner="+owner+"&user="+user+"&session="+s+"'>" + owner +"</a></td>"
        else:
            html +="<td><a href='main.cgi?action=albums_of_user&owner="+owner+"'>" + owner +"</a></td>"
	html +="</tr>"
	print(html.format(user=owner))
    print "</table>"

    


def albums_of_user(form) :
    owner = form['owner'].value
    list = c.execute("SELECT user_id FROM users WHERE username='"+owner+"'")
    conn.commit()
    row = list.fetchone()
    user_id = row[0]
    user = ""
    ss = ""
    if session.check_session(form)=="passed" and form["user"].value==owner:
        list = c.execute("SELECT album FROM albums WHERE user_id="+str(user_id))
        user = form["user"].value
        ss = form["session"].value
    else:
        list = c.execute("SELECT album FROM albums WHERE user_id="+str(user_id)+" AND public=1")
    conn.commit()


    print "<table><tr><th>Public Albums of "+owner+"</th></tr>"
    for row in list :
	album = row[0]
        html = "<tr>"
        html += "<td><a href='main.cgi?action=album_gallery&owner={owner}&album={album}&user={user}&session={session}'>" + album +"</a></td>"
        html += "</tr>"
    	print(html.format(owner=owner,album=album, user=user, session=ss))
    print "</table>"

def album_gallery(form) :
    owner = form['owner'].value
    album = form['album'].value
    user =""
    ss = ""
    if session.check_session(form)=="passed":
        user = form['user'].value
        ss = form['session'].value

    print '<H1>%s:%s</H1>' % (owner,album)
    html = "<a href='main.cgi?action=albums_of_user&owner={owner}&user={user}&session={session}'>Go back to the album</a>";
    print html.format(owner=owner, user=user, session=ss)
    #Read all pictures
    dir="users/"+owner+"/albums/"+album+"/*"
    pics=glob.glob(dir)
    
    #for pic in pics:
    #	print '<img src="%s">' % pic

    
    #sys.exit()
    
    # Print pictures in a table
    
    print """
    <center><form action="main.cgi"><table border="0">
    """
    pics_in_row=0
    for pic in pics:
    
	# Check if we need to start a new row
	if pics_in_row == 0:
	    print "<tr>"
    
	print """<td>
		<a href="%s"> 
			<img src="%s" width="100" height="100"><p>
		</a>
		<input type=checkbox name="delete_pic_%s">
		</td>""" % (pic, pic, pic)
	pics_in_row = pics_in_row + 1
    
	if pics_in_row == 5:
	    print "</tr>"
	    pics_in_row = 0
    
    #Close row if it is not closed
    if pics_in_row > 0:
	    print "</tr>"
    
    
    print """</table>
<input type=submit value="delete">
<input type=hidden name="owner" value="%s">
<input type=hidden name="user" value="%s">
<input type=hidden name="album" value="%s">
<input type=hidden name="session" value="%s">
<input type=hidden name="action" value="deleting_pic">
</form></center>
""" % (owner, owner, album, ss)
    print """
    </body>
    </html>
    """

def deleting_pic(form):
    if (session.check_session(form)=="passed"):
        user = form["user"].value
        album = form["album"].value
        for f in form:
            if f[0:11]=="delete_pic_":
                pic = f[11:len(f)]
                albums.delete_pic(pic)
                
    album_gallery(form)

def main():
    form = cgi.FieldStorage()
    main = "home_page"
    user =""
    action = "home_page"
    if "action" in form:
    	action=form["action"].value
                        
    print """<html>
	    <head>
		<title>CS390 : PictureShare</title>
	    </head>
	    <body>
                <h1> CS390 Picture Share </h1>
"""
    if session.check_session(form)=="passed":
        list = c.execute("SELECT user_id FROM users WHERE username='"+form["user"].value+"'")
        conn.commit()
        row = list.fetchone()
        user_id = row[0]
        print """<a href="admin.cgi?user=%s&user_id=%s&session=%s&action=view"> Edit Profile</a><br/>""" % (form["user"].value, user_id, form["session"].value)
        print """<a href="logout.cgi?user_id=%s">Log Out</a><br/>""" % user_id
    else:
        print """<h2>Login</h2>
			<a href="login.cgi"> Login</a>
                        <br/>
			<a href="createuser.cgi"> Register </a>"""

    if action == "home_page" :
        home_page(form)
    elif action == "albums_of_user" :
        albums_of_user(form)
    elif action == "album_gallery" :
        album_gallery(form)
    elif action == "deleting_pic" :
        deleting_pic(form) 
    
    
    print """
		    CS390 : Python <br/>Created by HongYuan Wang, Yibo Ma, ChenYang Qu
	</html>
	"""

main()
