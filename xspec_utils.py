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
    try:
        xcm.append('back ' + spectrum.background.fileName)
    except:
        pass
    xcm.append('resp ' + spectrum.response.rmf)
    try:
        xcm.append('arf '+spectrum.response.arf)
    except:
        pass
    xcm.append('ignore '+spectrum.ignoredString())
    if model:
        mo_xcm_list = write_xcm_model(xcmfile+'_mo.xcm',model)
        for m in mo_xcm_list:
            xcm.append(m)
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

def write_xcm_model(savefile, model, pyxspec = False):
    """
    The writes a model instance from pyxspe as an xspec 12 model command file
    or as a pyxspec- formatted command (need to develop a reader for
    pyxspec-formatted model file!)
    :param model: pyxspec model instance
    :param savefile: Name of xcm file to write to
    :param pyxspec: if False, saves to old-style xspec format
    :return:
    """
    with open(savefile, mode='wt') as mofile:
        mo_xcm_list=["model {0}".format(model.expression)]
        mofile.write("model {0}".format(model.expression))
        mofile.write("\n")
        if pyxspec:
            for c in model.componentNames:
                #print "component = {0}".format(c)
                for p in model.__getattribute__(c).parameterNames:
                    #print "Values of Parameter {0}".format(p)
                    val= model.__getattribute__(c).__getattribute__(p).values
                    mofile.write("model.{0}.{1}.values = {2}".format(c,p,val))
        else:
            for c in model.componentNames:
                #print "component = {0}".format(c)
                for p in model.__getattribute__(c).parameterNames:
                    #print "Values of Parameter {0}".format(p)
                    val= model.__getattribute__(c).__getattribute__(p).values
                    v = [str(x) for x in val]
                    mofile.write(','.join(v))
                    mo_xcm_list.append(','.join(v))
                    mofile.write("\n")
        mofile.close()
    return mo_xcm_list




if __name__== "__main__":
    xcmo = '/Users/corcoran/research/ETA_CAR/CHANDRA2/repro/seqid/200810/10787/work/meg-1_mo.xcm'
    mo = read_model_xcm(xcmo)
    mo.show()