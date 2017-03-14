"""
This module scrapes a sample edgar site and output its data in JSON accodring to the guidelines given in
part 2 of of the enigma data engineering test.
"""

import json
from bs4 import BeautifulSoup
import requests

MAIN_URL = 'http://data-interview.enigmalabs.org/companies/'
OUTPUT = 'solution.json'


def parse_single_company(company_info_url):
    """
    Takes in a URL of a single company and parses it to extract the information

    :param company_info_url (string): Normalized URL to get the data from
    :return dictionary: Dictionary of all the information on a particular company
    """

    r = requests.get(company_info_url)

    soup = BeautifulSoup(r.text, 'html.parser')
    all_td_tags = soup.find_all('td')

    company_info = {}
    for i in range(len(all_td_tags))[0::2]:  # Jump 2 tags at once
        company_info[all_td_tags[i].text] = all_td_tags[i + 1].text

    return company_info


def parse_single_page(url, base):
    """
    Parses a single page containing links to the companies.

    :param url (string): URL of the page with the company links
    :param base (string): Base URL of the webpage
    :return dictionary: Dictionary of all the related information of the companies in url
    """
    r = requests.get(url)

    soup = BeautifulSoup(r.text, 'html.parser')

    links = {}
    for link in soup.find_all('a'):  # Get all the hyperlinks
        links[link.contents[0].strip()] = link.get('href')

    single_page_info = {}
    for key, value in links.iteritems():
        if '/companies/' in value and value != '/companies/' and '/companies/?page' not in value:
            single_page_info[key] = parse_single_company(
                base + value.replace('/companies/', '').replace(' ', '%20'))
            # Normalize the URL before passing it as a parameter

    return single_page_info


def web_scrape(main_url, output):
    """
    Scrapes the webpage looking for information on all the companies and writes it to a json file

    :param main_url (string): Url of the webpage that will get parsed
    :param output (string): Name of the json file that will be outputted
    :return: None
    :Prints dictionary: Dictionary of all the company related info
    """
    company_info = {}  # This will be the dictionary that will be written to the JSON file

    for i in range(10):  # There are 10 pages
        url = main_url + '?page={0}'.format(i + 1)
        company_info.update(parse_single_page(url, main_url))

    with open(output, 'w') as f:
        json.dump(company_info, f)  # Writing the json file

    print json.dumps(company_info)

if __name__ == "__main__":
    web_scrape(MAIN_URL, OUTPUT)
