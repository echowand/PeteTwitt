#!/usr/bin/python

# Import the CGI, string, sys modules
import cgi, string, sys, os, re, random

import cgitb; cgitb.enable()  # for troubleshooting


def display_admin_options(user, user_id, session):
    html="""
<head>
<script type="text/javascript">
<!--
    window.location = "admin.cgi?action=new-album&user={user}&user_id={user_id}&session={session}"
//-->
</script>
</head>



        """
    print(html.format(user=user,user_id=user_id, session=session))
    

def album_gallery(form) :
    user = form['user'].value
    album = form['album'].value
    
    print '<H1>%s:%s</H1>' % (user,album)
    print "<a href='main.cgi?action=albums_of_user&user="+form['user'].value+"'>Go back to the album</a>"
    #Read all pictures
    dir="users/"+user+"/albums/"+album+"/*"
    pics=glob.glob(dir)
    
    #for pic in pics:
    #	print '<img src="%s">' % pic
    #	print "<p>"
    
    #sys.exit()
    
    # Print pictures in a table
    
    print """
    <center><table border="0">
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
    
    
    print "</table></center>"
    
    print """
    </body>
    </html>
    """