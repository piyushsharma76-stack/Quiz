import streamlit as st
import pandas as pd
import time

# --- 1. PAGE CONFIG & STYLING ---
st.set_page_config(page_title="Sahayaks Quiz", layout="wide")

st.markdown(f"""
    <style>
    .block-container {{
        padding-top: 3rem !important;
        padding-bottom: 0rem !important;
    }}

    hr {{
        margin-top: 0.8rem !important;
        margin-bottom: 0.8rem !important;
    }}

    .stApp {{
        background-color: #0F1937;
        color: #FFFFFF;
    }}

    .stat-box {{
        font-size: 24px !important;
        font-weight: bold;
        text-align: center;
    }}

    .stButton>button {{
        background-color: #1E2A4A;
        color: white;
        border-radius: 10px;
        height: 3.5em;
        width: 100%;
        font-size: 22px;
        font-weight: bold;
    }}
    </style>
    """, unsafe_allow_html=True)


# --- 2. LOAD DATA ---
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('Questions1.csv', encoding='latin1').dropna(subset=['question'])
        return df.to_dict('records')
    except Exception as e:
        st.error(f"CSV Error: {e}")
        return []


questions = load_data()
TOTAL_Q = len(questions)
TIME_PER_QUIZ = 15 * TOTAL_Q

# --- 3. SESSION STATE ---
if 'current_idx' not in st.session_state:
    st.session_state.current_idx = 0
    st.session_state.score = 0
    st.session_state.start_time = time.time()
    st.session_state.quiz_over = False

# --- 4. TIMER LOGIC ---
elapsed_time = time.time() - st.session_state.start_time
time_left = max(0, int(TIME_PER_QUIZ - elapsed_time))

if time_left <= 0:
    st.session_state.quiz_over = True

# --- 5. UI TOP BAR ---
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(
        f"<p class='stat-box' style='color: #FFD700;'>🏆 Score: {st.session_state.score} / {st.session_state.current_idx}</p>",
        unsafe_allow_html=True)
with col2:
    st.markdown(
        f"<p class='stat-box' style='color: #FFFFFF;'>❓ Questions Left: {TOTAL_Q - st.session_state.current_idx}</p>",
        unsafe_allow_html=True)
with col3:
    st.markdown(f"<p class='stat-box' style='color: #FF4B4B;'>⏳ Time: {time_left}s</p>", unsafe_allow_html=True)

st.divider()

# --- 6. QUIZ LOGIC ---
if not st.session_state.quiz_over and st.session_state.current_idx < TOTAL_Q:
    q_data = questions[st.session_state.current_idx]

    st.markdown(
        f"<h2 style='text-align: center; margin-top: -10px; color: #D3D3D3;'>Question {st.session_state.current_idx + 1}</h2>",
        unsafe_allow_html=True)

    st.markdown(f"<h2 style='text-align: center; margin-top: 0px; font-size: 30px;'>{q_data['question']}</h2>",
                unsafe_allow_html=True)

    st.write("")

    # --- BUTTON GRID ADJUSTMENT ---
    # We use 4 columns: Empty, Buttons, Buttons, Empty
    # The middle columns (index 1 and 2) get the buttons
    # Ratio [1, 2, 2, 1] makes the center columns wider than the side gaps
    cols = st.columns([1, 2, 2, 1])


    def check_ans(choice):
        if str(q_data[choice]).strip() == str(q_data['correct_answer']).strip():
            st.session_state.score += 1
        st.session_state.current_idx += 1
        if st.session_state.current_idx >= TOTAL_Q:
            st.session_state.quiz_over = True
        st.rerun()


    with cols[1]:  # Left-center column
        if st.button(f"A. {q_data['A']}"): check_ans('A')
        if st.button(f"C. {q_data['C']}"): check_ans('C')
    with cols[2]:  # Right-center column
        if st.button(f"B. {q_data['B']}"): check_ans('B')
        if st.button(f"D. {q_data['D']}"): check_ans('D')

    time.sleep(1)
    st.rerun()

else:
    # --- 7. END SCREEN ---
    st.balloons()
    st.markdown("<h1 style='text-align: center;'>Quiz Over!</h1>", unsafe_allow_html=True)
    st.markdown(f"<h2 style='text-align: center;'>Final Score: {st.session_state.score} / {TOTAL_Q}</h2>",
                unsafe_allow_html=True)

    if st.button("Try Again"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()