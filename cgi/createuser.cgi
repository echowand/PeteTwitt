#!/usr/bin/python
# Import the CGI, string, sys modules
import cgi, string, sys, os, re, random
import cgitb; cgitb.enable()  # for troubleshooting
import sqlite3
import session
import getpass
import smtplib

from email.mime.text import MIMEText

# Required header that tells the browser how to render the HTML.
print "Content-Type: text/html\n\n"
#host="http://data.cs.purdue.edu:4321/PictureShareDB/PictureShare"
host="http://data.cs.purdue.edu:7111/PeteTwitt"

MYLOGIN=getpass.getuser()
DATABASE="/homes/"+MYLOGIN+"/PeteTwitt/picture_share.db"
IMAGEPATH="/homes/"+MYLOGIN+"/PeteTwitt/images"
HOMEPATH="/homes/"+MYLOGIN+"/PeteTwitt"

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
<FORM METHOD = post ACTION = "createuser.cgi">
<TR><TH>Email Address:</TH><TD><INPUT type = text  name = "username"></TD><TR>
<TR><TH>Password:</TH><TD><INPUT type = password name ="password"></TD></TR>
</TABLE>

<INPUT TYPE = hidden NAME = "action" VALUE = "display">
<INPUT TYPE = submit VALUE = "Enter">
</FORM>
</BODY>
</HTML>
"""
    print(str)



# Define function create user.
def display_data(username, password):

    create_user_dir(username)
    sendemail(username,password)
    activate(username,password)
    str="""
    <html>
    <head>
    <script type="text/javascript">

    </script>
    </head>
    <body>
    <h2>Account Created</h2>
    <p>%s is created. You need check your email to activate your account.<p>
    
    </body>
    </html>"""
    print(str % (username))


def create_user_dir(username):
    filename = HOMEPATH + "/users/" + username
    if not os.path.exists(filename):
        os.makedirs(filename)
    filename2 = HOMEPATH +  "/users/" + username + "/albums"
    if not os.path.exists(filename2):
        os.makedirs(filename2)

def sendemail(username,password):
    ############# escapse character is critical in py ############################
    body = "Please click the following link to activate your account for CS390 PictureShare.\n\n"  \
    + host+"/activate.cgi?action=activate&username="+username+"&password="+password

    msg = MIMEText(body)
    fromaddr = "maggie@purdue.edu"
    toaddr = username
    msg['Subject'] = 'Please verfy your account for PictureShare! '
    msg['From'] = fromaddr
    msg['To'] = toaddr
    s = smtplib.SMTP("localhost")
    s.set_debuglevel(1)
    s.sendmail(fromaddr,[toaddr],msg.as_string())
    s.quit()

def activate(username,password):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()

    user=(username, password)
    c.execute('INSERT INTO users VALUES (?,?)', user);
    conn.commit()
        
# Define main function.
def main():
    form = cgi.FieldStorage()
    if (form.has_key("action") and form.has_key("username") and form.has_key("password")):
        if (form["action"].value == "display"):
            conn = sqlite3.connect(DATABASE)
            c = conn.cursor()
            t = (form["username"].value,)
            c.execute('SELECT * FROM users WHERE email=?', t)
            if(c.fetchone()):
                generate_form()
                print("<H3><font color=\"red\">User Name Exists! </font></H3>")
            else:
                display_data(form["username"].value, form["password"].value)
    else:
        generate_form()

# Call main function.
main()
