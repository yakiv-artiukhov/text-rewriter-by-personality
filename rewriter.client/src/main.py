import asyncio
import json
import streamlit as st
from websockets import connect, ConnectionClosed

def_text_fragment = "The rain had just stopped, leaving the streets slick and shimmering under the glow of streetlamps. Puddles mirrored the sky, still heavy with clouds that refused to move on. I walked slowly, the quiet drip of water from rooftops the only sound for blocks. There was a strange comfort in the emptiness, like the world had decided to whisper instead of shout."

st.markdown("""
    <style>
        .stMainBlockContainer {
            max-width: 80% !important;
            padding-left: 3rem;
            padding-right: 3rem;
        }
    </style>
""", unsafe_allow_html=True)

st.title("PersonaRewriter")
st.write("It is a creative rewriting assistant that transforms any text fragment to reflect the voice, mindset, and style of a chosen personality. Whether it's a historical figure, a fictional character, or a specific type of person, PersonaRewriter channels their essence to retell the text as if it were written by them.")

col1, col2 = st.columns([3, 2])

with col1:
  with st.form("input_form"):
    text_fragment = st.text_area("Text Fragment:", height=220, value=def_text_fragment)
    personality_description = st.text_area("Personality Description:", height=100)
    submitted = st.form_submit_button("Submit")

with col2:
    st.write("Rewritten Text:")
    rewritten_text = st.empty()



async def send_for_rewriting(message):
    async with connect("ws://server:5583/rewriter") as websocket:
        await websocket.send(message)
        response = ""
        while True:
            try:
                chunk = await websocket.recv()
                response += chunk
                rewritten_text.markdown(response)
            except ConnectionClosed:
                break
            
if submitted:
    if not text_fragment.strip():
        st.error("Please enter a text fragment.")
        st.stop()
    elif not personality_description.strip():
        st.error("Please enter a personality description.")
        st.stop()
    
    message = json.dumps({
        "fragment": text_fragment.strip(),
        "personality": personality_description.strip()
    })
    print(message)
    asyncio.run(send_for_rewriting(message))