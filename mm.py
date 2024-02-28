import requests

def fetch_latest_news(keyword):
    API_KEY = '849436492be140a7917b86738816ae95'  # Replace with your NewsAPI key
    BASE_URL = 'https://newsapi.org/v2/everything'  # Use 'top-headlines' if you prefer
    params = {
        'q': keyword,
        'pageSize': 5,  # Fetch 5 articles
        'apiKey': API_KEY,
    }
    
    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        articles = response.json().get('articles', [])
        for article in articles:
            print(f"Title: {article['title']}")
            print(f"Description: {article['description']}")
            print(f"URL: {article['url']}\n")
    else:
        print(f"Failed to fetch news articles. Status code: {response.status_code}")

# Example usage
keyword = 'technology'  # Replace with your keyword of interest
fetch_latest_news(keyword)
