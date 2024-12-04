import requests
from bs4 import BeautifulSoup
import csv
import json
import time

# URL of the website to scrape (without page number)
BASE_URL = "https://www.amazon.in/s?k=laptops&page="
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.101 Safari/537.36"}

# Function to fetch webpage content
def fetch_webpage(url):
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()  # Will raise an error for 4xx/5xx responses
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None  # Return None if there is an error

# Function to parse products from the HTML content
def parse_products(html):
    soup = BeautifulSoup(html, "html.parser")
    products = []  # List to store the extracted product data

    # Loop through each product entry
    for product in soup.find_all("div", class_="sg-col-inner"):
        # Initializing variables
        title = price = description = ratings = stars = "N/A"

        # Locate the container div
        container = product.find("div", class_="puisg-row")
        if container:
            # Extracting product details
            title_tag = container.find("div", class_="puisg-col puisg-col-4-of-12 puisg-col-8-of-16 puisg-col-12-of-20 puisg-col-12-of-24 puis-list-col-right")
            price_tag = container.find("span", class_="a-price-whole")
            description_tag = container.find("span", class_="a-size-base a-color-secondary")
            ratings_tag = container.find("span", class_="a-size-base s-underline-text")
            stars_tag = container.find("span", class_="a-icon-alt")

            # Extracting data if tags exist
            if title_tag:
                title = title_tag.find("h2").text.strip()  # Extracting the title 
            if price_tag:
                price = price_tag.text.strip() # Extracting the price 
            if description_tag:
                description = description_tag.text.strip() # Extracting how many people bought
            if ratings_tag:
                ratings = ratings_tag.text.strip()  # Extracting the rating
            if stars_tag:
                stars = stars_tag.text.strip()  # Extracting the stars

            print(f"Found title: {title}")  # Debugging statement
            print(f"Found price: {price}")
            print(f"Found description: {description}")
            print(f"Found rating: {ratings}")
            print(f"Found stars: {stars}")
        else:
            print("No caption div found in this product.")

        # Adding the product information to the list
        products.append({"title": title, "price": price, "description": description, "ratings": ratings, "stars": stars})

    return products

# Function to save data to CSV
def save_to_csv(data, filename="scraped_data.csv"):
    keys = data[0].keys()
    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)
        print(f"Data saved to {filename}")

# Function to save data to JSON
def save_to_json(data, filename="scraped_data.json"):
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
    print(f"Data saved to {filename}")

# Function to scrape multiple pages
def scrape_multiple_pages(start_page, end_page):
    all_products = []  # List to store products from all pages
    for page_number in range(start_page, end_page + 1):
        print(f"Fetching page {page_number}...")
        url = BASE_URL + str(page_number)
        html = fetch_webpage(url)
        print("Parsing data...")
        products = parse_products(html)
        all_products.extend(products)  # Add products from current page to the list
        time.sleep(2)  # Adding delay to avoid being blocked
    return all_products

# Main script
def main():
    print("Starting web scraping...")
    products = scrape_multiple_pages(2, 4)  # Scrape pages 2 to 4
    print(f"Found {len(products)} products. Saving to CSV and JSON...")
    if len(products) == 0:
        print("No products found. Exiting.")
    else:
        save_to_csv(products)
        save_to_json(products)

if __name__ == "__main__":
    main()
