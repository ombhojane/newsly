import json
import streamlit as st
import google.generativeai as genai

# Assume the API key is set properly in your environment
genai.configure(api_key="api")

generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

def generate_gemini_prompt(user_responses, user_topics):
    liked_articles = "\n".join([f"- {resp['title']}" for resp in user_responses if resp['response'] == 'Liked'])
    disliked_articles = "\n".join([f"- {resp['title']}" for resp in user_responses if resp['response'] == 'Disliked'])
    topics_list = "\n".join([f"- {topic}" for topic in user_topics])

    prompt_parts = [
        "Based on the following user responses to news articles and their selected topics of interest, predict the user's interests and suggest content themes that might appeal to them.",
        "\n\nLiked Articles:\n" + liked_articles,
        "\n\nDisliked Articles:\n" + disliked_articles,
        "\n\nSelected Topics:\n" + topics_list,
        "\n\nWhat are the user's interests and what content themes should we focus on to cater to their preferences?"
    ]

    return "\n".join(prompt_parts)

def generate_gemini_prompt2(user_responses, user_topics):
  
    prompt_parts = [
        f"""User Topics : {user_topics}. User responses : {user_responses}. Based on the following user responses to news articles and their selected topics of interest, predict the user's interests. Provide the predicted interests in a structured array format.",
        
        User's Interests in Array Format (e.g., [\"Interest 1\", \"Interest 2\"]):"""
    ]

    return (prompt_parts)


# Example usage in your Streamlit app
def app():
    st.title("Display User Responses and Predict Interests")
   

    if 'final_user_responses' in st.session_state and 'user_topics' in st.session_state:
        responses = st.session_state['final_user_responses']
        topics = st.session_state['user_topics']

        if responses:
            st.write("User's Liked and Disliked Articles:")
            for response in responses:
                st.markdown(f"- **{response['title']}**: {response['response']}")
        else:
            st.write("No responses have been recorded.")

        # Generate first prompt and send to Gemini
        prompt1 = generate_gemini_prompt2(responses, topics)
        response = model.generate_content(prompt1)
        st.subheader("Predicted Interests and Suggested Content Themes from Prompt 1:")
        st.write(response.text)
        st.session_state['predicted_interests'] = response.text

    else:
        st.write("No responses or topics have been recorded.")

if __name__ == "__main__":
    app()
