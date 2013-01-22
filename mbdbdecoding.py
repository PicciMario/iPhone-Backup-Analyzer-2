'''
 Analyzer for iPhone backup made by Apple iTunes

 (C)opyright 2010 Mario Piccinelli <mario.piccinelli@gmail.com>
 Released under MIT licence

 Functions to decode MBDB and MBDX files have been derived from the work of:
 - David Drysdale <dmd@lurklurk.org>
 - Markus Stenberg <fingon@iki.fi>
 - http://code.google.com/p/iphonebackupbrowser/
 
'''

#!/usr/bin/env python
import sys

def getint(data, offset, intsize):
    """Retrieve an integer (big-endian) and new offset from the current offset"""
    value = 0
    while intsize > 0:
        value = (value<<8) + ord(data[offset])
        offset = offset + 1
        intsize = intsize - 1
    return value, offset

def getstring(data, offset):
    """Retrieve a string and new offset from the current offset into the data"""
    if data[offset] == chr(0xFF) and data[offset+1] == chr(0xFF):
        return '', offset+2 # Blank string
    length, offset = getint(data, offset, 2) # 2-byte length
    value = data[offset:offset+length]
    return value, (offset + length)

def process_mbdb_file(filename):
    mbdb = {} # Map offset of info in this file => file info
    data = open(filename, 'rb').read()
    if data[0:4] != "mbdb": raise Exception("This does not look like an MBDB file")
    offset = 4
    offset = offset + 2 # value x05 x00, not sure what this is
    while offset < len(data):
        fileinfo = {}
        fileinfo['start_offset'] = offset
        fileinfo['domain'], offset = getstring(data, offset)
        fileinfo['filename'], offset = getstring(data, offset)
        fileinfo['linktarget'], offset = getstring(data, offset)
        fileinfo['datahash'], offset = getstring(data, offset)
        fileinfo['unknown1'], offset = getstring(data, offset)
        fileinfo['mode'], offset = getint(data, offset, 2)
        fileinfo['unknown2'], offset = getint(data, offset, 4)
        fileinfo['unknown3'], offset = getint(data, offset, 4)
        fileinfo['userid'], offset = getint(data, offset, 4)
        fileinfo['groupid'], offset = getint(data, offset, 4)
        fileinfo['mtime'], offset = getint(data, offset, 4)
        fileinfo['atime'], offset = getint(data, offset, 4)
        fileinfo['ctime'], offset = getint(data, offset, 4)
        fileinfo['filelen'], offset = getint(data, offset, 8)
        fileinfo['flag'], offset = getint(data, offset, 1)
        fileinfo['numprops'], offset = getint(data, offset, 1)
        fileinfo['properties'] = {}
        for ii in range(fileinfo['numprops']):
            propname, offset = getstring(data, offset)
            propval, offset = getstring(data, offset)
            fileinfo['properties'][propname] = propval
        mbdb[fileinfo['start_offset']] = fileinfo
    return mbdb

def process_mbdx_file(filename):
    mbdx = {} # Map offset of info in the MBDB file => fileID string
    data = open(filename).read()
    if data[0:4] != "mbdx": raise Exception("This does not look like an MBDX file")
    offset = 4
    offset = offset + 2 # value 0x02 0x00, not sure what this is
    filecount, offset = getint(data, offset, 4) # 4-byte count of records 
    while offset < len(data):
        # 26 byte record, made up of ...
        fileID = data[offset:offset+20] # 20 bytes of fileID
        fileID_string = ''.join(['%02x' % ord(b) for b in fileID])
        offset = offset + 20
        mbdb_offset, offset = getint(data, offset, 4) # 4-byte offset field
        mbdb_offset = mbdb_offset + 6 # Add 6 to get past prolog
        mode, offset = getint(data, offset, 2) # 2-byte mode field
        mbdx[mbdb_offset] = fileID_string
    return mbdx

def modestr(val):
    def mode(val):
        if (val & 0x4): r = 'r'
        else: r = '-'
        if (val & 0x2): w = 'w'
        else: w = '-'
        if (val & 0x1): x = 'x'
        else: x = '-'
        return r+w+x
    return mode(val>>6) + mode((val>>3)) + mode(val)

def fileinfo_str(f, verbose=False):
    if not verbose: return "(%s)%s::%s" % (f['fileID'], f['domain'], f['filename'])
    if (f['mode'] & 0xE000) == 0xA000: type = 'l' # symlink
    elif (f['mode'] & 0xE000) == 0x8000: type = '-' # file
    elif (f['mode'] & 0xE000) == 0x4000: type = 'd' # dir
    else: 
        print >> sys.stderr, "Unknown file type %04x for %s" % (f['mode'], fileinfo_str(f, False))
        type = '?' # unknown
    info = ("%s%s %08x %08x %7d %10d %10d %10d (%s)%s::%s" % 
            (type, modestr(f['mode']&0x0FFF) , f['userid'], f['groupid'], f['filelen'], 
             f['mtime'], f['atime'], f['ctime'], f['fileID'], f['domain'], f['filename']))
    
    info = ("%s%s %7d (%s)%s::%s" % 
            (type, modestr(f['mode']&0x0FFF), f['filelen'], 
             f['fileID'], f['domain'], f['filename']))
    
    if type == 'l': info = info + ' -> ' + f['linktarget'] # symlink destination
    for name, value in f['properties'].items(): # extra properties
        info = info + ' ' + name + '=' + repr(value)
    return info

verbose = True
if __name__ == '__main__':
    mbdb = process_mbdb_file("Manifest.mbdb")
    mbdx = process_mbdx_file("Manifest.mbdx")
    for offset, fileinfo in mbdb.items():
        if offset in mbdx:
            fileinfo['fileID'] = mbdx[offset]
        else:
            fileinfo['fileID'] = "<nofileID>"
            print >> sys.stderr, "No fileID found for %s" % fileinfo_str(fileinfo)
        print fileinfo_str(fileinfo, verbose)