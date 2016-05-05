#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#    iflist version 0.7 - File List Expansion Utility
#    Copyright (c) 2015 Avner Herskovits
#
#    For documentation please refer to the accompanying README.md file.
#
#    MIT License
#
#    Permission  is  hereby granted, free of charge, to any person  obtaining  a
#    copy of this  software and associated documentation files (the "Software"),
#    to deal in the Software  without  restriction, including without limitation
#    the rights to use, copy, modify, merge,  publish,  distribute,  sublicense,
#    and/or  sell  copies of  the  Software,  and to permit persons to whom  the
#    Software is furnished to do so, subject to the following conditions:
#
#    The above copyright notice and this  permission notice shall be included in
#    all copies or substantial portions of the Software.
#
#    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT  WARRANTY OF ANY KIND, EXPRESS OR
#    IMPLIED, INCLUDING BUT NOT LIMITED TO THE  WARRANTIES  OF  MERCHANTABILITY,
#    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR  ANY  CLAIM,  DAMAGES  OR  OTHER
#    LIABILITY, WHETHER IN AN  ACTION  OF  CONTRACT,  TORT OR OTHERWISE, ARISING
#    FROM,  OUT  OF  OR  IN  CONNECTION WITH THE SOFTWARE OR THE  USE  OR  OTHER
#    DEALINGS IN THE SOFTWARE.
#

from glob import iglob
from os. path import abspath, dirname, expanduser, expandvars, isdir, isfile, join, normpath, realpath
from os import altsep as ALTSEP, listdir, sep as SEP

COMMENT = '#'
REF = '@'

def _yielder( filename, path, recurse ):
    if recurse and isdir( filename ):
        for next_file in listdir( filename ):
            yield from iflist( join( filename, next_file ), path, recurse )
    else:
        yield abspath( filename )

def iflist( files, path = [], recurse = False ):
    if type( files ) is list:
        for file in files:
            yield from iflist( file, path, recurse )
        raise StopIteration
    file = str( files )
    if '' == file:
        raise StopIteration
    if REF == file[ 0 ]:
        _file = expandvars( expanduser( file[ 1: ]))
        with open( _file, "r", encoding = "utf-8" ) as f:
            for gross_line in f:
                line = gross_line. strip( '\n\r' ). split( ' ' + COMMENT, 1 )[ 0 ]. strip()
                if not len( line ) or COMMENT == line[ 0 ]:
                    continue
                at = ''
                if REF == line[ 0 ]:
                    at = REF
                    line = line[ 1: ]
                next_file = normpath( join( dirname( realpath( _file )), expandvars( expanduser( line ))))
                yield from iflist( at + next_file, path, recurse )
    else:
        found = False
        _file = expandvars( expanduser(  file ))
        for i in iglob( _file ):
            found = True
            yield from _yielder( i, path, recurse )
        if not found and SEP not in _file and ALTSEP is not None and ALTSEP not in _file:
            for i in ( j for p in path for j in iglob( join( p, _file ))):
                yield from _yielder( i, path, recurse )

def flist( files, path = [], recurse = False, cb = None ):
    result = []
    def _cb( filename ):
        if filename not in result:
            result. append( filename )
    if cb is None:
        cb = _cb
    for i in iflist( files, path, recurse ):
        cb( i )
    return result

def _usage():
    print( 'Usage: [options] iflist <filename> [...<filename>...]' )
    print()
    print( 'Options:' )
    print( "-h  Print this help message." )
    print( "-i  Use an iterator. Runs faster on larger lists, but may return duplicates." )
    print( "-r  Recurse into directories." )
    print( "-n  Don't use a path. Default path is sys.path." )
    print( "-p <path> Specify a path as a directory list sepearted by commas or semicolons." )

def main():
    from sys import argv, path
    counter = 1
    _search = []
    _path = path
    _recurse = False
    _worker = flist
    while counter < len( argv ):
        if len( argv[ counter ]) and '-' == argv[ counter ][ 0 ]:
            if 2 != len( argv[ counter ]):
                print( 'ERROR: Unknown option ' + argv[ counter ])
                _usage()
                exit( 1 )
            elif 'h' == argv[ counter ][ 1 ]:
                _usage()
                exit( 0 )
            elif 'i' == argv[ counter ][ 1 ]:
                _worker = iflist
            elif 'r' == argv[ counter ][ 1 ]:
                _recurse = True
            elif 'n' == argv[ counter ][ 1 ]:
                _path = []
            elif 'p' == argv[ counter ][ 1 ]:
                counter += 1
                if len( argv ) == counter:
                    print( 'ERROR: Path not provided' )
                    _usage()
                    exit( 1 )
                _path = argv[ counter ]. split( ';,' )
            else:
                print( 'ERROR: Unknown option ' + argv[ counter ])
                _usage()
                exit( 1 )
        else:
            _search. append( argv[ counter ])
        counter += 1
    if 0 == len( _search ):
        print( 'ERROR: Nothing to search' )
        _usage()
        exit( 1 )
    for i in _worker( _search, _path, _recurse ):
        print( '"' + i + '"', end = ' ' )

if '__main__' == __name__:
    main()
