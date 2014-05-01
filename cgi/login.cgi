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


    

#############################################################
#Main view
def display_admin_options(user, session):
    html= """
<html>
<head>
<title>PeteTwitt</title>
<meta http-equiv="refresh" content="30">
</head>

<body BGCOLOR = white>


<h2>
<image width="50" height="50" src="images/user1/test.jpg">
USER
</h2>

<a href="login.cgi?action=admin&user={user}&session={session}">Tweets</a>
<a href="login.cgi?action=Following&user={user}&session={session}">Following</a>
<a href="login.cgi?action=Followers&user={user}&session={session}">Followers</a>
<a href="login.cgi?action=Search&user={user}&session={session}">Search</a>
<a href="login.cgi?action=Profile&user={user}&session={session}">Profile</a>
<a href="login.cgi?action=Logout&user={user}&session={session}">Logout</a>

<br><br>
<hr>
<br>


<form ACTION="login.cgi" METHOD="POST" enctype="multipart/form-data">
<input size="50" maxlength="140" type="text" name="message">
<br>
<input type="hidden" value="ac72d082a0a7e941acc70599b98c0bcd" name="sid">
<input type="hidden" name="user" value="{user}">
<input type="hidden" name="session" value="{session}">
<input type="hidden" name="action" value="upload-pic-data">
<input TYPE="FILE" NAME="file">
<input type="submit" value="Tweet">
</form>
<br>



<h3>
<img height="50" width="50" src="images/user1/test.jpg">
ma70: Hello World! [Wed, 23 Apr 2014 17:31:15] 

<form action="pete_twitt.cgi" method="POST">
<input type="hidden" name="user" value="mm">
<input type="hidden" name="session" value="YJXS8FWUK2H3TGZ90VQM">
<input type="hidden" name="action" value="reply">
<input type="hidden" name="tweetid" value="64">
<input type="text" size="50" name="reply">
<input type="submit" value="Reply">
</form>



</h3>


</body>
</html>
    """
    print_html_content_type()
    print(html.format(user=user,session=session))

#############################################################
# Define function to generate HTML form.
def generate_form():
    str = """
<HTML>
<HEAD>
<TITLE>Info Form</TITLE>
</HEAD>

<BODY BGCOLOR = white>

<center><H2>Create New Account</H2></center>

<H3>Please enter your username and password.</H3>

<TABLE BORDER = 0>
<FORM METHOD = post ACTION = "login.cgi">
<TR><TH>Login:</TH><TD><INPUT type = text  name = "inputLogin"></TD><TR>
<TR><TH>Email Address:</TH><TD><INPUT type = text  name = "email"></TD><TR>
<TR><TH>displayName:</TH><TD><INPUT type = text  name = "displayName"></TD><TR>
<TR><TH>Password:</TH><TD><INPUT type = password name ="password"></TD></TR>


</TABLE>

<INPUT TYPE = hidden NAME = "action" VALUE = "registerSub">
<INPUT TYPE = submit VALUE = "Enter">
</FORM>
</BODY>
</HTML>
"""
    print_html_content_type()
    print(str)



# Define function create user.
def display_data(email, password, login, displayName):

    create_user_dir(login)
    #sendemail(username,password)
    activate(email,password, login, displayName)
    str="""
    <html>
    <head>
    <meta http-equiv="refresh" content="2; URL="www.google.com">
    <script type="text/javascript">

    </script>
    </head>
    <body>
    <h2>Account Created</h2>
    <p>%s is created. You need check your email to activate your account.<p>
    
    </body>
    </html>"""
    print_html_content_type()
    print(str % (email))


def create_user_dir(username):
    filename = HOMEPATH + "/users/" + username
    if not os.path.exists(filename):
        os.makedirs(filename)
    filename2 = HOMEPATH +  "/users/" + username + "/albums"
    if not os.path.exists(filename2):
        os.makedirs(filename2)


def activate(username,password, login, displayName):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()

    user=(login, username, displayName, password,"true", "Nothing" )
    c.execute('INSERT INTO users VALUES (?,?,?, ?, ?, ?)', user);
    conn.commit()


# Define main function.
        

##############################################################
# Define function to generate login HTML form.
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
<TR><TH>Username:</TH><TD><INPUT TYPE=text NAME="username"></TD><TR>
<TR><TH>Password:</TH><TD><INPUT TYPE=password NAME="password"></TD></TR>
</TABLE>

<INPUT TYPE=hidden NAME="action" VALUE="login">
<INPUT TYPE=submit VALUE="Enter">
</FORM>
<INPUT TYPE=submit VALUE="Create account"
    onclick="window.location='login.cgi?action=register';"/>
</BODY>
</HTML>
"""
    print_html_content_type()
    print(html)


###################################################################
# Define function to test the password.
def check_password(user, passwd):

    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()

    t = (user,)
    c.execute('SELECT * FROM users WHERE email=?', t)

    row = stored_password=c.fetchone()
    conn.close();

    if row != None: 
        stored_password=row[1]
        if (stored_password==passwd):
            return "passed"

    return "failed"



#################################################################
def create_new_session(user):
    return session.create_session(user)

##############################################################
def new_album(form):
    #Check session
    if session.check_session(form) != "passed":
       return

    html="""
        <H1> New Album</H1>
        """
    print_html_content_type()
    print(html);

##############################################################
def show_image(form):
    #Check session
    if session.check_session(form) != "passed":
       login_form()
       return

    # Your code should get the user album and picture and verify that the image belongs to this
    # user and this album before loading it

    #username=form["username"].value

    # Read image
    with open(IMAGEPATH+'/user1/test.jpg', 'rb') as content_file:
       content = content_file.read()

    # Send header and image content
    hdr = "Content-Type: image/jpeg\nContent-Length: %d\n\n" % len(content)
    print hdr+content

###############################################################################

def upload(form):
    if session.check_session(form) != "passed":
       login_form()
       return

    html="""
        <HTML>

        <FORM ACTION="login.cgi" METHOD="POST" enctype="multipart/form-data">
            <input type="hidden" name="user" value="{user}">
            <input type="hidden" name="session" value="{session}">
            <input type="hidden" name="action" value="upload-pic-data">
            <BR><I>Browse Picture:</I> <INPUT TYPE="FILE" NAME="file">
            <br>
            <input type="submit" value="Press"> to upload the picture!
            </form>
        </HTML>
    """

    user=form["user"].value
    s=form["session"].value
    print_html_content_type()
    print(html.format(user=user,session=s))

#######################################################

def upload_pic_data(form):
    #Check session is correct
    if (session.check_session(form) != "passed"):
        login_form()
        return

    #Get file info
    fileInfo = form['file']

    #Get user
    user=form["user"].value
    s=form["session"].value

    # Check if the file was uploaded
    if fileInfo.filename:
        # Remove directory path to extract name only
        fileName = os.path.basename(fileInfo.filename)
        open(IMAGEPATH+'/user1/test.jpg', 'wb').write(fileInfo.file.read())
        image_url="login.cgi?action=show_image&user={user}&session={session}".format(user=user,session=s)
        print_html_content_type()
        print ('<H2>The picture ' + fileName + ' was uploaded successfully</H2>')
        print('<image src="'+image_url+'">')
    else:
        message = 'No file was uploaded'

def print_html_content_type():
	# Required header that tells the browser how to render the HTML.
	print("Content-Type: text/html; image/jpg\n\n")

#############################################################


def register_new(form):
    if "email" in form and "password" in form and "inputLogin" in form and "displayName" in form:
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        t = (form["email"].value,)
        c.execute('SELECT * FROM users WHERE email=?', t)
        if(c.fetchone()):
            generate_form()
            print("<H3><font color=\"red\">Email Exists! </font></H3>")
        else:
            display_data(form["email"].value, form["password"].value, form["inputLogin"].value, form["displayName"].value)
    else:
        login_form()


def logoutUser(form):
    session.delete_session(form["user"].value)
    print_html_content_type()
    print("<H3><font color=\"black\">Successfully Loged out! </font></H3>\n\n")
    jump = """
    <meta http-equiv="refresh" content="5; url=login.cgi" />
    """
    print(jump)

##############################################################
# Define main function.
def main():
    form = cgi.FieldStorage()
    if "action" in form:
        action=form["action"].value
        #print("action=",action)
        if action == "login":
            if "username" in form and "password" in form:
                #Test password
                username=form["username"].value
                password=form["password"].value
                if check_password(username, password)=="passed":
                   session=create_new_session(username)
                   fowardLink = """
                   <meta http-equiv="refresh" content="0; url=login.cgi?action=admin&user={user}&session={session}" />
                   """
                   print_html_content_type()
                   print(fowardLink.format(user=username, session=session))
                   
                else:
                   login_form()
                   print("<H3><font color=\"red\">Incorrect user/password</font></H3>")
        elif action == "register":
            generate_form()
        elif action == "admin":
            display_admin_options(form["user"].value, form["session"].value)
        elif action == "registerSub":
            register_new(form)
        elif (action == "new-album"):
            new_album(form)
        elif (action == "upload"):
            upload(form)
        elif (action == "show_image"):
            show_image(form)
        elif action == "upload-pic-data":
            upload_pic_data(form)
        elif action == "Logout":
            logoutUser(form)
        else:
            login_form()
    else:
        login_form()

###############################################################
# Call main function.
main()
