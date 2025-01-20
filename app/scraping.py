import requests
from bs4 import BeautifulSoup

def scrape_homepage(url: str) -> str:
    """
    Fetches the homepage HTML from the given URL and extracts text content.
    Returns the text for further processing.
    """
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/108.0.0.0 Safari/537.36"
        )
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        raise ValueError(f"Failed to retrieve the URL: {e}")

    soup = BeautifulSoup(response.text, "html.parser")
    body = soup.body
    text = body.get_text(separator=' ', strip=True) if body else soup.get_text(separator=' ', strip=True)
    return text
