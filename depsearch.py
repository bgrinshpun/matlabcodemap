'''
depsearch.py      Author: Boris Grinshpun

Module containing functions used in depfun.py

copyright (c) 2010 Boris Grinshpun <bgrinshpun@gmail.com>
distributed under GPL 3.0: http://www.gnu.org/licenses/gpl.txt

'''

from os import path # to look at directories
from re import sub, escape, search # to search for regex
from string import replace # to replace all occurences of a substring
                            # with another string
                            
def file_read(fname, dirs):
    '''
    Inputs:
        fname: name of .m file
        plist: list of available directories and subdirectories

    Outputs:
        parsedfun: list with each line of code as a separate element

    Opens a file and returns list containing each line of the file

    '''
    for item in dirs:
        fpath = item+'\\' + fname
        if path.exists(fpath):
            # open and read file
            in_file=open(fpath,'r')
            fun=in_file.read()
            in_file.close()
            fun = fun.split('\n') # parses by line
            parsedfun=zip(fun,range(1,len(fun)+1)) # includes line numbers 
            return parsedfun


def search_text(textlst,searchword):
    '''
    Inputs:
        textlst: list containing lines of text to be searched
        searchword: word to be found

    Outputs:
        linehits: list of lines containing searchword

    Looks through lines of textlst which are comments and searches
    for an instance of the search word

    '''
    # finds lines containing search words
    linehits=[]
    for line in textlst:
        line=list(line)
        line[0]=line[0].lower()
        if search(r'%.+' + r'\b'+escape(searchword)+r'\b',line[0]): # regex search
            line[0]=sub(r'\b'+escape(searchword)+r'\b',searchword.upper(),line[0]) # capitalize search word
            line=tuple(line)
            linehits.append(line)
    return linehits

def getdep(textlst,files):
    '''
    Inputs:
        textlst: list containing lines of text to be searched
        files: all relevant files

    Outputs:
        deptree: list of dependent files

    Scans text of a file to look for dependent files

    '''
    allwords=[]
    for line in textlst:
        txt=line[0]
        if search('%',txt): # check for comments
            txt = txt[:txt.index('%')] # remove comments
        elif search('function',txt):
            txt=txt[:txt.index('function')] # remove function itself
        txt = sub(r'\W',' ',  txt) # remove non-alphanumeric chars
                                            #excluding underscore
        allwords.extend(txt.split(' ')) # build tokens
        allwords = list(set(allwords)) # remove duplicates
        
    deptree=[];
    # build tree
    for item in files:
        for word in allwords:
            if item.lower() == word.lower():
                deptree.append(word)
    return deptree
