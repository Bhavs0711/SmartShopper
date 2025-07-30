from flask import Flask, render_template, request
from meesho_scraper import scrape_meesho
from amazon_scraper import scrape_amazon
from flipkart_scraper import scrape_flipkart
import random

app = Flask(__name__)

def search_all_sources(query):
    amazon_results = scrape_amazon(query)
    flipkart_results = scrape_flipkart(query)
    meesho_results = scrape_meesho(query)

    # Combine all results into one list
    results = amazon_results + flipkart_results + meesho_results
    return results

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/search")
def search():
    query = request.args.get("query")
    sort = request.args.get('sort')
    if not query:
        return render_template("search.html", products=[])

    results = search_all_sources(query)

    # Convert price to int for sorting
    for r in results:
        if "price" in r and not r["price"].startswith("₹"):
            try:
                # If it's a number, re-format
                r["price"] = "₹" + str(int(r["price"]))
            except:
                pass

    # Sorting logic
    if sort == "price_low":
        results.sort(key=lambda x: float(str(x.get("price", "0")).replace("₹", "").replace(",", "").strip()) if str(
            x.get("price", "")).replace("₹", "").replace(",", "").strip().isdigit() else float('inf'))
    elif sort == "quality_best":
        results.sort(
            key=lambda x: float(x.get("rating", 0)) if str(x.get("rating", "0")).replace(".", "").isdigit() else 0,
            reverse=True)
    elif sort == "delivery_fast":
        results.sort(
            key=lambda x: float(str(x.get("delivery", "999")).replace("₹", "").replace(",", "").strip()) if str(
                x.get("delivery", "")).replace("₹", "").replace(",", "").strip().isdigit() else float('inf'))
    elif sort == "reviews_top":
        results.sort(key=lambda x: int(str(x.get("reviews", "0")).replace(",", "").strip()) if str(
            x.get("reviews", "0")).replace(",", "").strip().isdigit() else 0, reverse=True)

    # TODO: Add pagination logic here (coming next)

    return render_template('search.html', products=results, query=query)

@app.route("/about")
def about():
    return render_template("about.html")

if __name__ == '__main__':
    app.run(debug=True)
