from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import streamlit.components.v1 as components
from langchain_core.prompts import ChatPromptTemplate
from langchain_mistralai import ChatMistralAI

st.set_page_config(
    page_title="Movie Info Extractor",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Page shell CSS (Streamlit native elements only) ────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800;900&display=swap');

html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"], section.main, .block-container {
    background: #ffffff !important;
    font-family: 'Poppins', sans-serif !important;
}
.block-container { max-width:860px !important; padding-top:0 !important; }
[data-testid="stHeader"] { background:transparent !important; }
#MainMenu, header, footer, [data-testid="stDecoration"] { visibility:hidden; }

/* Orbs */
.orb-container{position:fixed;top:0;left:0;width:100%;height:100%;pointer-events:none;z-index:0;overflow:hidden;}
.orb{position:absolute;border-radius:50%;filter:blur(80px);opacity:0.18;animation:floatOrb 12s ease-in-out infinite;}
.orb1{width:420px;height:420px;background:radial-gradient(circle,#f72585,#7209b7);top:-100px;left:-80px;}
.orb2{width:350px;height:350px;background:radial-gradient(circle,#4cc9f0,#4361ee);top:10%;right:-80px;animation-delay:-4s;}
.orb3{width:300px;height:300px;background:radial-gradient(circle,#06d6a0,#4361ee);bottom:5%;left:5%;animation-delay:-8s;}
.orb4{width:260px;height:260px;background:radial-gradient(circle,#ffbe0b,#fb5607);bottom:15%;right:3%;animation-delay:-2s;}
@keyframes floatOrb{0%,100%{transform:translateY(0) scale(1);}33%{transform:translateY(-30px) scale(1.05);}66%{transform:translateY(15px) scale(0.97);}}

/* Hero */
.hero-wrap{position:relative;z-index:1;text-align:center;padding:3rem 1rem 0.5rem;}
.hero-badge{display:inline-block;background:linear-gradient(135deg,rgba(247,37,133,0.1),rgba(114,9,183,0.1));border:1px solid rgba(114,9,183,0.2);border-radius:50px;padding:0.3rem 1.1rem;font-size:0.7rem;font-weight:600;letter-spacing:0.15em;text-transform:uppercase;color:#7209b7;margin-bottom:1rem;}
.hero-title{font-size:clamp(2.2rem,5vw,3.8rem);font-weight:900;background:linear-gradient(135deg,#f72585,#7209b7,#4361ee,#4cc9f0);background-size:300% 300%;-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;animation:gradShift 5s ease infinite;margin-bottom:0.5rem;}
@keyframes gradShift{0%{background-position:0% 50%;}50%{background-position:100% 50%;}100%{background-position:0% 50%;}}
.hero-sub{font-size:0.9rem;color:#7a7a9a;margin-bottom:1rem;}
.hero-emojis{font-size:1.4rem;letter-spacing:0.4rem;margin-bottom:0.5rem;animation:pulse 3s ease-in-out infinite;}
@keyframes pulse{0%,100%{opacity:1;}50%{opacity:0.6;}}
.glow-divider{height:3px;max-width:260px;margin:1rem auto 1.8rem;border-radius:99px;background:linear-gradient(90deg,#f72585,#7209b7,#4361ee,#4cc9f0,#f72585);background-size:300% 100%;animation:slideGrad 3s linear infinite;box-shadow:0 0 16px rgba(114,9,183,0.3);}
@keyframes slideGrad{0%{background-position:0%;}100%{background-position:300%;}}

/* Stats */
.stats-bar{display:flex;justify-content:center;gap:2.5rem;margin:1rem 0;flex-wrap:wrap;position:relative;z-index:1;}
.stat-item{text-align:center;}
.stat-val{font-size:1.5rem;font-weight:800;background:linear-gradient(135deg,#f72585,#7209b7);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;}
.stat-label{font-size:0.62rem;color:#aaaacc;text-transform:uppercase;letter-spacing:0.1em;margin-top:2px;}

/* Pills */
.pills-row{display:flex;flex-wrap:wrap;gap:0.5rem;justify-content:center;margin-bottom:1.5rem;}
.pill{background:linear-gradient(135deg,rgba(247,37,133,0.07),rgba(76,201,240,0.07));border:1px solid rgba(114,9,183,0.15);border-radius:50px;padding:0.28rem 0.85rem;font-size:0.72rem;font-weight:500;color:#5a5a7a;}

/* Textarea */
[data-testid="stTextArea"] textarea{background:#fafaff !important;border:2px solid #ebebf8 !important;border-radius:16px !important;color:#1a1a2e !important;font-family:'Poppins',sans-serif !important;font-size:0.88rem !important;line-height:1.75 !important;padding:1rem 1.2rem !important;}
[data-testid="stTextArea"] textarea:focus{border-color:#7209b7 !important;box-shadow:0 0 0 4px rgba(114,9,183,0.08) !important;}
[data-testid="stTextArea"] label{font-family:'Poppins',sans-serif !important;font-size:0.72rem !important;font-weight:700 !important;letter-spacing:0.1em !important;color:#7209b7 !important;text-transform:uppercase !important;}

/* Button */
[data-testid="stButton"] button{background:linear-gradient(135deg,#f72585,#7209b7,#4361ee,#4cc9f0) !important;background-size:300% 300% !important;animation:btnPulse 4s ease infinite !important;color:#fff !important;border:none !important;border-radius:50px !important;font-family:'Poppins',sans-serif !important;font-size:0.9rem !important;font-weight:700 !important;padding:0.75rem 2rem !important;width:100% !important;box-shadow:0 4px 24px rgba(114,9,183,0.3) !important;}
[data-testid="stButton"] button:hover{transform:translateY(-3px) !important;}
@keyframes btnPulse{0%,100%{background-position:0% 50%;}50%{background-position:100% 50%;}}

[data-testid="stSpinner"] p{font-family:'Poppins',sans-serif !important;color:#7209b7 !important;font-weight:600 !important;}
.footer{text-align:center;padding:2rem 0 1rem;font-size:0.65rem;letter-spacing:0.15em;color:#c0c0d8;text-transform:uppercase;position:relative;z-index:1;}
</style>
""", unsafe_allow_html=True)


# ── Model ──────────────────────────────────────────────────────────────────────
@st.cache_resource
def get_model_and_prompt():
    model = ChatMistralAI(model="mistral-small-2506")
    prompt = ChatPromptTemplate.from_messages([
        ("system", """
You are a professional Movie Information Extraction Assistant.
Extract useful structured information from a movie paragraph.
Rules:
- Do NOT add explanations or commentary.
- Follow the exact format below.
- If information is missing, write NULL.
- Keep the summary short (2-3 lines maximum).
- Do NOT guess unknown facts.

Format:
Movie Title:
Release Year:
Genre:
Director:
Main Cast:
Setting/Location:
Plot:
Themes:
Ratings:
Notable Features:
Short Summary:
"""),
        ("human", "{movie_text}")
    ])
    return model, prompt


# ── Helpers ────────────────────────────────────────────────────────────────────
FIELDS = [
    ("Movie Title",      "🎬"),
    ("Release Year",     "📅"),
    ("Genre",            "🎭"),
    ("Director",         "🎥"),
    ("Main Cast",        "⭐"),
    ("Setting/Location", "📍"),
    ("Plot",             "📖"),
    ("Themes",           "💡"),
    ("Ratings",          "🏆"),
    ("Notable Features", "✨"),
    ("Short Summary",    "📝"),
]
TAG_FIELDS = {"Genre", "Main Cast", "Setting/Location", "Themes", "Notable Features"}

def parse_response(text: str) -> dict:
    lines = text.strip().splitlines()
    data, current_key, current_val = {}, None, []
    all_keys = [f[0] for f in FIELDS]
    for line in lines:
        matched = False
        for key in all_keys:
            if line.startswith(f"{key}:"):
                if current_key:
                    data[current_key] = " ".join(current_val).strip()
                current_key = key
                current_val = [line[len(key)+1:].strip()]
                matched = True
                break
        if not matched and current_key:
            current_val.append(line.strip())
    if current_key:
        data[current_key] = " ".join(current_val).strip()
    return data


def build_iframe_html(raw_text: str) -> str:
    """Build a fully self-contained HTML page for iframe rendering."""
    parsed = parse_response(raw_text)

    rows = ""
    for key, icon in FIELDS:
        val = parsed.get(key, "NULL")
        is_null = not val or val.upper() in ("NULL", "N/A")
        display = val if val else "NULL"

        if key == "Short Summary":
            value_html = f'<div class="summary-block">{display}</div>'
        elif key in TAG_FIELDS and not is_null and "," in display:
            tags = "".join(
                f'<span class="val-tag">{p.strip()}</span>'
                for p in display.split(",") if p.strip()
            )
            value_html = f'<div class="field-value">{tags}</div>'
        else:
            null_cls = " null-val" if is_null else ""
            value_html = f'<div class="field-value{null_cls}">{display}</div>'

        rows += f"""
        <div class="field-row">
            <div class="field-icon">{icon}</div>
            <div class="field-label">{key}</div>
            {value_html}
        </div>"""

    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
<style>
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  body {{ font-family:'Poppins',sans-serif; background:transparent; padding:4px; }}

  .result-outer {{
    border-radius: 20px;
    padding: 3px;
    background: linear-gradient(135deg, #f72585, #7209b7, #3a0ca3, #4361ee, #4cc9f0, #06d6a0, #f72585);
    background-size: 300% 300%;
    animation: borderGlow 4s linear infinite;
    box-shadow: 0 0 40px rgba(114,9,183,0.2), 0 20px 60px rgba(247,37,133,0.1);
  }}
  @keyframes borderGlow {{
    0%   {{ background-position: 0% 50%; }}
    50%  {{ background-position: 100% 50%; }}
    100% {{ background-position: 0% 50%; }}
  }}

  .result-inner {{ background:#ffffff; border-radius:18px; overflow:hidden; }}

  .card-header {{
    background: linear-gradient(135deg, #f72585 0%, #7209b7 35%, #3a0ca3 65%, #4cc9f0 100%);
    padding: 1.2rem 1.8rem;
    display: flex; align-items: center; justify-content: space-between;
  }}
  .card-header-left {{ display:flex; align-items:center; gap:0.7rem; }}
  .card-header-icon {{ font-size:1.5rem; }}
  .card-header-text {{ font-size:1rem; font-weight:700; color:#fff; }}
  .card-header-badge {{
    background: rgba(255,255,255,0.2);
    border: 1px solid rgba(255,255,255,0.35);
    border-radius: 50px; padding: 0.2rem 0.8rem;
    font-size: 0.65rem; font-weight:700; color:#fff;
    letter-spacing: 0.12em; text-transform: uppercase;
  }}

  .field-row {{
    display: flex; align-items: flex-start; gap: 1rem;
    padding: 0.85rem 1.8rem;
    border-bottom: 1px solid #f3f3fa;
    transition: background 0.2s;
  }}
  .field-row:hover {{ background: linear-gradient(90deg,rgba(247,37,133,0.03),rgba(76,201,240,0.03)); }}
  .field-row:last-child {{ border-bottom: none; }}

  .field-icon {{ font-size:1.05rem; min-width:26px; text-align:center; padding-top:2px; }}
  .field-label {{
    font-size: 0.67rem; font-weight:700; letter-spacing:0.1em;
    text-transform: uppercase; min-width:128px; padding-top:4px;
    background: linear-gradient(135deg,#f72585,#7209b7);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text;
  }}
  .field-value {{ font-size:0.87rem; font-weight:400; color:#2a2a4a; line-height:1.65; flex:1; }}
  .field-value.null-val {{ color:#c8c8de; font-style:italic; }}

  .val-tag {{
    display: inline-block;
    background: linear-gradient(135deg,rgba(247,37,133,0.09),rgba(114,9,183,0.09));
    border: 1px solid rgba(114,9,183,0.15);
    border-radius: 20px; padding: 0.12rem 0.7rem;
    font-size: 0.78rem; color:#5a2a7a;
    margin: 2px 3px 2px 0; font-weight:500;
  }}

  .summary-block {{
    flex: 1;
    background: linear-gradient(135deg,rgba(247,37,133,0.05),rgba(76,201,240,0.05));
    border: 1px solid rgba(114,9,183,0.1);
    border-radius: 12px; padding: 0.85rem 1.1rem;
    font-size: 0.87rem; color:#3a3a5c;
    line-height: 1.8; font-style:italic;
    position: relative; overflow:hidden;
  }}
  .summary-block::before {{
    content: '"'; position:absolute; top:-8px; left:8px;
    font-size:3.5rem; color:rgba(114,9,183,0.07);
    font-family:Georgia,serif; line-height:1;
  }}
</style>
</head>
<body>
  <div class="result-outer">
    <div class="result-inner">
      <div class="card-header">
        <div class="card-header-left">
          <span class="card-header-icon">🎞️</span>
          <span class="card-header-text">Extracted Movie Intelligence</span>
        </div>
        <span class="card-header-badge">✦ AI Powered</span>
      </div>
      {rows}
    </div>
  </div>
</body>
</html>"""


# ── UI ─────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="orb-container">
  <div class="orb orb1"></div><div class="orb orb2"></div>
  <div class="orb orb3"></div><div class="orb orb4"></div>
</div>
<div class="hero-wrap">
  <div class="hero-badge">✦ AI-Powered Extraction Engine</div>
  <div class="hero-emojis">🎬 🎭 🎥 🌟 🏆</div>
  <div class="hero-title">🎬 Movie Info Extractor</div>
  <div class="hero-sub">Paste any movie description — get clean, structured intelligence instantly</div>
</div>
<div class="glow-divider"></div>
<div class="stats-bar">
  <div class="stat-item"><div class="stat-val">11</div><div class="stat-label">Data Fields</div></div>
  <div class="stat-item"><div class="stat-val">🤖</div><div class="stat-label">Mistral AI</div></div>
  <div class="stat-item"><div class="stat-val">⚡</div><div class="stat-label">Instant</div></div>
  <div class="stat-item"><div class="stat-val">🎯</div><div class="stat-label">Accurate</div></div>
</div>
<div class="pills-row">
  <span class="pill">📰 Wikipedia snippets</span>
  <span class="pill">🎞️ IMDb descriptions</span>
  <span class="pill">✍️ Film critic reviews</span>
  <span class="pill">📋 Your own notes</span>
</div>
""", unsafe_allow_html=True)

movie_text = st.text_area(
    "🎬  Paste Your Movie Paragraph",
    placeholder=(
        "Paste a movie description, review, Wikipedia snippet, or plot summary here...\n\n"
        "Example: Interstellar (2014), directed by Christopher Nolan, stars Matthew McConaughey "
        "as a former NASA pilot who leads a crew through a wormhole in search of a new home for humanity..."
    ),
    height=190,
)

go = st.button("✦ 💕Extract Movie Information💖✦", use_container_width=True)

if go:
    if not movie_text.strip():
        st.warning("⚠️ Please paste a movie paragraph before extracting.")
    else:
        model, prompt = get_model_and_prompt()
        with st.spinner("🎬Extracting movie intelligence.💕💕"):
            try:
                final_prompt = prompt.invoke({"movie_text": movie_text})
                response = model.invoke(final_prompt)
                # ✅ KEY FIX: use components.html() — renders HTML in an iframe, 
                # completely bypasses Streamlit's HTML sanitizer
                components.html(
                    build_iframe_html(response.content),
                    height=860,
                    scrolling=False,
                )
            except Exception as e:
                st.error(f"❌ Extraction failed: {e}")

st.markdown("""
<div class="footer">
  <div style="font-size:1rem;letter-spacing:0.4rem;opacity:0.4;margin-bottom:0.4rem">🎬 🎭 🎥 🌟</div>
  Powered by Mistral AI · LangChain · Streamlit
</div>
""", unsafe_allow_html=True)
