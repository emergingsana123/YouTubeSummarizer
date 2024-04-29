import streamlit as st
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io
from googletrans import Translator

# Set Streamlit page configuration
st.set_page_config(page_title="YouTube Video Summarizer", layout="wide")

# Permanent Google API Key
google_api_key = "AIzaSyCzPf0rX7LUBC4DiHlP1B3jBs0a0hT7B88"

# Sidebar for user inputs
youtube_link = st.sidebar.text_input("Enter YouTube Video Link:")

# Summary length customization
summary_length = st.sidebar.select_slider(
    "Select Summary Length:", options=['Short', 'Medium', 'Long'], value='Medium'
)

# Language translation
translator = Translator()

# Define functions
def extract_transcript_details(youtube_video_url):
    try:
        video_id = youtube_video_url.split("=")[1]
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return " ".join(segment["text"] for segment in transcript)
    except Exception as e:
        st.sidebar.error(f"An error occurred: {e}")
        return None

def generate_gemini_content(transcript_text, prompt, api_key):
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt + transcript_text)
        return response.text
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None

def translate_text(text, target_lang):
    translation = translator.translate(text, dest=target_lang)
    return translation.text

def create_pdf(summary_text):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    c.drawString(72, 800, "Summary")
    text = c.beginText(40, 780)
    text.setFont("Helvetica", 12)
    for line in summary_text.split('\n'):
        text.textLine(line)
    c.drawText(text)
    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer.getvalue()

# UI elements
st.title("YouTube Video Summarizer")

# Display video thumbnail
if youtube_link:
    video_id = youtube_link.split("=")[1]
    video_thumbnail = f"http://img.youtube.com/vi/{video_id}/0.jpg"
    st.image(video_thumbnail, caption="Video Thumbnail", use_column_width=True)

# Language selection and summary generation
target_lang = st.selectbox("Select Target Language:", options=['en', 'fr', 'es', 'de'])
if st.button("Generate Summary"):
    if google_api_key and youtube_link:
        transcript_text = extract_transcript_details(youtube_link)
        if transcript_text:
            prompt = """You are a YouTube video summarizer. Summarize the video content into key points within 1500 words."""
            customized_prompt = f"{prompt} Please generate a {summary_length.lower()} summary."
            summary = generate_gemini_content(transcript_text, customized_prompt, google_api_key)
            if summary:
                st.success("Transcript extracted and summary generated successfully!")
                st.subheader("Detailed Notes:")
                st.write(summary)
                
                # Language translation
                if target_lang != 'en':
                    translated_summary = translate_text(summary, target_lang)
                    st.info(f"Summary translated to {translator.translate(target_lang, dest='en').text}.")
                    st.write(translated_summary)
                else:
                    st.info("No translation required.")
                
                # PDF download
                pdf_bytes = create_pdf(translated_summary if target_lang != 'en' else summary)
                st.download_button(label="Download Summary as PDF",
                                   data=pdf_bytes,
                                   file_name="YouTube_Summary.pdf",
                                   mime="application/pdf")
            else:
                st.error("Failed to generate summary.")
        else:
            st.error("Failed to extract transcript.")
    else:
        st.error("Google API Key or YouTube link is missing.")
