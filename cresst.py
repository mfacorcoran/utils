__author__ = 'corcoran'

def parse_sp_data(sptxtfile,outname,chatter=0):
    """
    To generate the special project quarterly stats
        1) do a search on the vtrs for the quarter (example for qtr 1: search activity start from 10/01/14 to 12/31/14)
        2) copy the resulting table and paste to a text file (called sp_stats.txt, for example)
        3) run this module on the file - it will create a pipe-delimited file which then can be loaded into Excel
    """
    file=open(sptxtfile,"r")
    a=file.read()
    file.close()
    b=b=a.replace("View detail ", " ") # replace occurrences of annoying "view detail"
    b=b.replace("\n", " | ") # replace the newlines with a pipe
    b=b.replace("[C]","\n[C]") # replace the [C] occurrences with a newline+[C] so each entry is on its own row.
    title="Name | START | BDG | VISA| CITIZEN | HTL| CREA| MOD | COMP| CNC"
    fout=open(outname,"w")
    fout.write(title)
    fout.write(b)
    fout.close()
    status="output written to file "+outname
    if chatter > 0:
        print status
    return status