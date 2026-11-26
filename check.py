import os, requests
from playwright.sync_api import sync_playwright

URL = "https://in.bookmyshow.com/cinemas/CHEN/rakki-cinemas-omr-kelambakkam/buytickets/RAKK/20261217"
DATE = "20261217"
KEYWORD = "doomsday"
TOPIC = os.environ["NTFY_TOPIC"]

def notify(title, msg):
    requests.post(f"https://ntfy.sh/{TOPIC}", data=msg.encode(),
                  headers={"Title": title, "Priority": "urgent", "Click": URL})

with sync_playwright() as p:
    b = p.chromium.launch()
    ctx = b.new_context(locale="en-IN", timezone_id="Asia/Kolkata",
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36")
    page = ctx.new_page()
    page.goto(URL, wait_until="networkidle", timeout=60000)
    page.wait_for_timeout(4000)
    html = page.content().lower()
    print("final url:", page.url, "| length:", len(html))
    print("title:", page.title())
    print("text:", page.inner_text("body")[:600].replace("\n", " | "))
    page.screenshot(path="shot.png", full_page=True)
    if "access denied" in html or len(html) < 5000:
        print("Looks blocked")
    elif DATE in page.url and KEYWORD in html:
        notify("BOOK NOW: Doomsday at Rakki OMR", "Dec 17 is open and Doomsday is listed")
    b.close()
