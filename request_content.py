import requests
from bs4 import BeautifulSoup

class GetContentByRequest:
    def __init__(self):
        pass

    def get_content(self, url):
      try:
          headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
          post = requests.get(url, headers=headers, timeout=10)
          if post.status_code == 200:
            soup = BeautifulSoup(post.text, 'html.parser')
            for script in soup(["script", "style"]):
                script.decompose()
            text_content = soup.get_text(separator=" ", strip=True)
            mailto_links = [a['href'] for a in soup.find_all('a', href=True) if a['href'].startswith("mailto:")]
            combined_result = text_content + "\n" + "\n".join(mailto_links)
            return combined_result        
          else:
              return None
      except requests.RequestException as e:
          print(f"Error fetching {url}: {e}")
          return None
      
