import requests
from bs4 import BeautifulSoup
import csv

with open("60607_apartments.csv", "w") as file:
    file.write(
        "Address,Bedrooms,Bathrooms,Rent,Total Area,Price per Sq.Ft.,Transit Score,Type of House\n")

with open("60607_apartments_link.csv", encoding="utf-8") as file:
    links = file.readlines()
    for link in links:
        url = link.strip()
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

        response = requests.get(url, headers=headers)
        html_content = response.content

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')

        if not soup:
            continue

        property_name = soup.find('h1', class_="propertyName")
        # Find the <div> element with class "propertyAddressRow"
        address_row = soup.find('div', class_='propertyAddressRow')

        # Extract the text from all child elements of the <div> element
        address_text = property_name.get_text(
            strip=True) + " " + address_row.get_text(strip=True)

        # Find the <ul> element with class "priceBedRangeInfo"
        price_info = soup.find('ul', class_='priceBedRangeInfo')

        # Extract minimum and maximum rent
        rent_detail = price_info.find(
            'p', class_='rentInfoDetail').get_text().split(' - ')
        rent = int(rent_detail[0].strip('$').replace(',', ''))

        # Extract number of bedrooms
        bedrooms_detail = price_info.find_all(
            'p', class_='rentInfoDetail')[1].get_text()
        num_bedrooms = bedrooms_detail.split(' ')[-2]

        # Extract number of bathrooms
        bathrooms_detail = price_info.find_all(
            'p', class_='rentInfoDetail')[2].get_text()
        num_bathrooms = bathrooms_detail.split(' ')[-2]

        # Extract minimum and maximum square feet
        sq_ft_detail = price_info.find_all('p', class_='rentInfoDetail')[
            3].get_text().split(' - ')
        sq_ft = sq_ft_detail[0].replace(',', '').strip(' sq ft').strip()

        if sq_ft:
            price_per_sq_ft = rent/int(sq_ft)
        else:
            price_per_sq_ft = 0

        residence_type = ""

        transit_score = soup.find('div', class_='transitScore').find(
            'div', class_='score').text

        with open("60607_apartments.csv", "a") as file:
            file.write(
                f"{address_text},{num_bedrooms},{num_bathrooms},{rent},{sq_ft},{price_per_sq_ft},{transit_score},{residence_type}\n")
