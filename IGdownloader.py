import os, requests, time
from playwright.sync_api import sync_playwright

INPUT_FILE = "input.txt"
OUTPUT_DIR = "downloads"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def get_video_url_playwright(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, timeout=60000)
        page.wait_for_selector("video", timeout=15000)
        video_src = page.locator("video").get_attribute("src")
        browser.close()
        if not video_src:
            raise Exception("Video tag not found or missing src")
        return video_src

def save_video(video_url, filename):
    filepath = os.path.join(OUTPUT_DIR, filename)
    r = requests.get(video_url, stream=True)
    with open(filepath, "wb") as f:
        for chunk in r.iter_content(chunk_size=8192):
            f.write(chunk)
    return filepath

with open(INPUT_FILE, "r") as f:
    urls = [line.strip() for line in f if line.strip()]

for url in urls:
    short_id = url.split("/")[-2]
    filename = f"{short_id}.mp4"
    try:
        print(f"[INFO] Scraping IG → {url}")
        video_url = get_video_url_playwright(url)
        path = save_video(video_url, filename)
        print(f"[SUCCESS] Saved → {path}")
    except Exception as e:
        print(f"[ERROR] {url} → {e}")
    time.sleep(2)
