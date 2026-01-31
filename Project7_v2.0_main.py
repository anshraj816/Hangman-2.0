import streamlit as st
import random
# Ensure hangman_words_day7.py exists in your directory with a word_list variable
try:
    from hangman_words_day7 import word_list
except ImportError:
    word_list = ["PYTHON", "STREAMLIT", "HANGMAN", "CYBERSPACE", "PROGRAMMING"]

import base64
import os

# ================= PAGE CONFIG =================
st.set_page_config(page_title="Hangman Pro", page_icon="🎯", layout="centered")

# --- ASSETS ---
LOGO = r"""
  _    _          _   _  _____ __  __          _   _ 
 | |  | |   /\   | \ | |/ ____|  \/  |   /\   | \ | |
 | |__| |  /  \  |  \| | |  __| \  / |  /  \  |  \| |
 |  __  | / /\ \ | . ` | | |_ | |\/| | / /\ \ | . ` |
 | |  | |/ ____ \| |\  | |__| | |  | |/ ____ \| |\  |
 |_|  |_/_/    \_\_| \_|\_____|_|  |_/_/    \_\_| \_|
"""

HANGMAN_PICS = [r'''
  +---+
  |   |
      |
      |
      |
      |
=========''', r'''
  +---+
  |   |
  O   |
      |
      |
      |
=========''', r'''
  +---+
  |   |
  O   |
  |   |
      |
      |
=========''', r'''
  +---+
  |   |
  O   |
 /|   |
      |
      |
=========''', r'''
  +---+
  |   |
  O   |
 /|\  |
      |
      |
=========''', r'''
  +---+
  |   |
  O   |
 /|\  |
 /    |
      |
=========''', r'''
  +---+
  |   |
  O   |
 /|\  |
 / \  |
      |
=========''']

# ================= VIDEO HELPER =================
def get_base64_video(video_path):
    if os.path.exists(video_path):
        with open(video_path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    return None

# ================= THEME SELECTION =================
if "theme" not in st.session_state:
    st.session_state.theme = "NEON"

themes = {
    "NEON": "radial-gradient(circle, #2a0845 0%, #000000 100%)",
    "CYBER": "linear-gradient(135deg, #000428 0%, #004e92 100%)",
    "SPACE": "radial-gradient(circle, #090a0f 0%, #000000 100%)",
    "WINTER": "radial-gradient(circle at center, #001524 0%, #000000 100%)"
}

# ================= SESSION STATE =================
if "word" not in st.session_state:
    st.session_state.word = random.choice(word_list).upper()
    st.session_state.guessed = []
    st.session_state.lives = 6
    st.session_state.game_over = False
    st.session_state.msg = ("info", "Welcome! Start guessing.")
    st.session_state.duplicate_flag = False

# ================= BACKGROUND LOGIC =================
video_file = "p71.gif.mp4" if st.session_state.theme == "NEON" else None
video_data = get_base64_video(video_file) if video_file else None

if video_data:
    st.markdown(f"""
        <style>
        #bg-video {{
            position: fixed;
            top: 0; left: 0; width: 100%; height: 100%;
            z-index: -1; object-fit: cover;
        }}
        .stApp {{ background: rgba(0,0,0,0.5) !important; }}
        </style>
        <video autoplay loop muted playsinline id="bg-video">
            <source src="data:video/mp4;base64,{video_data}" type="video/mp4">
        </video>
    """, unsafe_allow_html=True)

# ================= SPACE ROCKET EFFECT CSS =================
rocket_icons = ["🚀", "🛸", "🛰️", "☄️", "🚀"]
rockets_html = "".join([
    f'<div class="rocket" style="'
    f'left:{random.randint(-10, 110)}%; '
    f'top:{random.randint(0, 100)}%; '
    f'font-size:{random.randint(20, 60)}px; '
    f'animation-duration:{random.uniform(5, 15)}s; '
    f'animation-delay:{random.uniform(0, 10)}s; '
    f'filter: drop-shadow(0 0 {random.randint(5, 15)}px {random.choice(["#ff4b2b", "#00e5ff", "#ffffff"])});'
    f'">{random.choice(rocket_icons)}</div>'
    for _ in range(15)
])

space_css = f"""
<style>
@keyframes fly_space {{
  0% {{ transform: translate(-20vw, 20vh) rotate(-45deg); opacity: 0; }}
  10% {{ opacity: 1; }}
  90% {{ opacity: 1; }}
  100% {{ transform: translate(120vw, -20vh) rotate(-45deg); opacity: 0; }}
}}
.rocket {{
  position: fixed; z-index: 1000; pointer-events: none;
  animation: fly_space linear infinite;
}}
.stApp {{
    background: url('https://www.transparenttextures.com/patterns/stardust.png'), radial-gradient(circle, #090a0f 0%, #000000 100%) !important;
}}
</style>
{rockets_html}
"""

# ================= WINTER SNOW EFFECT CSS (UPDATED: 70 flakes, 4s avg) =================
snowflakes_html = "".join([
    f'<div class="snowflake" style="left:{random.randint(1, 98)}%; animation-duration:{random.uniform(3, 5)}s; animation-delay:{random.uniform(0, 4)}s;">❄️</div>'
    for _ in range(70)
])

snow_css = f"""
<style>
.stApp {{ background: radial-gradient(circle at center, #001524 0%, #000000 100%) !important; }}
[data-testid="stAppViewContainer"] {{ background-color: transparent !important; }}
@keyframes snow {{
  0% {{ transform: translateY(-10vh) translateX(0px); opacity: 1; }}
  100% {{ transform: translateY(100vh) translateX(20px); opacity: 0.2; }}
}}
.snowflake {{
  position: fixed; top: -5vh; color: white; font-size: 20px;
  user-select: none; z-index: 1000; pointer-events: none;
  animation-name: snow; animation-iteration-count: infinite; animation-timing-function: linear;
}}
</style>
{snowflakes_html}
"""

# ================= MOBILE-FRIENDLY CSS =================
st.markdown(f"""
    <style>
    audio {{ display: none !important; }}
    .stApp {{
        background: {themes[st.session_state.theme] if st.session_state.theme not in ["NEON", "SPACE", "WINTER"] else "transparent"} !important;
        background-attachment: fixed !important;
        color: #ffffff;
    }}
    .ascii-logo {{
        font-family: 'Courier New', monospace;
        color: #00e5ff; text-align: center; white-space: pre; font-weight: bold;
        text-shadow: 0 0 15px #00e5ff; font-size: clamp(6px, 1.5vw, 10px); 
        margin-bottom: 10px;
    }}
    .word-font {{
        font-size: clamp(28px, 8vw, 45px) !important;
        letter-spacing: clamp(5px, 2vw, 12px); text-align: center;
        color: {"#e0e0e0" if st.session_state.theme == "SPACE" else ("#b6fbff" if st.session_state.theme == "WINTER" else "#ff00ff")}; 
        font-family: 'Courier New', monospace; font-weight: 900; margin: 20px 0;
        text-shadow: 0 0 15px {"#ffffff" if st.session_state.theme == "SPACE" else ("#b6fbff" if st.session_state.theme == "WINTER" else "#ff00ff")};
    }}
    div.stButton > button {{
        background: rgba(255, 255, 255, 0.1); backdrop-filter: blur(15px);
        color: white !important; border: 1px solid rgba(255, 255, 255, 0.4) !important;
        border-radius: 12px; padding: 10px; width: 100%; transition: all 0.3s ease;
    }}
    div.stButton > button:hover {{
        background: #00e5ff; color: #000 !important; box-shadow: 0 0 20px #00e5ff;
    }}
    p, h3, label {{
        color: white !important;
        text-shadow: 1px 1px 3px black;
    }}
    </style>
    """, unsafe_allow_html=True)

if st.session_state.theme == "WINTER":
    st.markdown(snow_css, unsafe_allow_html=True)
elif st.session_state.theme == "SPACE":
    st.markdown(space_css, unsafe_allow_html=True)

# ================= CALLBACK LOGIC =================
def process_guess():
    guess = st.session_state.current_input.upper()
    st.session_state.current_input = ""
    st.session_state.duplicate_flag = False

    if not guess or not guess.isalpha():
        st.session_state.msg = ("warning", "Enter a valid letter!")
        return

    if guess in st.session_state.guessed:
        st.session_state.duplicate_flag = True
        return

    st.session_state.guessed.append(guess)

    if guess not in st.session_state.word:
        st.session_state.lives -= 1
        st.session_state.msg = ("error", f"Wrong! '{guess}' is not there.")
    else:
        st.session_state.msg = ("success", f"Nice! '{guess}' is correct.")

    current_display = [l for l in st.session_state.word if l in st.session_state.guessed]
    if len(set(st.session_state.word)) == len(set(current_display)):
        st.session_state.game_over = True
    elif st.session_state.lives <= 0:
        st.session_state.game_over = True

# ================= THEME BUTTONS =================
c1, c2, c3, c4 = st.columns(4)
with c1:
    if st.button("🚨 NEON"): st.session_state.theme = "NEON"; st.rerun()
with c2:
    if st.button("🤖 CYBER"): st.session_state.theme = "CYBER"; st.rerun()
with c3:
    if st.button("✨ SPACE"): st.session_state.theme = "SPACE"; st.rerun()
with c4:
    if st.button("☃️ WINTER"): st.session_state.theme = "WINTER"; st.rerun()

# ================= UI LAYOUT (FIXED MOBILE WARNING) =================
st.markdown(f'<div class="ascii-logo">{LOGO}</div>', unsafe_allow_html=True)

col1, col2 = st.columns([1, 1])
with col1:
    st.code(HANGMAN_PICS[6 - st.session_state.lives])

with col2:
    # Logic to show duplicate warning inside the main message container for mobile visibility
    if st.session_state.duplicate_flag:
        st.warning("⚠️ ALREADY GUESSED!")
    else:
        m_type, m_text = st.session_state.msg
        if m_type == "error": st.error(m_text)
        elif m_type == "success": st.success(m_text)
        elif m_type == "warning": st.warning(m_text)
        else: st.info(m_text)
    st.write(f"### Lives: {'❤️' * st.session_state.lives}")

display_word = " ".join([l if l in st.session_state.guessed else "_" for l in st.session_state.word])
st.markdown(f'<p class="word-font">{display_word}</p>', unsafe_allow_html=True)

if not st.session_state.game_over:
    st.text_input("GUESS", max_chars=1, key="current_input", on_change=process_guess)
    st.button("SUBMIT", on_click=process_guess)
else:
    if st.session_state.lives > 0:
        st.balloons()
        st.success("🎉 VICTORY!")
    else:
        st.error(f"💀 DEFEAT! Word: {st.session_state.word}")

    if st.button("New Game 🔄"):
        for key in list(st.session_state.keys()):
            if key != "theme": del st.session_state[key]
        st.rerun()

st.markdown("---")
st.caption("© Professional Gaming Experience | Ansh Raj")
