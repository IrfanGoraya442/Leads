import streamlit as st
from utils.auth import require_auth
from utils.styles import render_sidebar, page_header, kpi_card, status_badge
from database import get_db, Search, Lead
from sqlalchemy import func

st.set_page_config(page_title="Dashboard — LeadHunter", page_icon="📊", layout="wide")
user = require_auth()
render_sidebar(user, "dashboard")

page_header("Dashboard", f"Welcome back, {user['name']} 👋")

# ── KPI cards ──────────────────────────────────────────────────────────────────
with get_db() as db:
    total_leads = db.query(func.count(Lead.id)).scalar() or 0
    no_website  = db.query(func.count(Lead.id)).filter(Lead.has_website == False).scalar() or 0
    low_rating  = db.query(func.count(Lead.id)).filter(Lead.rating < 3.5, Lead.rating != None).scalar() or 0
    no_email    = db.query(func.count(Lead.id)).filter(Lead.email == None).scalar() or 0
    recent_orm  = db.query(Search).filter(Search.user_id == user["id"]).order_by(Search.created_at.desc()).limit(8).all()
    recent      = [{"id": s.id, "keyword": s.keyword, "city": s.city, "country": s.country,
                    "total": s.total_results, "status": s.status} for s in recent_orm]
    hot    = db.query(func.count(Lead.id)).filter(Lead.ai_score >= 70).scalar() or 0
    medium = db.query(func.count(Lead.id)).filter(Lead.ai_score >= 40, Lead.ai_score < 70).scalar() or 0
    cold   = db.query(func.count(Lead.id)).filter(Lead.ai_score < 40).scalar() or 0

c1, c2, c3, c4 = st.columns(4, gap="medium")
kpi_card(c1, total_leads, "Total Leads",   "🎯", "indigo")
kpi_card(c2, no_website,  "No Website",    "🌐", "orange")
kpi_card(c3, low_rating,  "Low Rating",    "⭐", "red")
kpi_card(c4, no_email,    "Missing Email", "📧", "green")

st.markdown("<div style='height:32px'></div>", unsafe_allow_html=True)

# ── Main grid ──────────────────────────────────────────────────────────────────
left, right = st.columns([2.4, 1], gap="large")

with left:
    st.markdown("""
    <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:16px">
        <div style="font-size:.95rem;font-weight:700;color:#0F172A">🕐 Recent Searches</div>
    </div>
    """, unsafe_allow_html=True)

    if not recent:
        st.markdown("""
        <div style="background:#FFFFFF;border:1px solid #EAECF0;border-radius:14px;padding:48px 24px;
                    text-align:center;box-shadow:0 1px 3px rgba(0,0,0,.04)">
            <div style="font-size:2rem;margin-bottom:12px">🔍</div>
            <div style="font-size:.95rem;font-weight:600;color:#0F172A;margin-bottom:6px">No searches yet</div>
            <div style="font-size:.82rem;color:#94A3B8">Click <strong>New Search</strong> in the sidebar to get started.</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Table header
        st.markdown("""
        <div style="background:#FFFFFF;border:1px solid #EAECF0;border-radius:14px;
                    box-shadow:0 1px 3px rgba(0,0,0,.04);overflow:hidden">
            <div style="padding:14px 20px;border-bottom:1px solid #F1F5F9;
                        display:grid;grid-template-columns:2.5fr 1.8fr 80px 110px 72px;gap:12px;align-items:center">
                <span style="font-size:.7rem;font-weight:700;color:#94A3B8;text-transform:uppercase;letter-spacing:.07em">Keyword</span>
                <span style="font-size:.7rem;font-weight:700;color:#94A3B8;text-transform:uppercase;letter-spacing:.07em">Location</span>
                <span style="font-size:.7rem;font-weight:700;color:#94A3B8;text-transform:uppercase;letter-spacing:.07em">Leads</span>
                <span style="font-size:.7rem;font-weight:700;color:#94A3B8;text-transform:uppercase;letter-spacing:.07em">Status</span>
                <span></span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        for row in recent:
            hc = st.columns([2.5, 1.8, 0.8, 1.1, 0.72])
            hc[0].markdown(f"<div style='font-weight:600;font-size:.875rem;color:#0F172A;padding:10px 0 10px 4px'>{row['keyword']}</div>", unsafe_allow_html=True)
            hc[1].markdown(f"<div style='color:#64748B;font-size:.84rem;padding:10px 0'>{row['city']}, {row['country']}</div>", unsafe_allow_html=True)
            hc[2].markdown(f"<div style='font-weight:700;color:#4F46E5;font-size:.88rem;padding:10px 0'>{row['total']}</div>", unsafe_allow_html=True)
            hc[3].markdown(f"<div style='padding:10px 0'>{status_badge(row['status'])}</div>", unsafe_allow_html=True)
            if hc[4].button("View →", key=f"v_{row['id']}", use_container_width=True):
                st.session_state.view_search_id = row["id"]
                st.switch_page("pages/3_Leads.py")
            st.markdown("<hr style='margin:0 0 0;border-color:#F8FAFC'>", unsafe_allow_html=True)

with right:
    # CTA card
    st.markdown("""
    <div style="background:linear-gradient(135deg,#4F46E5 0%,#6366F1 100%);border-radius:14px;padding:22px 20px;margin-bottom:14px">
        <div style="font-size:.65rem;font-weight:700;color:rgba(255,255,255,.55);text-transform:uppercase;
                    letter-spacing:.08em;margin-bottom:8px">Quick Action</div>
        <div style="font-size:1.2rem;font-weight:800;color:white;margin-bottom:6px">Find New Leads</div>
        <div style="color:rgba(255,255,255,.68);font-size:.82rem;line-height:1.55;margin-bottom:16px">
            Search any business type in any city worldwide — AI scores every result instantly.
        </div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("🔍  Start New Search", type="primary", use_container_width=True, key="dash_search"):
        st.switch_page("pages/2_Search.py")

    # Lead quality breakdown
    if total_leads > 0:
        st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)
        st.markdown("""
        <div style="font-size:.82rem;font-weight:700;color:#0F172A;margin-bottom:14px">Lead Quality</div>
        """, unsafe_allow_html=True)

        for label, count, c1, c2 in [
            ("🔥 Hot",    hot,    "#059669", "#34D399"),
            ("🟡 Medium", medium, "#D97706", "#FBBF24"),
            ("❄️ Cold",   cold,   "#DC2626", "#F87171"),
        ]:
            pct = int(count / max(total_leads, 1) * 100)
            st.markdown(f"""
            <div style="margin-bottom:14px">
                <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:5px">
                    <span style="font-size:.8rem;color:{c1};font-weight:600">{label}</span>
                    <span style="font-size:.8rem;font-weight:700;color:#0F172A">{count}</span>
                </div>
                <div style="background:#F1F5F9;height:6px;border-radius:999px">
                    <div style="background:linear-gradient(90deg,{c1},{c2});height:6px;border-radius:999px;width:{pct}%"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

# ── Coming Soon ────────────────────────────────────────────────────────────────
st.markdown("<div style='height:40px'></div>", unsafe_allow_html=True)
st.markdown("""
<div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:20px">
    <div>
        <div style="font-size:1rem;font-weight:700;color:#0F172A">🚀 Coming Soon</div>
        <div style="font-size:.8rem;color:#94A3B8;margin-top:3px">Features in active development</div>
    </div>
    <span style="background:#EEF2FF;color:#4F46E5;padding:4px 12px;border-radius:999px;
                 font-size:.72rem;font-weight:700">In Development</span>
</div>
""", unsafe_allow_html=True)

COMING_SOON = [
    ("📧", "Email Automation",   "Send personalized cold emails to leads with AI-written copy.",        "High Priority"),
    ("💬", "WhatsApp Outreach",  "Send bulk WhatsApp messages to leads with detected phone numbers.",   "High Priority"),
    ("🔄", "Scheduled Scraping", "Auto-scrape on a schedule — wake up to fresh leads every morning.",  "In Progress"),
    ("🏢", "CRM Integration",    "Sync leads directly to HubSpot, Salesforce, or Pipedrive.",          "Planned"),
    ("👥", "Team Dashboard",     "Invite team members, assign leads, and track outreach together.",    "Planned"),
    ("📱", "Mobile App",         "Manage and export leads on the go from iOS or Android.",             "Planned"),
]

TAG_STYLES = {
    "High Priority": ("#FFFBEB", "#D97706"),
    "In Progress":   ("#ECFDF5", "#059669"),
    "Planned":       ("#EEF2FF", "#4F46E5"),
}

cols = st.columns(3, gap="medium")
for i, (icon, title, desc, tag) in enumerate(COMING_SOON):
    tag_bg, tag_fg = TAG_STYLES[tag]
    with cols[i % 3]:
        st.markdown(f"""
        <div style="background:#FFFFFF;border:1px solid #EAECF0;border-radius:14px;padding:22px;
                    margin-bottom:14px;box-shadow:0 1px 3px rgba(0,0,0,.04)">
            <div style="display:flex;align-items:flex-start;justify-content:space-between;margin-bottom:14px">
                <div style="width:42px;height:42px;background:#F8FAFC;border:1px solid #EAECF0;
                            border-radius:10px;display:flex;align-items:center;justify-content:center;
                            font-size:1.15rem">{icon}</div>
                <span style="background:{tag_bg};color:{tag_fg};padding:3px 10px;border-radius:999px;
                             font-size:.68rem;font-weight:700;letter-spacing:.02em">{tag}</span>
            </div>
            <div style="font-size:.92rem;font-weight:700;color:#0F172A;margin-bottom:6px">{title}</div>
            <div style="font-size:.8rem;color:#64748B;line-height:1.6;margin-bottom:16px">{desc}</div>
            <div style="padding-top:12px;border-top:1px solid #F1F5F9">
                <span style="font-size:.73rem;color:#CBD5E1;font-weight:500">🔒 Coming Soon</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
