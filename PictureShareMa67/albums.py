#!/usr/bin/python

# Import the CGI, string, sys modules
import cgi, string, sys, os, re, random, shutil
import sqlite3
import cgitb; cgitb.enable()  # for troubleshooting

database='picture_share.db'
conn = sqlite3.connect(database)
c = conn.cursor()


def create_new_folder_album(user, user_id, dir, visibility) :
    albumpath = "users/"+user+"/albums/"+dir
    if not os.path.exists(albumpath) :
	c.execute("INSERT INTO albums (user_id, album, public) VALUES("+user_id+",'"+dir+"', "+visibility+");")
        conn.commit()        
        os.makedirs(albumpath)
        return 1
    else :
        return 0
    
def generate_list_of_albums(user_id, id) :
    if id == 1 :
        list = c.execute("SELECT album, public FROM albums WHERE user_id="+user_id)
    else :
        list = c.execute("SELECT album FROM albums WHERE user_id="+str(user_id)+" AND public=1")
    return list
 



def make_public(user_id, album) :
    c.execute("UPDATE albums  SET public=1 WHERE  album='"+album+"' AND user_id="+user_id)
    conn.commit()

def make_private(user_id,album) :
    c.execute("UPDATE albums  SET public=0 WHERE  album='"+album+"' AND user_id="+user_id)
    conn.commit()

def delete_album(user, user_id, album) :
    c.execute("DELETE FROM albums WHERE  album='"+album+"' AND user_id="+user_id)
    conn.commit()
    shutil.rmtree('users/'+user+'/albums/'+album+'/')

def upload_pic(user, album, fileitem):
    if fileitem.filename :
        # strip leading path from file name to avoid directory traversal attacks
        fn = os.path.basename(fileitem.filename)
        path = 'users/'+user+'/albums/'+ album + '/' + fn
        open(path, 'wb').write(fileitem.file.read())
        print "<strong>" + fileitem.filename + "</strong> was succesfully uploaded"
    else :
        print "<strong>" + fileitem.filename + "</strong> was not uploaded"

def delete_pic(pic):
    tmp = "rm -f "+ pic
    os.system(tmp)
