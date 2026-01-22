import streamlit as st
import random
from hangman_words_day7 import word_list

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

# ================= PAGE CONFIG =================
st.set_page_config(page_title="Hangman Pro", page_icon="🎯", layout="centered")

# ================= THEME SELECTION =================
if "theme" not in st.session_state:
    st.session_state.theme = "NEON"

themes = {
    "NEON": "radial-gradient(circle, #2a0845 0%, #000000 100%)",
    "CYBER": "linear-gradient(135deg, #000428 0%, #004e92 100%)",
    "SPACE": "url('https://www.transparenttextures.com/patterns/stardust.png'), radial-gradient(circle, #1b2735 0%, #090a0f 100%)",
    "NATURE": "url('https://www.transparenttextures.com/patterns/green-dust-and-scratches.png'), linear-gradient(135deg, #134e5e 0%, #71b280 100%)"
}

# ================= SESSION STATE =================
if "word" not in st.session_state:
    st.session_state.word = random.choice(word_list).upper()
    st.session_state.guessed = []
    st.session_state.lives = 6
    st.session_state.game_over = False
    st.session_state.msg = ("info", "Welcome! Start guessing.")
    st.session_state.duplicate_flag = False  # Track duplicate state

# ================= MOBILE-FRIENDLY CSS =================
st.markdown(f"""
    <style>
    audio {{ display: none !important; }}
    .stApp {{
        background: {themes[st.session_state.theme]};
        background-attachment: fixed;
        color: #ffffff;
    }}
    .ascii-logo {{
        font-family: 'Courier New', monospace;
        color: #00e5ff; 
        text-align: center;
        white-space: pre;
        font-weight: bold;
        text-shadow: 0 0 15px #00e5ff;
        font-size: clamp(6px, 1.5vw, 10px); 
        margin-bottom: 10px;
    }}
    .word-font {{
        font-size: clamp(28px, 8vw, 45px) !important;
        letter-spacing: clamp(5px, 2vw, 12px);
        text-align: center;
        color: {"#CCFF00" if st.session_state.theme == "NATURE" else "#ff00ff"}; 
        font-family: 'Courier New', monospace;
        font-weight: 900;
        margin: 20px 0;
        text-shadow: 3px 3px 0px rgba(0,0,0,0.5), 0 0 20px {"#CCFF00" if st.session_state.theme == "NATURE" else "#ff00ff"};
    }}
    div.stButton > button {{
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        color: white;
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 12px;
        padding: 10px;
        width: 100%;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }}
    div.stButton > button:hover {{
        background: #00e5ff;
        color: #000;
        transform: translateY(-2px);
        box-shadow: 0 0 20px #00e5ff;
    }}
    p, h3, label {{
        color: white !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }}
    </style>
    """, unsafe_allow_html=True)


# ================= CALLBACK LOGIC =================
def process_guess():
    guess = st.session_state.current_input.upper()
    st.session_state.current_input = ""
    st.session_state.duplicate_flag = False  # Reset flag on new guess attempt

    if not guess or not guess.isalpha():
        st.session_state.msg = ("warning", "Enter a valid letter!")
        return

    if guess in st.session_state.guessed:
        st.session_state.duplicate_flag = True  # Set flag for the notification
        st.session_state.msg = ("warning", f"'{guess}' was already tried!")
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
    if st.button("🌿 NATURE"): st.session_state.theme = "NATURE"; st.rerun()

# ================= UI LAYOUT =================
st.markdown(f'<div class="ascii-logo">{LOGO}</div>', unsafe_allow_html=True)

col1, col2 = st.columns([1, 1])

with col1:
    st.code(HANGMAN_PICS[6 - st.session_state.lives])

with col2:
    m_type, m_text = st.session_state.msg
    if m_type == "error":
        st.error(m_text)
    elif m_type == "success":
        st.success(m_text)
    elif m_type == "warning":
        st.warning(m_text)
    else:
        st.info(m_text)
    st.write(f"### Lives: {'❤️' * st.session_state.lives}")

display_word = " ".join([l if l in st.session_state.guessed else "_" for l in st.session_state.word])
st.markdown(f'<p class="word-font">{display_word}</p>', unsafe_allow_html=True)

if not st.session_state.game_over:
    st.text_input("GUESS", max_chars=1, key="current_input", on_change=process_guess)

    # --- ADDED NOTIFICATION LINE ---
    if st.session_state.duplicate_flag:
        st.markdown(
            "<p style='color: #FFD700; font-weight: bold; text-shadow: 2px 2px 4px black; text-align: center; font-size: 18px;'>⚠️ YOU ALREADY GUESSED THIS LETTER!</p>",
            unsafe_allow_html=True)

    st.button("SUBMIT GUESS", on_click=process_guess)
else:
    if st.session_state.lives > 0:
        st.balloons()
        st.success("🎉 VICTORY!")
        st.audio("https://www.myinstants.com/media/sounds/win-sound-effect-8.mp3", autoplay=True)
    else:
        st.error(f"💀 DEFEAT! Word: {st.session_state.word}")
        st.audio("https://www.myinstants.com/media/sounds/gta-v-death-sound-effect.mp3", autoplay=True)

    if st.button("New Game 🔄"):
        for key in list(st.session_state.keys()):
            if key != "theme": del st.session_state[key]
        st.rerun()

st.markdown("---")
st.caption("© Professional Gaming Experience | Ansh Raj")