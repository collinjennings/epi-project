#!/usr/bin/python 

""" 
This is a Python program to extract epigraph metadata from TEI XML documents.

Run this program with the command: 
	python parse.py your-xml-file-here.xml
Or optionally: 
	python parse.py -x xpath.txt your-xml-file-here.xml

"""
import sys # library for doing system things 
from optparse import OptionParser #parse options from the command line!
from lxml import etree # for parsing XML
import re # need regex for doing fancy split
import logging # send debugging messages

# Options {{{1
parser = OptionParser('usage: %prog [options] file1.xml [file2.xml]') 
parser.add_option("-x", "--xpath", action="store", dest="xpath",         
		help="A text file containing a comma-separated list of the names (i.e. XML IDs) of the characters whose dialog you want to extract. Default: characters.txt")
parser.add_option("-v", "--verbose", action="store_true", dest="verbose")
parser.add_option("-q", "--quiet", action="store_false", dest="verbose")

# End of Options }}} 

(options, files) = parser.parse_args()

if options.xpath: 
	xpath=options.xpath # first try using command-line-provided xpath
else: 
    xpathFile = "xpath.txt" 
    try: 
        xpath=open(xpathFile).read() 
    except IOError: 
        parser.error("Error reading from file %s" % xpathFile) 

xpath=re.split('\n|,',xpath) #split by commas or newlines and strip out whitespace
xpaths=[]
for xpath in xpath: 
	xpaths.append(xpath.strip()) #remove whitespace
xpaths=filter(None,xpaths) # get rid of empty entries

#Verbose output will help to debug
if options.verbose:
        print "Using xpath(s): "
        for xpath in xpaths:
                print '  '+xpath
        print "Using xml file(s): "
        for index, value in enumerate(files): 
                print ' ',index+1, value

if len(files) < 1:
    parser.error("Please specify at least one XML file.") 

for file in files: 
    if not file.lower().endswith('.xml'): 
        parser.error("It looks like file %s is not an XML file." % file) 

rawxmls = [open(file).read() for file in files] 

if options.verbose: 
	print "Files loaded successfully." 

xmls = [rawxml.replace(' xmlns="http://www.tei-c.org/ns/1.0"','') for rawxml in rawxmls] #strip out annoying TEI namespace

if options.verbose: 
    print "Here's what the beginning of the first XML file looks like after stripping out the namespace:\n" + xmls[0][:100] 

#load xml files
xmls=[etree.fromstring(xmlfile) for xmlfile in xmls] #parse files 

#from suggestion here: http://stackoverflow.com/questions/16640041/what-is-an-elementtree-object-exactly-and-how-can-i-get-data-from-it?noredirect=1#16640278 

output=[]
for xml in xmls: 
 	for xpath in xpaths: 
		output+=xml.xpath(xpath + '/text()')

#print "Output: " 
#print output

#exit() #temporary breakpoint

clean=""
#new way 
clean = '\t'.join(line.strip() for line in output)
#old way
#for line in output: 
#	clean+=line.strip()+'\n' #strip all extra space and then make them individual lines

#encoding it makes it work with piping as described here: http://stackoverflow.com/questions/492483/setting-the-correct-encoding-when-piping-stdout-in-python 
encoded=sys.stdout.write(clean.encode('utf-8'))
