from bs4 import BeautifulSoup
import requests
import csv
from urllib.parse import urljoin # For joining next page url with base url
from datetime import datetime # For inserting the current date and time

NYC_url = "https://www.airbnb.com/s/New-York--NY"
ATL_url = "https://www.airbnb.com/s/Atlanta--GA"
CHI_url = "https://www.airbnb.com/s/Chicago--IL"
SEA_url = "https://www.airbnb.com/s/Seattle--WA"
SAC_url = "https://www.airbnb.com/s/Sacramento--CA"

def scrape_airbnb(url, results, city):
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    
    for search_result in soup.find_all('div', 'listing-card-wrapper'):
        # Set up a dictionary for each search result on the page
        result = {}
        result['city'] = city
        try:
            result['price'] = search_result.find('span', attrs={"data-pricerate":"true"}).get_text()
        except:
            result['price'] = "Price not found"
        
        # The # of beds and # of guests all have a similarly named wrapper
        # Find all that are available and then determine which one is which by
        # looking for the "bed" and "guest" strings
        bed_guest = search_result.find_all('span', 'detailWithoutWrap_basc2l')
        for i in range(len(bed_guest)):
            if "bed" in bed_guest[i].get_text():
                result['beds'] = bed_guest[i].get_text()
            if "guest" in bed_guest[i].get_text():
                result['guests'] = bed_guest[i].get_text()
        
        if 'beds' not in result:
            result['beds'] = "Number of beds not found"
        if 'guests' not in result:
            result['guests'] = "Number of guests not found"
        
        results.append(result)

    # Search for a "Next Page" link
    next_page = soup.find('a', attrs={"rel":"next"})
    if next_page:
        next_page_url = urljoin(url, next_page.get('href'))
        print("next page: " + next_page_url)
        # Cycle back through the function until there are no more Next pages
        scrape_airbnb(next_page_url, results, city)
    return results

results = []
#results = scrape_airbnb(NYC_url, results, "New York")
results = scrape_airbnb(ATL_url, results, "Atlanta")
#results = scrape_airbnb(CHI_url, results, "Chicago")
#results = scrape_airbnb(SEA_url, results, "Seattle")
#results = scrape_airbnb(SAC_url, results, "Sacramento")

# Write the results to CSV
with open("scraper_data.csv",'w') as csvfile:
    writer = csv.DictWriter(csvfile, results[0].keys(), lineterminator = '\n')
    writer.writeheader()
    for result in results:
        try:
            writer.writerow(result)
        # Throw an error for Unicode errors
        except (UnicodeEncodeError, AttributeError):
            pass
    
print("finished")

