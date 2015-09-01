__author__ = 'corcoran'

def heapow_reverse(iname,outname,chatter=0):
    """
    This python function reverses the order of the rows in a heapow index file (stars/index.html or
    heapow_2013.html, for example) so that the most recent items are on the top
    """
    file=open(iname,"r")
    a=file.read()
    file.close()
    a=a.replace('\n',' ') # replace the \n with a blank space
    a=a.replace('\t',' ') # replace the \t with a blank space
    # get the html before the start of the rows
    x=a.upper().find("<TR>")
    htmlstart=a[0:x-1]
    rows=['']
    # first row is the table header, so save and remove it
    status=0
    x=a.find("<TR>")
    if x>=0:
        y=a.upper().find("</TR>") # this finds the first occurrence of the end of the row
        xstart=x
        yend=y+5
        row=a[xstart:yend] # this is the header row - it starts at x and goes to y+5 (since </TR> has 5 characters
        print "row = %s\n" % row
        htmlstart=htmlstart+"\n"+row
        a=a[yend+1:]
    else:
        status=-1
        print "Did not find first row in Table"
        return status
    while (len(a)>0):
        x=a.upper().find("<TR>") # this finds the first occurrence of the start of a row
        if x>=0:
            y=a.upper().find("</TR>") # this finds the first occurrence of the end of the row
            xstart=x
            yend=y+5
            row=a[xstart:yend] # this is the row - it starts at x and goes to y+5 (since </TR> has 5 characters
            if chatter>5:
                print "row = %s\n" % row
            rows=[row]+rows
            a=a[yend+1:]
        else:
            print "Found %i rows\n" % len(rows)
            htmlend=a[0:]
            rows=[htmlstart]+rows+[htmlend]
            a=''
    fout=open(outname,"w")
    for row in rows:
        row.replace("<br>","<br>\n")
        row.replace("<p>","<p>\n")
        fout.write(row+"\n")
    return status