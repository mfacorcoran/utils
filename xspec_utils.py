__author__ = 'corcoran'

import xspec
import numpy as np
import os


def read_model_xcm(xcmo, chatter=True):
    """
    This function reads a model file created wiht the xspec "save model <filename>" command
    and returns a pyxspec model object
    @param xcmo:
    @return:
    """
    par = []
    modelfound = False
    with open(xcmo) as file:
        for line in file:
            # print line
            if 'model' in line:
                if chatter:
                    print "model is {0}".format(line[5:].strip())
                xspecmodel = xspec.Model(line[5:].strip())
                modelfound = True
            if modelfound:
                par.append(line.strip('\n').strip())
    if modelfound:
        par = par[1:]
        for i in np.arange(len(par)) + 1:
            xspecmodel(i).values = par[i - 1]
        xspecmodel.show()
    else:
        xspecmodel = 0
    return xspecmodel


def write_xcm(xcmfile, spectrum, model=None):
    """
    This function takes a spectrum object and (optionally) a model object and writes out a xspec12 command file
    @param xcmfile: output filename
    @param spectrum: source spectrum object from pyxspec
    @param model: pyxspec model object
    @return:
    """
    xcm=['data '+spectrum.fileName]
    xcm.append('back '+spectrum.background)
    xcm.append('resp '+spectrum.response.rmf)
    xcm.append('arf '+spectrum.response.arf)
    xcm.append('ignore '+spectrum.ignoredString())
    if model:
        xcm.append('model ' + model.expression)
        for i in np.arange(model.nParameters) + 1:
            p = model(i).values
            parvals = str(p[0])
            for k in np.arange(len(p) - 1) + 1:
                parvals = parvals + ', ' + str(p[k])
            xcm.append(parvals)
        xcm.append('statistic ' + xspec.Fit.statMethod)
    if os.path.isfile(xcmfile):
        print "%s exists" % xcmfile
        ans = raw_input('Overwrite [y/n]? ')
        if ans.strip().lower() == 'n':
            print "%s not overwritten; Returning" % xcmfile
            return
    print "Writing File %s" % xcmfile
    f = open(xcmfile, 'w')
    for i in xcm:
        f.write(i + "\n")
    f.close()
    return


if __name__== "__main__":
    xcmo = '/Users/corcoran/research/ETA_CAR/CHANDRA2/repro/seqid/200810/10787/work/meg-1_mo.xcm'
    mo = read_model_xcm(xcmo)
    mo.show()