__author__ = 'corcoran'


def read_model_xcm(xcmo):
    """
    This function reads a model file created wiht the xspec "save model <filename>" command
    and returns a pyxspec model object
    @param xcmo_file:
    @return:
    """
    import xspec
    import numpy as np
    par = []
    modelfound = False
    with open(xcmo) as file:
        for line in file:
            # print line
            if 'model' in line:
                xspecmodel = xspec.Model(line[5:].strip())
                modelfound = True
            if modelfound:
                par.append(line.strip('\n').strip())
    par = par[1:]
    for i in np.arange(len(par)) + 1:
        xspecmodel(i).values = par[i - 1]
    xspecmodel.show()
    return xspecmodel


if __name__== "__main__":
    xcmo = '/Users/corcoran/research/ETA_CAR/CHANDRA2/repro/seqid/200810/10787/work/meg-1_mo.xcm'
    mo = read_model_xcm(xcmo)
    mo.show()
