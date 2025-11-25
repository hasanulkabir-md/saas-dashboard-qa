from playwright.sync_api import sync_playwright
import uuid

def test_create_user():
    unique_email = f"test_{uuid.uuid4().hex[:8]}@example.com"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto("http://localhost:3000")

        page.fill("[data-testid='name']", "Test User")
        page.fill("[data-testid='email']", unique_email)
        page.click("[data-testid='add-user']")

        # wait for the created email to appear in the list
        page.wait_for_timeout(2000)
        page.wait_for_selector(f"text={unique_email}", timeout=5000)

        body_text = page.inner_text("body")
        print("\nPAGE TEXT AFTER CREATE:\n", body_text, "\n")

        assert unique_email in body_text

        browser.close()
