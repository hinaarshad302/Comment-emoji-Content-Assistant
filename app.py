import os
import streamlit as st
from google import genai
from google.genai import types

# Page configuration
st.set_page_config(
    page_title="Comment & Emoji Content Assistant",
    page_icon="✍️",
    layout="centered"
)

st.title("✍️ Comment & Emoji Content Assistant")
st.write("Generate tailored posts with customized tones, emojis, and hashtags.")

# Sidebar for API Configuration
with st.sidebar:
    st.header("Configuration")
    api_key_input = st.text_input(
        "Enter Gemini API Key:",
        type="password",
        help="Get your key at https://aistudio.google.com/"
    )
    # Priority: user input > environment variable
    api_key = api_key_input or os.environ.get("GEMINI_API_KEY")

# Input Form
with st.form("content_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        platform = st.selectbox(
            "Platform",
            ["LinkedIn", "Instagram", "X (Twitter)", "Facebook", "TikTok"]
        )
        content_type = st.selectbox(
            "Content Type",
            ["Short Post", "Educational / Explainer", "Story / Case Study", "Announcement", "Opinion / Hot Take"]
        )
        tone = st.selectbox(
            "Tone",
            ["Professional & Authoritative", "Casual & Friendly", "Bold & Controversial", "Witty & Humorous", "Inspirational"]
        )

    with col2:
        topic = st.text_input("Topic", placeholder="e.g., Remote Work Trends in 2026")
        target_audience = st.text_input("Target Audience", placeholder="e.g., Tech Professionals & Managers")
        emoji_density = st.select_slider(
            "Emoji Level",
            options=["Minimal", "Moderate", "High"]
        )

    additional_instructions = st.text_area(
        "Optional Context or Notes",
        placeholder="e.g., Include a key takeaway about productivity tools..."
    )

    submitted = st.form_submit_button("Generate Post 🚀")

# Generation Logic
if submitted:
    if not api_key:
        st.error("Please provide a Gemini API Key in the sidebar.")
    elif not topic or not target_audience:
        st.warning("Please fill in both the Topic and Target Audience fields.")
    else:
        try:
            # Initialize official Google GenAI Client
            client = genai.Client(api_key=api_key)

            # Construct Prompt
            prompt = f"""
            You are an expert social media strategist. Create a complete social media post based on these specifications:

            - Platform: {platform}
            - Content Type: {content_type}
            - Topic: {topic}
            - Target Audience: {target_audience}
            - Tone: {tone}
            - Emoji Usage: {emoji_density} (Use emojis appropriately throughout the text based on this level)
            - Extra Notes: {additional_instructions if additional_instructions else 'None'}

            Please format your response into three clear sections:
            1. **MAIN POST CONTENT**: Structure with an engaging hook, formatted body text tailored to {platform}'s style.
            2. **CAPTION & CALL TO ACTION**: A short engaging closing summary with a question to encourage comments.
            3. **HASHTAGS**: A block of 5-10 highly relevant, trending hashtags.
            """

            with st.spinner("Generating your content..."):
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt
                )

            st.success("Post Generated!")
            st.markdown("---")
            st.markdown(response.text)

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
