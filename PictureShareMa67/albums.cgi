#!/usr/bin/python

# Import the CGI, string, sys modules
import cgi, string, sys, os, re, random

import cgitb; cgitb.enable()  # for troubleshooting

import login
import session
import albums

# Required header that tells the browser how to render the HTML.
print("Content-Type: text/html\n\n")

def delete_user(form) :
    user = form['user'].value
    user_id=form['user_id'].value
    user_session = form['session'].value
    html = '''
        <FORM METHOD=post ACTION="albums.cgi">
        <INPUT TYPE=hidden NAME="action" VALUE="delete_user">
        <INPUT TYPE=hidden NAME="user" VALUE="'''+user+'''">
        <INPUT TYPE=hidden NAME="user_id" VALUE="'''+user_id+'''">
        <INPUT TYPE=hidden NAME="session" VALUE="'''+user_session+'''">
        <INPUT TYPE=submit VALUE="Delete User">
        </FORM>
    '''
    return html

def user_profile(form) :
    if (session.check_session(form) != "passed"):
        login.login_form()
        print("Wrong session:", sys.exc_info()[0])
        return
    modify_pass = modify_password(form)
    d_user = delete_user(form)
    html = '''
    <table>
        <tr>
            <th>Logged In As</th>
            <th>Modify Password</th>
            <th>Delete User</th>
        </tr>
        <tr>
            <td>'''+ form['user'].value + '''</td>
            <td>'''+ modify_pass+'''</td>
            <td>'''+d_user+'''</td>
        </tr>
    </table>
     '''
    
    print(html)
    
def modify_password(form) :
    user = form['user'].value
    user_id=form['user_id'].value
    user_session = form['session'].value
    html = '''
        <FORM METHOD=post ACTION="albums.cgi">
        <INPUT TYPE=hidden NAME="action" VALUE="modify_password">
        <INPUT TYPE=hidden NAME="user" VALUE="'''+user+'''">
        <INPUT TYPE=hidden NAME="user_id" VALUE="'''+user_id+'''">
        <INPUT TYPE=hidden NAME="session" VALUE="'''+user_session+'''">
        <INPUT TYPE=submit VALUE="Modify Password">
        </FORM>
    '''
    return html
    
    
def new_album(form) :
    user = form['user'].value
    user_id=form['user_id'].value
    user_session = form['session'].value

    html = '''
        <TABLE BORDER = 0>
        <FORM METHOD=post ACTION="albums.cgi">
        <TR><TH>Create New Album:</TH><TD><INPUT TYPE=text NAME="album"></TD>
        <td><INPUT TYPE=submit VALUE="Create New Album"></td><TR>
        </TABLE>
        <INPUT TYPE=hidden NAME="action" VALUE="create_album">
        <INPUT TYPE=hidden NAME="user" VALUE="'''+user+'''">
        <INPUT TYPE=hidden NAME="user_id" VALUE="'''+user_id+'''">
        <INPUT TYPE=hidden NAME="session" VALUE="'''+user_session+'''">
        </FORM>
    '''
    print(html)
    list_albums(form)


def list_albums(form):
    list = albums.generate_list_of_albums(user_id, 3)
    print "<table><tr><th>Folder Name</th><th>Status</th><th>Change Permission</th><th>Upload Pics</th><th>Delete</th></tr>"
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

def upload_pics_form(form, album) :
    user = form['user'].value
    user_id=form['user_id'].value
    user_session = form['session'].value
    html = '''<td>
    <form enctype="multipart/form-data" METHOD=post action="albums.cgi">
    <input type="file" name="file">
    <input type="submit" value="Upload"></p>
    <FORM METHOD=post ACTION="albums.cgi">
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
    <FORM METHOD=post ACTION="albums.cgi">
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
    <FORM METHOD=post ACTION="albums.cgi"><td>
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
    <FORM METHOD=post ACTION="albums.cgi">
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
if form.has_key('user_id') :
    user_id = form['user_id'].value
if form.has_key('album') :
    album = form['album'].value
if form.has_key('file') :
    fileitem = form['file']
    
if action == "create_album" :
    if albums.create_new_folder_album(user, user_id, album) == 0 :
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
elif action == "modify_password" :
    print "modify_password"

user_profile(form)
new_album(form)