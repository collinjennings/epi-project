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

import config

parser = OptionParser('usage: %prog [options] file1.xml [file2.xml]') 
parser.add_option("-v", "--verbose", action="store_true", dest="verbose")

(options, files) = parser.parse_args()


if options.verbose:
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

#strip out annoying TEI namespace
xmls = [rawxml.replace(' xmlns="http://www.tei-c.org/ns/1.0"','') for rawxml in rawxmls] 

if options.verbose: 
    print "Here's what the beginning of the first XML file looks like after stripping out the namespace:\n" + xmls[0][:100] 

#parse files 
xmls=[etree.fromstring(xmlfile) for xmlfile in xmls] 

epigraphs = [] 
index = 0 
for xml in xmls: 
    title = xml.xpath(config.titleXPATH + '/text()')[0]
    author = xml.xpath(config.authorXPATH + '/text()')[0]
    epigraph = xml.xpath(config.epigraphXPATH + '/text()')  
    attribution = xml.xpath(config.attributionXPATH + '/text()')
    for epi_instance in epigraph: 
        epigraphs.append(title, author, epigraph[index], attribution[index]) 
        index++  

    output = "---------------\n" 
    for epi_instance in epigraphs: 
        output+= "Title: %s \nAuthor: %s \nEpigraph: %s \nAttribution: %s" % (epigraphs[0], epigraphs[1], epigraphs[2], epigraphs[3])
    output+= "---------------" 

print "Type, Epigraph Taken From, Epigraph Written By, Publication Date of Epigraph, Epigraph Used By, Genre of Containing Text, Date Setting of Containing Text, Publication Date of Containing Text, Epigraph Appears In, Epigraph Attributed to Person, Epigraph Attributed to Text, Location of Epigraph in Original Text, Location of Epigraph in New Text, Epigraph, Purpose, Genre of Epigraph, Filename"  

#separate xpath items with tabs, separate multi-line items with newlines
#clean = '\t'.join(['\n'.join(item) if isinstance(item, list) else item for item in output]) 

#encode in utf-8 so that it pipes nicely on the commandline: 
encoded=sys.stdout.write(output.encode('utf-8'))
