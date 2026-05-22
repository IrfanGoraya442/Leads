import json
import os

PROMPT = """Analyze this business lead. Reply ONLY valid JSON, no extra text.

Business: {business_name}
Category: {category}
Rating: {rating} ({reviews_count} reviews)
Website: {website}
Phone: {phone}

Return exactly:
{{"score": <1-100>, "website_quality": "<modern|outdated|none|broken>", "suggested_service": "<short service>", "outreach_message": "<under 40 words>", "notes": "<1 sentence>"}}"""

def analyze_lead(lead: dict) -> dict:
    try:
        import ollama
        prompt = PROMPT.format(
            business_name=lead.get("business_name", ""),
            category=lead.get("category", "N/A"),
            rating=lead.get("rating", "N/A"),
            reviews_count=lead.get("reviews_count", 0),
            website=lead.get("website") or "None",
            phone=lead.get("phone") or "None",
        )
        model = os.getenv("OLLAMA_MODEL", "mistral")
        res = ollama.chat(model=model, messages=[{"role": "user", "content": prompt}], format="json")
        return json.loads(res["message"]["content"])
    except Exception:
        return _fallback(lead)

def _fallback(lead: dict) -> dict:
    has_web = bool(lead.get("website"))
    rating = lead.get("rating") or 0
    score = 50
    if not has_web: score -= 20
    if rating >= 4.5: score += 20
    elif rating >= 4.0: score += 10
    elif rating < 3.0: score -= 10
    return {
        "score": max(10, min(score, 90)),
        "website_quality": "none" if not has_web else "unknown",
        "suggested_service": "Website Development" if not has_web else "SEO & Digital Marketing",
        "outreach_message": f"Hi {lead.get('business_name','there')}, we help businesses like yours grow online.",
        "notes": "Score estimated — AI offline.",
    }
