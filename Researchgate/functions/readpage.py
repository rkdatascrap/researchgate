import time
from playwright.sync_api import sync_playwright
import logging


def read_full_page_content(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        # Adjust viewport size for better visibility
        page.set_viewport_size({"width": 1200, "height": 800})
        page.goto(url,timeout=200000)
        #page to load fully
        #page.wait_for_load_state("networkidle")
        time.sleep(5)
        
        # Scroll to the bottom
        #page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        #time.sleep(5)

        #to expand author
        try:
            page.wait_for_selector('xpath=/html/body/div[2]/main/section/section[1]/div/div/div[4]/div/span[1]')
            # Click the element
            page.click('xpath=/html/body/div[2]/main/section/section[1]/div/div/div[4]/div/span[1]')
            logging.info("author list expanded")
        except:
            logging.info("author list not expanded")
        time.sleep(2)
        # Get the HTML content of the entire page
        full_page_content = page.content()
        
        # Close the browser
        browser.close()
        logging.info(url)
        logging.info("url read complete and returned ")
        return full_page_content

        

def fun(url):
    logging.info("reading: "+ url)
    full_page_content = read_full_page_content(url)
    return full_page_content