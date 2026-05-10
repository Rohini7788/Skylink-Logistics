import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ─── PAGE CONFIG ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="SkyLink · Festive Surge Report",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─── GLOBAL CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700;800&family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;1,9..40,300&display=swap');

/* ── Reset & Base ── */
*, *::before, *::after { box-sizing: border-box; }

html, body, [data-testid="stAppViewContainer"] {
    background: #08090d !important;
    color: #e8e9ef !important;
    font-family: 'DM Sans', sans-serif !important;
}

[data-testid="stAppViewContainer"] > .main {
    background: #08090d !important;
}

[data-testid="stHeader"] { background: transparent !important; }
[data-testid="stToolbar"] { display: none; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: #0d0e15 !important;
    border-right: 1px solid #1e2030 !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: #08090d; }
::-webkit-scrollbar-thumb { background: #2a2d40; border-radius: 2px; }

/* ── Typography ── */
h1, h2, h3, h4 {
    font-family: 'Syne', sans-serif !important;
    letter-spacing: -0.02em;
}

/* ── Top nav bar ── */
.skylink-nav {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 18px 32px;
    border-bottom: 1px solid #1a1c28;
    margin: -1rem -1rem 0 -1rem;
    background: rgba(8,9,13,0.95);
    backdrop-filter: blur(12px);
    position: sticky;
    top: 0;
    z-index: 999;
}

.skylink-logo {
    display: flex;
    align-items: center;
    gap: 10px;
}

.skylink-logo-icon {
    width: 36px;
    height: 36px;
    background: linear-gradient(135deg, #4f8ef7 0%, #7b5ea7 100%);
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 18px;
    box-shadow: 0 0 20px rgba(79,142,247,0.35);
}

.skylink-wordmark {
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: 20px;
    color: #ffffff;
    letter-spacing: -0.03em;
}

.skylink-wordmark span {
    color: #4f8ef7;
}

.nav-badge {
    background: #151825;
    border: 1px solid #252840;
    border-radius: 20px;
    padding: 6px 16px;
    font-size: 12px;
    color: #7b82a0;
    font-family: 'DM Sans', sans-serif;
    font-weight: 500;
    letter-spacing: 0.04em;
    text-transform: uppercase;
}

/* ── Hero section ── */
.hero-section {
    padding: 64px 32px 48px;
    position: relative;
    overflow: hidden;
}

.hero-section::before {
    content: '';
    position: absolute;
    top: -100px;
    right: -100px;
    width: 500px;
    height: 500px;
    background: radial-gradient(circle, rgba(79,142,247,0.08) 0%, transparent 70%);
    pointer-events: none;
}

.hero-section::after {
    content: '';
    position: absolute;
    bottom: -50px;
    left: 200px;
    width: 400px;
    height: 400px;
    background: radial-gradient(circle, rgba(123,94,167,0.06) 0%, transparent 70%);
    pointer-events: none;
}

.hero-label {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: rgba(79,142,247,0.08);
    border: 1px solid rgba(79,142,247,0.2);
    border-radius: 4px;
    padding: 4px 12px;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #4f8ef7;
    margin-bottom: 20px;
}

.hero-dot {
    width: 6px;
    height: 6px;
    background: #4f8ef7;
    border-radius: 50%;
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.5; transform: scale(0.8); }
}

.hero-title {
    font-family: 'Syne', sans-serif !important;
    font-size: 52px !important;
    font-weight: 800 !important;
    line-height: 1.05 !important;
    letter-spacing: -0.04em !important;
    color: #ffffff !important;
    margin: 0 0 16px !important;
    padding: 0 !important;
}

.hero-title .accent { color: #4f8ef7; }

.hero-subtitle {
    font-size: 17px;
    line-height: 1.6;
    color: #7b82a0;
    max-width: 600px;
    font-weight: 300;
}

/* ── KPI Cards ── */
.kpi-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 16px;
    padding: 0 32px 40px;
}

.kpi-card {
    background: #0d0f1a;
    border: 1px solid #1a1d2e;
    border-radius: 12px;
    padding: 28px 24px;
    position: relative;
    overflow: hidden;
    transition: border-color 0.2s, transform 0.2s;
}

.kpi-card:hover {
    border-color: #2a2d48;
    transform: translateY(-2px);
}

.kpi-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
}

.kpi-card.blue::before { background: linear-gradient(90deg, transparent, #4f8ef7, transparent); }
.kpi-card.red::before  { background: linear-gradient(90deg, transparent, #f74f6b, transparent); }
.kpi-card.amber::before{ background: linear-gradient(90deg, transparent, #f7a84f, transparent); }

.kpi-icon {
    width: 40px; height: 40px;
    border-radius: 8px;
    display: flex; align-items: center; justify-content: center;
    font-size: 18px;
    margin-bottom: 20px;
}

.kpi-card.blue .kpi-icon  { background: rgba(79,142,247,0.12); }
.kpi-card.red .kpi-icon   { background: rgba(247,79,107,0.12); }
.kpi-card.amber .kpi-icon { background: rgba(247,168,79,0.12); }

.kpi-label {
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #4a5070;
    margin-bottom: 8px;
}

.kpi-value {
    font-family: 'Syne', sans-serif;
    font-size: 38px;
    font-weight: 800;
    letter-spacing: -0.04em;
    color: #ffffff;
    line-height: 1;
    margin-bottom: 10px;
}

.kpi-delta {
    font-size: 12px;
    font-weight: 500;
    display: inline-flex;
    align-items: center;
    gap: 4px;
    padding: 3px 8px;
    border-radius: 4px;
}

.kpi-delta.neg {
    background: rgba(247,79,107,0.1);
    color: #f74f6b;
}

.kpi-delta.warn {
    background: rgba(247,168,79,0.1);
    color: #f7a84f;
}

/* ── Section headers ── */
.section-wrap {
    padding: 40px 32px 0;
}

.section-header {
    display: flex;
    align-items: flex-end;
    justify-content: space-between;
    margin-bottom: 8px;
    padding-bottom: 20px;
    border-bottom: 1px solid #13151f;
}

.section-number {
    font-family: 'Syne', sans-serif;
    font-size: 11px;
    font-weight: 700;
    color: #2a2d48;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    margin-bottom: 6px;
}

.section-title {
    font-family: 'Syne', sans-serif !important;
    font-size: 28px !important;
    font-weight: 800 !important;
    color: #ffffff !important;
    letter-spacing: -0.03em !important;
    margin: 0 !important;
    padding: 0 !important;
    line-height: 1.1 !important;
}

.section-desc {
    font-size: 14px;
    color: #555874;
    max-width: 560px;
    line-height: 1.6;
    margin-top: 12px;
}

/* ── Chart containers ── */
.chart-card {
    background: #0d0f1a;
    border: 1px solid #1a1d2e;
    border-radius: 12px;
    padding: 4px;
    margin-top: 20px;
}

/* ── Insight callouts ── */
.insight-box {
    display: flex;
    gap: 14px;
    align-items: flex-start;
    background: #0d0f1a;
    border: 1px solid #1d2030;
    border-left: 3px solid #f7a84f;
    border-radius: 8px;
    padding: 18px 20px;
    margin: 20px 0 8px;
    font-size: 14px;
    color: #c5c8da;
    line-height: 1.6;
}

.insight-box.blue { border-left-color: #4f8ef7; }
.insight-box.green { border-left-color: #4ff7a8; }

.insight-icon {
    font-size: 18px;
    flex-shrink: 0;
    margin-top: 1px;
}

/* ── Recommendations ── */
.rec-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 16px;
    margin-top: 24px;
}

.rec-card {
    background: #0d0f1a;
    border: 1px solid #1a1d2e;
    border-radius: 12px;
    padding: 28px 24px;
}

.rec-tag {
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    padding: 4px 10px;
    border-radius: 4px;
    display: inline-block;
    margin-bottom: 16px;
}

.rec-tag.quick  { background: rgba(79,247,168,0.1); color: #4ff7a8; }
.rec-tag.struct { background: rgba(79,142,247,0.1); color: #4f8ef7; }
.rec-tag.long   { background: rgba(123,94,167,0.1); color: #a07ed4; }

.rec-title {
    font-family: 'Syne', sans-serif;
    font-size: 16px;
    font-weight: 700;
    color: #ffffff;
    margin-bottom: 14px;
}

.rec-item {
    display: flex;
    gap: 10px;
    font-size: 13px;
    color: #7b82a0;
    line-height: 1.5;
    margin-bottom: 10px;
    align-items: flex-start;
}

.rec-bullet {
    width: 5px;
    height: 5px;
    background: #2a2d48;
    border-radius: 50%;
    margin-top: 7px;
    flex-shrink: 0;
}

/* ── Success banner ── */
.success-banner {
    margin: 32px 32px 0;
    background: linear-gradient(135deg, rgba(79,247,168,0.06) 0%, rgba(79,142,247,0.06) 100%);
    border: 1px solid rgba(79,247,168,0.15);
    border-radius: 12px;
    padding: 24px 28px;
    display: flex;
    align-items: center;
    gap: 16px;
}

.success-icon { font-size: 24px; }

.success-text {
    font-size: 14px;
    color: #a0f7c8;
    line-height: 1.6;
}

.success-text strong { color: #4ff7a8; }

/* ── Divider ── */
.styled-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, #1a1d2e 20%, #1a1d2e 80%, transparent);
    margin: 48px 32px;
}

/* ── Footer ── */
.footer {
    padding: 32px;
    border-top: 1px solid #13151f;
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-top: 48px;
}

.footer-logo {
    font-family: 'Syne', sans-serif;
    font-size: 13px;
    font-weight: 700;
    color: #2a2d48;
    letter-spacing: -0.02em;
}

.footer-note {
    font-size: 12px;
    color: #2a2d48;
}

/* ── Streamlit element overrides ── */
[data-testid="stVerticalBlock"] > [data-testid="stVerticalBlockBorderWrapper"] {
    background: transparent !important;
    border: none !important;
}

div[data-testid="stHorizontalBlock"] { gap: 16px; }

.stPlotlyChart {
    border-radius: 8px;
    overflow: hidden;
}

/* Remove default streamlit padding */
.block-container {
    padding: 0 !important;
    max-width: 100% !important;
}

section[data-testid="stSidebar"] { display: none; }
</style>
""", unsafe_allow_html=True)


# ─── DATA LOADING ───────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    orders = pd.read_csv('orders.csv').dropna(how='all')
    nps = pd.read_csv('nps.csv').dropna(how='all')
    hubs = pd.read_csv('hub_performance.csv').dropna(how='all')
    complaints = pd.read_csv('complaints.csv').dropna(how='all')
    customers = pd.read_csv('customers.csv').dropna(how='all')

    orders['promised_date'] = pd.to_datetime(orders['promised_date'])
    orders['delivery_date'] = pd.to_datetime(orders['delivery_date'])
    orders['order_date'] = pd.to_datetime(orders['order_date'])
    orders['sla_breached'] = orders['delivery_date'] > orders['promised_date']

    return orders, nps, hubs, complaints, customers

orders, nps, hubs, complaints, customers = load_data()

# ─── COMPUTED METRICS ───────────────────────────────────────────────────────────
promoters   = (nps['score'] >= 9).sum()
detractors  = (nps['score'] <= 6).sum()
nps_score   = ((promoters - detractors) / len(nps)) * 100
repeat_cust = customers[customers['segment'].isin(['Repeat', 'High Value'])].shape[0]
repeat_rate = (repeat_cust / len(customers)) * 100
overall_breach = orders['sla_breached'].mean() * 100


# ─── PLOTLY THEME ───────────────────────────────────────────────────────────────
PLOT_BG    = "#0d0f1a"
PAPER_BG   = "#0d0f1a"
GRID_COLOR = "#1a1d2e"
TEXT_COLOR = "#7b82a0"
FONT_FAM   = "DM Sans"

def styled_layout(fig, title=""):
    fig.update_layout(
        title=dict(text=title, font=dict(family="Syne", size=14, color="#c5c8da"), x=0, xanchor='left', pad=dict(l=16, t=16)),
        paper_bgcolor=PAPER_BG,
        plot_bgcolor=PLOT_BG,
        font=dict(family=FONT_FAM, color=TEXT_COLOR, size=12),
        margin=dict(l=20, r=20, t=50, b=20),
        legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor="rgba(0,0,0,0)", font=dict(color=TEXT_COLOR)),
        xaxis=dict(gridcolor=GRID_COLOR, linecolor=GRID_COLOR, tickfont=dict(color=TEXT_COLOR)),
        yaxis=dict(gridcolor=GRID_COLOR, linecolor=GRID_COLOR, tickfont=dict(color=TEXT_COLOR)),
        hoverlabel=dict(bgcolor="#151825", bordercolor="#252840", font=dict(color="#ffffff")),
    )
    return fig


# ══════════════════════════════════════════════════════════════════════════════
# NAV BAR
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="skylink-nav">
  <div class="skylink-logo">
    <div class="skylink-logo-icon">🔗</div>
    <div class="skylink-wordmark">Sky<span>Link</span></div>
  </div>
  <div class="nav-badge">Q4 · Post-Mortem Report</div>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# HERO
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="hero-section">
  <div class="hero-label">
    <div class="hero-dot"></div>
    Oct – Dec · Festive Surge Analysis
  </div>
  <h1 class="hero-title">The Festive Surge:<br>Scale vs. <span class="accent">Service</span></h1>
  <p class="hero-subtitle">Order volume grew 40% — a record. But customer satisfaction hit an all-time low. This report dissects where the logistics chain fractured under pressure.</p>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# KPI CARDS
# ══════════════════════════════════════════════════════════════════════════════
st.markdown(f"""
<div class="kpi-grid">
  <div class="kpi-card blue">
    <div class="kpi-icon">📊</div>
    <div class="kpi-label">Net Promoter Score</div>
    <div class="kpi-value">{nps_score:.1f}</div>
    <div class="kpi-delta neg">↓ −15 pts vs Q3</div>
  </div>
  <div class="kpi-card amber">
    <div class="kpi-icon">🔄</div>
    <div class="kpi-label">Repeat Usage Rate</div>
    <div class="kpi-value">{repeat_rate:.1f}%</div>
    <div class="kpi-delta warn">⚠ −5% churn risk</div>
  </div>
  <div class="kpi-card red">
    <div class="kpi-icon">⏱</div>
    <div class="kpi-label">SLA Breach Rate</div>
    <div class="kpi-value">{overall_breach:.1f}%</div>
    <div class="kpi-delta neg">↑ +22% delay spike</div>
  </div>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# CHAPTER 2 – FRICTION POINTS
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="styled-divider"></div>', unsafe_allow_html=True)

st.markdown("""
<div class="section-wrap">
  <div class="section-header">
    <div>
      <div class="section-number">Chapter 02</div>
      <h2 class="section-title">Identifying the Friction</h2>
    </div>
  </div>
  <p class="section-desc">The decline isn't uniform. Tier-2 cities — Nagpur and Indore — are the primary drivers of dissatisfaction, with specific courier partners amplifying the problem.</p>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    city_perf = (
        orders.groupby('city')['sla_breached']
        .mean()
        .reset_index()
        .sort_values('sla_breached', ascending=True)
    )
    fig_city = go.Figure(go.Bar(
        x=city_perf['sla_breached'] * 100,
        y=city_perf['city'],
        orientation='h',
        marker=dict(
            color=city_perf['sla_breached'],
            colorscale=[[0, "#1e3a5f"], [0.5, "#4f8ef7"], [1, "#f74f6b"]],
            line=dict(width=0),
        ),
        text=[f"{v*100:.1f}%" for v in city_perf['sla_breached']],
        textposition='outside',
        textfont=dict(color="#7b82a0", size=11),
        hovertemplate="<b>%{y}</b><br>Breach Rate: %{x:.1f}%<extra></extra>",
    ))
    fig_city = styled_layout(fig_city, "SLA Breach Rate by City")
    fig_city.update_xaxes(ticksuffix="%")

    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.plotly_chart(fig_city, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    courier_perf = orders.groupby('courier_partner')['sla_breached'].mean().reset_index()
    colors = ["#4f8ef7", "#f74f6b", "#f7a84f", "#4ff7a8", "#a07ed4"]
    fig_courier = go.Figure(go.Bar(
        x=courier_perf['courier_partner'],
        y=courier_perf['sla_breached'] * 100,
        marker=dict(color=colors[:len(courier_perf)], line=dict(width=0)),
        text=[f"{v*100:.1f}%" for v in courier_perf['sla_breached']],
        textposition='outside',
        textfont=dict(color="#7b82a0", size=11),
        hovertemplate="<b>%{x}</b><br>Breach Rate: %{y:.1f}%<extra></extra>",
    ))
    fig_courier = styled_layout(fig_courier, "Courier Partner Reliability")
    fig_courier.update_yaxes(ticksuffix="%")

    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.plotly_chart(fig_courier, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("""
<div class="section-wrap">
  <div class="insight-box">
    <div class="insight-icon">⚡</div>
    <div><strong style="color:#f7a84f">Key Finding:</strong> QuickShip is responsible for the highest volume of breaches in Indore, indicating a failure in their local hub handoff process.</div>
  </div>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# CHAPTER 3 – COMPLAINT FUNNEL
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="styled-divider"></div>', unsafe_allow_html=True)

st.markdown("""
<div class="section-wrap">
  <div class="section-header">
    <div>
      <div class="section-number">Chapter 03</div>
      <h2 class="section-title">The Cost of a Late Package</h2>
    </div>
  </div>
  <p class="section-desc">A delayed delivery triggers a predictable spiral: complaint → detractor → churn. Understanding the complaint taxonomy lets us intervene earlier.</p>
</div>
""", unsafe_allow_html=True)

comp_dist = complaints['issue_type'].value_counts().reset_index()

fig_pie = go.Figure(go.Pie(
    labels=comp_dist['issue_type'],
    values=comp_dist['count'],
    hole=0.6,
    marker=dict(
        colors=["#4f8ef7", "#f74f6b", "#f7a84f", "#4ff7a8", "#a07ed4"],
        line=dict(color=PLOT_BG, width=3),
    ),
    textinfo='label+percent',
    textfont=dict(family="DM Sans", color="#c5c8da", size=12),
    hovertemplate="<b>%{label}</b><br>Count: %{value}<br>Share: %{percent}<extra></extra>",
))

fig_pie.add_annotation(
    text=f"<b style='font-size:22px'>{comp_dist['count'].sum()}</b><br><span style='font-size:11px'>Total</span>",
    x=0.5, y=0.5, showarrow=False,
    font=dict(family="Syne", color="#ffffff", size=14),
)

fig_pie = styled_layout(fig_pie, "Primary Complaint Drivers")
fig_pie.update_layout(height=400, showlegend=True,
    legend=dict(orientation="v", x=0.75, y=0.5))

st.markdown('<div class="section-wrap"><div class="chart-card">', unsafe_allow_html=True)
st.plotly_chart(fig_pie, use_container_width=True)
st.markdown('</div></div>', unsafe_allow_html=True)

st.markdown("""
<div class="section-wrap">
  <div class="insight-box blue">
    <div class="insight-icon">🔍</div>
    <div><strong style="color:#4f8ef7">Nagpur Anomaly:</strong> 32% of complaints in Nagpur are flagged as 'Fake Delivery Attempts' — a behaviour that destroys customer trust immediately and is unlike any other city in our network.</div>
  </div>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# FINAL CHAPTER – RECOMMENDATIONS
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="styled-divider"></div>', unsafe_allow_html=True)

st.markdown("""
<div class="section-wrap">
  <div class="section-header">
    <div>
      <div class="section-number">Chapter 04</div>
      <h2 class="section-title">The Road to Recovery</h2>
    </div>
  </div>
  <p class="section-desc">To improve NPS without increasing costs, we optimize existing partnerships and fix hub-level behaviours. Three horizons of action.</p>

  <div class="rec-grid">
    <div class="rec-card">
      <div class="rec-tag quick">⚡ Quick Wins</div>
      <div class="rec-title">Immediate Actions</div>
      <div class="rec-item"><div class="rec-bullet"></div><div>Migrate all Nagpur volume from <strong style="color:#f7a84f">QuickShip</strong> to <strong style="color:#4ff7a8">FastEx</strong> immediately.</div></div>
      <div class="rec-item"><div class="rec-bullet"></div><div>Implement auto-SMS alerts when order status updates to 'Out for Delivery'.</div></div>
    </div>
    <div class="rec-card">
      <div class="rec-tag struct">🏗 Structural</div>
      <div class="rec-title">Systemic Fixes</div>
      <div class="rec-item"><div class="rec-bullet"></div><div>Audit the Nagpur hub for 'Fake Delivery' reporting behaviour — escalate if systemic.</div></div>
      <div class="rec-item"><div class="rec-bullet"></div><div>Tiered SLA penalties: couriers with >20% breach rate face a 10% payout reduction during festive windows.</div></div>
    </div>
    <div class="rec-card">
      <div class="rec-tag long">📈 Long-term</div>
      <div class="rec-title">KPI Framework</div>
      <div class="rec-item"><div class="rec-bullet"></div><div><strong style="color:#a07ed4">First-Attempt Delivery Rate:</strong> Focus metric for reducing RTO and courier penalties.</div></div>
      <div class="rec-item"><div class="rec-bullet"></div><div><strong style="color:#a07ed4">NPS Recovery Rate:</strong> Track if a resolved complaint leads to a repeat purchase within 30 days.</div></div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Success Banner ──
st.markdown("""
<div class="success-banner">
  <div class="success-icon">✅</div>
  <div class="success-text">
    By reallocating volume to high-performing couriers, we can reduce complaints by an estimated <strong>18%</strong> with <strong>zero additional shipping cost</strong> — making this the highest-leverage intervention available this quarter.
  </div>
</div>
""", unsafe_allow_html=True)

# ── Footer ──
st.markdown("""
<div class="footer">
  <div class="footer-logo">SkyLink Logistics Intelligence</div>
  <div class="footer-note">Q4 Festive Surge · Post-Mortem Report · Confidential</div>
</div>
""", unsafe_allow_html=True)
