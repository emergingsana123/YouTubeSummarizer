import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io
from googletrans import Translator

# Set Streamlit page configuration
st.set_page_config(page_title="YouTube Video Summarizer", layout="wide")

# Sidebar for user inputs
youtube_link = st.sidebar.text_input("Enter YouTube Video Link:")

# Language translation
translator = Translator()

# Define language codes and their names
language_codes = {
    'af': 'afrikaans', 'sq': 'albanian', 'am': 'amharic', 'ar': 'arabic', 'hy': 'armenian', 'az': 'azerbaijani', 'eu': 'basque',
    'be': 'belarusian', 'bn': 'bengali', 'bs': 'bosnian', 'bg': 'bulgarian', 'ca': 'catalan', 'ceb': 'cebuano', 'ny': 'chichewa',
    'zh-cn': 'chinese (simplified)', 'zh-tw': 'chinese (traditional)', 'co': 'corsican', 'hr': 'croatian', 'cs': 'czech', 'da': 'danish',
    'nl': 'dutch', 'en': 'english', 'eo': 'esperanto', 'et': 'estonian', 'tl': 'filipino', 'fi': 'finnish', 'fr': 'french', 'fy': 'frisian',
    'gl': 'galician', 'ka': 'georgian', 'de': 'german', 'el': 'greek', 'gu': 'gujarati', 'ht': 'haitian creole', 'ha': 'hausa', 'haw': 'hawaiian',
    'iw': 'hebrew', 'he': 'hebrew', 'hi': 'hindi', 'hmn': 'hmong', 'hu': 'hungarian', 'is': 'icelandic', 'ig': 'igbo', 'id': 'indonesian', 'ga': 'irish',
    'it': 'italian', 'ja': 'japanese', 'jw': 'javanese', 'kn': 'kannada', 'kk': 'kazakh', 'km': 'khmer', 'ko': 'korean', 'ku': 'kurdish (kurmanji)', 'ky': 'kyrgyz',
    'lo': 'lao', 'la': 'latin', 'lv': 'latvian', 'lt': 'lithuanian', 'lb': 'luxembourgish', 'mk': 'macedonian', 'mg': 'malagasy', 'ms': 'malay', 'ml': 'malayalam',
    'mt': 'maltese', 'mi': 'maori', 'mr': 'marathi', 'mn': 'mongolian', 'my': 'myanmar (burmese)', 'ne': 'nepali', 'no': 'norwegian', 'or': 'odia', 'ps': 'pashto',
    'fa': 'persian', 'pl': 'polish', 'pt': 'portuguese', 'pa': 'punjabi', 'ro': 'romanian', 'ru': 'russian', 'sm': 'samoan', 'gd': 'scots gaelic', 'sr': 'serbian',
    'st': 'sesotho', 'sn': 'shona', 'sd': 'sindhi', 'si': 'sinhala', 'sk': 'slovak', 'sl': 'slovenian', 'so': 'somali', 'es': 'spanish', 'su': 'sundanese', 'sw': 'swahili',
    'sv': 'swedish', 'tg': 'tajik', 'ta': 'tamil', 'te': 'telugu', 'th': 'thai', 'tr': 'turkish', 'uk': 'ukrainian', 'ur': 'urdu', 'ug': 'uyghur', 'uz': 'uzbek',
    'vi': 'vietnamese', 'cy': 'welsh', 'xh': 'xhosa', 'yi': 'yiddish', 'yo': 'yoruba', 'zu': 'zulu'
}

# Define functions
def extract_transcript_details(youtube_video_url):
    try:
        video_id = youtube_video_url.split("=")[1]
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return " ".join(segment["text"] for segment in transcript)
    except Exception as e:
        st.sidebar.error(f"An error occurred: {e}")
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

# Process and display summary
if youtube_link and st.button("Get Detailed Notes"):
    transcript_text = extract_transcript_details(youtube_link)
    if transcript_text:
        st.success("Transcript extracted successfully!")
        
        # Language translation
        target_lang = st.selectbox("Select Target Language:", options=list(language_codes.values()))
        target_lang_code = [key for key, value in language_codes.items() if value == target_lang][0]
        if target_lang_code != 'en':
            transcript_text = translate_text(transcript_text, target_lang_code)
            st.info(f"Transcript translated to {target_lang.upper()}.")

        st.subheader("Detailed Notes:")
        st.write(transcript_text)
        
        # PDF download
        pdf_bytes = create_pdf(transcript_text)
        st.download_button(label="Download Transcript as PDF",
                           data=pdf_bytes,
                           file_name="YouTube_Transcript.pdf",
                           mime="application/pdf")
    else:
        st.error("Failed to extract transcript.")
