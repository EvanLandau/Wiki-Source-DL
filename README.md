# Wiki-Source-DL
This is a python script to download wikipedia source domains from category pages.

For example, it could be run:
$python wiki_source_finder.py 'Wikipedia'
Which would create a file (by default, output.csv) listing all the top-level domains from the References of each page in the Wikipedia category Category:Wikipedia.

The script takes the following arguments:
$python wiki_source_finder.py title [output file]
The title is the name of the category to get sources from (WITHOUT the "Category:" part before it)
Output is an optional parameter that specifies what file to output to. Regardless of what is entered here, the output is always in .csv format.

This program requires pymediawiki and tldextract, both of which can be installed via pip.
pymediawiki: https://pypi.org/project/pymediawiki/
tldextract: https://pypi.org/project/tldextract/
