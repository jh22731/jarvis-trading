import streamlit as st
from google import genai
from elevenlabs.client import ElevenLabs
from streamlit_gsheets import GSheetsConnection
from io import BytesIO

# Configure Page
st.set_page_config(page_title="Jarvis OS", layout="centered")

# Initialize Connections
conn = st.connection("gsheets", type=GSheetsConnection)
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
xi_client = ElevenLabs(api_key=st.secrets["ELEVENLABS_API_KEY"])

st.title("Jarvis Command Terminal")

