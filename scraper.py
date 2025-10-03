import requests
from bs4 import BeautifulSoup
import json
import csv

def scrape_flipkart_products(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        html_content = response.text
    except requests.RequestException as e:
        print(f"Error fetching URL: {e}")
        return []

    soup = BeautifulSoup(html_content, 'html.parser')

    products = []

    # Flipkart search results have products in divs with specific classes
    # This may need adjustment based on current HTML structure
    product_containers = soup.find_all('div', class_='_75nlfW')

    for container in product_containers:
        product = {}

        # Extract product name
        name_elem = container.find('div', class_='KzDlHZ')
        if name_elem:
            product['name'] = name_elem.text.strip()

        # Extract price
        price_elem = container.find('div', class_='Nx9bqj _4b5DiR')
        if price_elem:
            product['price'] = price_elem.text.strip()

        # Extract rating
        rating_elem = container.find('div', class_='XQDdHH')
        if rating_elem:
            product['rating'] = rating_elem.text.strip()

        # Extract number of ratings/reviews
        reviews_elem = container.find('span', class_='Wphh3N')
        if reviews_elem:
            product['reviews'] = reviews_elem.text.strip()

        # Extract product link
        link_elem = container.find('a', class_='CGtC98')
        if link_elem:
            product['link'] = 'https://www.flipkart.com' + link_elem['href']

        if product.get('name'):  # Only add if name is found
            products.append(product)

    return products

if __name__ == "__main__":
    url = input("Enter the Flipkart search URL: ")
    products = scrape_flipkart_products(url)

    if products:
        print("Scraped Products:")
        for product in products:
            print(json.dumps(product, indent=4))

        # Save to CSV
        with open('flipkart_products.csv', 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['name', 'price', 'rating', 'reviews', 'link']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for product in products:
                writer.writerow(product)
        print("Products saved to flipkart_products.csv")
    else:
        print("No products found or error in scraping.")
