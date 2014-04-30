#!/usr/bin/python

import cgi
import cgitb; cgitb.enable()  # for troubleshooting
import glob
import sys

user = "george@cs.purdue.edu"

print "Content-type: text/html"


def display_album(user, album) :    
    print '<center><H1>%s:%s</H1></center>' % (user,album)
    
    #Read all pictures
    dir="users/"+user+"/albums/"+album+"/*"
    pics=glob.glob(dir)
    
    #for pic in pics:
    #	print '<img src="%s">' % pic
    #	print "<p>"
    
    #sys.exit()
    
    # Print pictures in a table
    
    print """
    <table border="0">
    """
    pics_in_row=0
    for pic in pics:
    
	# Check if we need to start a new row
	if pics_in_row == 0:
	    print "<tr>"
    
	print "<td>"
	print '<a href="%s">' % pic
	print '<img src="%s" width="100" height="100"><p>' % pic
	print '</a>'
	print "</td>"
	pics_in_row = pics_in_row + 1
    
	if pics_in_row == 5:
	    print "</tr>"
	    pics_in_row = 0
    
    #Close row if it is not closed
    if pics_in_row > 0:
	    print "</tr>"
    
    
    print "</table>"
    
    print """
    </body>
    </html>
    """
