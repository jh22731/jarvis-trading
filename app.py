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

# --- Tactical Dashboard Metrics ---
df = conn.read(worksheet="Sheet1", ttl="1m")
latest = df.iloc[-1] if not df.empty else None

col1, col2, col3 = st.columns(3)
if latest is not None:
    col1.metric("Symbol", latest['Symbol'])
    col2.metric("Action", latest['BUY/SELL'])
    col3.metric("Stop Loss", latest['Stop Loss'])
else:
    st.info("Awaiting market data from TradingView...")

# --- Intelligence Function ---
def get_latest_signal():
    if latest is None: return "No active signals."
    return f"""
    - Symbol: {latest.get('Symbol', 'N/A')}
    - Action: {latest.get('BUY/SELL', 'N/A')}
    - Signal: {latest.get('Signal_Type', 'N/A')}
    - Stop Loss: {latest.get('Stop Loss', 'N/A')}
    - Notes: {latest.get('Strategy_Notes', 'N/A')}
    """

# --- Chat Interaction ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Enter tactical command, sir..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Brain Processing with Context
    latest_intel = get_latest_signal()
    contextual_prompt = f"Market Intelligence: {latest_intel}. User Command: {prompt}. Instructions: Reference specific levels from intelligence, be tactical, address user as 'sir'."
    
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=contextual_prompt,
        config={"system_instruction": "You are Jarvis. Be precise, concise, and tactical."}
    )
    
    msg = response.text
    with st.chat_message("assistant"):
        st.markdown(msg)
    st.session_state.messages.append({"role": "assistant", "content": msg})
    
    # Audio Generation
    audio_stream = xi_client.text_to_speech.convert(text=msg, voice_id="Brian")
    audio_buffer = BytesIO()
    for chunk in audio_stream:
        if chunk: audio_buffer.write(chunk)
    audio_buffer.seek(0)
    st.audio(audio_buffer, format="audio/mpeg", autoplay=True)
    