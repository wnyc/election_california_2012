#!/usr/bin/python
import re
import sys

# python remove_description_from_kml.py <original.kml> > original_stripped.kml

def remove_description_tag(xmltext):
    # Simply use regular expression to remove <description>...</description> from kml files
    # Quick and dirty works with California files

    description_re = re.compile("<description>.+?</description>\s*", re.S)

    return re.sub(description_re, "", xmltext)

if __name__ == '__main__':
    infile = file(sys.argv[1])
    print remove_description_tag(infile.read())

    
    


    
