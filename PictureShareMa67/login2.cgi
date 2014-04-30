#!/usr/bin/python

# Import the CGI, string, sys modules
import cgi, string, sys, os, re, random

import cgitb; cgitb.enable()  # for troubleshooting

# Required header that tells the browser how to render the HTML.
print("Content-Type: text/html\n\n")

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
<FORM METHOD=post ACTION="login2.cgi">
<TR><TH>Username:</TH><TD><INPUT TYPE=text NAME="username"></TD><TR>
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

    if re.search("\.\.", user) or re.search("/", user):
        print("failed with ..")
        return "failed"

    try:
        passwd_file = open("users/"+user+"/password.txt", 'r')
    except:
        #No user"
        return "failed"

    stored_password = passwd_file.readline().strip()
    passwd_file.close()
    #print( "stored_password=\""+stored_password+"\"")
    if (stored_password==passwd): 
        return "passed"
    else:
        return "failed"


def display_admin_options(user, session):
    html="""
        <H1> Picture Share Admin Options</H1>
        <ul>
        <li> <a href="login2.cgi?action=new-album&user={user}&session={session}">Create new album</a>
        <li> <a href="login2.cgi?action=upload-pic&user={user}&session={session}">Upload Picture</a>
        <li> Delete album
        <li> Make album public
        <li> Change pawword
        </ul>
        """
        #Also set a session number in a hidden field so the
        #cgi can check that the user has been authenticated
    print(html.format(user=user,session=session))

def read_session_string(user):
    session_file = open("users/"+user+"/session.txt", 'r')
    session = session_file.readline().strip()
    session_file.close()
    return session

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
    print("Checking session")
    if "user" in form and "session" in form:
        print("User here")
        username=form["user"].value
        session=form["session"].value
        print("user=",username," session=",session)
        session_stored=read_session_string(username)
        print(" session_stored="+session_stored)
        if session_stored==session:
           return "passed"
    
    return "failed"

def upload_pic(form):
    if (check_session(form) != "passed"):
        login_form()
        print("Wrong session:", sys.exc_info()[0])
        return

    html="""
        <HTML>

        <FORM ACTION="login2.cgi" METHOD="POST" enctype="multipart/form-data">
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
    session=form["session"].value
    print(html.format(user=user,session=session))

def upload_pic_data(form):
    #Check session is correct
    if (check_session(form) != "passed"):
        login_form()
        print("Wrong session.")
        return

    #Get file info
    fileInfo = form['file']

    #Get user
    user=form["user"].value

    # Check if the file was uploaded
    if fileInfo.filename:
        # Remove directory path to extract name only
        fileName = os.path.basename(fileInfo.filename)
        open('users/'+user+"/albums/album1/" + fileName, 'wb').write(fileInfo.file.read())
        print('<H2>The picture ' + fileName + ' was uploaded successfully</H2>')
        print('<image src="users/'+user+'/albums/album1/' + fileName + '">')
    else:
        message = 'No file was uploaded'
   
def new_album(form):
    print("New album")
    if (check_session(form) != "passed"):
        login_form()
        print("Wrong session:", sys.exc_info()[0])
        return
 
    html = """
        <H1>New Album</H1>
        <TABLE BORDER = 0>
        <FORM METHOD=post ACTION="login2.cgi">
        <TR><TH>Album Name:</TH><TD><INPUT TYPE=text NAME="album"></TD><TR>
        </TABLE>
        <INPUT TYPE=hidden NAME="action" VALUE="new-album-response">
        <INPUT TYPE=submit VALUE="Enter">
        </FORM>
    """
    print(html)

# Define main function.
def main():
    #try:
        form = cgi.FieldStorage()
        if "action" in form:
            action=form["action"].value
            print("action=",action)
            if action == "login":
                if "username" in form and "password" in form:
                    #Test password
                    username=form["username"].value
                    password=form["password"].value
                    #print("You typed " + username + " and \"" + password +"\"<p>")
                    if check_password(username, password)=="passed":
                        session=create_session(username)
                        display_admin_options(username, session)
                    else:
                        login_form()
                        print("<H3><font color=\"red\">Incorrect user/password</font></H3>")
            elif action == "new-album":
                print("Here1")
                new_album(form)
            elif action == "upload-pic":
                upload_pic(form)
            elif action == "upload-pic-data":
                upload_pic_data(form)

        else:
            login_form()
    #except:
    #    login_form()
    #    print("Unexpected error:", sys.exc_info()[0])

# Call main function.
main()