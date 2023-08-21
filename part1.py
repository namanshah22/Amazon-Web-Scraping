import requests
from bs4 import BeautifulSoup
import csv

# Define the URL and headers
base_url = "https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1"
search_query = "bags"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
}

csv_header = ['Product URL', 'Product Name', 'Product Price', 'Rating', 'Number of Reviews']
csv_rows = []

# Loop through 20 pages of product listings
for page_number in range(1, 21):
    params = {
        'k': search_query,
        'page': page_number,
    }

    response = requests.get(base_url, headers=headers, params=params)
    soup = BeautifulSoup(response.content, 'html.parser')

    product_items = soup.find_all('div', {'data-component-type': 's-search-result'})

    for item in product_items:
        product_url_elem = item.find('a')

        if product_url_elem:
            product_url = "https://www.amazon.in" + product_url_elem['href']
        else:
            product_url = 'N/A'

        product_name_elem = item.find('span', {'class': 'a-text-normal'})
        if product_name_elem:
            product_name = product_name_elem.text.strip()
        else:
            product_name = 'N/A'

        product_price_elem = item.find('span', {'class': 'a-offscreen'})
        if product_price_elem:
            product_price = product_price_elem.text.strip()
        else:
            product_price = 'N/A'

        rating_elem = item.find('span', {'class': 'a-icon-alt'})
        if rating_elem:
            rating = rating_elem.text.strip()
        else:
            rating = 'N/A'

        num_reviews_elem = item.find('span', {'class': 'a-size-base'})
        if num_reviews_elem:
            num_reviews = num_reviews_elem.text.strip()
        else:
            num_reviews = 'N/A'

        csv_rows.append([product_url, product_name, product_price, rating, num_reviews])

# Save the data to a CSV file
with open('amazon_products.csv', 'w', encoding='utf-8', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(csv_header)
    csvwriter.writerows(csv_rows)


