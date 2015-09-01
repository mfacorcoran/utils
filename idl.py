import numpy as np

def findfile(search_string,ddir='.'):
    """
    searches for a filename search string in a directory ddir
    Reproduces some of the functionality of the IDL findfile procedure

    calling sequence:
        list=findfile("*.fits",ddir="/tmp")
    """
    import glob
    list=glob.glob(ddir+'/'+search_string)
    list=np.asarray(list)
    # count=len(list)
    return list

def forprint(*args):
    """
    for a set of arrays passed as *args, print columns one row at a time
    """
    print "type of args is ",type(args)
    numargs=len(args)
    print "Number of Args is %i" % numargs
    numitems=len(args[0])
    for i in range(numargs):
        for k in range(numitems):
            a=args[i]
    return
