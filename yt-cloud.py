import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
import base64

def get_video_id_from_url(url):
    # Extract video ID from the URL
    if 'youtu.be' in url:
        return url.split('/')[-1]
    if 'youtube.com' in url:
        return url.split('v=')[-1].split('&')[0]
    return None

def format_transcript(transcript):
    """Converts a transcript into plain text with no timestamps.
    :param transcript:
    :return: all transcript text lines separated by newline breaks.
    :rtype str
    """
    return '\n'.join(line['text'] for line in transcript)

def get_transcript(video_url, languages):
    video_id = get_video_id_from_url(video_url)
    if not video_id:
        return "Invalid YouTube URL", None

    try:
        # Fetching all available transcripts for the video
        transcripts = YouTubeTranscriptApi.list_transcripts(video_id)
        
        # Trying to fetch the preferred language transcript
        transcript = transcripts.find_transcript(languages)
        
        # Fetching the actual transcript data
        transcript_data = transcript.fetch()
        
        # Formatting the transcript
        plain_text_transcript = format_transcript(transcript_data)
        
        return plain_text_transcript, video_id
    except Exception as e:
        return f"An error occurred: {e}", None

def download_button(object_to_download, download_filename, button_text):
    """
    Generates a link to download the given object_to_download.
    :param object_to_download: The object to be downloaded (a string).
    :param download_filename: Filename and extension of the file. e.g. mydata.csv, some_txt_output.txt
    :param button_text: Text of the download button.
    :return: the button widget and download link
    """
    # Convert the object to download into bytes
    object_to_download = object_to_download.encode()
    
    # Create a base64 encoded string
    b64 = base64.b64encode(object_to_download).decode()

    # Create the download button with custom CSS for the border
    button_html = f"""
    <a download="{download_filename}" href="data:file/txt;base64,{b64}" class="btn btn-primary" style="border: 1px solid #ccc; border-radius: 4px; padding: 8px 16px; margin: 2px;">
        {button_text}
    </a>
    """
    st.markdown(button_html, unsafe_allow_html=True)

# Streamlit 页面布局
st.title('YouTube Transcript Extractor')

video_url = st.text_input('Enter the YouTube video URL')

if video_url:
    # Try fetching Traditional Chinese first, then English
    transcript, video_id = get_transcript(video_url, ['zh-Hant', 'en'])
    if transcript:
        # Render the download button directly after URL input field
        download_button(transcript, f"{video_id}_transcript.txt", "Download Transcript")
        st.subheader('Transcript')
        st.write(transcript)
    else:
        st.write("Transcript not available.")
