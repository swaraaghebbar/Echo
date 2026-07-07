import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


def analyze_image(image_path):
    # Convert to absolute path
    image_path = os.path.abspath(image_path)

    # --- Browser setup ---
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-infobars")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    # --- Open Google Lens ---
    driver.get("https://lens.google.com/upload")
    time.sleep(2)

    # --- Upload image ---
    upload_input = driver.find_element(By.CSS_SELECTOR, "input[type='file']")
    upload_input.send_keys(image_path)

    # Wait for Lens to load preview UI
    time.sleep(5)

    # Trigger search (Lens auto-searches but some versions need scroll/enter)
    driver.find_element(By.TAG_NAME, "body").send_keys(Keys.PAGE_DOWN)

    # Wait for results
    time.sleep(5)

    # --- SCRAPER FUNCTION ---
    def scrape_lens_results(driver):
        time.sleep(2)

        # Primary results block you found
        try:
            block = driver.find_element(By.CSS_SELECTOR, 'div[jsname="dvXlsc"]')
            text = block.text.strip()
            if text:
                return text
        except Exception as e:
            print("Selector dvXlsc failed:", e)

        # Secondary block (sometimes used)
        try:
            alt = driver.find_element(By.CSS_SELECTOR, 'div[jsname="E2Gq5e"]')
            text = alt.text.strip()
            if text:
                return text
        except:
            pass

        # Tile-style fallback
        try:
            tiles = driver.find_elements(By.CSS_SELECTOR, 'div[jsname="Cpkphb"]')
            combined = "\n".join([t.text for t in tiles if t.text.strip()])
            if combined.strip():
                return combined
        except:
            pass

        return None

    # --- Call scraper ---
    result = scrape_lens_results(driver)

    # Close browser
    driver.quit()

    # Return readable result
    return result if result else "No results found."
