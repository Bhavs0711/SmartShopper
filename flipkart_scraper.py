import requests
from bs4 import BeautifulSoup
from urllib.parse import quote, urljoin

def scrape_flipkart(query):
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"
    }

    search_url = f"https://www.flipkart.com/search?q={quote(query)}"
    response = requests.get(search_url, headers=headers)

    if response.status_code != 200:
        print(f"❌ Failed to fetch page: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    products = []

    for container in soup.select("div._1sdMkc"):
        try:
            title = container.select_one("a.WKTcLC").get_text(strip=True)
            price = container.select_one("div.Nx9bqj").get_text(strip=True)
            image = container.select_one("img._53J4C-")["src"]
            href = container.select_one("a.rPDeLR")["href"]
            product_link = urljoin("https://www.flipkart.com", href)
            brand_tag = container.select_one("div.syl9yP")
            brand = brand_tag.get_text(strip=True) if brand_tag else "Unknown"

            # ⭐ Extract rating
            rating_tag = container.select_one("div.XQDdHH span._3LWZlK")
            rating = rating_tag.get_text(strip=True) if rating_tag else "No rating"

            # 📦 Extract delivery info
            delivery_tag = container.select_one("div._3tcB5a")
            delivery = delivery_tag.get_text(strip=True) if delivery_tag else "Delivery info not available"

            products.append({
                "title": title,
                "price": price,
                "brand": brand,
                "link": product_link,
                "image": image,
                "rating": rating,
                "reviews": "N/A",
                "delivery": delivery,
                "platform": "Flipkart"
            })
        except Exception:
            continue  # Skip any containers with missing data

    return products

# Test it:
if __name__ == "__main__":
    query = input("Search Flipkart for: ")
    results = scrape_flipkart(query)
    for product in results:
        print(f"\n🛍️ {product['brand']} - {product['title']}")
        print(f"💰 {product['price']}")
        print(f"⭐ {product['rating']}")
        print(f"🚚 {product['delivery']}")
        print(f"🖼️ {product['image']}")
        print(f"🔗 {product['link']}")

