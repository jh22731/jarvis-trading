import streamlit as st
from google import genai
from elevenlabs.client import ElevenLabs

# Configure Page
st.set_page_config(page_title="Jarvis OS", layout="centered")
st.title("Jarvis Command Terminal")

# Secure Key Initialization (Managed via Streamlit Cloud Secrets)
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
xi_client = ElevenLabs(api_key=st.secrets["ELEVENLABS_API_KEY"])

# Session State for History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display History
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Tactical Prompt Handling
if prompt := st.chat_input("Enter tactical command, sir..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Brain Processing (Brevity Protocol Active)
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt,
        config={
            "system_instruction": "You are Jarvis. Be precise, concise, and tactical. Keep responses to 1-2 sentences maximum. Address user as 'sir'. Focus on DOL, Liquidity Sweeps, MSS, and FVG entries."
        }
    )
    
    msg = response.text
    with st.chat_message("assistant"):
        st.markdown(msg)
    st.session_state.messages.append({"role": "assistant", "content": msg})
    
    # Generate Audio
    audio = xi_client.text_to_speech.convert(text=msg, voice_id="Brian")
    st.audio(audio, format="audio/mp3", autoplay=True)
    