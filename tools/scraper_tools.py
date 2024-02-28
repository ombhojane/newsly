import requests
from bs4 import BeautifulSoup
from langchain.tools import tool

class ScraperTool():
  @tool("Scraper Tool")
  def scrape(url: str):
    """Useful tool to scrape website content, use to learn more about a given url."""

    headers = {
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

    response = requests.get(url, headers=headers)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all paragraphs or any other elements you're interested in
        paragraphs = soup.find_all('p')
        
        # Extract and concatenate the text from each paragraph
        text = ' '.join(paragraph.get_text(strip=True) for paragraph in paragraphs)
        
        return text
    else:
        print("Failed to retrieve the webpage")
