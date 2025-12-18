import os
from firecrawl import FirecrawlApp, V1ScrapeOptions
from dotenv import load_dotenv

load_dotenv()

class FirecrawlService:
    def __init__(self):
        api_key = os.getenv("FIRECRAWL_API_KEY")
        if not api_key:
            raise ValueError("FIRECRAWL_API_KEY Missing.")
        self.app = FirecrawlApp(api_key = api_key)

    def search_companies(self, query: str, num_result: int = 5):
        try:
            response = self.app.search(
                query=f"{query} company pricing",
                limit=num_result,
                scrape_options={
                    "formats": ["markdown"]
                }
            )

            # ✅ Firecrawl v2 returns SearchData
            if hasattr(response, "data"):
                return response.data or []

            # ✅ If already a list
            if isinstance(response, list):
                return response

            # ✅ If dict (defensive)
            if isinstance(response, dict):
                return list(response.values())

            return []

        except Exception as e:
            print(f"[Firecrawl search error] {e}")
            return []

    def scrap_company_pages(self, url: str):
        try:
            options = {
                "formats":["markdown"],
                "onlyMainContent":True
            }

            result = self.app.scrape_url(url, options)
            return result

        except Exception as e:
            print("Firecrawl scrape error:", e)
            return None
