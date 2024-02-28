# app.py
import streamlit as st
import topic_selection
import news_display
import display
import recommended_news_dashboard
import summarizer
import highlights

# Define the pages for each section
SECTIONS = {
    "Onboarding": {
        "Step 1 - Select Topics of Interest": topic_selection,
        "Step 2 - News Segmentation": news_display,
        "Step 3 - Display Interests": display,
    },
    "Personalized Feed": {
        "News Based on Your Interests": recommended_news_dashboard,
    },
    "Summarization": {
        "Summarization": summarizer,
    },
    "Breaking Alerts": {
        "Highlights": highlights,
    },
}

def main():
    st.sidebar.title('Main Menu')

    # Collect all section names and allow the user to select a section
    section = st.sidebar.selectbox("Choose a Section", options=list(SECTIONS.keys()))

    # Once a section is selected, dynamically generate the selectbox for pages within that section
    if section:
        pages = SECTIONS[section]
        selected_page = st.sidebar.selectbox("Choose a Page", options=list(pages.keys()))

        # Display the selected page
        page = pages[selected_page]
        page.app()

if __name__ == "__main__":
    main()
