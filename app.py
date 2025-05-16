import streamlit as st
from dotenv import load_dotenv 
load_dotenv()

import google.generativeai as genai
import os
from youtube_transcript_api import YouTubeTranscriptApi

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

prompt = """please summarize the following transcript of a youtube video into 250 words or less and highlight the key points:"""


#header
header = '''
# Youtube Video Transcript Summarizer
This app summarizes the transcript of a Youtube video into 250 words or less and highlights the key points.
'''

st.markdown(header)
youtube_link = st.text_input("Enter Youtube Video URL", "https://www.youtube.com/watch?v=8q2g0v4a1xA")
def extract_transcript_details(youtube_video_url):
    try:
        video_id= youtube_video_url.split("=")[1]
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id)
        transcript = "".join([t['text'] for t in transcript_text])
        return transcript   
    except Exception as e:
        raise e
    
    
#function to generate summary
def generate_summary(transcript_text, prompt):
    model = genai.GenerativeModel("models/gemini-2.0-flash")
    response = model.generate_content(prompt + transcript_text)

    return response.text



# Streamlit app
if st.button("Get DEtailed Notes"):
    transcript_text = extract_transcript_details(youtube_link)
    if transcript_text:
        summary = generate_summary(transcript_text, prompt)  # <-- fix here
        st.markdown("### Summary")
        st.write(summary)
# ...existing code...
        
        
footer='''
# Youtube Video Transcript Summarizer
# '''

st.markdown(header)
st.markdown(footer,unsafe_allow_html=True)


# Add this to check available models
for m in genai.list_models():
    print(m.name, m.supported_generation_methods)

          



