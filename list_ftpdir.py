__author__ = 'mcorcora'

import ftplib

def list_ftpdir(ftpurl,):
    """
    returns a list of files and directories for a given ftp site and specific directory path of the form
    ftpurl="ftp://heasarc.gsfc.nasa.gov/caldb/data
    """
    path=ftpurl.split('//')[1]
    server=path[0:path.find('/')]
    path=path[path.find('/')+1:]
    ftp=ftplib.FTP(server)
    #print "anonymous ftp login to "+ftpurl
    ftp.login("anonymous"," ")
    items=[]
    data=[]
    ftp.dir(path,data.append)
    for item in data:
        d=item.split(' ')[-1]
        items.append(d)
    return items