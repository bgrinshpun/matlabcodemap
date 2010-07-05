'''
depmap.py      Author: Boris Grinshpun

This script finds the dependency structure of MATLAB .m-files
within a directory and prints the results. Additionally,
it prints out the line number and text of any MATLAB
comments containing the word "important".

copyright (c) 2010 Boris Grinshpun <bgrinshpun@gmail.com>
distributed under GPL 3.0: http://www.gnu.org/licenses/gpl.txt

'''

from os import path, listdir, getcwd # to list directory contents
import sys # for system-specific params and arguments
from depsearch import * # module containing functions for finding
                        # dependency structure

pathslist=list()

if len(sys.argv)>2:
    raise BaseException("too many arguments")
elif len(sys.argv)==1:
    pathslist.append(getcwd())
else:
    pathslist.append(sys.argv[1])

# list directory contents
files = listdir(pathslist[0])

# list subdirectory contents
for nextpath in pathslist:
    for item in listdir(nextpath):
        trypath = nextpath + '\\' + item
        if path.isdir(trypath):
            files = files + listdir(trypath)
            pathslist.append(trypath)

# remove non m-files and .m extension
ffiles = [item[:-2] for item in files if item.lower().endswith('.m')]


# read each file, find IMPORTANT lines and dependencies
keyword = 'important'

depdict=dict()
for name in ffiles:
    fname = name + '.m'
    pfun=file_read(fname,pathslist) # read file
    linehits = search_text(pfun,keyword) # find desired lines
    deptree = getdep(pfun,ffiles) # find dependency structure
    depdict[fname]=[linehits, deptree] # create dictionary

# display results
for name in ffiles:
    fname=name+'.m'
    print fname + ':'
    # display important lines
    for line in depdict[fname][0]:
        print 'line ' +str(line[1]) +': '+ str(line[0])
    else:
        print 'no lines found'
    # display dependencies
    if len(depdict[fname][1])>0:
        print 'dependent functions:' + str(depdict[fname][1]) + '\n-----\n'
    else:
        print 'no dependent functions found\n-----\n'
