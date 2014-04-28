#!/usr/bin/python

import cgi,sqlite3

# Required header that tells the browser how to render the HTML.
print "Content-Type: text/html\n\n"

MYLOGIN=getpass.getuser()
DATABASE="/homes/"+MYLOGIN+"/PeteTwitt/picture_share.db"
IMAGEPATH="/homes/"+MYLOGIN+"/PeteTwitt/images"
HOMEPATH="/homes/"+MYLOGIN+"/PeteTwitt"

# Define function to generate HTML form.
def generate_form():
    str = """
    <html>
    <head>
    <h2>Congrduations! Your account has been created!</h2>
    <p>Click <a href="login.cgi">here</a> to log in</p>
    
    </body>
    </html>"""

    print(str)

def activate(username):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("UPDATE users set active = 1 WHERE username='"+username+"' ;")
    conn.commit()
    conn.close()

    
# Define main function.1
def main():
    form = cgi.FieldStorage()
    #activate(form["username"].value)
    #print form["username"].value
    generate_form()

# Call main function.
main()
