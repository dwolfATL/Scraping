# -*- coding: utf-8 -*-
"""
Scraping sentiment analysis from Sentdex.com
Author: DWolf

"""

from bs4 import BeautifulSoup
import requests
import csv

url = "http://www.sentdex.com/financial-analysis/"

def scrape_sentdex(url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    
    results = []
    
    # Table loop
    for tr in soup.find_all('tr')[1:]:
        
        result = {}
        tds = tr.find_all('td')
        result['Symbol'] = tds[0].text
        result['Instrument Name'] = tds[1].text
        result['all Volume of Mentions'] = tds[2].text
        result['all Overall Sentiment'] = tds[3].text
        # The only non-trivial part is getting the recent sentiment direction
        direction = tds[4].span.get('class')[1]
        if 'down' in direction:
            result['Recent Sentiment Rising or Falling'] = 'down'
        else:
            result['Recent Sentiment Rising or Falling'] = 'up'
        
        results.append(result)
        
    return results

results = scrape_sentdex(url)

with open("sentdex_data.csv",'w') as csvfile:
    # Using dictionary keys as fieldnames for the CSV file header
    writer = csv.DictWriter(csvfile, results[0].keys(), lineterminator = '\n')
    writer.writeheader()
    for result in results:
        try:
            writer.writerow(result)
        # Throw an error for Unicode errors
        except (UnicodeEncodeError, AttributeError):
            pass
    
print('finished')
