import streamlit as st

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

/* ── Base ─────────────────────────────────────────────────────────── */
*, html, body, [class*="css"] { font-family: 'Inter', sans-serif !important; box-sizing: border-box; }

/* ── Hide Streamlit chrome ────────────────────────────────────────── */
#MainMenu, footer, header                        { visibility: hidden; }
[data-testid="stToolbar"]                        { display: none !important; }
[data-testid="stDecoration"]                     { display: none !important; }
[data-testid="stSidebarNav"]                     { display: none !important; }
[data-testid="stSidebarNavSeparator"]            { display: none !important; }
[data-testid="stSidebarNavItems"]                { display: none !important; }
[data-testid="stSidebarCollapsedControl"]        { display: none !important; }
[data-testid="collapsedControl"]                 { display: none !important; }
button[kind="header"]                            { display: none !important; }

/* ── Content area padding ─────────────────────────────────────────── */
.block-container                              { padding: 0 !important; max-width: 100% !important; }
.main .block-container,
section.main .block-container,
[data-testid="stMain"] .block-container,
[data-testid="block-container"]               { padding: 2.4rem 3rem 4rem !important; max-width: 100% !important; }

/* ── App background ───────────────────────────────────────────────── */
.stApp { background: #F8FAFC !important; }

/* ── Sidebar shell ────────────────────────────────────────────────── */
[data-testid="stSidebar"] {
    background: #FFFFFF !important;
    border-right: 1px solid #EAECF0 !important;
    min-width: 252px !important;
    max-width: 252px !important;
}
[data-testid="stSidebar"] > div:first-child { padding-top: 0 !important; }

/* Sidebar nav buttons (inactive) */
[data-testid="stSidebar"] .stButton > button {
    width: calc(100% - 16px) !important;
    text-align: left !important;
    justify-content: flex-start !important;
    background: transparent !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 9px 14px !important;
    color: #64748B !important;
    font-size: .875rem !important;
    font-weight: 500 !important;
    box-shadow: none !important;
    margin: 1px 8px !important;
    transition: background .12s, color .12s !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
    background: #F8FAFC !important;
    color: #4F46E5 !important;
}

/* ── Primary button ───────────────────────────────────────────────── */
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #4F46E5, #6366F1) !important;
    border: none !important;
    border-radius: 9px !important;
    color: #FFFFFF !important;
    font-weight: 600 !important;
    font-size: .9rem !important;
    box-shadow: 0 2px 10px rgba(79,70,229,.28) !important;
    transition: all .15s ease !important;
}
.stButton > button[kind="primary"]:hover {
    box-shadow: 0 4px 18px rgba(79,70,229,.4) !important;
    transform: translateY(-1px) !important;
}

/* ── Secondary button ─────────────────────────────────────────────── */
.stButton > button[kind="secondary"] {
    background: #FFFFFF !important;
    border: 1px solid #E2E8F0 !important;
    border-radius: 9px !important;
    color: #374151 !important;
    font-weight: 500 !important;
}
.stButton > button[kind="secondary"]:hover {
    border-color: #C7D2FE !important;
    color: #4F46E5 !important;
}

/* ── Inputs ───────────────────────────────────────────────────────── */
.stTextInput > label { font-size: .82rem !important; font-weight: 600 !important; color: #374151 !important; }
.stTextInput > div > div > input {
    background: #FFFFFF !important;
    border: 1.5px solid #E2E8F0 !important;
    border-radius: 9px !important;
    padding: 10px 14px !important;
    font-size: .9rem !important;
    color: #0F172A !important;
    transition: border .15s !important;
}
.stTextInput > div > div > input:focus {
    border-color: #4F46E5 !important;
    box-shadow: 0 0 0 3px rgba(79,70,229,.1) !important;
    outline: none !important;
}

/* ── Selectbox ────────────────────────────────────────────────────── */
[data-baseweb="select"] > div:first-child {
    border: 1.5px solid #E2E8F0 !important;
    border-radius: 9px !important;
    background: #FFFFFF !important;
}

/* ── Form box ─────────────────────────────────────────────────────── */
[data-testid="stForm"] {
    background: #FFFFFF !important;
    border: 1px solid #E2E8F0 !important;
    border-radius: 16px !important;
    padding: 28px 24px 20px !important;
    box-shadow: 0 2px 12px rgba(0,0,0,.06) !important;
}

/* ── Expander ─────────────────────────────────────────────────────── */
[data-testid="stExpander"] {
    background: #FFFFFF !important;
    border: 1px solid #E2E8F0 !important;
    border-radius: 12px !important;
    box-shadow: 0 1px 3px rgba(0,0,0,.04) !important;
    margin-bottom: 10px !important;
    overflow: hidden !important;
}
[data-testid="stExpander"]:hover { border-color: #C7D2FE !important; }
[data-testid="stExpander"] summary { padding: 13px 18px !important; font-weight: 600 !important; }

/* ── Progress ─────────────────────────────────────────────────────── */
[data-testid="stProgressBar"] > div { background: linear-gradient(90deg,#4F46E5,#818CF8) !important; border-radius: 999px !important; }

/* ── Download button ──────────────────────────────────────────────── */
.stDownloadButton > button { border-radius: 9px !important; font-weight: 600 !important; font-size: .83rem !important; }

/* ── Alerts ───────────────────────────────────────────────────────── */
[data-testid="stAlert"] { border-radius: 10px !important; font-size: .875rem !important; }

/* ── Divider ──────────────────────────────────────────────────────── */
hr { border: none !important; border-top: 1px solid #E2E8F0 !important; margin: 20px 0 !important; }

/* ── Scrollbar ────────────────────────────────────────────────────── */
::-webkit-scrollbar         { width: 5px; height: 5px; }
::-webkit-scrollbar-track   { background: transparent; }
::-webkit-scrollbar-thumb   { background: #CBD5E1; border-radius: 3px; }
</style>
"""


def inject_css():
    st.markdown(CSS, unsafe_allow_html=True)


def render_sidebar(user: dict, active: str = ""):
    inject_css()

    # ── Logo ──────────────────────────────────────────────────────────────────
    st.sidebar.markdown("""
    <div style="padding:20px 20px 14px;display:flex;align-items:center;gap:10px;
                border-bottom:1px solid #F1F5F9;margin-bottom:6px">
        <div style="width:36px;height:36px;border-radius:10px;flex-shrink:0;
                    background:linear-gradient(135deg,#4F46E5,#818CF8);
                    display:flex;align-items:center;justify-content:center;font-size:.95rem;
                    box-shadow:0 2px 8px rgba(79,70,229,.3)">🎯</div>
        <div>
            <div style="font-size:.97rem;font-weight:800;color:#0F172A;line-height:1.1;letter-spacing:-.01em">LeadHunter</div>
            <div style="font-size:.6rem;font-weight:700;color:#6366F1;text-transform:uppercase;letter-spacing:.08em;margin-top:1px">AI Lead Generation</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Nav label ─────────────────────────────────────────────────────────────
    st.sidebar.markdown("""
    <div style="padding:10px 20px 4px;font-size:.65rem;font-weight:700;
                letter-spacing:.1em;text-transform:uppercase;color:#CBD5E1">Navigation</div>
    """, unsafe_allow_html=True)

    # ── Nav items ─────────────────────────────────────────────────────────────
    NAV = [
        ("dashboard", "📊", "Dashboard",  "pages/1_Dashboard.py"),
        ("search",    "🔍", "New Search", "pages/2_Search.py"),
        ("leads",     "📋", "All Leads",  "pages/3_Leads.py"),
    ]
    for key, icon, label, page in NAV:
        if active == key:
            st.sidebar.markdown(f"""
            <div style="display:flex;align-items:center;gap:10px;
                        margin:2px 8px;padding:9px 14px;border-radius:8px;
                        background:#EEF2FF;cursor:default">
                <span style="font-size:.95rem;width:20px;text-align:center">{icon}</span>
                <span style="font-size:.875rem;font-weight:700;color:#4F46E5">{label}</span>
                <span style="margin-left:auto;width:6px;height:6px;border-radius:50%;background:#4F46E5"></span>
            </div>
            """, unsafe_allow_html=True)
        else:
            if st.sidebar.button(f"{icon}  {label}", key=f"nav_{key}", use_container_width=True):
                st.switch_page(page)

    # ── Coming soon ───────────────────────────────────────────────────────────
    st.sidebar.markdown("""
    <div style="padding:14px 20px 4px;margin-top:4px;font-size:.65rem;font-weight:700;
                letter-spacing:.1em;text-transform:uppercase;color:#CBD5E1">Coming Soon</div>
    """, unsafe_allow_html=True)

    for icon, label in [("📧", "Email Automation"), ("💬", "WhatsApp Outreach"), ("🔄", "Auto Scheduler")]:
        st.sidebar.markdown(f"""
        <div style="display:flex;align-items:center;justify-content:space-between;
                    margin:2px 8px;padding:8px 14px;border-radius:8px;opacity:.45">
            <div style="display:flex;align-items:center;gap:10px">
                <span style="font-size:.9rem;width:20px;text-align:center">{icon}</span>
                <span style="font-size:.875rem;font-weight:500;color:#64748B">{label}</span>
            </div>
            <span style="font-size:.58rem;background:#F1F5F9;color:#94A3B8;
                         padding:2px 8px;border-radius:999px;font-weight:700;letter-spacing:.04em">SOON</span>
        </div>
        """, unsafe_allow_html=True)

    # ── User profile (pinned to bottom) ───────────────────────────────────────
    st.sidebar.markdown("<div style='flex:1;min-height:24px'></div>", unsafe_allow_html=True)

    initial = user["name"][0].upper()
    st.sidebar.markdown(f"""
    <div style="margin:0 8px 0;border-top:1px solid #F1F5F9;padding:14px 10px 8px">
        <div style="display:flex;align-items:center;gap:10px">
            <div style="width:36px;height:36px;border-radius:50%;flex-shrink:0;
                        background:linear-gradient(135deg,#4F46E5,#818CF8);
                        display:flex;align-items:center;justify-content:center;
                        color:white;font-weight:700;font-size:.85rem">{initial}</div>
            <div style="min-width:0">
                <div style="font-size:.84rem;font-weight:700;color:#0F172A;
                            white-space:nowrap;overflow:hidden;text-overflow:ellipsis">{user['name']}</div>
                <div style="font-size:.72rem;color:#94A3B8;
                            white-space:nowrap;overflow:hidden;text-overflow:ellipsis">{user['email']}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Logout — styled inline
    st.sidebar.markdown("""
    <style>
    [data-testid="stSidebar"] .sign-out > button {
        color: #EF4444 !important;
        font-size: .83rem !important;
        font-weight: 500 !important;
    }
    [data-testid="stSidebar"] .sign-out > button:hover {
        background: #FEF2F2 !important;
        color: #DC2626 !important;
    }
    </style>
    """, unsafe_allow_html=True)
    with st.sidebar:
        st.markdown('<div class="sign-out">', unsafe_allow_html=True)
        if st.button("↩  Sign Out", key="logout_btn", use_container_width=True):
            del st.session_state.user
            st.switch_page("app.py")
        st.markdown('</div>', unsafe_allow_html=True)
    st.sidebar.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)


def page_header(title: str, subtitle: str = ""):
    st.markdown(f"""
    <div style="margin-bottom:28px">
        <h1 style="font-size:1.55rem;font-weight:800;color:#0F172A;margin:0 0 4px;line-height:1.2">{title}</h1>
        {"<p style='color:#94A3B8;font-size:.875rem;margin:0;font-weight:400'>"+subtitle+"</p>" if subtitle else ""}
    </div>
    """, unsafe_allow_html=True)


def kpi_card(col, value, label: str, icon: str, color: str):
    COLORS = {
        "indigo": ("#4F46E5", "#EEF2FF"),
        "green":  ("#059669", "#ECFDF5"),
        "orange": ("#D97706", "#FFFBEB"),
        "red":    ("#DC2626", "#FEF2F2"),
    }
    fg, bg = COLORS.get(color, ("#4F46E5", "#EEF2FF"))
    col.markdown(f"""
    <div style="background:#FFFFFF;border:1px solid #EAECF0;border-radius:14px;padding:20px 22px;
                box-shadow:0 1px 3px rgba(0,0,0,.04);height:100%">
        <div style="display:flex;align-items:flex-start;justify-content:space-between;margin-bottom:14px">
            <div style="width:42px;height:42px;background:{bg};border-radius:10px;
                        display:flex;align-items:center;justify-content:center;font-size:1.1rem">{icon}</div>
        </div>
        <div style="font-size:2rem;font-weight:800;color:#0F172A;line-height:1;margin-bottom:6px">{value:,}</div>
        <div style="font-size:.75rem;font-weight:600;color:#64748B;letter-spacing:.01em">{label}</div>
    </div>
    """, unsafe_allow_html=True)


def score_badge(score) -> str:
    if score is None:
        return '<span style="color:#94A3B8">—</span>'
    if score >= 70:
        return f'<span style="background:#ECFDF5;color:#059669;padding:3px 10px;border-radius:999px;font-size:.73rem;font-weight:700">🔥 {score}</span>'
    if score >= 40:
        return f'<span style="background:#FFFBEB;color:#D97706;padding:3px 10px;border-radius:999px;font-size:.73rem;font-weight:700">🟡 {score}</span>'
    return f'<span style="background:#FEF2F2;color:#DC2626;padding:3px 10px;border-radius:999px;font-size:.73rem;font-weight:700">❄️ {score}</span>'


def status_badge(status: str) -> str:
    MAP = {
        "completed": ("#ECFDF5", "#059669", "✓"),
        "running":   ("#EEF2FF", "#4F46E5", "◌"),
        "failed":    ("#FEF2F2", "#DC2626", "✗"),
        "pending":   ("#F1F5F9", "#475569", "○"),
    }
    bg, fg, ic = MAP.get(status, ("#F1F5F9", "#475569", "○"))
    return f'<span style="background:{bg};color:{fg};padding:3px 10px;border-radius:999px;font-size:.72rem;font-weight:700;display:inline-block">{ic} {status.capitalize()}</span>'
