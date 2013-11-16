#About this Program
This is a simple command-line utility to extract information from TEI XML documents. It is only compatible with python 2.7.x at the moment. It was created by the Digital Experiments Working Group at NYU for their Epigraphs Project.  

It parses XML files using user-provided XPATH expressions, and writes these to the standard output, in tab-separated format. 

#Usage Examples
You can specify your xpath in the command line: 

`python parse.py -x '//epigraph/q/l' 4397.xml`  

Or you can put it all in a file called xpath.txt (example included in this repository). 

You can also specify multiple xml files: 

`python parse.py 4397.xml 4399.xml 5129.xml` 

Or use the wildcard to parse all XML files in your directory: 

`python parse.py *.xml` 

You can also write the output to a file like this: 

`python parse.py 4397.xml > output.txt` 

