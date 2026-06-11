import streamlit as st
import random
import time
from words import CATEGORIES

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Heads Up!",
    page_icon="🎯",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Lexend:wght@400;700;900&display=swap');

html, body, [class*="css"] {
    font-family: 'Lexend', sans-serif;
}

/* Hide default Streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 2rem; padding-bottom: 2rem; }

/* ── SETUP screen ── */
.setup-title {
    font-size: 3rem;
    font-weight: 900;
    text-align: center;
    letter-spacing: -1px;
    margin-bottom: 0.2rem;
}
.setup-subtitle {
    text-align: center;
    color: #888;
    margin-bottom: 2rem;
    font-size: 1rem;
}

/* ── READY screen ── */
.ready-box {
    background: #1a1a2e;
    border-radius: 24px;
    padding: 3rem 2rem;
    text-align: center;
    margin: 1rem 0;
}
.ready-title {
    font-size: 2rem;
    font-weight: 900;
    color: #fff;
}
.ready-hint {
    color: #aaa;
    margin-top: 0.5rem;
    font-size: 0.95rem;
}

/* ── PLAYING screen ── */
.play-card {
    background: linear-gradient(135deg, #6c3fc5, #3a86ff);
    border-radius: 28px;
    padding: 3.5rem 2rem;
    text-align: center;
    margin: 0.5rem 0 1.5rem 0;
    box-shadow: 0 8px 32px rgba(108, 63, 197, 0.3);
}
.play-word {
    font-size: 3rem;
    font-weight: 900;
    color: #fff;
    letter-spacing: -1px;
    line-height: 1.1;
}
.play-category {
    color: rgba(255,255,255,0.7);
    font-size: 0.9rem;
    margin-top: 0.75rem;
    letter-spacing: 1px;
    text-transform: uppercase;
}
.timer-bar-wrap {
    background: #eee;
    border-radius: 99px;
    height: 10px;
    margin: 1rem 0;
    overflow: hidden;
}
.timer-bar {
    height: 10px;
    border-radius: 99px;
    transition: width 0.9s linear, background 0.5s;
}
.score-badge {
    display: inline-block;
    background: #f0fdf4;
    color: #16a34a;
    border-radius: 99px;
    padding: 0.3rem 1.1rem;
    font-weight: 700;
    font-size: 1.1rem;
    margin-bottom: 0.5rem;
}

/* ── RESULTS screen ── */
.result-box {
    background: linear-gradient(135deg, #f0fdf4, #dcfce7);
    border-radius: 24px;
    padding: 3rem 2rem;
    text-align: center;
    margin: 1rem 0;
}
.result-number {
    font-size: 5rem;
    font-weight: 900;
    color: #16a34a;
    line-height: 1;
}
.result-label {
    color: #555;
    font-size: 1rem;
    margin-top: 0.3rem;
}

/* ── Buttons ── */
div.stButton > button {
    border-radius: 14px;
    font-family: 'Lexend', sans-serif;
    font-weight: 700;
    font-size: 1.1rem;
    padding: 0.7rem 1.5rem;
    width: 100%;
    border: none;
    cursor: pointer;
    transition: transform 0.1s, box-shadow 0.1s;
}
div.stButton > button:active {
    transform: scale(0.97);
}
</style>
""", unsafe_allow_html=True)

# ── Session state init ────────────────────────────────────────────────────────
def init_state():
    defaults = {
        "phase": "setup",
        "category": list(CATEGORIES.keys())[0],
        "words": [],
        "word_idx": 0,
        "score": 0,
        "timer_duration": 60,
        "start_time": None,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

# ── Helpers ───────────────────────────────────────────────────────────────────
def start_game():
    words = CATEGORIES[st.session_state.category].copy()
    random.shuffle(words)
    st.session_state.words = words
    st.session_state.word_idx = 0
    st.session_state.score = 0
    st.session_state.phase = "ready"

def begin_round():
    st.session_state.start_time = time.time()
    st.session_state.phase = "playing"

def mark_correct():
    st.session_state.score += 1
    st.session_state.word_idx += 1
    if st.session_state.word_idx >= len(st.session_state.words):
        st.session_state.phase = "results"

def mark_skip():
    st.session_state.word_idx += 1
    if st.session_state.word_idx >= len(st.session_state.words):
        st.session_state.phase = "results"

def time_left():
    elapsed = time.time() - st.session_state.start_time
    return max(0, st.session_state.timer_duration - elapsed)

def reset():
    st.session_state.phase = "setup"

# ── PHASES ────────────────────────────────────────────────────────────────────

# ── 1. SETUP ──────────────────────────────────────────────────────────────────
if st.session_state.phase == "setup":
    st.markdown('<div class="setup-title">🎯 Heads Up!</div>', unsafe_allow_html=True)
    st.markdown('<div class="setup-subtitle">Daj telefón niekomu inému — on bude klikať!</div>', unsafe_allow_html=True)

    st.session_state.category = st.selectbox(
        "Kategória",
        options=list(CATEGORIES.keys()),
        index=list(CATEGORIES.keys()).index(st.session_state.category),
    )
    st.session_state.timer_duration = st.number_input(
        "Čas (sekundy)",
        min_value=10,
        max_value=300,
        value=st.session_state.timer_duration,
        step=5,
    )

    st.write("")
    if st.button("🚀 Začať hru", use_container_width=True):
        start_game()
        st.rerun()

# ── 2. READY ──────────────────────────────────────────────────────────────────
elif st.session_state.phase == "ready":
    st.markdown(f"""
    <div class="ready-box">
        <div class="ready-title">📱 Priprav sa!</div>
        <div class="ready-hint">
            Odlož telefón — kamoška bude klikať<br>
            <strong>{st.session_state.category}</strong> · {st.session_state.timer_duration}s
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("▶️ Štart!", use_container_width=True):
        begin_round()
        st.rerun()

    if st.button("← Späť", use_container_width=True):
        reset()
        st.rerun()

# ── 3. PLAYING ────────────────────────────────────────────────────────────────
elif st.session_state.phase == "playing":
    remaining = time_left()

    if remaining <= 0:
        st.session_state.phase = "results"
        st.rerun()

    current_word = st.session_state.words[st.session_state.word_idx]
    pct = remaining / st.session_state.timer_duration
    bar_color = "#22c55e" if pct > 0.4 else "#f97316" if pct > 0.15 else "#ef4444"
    bar_width = int(pct * 100)

    # Score badge
    st.markdown(f'<div style="text-align:center"><span class="score-badge">✅ {st.session_state.score} správnych</span></div>', unsafe_allow_html=True)

    # Word card
    st.markdown(f"""
    <div class="play-card">
        <div class="play-word">{current_word}</div>
        <div class="play-category">{st.session_state.category}</div>
    </div>
    """, unsafe_allow_html=True)

    # Timer bar
    st.markdown(f"""
    <div class="timer-bar-wrap">
        <div class="timer-bar" style="width:{bar_width}%; background:{bar_color};"></div>
    </div>
    <div style="text-align:center; font-size:1.5rem; font-weight:900; color:{bar_color}; margin-bottom:1rem;">
        {int(remaining)}s
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ Správne", use_container_width=True):
            mark_correct()
            st.rerun()
    with col2:
        if st.button("⏭️ Preskočiť", use_container_width=True):
            mark_skip()
            st.rerun()

    # Auto-refresh every second for the timer
    time.sleep(0.9)
    st.rerun()

# ── 4. RESULTS ────────────────────────────────────────────────────────────────
elif st.session_state.phase == "results":
    total = st.session_state.word_idx
    score = st.session_state.score
    skipped = total - score

    st.markdown(f"""
    <div class="result-box">
        <div class="result-number">{score}</div>
        <div class="result-label">správnych odpovedí z {total} slov</div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.metric("✅ Správne", score)
    with col2:
        st.metric("⏭️ Preskočené", skipped)

    st.write("")
    if st.button("🔄 Hrať znova", use_container_width=True):
        reset()
        st.rerun()
