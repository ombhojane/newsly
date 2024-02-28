# review_interests.py
import streamlit as st
import json

def load_interests():
    try:
        with open('user_interests.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def app():
    st.title('Review Your Interests')

    interests = load_interests()
    if interests:
        st.write("Your Interests:")
        for interest in interests:
            st.write("- ", interest)
    else:
        st.write("No interests selected.")
