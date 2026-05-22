import streamlit as st
from utils.auth import require_auth
from utils.styles import render_sidebar, page_header
from database import get_db, Search, Lead
from services.scraper.maps_scraper import GoogleMapsScraper
from services.ai.lead_analyzer import analyze_lead
import uuid

st.set_page_config(page_title="Search — LeadHunter", page_icon="🔍", layout="wide")
user = require_auth()
render_sidebar(user, "search")

page_header("New Search", "Find businesses on Google Maps and score them with AI.")

EXAMPLES = [
    ("🦷", "Dentists",    "Dubai",    "UAE"),
    ("🚗", "Car Rentals", "Lahore",   "Pakistan"),
    ("🍽️", "Restaurants", "London",   "UK"),
    ("💪", "Gyms",        "New York",  "USA"),
    ("⚖️", "Law Firms",   "Toronto",  "Canada"),
    ("💇", "Beauty Salons","Sydney",  "Australia"),
]

# ── Example chips ──────────────────────────────────────────────────────────────
st.markdown("""
<div style="margin-bottom:16px">
    <span style="font-size:.8rem;font-weight:700;color:#94A3B8;text-transform:uppercase;letter-spacing:.05em">
        Quick Examples
    </span>
</div>
""", unsafe_allow_html=True)

cols = st.columns(len(EXAMPLES))
for i, (icon, kw, city, country) in enumerate(EXAMPLES):
    if cols[i].button(f"{icon} {kw} · {city}", key=f"ex{i}", use_container_width=True):
        st.session_state.kw      = kw
        st.session_state.city    = city
        st.session_state.country = country
        st.rerun()

st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

# ── Search form ────────────────────────────────────────────────────────────────
with st.form("search_form"):
    st.markdown("<div style='font-size:1rem;font-weight:700;color:#0F172A;margin-bottom:16px'>Search Parameters</div>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    keyword = c1.text_input("Business Type *",
        value=st.session_state.get("kw", ""),
        placeholder="Dentists, Gyms, Restaurants...")
    city    = c2.text_input("City *",
        value=st.session_state.get("city", ""),
        placeholder="Dubai, London, New York...")
    country = c3.text_input("Country *",
        value=st.session_state.get("country", ""),
        placeholder="UAE, UK, USA...")

    c4, c5 = st.columns(2)
    category = c4.selectbox("Category", [
        "Auto-detect", "Restaurant", "Dental Clinic", "Gym & Fitness",
        "Real Estate", "Car Rental", "Hotel", "Law Firm",
        "Beauty Salon", "Construction", "E-commerce"
    ])
    limit = c5.select_slider("Max Results",
        options=[10, 20, 50, 100, 150, 200], value=50)

    st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)

    go = st.form_submit_button(
        "🚀  Start Search",
        use_container_width=True,
        type="primary"
    )

# ── Run search ─────────────────────────────────────────────────────────────────
if go:
    if not keyword or not city or not country:
        st.error("Please fill all required fields (marked *)")
        st.stop()

    search_id = str(uuid.uuid4())
    with get_db() as db:
        db.add(Search(
            id=search_id, user_id=user["id"],
            keyword=keyword, city=city, country=country,
            category=None if category == "Auto-detect" else category,
            status="running"
        ))

    # Status UI
    st.markdown(f"""
    <div style="background:#EEF2FF;border:1px solid #C7D2FE;border-radius:10px;padding:16px 20px;margin:16px 0;display:flex;align-items:center;gap:12px">
        <div style="font-size:1.5rem">🔍</div>
        <div>
            <div style="font-weight:700;color:#3730A3">Searching for <em>{keyword}</em> in {city}, {country}</div>
            <div style="font-size:.82rem;color:#6366F1;margin-top:2px">Up to {limit} results · AI analysis included</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    progress_bar = st.progress(0, text="Launching scraper...")
    status_text  = st.empty()

    def on_progress(current, total, msg):
        pct = min(int((current / max(total, 1)) * 50), 50)
        progress_bar.progress(pct, text=msg)

    raw_leads = GoogleMapsScraper().search(keyword, city, country, limit, progress_cb=on_progress)

    if not raw_leads:
        with get_db() as db:
            db.query(Search).filter(Search.id == search_id).update({"status": "failed"})
        st.error("No results found. Try a different keyword or city.")
        st.stop()

    leads_to_save = []
    for i, raw in enumerate(raw_leads):
        pct = 50 + int((i / len(raw_leads)) * 48)
        progress_bar.progress(pct, text=f"AI scoring {i+1}/{len(raw_leads)}: {raw.get('business_name','')[:30]}")
        ai = analyze_lead(raw)
        leads_to_save.append(Lead(
            id=str(uuid.uuid4()), search_id=search_id,
            business_name=raw.get("business_name"), category=raw.get("category"),
            rating=raw.get("rating"),         reviews_count=raw.get("reviews_count"),
            address=raw.get("address"),       phone=raw.get("phone"),
            website=raw.get("website"),       maps_url=raw.get("maps_url"),
            has_website=raw.get("has_website", False),
            website_quality=ai.get("website_quality"),
            ai_score=ai.get("score"),         ai_notes=ai.get("notes"),
            suggested_service=ai.get("suggested_service"),
            outreach_message=ai.get("outreach_message"),
        ))

    with get_db() as db:
        db.add_all(leads_to_save)
        db.query(Search).filter(Search.id == search_id).update(
            {"total_results": len(leads_to_save), "status": "completed"}
        )

    progress_bar.progress(100, text="Complete!")

    hot    = sum(1 for l in leads_to_save if (l.ai_score or 0) >= 70)
    medium = sum(1 for l in leads_to_save if 40 <= (l.ai_score or 0) < 70)
    no_web = sum(1 for l in leads_to_save if not l.has_website)

    st.markdown(f"""
    <div style="background:#ECFDF5;border:1px solid #A7F3D0;border-radius:10px;padding:20px 24px;margin:16px 0">
        <div style="font-size:1.1rem;font-weight:700;color:#065F46;margin-bottom:12px">
            ✅ Found {len(leads_to_save)} leads
        </div>
        <div style="display:flex;gap:24px;flex-wrap:wrap">
            <div style="font-size:.85rem;color:#059669"><strong>🔥 {hot}</strong> Hot leads</div>
            <div style="font-size:.85rem;color:#D97706"><strong>🟡 {medium}</strong> Medium leads</div>
            <div style="font-size:.85rem;color:#DC2626"><strong>🌐 {no_web}</strong> No website</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.session_state.view_search_id = search_id
    if st.button("📋  View All Leads →", type="primary", use_container_width=True):
        st.switch_page("pages/3_Leads.py")
