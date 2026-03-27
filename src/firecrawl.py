import os
from typing import Any, Dict, List
from firecrawl import FirecrawlApp
from dotenv import load_dotenv

load_dotenv()

class FirecrawlService:
    def __init__(self):
        api_key = os.getenv("FIRECRAWL_API_KEY")
        if not api_key:
            raise ValueError("Missing FIRECRAWL_API_KEY environment variable ")
        self.app = FirecrawlApp(api_key=api_key)

    def _item_to_dict(self, item: Any) -> Dict[str, Any]:
        if isinstance(item, dict):
            return item

        if hasattr(item, "model_dump"):
            return item.model_dump()

        return {
            "url": getattr(item, "url", ""),
            "markdown": getattr(item, "markdown", ""),
            "metadata": getattr(item, "metadata", {}) or {},
        }

    def search_companies(self, query: str, num_results: int = 5) -> List[Dict[str, Any]]:
        try:
            result = self.app.search(
                query = f"{query} company pricing",
                limit = num_results,
                scrape_options = {
                    "formats" : ["markdown"],
                },

            )

            data = getattr(result, "data", [])
            if not isinstance(data, list):
                data = []

            return [self._item_to_dict(item) for item in data]
        except Exception as e:
            print(f"Error during search: {e}")
            return []
        
    def scrape_company_pages(self, url: str) -> str:
        try:
            if not url:
                return ""

            result = self.app.scrape(
                url,
                formats = ["markdown"],
            )

            if isinstance(result, dict):
                return result.get("markdown", "")

            if hasattr(result, "markdown"):
                return result.markdown or ""

            if hasattr(result, "model_dump"):
                payload = result.model_dump()
                return payload.get("markdown", "")

            return ""
        except Exception as e:
            print(f"Error during scraping: {e}")
            return ""
        