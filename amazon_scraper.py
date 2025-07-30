import requests
from bs4 import BeautifulSoup
from urllib.parse import quote_plus, urljoin
import random

def scrape_amazon(query):
    headers = {
        "User-Agent": random.choice([
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Safari/605.1.15",
        ]),
        "Accept-Language": "en-US,en;q=0.9",
    }

    url = f"https://www.amazon.in/s?k={quote_plus(query)}"
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    results = []

    for item in soup.select("div.s-main-slot > div"):
        link = item.select_one("a.a-link-normal[href*='/dp/']")
        img = item.select_one("img.s-image")

        if not link or not img:
            continue

        title = img.get("alt")
        image_url = img.get("src")
        product_url = urljoin("https://www.amazon.in", link["href"])

        price_whole = item.select_one("span.a-price-whole")
        price_fraction = item.select_one("span.a-price-fraction")

        if price_whole and price_fraction:
            price = f"₹{price_whole.text}{price_fraction.text}"
        elif price_whole:
            price = f"₹{price_whole.text}"
        else:
            price = "Not listed"

        rating = item.select_one("span.a-icon-alt")
        delivery = item.select_one("span.a-color-base.a-text-bold") or item.select_one("span.a-color-base.a-text-normal")

        results.append({
            "title": title,
            "price": price,
            "image": image_url,
            "link": product_url,
            "rating": rating.text.split()[0] if rating else "No rating",
            "delivery": delivery.text.strip() if delivery else "Delivery info not listed",
            "reviews": "N / A",
            "platform": "Amazon"
        })

    return results

if __name__ == "__main__":
    query = input("Search for a product: ")
    products = scrape_amazon(query)
    for i, r in enumerate(products[:5], 1):
        print(f"\n📦 Product {i}")
        print("🛍️ Title:", r['title'])
        print("💰 Price:", r['price'])
        print("⭐ Rating:", r['rating'])
        print("🚚 Delivery:", r['delivery'])
        print("🌐 Link:", r['link'])
        print("🖼️ Image:", r['image'])
