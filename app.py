import streamlit as st
from study_assistant_full import run_study_assistant
from streamlit_lottie import st_lottie
import requests

# -------------- Load Lottie ----------------
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_ai = load_lottieurl("https://assets4.lottiefiles.com/packages/lf20_j1adxtyb.json")  # AI animation
lottie_book = load_lottieurl("https://assets2.lottiefiles.com/packages/lf20_tno6cg2w.json")  # Study animation

# -------------- 🎨 Page Config ----------------
st.set_page_config(
    page_title="📚 Study Assistant AI",
    layout="centered",
    page_icon="🎓",
)

# -------------- 🎓 Header Section ----------------
col_a1, col_a2, col_a3 = st.columns([1, 2, 1])
with col_a2:
    st_lottie(lottie_ai, height=150, key="header_anim")

st.markdown("""
    <h1 style='text-align: center; color: #4F8BF9;'>🎓 Study Assistant AI Agent</h1>
    <p style='text-align: center; font-size: 18px;'>An intelligent assistant to help you learn faster and better.</p>
    <hr style='margin-top: 20px; margin-bottom: 20px;'>
""", unsafe_allow_html=True)

# -------------- 🧾 Input Form ----------------
with st.form("input_form"):
    st.markdown("### 🧠 Enter Study Input")
    col1, col2 = st.columns(2)
    with col1:
        topic = st.text_input("📘 Study Topic", value="Photosynthesis")
    with col2:
        question = st.text_input("❓ Specific Question", value="Why is chlorophyll important?")
    submitted = st.form_submit_button("🚀 Run Study Assistant")

# -------------- 📊 Run Agent ----------------
if submitted:
    with st.spinner("🧬 Running the AI agents..."):
        result = run_study_assistant(topic, question)

    st.success("✅ AI Agent Finished!")
    
    st_lottie(lottie_book, height=200, key="done_anim")

    # Display structured outputs
    st.markdown("### 📘 Topic Explanation")
    st.markdown(
        f"<div style='background-color: #e8f0fe; padding: 15px; border-radius: 10px;'>{result['steps'].get('task_1')}</div>",
        unsafe_allow_html=True
    )

    st.markdown("### ❓ Answer to Your Question")
    st.markdown(
        f"<div style='background-color: #fef8e8; padding: 15px; border-radius: 10px;'>{result['steps'].get('task_2')}</div>",
        unsafe_allow_html=True
    )

    st.markdown("### 📝 Quiz Questions")
    st.markdown(
        f"<div style='background-color: #e8fff0; padding: 15px; border-radius: 10px;'>{result['steps'].get('task_3')}</div>",
        unsafe_allow_html=True
    )

    # Optional: Review Inputs
    with st.expander("🔍 Review Your Input"):
        st.markdown(f"**Topic:** {topic}")
        st.markdown(f"**Question:** {question}")
