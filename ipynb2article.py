# Convert IPYthon notebook to LaTeX for ApJ or A&A
import json
import re

import sys
import getopt

def isstartmarker(cell, start):
    if 'source' in cell.keys():
        return cell['source'] == [start]
    elif 'input' in cell.keys():
        return cell['input'] == [start]
    else:
        raise ValueError('Type of cell not recognized.')

class IgnoreConverter(object):
    '''Use this converter for cell types that should be ignored'''
    def __call__(self, cell):
        return []

class LiteralSourceConverter(object):
    '''This converter return the literal ``source`` entry of a cell.'''
    def __call__(self, cell):
        text = cell['source']
        text[-1] +='\n'
        return text

class MarkedCodeOutputConverter(object):
    '''Add output of code cells that have a specific string in the code cell'''
    def __init__(self, marker):
        '''Add output of code cells that have a specific string in the code cell

        Parameters
        ----------
        marker : string
         Convert the output of a code cell if and only if one line in the
         code matches ``marker``.
         I often use ``marker='# output->LaTeX'`` to mark cells whose
         output I want.
        '''
        self.marker = marker
    def __call__(self, cell):
        text = []
        if (self.marker in cell['input']) or (self.marker+'\n' in cell['input']):
            for out in cell['outputs']:
                if 'text' in out:
                    text.extend(out['text'])

        if len(text) > 0:
            text[-1] +='\n'
        return text

class LatexHeadingConverter(object):
    '''Convert headings in notebook to appropriate level in LaTeX'''
    def __init__(self, latexlevels=['chapter','section','subsection', 'subsubsection', 'paragraph', 'subparagraph']):
        '''Convert headings in notebook to appropriate level in LaTeX

        Parameters
        ----------
        latexlevels : list of 6 strings
         Latex equivalents for 'Heading 1', 'Heading 2' etc.
        '''
        self.latexlevels = latexlevels
    def __call__(self, cell):
        # Just to be careful for multi-line headings
        title = ''.join(cell['source'])
        line1 = '\\{0}{{{1}}}\n'.format(self.latexlevels[cell['level']-1],
                                        title)
        cleantitle = re.sub(r'\W+', '', title)
        line2 = '\\label{{sect:{0}}}\n'.format(cleantitle.lower())
        return ['\n','\n', line1, line2, '\n']

class NotebookConverter(object):
    cellconverters = {
        'code' : MarkedCodeOutputConverter('# output->LaTeX'),
        'heading': LatexHeadingConverter(),
        'markdown': LiteralSourceConverter(),
        'raw': LiteralSourceConverter()
    }
    def convert(self, infile, outfile, start = 0, file_before=None, file_after=None):
        '''Convert IPython notebook to LaTeX file

        Parameters
        ----------
        infile : string
         filename of IPython notebook
        outfile : string
         filename of Latex file to be written
        start : int or string
         If this is a number, skip that many cells starting from the top;
         if it is a string, skip cells until a cell has *exactly* the
         content that ``start`` has.
        file_before : string
        file_after: string
         String with filename. These files are copied above and below
         the content from the ipynb file. Use this e.g. for templates
         that contain the LaTeX header info that does not appear in the
         notebook.
        '''
        with open(infile, 'r') as f:
            print 'Parsing ', infile
            ipynb = json.load(f)

        cells = ipynb['worksheets'][0]['cells']
        if isinstance(start, basestring):
            while not isstartmarker(cells[0], start):
                discard = cells.pop(0)
            discard = cells.pop(0) # pop the marker cell
        else:
            for i in range(start):
                discard = cells.pop(0)

        with open(outfile, 'w') as out:
            print 'Writing ', outfile
            if file_before is not None:
                with open(file_before, 'r') as f:
                    for line in f:
                        out.write(line)
            for cell in cells:
                lines = self.cellconverters[cell['cell_type']](cell)
                for line in lines:
                    out.write(line)
            if file_after is not None:
                with open(file_after, 'r') as f:
                    for line in f:
                        out.write(line)


if __name__ == '__main__':
    converter = NotebookConverter()
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h", ["help"])
    except getopt.GetoptError:
        print converter.convert.__doc__
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print converter.convert.__doc__
            sys.exit()

    print args
    converter.convert(*args)

