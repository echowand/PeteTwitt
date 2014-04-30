#!/usr/bin/python

# Import the CGI module
import cgi

# Required header that tells the browser how to render the HTML.
print "Content-Type: text/html\n\n"

# Define function to generate HTML form.
def generate_form():
    str = """
<HTML>
<HEAD>
<TITLE>Info Form</TITLE>
</HEAD>
<BODY BGCOLOR = white>
<H3>Please, enter your name and age.</H3>
<TABLE BORDER = 0>
<FORM METHOD = post ACTION = \"age.cgi\">
<TR><TH>Name:</TH><TD><INPUT type = text  name = \"name\"></TD><TR>
<TR><TH>Age:</TH><TD><INPUT type = text name =\"age\"></TD></TR>
</TABLE>
<INPUT TYPE = hidden NAME = \"action\" VALUE = \"display\">
<INPUT TYPE = submit VALUE = \"Enter\">
</FORM>
</BODY>
</HTML>
"""
    print(str)

# Define function display data.
def display_data(name, age):
    str="""
<HTML>
<HEAD>
<TITLE>Info Form</TITLE>
</HEAD>
<BODY BGCOLOR = white>
%s you are %s years old.
</BODY>
</HTML>
"""
    print(str % (name,age))

# Define main function.
def main():
    form = cgi.FieldStorage()
    if (form.has_key("action") and form.has_key("name") and form.has_key("age")):
        if (form["action"].value == "display"):
            display_data(form["name"].value, form["age"].value)
    else:
        generate_form()

# Call main function.
main()

