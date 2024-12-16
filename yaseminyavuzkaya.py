import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Film Review Generator", page_icon=":robot:", initial_sidebar_state="expanded")
st.title("Film Review Generator")
st.write("Enter a movie title to get a review.")

api_key = os.getenv("GEMINI_API_KEY")
if api_key is None:
    st.error("API key not found in environment variables. Please set the 'GEMINI_API_KEY' variable in your .env file.")
    st.stop()

try:
    genai.configure(api_key=api_key)
except Exception as e:
    st.error(f"Error configuring Gemini API: {e}")
    st.stop()


@st.cache_resource
def get_gemini_response(prompt):
    # Modelin Ayar Kısmı
    generation_config = {
        "temperature": 0.9,
        "top_p": 0.90,
        "top_k": 64,
        "max_output_tokens": 18192,
        "response_mime_type": "text/plain",
    }

    safety_settings = [
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_NONE",
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE",
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE",
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE",
        },
    ]

    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash-latest",
        safety_settings=safety_settings,
        generation_config=generation_config,
    )

    prompt_token_count = model.count_tokens(prompt)

    response = model.generate_content(prompt)

    response_token_count = model.count_tokens(response.text)

    return response.text, prompt_token_count, response_token_count # Return only the text


film_name = st.text_input("Movie Title", max_chars=100, placeholder="e.g., The Shawshank Redemption")

if st.button("Get Review"):
    if film_name.strip():
        prompt = f"Write a detailed and thoughtful review about the movie '{film_name}'."
        with st.spinner("Generating review..."):
            review_text, prompt_tokens, response_tokens = get_gemini_response(prompt) # Get only the text
            if review_text:
                st.subheader("Movie Review")
                st.markdown(review_text) # Display the review only once here
    else:
        st.error("Please enter a movie title.")

if st.button("IMDB RATING"):
    if film_name.strip():
        prompt = f"Write IMDB raitind of the film '{film_name}'."
        with st.spinner("IMDB rating"):
            review_text, prompt_tokens, response_tokens = get_gemini_response(prompt)  # Get only the text
            if review_text:
                st.subheader("IMDB rating")
                st.markdown(review_text)  # Display the review only once here

if st.button("FILM CASTING"):
    if film_name.strip():
        prompt = f"Write casting of the film '{film_name}'."
        with st.spinner("Film Casting"):
            review_text, prompt_tokens, response_tokens = get_gemini_response(prompt)  # Get only the text
            if review_text:
                st.subheader("Film Casting")
                st.markdown(review_text)