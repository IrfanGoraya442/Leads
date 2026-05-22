from playwright.sync_api import sync_playwright
import re
import time
import subprocess
import sys

def _ensure_chromium():
    try:
        subprocess.run(
            [sys.executable, "-m", "playwright", "install", "chromium"],
            check=True, capture_output=True
        )
    except Exception as e:
        print(f"[Scraper] playwright install warning: {e}")

_ensure_chromium()

class GoogleMapsScraper:

    def search(self, keyword: str, city: str, country: str, limit: int = 50, progress_cb=None) -> list[dict]:
        query = f"{keyword} in {city}, {country}"
        results = []

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True, args=["--no-sandbox", "--disable-dev-shm-usage", "--disable-gpu"])
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124 Safari/537.36"
            )
            page = context.new_page()

            try:
                # Step 1: Load search results
                url = f"https://www.google.com/maps/search/{query.replace(' ', '+')}"
                page.goto(url, wait_until="domcontentloaded", timeout=30000)
                time.sleep(3)

                # Step 2: Scroll to load more listings
                self._scroll_feed(page, limit, progress_cb)

                # Step 3: Collect all place URLs
                place_links = page.query_selector_all("a.hfpxzc")
                place_urls = []
                for a in place_links[:limit]:
                    href = a.get_attribute("href")
                    name = a.get_attribute("aria-label") or ""
                    if href:
                        place_urls.append((name, href))

                if progress_cb:
                    progress_cb(len(place_urls), limit, f"Found {len(place_urls)} listings, extracting details...")

                # Step 4: Visit each place URL and extract data
                for i, (name, href) in enumerate(place_urls):
                    data = self._extract_place(page, name, href)
                    if data:
                        results.append(data)
                    if progress_cb:
                        progress_cb(i + 1, len(place_urls), f"Extracting: {name[:40]}")
                    time.sleep(0.8)

            except Exception as e:
                print(f"[Scraper] Error: {e}")
            finally:
                browser.close()

        return results

    def _scroll_feed(self, page, limit: int, progress_cb=None):
        try:
            feed = page.locator('div[role="feed"]')
            prev = 0
            for _ in range(limit // 5 + 5):
                feed.evaluate("el => el.scrollBy(0, 3000)")
                time.sleep(1.5)
                count = page.locator("a.hfpxzc").count()
                if progress_cb:
                    progress_cb(count, limit, f"Loading listings... {count} found")
                if count >= limit or count == prev:
                    break
                prev = count
        except Exception:
            pass

    def _extract_place(self, page, name: str, href: str) -> dict | None:
        try:
            page.goto(href, wait_until="domcontentloaded", timeout=20000)
            time.sleep(2)

            def get_text(sel, timeout=2000):
                try:
                    return page.locator(sel).first.inner_text(timeout=timeout).strip()
                except Exception:
                    return None

            def get_attr(sel, attr, timeout=2000):
                try:
                    return page.locator(sel).first.get_attribute(attr, timeout=timeout)
                except Exception:
                    return None

            # Name — try multiple selectors, fall back to aria-label
            biz_name = (
                get_text("h1.DUwDvf") or
                get_text("h1") or
                name
            )
            # Strip Google Maps internal rendering prefixes like _arr, _fc, etc.
            if biz_name:
                biz_name = re.sub(r'^_[a-zA-Z]+\s*', '', biz_name).strip()

            # Phone — extract number from aria-label "Phone: +971 ..."
            phone_label = get_attr('button[aria-label*="Phone"]', "aria-label")
            phone = re.sub(r"^Phone:\s*", "", phone_label).strip() if phone_label else None

            # Address — extract from aria-label
            addr_label = get_attr('button[aria-label*="Avenue"], button[aria-label*="Street"], button[aria-label*="Road"], button[aria-label*="Dubai"], button[aria-label*="Floor"]', "aria-label")
            if not addr_label:
                # fallback: look for copy-address button
                addr_el = page.locator('[data-item-id="address"]').first
                try:
                    addr_label = addr_el.inner_text(timeout=1500).replace("", "").strip()
                except Exception:
                    addr_label = None

            # Website
            website = get_attr('a[data-item-id="authority"]', "href")

            # Category
            category = get_text("button.DkEaL")

            # Rating
            rating_raw = get_text("div.fontDisplayLarge")
            try:
                rating = float(rating_raw) if rating_raw else None
            except Exception:
                rating = None

            # Reviews count — from the reviews button aria-label
            reviews_label = get_attr('button[aria-label*="review"]', "aria-label")
            reviews_count = None
            if reviews_label:
                m = re.search(r"([\d,]+)", reviews_label)
                if m:
                    reviews_count = int(m.group(1).replace(",", ""))

            return {
                "business_name": biz_name,
                "category": category,
                "rating": rating,
                "reviews_count": reviews_count,
                "address": addr_label,
                "phone": phone,
                "website": website,
                "maps_url": page.url,
                "has_website": bool(website),
            }

        except Exception as e:
            print(f"[Scraper] Extract error for {name}: {e}")
            return None
