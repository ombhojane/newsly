import streamlit as st
import requests
import random

API_KEY = 'api'  # Replace with your actual NewsAPI key

def fetch_news_across_categories(pageSize=5):
    BASE_URL = 'https://newsapi.org/v2/top-headlines'
    categories = ["business", "entertainment", "general", "health", "science", "sports", "technology"]
    all_articles = []

    # Fetch news from each category
    for category in categories:
        params = {
            'category': category,
            'pageSize': 2,  # Adjust based on how many articles you want from each category
            'apiKey': API_KEY,
            'country': 'us'
        }
        response = requests.get(BASE_URL, params=params)
        if response.status_code == 200:
            articles = response.json().get('articles', [])
            all_articles.extend(articles)

    # Randomly select articles to display
    if len(all_articles) > pageSize:
        displayed_articles = random.sample(all_articles, pageSize)
    else:
        displayed_articles = all_articles
    
    return displayed_articles

def display_news_with_feedback(session_state_key):
    if 'generate_more' not in st.session_state:
        st.session_state['generate_more'] = False

    if session_state_key not in st.session_state or st.session_state['generate_more']:
        st.session_state[session_state_key] = {
            'user_responses': [],
            'articles_to_display': fetch_news_across_categories(),
        }
        # Reset the generate_more flag after fetching new articles
        st.session_state['generate_more'] = False

    state = st.session_state[session_state_key]

    for idx, article in enumerate(state['articles_to_display']):
        with st.container():
            if article['urlToImage']:
                st.image(article['urlToImage'], width=300)
            st.markdown(f"#### {article['title']}")
            st.markdown(article['description'])
            feedback_col1, feedback_col2 = st.columns([0.1, 1])
            with feedback_col1:
                like = st.button("👍", key=f"like_{idx}")
            with feedback_col2:
                dislike = st.button("👎", key=f"dislike_{idx}")

            if like:
                state['user_responses'].append({'title': article['title'], 'response': 'like'})
                st.success("Liked!")
            if dislike:
                state['user_responses'].append({'title': article['title'], 'response': 'dislike'})
                st.error("Disliked!")

    st.session_state['final_user_responses'] = state['user_responses']

    # Place the "Generate More" button outside the loop to avoid duplication
    if st.button('Generate More'):
        st.session_state['generate_more'] = True
        # Refresh the page to apply the changes
        st.experimental_rerun()

def app():
    st.title("News Display and Feedback")

    display_news_with_feedback('news_feedback')

if __name__ == "__main__":
    app()
