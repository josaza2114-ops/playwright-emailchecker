from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)

    ##This line loads the saved state, it also can be saved into an auth folder if prohect size were to increase
    context = browser.new_context(
        storage_state="storage_state.json"
        ) 
    page = context.new_page()
    page.goto("https://gmail.com")

    emails = page.locator("div.UI table tr")

    new_emails = [] 

    for email in emails.all():
        if email.locator("td li[data-tooltip='Mark as unread']").count() == 0:
            sender = email.locator("td span[email]:visible").inner_text()
            title = email.locator("td span[data-thread-id]:visible").inner_text()
            new_emails.append([sender, title])

    if len(new_emails) == 0:
        print("No new emails found.")
    else:
        for sender, title in new_emails:
            print(f"New email from {sender}: {title}")
            print("----------------------------------") 
        print("Total new emails:", len(new_emails))
    
    context.close()