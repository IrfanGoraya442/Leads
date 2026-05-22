import streamlit as st
import pandas as pd
from utils.auth import require_auth
from utils.styles import render_sidebar, page_header, score_badge
from utils.export import to_csv, to_excel
from database import get_db, Lead, Search

st.set_page_config(page_title="Leads — LeadHunter", page_icon="📋", layout="wide")
user = require_auth()
render_sidebar(user, "leads")

page_header("Leads", "Browse, filter and export your scraped business leads.")

LEAD_COLS = ["id","business_name","category","rating","reviews_count","address",
             "phone","email","website","maps_url","has_website","website_quality",
             "ai_score","ai_notes","suggested_service","outreach_message"]

# ── Load searches ──────────────────────────────────────────────────────────────
with get_db() as db:
    searches_orm = db.query(Search).filter(Search.user_id == user["id"]).order_by(Search.created_at.desc()).all()
    searches_data = [{"label": f"{s.keyword} · {s.city} ({s.total_results} leads)", "id": s.id} for s in searches_orm]

if not searches_data:
    st.info("No searches yet."); st.stop()

# ── Selector + filters bar ────────────────────────────────────────────────────
fc0, fc1, fc2, fc3 = st.columns([2.5, 2, 1.8, 1.8])

default_idx = 0
if "view_search_id" in st.session_state:
    ids = [s["id"] for s in searches_data]
    if st.session_state.view_search_id in ids:
        default_idx = ids.index(st.session_state.view_search_id)

labels = [s["label"] for s in searches_data]
selected_label = fc0.selectbox("Search", labels, index=default_idx, label_visibility="collapsed")
selected_id    = searches_data[labels.index(selected_label)]["id"]

search_name    = fc1.text_input("Filter", placeholder="🔎  Filter by name...", label_visibility="collapsed")
website_filter = fc2.selectbox("Website", ["All Websites", "Has Website ✅", "No Website ❌"], label_visibility="collapsed")
score_filter   = fc3.selectbox("Score", ["All Scores", "🔥 Hot (70+)", "🟡 Medium (40-69)", "❄️ Cold (<40)"], label_visibility="collapsed")

# ── Load leads as dicts ────────────────────────────────────────────────────────
with get_db() as db:
    leads_orm = db.query(Lead).filter(Lead.search_id == selected_id).all()
    leads = [{c: getattr(l, c) for c in LEAD_COLS} for l in leads_orm]

if not leads:
    st.warning("No leads in this search."); st.stop()

# ── Apply filters ──────────────────────────────────────────────────────────────
filtered = leads
if search_name:
    filtered = [l for l in filtered if search_name.lower() in (l["business_name"] or "").lower()]
if website_filter == "Has Website ✅":
    filtered = [l for l in filtered if l["has_website"]]
elif website_filter == "No Website ❌":
    filtered = [l for l in filtered if not l["has_website"]]
if score_filter == "🔥 Hot (70+)":
    filtered = [l for l in filtered if (l["ai_score"] or 0) >= 70]
elif score_filter == "🟡 Medium (40-69)":
    filtered = [l for l in filtered if 40 <= (l["ai_score"] or 0) < 70]
elif score_filter == "❄️ Cold (<40)":
    filtered = [l for l in filtered if (l["ai_score"] or 0) < 40]

# ── Summary bar ────────────────────────────────────────────────────────────────
hot_c    = sum(1 for l in filtered if (l["ai_score"] or 0) >= 70)
web_c    = sum(1 for l in filtered if l["has_website"])
no_web_c = len(filtered) - web_c

st.markdown(f"""
<div style="display:flex;align-items:center;gap:20px;background:#F8FAFC;border:1px solid #E2E8F0;border-radius:10px;padding:12px 20px;margin:12px 0;flex-wrap:wrap">
    <div style="font-weight:700;color:#0F172A;font-size:.95rem">{len(filtered)} leads</div>
    <div style="width:1px;height:18px;background:#E2E8F0"></div>
    <div style="font-size:.82rem;color:#059669;font-weight:600">🔥 {hot_c} hot</div>
    <div style="font-size:.82rem;color:#4F46E5;font-weight:600">✅ {web_c} with website</div>
    <div style="font-size:.82rem;color:#DC2626;font-weight:600">❌ {no_web_c} no website</div>
    <div style="margin-left:auto;display:flex;gap:8px">
    </div>
</div>
""", unsafe_allow_html=True)

# ── Export buttons ─────────────────────────────────────────────────────────────
ex1, ex2, ex3 = st.columns([1, 1, 6])
ex1.download_button("⬇ CSV",   to_csv(filtered),   f"leads_{selected_id[:8]}.csv",  "text/csv",  use_container_width=True)
ex2.download_button("⬇ Excel", to_excel(filtered), f"leads_{selected_id[:8]}.xlsx",              use_container_width=True)

st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

# ── Lead cards ─────────────────────────────────────────────────────────────────
for lead in filtered:
    score = lead["ai_score"]
    score_color = "#059669" if (score or 0) >= 70 else "#D97706" if (score or 0) >= 40 else "#DC2626"
    score_bg    = "#ECFDF5" if (score or 0) >= 70 else "#FFFBEB" if (score or 0) >= 40 else "#FEF2F2"
    initial = (lead["business_name"] or "?")[0].upper()

    with st.expander(f"**{lead['business_name']}**   ·   {'✅ Has Website' if lead['has_website'] else '❌ No Website'}   ·   {('⭐ ' + str(lead['rating'])) if lead['rating'] else 'No rating'}"):

        # Top row
        top_left, top_right = st.columns([3, 1])
        with top_left:
            st.markdown(f"""
            <div style="display:flex;align-items:flex-start;gap:16px;margin-bottom:16px">
                <div style="width:48px;height:48px;border-radius:12px;background:linear-gradient(135deg,#4F46E5,#818CF8);
                            display:flex;align-items:center;justify-content:center;color:white;font-weight:800;font-size:1.2rem;flex-shrink:0">
                    {initial}
                </div>
                <div>
                    <div style="font-size:1.05rem;font-weight:700;color:#0F172A">{lead['business_name']}</div>
                    <div style="font-size:.82rem;color:#64748B;margin-top:2px">{lead['category'] or '—'}
                        {(' · ' + lead['address']) if lead['address'] else ''}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with top_right:
            if score is not None:
                st.markdown(f"""
                <div style="text-align:center;background:{score_bg};border-radius:12px;padding:12px 16px">
                    <div style="font-size:1.8rem;font-weight:800;color:{score_color};line-height:1">{score}</div>
                    <div style="font-size:.7rem;font-weight:700;color:{score_color};text-transform:uppercase;letter-spacing:.05em;margin-top:2px">AI Score</div>
                </div>
                """, unsafe_allow_html=True)

        # Info grid
        d1, d2, d3 = st.columns(3)
        d1.markdown(f"""
        <div style="background:#F8FAFC;border-radius:8px;padding:12px;margin-bottom:8px">
            <div style="font-size:.7rem;font-weight:700;color:#94A3B8;text-transform:uppercase;letter-spacing:.04em;margin-bottom:4px">📞 Phone</div>
            <div style="font-size:.88rem;font-weight:600;color:#0F172A">{lead['phone'] or '—'}</div>
        </div>
        <div style="background:#F8FAFC;border-radius:8px;padding:12px">
            <div style="font-size:.7rem;font-weight:700;color:#94A3B8;text-transform:uppercase;letter-spacing:.04em;margin-bottom:4px">📧 Email</div>
            <div style="font-size:.88rem;font-weight:600;color:#0F172A">{lead['email'] or '—'}</div>
        </div>
        """, unsafe_allow_html=True)

        d2.markdown(f"""
        <div style="background:#F8FAFC;border-radius:8px;padding:12px;margin-bottom:8px">
            <div style="font-size:.7rem;font-weight:700;color:#94A3B8;text-transform:uppercase;letter-spacing:.04em;margin-bottom:4px">⭐ Rating</div>
            <div style="font-size:.88rem;font-weight:600;color:#0F172A">{'⭐ ' + str(lead['rating']) + '  (' + str(lead['reviews_count'] or 0) + ' reviews)' if lead['rating'] else '—'}</div>
        </div>
        <div style="background:#F8FAFC;border-radius:8px;padding:12px">
            <div style="font-size:.7rem;font-weight:700;color:#94A3B8;text-transform:uppercase;letter-spacing:.04em;margin-bottom:4px">🌐 Website Quality</div>
            <div style="font-size:.88rem;font-weight:600;color:#0F172A">{(lead['website_quality'] or '—').capitalize()}</div>
        </div>
        """, unsafe_allow_html=True)

        d3.markdown(f"""
        <div style="background:#EEF2FF;border-radius:8px;padding:12px;margin-bottom:8px;border:1px solid #C7D2FE">
            <div style="font-size:.7rem;font-weight:700;color:#6366F1;text-transform:uppercase;letter-spacing:.04em;margin-bottom:4px">💡 Suggested Service</div>
            <div style="font-size:.88rem;font-weight:700;color:#3730A3">{lead['suggested_service'] or '—'}</div>
        </div>
        """, unsafe_allow_html=True)

        if lead["website"]:
            d3.markdown(f"[🔗 Visit Website]({lead['website']})", unsafe_allow_html=False)
        if lead["maps_url"]:
            d3.markdown(f"[📍 Google Maps]({lead['maps_url']})", unsafe_allow_html=False)

        # AI Notes + Outreach
        if lead["ai_notes"]:
            st.markdown(f"""
            <div style="background:#F8FAFC;border-left:3px solid #4F46E5;border-radius:0 8px 8px 0;padding:12px 16px;margin-top:4px">
                <div style="font-size:.7rem;font-weight:700;color:#4F46E5;text-transform:uppercase;letter-spacing:.04em;margin-bottom:4px">AI Notes</div>
                <div style="font-size:.87rem;color:#334155">{lead['ai_notes']}</div>
            </div>
            """, unsafe_allow_html=True)

        if lead["outreach_message"]:
            st.markdown("""
            <div style="margin-top:12px">
                <div style="font-size:.7rem;font-weight:700;color:#94A3B8;text-transform:uppercase;letter-spacing:.04em;margin-bottom:6px">
                    ✉️ Outreach Message
                </div>
            </div>
            """, unsafe_allow_html=True)
            st.code(lead["outreach_message"], language=None)
