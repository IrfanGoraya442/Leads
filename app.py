import streamlit as st
from dotenv import load_dotenv
from database import init_db
from utils.auth import login_user, register_user

load_dotenv()
init_db()

st.set_page_config(
    page_title="LeadHunter",
    page_icon="🎯",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
*, html, body, [class*="css"] { font-family: 'Inter', sans-serif !important; }
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stSidebarNav"],
[data-testid="collapsedControl"] { display: none !important; }

/* Full-page background image */
.stApp {
    background-image:
        linear-gradient(135deg, rgba(15,23,42,0.72) 0%, rgba(30,27,75,0.65) 100%),
        url('https://images.unsplash.com/photo-1477959858617-67f85cf4f1df?w=1600&q=80&fit=crop');
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}

.block-container { padding-top: 60px !important; max-width: 420px !important; }

/* White card */
[data-testid="stForm"] {
    background: #FFFFFF !important;
    border: none !important;
    border-radius: 20px !important;
    padding: 32px 28px !important;
    box-shadow: 0 24px 64px rgba(0,0,0,.35) !important;
}

.stTextInput > label { font-size: .82rem !important; font-weight: 600 !important; color: #374151 !important; }
.stTextInput > div > div > input {
    border-radius: 9px !important; font-size: .9rem !important;
    border: 1.5px solid #E2E8F0 !important; padding: 11px 14px !important;
    background: #F8FAFC !important;
}
.stTextInput > div > div > input:focus {
    border-color: #4F46E5 !important;
    box-shadow: 0 0 0 3px rgba(79,70,229,.1) !important;
    background: #FFFFFF !important;
}
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg,#4F46E5,#6366F1) !important;
    border: none !important; border-radius: 9px !important;
    font-weight: 600 !important; color: white !important;
    box-shadow: 0 2px 10px rgba(79,70,229,.4) !important;
    font-size: .92rem !important;
}
.stButton > button[kind="primary"]:hover {
    box-shadow: 0 4px 18px rgba(79,70,229,.55) !important;
    transform: translateY(-1px) !important;
}
/* Switch link */
.stButton > button[kind="secondary"] {
    background: transparent !important; border: none !important;
    color: rgba(255,255,255,.75) !important; font-size: .84rem !important;
    font-weight: 500 !important; box-shadow: none !important;
    text-decoration: underline !important; text-underline-offset: 3px !important;
}
.stButton > button[kind="secondary"]:hover { color: white !important; }
</style>
""", unsafe_allow_html=True)

if "user" in st.session_state:
    st.switch_page("pages/1_Dashboard.py")

if "auth_mode" not in st.session_state:
    st.session_state.auth_mode = "login"

# ── Logo ───────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;margin-bottom:28px">
    <div style="width:52px;height:52px;background:linear-gradient(135deg,#4F46E5,#818CF8);
                border-radius:14px;display:flex;align-items:center;justify-content:center;
                font-size:1.4rem;margin:0 auto 12px;box-shadow:0 4px 16px rgba(79,70,229,.45)">🎯</div>
    <div style="font-size:1.5rem;font-weight:800;color:white;letter-spacing:-.02em">LeadHunter</div>
    <div style="font-size:.82rem;color:rgba(255,255,255,.55);margin-top:5px">AI-powered Google Maps lead generation</div>
</div>
""", unsafe_allow_html=True)

# ── Login ──────────────────────────────────────────────────────────────────────
if st.session_state.auth_mode == "login":
    with st.form("login_form"):
        st.markdown("<div style='font-size:1.15rem;font-weight:800;color:#0F172A;margin-bottom:18px'>Sign in to your account</div>", unsafe_allow_html=True)
        email    = st.text_input("Email", placeholder="you@example.com")
        password = st.text_input("Password", type="password", placeholder="••••••••")
        st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
        submitted = st.form_submit_button("Sign In →", use_container_width=True, type="primary")

    if submitted:
        if not email or not password:
            st.error("Please fill in all fields.")
        else:
            user = login_user(email, password)
            if user:
                st.session_state.user = user
                st.switch_page("pages/1_Dashboard.py")
            else:
                st.error("Incorrect email or password.")

    st.markdown("<div style='text-align:center;margin-top:14px'>", unsafe_allow_html=True)
    if st.button("Don't have an account? Create one free →", use_container_width=True, key="go_reg"):
        st.session_state.auth_mode = "register"
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# ── Register ───────────────────────────────────────────────────────────────────
else:
    with st.form("register_form"):
        st.markdown("<div style='font-size:1.15rem;font-weight:800;color:#0F172A;margin-bottom:18px'>Create a free account</div>", unsafe_allow_html=True)
        name         = st.text_input("Full name", placeholder="Muhammad Irfan")
        reg_email    = st.text_input("Email", placeholder="you@example.com")
        reg_password = st.text_input("Password", type="password", placeholder="••••••••")
        st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
        reg_sub = st.form_submit_button("Create Account →", use_container_width=True, type="primary")

    if reg_sub:
        if not name or not reg_email or not reg_password:
            st.error("Please fill in all fields.")
        else:
            user, err = register_user(name, reg_email, reg_password)
            if err:
                st.error(err)
            else:
                st.session_state.user = user
                st.switch_page("pages/1_Dashboard.py")

    st.markdown("<div style='text-align:center;margin-top:14px'>", unsafe_allow_html=True)
    if st.button("Already have an account? Sign in →", use_container_width=True, key="go_login"):
        st.session_state.auth_mode = "login"
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
