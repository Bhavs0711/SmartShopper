import pandas as pd
import difflib

# Load the Meesho data CSV once
CSV_PATH = "Meesho Data - MeeshoData.csv"
df = pd.read_csv(CSV_PATH)

# Clean and normalize data
df.dropna(subset=["title", "price", "category"], inplace=True)
df['price'] = df['price'].astype(str).str.replace('₹', '').str.strip()
df['price'] = pd.to_numeric(df['price'], errors='coerce')
df['rating'] = pd.to_numeric(df['rating'], errors='coerce')
df['reviews'] = pd.to_numeric(df['reviews'], errors='coerce')
df['delivery'] = df['delivery'].fillna("").astype(str)

def fuzzy_match_category(query, categories):
    matches = difflib.get_close_matches(query.lower(), [cat.lower() for cat in categories], n=1, cutoff=0.4)
    if matches:
        for cat in categories:
            if cat.lower() == matches[0]:
                return cat
    return None

def scrape_meesho(query=None, sort=None):
    if query:
        matched_category = fuzzy_match_category(query, df['category'].unique())
        if matched_category:
            filtered_df = df[df['category'].str.lower() == matched_category.lower()]
        else:
            filtered_df = df[df['title'].str.lower().str.contains(query.lower())]
    else:
        filtered_df = df.copy()

    if sort == "price_low":
        filtered_df = filtered_df.sort_values(by="price", ascending=True)
    elif sort == "quality_best":
        filtered_df = filtered_df.sort_values(by="rating", ascending=False)
    elif sort == "reviews_top":
        filtered_df = filtered_df.sort_values(by="reviews", ascending=False)
    elif sort == "delivery_low":
        # Move "Free" delivery to the top
        filtered_df["delivery_fee"] = filtered_df["delivery"].apply(lambda x: 0 if "free" in x.lower() else int(''.join(filter(str.isdigit, x))) if x else 999)
        filtered_df = filtered_df.sort_values(by="delivery_fee", ascending=True)

    results = []
    for _, row in filtered_df.iterrows():
        results.append({
            "title": row["title"],
            "link": row["link"],
            "image": row["image"],
            "price": f"₹{int(row['price'])}" if not pd.isna(row["price"]) else "N/A",
            "delivery": row["delivery"],
            "rating": row["rating"] if not pd.isna(row["rating"]) else "No rating",
            "reviews": int(row["reviews"]) if not pd.isna(row["reviews"]) else 0,
            "platform": "Meesho"
        })

    return results

# --------------------------- RUN TEST ---------------------------
if __name__ == "__main__":
    user_query = input("Enter your product search: ")
    results = scrape_meesho(user_query)
    # print_products(results, "Meesho")
