def get_simbad_mag(star_id, band='V', simsite='simbad.cfa.harvard.edu', quiet=True):
    """
    for an input star_id (say HD193793), returns the magnitude from Simbad in the specified band
    @param: star_id = SIMBAD recognized identifier of the star
    @param: band = filter band for desired magnitude (Default = V)
    @param: simsite = simbad site to use (Default = simbad.cfa.harvard.edu,
    or use simbad.u-strasbg.fr)
    @param quiet = if False, prints out a re-assuring message
    :return
    """
    import requests
    from bs4 import BeautifulSoup
    import re
    simurl = 'http://'+simsite+'/simbad/sim-id?Ident='+str(star_id)+'&NbIdent=1&Radius=2&Radius.unit=arcmin&submit=submit+id'
    starsim= requests.get(simurl)
    starsoup = BeautifulSoup(starsim.text,'lxml')
    flux = float('nan')
    try:
        fluxtab=starsoup.find_all('table')[4] # the fourth table on the page has the fluxes in various bands
    except IndexError:
        print "Could not find information for {0}".format(star_id)
        return
    for t in fluxtab.find_all('tt'): # rather tortured method to find the flux but it works in 1 case at least
        if band.strip() in t.text:
            a= t.text.split(' ')
            for b in a:
                if len(b.strip()) > 0:
                    if re.match('^\d\.\d',b.strip()): # this matches a digit followed by a '.' then another digit
                        #print b.replace(" ","")+' match'
                        flux = float(b.replace(" ",""))
    if not quiet:
        print "Mag of {0} is {1}".format(star_id, get_simbad_mag(star_id))
    return flux

def get_simbad_pos(star_id, coordsys='ICRS', simsite='simbad.cfa.harvard.edu', quiet=True):
    """
    for an input star_id (say HD193793), returns the position (currently only supports ICRS RA & Dec in
    sexigesimal) from Simbad
    @param: star_id = SIMBAD recognized identifier of the star
    @param: coordsys = coordinate system (Default = 'ICRS')
    @param: simsite = simbad site to use (Default = simbad.cfa.harvard.edu,
    or use simbad.u-strasbg.fr)
    @param quiet = if False, prints out a re-assuring message
    :return
    """
    import requests
    from bs4 import BeautifulSoup
    import re
    simurl = 'http://'+simsite+'/simbad/sim-id?Ident='+str(star_id)+'&NbIdent=1&Radius=2&Radius.unit=arcmin&submit=submit+id'
    try:
        starsim= requests.get(simurl)
    except Exception, errmsg:
        print errmsg
        return
    starsoup = BeautifulSoup(starsim.text,'lxml')
    if coordsys.strip().upper() <> "ICRS":
        print "Specified Coordinate system {0} not available".format(coordsys)
        print "Returning"
        return
    else:
        posname1 = 'RA'
        posname2 = 'Dec'
    try:
        postab=starsoup.find_all('table')[3] # the third table on the page has the fluxes in various bands
    except IndexError:
        print "\nCould not find information for name = {0}".format(star_id)
        return
    # 3rd table should have the position info
    td = postab.find_all('td')
    # 6th table within table group has the ICRS position
    pos = td[6].text.split('\n')[2].split(" ")
    pos = [float(x) for x in pos]
    starpos ={posname1:pos[0:3], posname2:pos[3:6]}
    if not quiet:
        print "\nPosition of {0} is {1} = {2}, {3} = {4}".format(star_id,
                                                               starpos.keys()[0],
                                                               starpos[starpos.keys()[0]],
                                                               starpos.keys()[1],
                                                               starpos[starpos.keys()[1]])
    return starpos

if __name__ == "__main__":
    starid ="HD 193793"
    #starid = 'nose'
    starpos = get_simbad_pos(starid, quiet=False)