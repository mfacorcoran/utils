#!/usr/bin/env python
import fileinput
import locale
from contextlib import closing
from unidecode import unidecode # $ pip install unidecode

def toascii(files=None, encoding=None, bufsize=-1):
    if encoding is None:
        encoding = locale.getpreferredencoding(False)
    with closing(fileinput.FileInput(files=files, bufsize=bufsize)) as file:
        for line in file:
            print unidecode(line.decode(encoding)),

if __name__ == "__main__":
    import sys
    toascii(encoding=sys.argv.pop(1) if len(sys.argv) > 1 else None)