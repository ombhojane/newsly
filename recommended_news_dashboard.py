import streamlit as st
import requests
from bs4 import BeautifulSoup
import os
from contextlib import redirect_stdout
import io
from crewai import Agent, Task, Crew, Process
from tools.scraper_tools import ScraperTool
from langchain.chat_models import ChatOpenAI

# Function to fetch the latest news based on a keyword
def fetch_latest_news(keyword, API_KEY):
    BASE_URL = 'https://newsapi.org/v2/everything'  # Adjust if necessary
    params = {
        'q': keyword,
        'pageSize': 5,  # Number of articles to fetch
        'apiKey': API_KEY,
    }

    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        articles = response.json().get('articles', [])
        for article in articles:
            display_news_card(article)
    else:
        st.write(f"Failed to fetch news articles for '{keyword}'. Status code: {response.status_code}")
class ScraperTool():
    @staticmethod
    def scrape(url: str):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            paragraphs = soup.find_all('p')
            text = ' '.join(paragraph.get_text(strip=True) for paragraph in paragraphs)
            return text
        else:
            return "Failed to retrieve the webpage"

# Modify the display_news_card function to include a button that when clicked,
# calls the scrape function and displays the scraped content
def display_news_card(article):
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
            st.markdown(f"[Read More]({article['url']})", unsafe_allow_html=True)
            
            # Button to scrape and display content
            if st.button('Scrape Content', key=article['url']):
                scraped_content = ScraperTool.scrape(article['url'])
                st.expander("Scraped Content").write(scraped_content)

# The main app function
def app():
    st.title("Recommended News Dashboard")

    # Replace 'YOUR_API_KEY_HERE' with your actual NewsAPI key
    API_KEY = 'api'

    if 'predicted_interests' in st.session_state:
        interests = st.session_state['predicted_interests']

        # Ensure interests are in the correct format (a list of strings)
        if isinstance(interests, str):
            # Clean up and convert string to list if necessary
            interests = interests.strip("[]").replace('"', '').replace("'", "").split(", ")
        elif isinstance(interests, list):
            # Further clean up if necessary (for lists containing a single string with multiple interests)
            if len(interests) == 1 and ',' in interests[0]:
                interests = interests[0].split(", ")
        
        # Display news for each cleaned interest
        for interest in interests:
            interest_cleaned = interest.strip()  # Remove any leading/trailing whitespace
            st.subheader(f"News for: {interest_cleaned}")
            fetch_latest_news(interest_cleaned, API_KEY)
    else:
        st.write("No predicted interests found.")

if __name__ == "__main__":
    app()
