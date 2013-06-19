#!/usr/bin/env python2

import argparse
from BeautifulSoup import BeautifulSoup
import urllib2
import unicodedata
import json


def get_page(city):
    '''Sends a request to the results page with the
    page number and city returns the BeautifulSoup page'''
    city = city.replace(' ', '+')
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.110 Safari/537.36"
    }
    page = urllib2.Request('http://www.sermilweb.eb.mil.br/sermilweb/jsm.action?descricao={0}'.format(city), None, headers)
    return BeautifulSoup(urllib2.urlopen(page).read())


def scrape(page):
    '''Scrapes the page for the JSMs and parses them
    into an array of size 4'''

    jsms = []
    table = page.findAll('table', {'class': 'simples'})[1]
    rows = table.findAll('tr')
    #remove table header
    rows.pop(0)
    for row in rows:
        columns = row.findAll('td')
        jsm_data = [unicodedata.normalize("NFKD", column.text).encode('ascii', 'ignore') for column in columns]
        coords = get_coords(jsm_data[1] + " " + jsm_data[0])
        jsm = {
            'neighborhood': jsm_data[2],
            'address': jsm_data[1],
            'phone': jsm_data[3],
            'email': jsm_data[4],
            'lat': coords[0],
            'lng': coords[1],
        }
        jsms.append(jsm)
    return jsms


def get_coords(address):
    '''Gets the latitude and longitude of an address
    from the google geocode api'''
    address = address.replace(' ', '+')
    page = urllib2.urlopen('http://maps.googleapis.com/maps/api/geocode/json?address={0}&sensor=true'.format(address))
    location_info = json.loads(page.read())
    try:
        return (location_info['results'][0]['geometry']['location']['lat'], location_info['results'][0]['geometry']['location']['lng'])
    except IndexError:
        return (0, 0)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--search', help='City to search', required=True)

    args = parser.parse_args()

    page = get_page(args.search)
    print(json.dumps(scrape(page)))
