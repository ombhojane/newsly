import streamlit as st
import requests
from bs4 import BeautifulSoup
from transformers import pipeline


# Function to fetch news based on region or search query
def fetch_news(region, api_key, query=None):
    if query:
        BASE_URL = 'https://newsapi.org/v2/everything'
        params = {
            'q': query,
            'pageSize': 5,
            'apiKey': api_key,
        }
    else:
        BASE_URL = 'https://newsapi.org/v2/top-headlines'
        params = {
            'country': region.lower(),
            'pageSize': 5,
            'apiKey': api_key,
        }
    response = requests.get(BASE_URL, params=params)
    return response.json() if response.status_code == 200 else None

summarizer = pipeline("summarization")

# Scraper tool to get full article content
def scrape_article_content(url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        paragraphs = soup.find_all('p')
        article_text = ' '.join(paragraph.get_text(strip=True) for paragraph in paragraphs)
        return article_text
    else:
        return "Failed to retrieve the webpage"

# Function to summarize the article
def summarize_article(article_text):
    max_chunk_size = 1024  # Maximum size for the model input
    summarized_text = ""
    if len(article_text) > max_chunk_size:
        # Split the article into chunks
        chunks = [article_text[i:i+max_chunk_size] for i in range(0, len(article_text), max_chunk_size)]
        for chunk in chunks:
            summary = summarizer(chunk, max_length=120, min_length=30, do_sample=False)
            summarized_text += summary[0]['summary_text'] + " "
    else:
        summary = summarizer(article_text, max_length=120, min_length=30, do_sample=False)
        summarized_text = summary[0]['summary_text']
    return summarized_text

# Custom function to display news article card with summarization option
def display_news_card_with_summarization(article):
    with st.container():
        col1, col2 = st.columns([1, 2])
        with col1:
            if article['urlToImage']:
                st.image(article['urlToImage'], use_column_width=True)
            else:
                st.write("No image available")
        with col2:
            st.subheader(article['title'])
            st.write(article['description'])
            if st.button('Read Full Article', key=article['title']):
                with st.spinner('Fetching full article...'):
                    full_content = scrape_article_content(article['url'])
                    st.markdown(full_content)  # Display the full article content
            if st.button('Summarize', key=f"summarize_{article['title']}"):
                with st.spinner('Summarizing...'):
                    full_content = scrape_article_content(article['url'])
                    summary = summarize_article(full_content)
                    st.markdown(summary)  # Display the summarized content
            st.markdown(f"[Read more]({article['url']})", unsafe_allow_html=True)


def app():
    st.title('News Highlights')

    # Sidebar for user input
    region = st.sidebar.text_input("Enter your country code", value='in').lower()
    API_KEY = "690782566c704f90bc1827be4976e3c6"  # Use your actual NewsAPI key
    search_query = st.sidebar.text_input("Search for news")

    # Fetch and display news based on the user's input
    if API_KEY:
        news_data = fetch_news(region, API_KEY, query=search_query)
        if news_data and news_data['status'] == 'ok':
            st.markdown("## News Results")
            articles = news_data.get('articles', [])
            for article in articles:
                display_news_card_with_summarization(article)
        else:
            st.error("Failed to fetch news articles.")
    else:
        st.error("Please enter your News API Key to fetch news.")

if __name__ == "__main__":
    app()