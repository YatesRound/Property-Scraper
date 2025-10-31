from playwright.sync_api import sync_playwright
import time

def scrape_jordan_halstead():
    print("Launching browser for Jordan & Halstead listings…")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=200)
        page = browser.new_page()
        url = "https://jordanandhalstead.co.uk/search-results/?keyword=&department=residential-sales"
        print(f"Loading: {url}")
        page.goto(url, timeout=60000)

        # Wait for property grid to load
        try:
            page.wait_for_selector("div[data-elementor-type='loop-item']", timeout=45000)
            print("Property grid loaded.")
        except Exception:
            print("❌ Property grid did **not** appear, stopping.")
            browser.close()
            return []

        # Keep clicking Load More until it disappears
        while True:
            try:
                load_more = page.locator("div.e-loop__load-more a")
                if load_more.is_visible():
                    print("Clicking Load More…")
                    load_more.click()
                    time.sleep(3)  # wait for new listings to load
                else:
                    print("No more 'Load More' button, stopping…")
                    break
            except Exception:
                print("Error clicking Load More, stopping…")
                break

        # Extract all property cards
        print("Extracting listings…")
        properties = []
        cards = page.query_selector_all("div[data-elementor-type='loop-item']")
        print(f"Found {len(cards)} property cards")

        for card in cards:
            try:
                title_el = card.query_selector(".elementor-widget-address-full")
                title = title_el.inner_text().strip() if title_el else None

                price_el = card.query_selector(".elementor-widget-property-price .price")
                price = price_el.inner_text().strip() if price_el else None

                link_el = card.query_selector("a.elementor-button-link")
                link = link_el.get_attribute("href") if link_el else None

                img_el = card.query_selector("img")
                img = img_el.get_attribute("src") if img_el else None

                bedrooms_el = card.query_selector(".elementor-widget-bedrooms")
                bedrooms = bedrooms_el.inner_text().strip() if bedrooms_el else None

                bathrooms_el = card.query_selector(".elementor-widget-bathrooms")
                bathrooms = bathrooms_el.inner_text().strip() if bathrooms_el else None

                properties.append({
                    "title": title,
                    "price": price,
                    "url": link,
                    "image": img,
                    "bedrooms": bedrooms,
                    "bathrooms": bathrooms
                })
            except Exception as e:
                print("Error parsing card:", e)

        browser.close()
        print(f"🎉 Done — scraped {len(properties)} properties total.")
        return properties
