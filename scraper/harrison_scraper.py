import requests
from bs4 import BeautifulSoup
from database.models import Property, SessionLocal
from urllib.parse import urljoin
import time

BASE_URL = "https://www.harrisonsnet.co.uk"

def scrape_harrisons():
    all_properties = []
    session = SessionLocal()

    # Go through multiple pages (up to 9 pages)
    for page in range(1, 10):
        print(f"Scraping page {page}...")
        url = f"{BASE_URL}/properties-for-sale?start={12 * (page - 1)}"  # pagination pattern
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(response.text, "html.parser")

        # Find all property cards
        listings = soup.find_all("div", class_="eapow-overview-row")
        print(f"Found {len(listings)} listings on page {page}")

        if not listings:
            break

        for listing in listings:
            try:
                link_tag = listing.find("a", href=True)
                if not link_tag:
                    continue

                relative_link = link_tag["href"]
                full_link = urljoin(BASE_URL, relative_link)

                title_tag = listing.find("h3")
                title = title_tag.get_text(strip=True) if title_tag else "No title"

                price_tag = listing.find("span", class_="eapow-overview-price")
                price = price_tag.get_text(strip=True) if price_tag else "No price"

                image_tag = listing.find("img", class_="eapow-overview-thumb")
                image_url = image_tag["data-src"] if image_tag and image_tag.has_attr("data-src") else ""

                short_desc_tag = listing.find("div", class_="eapow-overview-short-desc")
                short_desc = short_desc_tag.get_text(strip=True) if short_desc_tag else ""

                # Add property to database
                property_obj = Property(
                    title=title,
                    price=price,
                    description=short_desc,
                    image_url=image_url,
                    url=full_link
                )
                session.add(property_obj)

                # Also keep in local list
                all_properties.append({
                    "title": title,
                    "price": price,
                    "url": full_link,
                    "image": image_url,
                    "description": short_desc
                })

            except Exception as e:
                print(f"Error parsing listing: {e}")

        time.sleep(1)  # polite delay

    session.commit()
    session.close()
    print(f"Scraped {len(all_properties)} properties total.")
    return all_properties
