# streamlit_app.py
import streamlit as st
import os
from contextlib import redirect_stdout
import io
from crewai import Agent, Task, Crew, Process
from tools.scraper_tools import ScraperTool
from langchain.chat_models import ChatOpenAI

# Assuming OPENAI_API_KEY is already set in your environment for simplicity
os.environ["OPENAI_API_KEY"] = "api"

scrape_tool = ScraperTool().scrape
llm = ChatOpenAI(model='gpt-3.5-turbo')

class NewsletterCrew:
    def __init__(self, urls):
        self.urls = urls.split(',')  # Splitting URLs assuming they're comma-separated

    def run(self):
        scraper = Agent(
            role='Summarizer of Websites',
            goal='Scrape the content from the provided URLs and pass the full content to the writer agent for summarization',
            backstory="Expert in extracting text content from websites for analysis.",
            verbose=True,
            allow_delegation=False,
            tools=[scrape_tool],
            llm=llm
        )
        writer = Agent(
            role='Tech Content Summarizer and Writer',
            goal='Create engaging summaries of AI advancements from the scraped content',
            backstory="Skilled at transforming complex tech articles into digestible summaries.",
            verbose=True,
            allow_delegation=True,
            llm=llm
        )

        task1 = Task(
            description=f"Scrape and compile content from the following URLs: {self.urls}",
            agent=scraper
        )
        task2 = Task(
            description="Summarize the compiled content into a short, engaging format.",
            agent=writer
        )

        process = Crew(
            agents=[scraper, writer],
            tasks=[task1, task2],
            verbose=2
        )

        result = process.kickoff()
        return result  # This needs to be implemented based on your Crew and Task logic

def app():
    st.title("Newsletter Scraper and Summarizer")

    urls = st.text_input("Enter URLs to scrape and summarize, separated by commas:")

    if st.button("Run Newsletter Crew"):
        with io.StringIO() as buf, redirect_stdout(buf):
            if urls:
                newsletter_crew = NewsletterCrew(urls)
                result = newsletter_crew.run()
                logs = buf.getvalue()

                st.subheader("Summary Result")
                st.write(result or "No result returned.")

                st.subheader("Terminal Logs")
                st.text_area("Logs", value=logs, height=300)
            else:
                st.error("Please enter at least one URL.")

if __name__ == "__main__":
    app()
