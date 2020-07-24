"""This is a program to collect and sort sources from wikipedia articles, and optionally check them against an external database, then return a CSV file.
This program was created for money at the request of a client, who gave permission for it to be released, open source, to the general public.
It relies on the PyMediaWiki and tldextract libraries, which can be found on pypi.org and are released under the MIT and BSD licenses respectively.
Developed by Evan Landau, 7/18/2020 - 7/23/2020.
"""

import argparse
import datetime

import mediawiki
import tldextract

wikipedia = mediawiki.MediaWiki()
wikipedia.user_agent = 'Source-checking Bot, source code available from https://github.com/EvanLandau/Wiki-Source-DL'

def article_sources_from_category(input_page):
    """Takes in a wikipedia.WikipediaPage article, which should be a category (but this is not checked)
    Returns a dictionary with the sources listed (all external links, ) for keys and the articles listed as values
    May take a long time to run! The process slows exponentially 
    """
    source_dictionary = {}
    
    #Turns list of page titles into list of page objects
    print("Accessing links to pages...")
    pages = []
    page_access_success_count = 0
    page_access_try_count = 0
    pages_in_category = wikipedia.categorymembers(input_page.strip(), results=None, subcategories=False)
    for page_name in pages_in_category:
        try:
             pages.append(wikipedia.page(page_name))
        except:
            print("There was an error opening the link titled \"" + page_name + "\", ignoring.") #TODO: Implement proper exception tracking
        else:
            page_access_success_count += 1
        page_access_try_count += 1
    print('Accessed', page_access_success_count, 'pages successfully of', page_access_try_count, 'pages (' + str(int(page_access_success_count/page_access_try_count*100)) + '%).')
    #TODO: Remove duplicates?
    #Gets references from pages, adds them to dictionary
    #TODO: Implement multithreading?
    print('Getting references from pages, starting at', datetime.datetime.now().isoformat())
    for page in pages:
        ref_url_list = page.references
        for reference in ref_url_list:
            # Convert URL into just the domain
            domain_er = tldextract.extract(reference)
            domain = '.'.join(domain_er[1:3])
            #Find it in the dictionary, and add one, or add to the dictionary
            if domain in source_dictionary:
                source_dictionary[domain] += 1
            else:
                source_dictionary.update({domain:1})
    return source_dictionary

def getKey(tuple):
    return tuple[1]

def article_sources_output(category_name, output_file_name):
    """Takes in the name of a wikipedia category
    Creates a .csv file with the sources and their quantities
    """
    source_dictionary = article_sources_from_category(category_name)
    print("Sources collected at", datetime.datetime.now().isoformat(), ".")
    sorted_list = sorted(source_dictionary.items(), key = getKey, reverse = True)
    out = open(output_file_name, 'w')
    for line in sorted_list:
        out.write(str(line[0]) + ',' + str(line[1]) + '\n')
    out.close()
    print("Output file created. (" + output_file_name + ").")
    
parser = argparse.ArgumentParser()
parser.add_argument('category', nargs=1, type=str, help='The name of the wikipedia category you would like to search through.')
parser.add_argument('output', nargs='?', type=str, help='The output file ("output.csv" by default).', default = 'output.csv')
args = parser.parse_args()

article_sources_output(args.category[0], args.output)
