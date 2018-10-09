# Wikipedia parser, from:
# http://gis.stackexchange.com/questions/1047/full-list-of-iso-alpha-2-and-iso-alpha-3-country-codes/151571#151571

import csv
import urllib2
from BeautifulSoup import BeautifulSoup

opener = urllib2.build_opener()
opener.addheaders = [("User-agent", "Mozilla/5.0")]

url = "http://en.wikipedia.org/wiki/ISO_3166-1"

page = opener.open(url)
soup = BeautifulSoup(page.read())

t = soup.find("table", {"class": "wikitable sortable"})

# create a new CSV for the output
iso_csv = csv.writer(open("wikipedia-iso-country-codes.csv", "w"))

# get the header rows, write to the CSV
iso_csv.writerow([th.findAll(text=True)[0] for th in t.findAll("th")])

# Iterate over the table pulling out the country table results. Skip the first
# row as it contains the already-parsed header information.
for row in t.findAll("tr")[1:]:
    tds = row.findAll("td")
    raw_cols = [td.findAll(text=True) for td in tds]
    cols = []
    # country field contains differing numbers of elements, due to the flag --
    # only take the name
    cols.append(raw_cols[0][-1:][0])
    # for all other columns, use the first result text
    cols.extend([col[0] for col in raw_cols[1:]])
    iso_csv.writerow(cols)
