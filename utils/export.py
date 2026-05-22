import pandas as pd
import io

FIELDS = ["business_name","category","phone","email","website","address",
          "rating","reviews_count","has_website","ai_score",
          "suggested_service","outreach_message","maps_url"]

def leads_to_df(leads):
    if leads and isinstance(leads[0], dict):
        return pd.DataFrame([{f: l.get(f) for f in FIELDS} for l in leads])
    return pd.DataFrame([{f: getattr(l, f, None) for f in FIELDS} for l in leads])

def to_csv(leads) -> bytes:
    return leads_to_df(leads).to_csv(index=False).encode()

def to_excel(leads) -> bytes:
    buf = io.BytesIO()
    leads_to_df(leads).to_excel(buf, index=False)
    return buf.getvalue()
