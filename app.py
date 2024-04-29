import streamlit as st
import pickle
from googletrans import Translator
from youtube_transcript_api import YouTubeTranscriptApi

# Load the summarizer pipeline from the pickle file
with open('summarizer.pkl', 'rb') as f:
    summarizer = pickle.load(f)

# Function to summarize transcript
def summarize_transcript(transcript):
    max_seq_length = 1024  # Maximum sequence length supported by the model
    summarized_text = []
    for i in range(0, len(transcript), max_seq_length):
        chunk = transcript[i:i + max_seq_length]
        summarized_chunk = summarizer(chunk, max_length=150, min_length=50, do_sample=False)
        summarized_text.append(summarized_chunk[0]['summary_text'])
    return ' '.join(summarized_text)

# Function to translate text
def translate_text(text, target_language):
    translator = Translator()
    translated_text = translator.translate(text, dest=target_language)
    return translated_text.text

# Main function to run the app
def main():
    st.title("YouTube Summarizer & Translator")

    # Input for YouTube video URL
    youtube_url = st.text_input("Enter the YouTube video URL:")

    if youtube_url:
        try:
            video_id = youtube_url.split("=")[1]
            transcript = YouTubeTranscriptApi.get_transcript(video_id)

            if not transcript:
                st.error("Transcript is empty or unavailable.")
                return

            # Concatenate transcript into a single string
            result = " ".join([i['text'] for i in transcript])

            # Summarize transcript
            summary = summarize_transcript(result)

            # Translation option
            st.subheader("Translate Summary")
            language_codes = {
                'af': 'afrikaans', 'sq': 'albanian', 'am': 'amharic', 'ar': 'arabic', 'hy': 'armenian',
                'az': 'azerbaijani', 'eu': 'basque', 'be': 'belarusian', 'bn': 'bengali', 'bs': 'bosnian',
                'bg': 'bulgarian', 'ca': 'catalan', 'ceb': 'cebuano', 'ny': 'chichewa', 'zh-cn': 'chinese (simplified)',
                'zh-tw': 'chinese (traditional)', 'co': 'corsican', 'hr': 'croatian', 'cs': 'czech', 'da': 'danish',
                'nl': 'dutch', 'en': 'english', 'eo': 'esperanto', 'et': 'estonian', 'tl': 'filipino', 'fi': 'finnish',
                'fr': 'french', 'fy': 'frisian', 'gl': 'galician', 'ka': 'georgian', 'de': 'german', 'el': 'greek',
                'gu': 'gujarati', 'ht': 'haitian creole', 'ha': 'hausa', 'haw': 'hawaiian', 'iw': 'hebrew', 'he': 'hebrew',
                'hi': 'hindi', 'hmn': 'hmong', 'hu': 'hungarian', 'is': 'icelandic', 'ig': 'igbo', 'id': 'indonesian',
                'ga': 'irish', 'it': 'italian', 'ja': 'japanese', 'jw': 'javanese', 'kn': 'kannada', 'kk': 'kazakh',
                'km': 'khmer', 'ko': 'korean', 'ku': 'kurdish (kurmanji)', 'ky': 'kyrgyz', 'lo': 'lao', 'la': 'latin',
                'lv': 'latvian', 'lt': 'lithuanian', 'lb': 'luxembourgish', 'mk': 'macedonian', 'mg': 'malagasy',
                'ms': 'malay', 'ml': 'malayalam', 'mt': 'maltese', 'mi': 'maori', 'mr': 'marathi', 'mn': 'mongolian',
                'my': 'myanmar (burmese)', 'ne': 'nepali', 'no': 'norwegian', 'or': 'odia', 'ps': 'pashto', 'fa': 'persian',
                'pl': 'polish', 'pt': 'portuguese', 'pa': 'punjabi', 'ro': 'romanian', 'ru': 'russian', 'sm': 'samoan',
                'gd': 'scots gaelic', 'sr': 'serbian', 'st': 'sesotho', 'sn': 'shona', 'sd': 'sindhi', 'si': 'sinhala',
                'sk': 'slovak', 'sl': 'slovenian', 'so': 'somali', 'es': 'spanish', 'su': 'sundanese', 'sw': 'swahili',
                'sv': 'swedish', 'tg': 'tajik', 'ta': 'tamil', 'te': 'telugu', 'th': 'thai', 'tr': 'turkish', 'uk': 'ukrainian',
                'ur': 'urdu', 'ug': 'uyghur', 'uz': 'uzbek', 'vi': 'vietnamese', 'cy': 'welsh', 'xh': 'xhosa', 'yi': 'yiddish',
                'yo': 'yoruba', 'zu': 'zulu'
            }
            target_language = st.selectbox("Select Target Language:", list(language_codes.values())) 

            # Translate summary if language selected
            if target_language:
                lang_code = [code for code, name in language_codes.items() if name == target_language][0]
                translated_summary = translate_text(summary, lang_code)
                st.write("Translated Summary:")
                st.write(translated_summary)
            else:
                st.write("Please select a target language.")

        except Exception as e:
            st.error(f"Error occurred: {e}")

# Run the app
if __name__ == "__main__":
    main()
