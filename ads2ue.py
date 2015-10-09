from BeautifulSoup import BeautifulSoup
import urllib2

import re, htmlentitydefs
import unicodedata


##
# Removes HTML or XML character references and entities from a text string.
#
# @param text The HTML (or XML) source text.
# @return The plain text, as a Unicode string, if necessary.

def unescape(text):
    def fixup(m):
        text = m.group(0)
        if text[:2] == "&#":
            # character reference
            try:
                if text[:3] == "&#x":
                    return unichr(int(text[3:-1], 16))
                else:
                    return unichr(int(text[2:-1]))
            except ValueError:
                pass
        else:
            # named entity
            try:
                text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
            except KeyError:
                pass
        return text # leave as is
    return re.sub("&#?\w+;", fixup, text)

def mkadsurl(name,yearstart=2013, yearend=2014, numret=2000):
    """
    creates an ads url for an author between the given years
    name is of the form "corcoran, m. f." or "drake, s."
    year start and end are the start and end years to search
    numret = maximum number of entries to return

    @param name:
    @param yearstart:
    @param yearend:
    @return:
    """
    n = name.strip().split(",")
    lname = n[0]
    fi = n[1].split('.')[0] + '.'
    try:
        mi = n[1].split('.')[1]
    except IndexError:
        pass
    try:
        author = lname + "%2C" + "+" + fi.strip() + "+" + mi.strip()
    except: # no middle initial
        author = lname + "%2C" + "+" + fi.strip()
    """
    adsurl = "http://adsabs.harvard.edu/cgi-bin/nph-abs_connect?db_key=AST&db_key=PRE&" \
             "qform=AST&arxiv_sel=astro-ph&arxiv_sel=cond-mat&arxiv_sel=cs&arxiv_sel=gr-qc&" \
             "arxiv_sel=hep-ex&arxiv_sel=hep-lat&arxiv_sel=hep-ph&arxiv_sel=" \
             "hep-th&arxiv_sel=math&arxiv_sel=math-ph&" \
             "arxiv_sel=nlin&arxiv_sel=nucl-ex&arxiv_sel=nucl-th&arxiv_sel=physics" \
             "&arxiv_sel=quant-ph&arxiv_sel=q-bio&sim_query=YES&ned_query=YES&adsobj_query=YES&" \
             "aut_logic=OR&obj_logic=OR&" \
             "author="+author.strip()+"&" \
             "object=&start_mon=&" \
             "start_year="+str(yearstart).strip()+"&" \
             "end_mon=&" \
             "end_year="+str(yearend).strip()+"&" \
             "ttl_logic=OR&" \
             "title=&txt_logic=OR&text=&" \
             "nr_to_return="+str(numret).strip()+"&" \
             "start_nr=1&jou_pick=NO&ref_stems=&data_and=ALL&group_and=ALL&start_entry_day=&" \
             "start_entry_mon=&start_entry_year=&end_entry_day=&end_entry_mon=&end_entry_year=&" \
             "min_score=&sort=SCORE&data_type=SHORT&aut_syn=YES&ttl_syn=YES&txt_syn=YES&aut_wt=1.0&" \
             "obj_wt=1.0&ttl_wt=0.3&txt_wt=3.0&aut_wgt=YES&obj_wgt=YES&ttl_wgt=YES&txt_wgt=YES&ttl_sco=YES&" \
             "txt_sco=YES&version=1"
    """
    adsurl = "http://adsabs.harvard.edu/cgi-bin/nph-abs_connect?db_key=AST&db_key=PRE" \
             "&qform=AST&arxiv_sel=astro-ph&arxiv_sel=cond-mat&arxiv_sel=cs&arxiv_sel=gr-qc&arxiv_sel=hep-ex&"\
             "arxiv_sel=hep-lat&arxiv_sel=hep-ph&arxiv_sel=hep-th&arxiv_sel=math&arxiv_sel=math-ph&" \
             "arxiv_sel=nlin&arxiv_sel=nucl-ex&arxiv_sel=nucl-th&arxiv_sel=physics&"\
             "arxiv_sel=quant-ph&arxiv_sel=q-bio&sim_query=YES&ned_query=YES&adsobj_query=YES&aut_logic=OR&"\
             "obj_logic=OR&" \
             "author="+author.strip()+"&" \
             "start_mon=&" \
             "start_year="+str(yearstart).strip()+"&" \
             "end_mon=&" \
             "end_year="+str(yearend).strip()+"&" \
             "ttl_logic=OR&title=&txt_logic=OR&text=&nr_to_return=200&start_nr=1&jou_pick=NO&ref_stems=&" \
             "data_and=ALL&group_and=ALL&start_entry_day=&start_entry_mon=&start_entry_year=&" \
             "end_entry_day=&end_entry_mon=&end_entry_year=&min_score=&sort=SCORE&data_type=SHORT&aut_req=YES&" \
             "ttl_req=YES&aut_syn=YES&ttl_syn=YES&txt_syn=YES&aut_wt=1.0&obj_wt=1.0&ttl_wt=1.0&txt_wt=3.0&" \
             "aut_wgt=YES&obj_wgt=YES&ttl_wgt=YES&txt_wgt=YES&ttl_sco=YES&txt_sco=YES&version=1"
    return adsurl

def get_bibcodes(adsurl):
    """
    for a given adsurl for a specified author (and start and end years),
    return the bibcode urls associated with his/her publications

    @param adsurl:
    @return:
    """
    print "Generating ADSURL"
    try:
        website = urllib2.urlopen(adsurl)
    except urllib2.HTTPError, e:
        print "Cannot retrieve URL: HTTP Error Code", e.code
    except urllib2.URLError, e:
        print "Cannot retrieve URL: " + e.reason[1]
    adshtml = website.read()
    soup = BeautifulSoup(''.join(adshtml)) # this returns the page listing the authors publications
    bibc = list() # create empty list to store the bibcodes
    bibcode = list()
    for link in soup.findAll('a'):
        href = link.get('href')
        if href:
            if "bibcode" in href:
                bc = href.split("&link_type")[0]  # returns the bibcode url
                bibc.append(bc)
    bibc = set(bibc) # get unique bibcodes
    bibc = list(bibc) # convert set to list
    for b in bibc:
        bibcode.append(b+"&link_type=ABSTRACT")
    return bibcode

def parse_bibcode(name,bibcode,maxauthors=10):
    """
    for an author name and a given bibcode, return the title of the paper from ads along with
    a dictionary giving co-authors and their institutes of the form {'Corcoran':'USRA', "GULL":'NASA/GSFC'} etc
    @param name:
    @param bibcode:
    @param title:
    @param coauthors:
    @param institutes:
    @return:
    """
    #print "Parsing Bibcodes..."
    lname = name.split(',')[0].strip().lower()
    fi = name.split(',')[1].strip().lower()[0]
    try:
        website = urllib2.urlopen(bibcode)
    except urllib2.HTTPError, e:
        print "Cannot retrieve URL: HTTP Error Code", e.code
    except urllib2.URLError, e:
        print "Cannot retrieve URL: " + e.reason[1]
    pubhtml = website.read()
    soup = BeautifulSoup(''.join(pubhtml)) # this returns the webpage for a given bibcode as a soup object
    rows=soup.findAll('tr')
    title=''
    authors=''
    affil=''
    country = list()
    affiliation = list()
    for row in rows:
        if "Title:" in str(row):
            title = row.getText()
            title=unicodedata.normalize('NFKD', unescape(title)).encode('ascii','ignore') # converts html special characters
        if "Authors:" in str(row):
            #auth = str(row.getText()).replace("&#160;"," ").replace("&#233;", "e").replace("&#252;","ue").replace("&#237;","i").replace("&#225;","a")
            auth = row.getText()
            auth=unicodedata.normalize('NFKD', unescape(auth)).encode('ascii','ignore') # converts html special characters
        if "Affiliation:" in str(row):
            #affil=str(row.getText()).replace("&#160;"," ").replace("&#233;", "e").replace("&#252;","ue").replace("&#237;","i").replace("&#225;","a")
            affil = row.getText()
            affil = unicodedata.normalize('NFKD', unescape(affil)).encode('ascii', 'ignore') # converts html special
    title = title.split("Title:")[1] # get rid of Title: tag
    try:
        authors = auth.split('Authors:')[1] # get rid of Authors: tag
        authors = authors.split(";") # create list of authors
        i = -1
        for a in authors: # find index of name in list
            i += 1
            if ',' in a:
                authlname = a.split(',')[0].strip().lower()
                authfi = a.split(',')[1].strip().lower()[0]
                if (authlname == lname and authfi == fi):
                    selfnameindex=i
    except:
        authors="Problem with parsing Authors"
    if len(authors)>maxauthors:
        authors = authors[0:maxauthors]
    if affil:
        try:
            affil = affil.split("Affiliation:")[1] # get rid of Affiliation: tag
        except:
            pass
    else:
        affil='AA('
    affil.replace("&#232;","e")
    afsep = ['AA(','), AB(','), AC(','), AD(','), AE(','), AF(','), AG(','), AH(','), AI(',
             'AJ(','AK(','AL(','AM(','AN(','AO(',
             'AP(','AQ(','AR(','AS(','AT(','AU(','AV(','AW(','AX(','AY(','AZ('] # affiliation separators; max of 8
    ii=0
    affil = affil.split(afsep[ii])[1] # remove up to AA(
    for i in range(1,len(authors)):
        af = affil.split(afsep[i])
        aff = af[0]
        if "document.write" in aff:
            aff = aff.split("document.write")[0]
        afa = aff.rsplit(",",1)
        if len(afa[0].strip())>0:
            affiliation.append(afa[0])
        else:
            affiliation.append("")
        try:
            country.append(afa[1])
        except IndexError:
            country.append('')
        try:
            affil = af[1]
        except IndexError:
            pass
        ii=i
    if afsep[ii+1] in affil:
        aff=affil.split(afsep[i+1])[0]
    else:
        aff=affil
    afa=aff.rsplit(",",1)
    if not afa[0]: # if afa[0] is empty
        afa=['','']
    affiliation.append(afa[0])
    try:
        country.append(afa[1])
    except:
        print "Country not found in affiliation "+afa[0]
        country.append(' ')
    # remove self from authorlist
    del authors[selfnameindex]
    del affiliation[selfnameindex]
    return title, authors, affiliation, country

def ads2uename(adsname):
    """
    takes a name string of the form 'lastname, fi. mi.' required by ADS
    and reformats to 'fi. mi. lastname' needed for UE report
    @param lname:
    @param fname:
    @return:
    """
    lname=adsname.split(",")[0].capitalize()
    try:
        initials = adsname.split(",")[1].strip().upper()
    except IndexError:
        initials=' '
    uename = initials + ' ' + lname
    return uename

def ads2ue(name, yearstart=2013, yearend=2014):
    """
    for a given scientist name and year range,
    takes the output of an ads search and creates a report compatible with the USRA
    University engagement report
    name should be a string of the form corcoran, m. f.
    Returns title, authors, affils for given scientist name for the year range
    @rtype : basestring
    @param name: name in ADS format (Lastname, First initial, middle initial)
    @param yearstart: beginning year for the ADS query
    @param yearend: end year for the ADS query
    @return:
    """
    title=''
    authors=''
    affils=''
    adsurl = mkadsurl(name,yearstart=yearstart,yearend=yearend)
    bibcodes = get_bibcodes(adsurl)
    print "%15s  %15s  %s %4s %4s %s" % ("USRA Lead","Contact","Organization","Start","End","Topic")
    maxauthors=20
    for b in bibcodes:
        print "\nFound %s" % b
        title, authors, affils, country = parse_bibcode(name, b, maxauthors=maxauthors)
        lname=name.split(',')[0].strip() # get last name of USRA scientist
        try:
            lname_index = [i for i, s in enumerate(authors) if lname.lower() in s.lower()][0]
            if (('Goddard'.lower() or 'GSFC'.lower()) or ('USRA'.lower() or 'Universities Space Research Association'.lower())) in affils[lname_index ].lower():
                for i in range(len(authors)):
                    print "%15s | %15s | %40s | %10s | %4i | %4i | %s" % (ads2uename(name), ads2uename(authors[i].strip()),affils[i].strip(),
                                                                country[i].strip(), yearstart, yearend, title.strip())
            else: # non-relevant bibcode since name is not associated with USRA or GSFC
                title=''
                authors=''
                affils=''
        except IndexError:
            print ('{0} is not in first {1} authors').format(name, maxauthors)
            title = ''
            authors = ''
            affils = ''
    return title, authors, affils


if __name__=="__main__":
    names=['drake, s. a.',
           'corcoran, m. f.',
           'arzoumanian, z.',
           'soong, y.',
           'shrader, c.',
           'mattson, b.',
           'link, j.',
           'nowicki, s.',
           'krizmanic, j.',
           'krimm, h.']
    #name='drake, s. a.'
    #for name in names:
    #    ads2ue(name)
    """
    bibcode = 'http://adsabs.harvard.edu/abs/2014SPIE.9144E..20A'
    name='arzoumanian, z.'
    yearstart = 2013
    yearend = 2014
    title, authors, affils, country = parse_bibcode(name, bibcode, maxauthors=25)
    for i in range(len(authors)):
        print "%15s | %15s | %40s | %10s | %4i | %4i | %s" % (
            ads2uename(name), 'Dr. '+ads2uename(authors[i].strip()).strip(), affils[i].strip(),
            country[i].strip(), yearstart, yearend, title.strip())
    """
    title, authors, affils = ads2ue('Corcoran, M.',yearstart=2014, yearend=2015)



