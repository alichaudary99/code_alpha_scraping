
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random

# ========== CONFIGURATION ==========
BASE_URL = "https://books.toscrape.com/catalogue/page-{}.html"
START_PAGE = 1
END_PAGE = 5  # You can set up to 50 (there are 50 pages on the site)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; CodeAlphaBot/1.0; +https://codealpha.example)"
}

SELECTORS = {
    "container": "article.product_pod",
    "title": "h3 a",
    "price": "p.price_color",
    "link": "h3 a"
}

# ========== SCRAPING FUNCTION ==========
def scrape_page(page_number):
    """Scrape one page and return list of dicts."""
    url = BASE_URL.format(page_number)
    print(f"[INFO] Scraping page {page_number}: {url}")

    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"[ERROR] Could not fetch page {page_number}: {e}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    items = soup.select(SELECTORS["container"])
    data = []

    for item in items:
        title_tag = item.select_one(SELECTORS["title"])
        price_tag = item.select_one(SELECTORS["price"])
        link_tag = item.select_one(SELECTORS["link"])

        title = title_tag.get("title") if title_tag and title_tag.has_attr("title") else title_tag.get_text(strip=True)
        price = price_tag.get_text(strip=True) if price_tag else None
        link = link_tag["href"] if link_tag and link_tag.has_attr("href") else None

        # make full URL if relative
        if link and not link.startswith("http"):
            link = "https://books.toscrape.com/catalogue/" + link.replace("../", "")

        data.append({
            "title": title,
            "price": price,
            "link": link
        })
    return data

# ========== MAIN LOOP ==========
all_books = []
for page in range(START_PAGE, END_PAGE + 1):
    page_data = scrape_page(page)
    all_books.extend(page_data)
    
    delay = random.uniform(1, 3)
    print(f"[INFO] Sleeping for {delay:.1f} seconds...\n")
    time.sleep(delay)

print(f"[INFO] Total books scraped: {len(all_books)}")

# ========== DATA CLEANING & SAVING ==========
df = pd.DataFrame(all_books)

# Clean prices (remove £ and Â symbols)
df["price_cleaned"] = (
    df["price"]
    .astype(str)
    .str.replace("Â", "", regex=False)
    .str.replace("£", "", regex=False)
    .str.strip()
)
df["price_cleaned"] = pd.to_numeric(df["price_cleaned"], errors="coerce")

df.drop_duplicates(subset=["title"], inplace=True)
df.dropna(subset=["title"], inplace=True)

# Save to CSV and Excel
df.to_csv("books_scraped_data.csv", index=False, encoding="utf-8-sig")
df.to_excel("books_scraped_data.xlsx", index=False)

print("\n✅ SCRAPING COMPLETE!")
print(f"💾 Saved {len(df)} books to:")
print("   - books_scraped_data.csv")
print("   - books_scraped_data.xlsx")
print("\nVisit https://books.toscrape.com/ to verify the results.")

