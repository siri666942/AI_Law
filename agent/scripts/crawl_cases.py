import argparse
import json
import time
import requests
from bs4 import BeautifulSoup

def fetch(url, timeout=20):
    r = requests.get(url, timeout=timeout, headers={"User-Agent": "Mozilla/5.0"})
    r.raise_for_status()
    return r.text

def parse(html):
    soup = BeautifulSoup(html, "lxml")
    title = soup.title.string if soup.title else ""
    body = soup.get_text(separator="\n")
    return title, body

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--urls_file", type=str, required=True)
    parser.add_argument("--output", type=str, required=True)
    parser.add_argument("--sleep", type=float, default=1.0)
    args = parser.parse_args()
    with open(args.urls_file, "r", encoding="utf-8") as f:
        urls = [x.strip() for x in f if x.strip()]
    out = []
    for u in urls:
        try:
            html = fetch(u)
            title, text = parse(html)
            out.append({"url": u, "title": title, "content": text})
            time.sleep(args.sleep)
        except Exception as e:
            out.append({"url": u, "error": str(e)})
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
