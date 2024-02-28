# topic_selection.py
import streamlit as st

def app():
    st.title("Select Topics of Interest")
    st.markdown("Choose your favorite topics from the list below to tailor the news feed to your interests.")

    topics = [
        "Education", "Food", "Travel", "Health", "Science", 
        "Business", "Entertainment", "Sports", "Tech", "Politics"
    ]
    
    # Initialize an empty list to store user's selected topics
    user_topics = []
    
    # Generate a checkbox for each topic
    for topic in topics:
        if st.checkbox(topic, key=topic):
            user_topics.append(topic)
    
    # Store the selected topics in the session state
    if user_topics:
        st.session_state['user_topics'] = user_topics
        st.success("Topics selected successfully! Proceed to the next page to view news.")
