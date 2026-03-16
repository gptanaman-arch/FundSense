import streamlit as st
import requests
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings("ignore")

st.set_page_config(
    page_title="FundSense",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ══════════════════════════════════════════════════════════════
# CSS — Deep forest green + gold. Premium wealth aesthetic.
# ══════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500;600&family=Fira+Code:wght@400;500&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background: #0B0F0E !important;
    color: #D4CFBF;
    -webkit-font-smoothing: antialiased;
}
.main { background: #0B0F0E !important; }
.block-container { padding: 0.5rem 1rem 3rem !important; max-width: 1400px !important; }

::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: #0B0F0E; }
::-webkit-scrollbar-thumb { background: #C9A84C; border-radius: 4px; }

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #0E1412 !important;
    border-right: 1px solid #1E2B27 !important;
}

/* Header */
.fs-header {
    padding: 28px 0 20px;
    border-bottom: 1px solid #1E2B27;
    margin-bottom: 24px;
    display: flex;
    align-items: baseline;
    gap: 14px;
}
.fs-logo {
    font-family: 'DM Serif Display', serif;
    font-size: clamp(28px, 4vw, 40px);
    font-weight: 400;
    color: #F0E6C8;
    letter-spacing: -0.5px;
}
.fs-logo span { color: #C9A84C; }
.fs-tagline {
    font-size: 12px;
    color: #4A6358;
    text-transform: uppercase;
    letter-spacing: 2px;
    font-weight: 500;
}

/* Fund card */
.fund-card {
    background: #0E1412;
    border: 1px solid #1E2B27;
    border-radius: 12px;
    padding: 20px 22px;
    margin-bottom: 16px;
    position: relative;
    overflow: hidden;
}
.fund-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, #C9A84C, #8BA888);
}
.fund-name {
    font-family: 'DM Serif Display', serif;
    font-size: clamp(16px, 2.5vw, 22px);
    color: #F0E6C8;
    font-weight: 400;
    line-height: 1.3;
    margin-bottom: 6px;
}
.fund-meta {
    font-size: 11px;
    color: #4A6358;
    text-transform: uppercase;
    letter-spacing: 1.2px;
    margin-bottom: 14px;
}
.fund-nav-big {
    font-family: 'Fira Code', monospace;
    font-size: clamp(28px, 4vw, 42px);
    color: #C9A84C;
    font-weight: 500;
    letter-spacing: -1px;
}
.fund-nav-change {
    font-family: 'Fira Code', monospace;
    font-size: 14px;
    margin-left: 10px;
}

/* Returns strip */
.returns-strip {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-top: 14px;
}
.ret-cell {
    background: #111A17;
    border: 1px solid #1E2B27;
    border-radius: 8px;
    padding: 8px 14px;
    text-align: center;
    flex: 1;
    min-width: 70px;
}
.ret-label { font-size: 10px; color: #4A6358; text-transform: uppercase; letter-spacing: 1px; }
.ret-val { font-family: 'Fira Code', monospace; font-size: 15px; font-weight: 500; margin-top: 2px; }

/* KPI grid */
.kpi-row {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    margin: 16px 0;
}
.kpi-box {
    background: #0E1412;
    border: 1px solid #1E2B27;
    border-radius: 10px;
    padding: 14px 16px;
    flex: 1;
    min-width: 120px;
}
.kpi-lbl { font-size: 10px; color: #4A6358; text-transform: uppercase; letter-spacing: 1px; }
.kpi-val { font-family: 'Fira Code', monospace; font-size: 18px; color: #F0E6C8; margin-top: 3px; }

/* Section title */
.sec-title {
    font-family: 'DM Serif Display', serif;
    font-size: 20px;
    color: #F0E6C8;
    font-weight: 400;
    margin: 22px 0 12px;
    padding-bottom: 8px;
    border-bottom: 1px solid #1E2B27;
}

/* AI insight box */
.ai-box {
    background: linear-gradient(135deg, #0E1A16 0%, #0B1510 100%);
    border: 1px solid #2A4A3A;
    border-radius: 12px;
    padding: 22px 24px;
    margin: 14px 0;
    position: relative;
}
.ai-box::before {
    content: 'AI INSIGHT';
    position: absolute;
    top: -10px; left: 20px;
    background: #0B0F0E;
    padding: 2px 10px;
    font-size: 9px;
    color: #C9A84C;
    letter-spacing: 2px;
    font-weight: 600;
    border: 1px solid #2A4A3A;
    border-radius: 4px;
}
.ai-text {
    font-size: 14px;
    line-height: 1.8;
    color: #C4BFB0;
}

/* SIP result */
.sip-result {
    background: #0E1412;
    border: 1px solid #C9A84C40;
    border-radius: 12px;
    padding: 20px 22px;
    text-align: center;
    margin-top: 10px;
}
.sip-corpus {
    font-family: 'DM Serif Display', serif;
    font-size: clamp(28px,4vw,42px);
    color: #C9A84C;
}
.sip-breakdown { font-size: 12px; color: #4A6358; margin-top: 6px; line-height: 2; }

/* Tags */
.tag {
    display: inline-block;
    background: #111A17;
    border: 1px solid #1E2B27;
    border-radius: 20px;
    padding: 3px 12px;
    font-size: 11px;
    color: #8BA888;
    margin: 2px 3px 2px 0;
    font-weight: 500;
}

/* Compare mode */
.compare-divider {
    width: 1px;
    background: #1E2B27;
    margin: 0 12px;
}

/* Buttons */
.stButton > button {
    background: #C9A84C !important;
    color: #0B0F0E !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 13px !important;
    padding: 10px 20px !important;
    letter-spacing: 0.5px !important;
    transition: all 0.2s !important;
}
.stButton > button:hover { background: #E0BC6A !important; }

/* Secondary button */
.stButton.secondary > button {
    background: transparent !important;
    color: #8BA888 !important;
    border: 1px solid #1E2B27 !important;
}

/* Inputs */
.stTextInput > div > div > input,
.stNumberInput > div > div > input,
.stSelectbox > div > div {
    background: #0E1412 !important;
    border: 1px solid #1E2B27 !important;
    color: #D4CFBF !important;
    border-radius: 8px !important;
    font-family: 'DM Sans', sans-serif !important;
}
.stSlider > div > div > div { background: #C9A84C !important; }

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: transparent !important;
    border-bottom: 1px solid #1E2B27 !important;
    gap: 0 !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: #4A6358 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 500 !important;
    font-size: 13px !important;
    padding: 10px 20px !important;
    border: none !important;
}
.stTabs [aria-selected="true"] {
    color: #C9A84C !important;
    border-bottom: 2px solid #C9A84C !important;
}

/* Spinner */
.stSpinner > div { border-top-color: #C9A84C !important; }

/* Metrics */
[data-testid="stMetric"] {
    background: #0E1412 !important;
    border: 1px solid #1E2B27 !important;
    border-radius: 10px !important;
    padding: 12px 14px !important;
}
[data-testid="stMetricLabel"] { color: #4A6358 !important; font-size: 11px !important; }
[data-testid="stMetricValue"] { color: #F0E6C8 !important; font-family: 'Fira Code', monospace !important; }
[data-testid="stMetricDelta"] { font-size: 12px !important; }

.footer {
    text-align: center;
    color: #1E2B27;
    font-size: 11px;
    padding: 24px;
    border-top: 1px solid #1E2B27;
    margin-top: 32px;
}
hr { border-color: #1E2B27 !important; }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# MFAPI.IN  — free, no key needed
# ══════════════════════════════════════════════════════════════
MFAPI = "https://api.mfapi.in"
ANTHROPIC_KEY = ""   # set via st.secrets or sidebar

@st.cache_data(ttl=3600, show_spinner=False)
def search_funds(query):
    try:
        r = requests.get(f"{MFAPI}/mf/search", params={"q": query}, timeout=10)
        if r.status_code == 200:
            return r.json()
    except Exception:
        pass
    return []

@st.cache_data(ttl=1800, show_spinner=False)
def get_fund_data(scheme_code):
    try:
        r = requests.get(f"{MFAPI}/mf/{scheme_code}", timeout=15)
        if r.status_code == 200:
            return r.json()
    except Exception:
        pass
    return None

def parse_nav_history(data):
    """Convert API nav list to DataFrame sorted oldest→newest."""
    if not data or "data" not in data:
        return pd.DataFrame()
    rows = []
    for d in data["data"]:
        try:
            rows.append({"date": datetime.strptime(d["date"], "%d-%m-%Y"), "nav": float(d["nav"])})
        except Exception:
            continue
    if not rows:
        return pd.DataFrame()
    df = pd.DataFrame(rows).sort_values("date").reset_index(drop=True)
    return df

def compute_returns(df):
    """Compute trailing returns for various periods."""
    if df.empty:
        return {}
    latest = df.iloc[-1]["nav"]
    today  = df.iloc[-1]["date"]
    result = {}
    periods = {"1W": 7, "1M": 30, "3M": 90, "6M": 180, "1Y": 365, "3Y": 1095}
    for label, days in periods.items():
        cutoff = today - timedelta(days=days)
        subset = df[df["date"] <= cutoff]
        if not subset.empty:
            past_nav = subset.iloc[-1]["nav"]
            if days >= 365:
                years = days / 365
                cagr  = ((latest / past_nav) ** (1 / years) - 1) * 100
                result[label] = round(cagr, 2)
            else:
                result[label] = round((latest / past_nav - 1) * 100, 2)
        else:
            result[label] = None
    return result

def filter_period(df, period):
    if df.empty:
        return df
    latest = df.iloc[-1]["date"]
    days   = {"1M":30,"3M":90,"6M":180,"1Y":365,"3Y":1095,"5Y":1825,"All":99999}
    cutoff = latest - timedelta(days=days.get(period, 99999))
    return df[df["date"] >= cutoff].reset_index(drop=True)

def sip_projection(monthly, years, cagr_pct):
    r     = (cagr_pct / 100) / 12
    n     = years * 12
    if r == 0:
        corpus = monthly * n
    else:
        corpus = monthly * (((1 + r) ** n - 1) / r) * (1 + r)
    invested = monthly * n
    gain     = corpus - invested
    return round(corpus), round(invested), round(gain)

def nav_chart(df, label, color="#C9A84C", height=340):
    if df.empty:
        return None
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["date"], y=df["nav"],
        mode="lines",
        line=dict(color=color, width=2),
        fill="tozeroy",
        fillcolor="rgba(201,168,76,0.08)",
        hovertemplate="<b>%{x|%d %b %Y}</b><br>NAV: ₹%{y:.4f}<extra></extra>",
        name=label,
    ))
    fig.update_layout(
        height=height,
        margin=dict(l=0, r=0, t=10, b=0),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#0E1412",
        font=dict(family="DM Sans", size=11, color="#4A6358"),
        xaxis=dict(gridcolor="#1E2B27", linecolor="#1E2B27", showgrid=True,
                   tickfont=dict(color="#4A6358"), zeroline=False),
        yaxis=dict(gridcolor="#1E2B27", linecolor="#1E2B27", showgrid=True,
                   tickfont=dict(color="#4A6358"), tickprefix="₹", zeroline=False),
        hovermode="x unified",
        showlegend=False,
    )
    return fig

def compare_chart(df1, name1, df2, name2, height=340):
    # Normalise both to 100 at start of overlap
    if df1.empty or df2.empty:
        return None
    start = max(df1["date"].min(), df2["date"].min())
    d1 = df1[df1["date"] >= start].copy()
    d2 = df2[df2["date"] >= start].copy()
    if d1.empty or d2.empty:
        return None
    base1 = d1.iloc[0]["nav"]
    base2 = d2.iloc[0]["nav"]
    d1["norm"] = d1["nav"] / base1 * 100
    d2["norm"] = d2["nav"] / base2 * 100
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=d1["date"], y=d1["norm"], mode="lines",
        line=dict(color="#C9A84C", width=2), name=name1[:30],
        hovertemplate="<b>" + name1[:20] + "</b><br>%{y:.1f}<extra></extra>"))
    fig.add_trace(go.Scatter(x=d2["date"], y=d2["norm"], mode="lines",
        line=dict(color="#8BA888", width=2), name=name2[:30],
        hovertemplate="<b>" + name2[:20] + "</b><br>%{y:.1f}<extra></extra>"))
    fig.update_layout(
        height=height, margin=dict(l=0,r=0,t=10,b=0),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="#0E1412",
        font=dict(family="DM Sans", size=11, color="#4A6358"),
        xaxis=dict(gridcolor="#1E2B27", linecolor="#1E2B27", tickfont=dict(color="#4A6358")),
        yaxis=dict(gridcolor="#1E2B27", linecolor="#1E2B27", tickfont=dict(color="#4A6358"),
                   ticksuffix=""),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#D4CFBF", size=11)),
        hovermode="x unified",
    )
    return fig

def sip_chart(months, corpus_vals, invested_vals, height=280):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=months, y=corpus_vals, mode="lines",
        line=dict(color="#C9A84C", width=2.5),
        fill="tozeroy", fillcolor="rgba(201,168,76,0.08)",
        name="Corpus", hovertemplate="Year %{x}: ₹%{y:,.0f}<extra></extra>"))
    fig.add_trace(go.Scatter(x=months, y=invested_vals, mode="lines",
        line=dict(color="#4A6358", width=1.5, dash="dot"),
        name="Invested", hovertemplate="Invested: ₹%{y:,.0f}<extra></extra>"))
    fig.update_layout(
        height=height, margin=dict(l=0,r=0,t=10,b=0),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="#0E1412",
        font=dict(family="DM Sans", size=11, color="#4A6358"),
        xaxis=dict(gridcolor="#1E2B27", linecolor="#1E2B27", tickfont=dict(color="#4A6358"),
                   title=dict(text="Year", font=dict(color="#4A6358"))),
        yaxis=dict(gridcolor="#1E2B27", linecolor="#1E2B27", tickfont=dict(color="#4A6358"),
                   tickprefix="₹"),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#D4CFBF", size=11)),
        hovermode="x unified",
    )
    return fig

def get_ai_insight(fund_meta, returns, nav_latest, api_key):
    """Call Claude API for fund insight."""
    if not api_key:
        return None
    prompt = f"""You are an expert Indian mutual fund analyst. Analyse this fund and give a clear, useful insight for a retail investor.

Fund: {fund_meta.get('scheme_name','')}
Category: {fund_meta.get('scheme_category','')}
Fund House: {fund_meta.get('fund_house','')}
Type: {fund_meta.get('scheme_type','')}
Latest NAV: ₹{nav_latest:.2f}

Trailing Returns:
{chr(10).join([f"  {k}: {v}%" for k,v in returns.items() if v is not None])}

Write 3–4 sentences covering:
1. What kind of investor this fund suits
2. How the returns look vs category benchmarks
3. One key risk to watch
4. Overall verdict (good/average/poor for long-term SIP)

Be direct and specific. No generic disclaimers. Write in plain English suitable for a young Indian investor."""

    try:
        r = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "x-api-key": api_key,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json",
            },
            json={
                "model": "claude-sonnet-4-20250514",
                "max_tokens": 300,
                "messages": [{"role": "user", "content": prompt}],
            },
            timeout=20,
        )
        if r.status_code == 200:
            return r.json()["content"][0]["text"]
    except Exception:
        pass
    return None

# ══════════════════════════════════════════════════════════════
# HEADER
# ══════════════════════════════════════════════════════════════
st.markdown("""
<div class="fs-header">
  <div class="fs-logo">Fund<span>Sense</span></div>
  <div class="fs-tagline">Indian Mutual Fund Analyser · Powered by AI</div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# SIDEBAR — API key + mode
# ══════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div style="padding:16px 0 10px">
      <div style="font-family:'DM Serif Display',serif;font-size:22px;color:#F0E6C8">FundSense</div>
      <div style="font-size:10px;color:#4A6358;letter-spacing:2px;text-transform:uppercase;margin-top:3px">Settings</div>
    </div>""", unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)

    st.markdown('<div style="font-size:11px;color:#4A6358;text-transform:uppercase;letter-spacing:1px;margin-bottom:6px">Claude API Key</div>', unsafe_allow_html=True)
    api_key_input = st.text_input("API Key", type="password", label_visibility="collapsed",
                                   placeholder="sk-ant-... (for AI insights)")
    if api_key_input:
        st.markdown('<div style="font-size:11px;color:#8BA888;margin-top:4px">✓ AI insights enabled</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div style="font-size:11px;color:#4A6358;margin-top:4px">Enter key to unlock AI insights</div>', unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    mode = st.radio("Mode", ["Single Fund", "Compare Funds"], label_visibility="collapsed")
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("""<div style="font-size:10px;color:#1E2B27;line-height:2.2">
    Data: mfapi.in (AMFI)<br>
    AI: Anthropic Claude<br>
    Updates: Daily NAV<br>
    <span style="color:#2A4A3A">Not financial advice</span>
    </div>""", unsafe_allow_html=True)

ANTHROPIC_KEY = api_key_input

# ══════════════════════════════════════════════════════════════
# SINGLE FUND MODE
# ══════════════════════════════════════════════════════════════
if mode == "Single Fund":
    st.markdown('<div class="sec-title">Search Fund</div>', unsafe_allow_html=True)

    col_search, col_btn = st.columns([4, 1])
    with col_search:
        query = st.text_input("search", placeholder="e.g. Mirae Asset Large Cap, SBI Small Cap, HDFC Flexi Cap...",
                               label_visibility="collapsed")
    with col_btn:
        search_btn = st.button("Search", width='stretch')

    if query and (search_btn or "fund_results" in st.session_state):
        if search_btn or "fund_query" not in st.session_state or st.session_state.fund_query != query:
            with st.spinner("Searching..."):
                results = search_funds(query)
                st.session_state.fund_results = results
                st.session_state.fund_query   = query
                st.session_state.fund_data    = None
                st.session_state.ai_insight   = None

        results = st.session_state.get("fund_results", [])
        if not results:
            st.warning("No funds found. Try a different search term.")
        else:
            # Filter to Growth / Direct plans first, then show all
            growth = [r for r in results if "growth" in r["schemeName"].lower() and "direct" in r["schemeName"].lower()]
            display = growth[:8] if growth else results[:8]

            options = {r["schemeName"]: r["schemeCode"] for r in display}
            chosen_name = st.selectbox("Select fund", list(options.keys()), label_visibility="collapsed")
            chosen_code = options[chosen_name]

            col_a, col_b = st.columns([1, 1])
            with col_a:
                analyse_btn = st.button("Analyse Fund ›", width='stretch')
            with col_b:
                period_sel = st.selectbox("Chart period", ["1M","3M","6M","1Y","3Y","5Y","All"],
                                           index=3, label_visibility="collapsed")

            if analyse_btn or st.session_state.get("fund_data") is not None:
                if analyse_btn:
                    with st.spinner("Fetching fund data..."):
                        data = get_fund_data(chosen_code)
                        st.session_state.fund_data   = data
                        st.session_state.ai_insight  = None
                        st.session_state.chosen_code = chosen_code

                data = st.session_state.get("fund_data")
                if not data:
                    st.error("Could not fetch fund data. Try again.")
                else:
                    meta = data.get("meta", {})
                    df   = parse_nav_history(data)
                    returns = compute_returns(df)

                    if df.empty:
                        st.error("No NAV history available.")
                    else:
                        latest_nav  = df.iloc[-1]["nav"]
                        latest_date = df.iloc[-1]["date"].strftime("%d %b %Y")
                        prev_nav    = df.iloc[-2]["nav"] if len(df) > 1 else latest_nav
                        day_change  = latest_nav - prev_nav
                        day_pct     = (day_change / prev_nav) * 100
                        chg_color   = "#8BA888" if day_change >= 0 else "#C47A7A"
                        chg_arrow   = "▲" if day_change >= 0 else "▼"

                        # ── Fund card
                        cat  = meta.get("scheme_category", "")
                        house = meta.get("fund_house", "")
                        st.markdown(f"""
                        <div class="fund-card">
                          <div class="fund-meta">{house} &nbsp;·&nbsp; {cat}</div>
                          <div class="fund-name">{meta.get('scheme_name','')}</div>
                          <div style="display:flex;align-items:baseline;gap:4px">
                            <div class="fund-nav-big">₹{latest_nav:,.4f}</div>
                            <div class="fund-nav-change" style="color:{chg_color}">{chg_arrow} ₹{abs(day_change):.4f} ({day_pct:+.2f}%)</div>
                          </div>
                          <div style="font-size:11px;color:#4A6358;margin-top:4px">As of {latest_date}</div>
                          <div class="returns-strip">
                            {''.join([
                              f'<div class="ret-cell"><div class="ret-label">{k}</div>'
                              f'<div class="ret-val" style="color:{"#8BA888" if (v or 0)>=0 else "#C47A7A"}">'
                              f'{"—" if v is None else f"{v:+.1f}%"}</div></div>'
                              for k,v in returns.items()
                            ])}
                          </div>
                        </div>""", unsafe_allow_html=True)

                        # ── Tabs
                        tab1, tab2, tab3, tab4 = st.tabs(["📈 NAV Chart", "💰 SIP Calculator", "🤖 AI Insight", "ℹ️ Details"])

                        # ── Tab 1: NAV Chart
                        with tab1:
                            df_plot = filter_period(df, period_sel)
                            fig = nav_chart(df_plot, meta.get("scheme_name",""), "#C9A84C")
                            if fig:
                                st.plotly_chart(fig, width='stretch')

                            # Stats
                            if not df_plot.empty:
                                hi = df_plot["nav"].max()
                                lo = df_plot["nav"].min()
                                cols = st.columns(3)
                                cols[0].metric("Period High", f"₹{hi:,.2f}")
                                cols[1].metric("Period Low",  f"₹{lo:,.2f}")
                                cols[2].metric("Data Points", f"{len(df_plot):,}")

                        # ── Tab 2: SIP Calculator
                        with tab2:
                            st.markdown('<div class="sec-title" style="margin-top:8px">SIP Projection</div>', unsafe_allow_html=True)
                            c1, c2, c3 = st.columns(3)
                            with c1:
                                sip_amt = st.number_input("Monthly SIP (₹)", min_value=500, max_value=1000000,
                                                           value=5000, step=500, label_visibility="visible")
                            with c2:
                                sip_yrs = st.slider("Investment period (years)", 1, 30, 10)
                            with c3:
                                # Use 1Y return as default expected return, fallback to 12%
                                default_ret = returns.get("1Y") or returns.get("3Y") or 12.0
                                default_ret = max(1.0, min(float(default_ret), 40.0))
                                exp_ret = st.number_input("Expected annual return (%)", min_value=1.0, max_value=50.0,
                                                           value=round(default_ret, 1), step=0.5)

                            corpus, invested, gain = sip_projection(sip_amt, sip_yrs, exp_ret)

                            st.markdown(f"""
                            <div class="sip-result">
                              <div style="font-size:11px;color:#4A6358;text-transform:uppercase;letter-spacing:1px;margin-bottom:6px">Projected Corpus after {sip_yrs} years</div>
                              <div class="sip-corpus">₹{corpus:,.0f}</div>
                              <div class="sip-breakdown">
                                Invested: ₹{invested:,.0f} &nbsp;·&nbsp;
                                Est. Gain: ₹{gain:,.0f} &nbsp;·&nbsp;
                                Wealth Ratio: {corpus/invested:.1f}x
                              </div>
                            </div>""", unsafe_allow_html=True)

                            # Growth chart
                            month_list, corpus_list, inv_list = [], [], []
                            for y in range(1, sip_yrs + 1):
                                c_, i_, _ = sip_projection(sip_amt, y, exp_ret)
                                month_list.append(y)
                                corpus_list.append(c_)
                                inv_list.append(i_)
                            fig2 = sip_chart(month_list, corpus_list, inv_list)
                            if fig2:
                                st.plotly_chart(fig2, width='stretch')

                        # ── Tab 3: AI Insight
                        with tab3:
                            if not ANTHROPIC_KEY:
                                st.markdown("""
                                <div style="text-align:center;padding:40px 20px;border:1px dashed #1E2B27;border-radius:12px;margin-top:10px">
                                  <div style="font-size:32px;margin-bottom:12px">🔑</div>
                                  <div style="font-family:'DM Serif Display',serif;font-size:20px;color:#F0E6C8;margin-bottom:8px">Enter your Claude API Key</div>
                                  <div style="font-size:13px;color:#4A6358">Add your Anthropic API key in the sidebar to unlock AI-powered fund analysis</div>
                                </div>""", unsafe_allow_html=True)
                            else:
                                if st.session_state.get("ai_insight") is None or st.session_state.get("ai_fund") != chosen_code:
                                    with st.spinner("Generating AI insight..."):
                                        insight = get_ai_insight(meta, returns, latest_nav, ANTHROPIC_KEY)
                                        st.session_state.ai_insight = insight
                                        st.session_state.ai_fund    = chosen_code

                                insight = st.session_state.get("ai_insight")
                                if insight:
                                    st.markdown(f'<div class="ai-box"><div class="ai-text">{insight}</div></div>', unsafe_allow_html=True)

                                    # Quick verdict chips
                                    one_y = returns.get("1Y")
                                    three_y = returns.get("3Y")
                                    chips = []
                                    if one_y and one_y > 15: chips.append(("Strong 1Y return", "#8BA888"))
                                    elif one_y and one_y < 5: chips.append(("Weak 1Y return", "#C47A7A"))
                                    if three_y and three_y > 12: chips.append(("Solid 3Y CAGR", "#8BA888"))
                                    if "direct" in meta.get("scheme_name","").lower(): chips.append(("Direct Plan ✓", "#C9A84C"))
                                    if "small cap" in cat.lower(): chips.append(("High Risk", "#C47A7A"))
                                    elif "large cap" in cat.lower(): chips.append(("Lower Risk", "#8BA888"))

                                    if chips:
                                        st.markdown('<div style="margin-top:12px">' +
                                            ''.join([f'<span class="tag" style="border-color:{c}40;color:{c}">{t}</span>' for t,c in chips]) +
                                            '</div>', unsafe_allow_html=True)
                                else:
                                    st.error("Could not generate insight. Check your API key.")

                        # ── Tab 4: Details
                        with tab4:
                            col_d1, col_d2 = st.columns(2)
                            with col_d1:
                                st.markdown('<div class="sec-title" style="margin-top:8px">Fund Details</div>', unsafe_allow_html=True)
                                details = {
                                    "Fund House": meta.get("fund_house","—"),
                                    "Scheme Type": meta.get("scheme_type","—"),
                                    "Category":    meta.get("scheme_category","—"),
                                    "Scheme Code": str(meta.get("scheme_code","—")),
                                    "ISIN (Growth)": meta.get("isin_growth","—") or "—",
                                }
                                for k, v in details.items():
                                    st.markdown(f"""
                                    <div style="display:flex;justify-content:space-between;padding:8px 0;
                                                border-bottom:1px solid #1E2B27;font-size:13px">
                                      <span style="color:#4A6358">{k}</span>
                                      <span style="color:#D4CFBF;text-align:right;max-width:60%">{v}</span>
                                    </div>""", unsafe_allow_html=True)

                            with col_d2:
                                st.markdown('<div class="sec-title" style="margin-top:8px">Trailing Returns</div>', unsafe_allow_html=True)
                                for period, val in returns.items():
                                    label = "CAGR" if period in ["3Y","1Y"] else "Absolute"
                                    col_v = "#8BA888" if (val or 0) >= 0 else "#C47A7A"
                                    st.markdown(f"""
                                    <div style="display:flex;justify-content:space-between;padding:8px 0;
                                                border-bottom:1px solid #1E2B27;font-size:13px">
                                      <span style="color:#4A6358">{period} ({label})</span>
                                      <span style="font-family:'Fira Code',monospace;color:{col_v}">
                                        {"—" if val is None else f"{val:+.2f}%"}
                                      </span>
                                    </div>""", unsafe_allow_html=True)

                            # Full NAV history download
                            st.markdown('<div class="sec-title">Export NAV History</div>', unsafe_allow_html=True)
                            csv = df.to_csv(index=False).encode("utf-8")
                            st.download_button(
                                "Download NAV History (CSV)",
                                data=csv,
                                file_name=f"{meta.get('scheme_code','fund')}_nav.csv",
                                mime="text/csv",
                                width='content',
                            )

# ══════════════════════════════════════════════════════════════
# COMPARE MODE
# ══════════════════════════════════════════════════════════════
else:
    st.markdown('<div class="sec-title">Compare Two Funds</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    fund_data_list = []

    for i, (col, key) in enumerate([(col1, "cmp1"), (col2, "cmp2")]):
        with col:
            st.markdown(f'<div style="font-size:11px;color:#4A6358;text-transform:uppercase;letter-spacing:1px;margin-bottom:6px">Fund {i+1}</div>', unsafe_allow_html=True)
            q = st.text_input(f"Search fund {i+1}", placeholder="e.g. Axis Bluechip",
                               key=f"cmp_q{i}", label_visibility="collapsed")
            if q:
                results = search_funds(q)
                growth  = [r for r in results if "growth" in r["schemeName"].lower() and "direct" in r["schemeName"].lower()]
                display = growth[:6] if growth else results[:6]
                if display:
                    opts = {r["schemeName"]: r["schemeCode"] for r in display}
                    chosen = st.selectbox(f"Fund {i+1}", list(opts.keys()),
                                           key=f"cmp_sel{i}", label_visibility="collapsed")
                    fund_data_list.append((chosen, opts[chosen]))
                else:
                    fund_data_list.append(None)
            else:
                fund_data_list.append(None)

    cmp_period = st.selectbox("Compare period", ["3M","6M","1Y","3Y","5Y","All"], index=2, label_visibility="collapsed")
    compare_btn = st.button("Compare Funds ›", width='content')

    if compare_btn and len(fund_data_list) == 2 and all(fund_data_list):
        with st.spinner("Loading fund data..."):
            name1, code1 = fund_data_list[0]
            name2, code2 = fund_data_list[1]
            d1 = get_fund_data(code1)
            d2 = get_fund_data(code2)

        if d1 and d2:
            df1 = parse_nav_history(d1)
            df2 = parse_nav_history(d2)
            r1  = compute_returns(df1)
            r2  = compute_returns(df2)
            m1  = d1.get("meta", {})
            m2  = d2.get("meta", {})

            # ── Normalised comparison chart
            st.markdown('<div class="sec-title">Performance Comparison (Indexed to 100)</div>', unsafe_allow_html=True)
            fp1 = filter_period(df1, cmp_period)
            fp2 = filter_period(df2, cmp_period)
            fig = compare_chart(fp1, name1, fp2, name2)
            if fig:
                st.plotly_chart(fig, width='stretch')

            # ── Side by side metrics
            st.markdown('<div class="sec-title">Head to Head</div>', unsafe_allow_html=True)
            h1, h2 = st.columns(2)
            for col, meta, df_, rets, nm in [(h1,m1,df1,r1,name1),(h2,m2,df2,r2,name2)]:
                with col:
                    latest = df_.iloc[-1]["nav"] if not df_.empty else 0
                    st.markdown(f"""
                    <div class="fund-card">
                      <div class="fund-meta">{meta.get('fund_house','')}</div>
                      <div class="fund-name" style="font-size:15px">{nm[:60]}</div>
                      <div style="font-family:'Fira Code',monospace;font-size:24px;color:#C9A84C;margin:8px 0">₹{latest:,.2f}</div>
                      <div class="returns-strip">
                        {''.join([
                          f'<div class="ret-cell"><div class="ret-label">{k}</div>'
                          f'<div class="ret-val" style="color:{"#8BA888" if (v or 0)>=0 else "#C47A7A"}">'
                          f'{"—" if v is None else f"{v:+.1f}%"}</div></div>'
                          for k,v in rets.items()
                        ])}
                      </div>
                    </div>""", unsafe_allow_html=True)

            # ── Winner highlights
            st.markdown('<div class="sec-title">Winner by Period</div>', unsafe_allow_html=True)
            winner_html = '<div class="returns-strip">'
            for period in ["1M","3M","6M","1Y","3Y"]:
                v1 = r1.get(period)
                v2 = r2.get(period)
                if v1 is not None and v2 is not None:
                    winner = name1[:20] if v1 >= v2 else name2[:20]
                    w_col  = "#C9A84C" if v1 >= v2 else "#8BA888"
                    winner_html += (
                        f'<div class="ret-cell" style="min-width:100px;flex:1">'
                        f'<div class="ret-label">{period}</div>'
                        f'<div style="font-size:11px;color:{w_col};margin-top:4px;font-weight:600">{winner}</div>'
                        f'<div style="font-family:\'Fira Code\',monospace;font-size:12px;color:#4A6358">'
                        f'{"↑" if v1>=v2 else "↑"}{max(v1,v2):+.1f}%</div></div>'
                    )
            winner_html += '</div>'
            st.markdown(winner_html, unsafe_allow_html=True)

# ── Footer
st.markdown("""
<div class="footer">
  FundSense · Data from AMFI via mfapi.in · AI by Anthropic Claude · Not financial advice
</div>""", unsafe_allow_html=True)
