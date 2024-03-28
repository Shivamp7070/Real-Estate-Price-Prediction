import requests
from bs4 import BeautifulSoup


url = 'https://www.apartments.com/chicago-il-60607/'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

response = requests.get(url, headers=headers)
html_content = response.content

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Find the <span> element with class "pageRange"
page_range = soup.find('span', class_='pageRange')

# Extract the text from the <span> element
page_range_text = page_range.get_text()

# Extract the last two words from the text and convert to integer
last_page = page_range_text.split()[-1]
last_page = int(last_page)

links = set()

for i in range(1, last_page + 1):
    url = 'https://www.apartments.com/chicago-il-60607/' + str(i) + "/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

    response = requests.get(url, headers=headers)
    html_content = response.content

    soup = BeautifulSoup(html_content, 'html.parser')

    # Find all the listings on the page
    listings = soup.find_all('a', {'class': 'property-link'})

    # Loop through each listing and extract the data
    for listing in listings:
        # Get the link to the listing's detail page
        detail_link = listing['href']
        links.add(detail_link)

with open("60607_apartments.csv", "w", encoding="utf-8") as file:
    for link in links:
        file.write(link + '\n')
