import requests
from bs4 import BeautifulSoup
import time
import re
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

# --- CONFIG ---
webhook_url = 'https://discord.com/api/webhooks/1410152967717519390/-vDrVmbY07yI8geD53EyyokC8PORAs7fUzfdQbO9N9hfrPEbdlExfRWQgTs6e0KPWf0e'  # Replace with your Discord webhook
keywords = ['proxynets', 'alexjamescunn@gmail.com', 'Rax', 'RAX', 'geskorian', 'Hull', 'grave_ace', 'kingston upon hull', 'kingston upon hull', 'hull', '5.198.84.128', 'Alex james cunningham', 'd', 'h',]  # Your info to monitor
scan_interval = 180  # seconds, adjust for scan speed
alerted_urls = set()  # Prevent duplicate alerts

# List of doxxing sources (expandable)
dox_sites = [
    'https://doxbin.org/recent',
    'https://doxbin.net/',
    'https://rarbin.com/',
    'https://doxxing.site/home',
    'https://doxbin.online',
    'https://ghostbin.fun',
    'https://leak-search.com/',



    # Add more real/pastebin style sites
]

# --- FUNCTIONS ---
def notify_discord(message, url, severity="High"):
    """Send rich Discord embed alert with severity and timestamp"""
    timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')
    colors = {"Low": 65280, "Medium": 16753920, "High": 16711680}  # Green, Orange, Red
    embed = {
        "embeds": [
            {
                "title": f"⚠️ Dox Alert [{severity}] ⚠️",
                "description": f"{message}",
                "url": url,
                "color": colors.get(severity, 16711680),
                "footer": {"text": f"Detected at {timestamp}"},
                "fields": [
                    {"name": "Keywords Found", "value": ', '.join(keywords), "inline": True}
                ]
            }
        ]
    }
    requests.post(webhook_url, json=embed)

def scan_site(url):
    """Scrape a doxxing site and check for keywords"""
    try:
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            text = r.text.lower()
            matches = [kw for kw in keywords if re.search(re.escape(kw.lower()), text)]
            if matches and url not in alerted_urls:
                message = f"Found your info ({', '.join(matches)}) on {url} ❗"
                notify_discord(message, url, severity="High")
                alerted_urls.add(url)
                print(message)
        else:
            print(f"Failed to fetch {url}: Status {r.status_code}")
    except Exception as e:
        print(f"Error scanning {url}: {e}")

def multi_site_scan():
    """Scan all sites concurrently for speed"""
    with ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(scan_site, dox_sites)

# --- MAIN LOOP ---
print("Hyper Scan Activated, Scanning hundreds of sources in real-time...")
while True:
    multi_site_scan()
    time.sleep(scan_interval)
