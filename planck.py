__author__ = 'corcoran'

def planck(T, wave):
    #
    # input wavelength in Angstrom, T in K
    #
    from astropy import constants as const
    from astropy import units as u
    try:
        wave.unit
     except AttributeError:
        print 'Must specify Units of wave in Angstrom using astropy.units'
        return 0
    try:
        T.unit
    except AttributeError:
        print 'Must specify Units of T in K using astropy.units'
        return 0
    if wave.unit <> "Angstrom":
        wave.to(u.Angstrom)
    if T.unit <> "K":
        T.to(u.K)
    """
    convert wave from Angstroms to meters
    """
    wave=wave.to(u.m)
    b = 2.0*const.h*const.c**2/wave**5*(exp(1.0/((const.h*const.c/wave/const.k_B/T).value))-1.0)
    return b