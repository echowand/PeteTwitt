#!/usr/bin/python

# Import the CGI, string, sys modules
import cgi, string, sys, os, re, random

import cgitb; cgitb.enable()  # for troubleshooting

import login
import session
import albums
import admin

# Required header that tells the browser how to render the HTML.
print("Content-Type: text/html\n\n")

MYLOGIN=getpass.getuser()
DATABASE="/homes/"+MYLOGIN+"/PeteTwitt/picture_share.db"
IMAGEPATH="/homes/"+MYLOGIN+"/PeteTwitt/images"
HOMEPATH="/homes/"+MYLOGIN+"/PeteTwitt"

def delete_user(form) :
    user = form['user'].value
    user_id=form['user_id'].value
    user_session = form['session'].value
    html = '''
        <FORM METHOD=post ACTION="admin.cgi">
        <INPUT TYPE=hidden NAME="action" VALUE="deleting_user">
        <INPUT TYPE=hidden NAME="user" VALUE="'''+user+'''">
        <INPUT TYPE=hidden NAME="user_id" VALUE="'''+user_id+'''">
        <INPUT TYPE=hidden NAME="session" VALUE="'''+user_session+'''">
        <INPUT TYPE=submit VALUE="Delete User">
        </FORM>
    '''
    return html

def deleting_user(user, user_id) :
    login.delete(user, user_id);
    print """
    <head>
<script type="text/javascript">
<!--
    window.location = "main.cgi"
//-->
</script>
</head>"""

def user_profile(form) :
    if (session.check_session(form) != "passed"):
        login.login_form()
        return
    
    d_user = delete_user(form)
    change_pass = change_password(form)
    html = "<br/>Welcome, " + form['user'].value + "!<br/>" 
    print(html)
    new_album(form)
    html =  change_pass + d_user + "<br/>"
    print(html)

def changing_passwd(user, pwd):
    login.change_passwd(user, pwd)
    print "You have succesfully changed your password to <b>"+ pwd + "<b>"
    
def change_password(form) :
    user = form['user'].value
    user_id=form['user_id'].value
    user_session = form['session'].value
    html = '''
        <FORM METHOD=post ACTION="admin.cgi">
	New Password:<INPUT TYPE=password NAME="password" VALUE="">
        <INPUT TYPE=hidden NAME="action" VALUE="changing_passwd">
        <INPUT TYPE=hidden NAME="user" VALUE="'''+user+'''">
        <INPUT TYPE=hidden NAME="user_id" VALUE="'''+user_id+'''">
        <INPUT TYPE=hidden NAME="session" VALUE="'''+user_session+'''">
        <INPUT TYPE=submit VALUE="Change Password">
        </FORM>
    '''
    return html
    
    
def new_album(form) :
    user = form['user'].value
    user_id=form['user_id'].value
    user_session = form['session'].value
    
    html = '''
        <FORM METHOD=post ACTION="admin.cgi">
        Name: <INPUT TYPE=text NAME="album">
	Made Public: <INPUT TYPE=checkbox NAME="made_public">
        <INPUT TYPE=submit VALUE="Create New Album">
        <INPUT TYPE=hidden NAME="action" VALUE="create_album">
        <INPUT TYPE=hidden NAME="user" VALUE="'''+user+'''">
        <INPUT TYPE=hidden NAME="user_id" VALUE="'''+user_id+'''">
        <INPUT TYPE=hidden NAME="session" VALUE="'''+user_session+'''">
        </FORM>
    '''
    print(html)
    list_albums(form)


def list_albums(form):
    user = form['user'].value
    user_id=form['user_id'].value

    list = albums.generate_list_of_albums(user_id, 1)

    if list != None:
        print "<br><table border = 0><tr><th>Folder Name</th><th>Status</th><th>Change Permission</th><th>Upload Pics</th><th>Delete</th></tr>"
        for row in list :
            print "<tr><td>"+row[0]+"</td>"
            if row[1] == 1 :
                print "<td>Public</td>"
                public_form(form, row[0])
            else :
                print"<td>Private</td>"
  	        private_form(form, row[0])
            upload_pics_form(form, row[0])
            delete_album(form, row[0])
            print "</tr>"
        print "</table>"
    else:
        print("There is no Album!")
    

def upload_pics_form(form, album) :
    user = form['user'].value
    user_id=form['user_id'].value
    user_session = form['session'].value
    html = '''<td>
    <form enctype="multipart/form-data" METHOD=post action="admin.cgi">
    <input type="file" name="file">
    <input type="submit" value="Upload">
    <INPUT TYPE=hidden NAME="action" VALUE="upload_pics">
    <INPUT TYPE=hidden NAME="user" VALUE="'''+user+'''">
    <INPUT TYPE=hidden NAME="user_id" VALUE="'''+user_id+'''">
    <INPUT TYPE=hidden NAME="session" VALUE="'''+user_session+'''">
    <INPUT TYPE=hidden NAME="album" VALUE="'''+album+'''">
    </form></td>
    '''
    print(html)


def public_form(form, album) :
    user = form['user'].value
    user_id=form['user_id'].value
    user_session = form['session'].value
    html = '''<td>
    <FORM METHOD=post ACTION="admin.cgi">
    <INPUT TYPE=hidden NAME="action" VALUE="make_private">
    <INPUT TYPE=hidden NAME="user" VALUE="'''+user+'''">
    <INPUT TYPE=hidden NAME="user_id" VALUE="'''+user_id+'''">
    <INPUT TYPE=hidden NAME="session" VALUE="'''+user_session+'''">
    <INPUT TYPE=hidden NAME="album" VALUE="'''+album+'''">
    <INPUT TYPE=submit VALUE="Make Private">
    </FORM></td>
    '''
    print(html)

def private_form(form, album) :
    user = form['user'].value
    user_id=form['user_id'].value
    user_session = form['session'].value
    html = '''
    <FORM METHOD=post ACTION="admin.cgi"><td>
    <INPUT TYPE=hidden NAME="action" VALUE="make_public">
    <INPUT TYPE=hidden NAME="user" VALUE="'''+user+'''">
    <INPUT TYPE=hidden NAME="user_id" VALUE="'''+user_id+'''">
    <INPUT TYPE=hidden NAME="session" VALUE="'''+user_session+'''">
    <INPUT TYPE=hidden NAME="album" VALUE="'''+album+'''">
    <INPUT TYPE=submit VALUE="Make Public">
    </FORM></td>
    '''
    print(html)
    
def delete_album(form, album) :
    user = form['user'].value
    user_id=form['user_id'].value
    user_session = form['session'].value
    html = '''<td>
    <FORM METHOD=post ACTION="admin.cgi">
    <INPUT TYPE=hidden NAME="action" VALUE="delete_album">
    <INPUT TYPE=hidden NAME="user" VALUE="'''+user+'''">
    <INPUT TYPE=hidden NAME="user_id" VALUE="'''+user_id+'''">
    <INPUT TYPE=hidden NAME="session" VALUE="'''+user_session+'''">
    <INPUT TYPE=hidden NAME="album" VALUE="'''+album+'''">
    <INPUT TYPE=submit VALUE="Delete Album">
    </FORM></td>
    '''
    print(html)
    

form = cgi.FieldStorage()

if(form.has_key('action')) :
    action = form['action'].value
else:
    action = "empty"    

if form.has_key('user') :
    user = form['user'].value
else:
    user = ""

if form.has_key('session') :
    ss = form['session'].value
else:
    ss = ""

if form.has_key('user_id') :
    user_id = form['user_id'].value
if form.has_key('album') :
    album = form['album'].value
if form.has_key('file') :
    fileitem = form['file']

if action == "create_album" :
    if form.has_key('made_public'):
        visibility = '1'
    else:
        visibility = '0'
    if not form.has_key('album') :
        print "File Name invalid<br>"
    else:
        if albums.create_new_folder_album(user, user_id, album, visibility) == 0 :
            print "<strong>"+album+" already exists.</strong>"
elif action == "make_private" :
    albums.make_private(user_id, album)
elif action == "make_public" :
    albums.make_public(user_id , album)
elif action == "upload_pics" :
    albums.upload_pic(user, album, fileitem)
elif action == "delete_album" :
    albums.delete_album(user, user_id, album)
elif action == "delete_user" :
    print "delete_user"
elif action == "change_password" :
    print "change_password"
elif action == "deleting_user" :
    deleting_user(user)
elif action == "changing_passwd"  :
    pwd = form['password'].value
    changing_passwd(user, pwd)


    
if action == "empty" :
    login.login_form()
else :
    print '<a href="main.cgi?user='+user+'&session='+ss+'" target=_blank>Go the Home Page</a>'
    user_profile(form)

