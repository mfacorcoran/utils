def html2csv(htmlfile,tabnum=0, UE=False):
    """
    this converts an html file containing a table to an csv formatted table
    to import into Excel
    htmlfile is the source html file containing the table
    tabnum is the number of the table on the html page (default is the first table)
    UE= True means this is a USRA university engagement page (requires special handling of title field)

    @param htmlfile:
    @param outfile:
    @param tabnum:
    @return:
    """
    from BeautifulSoup import BeautifulSoup

    file=open(htmlfile,'r')
    html=file.read()
    file.close()
    soup = BeautifulSoup(''.join(html))
    table = soup.findAll('table')
    csvtab=table[tabnum]
    rows = csvtab.findAll('tr')
    cvstable=['']
    topic=''
    for row in rows:
        n=''
        if UE:
            topic=row.findAll('div')
            if len(topic) == 2:
                topic = str(topic[1].find(text=True))
            else: topic = ""
        cols=row.findAll('td')
        for col in cols:
            n = n+' | '+str(col.find(text=True)).strip()
        n = n.replace("&nbsp;"," ")
        n = n.replace("\n", " ")
        n = n.replace(" ,", " ") # if comma has only space character in front of it, remove it.
        print n+topic
        if len(n) > 0:
            cvstable.append(n)
        if UE:
            cvstable.append(topic)
    return cvstable[1:]


if __name__== "__main__":
    filename = "/Volumes/Area51/USRA/Reports/Board of Trustees Report/2014/University Engagement/University Engagement by USRA Institutes and Programs - Institute-Program Listing.html"

    n = html2csv(filename,tabnum=3, UE=True)


