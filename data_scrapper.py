def scrape_bbc_news_with_selenium(url, output_file):
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.service import Service
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC

        from bs4 import BeautifulSoup
        from datetime import datetime
        import csv
        import time
        import os

        options = Options()
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--log-level=3")

        service = Service("chromedriver.exe")
        driver = webdriver.Chrome(service=service, options=options)

        print("🔄 Opening BBC News...")
        driver.get(url)

        try:
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "main"))
            )
            print("✅ Main content loaded.")
        except:
            print("⚠️ Timeout. Couldn't detect main container.")
            driver.save_screenshot("bbc_debug.png")
            print("📸 Screenshot saved as 'bbc_debug.png'")
            return []

        # Scroll to bottom to trigger lazy loading
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)

        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Use href pattern instead of class (since classes are obfuscated)
        article_tags = soup.select("a[href^='/news'], a[href^='/business'], a[href^='/sport'], a[href^='/world']")

        if not article_tags:
            print("⚠️ Still no articles found. Saving HTML for inspection...")
            with open("bbc_debug.html", "w", encoding="utf-8") as f:
                f.write(soup.prettify())
            driver.save_screenshot("bbc_debug2.png")
            print("📸 Screenshot and HTML saved. Check bbc_debug2.png and bbc_debug.html")
            driver.quit()
            return []

        data = []
        seen = set()
        for article in article_tags:
            href = article.get("href", "")
            title = article.get_text(strip=True)

            # Skip navigation links like "/news"
            if href.count('/') <= 2 or not title or href in seen:
                continue

            if href.startswith("/"):
                href = "https://www.bbc.com" + href

            seen.add(href)
            data.append({"title": title, "link": href})

        if data:
            with open(output_file, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=["title", "link"])
                writer.writeheader()
                writer.writerows(data)
            print(f"\n✅ Saved {len(data)} articles to {output_file}")
        else:
            print("⚠️ No data found to save.")

        driver.quit()
        return data

    except Exception as e:
        print(f"❌ Error: {e}")
        return []
    
if __name__ == "__main__":
    scrape_bbc_news_with_selenium("https://www.bbc.com/news", "bbc_articles.csv")
