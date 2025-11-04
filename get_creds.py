from playwright.sync_api import sync_playwright

from dotenv import load_dotenv
import os

load_dotenv()

email = os.getenv("EMAIL_ADDRESS")
password = os.getenv("EMAIL_PASSWORD")
url = os.getenv("GMAIL_URL")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, args=["--disable-blink-features=AutomationControlled","--disable-dev-shm-usage"])
    context = browser.new_context()
    page = context.new_page()

    
    page.goto(url)
    page.get_by_label("Email or phone").fill(email)
    page.get_by_role("button", name="Next").click()
    page.get_by_label("Enter your password").fill(password)
    page.get_by_role("button", name="Next").click()
    page.pause()

    context.storage_state(path="storage_state.json")
    
    browser.close()