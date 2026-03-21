"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  PALANTIR TECHNOLOGIES (PLTR) — EQUITY RESEARCH ANALYTICS DASHBOARD       ║
║  MBAN5570 Accounting & Financial Analytics | Sobey School of Business      ║
║  Dr. Mohammad M. Rahaman                                                   ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from scipy import stats
from pltr_data import (
    COMPANY_INFO, MARKET_DATA, INCOME_STATEMENT, BALANCE_SHEET, CASH_FLOW,
    REVENUE_SEGMENTS, KEY_RATIOS, DUPONT, PEER_COMPARISON, KEY_EVENTS,
    ANALYST_DATA, GUIDANCE, compute_ratios
)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE CONFIG & CUSTOM CSS
# ══════════════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="PLTR Equity Research | MBAN5570",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Premium dark theme CSS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

:root {
    --bg-primary: #0a0e17;
    --bg-card: #111827;
    --bg-card-hover: #1a2332;
    --accent: #3b82f6;
    --accent-green: #10b981;
    --accent-red: #ef4444;
    --accent-amber: #f59e0b;
    --text-primary: #f1f5f9;
    --text-secondary: #94a3b8;
    --border: #1e293b;
}

.stApp { background-color: var(--bg-primary); font-family: 'Inter', sans-serif; }

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f172a 0%, #1e1b4b 100%);
    border-right: 1px solid var(--border);
}
section[data-testid="stSidebar"] .stMarkdown p,
section[data-testid="stSidebar"] .stMarkdown li,
section[data-testid="stSidebar"] label { color: var(--text-secondary) !important; }

/* Metric cards */
div[data-testid="stMetric"] {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 16px 20px;
    transition: border-color 0.2s;
}
div[data-testid="stMetric"]:hover { border-color: var(--accent); }
div[data-testid="stMetric"] label { color: var(--text-secondary) !important; font-size: 0.82rem !important; }
div[data-testid="stMetric"] [data-testid="stMetricValue"] { color: var(--text-primary) !important; font-weight: 600 !important; }

/* Headers */
h1, h2, h3 { color: var(--text-primary) !important; font-family: 'Inter', sans-serif !important; }
h1 { font-weight: 700 !important; letter-spacing: -0.02em; }
h2 { font-weight: 600 !important; border-bottom: 2px solid var(--accent); padding-bottom: 8px; }
h3 { font-weight: 500 !important; color: var(--text-secondary) !important; }

/* Tabs */
.stTabs [data-baseweb="tab-list"] { gap: 4px; background: var(--bg-card); border-radius: 12px; padding: 4px; }
.stTabs [data-baseweb="tab"] {
    border-radius: 8px; padding: 8px 20px; color: var(--text-secondary);
    font-weight: 500; transition: all 0.2s;
}
.stTabs [aria-selected="true"] { background: var(--accent) !important; color: white !important; }

/* Tables */
.stDataFrame { border-radius: 12px; overflow: hidden; border: 1px solid var(--border); }

/* Expander */
.streamlit-expanderHeader { background: var(--bg-card) !important; border-radius: 8px; color: var(--text-primary) !important; }

/* Custom KPI card */
.kpi-card {
    background: linear-gradient(135deg, var(--bg-card) 0%, var(--bg-card-hover) 100%);
    border: 1px solid var(--border); border-radius: 16px; padding: 24px;
    text-align: center; transition: transform 0.2s, border-color 0.2s;
}
.kpi-card:hover { transform: translateY(-2px); border-color: var(--accent); }
.kpi-label { color: var(--text-secondary); font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 8px; }
.kpi-value { color: var(--text-primary); font-size: 1.8rem; font-weight: 700; }
.kpi-delta { font-size: 0.85rem; font-weight: 500; margin-top: 4px; }
.kpi-delta.positive { color: var(--accent-green); }
.kpi-delta.negative { color: var(--accent-red); }

/* Section divider */
.section-divider { height: 1px; background: linear-gradient(90deg, transparent, var(--border), transparent); margin: 2rem 0; }

/* Scrollbar */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--bg-primary); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# PLOTLY THEME
# ══════════════════════════════════════════════════════════════════════════════
PLOTLY_LAYOUT = dict(
    template="plotly_dark",
    paper_bgcolor="rgba(17,24,39,0)",
    plot_bgcolor="rgba(17,24,39,0.5)",
    font=dict(family="Inter", color="#f1f5f9", size=12),
    margin=dict(l=40, r=20, t=50, b=40),
    legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(size=11)),
    xaxis=dict(gridcolor="rgba(30,41,59,0.5)", zerolinecolor="rgba(30,41,59,0.5)"),
    yaxis=dict(gridcolor="rgba(30,41,59,0.5)", zerolinecolor="rgba(30,41,59,0.5)"),
)
COLORS = ["#3b82f6", "#10b981", "#f59e0b", "#ef4444", "#8b5cf6", "#ec4899", "#06b6d4"]


def apply_layout(fig, title="", height=450):
    fig.update_layout(**PLOTLY_LAYOUT, title=dict(text=title, font=dict(size=16, weight=600)), height=height)
    return fig


# ══════════════════════════════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ══════════════════════════════════════════════════════════════════════════════
def fmt_b(val):
    """Format to billions."""
    if val is None: return "N/A"
    return f"${val/1e3:.1f}B" if abs(val) >= 1000 else f"${val:.0f}M"

def fmt_pct(val):
    if val is None: return "N/A"
    return f"{val:.1f}%"

def fmt_price(val):
    if val is None: return "N/A"
    return f"${val:,.2f}"

def kpi_html(label, value, delta=None, delta_positive=True):
    delta_cls = "positive" if delta_positive else "negative"
    delta_html = f'<div class="kpi-delta {delta_cls}">{delta}</div>' if delta else ""
    return f"""<div class="kpi-card">
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
        {delta_html}
    </div>"""

def divider():
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR NAVIGATION
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("## 🏛️ PLTR Research")
    st.markdown(f"**{COMPANY_INFO['name']}**")
    st.markdown(f"NASDAQ: PLTR | {fmt_price(MARKET_DATA['current_price'])}")
    st.markdown("---")

    page = st.radio(
        "Navigate",
        [
            "📊 Executive Summary",
            "🏢 Business Overview",
            "📈 Financial Statements",
            "🔬 Financial Analytics",
            "💰 Valuation Models",
            "🎯 Risk & Monte Carlo",
            "📉 Peer Comparison",
            "🤖 AI-Assisted Analysis",
            "📋 Critical Evaluation",
        ],
        label_visibility="collapsed",
    )

    st.markdown("---")
    st.markdown("##### MBAN5570 Project")
    st.caption("Accounting & Financial Analytics")
    st.caption("Sobey School of Business")
    st.caption("Dr. Mohammad M. Rahaman")


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 1: EXECUTIVE SUMMARY
# ══════════════════════════════════════════════════════════════════════════════
if page == "📊 Executive Summary":
    st.markdown("# Palantir Technologies — Equity Research")
    st.markdown(f"*As of March 20, 2026 | Market Cap: ${MARKET_DATA['market_cap_B']:.0f}B*")
    divider()

    # Top KPI row
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    c1.metric("Share Price", fmt_price(MARKET_DATA["current_price"]), "↑ from $9.50 IPO")
    c2.metric("Market Cap", f"${MARKET_DATA['market_cap_B']:.0f}B")
    c3.metric("FY2025 Revenue", fmt_b(INCOME_STATEMENT.loc[2025, "Total Revenue"]), "+56% YoY")
    c4.metric("Adj Op. Margin", "50.6%", "+17.2pp YoY")
    c5.metric("FCF (FY2025)", fmt_b(CASH_FLOW.loc[2025, "Free Cash Flow"]), "+99% YoY")
    c6.metric("FY2026 Guide", "$7.19B", "+61% YoY")

    divider()

    # Revenue & Profitability chart
    col1, col2 = st.columns(2)

    with col1:
        ist = INCOME_STATEMENT
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(go.Bar(x=ist.index, y=ist["Total Revenue"], name="Revenue ($M)",
                             marker_color=COLORS[0], opacity=0.85), secondary_y=False)
        fig.add_trace(go.Scatter(x=ist.index, y=ist["Adj Operating Margin%"], name="Adj Op Margin %",
                                 line=dict(color=COLORS[1], width=3), mode="lines+markers"), secondary_y=True)
        fig.update_yaxes(title_text="Revenue ($M)", secondary_y=False)
        fig.update_yaxes(title_text="Adj Op Margin (%)", secondary_y=True)
        apply_layout(fig, "Revenue & Adj Operating Margin Trajectory")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        cf = CASH_FLOW
        fig = go.Figure()
        fig.add_trace(go.Bar(x=cf.index, y=cf["Operating Cash Flow"], name="Operating CF", marker_color=COLORS[0]))
        fig.add_trace(go.Bar(x=cf.index, y=cf["Free Cash Flow"], name="Free Cash Flow", marker_color=COLORS[1]))
        fig.add_trace(go.Scatter(x=cf.index, y=cf["FCF Margin %"], name="FCF Margin %",
                                 line=dict(color=COLORS[2], width=3), mode="lines+markers", yaxis="y2"))
        fig.update_layout(
            yaxis2=dict(overlaying="y", side="right", title="FCF Margin %",
                        gridcolor="rgba(30,41,59,0.3)"),
            barmode="group"
        )
        apply_layout(fig, "Cash Flow Generation")
        st.plotly_chart(fig, use_container_width=True)

    # Investment thesis
    divider()
    st.markdown("## Investment Thesis")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Bull Case")
        st.markdown("""
        - **AIP is the growth engine**: US Commercial revenue grew 137% YoY in Q4 2025, driven by AIP boot camps converting to production contracts
        - **Rule of 40+ dominance**: Revenue growth (56%) + FCF margin (51%) = **107** — exceptional for any software company at this scale
        - **Government durability**: 20+ year relationships provide stable, high-margin base revenue with expansion potential via AIP
        - **FY2026 guidance of 61% growth** signals continued acceleration, not deceleration — rare at $4.5B revenue scale
        - **Net cash position** of ~$7.2B with zero debt provides strategic optionality
        """)

    with col2:
        st.markdown("### Bear Case / Key Risks")
        st.markdown("""
        - **Extreme valuation**: Trading at ~81x EV/Revenue vs peer median of ~12x — prices in years of perfect execution
        - **SBC dilution**: $700M in FY2025 stock-based compensation (~15.6% of revenue) dilutes existing shareholders
        - **Customer concentration**: Government contracts can be lumpy; policy shifts could impact revenue
        - **Competition intensifying**: Microsoft, AWS, Google all investing heavily in enterprise AI platforms
        - **Insider selling**: Consistent insider sales, including CEO Alex Karp's 10b5-1 plan
        """)

    # Analyst consensus
    divider()
    st.markdown("## Analyst Consensus & Price Targets")
    ac = ANALYST_DATA
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Consensus", ac["consensus"])
    c2.metric("Mean Target", fmt_price(ac["target_mean"]))
    c3.metric("Range", f"${ac['target_low']:.0f} — ${ac['target_high']:.0f}")
    c4.metric("# of Analysts", ac["num_analysts"])

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=["Buy", "Hold", "Sell"],
        y=[ac["buy"], ac["hold"], ac["sell"]],
        marker_color=[COLORS[1], COLORS[2], COLORS[3]],
        text=[ac["buy"], ac["hold"], ac["sell"]],
        textposition="outside"
    ))
    apply_layout(fig, "Analyst Recommendation Distribution", height=300)
    st.plotly_chart(fig, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 2: BUSINESS OVERVIEW
# ══════════════════════════════════════════════════════════════════════════════
elif page == "🏢 Business Overview":
    st.markdown("# Business Model & Competitive Position")
    divider()

    st.markdown(f"> {COMPANY_INFO['description']}")

    # Products
    st.markdown("## Platform Ecosystem")
    c1, c2, c3 = st.columns(3)
    for col, (prod, desc) in zip([c1, c2, c3], COMPANY_INFO["products"].items()):
        with col:
            st.markdown(f"### {prod}")
            st.markdown(desc)

    divider()

    # Revenue segments
    st.markdown("## Revenue Segmentation")
    seg = REVENUE_SEGMENTS

    col1, col2 = st.columns(2)
    with col1:
        fig = go.Figure()
        fig.add_trace(go.Bar(x=seg.index, y=seg["Government Revenue"], name="Government", marker_color=COLORS[0]))
        fig.add_trace(go.Bar(x=seg.index, y=seg["Commercial Revenue"], name="Commercial", marker_color=COLORS[1]))
        fig.update_layout(barmode="stack")
        apply_layout(fig, "Revenue by Segment ($M)")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = go.Figure()
        fig.add_trace(go.Bar(x=seg.index, y=seg["US Revenue"], name="United States", marker_color=COLORS[0]))
        fig.add_trace(go.Bar(x=seg.index, y=seg["International Revenue"], name="International", marker_color=COLORS[4]))
        fig.update_layout(barmode="stack")
        apply_layout(fig, "Revenue by Geography ($M)")
        st.plotly_chart(fig, use_container_width=True)

    # 4-quadrant breakdown
    st.markdown("### Detailed Revenue Breakdown (FY2025)")
    fig = go.Figure(data=[go.Pie(
        labels=["US Government", "US Commercial", "Int'l Government", "Int'l Commercial"],
        values=[seg.loc[2025, "US Government"], seg.loc[2025, "US Commercial"],
                seg.loc[2025, "Intl Government"], seg.loc[2025, "Intl Commercial"]],
        hole=0.5, marker_colors=COLORS[:4],
        textinfo="label+percent+value", texttemplate="%{label}<br>$%{value}M<br>(%{percent})",
    )])
    apply_layout(fig, "FY2025 Revenue Mix", height=400)
    st.plotly_chart(fig, use_container_width=True)

    # US Commercial hypergrowth
    divider()
    st.markdown("## US Commercial — Hypergrowth Engine")
    us_comm = seg["US Commercial"]
    growth = us_comm.pct_change() * 100
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Bar(x=us_comm.index, y=us_comm.values, name="US Comm Revenue ($M)",
                         marker_color=COLORS[1]), secondary_y=False)
    fig.add_trace(go.Scatter(x=growth.index, y=growth.values, name="YoY Growth %",
                             line=dict(color=COLORS[2], width=3), mode="lines+markers"), secondary_y=True)
    fig.update_yaxes(title_text="Revenue ($M)", secondary_y=False)
    fig.update_yaxes(title_text="YoY Growth (%)", secondary_y=True)
    apply_layout(fig, "US Commercial Revenue — AIP-Driven Acceleration")
    st.plotly_chart(fig, use_container_width=True)

    # Competitive moats
    divider()
    st.markdown("## Sustainable Competitive Advantage")
    for moat in COMPANY_INFO["competitive_moats"]:
        st.markdown(f"- {moat}")


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 3: FINANCIAL STATEMENTS
# ══════════════════════════════════════════════════════════════════════════════
elif page == "📈 Financial Statements":
    st.markdown("# Financial Statement Analysis")
    divider()

    tab1, tab2, tab3 = st.tabs(["Income Statement", "Balance Sheet", "Cash Flow Statement"])

    with tab1:
        st.markdown("### Income Statement ($M)")
        display_cols = ["Total Revenue", "Cost of Revenue", "Gross Profit", "R&D Expense",
                        "SGA Expense", "SBC Expense", "Operating Income", "Net Income",
                        "EBITDA", "Diluted EPS"]
        st.dataframe(INCOME_STATEMENT[display_cols].style.format("{:,.0f}", subset=[c for c in display_cols if c != "Diluted EPS"])
                     .format("{:.2f}", subset=["Diluted EPS"])
                     .background_gradient(cmap="RdYlGn", axis=1),
                     use_container_width=True)

        # Margin evolution
        ist = INCOME_STATEMENT
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=ist.index, y=(ist["Gross Profit"]/ist["Total Revenue"]*100),
                                 name="Gross Margin", line=dict(color=COLORS[0], width=2.5), mode="lines+markers"))
        fig.add_trace(go.Scatter(x=ist.index, y=(ist["Operating Income"]/ist["Total Revenue"]*100),
                                 name="GAAP Op Margin", line=dict(color=COLORS[1], width=2.5), mode="lines+markers"))
        fig.add_trace(go.Scatter(x=ist.index, y=(ist["Net Income"]/ist["Total Revenue"]*100),
                                 name="Net Margin", line=dict(color=COLORS[2], width=2.5), mode="lines+markers"))
        fig.add_trace(go.Scatter(x=ist.index, y=ist["Adj Operating Margin%"],
                                 name="Adj Op Margin", line=dict(color=COLORS[4], width=3, dash="dash"), mode="lines+markers"))
        apply_layout(fig, "Margin Evolution (2020–2025)")
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        st.markdown("### Balance Sheet ($M)")
        st.dataframe(BALANCE_SHEET.style.format("{:,.0f}").background_gradient(cmap="Blues", axis=1),
                     use_container_width=True)

        bs = BALANCE_SHEET
        fig = go.Figure()
        fig.add_trace(go.Bar(x=bs.index, y=bs["Cash & Equivalents"] + bs["Short-Term Investments"],
                             name="Cash + ST Investments", marker_color=COLORS[1]))
        fig.add_trace(go.Bar(x=bs.index, y=bs["Total Stockholders Equity"], name="Equity", marker_color=COLORS[0]))
        fig.add_trace(go.Bar(x=bs.index, y=bs["Total Liabilities"], name="Liabilities", marker_color=COLORS[3]))
        fig.update_layout(barmode="group")
        apply_layout(fig, "Balance Sheet Composition ($M)")
        st.plotly_chart(fig, use_container_width=True)

    with tab3:
        st.markdown("### Cash Flow Statement ($M)")
        cf_cols = ["Operating Cash Flow", "Capital Expenditure", "Free Cash Flow",
                   "Purchases of Investments", "SBC", "FCF Margin %"]
        st.dataframe(CASH_FLOW[cf_cols].style.format("{:,.0f}", subset=[c for c in cf_cols if c != "FCF Margin %"])
                     .format("{:.1f}", subset=["FCF Margin %"])
                     .background_gradient(cmap="RdYlGn", axis=1),
                     use_container_width=True)

        # FCF waterfall
        cf25 = CASH_FLOW.loc[2025]
        fig = go.Figure(go.Waterfall(
            x=["Net Income", "+D&A", "+SBC", "+WC Changes", "=Operating CF", "-CapEx", "=Free Cash Flow"],
            y=[cf25["Net Income"], cf25["D&A"], cf25["SBC"], cf25["Changes in Working Capital"],
               0, cf25["Capital Expenditure"], 0],
            measure=["relative", "relative", "relative", "relative", "total", "relative", "total"],
            connector={"line": {"color": "rgba(59,130,246,0.4)"}},
            increasing={"marker": {"color": COLORS[1]}},
            decreasing={"marker": {"color": COLORS[3]}},
            totals={"marker": {"color": COLORS[0]}},
            text=[f"${v:,.0f}M" for v in [cf25["Net Income"], cf25["D&A"], cf25["SBC"],
                  cf25["Changes in Working Capital"], cf25["Operating Cash Flow"],
                  cf25["Capital Expenditure"], cf25["Free Cash Flow"]]],
            textposition="outside"
        ))
        apply_layout(fig, "FY2025 Free Cash Flow Bridge ($M)", height=420)
        st.plotly_chart(fig, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 4: FINANCIAL ANALYTICS (Horizontal, Vertical, Ratio, DuPont, Trend)
# ══════════════════════════════════════════════════════════════════════════════
elif page == "🔬 Financial Analytics":
    st.markdown("# Financial Statement Analytics")
    st.markdown("*Per MBAN5570 methodology: Horizontal, Vertical, Ratio, Trend, and DuPont Analysis*")
    divider()

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Horizontal Analysis", "Vertical Analysis", "Ratio Analysis", "DuPont Analysis", "Trend Analysis"
    ])

    with tab1:
        st.markdown("### Horizontal Analysis — Year-over-Year % Change")
        st.markdown("Measures the change in each line item relative to the prior year.")
        ist = INCOME_STATEMENT[["Total Revenue", "Gross Profit", "Operating Income", "Net Income", "EBITDA"]]
        horiz = ist.pct_change() * 100
        horiz = horiz.dropna(how="all")
        st.dataframe(horiz.style.format("{:+.1f}%").background_gradient(cmap="RdYlGn", axis=1, vmin=-50, vmax=100),
                     use_container_width=True)

        fig = go.Figure()
        for i, col in enumerate(["Total Revenue", "Gross Profit", "Net Income"]):
            fig.add_trace(go.Bar(x=horiz.index, y=horiz[col], name=col, marker_color=COLORS[i]))
        fig.update_layout(barmode="group")
        apply_layout(fig, "YoY Growth Rates (%)")
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        st.markdown("### Vertical Analysis — Common-Size Income Statement")
        st.markdown("Each item as a percentage of Total Revenue.")
        ist = INCOME_STATEMENT
        rev = ist["Total Revenue"]
        vert_cols = ["Cost of Revenue", "Gross Profit", "R&D Expense", "SGA Expense",
                     "SBC Expense", "Operating Income", "Net Income"]
        vert = ist[vert_cols].div(rev, axis=0) * 100
        st.dataframe(vert.style.format("{:.1f}%").background_gradient(cmap="RdYlGn", axis=1),
                     use_container_width=True)

        fig = go.Figure()
        for i, col in enumerate(["Gross Profit", "Operating Income", "Net Income", "SBC Expense"]):
            fig.add_trace(go.Scatter(x=vert.index, y=vert[col], name=f"{col} % of Rev",
                                     line=dict(color=COLORS[i], width=2.5), mode="lines+markers"))
        apply_layout(fig, "Common-Size Trends (% of Revenue)")
        st.plotly_chart(fig, use_container_width=True)

    with tab3:
        st.markdown("### Comprehensive Ratio Analysis")
        st.markdown("*Four quadrants: Profitability & Return, Liquidity & Solvency, Efficiency, Cash Flow*")
        ratios = KEY_RATIOS
        st.dataframe(ratios.style.format("{:.1f}").background_gradient(cmap="RdYlGn", axis=0),
                     use_container_width=True)

        # Profitability ratios chart
        col1, col2 = st.columns(2)
        with col1:
            fig = go.Figure()
            for i, col_name in enumerate(["Gross Margin (%)", "Operating Margin (%)", "Net Margin (%)", "FCF Margin (%)"]):
                if col_name in ratios.columns:
                    fig.add_trace(go.Scatter(x=ratios.index, y=ratios[col_name], name=col_name,
                                             line=dict(color=COLORS[i], width=2.5), mode="lines+markers"))
            apply_layout(fig, "Profitability Ratios")
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            fig = go.Figure()
            for i, col_name in enumerate(["Current Ratio", "Cash Ratio", "Debt/Equity"]):
                if col_name in ratios.columns:
                    fig.add_trace(go.Scatter(x=ratios.index, y=ratios[col_name], name=col_name,
                                             line=dict(color=COLORS[i], width=2.5), mode="lines+markers"))
            apply_layout(fig, "Liquidity & Solvency Ratios")
            st.plotly_chart(fig, use_container_width=True)

    with tab4:
        st.markdown("### DuPont Decomposition")
        st.markdown("**ROE = Net Profit Margin × Asset Turnover × Equity Multiplier**")
        st.dataframe(DUPONT.style.format("{:.4f}").background_gradient(cmap="RdYlGn", axis=0),
                     use_container_width=True)

        fig = make_subplots(rows=1, cols=3, subplot_titles=("Net Profit Margin", "Asset Turnover", "Equity Multiplier"))
        fig.add_trace(go.Bar(x=DUPONT.index, y=DUPONT["Net Profit Margin"], marker_color=COLORS[0],
                             name="Margin"), row=1, col=1)
        fig.add_trace(go.Bar(x=DUPONT.index, y=DUPONT["Asset Turnover"], marker_color=COLORS[1],
                             name="Turnover"), row=1, col=2)
        fig.add_trace(go.Bar(x=DUPONT.index, y=DUPONT["Equity Multiplier"], marker_color=COLORS[4],
                             name="Leverage"), row=1, col=3)
        apply_layout(fig, "DuPont 3-Factor Decomposition", height=380)
        st.plotly_chart(fig, use_container_width=True)

        # ROE trend
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=DUPONT.index, y=DUPONT["ROE (DuPont)"],
                                 line=dict(color=COLORS[0], width=3), mode="lines+markers+text",
                                 text=[f"{v:.1f}%" for v in DUPONT["ROE (DuPont)"]],
                                 textposition="top center", name="ROE"))
        apply_layout(fig, "ROE (DuPont) Evolution", height=350)
        st.plotly_chart(fig, use_container_width=True)

    with tab5:
        st.markdown("### Trend Analysis — Indexed to Base Year (2020 = 100)")
        ist = INCOME_STATEMENT[["Total Revenue", "Gross Profit", "Operating Income", "Net Income"]].copy()
        ist_sorted = ist.sort_index()
        base = ist_sorted.iloc[0].replace(0, np.nan)
        trend = ist_sorted.div(base, axis=1) * 100

        fig = go.Figure()
        for i, col in enumerate(trend.columns):
            fig.add_trace(go.Scatter(x=trend.index, y=trend[col], name=col,
                                     line=dict(color=COLORS[i], width=2.5), mode="lines+markers"))
        fig.add_hline(y=100, line_dash="dash", line_color="rgba(255,255,255,0.3)")
        apply_layout(fig, "Income Statement Trend Index (2020 = 100)")
        st.plotly_chart(fig, use_container_width=True)

        # Revenue CAGR
        rev_20 = INCOME_STATEMENT.loc[2020, "Total Revenue"]
        rev_25 = INCOME_STATEMENT.loc[2025, "Total Revenue"]
        cagr = (rev_25 / rev_20) ** (1/5) - 1
        st.metric("5-Year Revenue CAGR (2020–2025)", f"{cagr*100:.1f}%")


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 5: VALUATION MODELS
# ══════════════════════════════════════════════════════════════════════════════
elif page == "💰 Valuation Models":
    st.markdown("# Valuation Analysis")
    st.markdown("*DCF, Comparable Company, and Scenario Analysis per MBAN5570 Financial Modelling*")
    divider()

    tab1, tab2, tab3 = st.tabs(["DCF Model", "Comparable Company", "Sensitivity & Scenarios"])

    with tab1:
        st.markdown("### Discounted Cash Flow (DCF) Valuation")

        # User inputs
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            wacc = st.slider("WACC (%)", 8.0, 15.0, 10.0, 0.5) / 100
        with col2:
            tg = st.slider("Terminal Growth (%)", 1.0, 5.0, 3.0, 0.5) / 100
        with col3:
            fcf_margin = st.slider("Steady-State FCF Margin (%)", 15.0, 40.0, 28.0, 1.0) / 100
        with col4:
            base_growth = st.slider("Y1 Revenue Growth (%)", 20.0, 70.0, 55.0, 5.0) / 100

        # Project revenues
        proj_years = 7
        current_rev = INCOME_STATEMENT.loc[2025, "Total Revenue"]
        shares = MARKET_DATA["shares_outstanding"]
        growth_rates = [max(base_growth * (0.82 ** i), tg + 0.02) for i in range(proj_years)]

        projections = []
        rev = current_rev
        for i, g in enumerate(growth_rates):
            rev = rev * (1 + g)
            # Margin ramp
            margin_i = fcf_margin * min(1.0, 0.7 + 0.3 * (i / proj_years))
            fcf = rev * margin_i
            pv = fcf / (1 + wacc) ** (i + 1)
            projections.append({
                "Year": f"FY{2026+i}", "Rev Growth": f"{g:.1%}", "Revenue ($M)": rev,
                "FCF Margin": f"{margin_i:.1%}", "FCF ($M)": fcf,
                "PV Factor": 1/(1+wacc)**(i+1), "PV of FCF ($M)": pv
            })

        df_proj = pd.DataFrame(projections)
        st.dataframe(df_proj.style.format({
            "Revenue ($M)": "${:,.0f}", "FCF ($M)": "${:,.0f}", "PV of FCF ($M)": "${:,.0f}",
            "PV Factor": "{:.4f}"
        }), use_container_width=True)

        sum_pv = df_proj["PV of FCF ($M)"].sum()
        terminal_fcf = projections[-1]["FCF ($M)"] * (1 + tg)
        terminal_value = terminal_fcf / (wacc - tg)
        pv_tv = terminal_value / (1 + wacc) ** proj_years
        net_cash = (BALANCE_SHEET.loc[2025, "Cash & Equivalents"] +
                    BALANCE_SHEET.loc[2025, "Short-Term Investments"] -
                    BALANCE_SHEET.loc[2025, "Long-Term Debt"])
        ev = sum_pv + pv_tv
        equity_val = ev + net_cash
        implied_price = equity_val * 1e6 / shares

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Sum of PV(FCF)", f"${sum_pv:,.0f}M")
        c2.metric("PV(Terminal Value)", f"${pv_tv:,.0f}M")
        c3.metric("Enterprise Value", f"${ev:,.0f}M")
        c4.metric("Implied Share Price", fmt_price(implied_price),
                  f"{'↑' if implied_price > MARKET_DATA['current_price'] else '↓'} vs ${MARKET_DATA['current_price']:.2f}")

        # Pie: PV split
        fig = go.Figure(data=[go.Pie(
            labels=["PV of Projected FCFs", "PV of Terminal Value"],
            values=[sum_pv, pv_tv], hole=0.55,
            marker_colors=[COLORS[0], COLORS[4]],
            textinfo="label+percent", texttemplate="%{label}<br>%{percent}"
        )])
        apply_layout(fig, "DCF Value Composition", height=350)
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        st.markdown("### Comparable Company Analysis")
        st.markdown("Enterprise Value multiples vs. peer group median.")
        st.dataframe(PEER_COMPARISON.style.format({
            "Market Cap ($B)": "${:.1f}B", "Revenue TTM ($B)": "${:.2f}B",
            "Rev Growth (%)": "{:.1f}%", "Gross Margin (%)": "{:.1f}%",
            "Op Margin (%)": "{:.1f}%", "FCF Margin (%)": "{:.1f}%",
            "EV/Revenue": "{:.1f}x", "P/S": "{:.1f}x",
            "ROE (%)": "{:.1f}%", "Beta": "{:.2f}",
        }).background_gradient(cmap="RdYlGn", subset=["Rev Growth (%)", "Op Margin (%)", "FCF Margin (%)"]),
                     use_container_width=True)

        # Visual comparison
        peer = PEER_COMPARISON
        fig = make_subplots(rows=1, cols=3, subplot_titles=("EV/Revenue", "Revenue Growth %", "FCF Margin %"))
        for i, metric in enumerate(["EV/Revenue", "Rev Growth (%)", "FCF Margin (%)"]):
            colors_bar = [COLORS[1] if t == "PLTR" else COLORS[0] for t in peer["Ticker"]]
            fig.add_trace(go.Bar(x=peer["Ticker"], y=peer[metric], marker_color=colors_bar,
                                 name=metric, showlegend=False), row=1, col=i+1)
        apply_layout(fig, "PLTR vs Peers — Key Multiples", height=380)
        st.plotly_chart(fig, use_container_width=True)

        # Implied valuation from peer multiples
        peer_only = peer[peer["Ticker"] != "PLTR"]
        med_evr = peer_only["EV/Revenue"].median()
        pltr_rev = INCOME_STATEMENT.loc[2025, "Total Revenue"]
        implied_ev = pltr_rev * med_evr
        implied_p = (implied_ev * 1e6 + net_cash * 1e6) / shares
        st.metric(f"Implied Price at Peer Median EV/Rev ({med_evr:.1f}x)", fmt_price(implied_p),
                  f"vs Current {fmt_price(MARKET_DATA['current_price'])}")

    with tab3:
        st.markdown("### Sensitivity Analysis — WACC vs Terminal Growth Rate")

        wacc_range = [0.08, 0.09, 0.10, 0.11, 0.12, 0.13]
        tg_range = [0.02, 0.025, 0.03, 0.035, 0.04]
        sens = {}
        for w in wacc_range:
            row = {}
            for t in tg_range:
                gr = [max(0.55 * (0.82 ** i), t + 0.02) for i in range(7)]
                rev_s = current_rev
                pv_sum = 0
                for i, g in enumerate(gr):
                    rev_s *= (1 + g)
                    m = 0.28 * min(1.0, 0.7 + 0.3 * (i / 7))
                    pv_sum += (rev_s * m) / (1 + w) ** (i + 1)
                tv = (rev_s * 0.28 * (1 + t)) / (w - t)
                pvtv = tv / (1 + w) ** 7
                eq = (pv_sum + pvtv + net_cash) * 1e6 / shares
                row[f"TG={t:.1%}"] = round(eq, 2)
            sens[f"WACC={w:.0%}"] = row

        df_sens = pd.DataFrame(sens).T
        st.dataframe(df_sens.style.format("${:,.2f}")
                     .background_gradient(cmap="RdYlGn", axis=None),
                     use_container_width=True)

        # Heatmap
        fig = go.Figure(data=go.Heatmap(
            z=df_sens.values, x=df_sens.columns, y=df_sens.index,
            colorscale="RdYlGn", text=[[f"${v:.0f}" for v in row] for row in df_sens.values],
            texttemplate="%{text}", colorbar_title="Price ($)"
        ))
        apply_layout(fig, "Implied Share Price — WACC vs Terminal Growth", height=380)
        st.plotly_chart(fig, use_container_width=True)

        # Scenario analysis
        divider()
        st.markdown("### Scenario Analysis — Bull / Base / Bear")
        scenarios = {
            "Bull": {"growth": [0.65, 0.55, 0.45, 0.38, 0.32, 0.28, 0.24], "fcf_m": 0.32, "wacc": 0.09, "tg": 0.04},
            "Base": {"growth": [0.55, 0.42, 0.32, 0.26, 0.22, 0.18, 0.16], "fcf_m": 0.28, "wacc": 0.10, "tg": 0.03},
            "Bear": {"growth": [0.35, 0.25, 0.18, 0.14, 0.12, 0.10, 0.08], "fcf_m": 0.22, "wacc": 0.12, "tg": 0.02},
        }
        scen_results = {}
        for name, p in scenarios.items():
            rev_s = current_rev
            pv_sum = 0
            for i, g in enumerate(p["growth"]):
                rev_s *= (1 + g)
                m = p["fcf_m"] * min(1.0, 0.7 + 0.3 * (i / 7))
                pv_sum += (rev_s * m) / (1 + p["wacc"]) ** (i + 1)
            tv = (rev_s * p["fcf_m"] * (1 + p["tg"])) / (p["wacc"] - p["tg"])
            pvtv = tv / (1 + p["wacc"]) ** 7
            eq = (pv_sum + pvtv + net_cash) * 1e6 / shares
            scen_results[name] = {
                "Implied Price": eq, "FY2032 Revenue ($B)": rev_s / 1000,
                "WACC": p["wacc"], "Terminal Growth": p["tg"], "FCF Margin": p["fcf_m"],
            }

        df_scen = pd.DataFrame(scen_results).T
        st.dataframe(df_scen.style.format({
            "Implied Price": "${:,.2f}", "FY2032 Revenue ($B)": "${:.1f}B",
            "WACC": "{:.0%}", "Terminal Growth": "{:.0%}", "FCF Margin": "{:.0%}"
        }), use_container_width=True)

        c1, c2, c3 = st.columns(3)
        for col, (name, data) in zip([c1, c2, c3], scen_results.items()):
            color = {"Bull": "green", "Base": "blue", "Bear": "red"}[name]
            col.metric(f"{name} Case", fmt_price(data["Implied Price"]),
                      f"vs {fmt_price(MARKET_DATA['current_price'])}")


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 6: RISK & MONTE CARLO
# ══════════════════════════════════════════════════════════════════════════════
elif page == "🎯 Risk & Monte Carlo":
    st.markdown("# Risk Analysis & Monte Carlo Simulation")
    st.markdown("*Per MBAN5570: GBM, Monte Carlo, Sensitivity Analysis*")
    divider()

    tab1, tab2 = st.tabs(["Monte Carlo (GBM)", "Risk Factors"])

    with tab1:
        st.markdown("### Geometric Brownian Motion — Stock Price Simulation")
        st.markdown(r"$dS = S \cdot \mu \cdot dt + S \cdot \sigma \cdot \varepsilon \cdot \sqrt{\Delta t}$")

        c1, c2, c3 = st.columns(3)
        with c1:
            n_sims = st.selectbox("Simulations", [500, 1000, 5000, 10000], index=1)
        with c2:
            n_days = st.selectbox("Trading Days", [63, 126, 252], index=2, format_func=lambda x: {63:"3 Months", 126:"6 Months", 252:"1 Year"}[x])
        with c3:
            vol_mult = st.slider("Volatility Multiplier", 0.5, 2.0, 1.0, 0.1)

        # GBM parameters (based on PLTR historical)
        S0 = MARKET_DATA["current_price"]
        mu = 0.65  # annualized drift (based on recent performance)
        sigma = 0.70 * vol_mult  # annualized vol (PLTR is high-vol)
        dt = 1 / 252

        np.random.seed(42)
        paths = np.zeros((n_sims, n_days + 1))
        paths[:, 0] = S0
        for t in range(1, n_days + 1):
            z = np.random.standard_normal(n_sims)
            paths[:, t] = paths[:, t-1] * np.exp((mu - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * z)

        final = paths[:, -1]

        # Summary stats
        c1, c2, c3, c4, c5 = st.columns(5)
        c1.metric("Current Price", fmt_price(S0))
        c2.metric("Mean Outcome", fmt_price(np.mean(final)))
        c3.metric("Median Outcome", fmt_price(np.median(final)))
        c4.metric("5th Percentile", fmt_price(np.percentile(final, 5)))
        c5.metric("95th Percentile", fmt_price(np.percentile(final, 95)))

        # Fan chart
        fig = go.Figure()
        days_x = list(range(n_days + 1))
        # Percentile bands
        for lo, hi, opacity in [(5,95,0.1), (10,90,0.15), (25,75,0.2)]:
            lo_line = np.percentile(paths, lo, axis=0)
            hi_line = np.percentile(paths, hi, axis=0)
            fig.add_trace(go.Scatter(x=days_x, y=hi_line, mode="lines", line=dict(width=0), showlegend=False))
            fig.add_trace(go.Scatter(x=days_x, y=lo_line, mode="lines", line=dict(width=0),
                                     fill="tonexty", fillcolor=f"rgba(59,130,246,{opacity})",
                                     name=f"{lo}th-{hi}th Percentile"))
        # Median
        fig.add_trace(go.Scatter(x=days_x, y=np.median(paths, axis=0), mode="lines",
                                 line=dict(color=COLORS[2], width=2.5), name="Median Path"))
        # Sample paths
        for i in range(min(20, n_sims)):
            fig.add_trace(go.Scatter(x=days_x, y=paths[i], mode="lines",
                                     line=dict(color="rgba(255,255,255,0.05)", width=0.5), showlegend=False))
        fig.add_hline(y=S0, line_dash="dash", line_color="white", opacity=0.3)
        apply_layout(fig, f"Monte Carlo GBM — {n_sims} Simulations, {n_days} Days", height=500)
        fig.update_xaxes(title="Trading Days")
        fig.update_yaxes(title="Price ($)")
        st.plotly_chart(fig, use_container_width=True)

        # Distribution
        fig = go.Figure()
        fig.add_trace(go.Histogram(x=final, nbinsx=80, marker_color=COLORS[0], opacity=0.7, name="Final Prices"))
        fig.add_vline(x=S0, line_dash="dash", line_color=COLORS[3], annotation_text="Current")
        fig.add_vline(x=np.mean(final), line_dash="dash", line_color=COLORS[1], annotation_text="Mean")
        apply_layout(fig, "Distribution of Simulated Final Prices", height=380)
        fig.update_xaxes(title="Price ($)")
        st.plotly_chart(fig, use_container_width=True)

        prob_up = np.mean(final > S0) * 100
        prob_double = np.mean(final > S0 * 2) * 100
        prob_half = np.mean(final < S0 * 0.5) * 100
        st.markdown(f"**Probability above current price:** {prob_up:.1f}% | "
                    f"**Probability of doubling:** {prob_double:.1f}% | "
                    f"**Probability of halving:** {prob_half:.1f}%")

    with tab2:
        st.markdown("### Critical Risk Factors")

        risks = [
            ("Valuation Risk", "HIGH", "Trading at ~81x EV/Revenue — among the most expensive large-cap software stocks. "
             "Any slowdown in growth could trigger severe multiple compression."),
            ("Competition Risk", "MEDIUM-HIGH", "Microsoft (Azure AI), AWS (SageMaker), Google (Vertex AI) all competing "
             "in enterprise AI. Hyperscalers have deeper distribution and bundling advantages."),
            ("SBC Dilution", "MEDIUM", "$700M in FY2025 stock-based compensation dilutes shareholders. "
             "SBC as % of revenue has improved (15.6% in FY2025 vs 50% in FY2021) but remains elevated."),
            ("Customer Concentration", "MEDIUM", "Government contracts are lumpy and subject to political/budget cycles. "
             "Top 20 customers account for significant revenue share."),
            ("Insider Selling", "MEDIUM", "CEO Alex Karp has sold billions in shares via 10b5-1 plans. "
             "While common for founders, sustained selling may pressure sentiment."),
            ("Macro / Rate Risk", "MEDIUM", "High-duration growth stock — highly sensitive to interest rate changes. "
             "Rising rates compress multiples on high-growth, high-P/E names disproportionately."),
            ("Execution Risk", "LOW-MEDIUM", "FY2026 guidance of 61% growth is aggressive. AIP must continue "
             "converting boot camps to production; any stall could disappoint expectations."),
        ]

        for name, level, desc in risks:
            color = {"HIGH": "🔴", "MEDIUM-HIGH": "🟠", "MEDIUM": "🟡", "LOW-MEDIUM": "🟢"}[level]
            with st.expander(f"{color} **{name}** — {level}"):
                st.markdown(desc)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 7: PEER COMPARISON
# ══════════════════════════════════════════════════════════════════════════════
elif page == "📉 Peer Comparison":
    st.markdown("# Comparable Company Analysis")
    st.markdown("*PLTR vs Enterprise AI / Cloud Infrastructure Peers*")
    divider()

    peer = PEER_COMPARISON

    st.dataframe(peer.set_index("Ticker").style.format({
        "Market Cap ($B)": "${:.1f}B", "Revenue TTM ($B)": "${:.2f}B",
        "Rev Growth (%)": "{:.1f}%", "Gross Margin (%)": "{:.1f}%",
        "Op Margin (%)": "{:.1f}%", "Net Margin (%)": "{:.1f}%",
        "FCF Margin (%)": "{:.1f}%", "EV/Revenue": "{:.1f}x",
        "Forward P/E": "{:.0f}x", "P/S": "{:.1f}x",
        "ROE (%)": "{:.1f}%", "Debt/Equity": "{:.2f}", "Beta": "{:.2f}",
    }).background_gradient(cmap="RdYlGn", subset=["Rev Growth (%)", "Op Margin (%)", "FCF Margin (%)", "ROE (%)"]),
                 use_container_width=True)

    # Spider chart
    categories = ["Rev Growth (%)", "Gross Margin (%)", "Op Margin (%)", "FCF Margin (%)", "ROE (%)"]
    fig = go.Figure()
    for _, row in peer.iterrows():
        vals = [row[c] if pd.notna(row[c]) else 0 for c in categories]
        fig.add_trace(go.Scatterpolar(r=vals + [vals[0]], theta=categories + [categories[0]],
                                       name=row["Ticker"], fill="toself", opacity=0.3))
    apply_layout(fig, "Peer Radar — Profitability & Growth", height=500)
    fig.update_layout(polar=dict(
        bgcolor="rgba(17,24,39,0.5)",
        radialaxis=dict(gridcolor="rgba(30,41,59,0.5)", color="rgba(255,255,255,0.5)"),
        angularaxis=dict(gridcolor="rgba(30,41,59,0.5)", color="rgba(255,255,255,0.8)")
    ))
    st.plotly_chart(fig, use_container_width=True)

    # Bar comparisons
    col1, col2 = st.columns(2)
    with col1:
        fig = go.Figure()
        colors_bar = [COLORS[1] if t == "PLTR" else COLORS[0] for t in peer["Ticker"]]
        fig.add_trace(go.Bar(x=peer["Ticker"], y=peer["EV/Revenue"], marker_color=colors_bar))
        fig.add_hline(y=peer["EV/Revenue"].median(), line_dash="dash", line_color=COLORS[2],
                      annotation_text=f"Median: {peer['EV/Revenue'].median():.1f}x")
        apply_layout(fig, "EV/Revenue Multiple", height=350)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = go.Figure()
        # Rule of 40 (Growth + FCF Margin)
        r40 = peer["Rev Growth (%)"] + peer["FCF Margin (%)"]
        colors_bar = [COLORS[1] if t == "PLTR" else COLORS[0] for t in peer["Ticker"]]
        fig.add_trace(go.Bar(x=peer["Ticker"], y=r40, marker_color=colors_bar))
        fig.add_hline(y=40, line_dash="dash", line_color=COLORS[3], annotation_text="Rule of 40")
        apply_layout(fig, "Rule of 40 (Growth % + FCF Margin %)", height=350)
        st.plotly_chart(fig, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 8: AI-ASSISTED ANALYSIS (Course Section 2.B)
# ══════════════════════════════════════════════════════════════════════════════
elif page == "🤖 AI-Assisted Analysis":
    st.markdown("# AI-Assisted Equity Research")
    st.markdown("*Per MBAN5570 Section 2.B: How AI tools enhanced this analysis*")
    divider()

    st.markdown("## How AI Was Used in This Research")

    st.markdown("""
    ### 1. Financial Data Aggregation & Summarization
    AI was used to rapidly aggregate Palantir's financial statements, key metrics, and segment data
    from multiple sources (SEC filings, earnings releases, investor presentations) into a structured
    dataset. This process — which would typically take an analyst 4–6 hours — was completed in minutes,
    allowing more time for actual analytical interpretation.

    ### 2. Earnings Call & Filing Analysis
    AI analyzed Palantir's earnings call transcripts to identify recurring themes: AIP adoption rates,
    boot camp conversion metrics, government contract momentum, and management's forward guidance
    language. Key insight extracted: management's shift from discussing customer count growth to
    emphasizing deal value and expansion rates — signaling product maturity.

    ### 3. Valuation Scenario Generation
    AI generated multiple DCF scenarios with varying assumptions (growth rates, margins, discount rates)
    and produced sensitivity tables that would be labor-intensive to build manually. The Monte Carlo
    simulation runs 1,000–10,000 GBM paths to model price uncertainty probabilistically.

    ### 4. Risk Identification & Pattern Recognition
    AI scanned financial statement trends to identify SBC dilution patterns, cash conversion cycles,
    and margin expansion trajectories. It also flagged the valuation premium relative to peers as the
    primary risk factor — corroborated by traditional analysis.

    ### 5. Visualization & Dashboard Development
    This Streamlit dashboard was built with AI assistance, creating interactive Plotly visualizations
    that allow the user to explore financial data like an advanced analyst. The dashboard automates
    ratio calculations, DuPont decomposition, and comparable analysis.
    """)

    divider()
    st.markdown("## AI-Generated Insights")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### Key Patterns Identified by AI")
        st.markdown("""
        - **Revenue acceleration curve**: Growth rate increased from 17% (2022) to 56% (2025) — counter to typical SaaS deceleration
        - **Margin expansion inflection**: GAAP operating margin went from -8.4% (2022) to +24.6% (2025) — 33pp improvement in 3 years
        - **FCF conversion quality**: FCF margin (51%) exceeds GAAP net margin (36%) — driven by SBC add-back and low capex intensity
        - **US Commercial as growth driver**: This segment grew from $156M (2020) to $1,370M (2025) — a 9x increase, validating AIP
        - **Balance sheet strength**: $7.2B net cash, zero debt — rare for a high-growth software company
        """)

    with col2:
        st.markdown("### AI-Generated Forward Projections")
        st.markdown("""
        - **FY2026E Revenue**: $7.19B (per company guidance of 61% growth)
        - **FY2026E Adj. Operating Income**: $3.8–3.9B (guided ~53% margin)
        - **FY2026E FCF**: $3.5–3.6B (guided, ~50% margin sustained)
        - **3-Year Revenue CAGR (2025–2028E)**: 35–45% in base case
        - **Implied terminal revenue (2032E)**: $20–35B range across scenarios
        """)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 9: CRITICAL EVALUATION (Course Section 2.C)
# ══════════════════════════════════════════════════════════════════════════════
elif page == "📋 Critical Evaluation":
    st.markdown("# Critical Evaluation of AI Outputs")
    st.markdown("*Per MBAN5570 Section 2.C: What AI Got Right, Wrong, and Our Final Assessment*")
    divider()

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "What AI Got Right", "What AI Got Wrong", "What We Accept",
        "What We Discarded", "How AI Enhances Research"
    ])

    with tab1:
        st.markdown("### What AI Got Right")
        st.markdown("""
        **1. Revenue trajectory identification** — AI correctly identified the acceleration pattern in
        Palantir's revenue growth, which defies typical SaaS deceleration curves. This was validated
        by Q4 2025 results showing 70% growth.

        **2. Margin expansion narrative** — AI accurately captured the operating leverage story: as
        Palantir scales, its high gross margins (~82%) flow through to operating income at increasing
        rates due to relatively fixed R&D and SGA costs.

        **3. Cash flow quality** — AI correctly identified that Palantir's free cash flow exceeds
        GAAP net income due to high SBC (non-cash) and minimal capex requirements. This is an important
        nuance for valuation.

        **4. Competitive positioning** — AI accurately assessed Palantir's differentiation through its
        ontology layer and AIP platform, distinguishing it from generic cloud/AI competitors.

        **5. Risk factor prioritization** — Valuation risk was correctly identified as the #1 concern,
        which aligns with Wall Street's split consensus (6 Buy, 10 Hold, 6 Sell).
        """)

    with tab2:
        st.markdown("### What AI Got Wrong or Oversimplified")
        st.markdown("""
        **1. DCF precision fallacy** — AI-generated DCF models imply false precision. With PLTR's
        growth profile, small changes in WACC or terminal growth swing implied price by 50%+. The
        sensitivity table demonstrates this fragility.

        **2. Peer comparison limitations** — AI treated all peers equally, but PLTR's business model
        (government + commercial, platform vs. point solution) makes direct comparison imperfect.
        CrowdStrike (cybersecurity) and MongoDB (database) serve fundamentally different markets.

        **3. SBC normalization** — AI's adjusted metrics (adding back SBC) paint a rosier picture
        than GAAP. In reality, SBC is a real economic cost to shareholders through dilution.
        The $700M in FY2025 SBC represents ~15.6% of revenue — material.

        **4. Growth extrapolation risk** — AI's base case projects 35–45% CAGR over 3 years. History
        shows very few software companies sustain >30% growth beyond $5B revenue. The probability of
        deceleration is higher than models suggest.

        **5. Qualitative factors underweighted** — AI underweighted key risks like key-man risk
        (Alex Karp's leadership style), geopolitical sensitivities, and potential regulatory scrutiny
        of government AI deployment.
        """)

    with tab3:
        st.markdown("### What We Accept from AI Analysis")
        st.markdown("""
        - The **directional thesis** that Palantir is a legitimate AI platform leader, not a government contractor
        - **Financial statement analysis** — ratio calculations, trend identification, DuPont decomposition are mathematically reliable
        - The **Rule of 40+ assessment** — with growth + FCF margin = 107, Palantir objectively meets elite software metrics
        - **Balance sheet strength** assessment — zero debt, $7.2B net cash is factual and strategically significant
        - The **peer comparison framework** — while imperfect, it provides useful context for relative valuation
        - **Monte Carlo outputs** as a probability framework — not as precise predictions, but as a range of outcomes
        """)

    with tab4:
        st.markdown("### What We Discarded or Modified")
        st.markdown("""
        - **Point-estimate DCF valuations** — We use sensitivity tables and scenario ranges instead of a single "fair value"
        - **AI's implicit growth bias** — We applied more conservative decay rates to growth projections
        - **Adjusted metrics as primary** — We present both GAAP and adjusted side-by-side; neither alone tells the full story
        - **Simple peer average multiples** — We note the median but emphasize PLTR trades at a massive premium for a reason (or not)
        - **Linear extrapolation of margins** — Operating leverage has limits; we cap steady-state FCF margin assumptions
        """)

    with tab5:
        st.markdown("### How AI Enhances Equity Research")
        st.markdown("""
        **Speed of analysis**: What would take a team of analysts days was accomplished in hours —
        data aggregation, ratio computation, visualization, and scenario modeling.

        **Breadth of coverage**: AI enabled simultaneous analysis across all course-required dimensions
        (horizontal, vertical, ratio, trend, DuPont, DCF, comparable, Monte Carlo, event study) that
        would be impractical for a two-person team manually.

        **Interactive exploration**: The Streamlit dashboard allows dynamic what-if analysis (adjusting
        WACC, growth rates, vol assumptions) that static reports cannot provide.

        **Consistency**: AI ensures all ratios are computed identically across years, eliminating
        human calculation errors that can creep into manual spreadsheet analysis.

        **Limitations remain**: AI cannot replace investment judgment. It generates analysis, but the
        "so what" — whether to buy, hold, or sell at this price — requires human interpretation of
        qualitative factors, market sentiment, and personal risk tolerance.

        **Our conclusion**: AI is a powerful analytical accelerator but not a replacement for
        fundamental investment thinking. The most valuable insights came from questioning AI outputs,
        not accepting them uncritically.
        """)


# ══════════════════════════════════════════════════════════════════════════════
# FOOTER
# ══════════════════════════════════════════════════════════════════════════════
divider()
st.markdown("""
<div style="text-align: center; color: var(--text-secondary); font-size: 0.8rem; padding: 20px 0;">
    MBAN5570 Accounting & Financial Analytics | Sobey School of Business, Saint Mary's University<br>
    Dr. Mohammad M. Rahaman | Equity Research Analytics — Palantir Technologies (PLTR)<br>
    <em>Data sources: SEC EDGAR, Palantir Investor Relations, Yahoo Finance</em>
</div>
""", unsafe_allow_html=True)
