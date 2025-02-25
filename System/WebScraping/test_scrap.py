import requests
from bs4 import BeautifulSoup


class AmazonProductExtractor:
    def __init__(self, url):
        self.url = url
        self.soup = self._get_soup()

    def _get_soup(self):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9",
        }
        response = requests.get(self.url, headers=headers)
        if response.status_code == 200:
            return BeautifulSoup(response.text, "html.parser")
        else:
            raise Exception(
                f"Failed to fetch page, status code: {response.status_code}"
            )

    def extract_title(self):
        title_tag = self.soup.find("span", id="productTitle")
        return title_tag.get_text(strip=True) if title_tag else None

    def extract_description(self):
        desc_tag = self.soup.find("div", id="productDescription")
        return desc_tag.get_text(strip=True) if desc_tag else None


# Example Usage
url = "https://www.amazon.in/Catwalk-Womens-Fashion-Sandals-7-3882BX-7/dp/B07JKTYMDV/ref=sr_1_245?qid=1679211656&s=shoes&sr=1-245"
extractor = AmazonProductExtractor(url)

print("Title:", extractor.extract_title())
print("Description:", extractor.extract_description())
