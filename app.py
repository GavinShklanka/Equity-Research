"""
PALANTIR TECHNOLOGIES — EQUITY RESEARCH INVESTIGATION
MBAN5570 Accounting & Financial Analytics | Sobey School of Business
Dr. Mohammad M. Rahaman
"""
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from pltr_data import (
    COMPANY_INFO, MARKET_DATA, INCOME_STATEMENT, BALANCE_SHEET, CASH_FLOW,
    REVENUE_SEGMENTS, KEY_RATIOS, DUPONT, PEER_COMPARISON, KEY_EVENTS,
    ANALYST_DATA, GUIDANCE, compute_ratios,
    GLOBAL_FOOTPRINT, EXPANSION_SIGNALS, AI_ECOSYSTEM_DATA, TOOLTIP_CONTENT,
)

st.set_page_config(page_title="PLTR Equity Research | MBAN5570", page_icon="📄", layout="wide", initial_sidebar_state="expanded")

B = {"bg":"#F7F4F1","surface":"#FFFFFF","sfa":"#F1ECE7","maroon":"#6E2233","ms":"#8E3B4D",
     "navy":"#324B6B","gold":"#C7A86D","text":"#1F2937","muted":"#6B7280","border":"#D8CDD2",
     "pos":"#1F6B52","neg":"#A13A3A"}
C = [B["navy"], B["pos"], B["gold"], B["neg"], B["ms"], "#6366F1", "#0D9488"]

st.markdown(f"""<style>
@import url('https://fonts.googleapis.com/css2?family=Source+Serif+4:wght@400;600;700&family=Inter:wght@300;400;500;600&display=swap');
.stApp {{ background-color: {B['bg']}; }}
h1 {{ color: {B['maroon']} !important; font-family: 'Source Serif 4', Georgia, serif !important; font-weight: 700 !important; font-size: 1.7rem !important; }}
h2 {{ color: {B['navy']} !important; font-family: 'Source Serif 4', Georgia, serif !important; font-weight: 600 !important; border-bottom: 2px solid {B['gold']}; padding-bottom: 6px; font-size: 1.25rem !important; }}
h3 {{ color: {B['text']} !important; font-family: 'Inter', sans-serif !important; font-weight: 500 !important; font-size: 1.0rem !important; }}
p, li, span {{ font-family: 'Inter', sans-serif; color: {B['text']}; line-height: 1.6; }}
section[data-testid="stSidebar"] {{ background: linear-gradient(180deg, {B['maroon']} 0%, #4A1522 100%); }}
section[data-testid="stSidebar"] .stMarkdown p, section[data-testid="stSidebar"] .stMarkdown li, section[data-testid="stSidebar"] label {{ color: #E8D8DC !important; }}
section[data-testid="stSidebar"] .stMarkdown h2 {{ color: #FFF !important; border-bottom-color: {B['gold']} !important; }}
div[data-testid="stMetric"] {{ background: {B['surface']}; border: 1px solid {B['border']}; border-radius: 8px; padding: 14px 18px; }}
div[data-testid="stMetric"] label {{ color: {B['muted']} !important; font-size: 0.78rem !important; text-transform: uppercase; letter-spacing: 0.04em; }}
div[data-testid="stMetric"] [data-testid="stMetricValue"] {{ color: {B['text']} !important; font-weight: 600 !important; }}
.stTabs [data-baseweb="tab-list"] {{ gap: 2px; background: {B['sfa']}; border-radius: 8px; padding: 3px; }}
.stTabs [data-baseweb="tab"] {{ border-radius: 6px; padding: 8px 16px; color: {B['muted']}; font-weight: 500; font-size: 0.85rem; }}
.stTabs [aria-selected="true"] {{ background: {B['maroon']} !important; color: white !important; }}
.stDataFrame {{ border-radius: 8px; overflow: hidden; border: 1px solid {B['border']}; }}
.streamlit-expanderHeader {{ background: {B['sfa']} !important; border-radius: 6px; color: {B['text']} !important; }}
.pq {{ font-family: 'Source Serif 4', serif; font-size: 1.4rem; font-weight: 600; color: {B['maroon']}; line-height: 1.3; margin-bottom: 4px; }}
.pa {{ font-size: 0.95rem; color: {B['text']}; font-weight: 500; padding: 10px 16px; background: {B['surface']}; border-left: 3px solid {B['gold']}; border-radius: 0 6px 6px 0; margin-bottom: 4px; }}
.pi {{ font-size: 0.85rem; color: {B['muted']}; font-style: italic; margin-bottom: 18px; }}
.cbox {{ background: {B['surface']}; border: 1px solid {B['border']}; border-radius: 8px; padding: 12px 16px; margin: 8px 0; font-size: 0.88rem; line-height: 1.5; }}
.cbox .cl {{ font-weight: 600; font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 3px; }}
.cbox.cs .cl {{ color: {B['pos']}; }} .cbox.cc .cl {{ color: {B['neg']}; }}
.cbox.cn .cl {{ color: {B['navy']}; }} .cbox.cv .cl {{ color: {B['maroon']}; }}
.cap {{ font-size: 0.82rem; color: {B['muted']}; margin-top: -8px; margin-bottom: 14px; line-height: 1.5; }}
.cap strong {{ color: {B['text']}; }}
.sr {{ height: 1px; background: linear-gradient(90deg, transparent, {B['border']}, transparent); margin: 1.5rem 0; }}
.tt {{ background: rgba(110,34,51,0.04); border: 1px solid rgba(110,34,51,0.12); border-radius: 8px; padding: 10px 14px; margin: 6px 0 12px; font-size: 0.82rem; }}
.tt .tl {{ color: {B['maroon']}; font-weight: 600; font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.05em; }}
.tt .tf {{ font-family: monospace; color: {B['navy']}; background: rgba(50,75,107,0.06); padding: 2px 6px; border-radius: 3px; display: inline-block; }}
</style>""", unsafe_allow_html=True)

PL = dict(template="plotly_white", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(247,244,241,0.3)",
    font=dict(family="Inter", color=B["text"], size=12), margin=dict(l=40, r=20, t=50, b=40),
    legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(size=11)),
    xaxis=dict(gridcolor="rgba(216,205,210,0.4)"), yaxis=dict(gridcolor="rgba(216,205,210,0.4)"))

def al(fig, title="", h=450):
    fig.update_layout(**PL, title=dict(text=title, font=dict(size=14)), height=h); return fig
def fmt_b(v):
    return "N/A" if v is None else (f"${v/1e3:.1f}B" if abs(v) >= 1000 else f"${v:.0f}M")
def fmt_p(v): return "N/A" if v is None else f"${v:,.2f}"
def ph(q, a, i):
    st.markdown(f'<div class="pq">{q}</div><div class="pa">{a}</div><div class="pi">{i}</div>', unsafe_allow_html=True)
def cap(p, a):
    st.markdown(f'<div class="cap"><strong>What this shows:</strong> {p}<br><strong>Analyst lens:</strong> {a}</div>', unsafe_allow_html=True)
def cbox(label, text, tone="n"):
    st.markdown(f'<div class="cbox c{tone}"><div class="cl">{label}</div>{text}</div>', unsafe_allow_html=True)
def sr(): st.markdown('<div class="sr"></div>', unsafe_allow_html=True)
def tt(key):
    if not st.session_state.get("learn_mode", False): return
    t = TOOLTIP_CONTENT.get(key)
    if not t: return
    parts = [f'<div class="tl">Definition</div><div>{t["definition"]}</div>']
    if t.get("formula"): parts.append(f'<div class="tl" style="margin-top:6px">Formula</div><div class="tf">{t["formula"]}</div>')
    parts.append(f'<div class="tl" style="margin-top:6px">Interpretation</div><div style="color:{B["muted"]}">{t["interpretation"]}</div>')
    st.markdown(f'<div class="tt">{" ".join(parts)}</div>', unsafe_allow_html=True)

NC = BALANCE_SHEET.loc[2025,"Cash & Equivalents"] + BALANCE_SHEET.loc[2025,"Short-Term Investments"] - BALANCE_SHEET.loc[2025,"Long-Term Debt"]
SH = MARKET_DATA["shares_outstanding"]
CR = INCOME_STATEMENT.loc[2025,"Total Revenue"]

with st.sidebar:
    st.markdown("## Palantir Technologies")
    st.markdown(f"NASDAQ: PLTR | {fmt_p(MARKET_DATA['current_price'])}")
    st.markdown("---")
    page = st.radio("Investigation", ["The Market Puzzle","What Palantir Does","The Bull Case",
        "The Bear Case","The Valuation Test","The Verdict"], label_visibility="collapsed")
    st.markdown("---")
    st.session_state["learn_mode"] = st.toggle("Show educational notes", value=False)
    st.markdown("---")
    st.markdown("**MBAN5570**"); st.caption("Accounting & Financial Analytics")
    st.caption("Sobey School of Business"); st.caption("Dr. Mohammad M. Rahaman")

# ═══════════════════════════════════════════════════════════════════════════
# PAGE 1: THE MARKET PUZZLE
# ═══════════════════════════════════════════════════════════════════════════
if page == "The Market Puzzle":
    ph("Why is Palantir priced like no other software company?",
       f"At ~${MARKET_DATA['market_cap_B']:.0f}B market cap and ~81× EV/Revenue, Palantir trades at roughly six times the valuation multiple of its closest peers.",
       "Either the market sees a structural advantage that justifies an extreme premium, or this is a sentiment-driven anomaly that will eventually correct.")
    peer = PEER_COMPARISON; pex = peer[peer["Ticker"] != "PLTR"]
    fig = go.Figure()
    fig.add_trace(go.Bar(x=peer["Ticker"], y=peer["EV/Revenue"],
        marker_color=[B["maroon"] if t == "PLTR" else B["navy"] for t in peer["Ticker"]],
        text=[f"{v:.1f}x" for v in peer["EV/Revenue"]], textposition="outside"))
    fig.add_hline(y=pex["EV/Revenue"].median(), line_dash="dash", line_color=B["gold"],
        annotation_text=f"Peer Median: {pex['EV/Revenue'].median():.1f}x")
    al(fig, "Enterprise Value / Revenue Multiple", 380)
    st.plotly_chart(fig, use_container_width=True)
    cap("This chart compares how expensive each company is relative to its revenue. Palantir's bar towers over every peer.",
        "EV/Revenue at 81× implies the market is pricing in years of sustained 40%+ growth with elite margins — a bet fewer than five companies at this scale have historically delivered.")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Share Price", fmt_p(MARKET_DATA["current_price"]))
    c2.metric("Market Cap", f"${MARKET_DATA['market_cap_B']:.0f}B")
    c3.metric("EV/Revenue", f"{peer[peer['Ticker']=='PLTR']['EV/Revenue'].iloc[0]:.1f}x", "vs 12x peer median")
    c4.metric("Consensus", ANALYST_DATA["consensus"], f"{ANALYST_DATA['num_analysts']} analysts")
    sr()
    st.markdown("## Where Wall Street Stands")
    cbox("Signal", f"{ANALYST_DATA['num_analysts']} analysts cover PLTR: {ANALYST_DATA['buy']} Buy, {ANALYST_DATA['hold']} Hold, {ANALYST_DATA['sell']} Sell. Mean target: {fmt_p(ANALYST_DATA['target_mean'])} — {((ANALYST_DATA['target_mean']/MARKET_DATA['current_price'])-1)*100:.0f}% from current.", "n")
    fig = go.Figure()
    fig.add_trace(go.Bar(x=["Buy","Hold","Sell"], y=[ANALYST_DATA["buy"], ANALYST_DATA["hold"], ANALYST_DATA["sell"]],
        marker_color=[C[1], C[2], C[3]], text=[ANALYST_DATA["buy"], ANALYST_DATA["hold"], ANALYST_DATA["sell"]], textposition="outside"))
    al(fig, "Analyst Recommendation Distribution", 280)
    st.plotly_chart(fig, use_container_width=True)
    with st.expander("Revenue Trajectory"):
        ist = INCOME_STATEMENT
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(go.Bar(x=ist.index, y=ist["Total Revenue"], name="Revenue ($M)", marker_color=C[0], opacity=0.85), secondary_y=False)
        fig.add_trace(go.Scatter(x=ist.index, y=ist["Adj Operating Margin%"], name="Adj Op Margin %",
            line=dict(color=C[1], width=3), mode="lines+markers"), secondary_y=True)
        fig.update_yaxes(title_text="Revenue ($M)", secondary_y=False)
        fig.update_yaxes(title_text="Adj Op Margin (%)", secondary_y=True)
        al(fig, "Revenue & Adjusted Operating Margin Trajectory")
        st.plotly_chart(fig, use_container_width=True)

# ═══════════════════════════════════════════════════════════════════════════
# PAGE 2: WHAT PALANTIR DOES
# ═══════════════════════════════════════════════════════════════════════════
elif page == "What Palantir Does":
    ph("What does Palantir sell, who pays for it, and how fast is each segment growing?",
       "Palantir operates three platforms — Gotham, Foundry, and AIP — serving government (~54%) and commercial (~46%) customers, with U.S. commercial revenue accelerating fastest at 137% YoY.",
       "Government revenue is a contract-backed floor. Commercial revenue is the growth option. The mix shift determines the company's risk and reward profile.")
    seg = REVENUE_SEGMENTS
    fig = go.Figure()
    fig.add_trace(go.Bar(x=seg.index, y=seg["Government Revenue"], name="Government", marker_color=C[0]))
    fig.add_trace(go.Bar(x=seg.index, y=seg["Commercial Revenue"], name="Commercial", marker_color=C[1]))
    fig.update_layout(barmode="stack")
    al(fig, "Revenue by Segment ($M)")
    st.plotly_chart(fig, use_container_width=True)
    cap("This chart shows where Palantir's revenue comes from and how the mix has shifted toward commercial customers.",
        "The government-to-commercial rebalancing is significant: commercial contracts carry higher growth but lack the multi-year budget-cycle durability of defense spending.")
    sr(); st.markdown("## Platform Ecosystem")
    c1, c2, c3 = st.columns(3)
    for col, (prod, desc) in zip([c1, c2, c3], COMPANY_INFO["products"].items()):
        with col: st.markdown(f"### {prod}"); st.markdown(desc)
    sr(); st.markdown("## U.S. Commercial Acceleration")
    cbox("Signal", "US Commercial grew from $156M (2020) to $1,370M (2025) — a 9× increase driven by AIP boot camp conversions.", "s")
    us_c = seg["US Commercial"]; gr = us_c.pct_change() * 100
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Bar(x=us_c.index, y=us_c.values, name="US Comm Revenue ($M)", marker_color=C[1]), secondary_y=False)
    fig.add_trace(go.Scatter(x=gr.index, y=gr.values, name="YoY Growth %", line=dict(color=C[2], width=3), mode="lines+markers"), secondary_y=True)
    al(fig, "U.S. Commercial Revenue — AIP-Driven Acceleration")
    st.plotly_chart(fig, use_container_width=True)
    with st.expander("FY2025 Revenue Breakdown"):
        fig = go.Figure(data=[go.Pie(labels=["US Government","US Commercial","Int'l Government","Int'l Commercial"],
            values=[seg.loc[2025,"US Government"], seg.loc[2025,"US Commercial"], seg.loc[2025,"Intl Government"], seg.loc[2025,"Intl Commercial"]],
            hole=0.5, marker_colors=C[:4], textinfo="label+percent+value", texttemplate="%{label}<br>$%{value}M<br>(%{percent})")])
        al(fig, "FY2025 Revenue Mix", 400); st.plotly_chart(fig, use_container_width=True)
    with st.expander("Global Presence"):
        gf = pd.DataFrame(GLOBAL_FOOTPRINT)
        ca = gf[gf["iso_alpha"].notna()].groupby("iso_alpha").agg(count=("entity","count"), country=("country","first"),
            uses=("use_case", lambda x: " | ".join(x.unique()))).reset_index()
        fig = go.Figure(data=go.Choropleth(locations=ca["iso_alpha"], z=ca["count"],
            text=ca.apply(lambda r: f"{r['country']}<br>{r['count']} deployments", axis=1),
            colorscale=[[0,"rgba(50,75,107,0.15)"],[0.5,"rgba(50,75,107,0.5)"],[1,"rgba(50,75,107,1)"]],
            colorbar_title="Deployments", hoverinfo="text"))
        fig.update_geos(bgcolor=B["bg"], landcolor=B["sfa"], oceancolor=B["bg"], showocean=True, coastlinecolor=B["border"], countrycolor=B["border"])
        fig.update_layout(height=420, margin=dict(l=0,r=0,t=20,b=0), paper_bgcolor=B["bg"], font=dict(family="Inter", color=B["text"]))
        st.plotly_chart(fig, use_container_width=True)
        dd = gf[["country","entity","use_case","segment","evidence","strategic_importance","notes"]]
        dd.columns = ["Country","Entity","Use Case","Segment","Evidence","Importance","Notes"]
        st.dataframe(dd.style.background_gradient(cmap="Blues", subset=["Importance"]), use_container_width=True, height=350)

# ═══════════════════════════════════════════════════════════════════════════
# PAGE 3: THE BULL CASE
# ═══════════════════════════════════════════════════════════════════════════
elif page == "The Bull Case":
    ph("Is Palantir's financial profile genuinely exceptional?",
       "By every standard growth-profitability metric — Rule of 40, FCF margin, gross margin, revenue acceleration at scale — Palantir ranks in the top 1% of enterprise software companies.",
       "Strong fundamentals are necessary but not sufficient for justifying an extreme valuation. This page tests whether the financial substance is real.")
    ist = INCOME_STATEMENT
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Bar(x=ist.index, y=ist["Total Revenue"], name="Revenue ($M)", marker_color=C[0], opacity=0.85), secondary_y=False)
    fig.add_trace(go.Scatter(x=ist.index, y=ist["Adj Operating Margin%"], name="Adj Op Margin %",
        line=dict(color=C[1], width=3), mode="lines+markers"), secondary_y=True)
    fig.update_yaxes(title_text="Revenue ($M)", secondary_y=False)
    fig.update_yaxes(title_text="Adj Op Margin (%)", secondary_y=True)
    al(fig, "Revenue & Adjusted Operating Margin (2020–2025)")
    st.plotly_chart(fig, use_container_width=True)
    cap("Palantir is growing faster each year while becoming dramatically more profitable — an unusual combination at $4.5B revenue scale.",
        "Revenue CAGR of 32.5% with accelerating growth at scale is atypical. Adjusted margin expansion from 7.6% to 50.6% reflects genuine operating leverage — but SBC exclusion flatters margins by ~25pp.")
    cbox("Signal", "Rule of 40 score: 107 (56% growth + 51% FCF margin). Top 1% of all software companies historically.", "s")
    cbox("Counterpoint", "Using GAAP operating margin instead of FCF margin yields ~81. Still strong — but the gap is $700M of stock-based compensation.", "c")
    sr()
    t1, t2, t3 = st.tabs(["Financial Statements", "Ratios & DuPont", "Growth Trends"])
    with t1:
        st.markdown("### Income Statement ($M)")
        dc = ["Total Revenue","Cost of Revenue","Gross Profit","R&D Expense","SGA Expense","SBC Expense","Operating Income","Net Income","EBITDA","Diluted EPS"]
        st.dataframe(ist[dc].style.format("{:,.0f}", subset=[c for c in dc if c!="Diluted EPS"]).format("{:.2f}", subset=["Diluted EPS"]).background_gradient(cmap="RdYlGn", axis=1), use_container_width=True)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=ist.index, y=(ist["Gross Profit"]/ist["Total Revenue"]*100), name="Gross Margin", line=dict(color=C[0], width=2.5), mode="lines+markers"))
        fig.add_trace(go.Scatter(x=ist.index, y=(ist["Operating Income"]/ist["Total Revenue"]*100), name="GAAP Op Margin", line=dict(color=C[1], width=2.5), mode="lines+markers"))
        fig.add_trace(go.Scatter(x=ist.index, y=(ist["Net Income"]/ist["Total Revenue"]*100), name="Net Margin", line=dict(color=C[2], width=2.5), mode="lines+markers"))
        fig.add_trace(go.Scatter(x=ist.index, y=ist["Adj Operating Margin%"], name="Adj Op Margin", line=dict(color=C[4], width=3, dash="dash"), mode="lines+markers"))
        al(fig, "Margin Evolution (2020–2025)"); st.plotly_chart(fig, use_container_width=True)
        with st.expander("Balance Sheet ($M)"):
            st.dataframe(BALANCE_SHEET.style.format("{:,.0f}").background_gradient(cmap="Blues", axis=1), use_container_width=True)
        with st.expander("Cash Flow & FCF Waterfall"):
            cfc = ["Operating Cash Flow","Capital Expenditure","Free Cash Flow","SBC","FCF Margin %"]
            st.dataframe(CASH_FLOW[cfc].style.format("{:,.0f}", subset=[c for c in cfc if c!="FCF Margin %"]).format("{:.1f}", subset=["FCF Margin %"]).background_gradient(cmap="RdYlGn", axis=1), use_container_width=True)
            cf25 = CASH_FLOW.loc[2025]
            fig = go.Figure(go.Waterfall(
                x=["Net Income","+D&A","+SBC","+WC Changes","=Operating CF","-CapEx","=Free Cash Flow"],
                y=[cf25["Net Income"],cf25["D&A"],cf25["SBC"],cf25["Changes in Working Capital"],0,cf25["Capital Expenditure"],0],
                measure=["relative","relative","relative","relative","total","relative","total"],
                connector={"line":{"color":"rgba(50,75,107,0.3)"}},
                increasing={"marker":{"color":C[1]}}, decreasing={"marker":{"color":C[3]}}, totals={"marker":{"color":C[0]}},
                text=[f"${v:,.0f}M" for v in [cf25["Net Income"],cf25["D&A"],cf25["SBC"],cf25["Changes in Working Capital"],cf25["Operating Cash Flow"],cf25["Capital Expenditure"],cf25["Free Cash Flow"]]],
                textposition="outside"))
            al(fig, "FY2025 Free Cash Flow Bridge ($M)", 420); st.plotly_chart(fig, use_container_width=True)
    with t2:
        tt("ratio_analysis")
        st.dataframe(KEY_RATIOS.style.format("{:.1f}").background_gradient(cmap="RdYlGn", axis=0), use_container_width=True)
        col1, col2 = st.columns(2)
        with col1:
            fig = go.Figure()
            for i, cn in enumerate(["Gross Margin (%)","Operating Margin (%)","Net Margin (%)","FCF Margin (%)"]):
                if cn in KEY_RATIOS.columns: fig.add_trace(go.Scatter(x=KEY_RATIOS.index, y=KEY_RATIOS[cn], name=cn, line=dict(color=C[i], width=2.5), mode="lines+markers"))
            al(fig, "Profitability Ratios"); st.plotly_chart(fig, use_container_width=True)
        with col2:
            fig = go.Figure()
            for i, cn in enumerate(["Current Ratio","Cash Ratio","Debt/Equity"]):
                if cn in KEY_RATIOS.columns: fig.add_trace(go.Scatter(x=KEY_RATIOS.index, y=KEY_RATIOS[cn], name=cn, line=dict(color=C[i], width=2.5), mode="lines+markers"))
            al(fig, "Liquidity & Solvency"); st.plotly_chart(fig, use_container_width=True)
        st.markdown("### DuPont Decomposition")
        tt("dupont_analysis"); st.markdown("**ROE = Net Profit Margin × Asset Turnover × Equity Multiplier**")
        st.dataframe(DUPONT.style.format("{:.4f}").background_gradient(cmap="RdYlGn", axis=0), use_container_width=True)
        fig = make_subplots(rows=1, cols=3, subplot_titles=("Net Profit Margin","Asset Turnover","Equity Multiplier"))
        fig.add_trace(go.Bar(x=DUPONT.index, y=DUPONT["Net Profit Margin"], marker_color=C[0], name="Margin"), row=1, col=1)
        fig.add_trace(go.Bar(x=DUPONT.index, y=DUPONT["Asset Turnover"], marker_color=C[1], name="Turnover"), row=1, col=2)
        fig.add_trace(go.Bar(x=DUPONT.index, y=DUPONT["Equity Multiplier"], marker_color=C[4], name="Leverage"), row=1, col=3)
        al(fig, "DuPont 3-Factor Decomposition", 380); st.plotly_chart(fig, use_container_width=True)
    with t3:
        st.markdown("### Horizontal Analysis — YoY % Change"); tt("horizontal_analysis")
        horiz = ist[["Total Revenue","Gross Profit","Operating Income","Net Income","EBITDA"]].pct_change() * 100
        horiz = horiz.dropna(how="all")
        st.dataframe(horiz.style.format("{:+.1f}%").background_gradient(cmap="RdYlGn", axis=1, vmin=-50, vmax=100), use_container_width=True)
        fig = go.Figure()
        for i, col in enumerate(["Total Revenue","Gross Profit","Net Income"]):
            fig.add_trace(go.Bar(x=horiz.index, y=horiz[col], name=col, marker_color=C[i]))
        fig.update_layout(barmode="group"); al(fig, "YoY Growth Rates (%)"); st.plotly_chart(fig, use_container_width=True)
        st.markdown("### Trend Index (2020 = 100)"); tt("trend_analysis")
        ist2 = ist[["Total Revenue","Gross Profit","Operating Income","Net Income"]].copy().sort_index()
        base = ist2.iloc[0].replace(0, np.nan); trend = ist2.div(base, axis=1) * 100
        fig = go.Figure()
        for i, col in enumerate(trend.columns):
            fig.add_trace(go.Scatter(x=trend.index, y=trend[col], name=col, line=dict(color=C[i], width=2.5), mode="lines+markers"))
        fig.add_hline(y=100, line_dash="dash", line_color="rgba(100,100,100,0.3)")
        al(fig, "Income Statement Trend Index (2020 = 100)"); st.plotly_chart(fig, use_container_width=True)
        r20 = ist.loc[2020,"Total Revenue"]; r25 = ist.loc[2025,"Total Revenue"]
        st.metric("5-Year Revenue CAGR (2020–2025)", f"{((r25/r20)**(1/5)-1)*100:.1f}%")

# ═══════════════════════════════════════════════════════════════════════════
# PAGE 4: THE BEAR CASE
# ═══════════════════════════════════════════════════════════════════════════
elif page == "The Bear Case":
    ph("What are the strongest arguments that Palantir is overvalued?",
       "The stock trades at 81× revenue, insiders have sold billions in shares, stock-based compensation remains 15.6% of revenue, and hyperscalers are investing aggressively in competing platforms.",
       "Every high-expectation stock looks strong on fundamentals. The question is whether the risks are priced in or priced out.")

    # Hero: SBC as % of revenue — the clearest non-obvious bear argument
    ist = INCOME_STATEMENT
    sbc_pct = ist["SBC Expense"] / ist["Total Revenue"] * 100
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=sbc_pct.index, y=sbc_pct.values, mode="lines+markers+text",
        text=[f"{v:.1f}%" for v in sbc_pct.values], textposition="top center",
        line=dict(color=B["neg"], width=3), fill="tozeroy",
        fillcolor="rgba(161,58,58,0.08)", name="SBC % of Revenue"))
    fig.add_hline(y=10, line_dash="dash", line_color=B["muted"],
        annotation_text="Mature-tech target: <10%")
    al(fig, "Stock-Based Compensation as % of Revenue", 350)
    st.plotly_chart(fig, use_container_width=True)
    cap("This chart tracks how much of Palantir's revenue goes to paying employees in stock. It has improved dramatically — but remains significant.",
        "SBC/Revenue at 15.6% remains above the mature-tech benchmark of <10%. The gap between GAAP operating margin (25%) and adjusted margin (51%) is almost entirely explained by this $700M annual charge.")

    cbox("Counterpoint", "SBC declined from 100% of revenue to 15.6% — a dramatic improvement. But $700M annually is $0.29 per share in real shareholder dilution.", "c")
    cbox("Signal", f"Analyst mean target: {fmt_p(ANALYST_DATA['target_mean'])} — {((ANALYST_DATA['target_mean']/MARKET_DATA['current_price'])-1)*100:.0f}% from current price. Consensus: Hold. Six of 22 analysts rate it Sell.", "n")
    cbox("Implication", "At 81× EV/Revenue, there is no margin for error. Any meaningful deceleration in growth, margin expansion, or AI sentiment would trigger disproportionate downside.", "c")

    sr()
    st.markdown("## Risk Register")
    risks = [
        ("Valuation Risk", "HIGH",
         "At ~81× EV/Revenue, this is among the most expensive large-cap software stocks ever. The valuation requires sustained exceptional execution for years. Any growth miss risks severe multiple compression."),
        ("Competition", "MEDIUM-HIGH",
         "Microsoft (Copilot + Azure), AWS (SageMaker + Bedrock), and Google (Vertex AI) are all investing heavily in enterprise AI. Hyperscalers have distribution and bundling advantages that Palantir lacks."),
        ("SBC Dilution", "MEDIUM",
         "$700M in FY2025 stock-based compensation dilutes shareholders at roughly 15.6% of revenue. Adjusted metrics exclude this — GAAP metrics do not. Both are valid lenses."),
        ("Customer Concentration", "MEDIUM",
         "Government contracts are lumpy and subject to political and budget cycles. Top-20 customers account for a significant share of revenue. Losing one major contract has outsized impact."),
        ("Insider Selling", "MEDIUM",
         "CEO Alex Karp has sold billions in shares through 10b5-1 plans. This is common for founders, but sustained selling can weigh on sentiment."),
        ("Macro & Rate Sensitivity", "MEDIUM",
         "Beta of 2.7 means PLTR falls materially harder than the market in a downturn. It is a long-duration growth asset highly sensitive to interest rate changes and AI sector repricing."),
        ("Execution Risk", "LOW-MEDIUM",
         "FY2026 guidance of 61% growth is aggressive at $4.5B scale. AIP must continue converting boot camps to production contracts. A stall in conversion rates would disappoint expectations quickly."),
    ]
    level_colors = {"HIGH": B["neg"], "MEDIUM-HIGH": "#C97A3A", "MEDIUM": B["gold"], "LOW-MEDIUM": B["pos"]}
    for name, level, desc in risks:
        with st.expander(f"**{name}** — {level}"):
            st.markdown(f'<div style="border-left: 3px solid {level_colors[level]}; padding-left:12px; color:{B["text"]}">{desc}</div>', unsafe_allow_html=True)

    sr()
    st.markdown("## AI Ecosystem Exposure")
    st.markdown(f"<span style='color:{B['muted']}; font-size:0.9rem'>Palantir benefits from the AI wave but is exposed to ecosystem-level sentiment shifts. Partnership upside and dependency risk coexist.</span>", unsafe_allow_html=True)

    # Partnership summary table
    p_rows = []
    for p in AI_ECOSYSTEM_DATA["partnerships"]:
        p_rows.append({"Partner": p["partner"], "Type": p["type"],
            "Dependency": p["dependency_level"], "Contagion Risk": p["contagion_risk"].split(" — ")[0]})
    st.dataframe(pd.DataFrame(p_rows).set_index("Partner"), use_container_width=True)

    with st.expander("Partnership detail"):
        for p in AI_ECOSYSTEM_DATA["partnerships"]:
            with st.container():
                c1, c2 = st.columns(2)
                with c1:
                    st.markdown(f"**{p['partner']}** ({p['type']}, {p['dependency_level']} dependency)")
                    st.markdown(f"✅ {p['upside']}")
                with c2:
                    st.markdown(f"⚠️ {p['downside']}")
                st.caption(f"Contagion risk: {p['contagion_risk']}")
                st.markdown("---")

    st.markdown("## Governance Note")
    cbox("Implication",
         "Palantir uses a multi-class share structure that concentrates voting control with founders. CEO Alex Karp's leadership style is unconventional by large-cap standards. These are not disqualifying factors, but they represent governance risk that institutional investors weigh carefully.",
         "n")

# ═══════════════════════════════════════════════════════════════════════════
# PAGE 5: THE VALUATION TEST
# ═══════════════════════════════════════════════════════════════════════════
elif page == "The Valuation Test":
    ph("What does Palantir need to deliver to justify its current stock price?",
       f"Under base-case assumptions (WACC 10%, TG 3%), our DCF implies a fair-value range of $80–$130 — suggesting the current price of {fmt_p(MARKET_DATA['current_price'])} already embeds years of exceptional execution.",
       "The sensitivity table — not any single price target — is the honest output of this model. Small changes in assumptions create large swings in implied value.")

    # Hero: DCF sensitivity heatmap
    wacc_range = [0.08, 0.09, 0.10, 0.11, 0.12, 0.13]
    tg_range = [0.02, 0.025, 0.03, 0.035, 0.04]
    sens = {}
    for w in wacc_range:
        row = {}
        for t in tg_range:
            gr = [max(0.55 * (0.82 ** i), t + 0.02) for i in range(7)]
            rev_s = CR; pv_sum = 0
            for i, g in enumerate(gr):
                rev_s *= (1 + g)
                m = 0.28 * min(1.0, 0.7 + 0.3 * (i / 7))
                pv_sum += (rev_s * m) / (1 + w) ** (i + 1)
            tv = (rev_s * 0.28 * (1 + t)) / (w - t)
            pvtv = tv / (1 + w) ** 7
            eq = (pv_sum + pvtv + NC) * 1e6 / SH
            row[f"TG {t:.1%}"] = round(eq, 2)
        sens[f"WACC {w:.0%}"] = row
    df_sens = pd.DataFrame(sens).T

    fig = go.Figure(data=go.Heatmap(
        z=df_sens.values, x=df_sens.columns, y=df_sens.index,
        colorscale=[[0, "#A13A3A"], [0.4, "#C7A86D"], [0.7, "#1F6B52"], [1, "#1A4F3A"]],
        text=[[f"${v:.0f}" for v in row] for row in df_sens.values],
        texttemplate="%{text}", colorbar_title="Implied Price",
        zmin=20, zmax=280))
    fig.add_annotation(x="TG 3.0%", y="WACC 10%", text="Base", showarrow=True,
        arrowhead=2, arrowcolor=B["navy"], font=dict(color=B["navy"], size=11))
    al(fig, "DCF Implied Share Price — WACC vs Terminal Growth Rate", 400)
    st.plotly_chart(fig, use_container_width=True)
    cap("Each cell shows what Palantir would be worth under a specific combination of discount rate (rows) and long-term growth assumption (columns). Small changes create large swings.",
        "Terminal value accounts for 60–70% of implied equity value. This makes the output highly sensitive to long-run assumptions that are inherently uncertain. The range IS the analytically honest answer.")
    cbox("Verdict",
         f"At WACC 10% / TG 3%, implied price ≈ $105. The current price of {fmt_p(MARKET_DATA['current_price'])} requires assumptions closer to WACC 9% / TG 4% — the optimistic corner of the matrix.",
         "v")
    cbox("Implication",
         f"At the peer-median EV/Revenue of ~12×, Palantir's implied price would be ~$25. The 6× premium represents the market's thesis that PLTR is categorically different from its peers. That thesis may be correct — but it must be earned every quarter.",
         "n")

    sr()
    t1, t2, t3, t4 = st.tabs(["Interactive DCF", "Peer Valuation", "Scenarios", "Monte Carlo"])

    with t1:
        st.markdown("### Discounted Cash Flow Model")
        col1, col2, col3, col4 = st.columns(4)
        with col1: wacc = st.slider("WACC (%)", 8.0, 15.0, 10.0, 0.5) / 100
        with col2: tg = st.slider("Terminal Growth (%)", 1.0, 5.0, 3.0, 0.5) / 100
        with col3: fcf_margin = st.slider("Steady-State FCF Margin (%)", 15.0, 40.0, 28.0, 1.0) / 100
        with col4: base_growth = st.slider("Y1 Revenue Growth (%)", 20.0, 70.0, 55.0, 5.0) / 100
        proj_years = 7
        growth_rates = [max(base_growth * (0.82 ** i), tg + 0.02) for i in range(proj_years)]
        projections = []; rev = CR
        for i, g in enumerate(growth_rates):
            rev = rev * (1 + g)
            m_i = fcf_margin * min(1.0, 0.7 + 0.3 * (i / proj_years))
            fcf = rev * m_i; pv = fcf / (1 + wacc) ** (i + 1)
            projections.append({"Year": f"FY{2026+i}", "Rev Growth": f"{g:.1%}", "Revenue ($M)": rev,
                "FCF Margin": f"{m_i:.1%}", "FCF ($M)": fcf, "PV Factor": 1/(1+wacc)**(i+1), "PV of FCF ($M)": pv})
        df_proj = pd.DataFrame(projections)
        st.dataframe(df_proj.style.format({"Revenue ($M)": "${:,.0f}", "FCF ($M)": "${:,.0f}",
            "PV of FCF ($M)": "${:,.0f}", "PV Factor": "{:.4f}"}), use_container_width=True)
        sum_pv = df_proj["PV of FCF ($M)"].sum()
        terminal_fcf = projections[-1]["FCF ($M)"] * (1 + tg)
        terminal_value = terminal_fcf / (wacc - tg)
        pv_tv = terminal_value / (1 + wacc) ** proj_years
        ev = sum_pv + pv_tv; equity_val = ev + NC
        implied_price = equity_val * 1e6 / SH
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Sum of PV(FCF)", f"${sum_pv:,.0f}M")
        c2.metric("PV(Terminal Value)", f"${pv_tv:,.0f}M")
        c3.metric("Enterprise Value", f"${ev:,.0f}M")
        c4.metric("Implied Share Price", fmt_p(implied_price),
            f"{'↑' if implied_price > MARKET_DATA['current_price'] else '↓'} vs {fmt_p(MARKET_DATA['current_price'])}")
        fig = go.Figure(data=[go.Pie(
            labels=["PV of Projected FCFs", "PV of Terminal Value"],
            values=[sum_pv, pv_tv], hole=0.55, marker_colors=[C[0], C[4]],
            textinfo="label+percent")])
        al(fig, "DCF Value Composition", 320); st.plotly_chart(fig, use_container_width=True)

    with t2:
        st.markdown("### Comparable Company Analysis")
        peer = PEER_COMPARISON
        st.dataframe(peer.set_index("Ticker").style.format({
            "Market Cap ($B)": "${:.1f}B", "Revenue TTM ($B)": "${:.2f}B",
            "Rev Growth (%)": "{:.1f}%", "Gross Margin (%)": "{:.1f}%",
            "Op Margin (%)": "{:.1f}%", "FCF Margin (%)": "{:.1f}%",
            "EV/Revenue": "{:.1f}x", "P/S": "{:.1f}x", "ROE (%)": "{:.1f}%", "Beta": "{:.2f}",
        }).background_gradient(cmap="RdYlGn", subset=["Rev Growth (%)","Op Margin (%)","FCF Margin (%)"]),
            use_container_width=True)
        pex = peer[peer["Ticker"] != "PLTR"]
        med_evr = pex["EV/Revenue"].median()
        implied_ev = CR * med_evr
        implied_p = (implied_ev * 1e6 + NC * 1e6) / SH
        st.metric(f"Implied Price at Peer Median EV/Rev ({med_evr:.1f}x)", fmt_p(implied_p),
            f"vs current {fmt_p(MARKET_DATA['current_price'])}")
        fig = make_subplots(rows=1, cols=3, subplot_titles=("EV/Revenue", "Revenue Growth %", "FCF Margin %"))
        for i, metric in enumerate(["EV/Revenue", "Rev Growth (%)", "FCF Margin (%)"]):
            colors_bar = [B["maroon"] if t == "PLTR" else C[0] for t in peer["Ticker"]]
            fig.add_trace(go.Bar(x=peer["Ticker"], y=peer[metric], marker_color=colors_bar, showlegend=False), row=1, col=i+1)
        al(fig, "PLTR vs Peers — Key Multiples", 380); st.plotly_chart(fig, use_container_width=True)

    with t3:
        st.markdown("### Bull / Base / Bear Scenarios")
        scenarios = {
            "Bull": {"growth": [0.65,0.55,0.45,0.38,0.32,0.28,0.24], "fcf_m": 0.32, "wacc": 0.09, "tg": 0.04},
            "Base": {"growth": [0.55,0.42,0.32,0.26,0.22,0.18,0.16], "fcf_m": 0.28, "wacc": 0.10, "tg": 0.03},
            "Bear": {"growth": [0.35,0.25,0.18,0.14,0.12,0.10,0.08], "fcf_m": 0.22, "wacc": 0.12, "tg": 0.02},
        }
        scen_results = {}
        for name, p in scenarios.items():
            rev_s = CR; pv_sum = 0
            for i, g in enumerate(p["growth"]):
                rev_s *= (1 + g)
                m = p["fcf_m"] * min(1.0, 0.7 + 0.3 * (i / 7))
                pv_sum += (rev_s * m) / (1 + p["wacc"]) ** (i + 1)
            tv = (rev_s * p["fcf_m"] * (1 + p["tg"])) / (p["wacc"] - p["tg"])
            pvtv = tv / (1 + p["wacc"]) ** 7
            eq = (pv_sum + pvtv + NC) * 1e6 / SH
            scen_results[name] = {"Implied Price": eq, "FY2032 Revenue ($B)": rev_s / 1000,
                "WACC": p["wacc"], "Terminal Growth": p["tg"], "FCF Margin": p["fcf_m"]}
        df_scen = pd.DataFrame(scen_results).T
        st.dataframe(df_scen.style.format({"Implied Price": "${:,.2f}", "FY2032 Revenue ($B)": "${:.1f}B",
            "WACC": "{:.0%}", "Terminal Growth": "{:.0%}", "FCF Margin": "{:.0%}"}), use_container_width=True)
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=["Bull Case", "Base Case", "Bear Case"],
            y=[scen_results["Bull"]["Implied Price"], scen_results["Base"]["Implied Price"], scen_results["Bear"]["Implied Price"]],
            marker_color=[C[1], C[0], C[3]], text=[f"${v:,.0f}" for v in [scen_results["Bull"]["Implied Price"], scen_results["Base"]["Implied Price"], scen_results["Bear"]["Implied Price"]]],
            textposition="outside"))
        fig.add_hline(y=MARKET_DATA["current_price"], line_dash="dash", line_color=B["maroon"],
            annotation_text=f"Current: {fmt_p(MARKET_DATA['current_price'])}")
        al(fig, "Implied Price by Scenario", 380); st.plotly_chart(fig, use_container_width=True)
        cap("This chart shows what Palantir could be worth under optimistic, moderate, and pessimistic assumptions — and where it trades today.",
            "The bull case ($180–280) requires sustained 50%+ growth. The bear case ($35–70) requires only normal SaaS deceleration and multiple convergence toward peers.")

    with t4:
        st.markdown("### Monte Carlo Simulation (GBM)")
        st.markdown(r"$dS = S \cdot \mu \cdot dt + S \cdot \sigma \cdot \varepsilon \cdot \sqrt{\Delta t}$")
        col1, col2, col3 = st.columns(3)
        with col1: n_sims = st.selectbox("Simulations", [500, 1000, 5000], index=1)
        with col2: n_days = st.selectbox("Trading Days", [63, 126, 252], index=2,
            format_func=lambda x: {63:"3 Months",126:"6 Months",252:"1 Year"}[x])
        with col3: vol_mult = st.slider("Volatility Multiplier", 0.5, 2.0, 1.0, 0.1)
        S0 = MARKET_DATA["current_price"]; mu = 0.65; sigma = 0.70 * vol_mult; dt = 1/252
        np.random.seed(42)
        paths = np.zeros((n_sims, n_days + 1)); paths[:, 0] = S0
        for t in range(1, n_days + 1):
            z = np.random.standard_normal(n_sims)
            paths[:, t] = paths[:, t-1] * np.exp((mu - 0.5*sigma**2)*dt + sigma*np.sqrt(dt)*z)
        final = paths[:, -1]
        c1, c2, c3, c4, c5 = st.columns(5)
        c1.metric("Current", fmt_p(S0)); c2.metric("Mean", fmt_p(np.mean(final)))
        c3.metric("Median", fmt_p(np.median(final))); c4.metric("5th Pctl", fmt_p(np.percentile(final, 5)))
        c5.metric("95th Pctl", fmt_p(np.percentile(final, 95)))
        fig = go.Figure()
        for lo, hi, op in [(5,95,0.08),(25,75,0.15)]:
            lo_l = np.percentile(paths, lo, axis=0); hi_l = np.percentile(paths, hi, axis=0)
            days_x = list(range(n_days+1))
            fig.add_trace(go.Scatter(x=days_x, y=hi_l, mode="lines", line=dict(width=0), showlegend=False))
            fig.add_trace(go.Scatter(x=days_x, y=lo_l, mode="lines", line=dict(width=0),
                fill="tonexty", fillcolor=f"rgba(50,75,107,{op})", name=f"{lo}th–{hi}th pctl"))
        fig.add_trace(go.Scatter(x=list(range(n_days+1)), y=np.median(paths, axis=0),
            mode="lines", line=dict(color=C[2], width=2.5), name="Median"))
        fig.add_hline(y=S0, line_dash="dash", line_color="rgba(100,100,100,0.4)")
        al(fig, f"Monte Carlo GBM — {n_sims} Simulations, {n_days} Trading Days", 420)
        st.plotly_chart(fig, use_container_width=True)
        fig2 = go.Figure()
        fig2.add_trace(go.Histogram(x=final, nbinsx=60, marker_color=C[0], opacity=0.75, name="Final Prices"))
        fig2.add_vline(x=S0, line_dash="dash", line_color=C[3])
        fig2.add_vline(x=np.mean(final), line_dash="dash", line_color=C[2])
        al(fig2, "Distribution of Simulated 1-Year Prices", 320); st.plotly_chart(fig2, use_container_width=True)
        prob_up = np.mean(final > S0) * 100
        st.markdown(f"**Probability above current price:** {prob_up:.1f}% | **Prob. of doubling:** {np.mean(final > S0*2)*100:.1f}% | **Prob. of halving:** {np.mean(final < S0*0.5)*100:.1f}%")

# ═══════════════════════════════════════════════════════════════════════════
# PAGE 6: THE VERDICT
# ═══════════════════════════════════════════════════════════════════════════
elif page == "The Verdict":
    ph("Is the premium justified?",
       "Palantir is a fundamentally strong business trading at a valuation that prices in years of sustained exceptional execution — making it a high-conviction position with a thin margin of safety.",
       "The purpose of equity research is not to produce a single number. It is to understand what you are betting on — and what would have to go wrong.")

    # Hero: scenario bar with current price line
    scenarios = {
        "Bull": {"growth": [0.65,0.55,0.45,0.38,0.32,0.28,0.24], "fcf_m": 0.32, "wacc": 0.09, "tg": 0.04},
        "Base": {"growth": [0.55,0.42,0.32,0.26,0.22,0.18,0.16], "fcf_m": 0.28, "wacc": 0.10, "tg": 0.03},
        "Bear": {"growth": [0.35,0.25,0.18,0.14,0.12,0.10,0.08], "fcf_m": 0.22, "wacc": 0.12, "tg": 0.02},
    }
    scen_prices = {}
    for name, p in scenarios.items():
        rev_s = CR; pv_sum = 0
        for i, g in enumerate(p["growth"]):
            rev_s *= (1 + g)
            m = p["fcf_m"] * min(1.0, 0.7 + 0.3 * (i / 7))
            pv_sum += (rev_s * m) / (1 + p["wacc"]) ** (i + 1)
        tv = (rev_s * p["fcf_m"] * (1 + p["tg"])) / (p["wacc"] - p["tg"])
        pvtv = tv / (1 + p["wacc"]) ** 7
        scen_prices[name] = (pv_sum + pvtv + NC) * 1e6 / SH

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=["Bear Case", "Base Case", "Bull Case"],
        y=[scen_prices["Bear"], scen_prices["Base"], scen_prices["Bull"]],
        marker_color=[C[3], C[0], C[1]],
        text=[f"${v:,.0f}" for v in [scen_prices["Bear"], scen_prices["Base"], scen_prices["Bull"]]],
        textposition="outside", width=0.5))
    fig.add_hline(y=MARKET_DATA["current_price"], line_dash="dash", line_color=B["maroon"], line_width=2,
        annotation_text=f"Current: {fmt_p(MARKET_DATA['current_price'])}",
        annotation_font_color=B["maroon"])
    al(fig, "Implied Share Price by Scenario vs. Current Market Price", 360)
    st.plotly_chart(fig, use_container_width=True)
    cap("This chart shows what Palantir could be worth under three sets of assumptions — and where it trades today.",
        "The bull case requires sustained 50%+ growth and ~32% FCF margins. The bear case requires only normal SaaS deceleration and peer-level multiple convergence. The current price sits above the base-case midpoint.")

    sr()
    st.markdown("## Our Assessment")
    st.markdown(f"""
<div style="background:{B['surface']};border:1px solid {B['border']};border-left:4px solid {B['maroon']};
border-radius:8px;padding:20px 24px;font-family:'Inter',sans-serif;color:{B['text']};line-height:1.75;font-size:0.93rem;">
Palantir Technologies is a company whose financial performance is genuinely unusual — 56% revenue growth
at $4.5B scale, 82% gross margins, 51% free cash flow margins, and a fortress balance sheet with $7.2B
in net cash and zero debt. By any standard measure of software-company quality, it ranks in the top percentile.
<br><br>
But financial strength and fair valuation are different questions. At ~81× EV/Revenue, the stock
requires investors to believe that this level of performance will persist for years — through competitive
pressure from hyperscalers, through potential government budget shifts, through inevitable growth
deceleration, and through an AI sentiment cycle that could compress multiples across the sector.
<br><br>
Our base-case DCF suggests a fair-value range of $80–$130. The current price of ~$153 implies the
market is already pricing the optimistic scenario. This does not mean the market is wrong.
It means the margin for error is thin.
<br><br>
<strong>Strong business. Contested stock. Priced for high expectations.</strong>
</div>
""", unsafe_allow_html=True)

    sr()
    tv1, tv2, tv3 = st.tabs(["How AI Was Used", "What We Accepted", "What We Discarded"])

    with tv1:
        st.markdown("### AI-Assisted Analysis — Section 2.B")
        st.markdown(f"<span style='color:{B['muted']};font-size:0.88rem'>Per MBAN5570 Section 2.B: How AI tools enhanced this research</span>", unsafe_allow_html=True)
        points = [
            ("Financial Data Aggregation", "AI rapidly aggregated Palantir's financial statements, key metrics, and segment data from SEC filings, earnings releases, and investor presentations into a structured dataset. A process that typically takes 4–6 hours was completed in minutes, freeing time for analytical interpretation."),
            ("Earnings Call Analysis", "AI analyzed earnings call transcripts to identify recurring themes: AIP adoption rates, boot-camp conversion metrics, government contract momentum, and shifts in management's forward guidance language. Key finding: management's transition from discussing customer count to emphasizing deal value — signaling product maturity."),
            ("Valuation Scenario Generation", "AI generated multiple DCF scenarios with varying assumptions and produced sensitivity tables. The Monte Carlo simulation runs 500–5,000 GBM paths to model price uncertainty probabilistically."),
            ("Pattern Recognition", "AI flagged the revenue acceleration curve (growth rate increasing, not decreasing, at scale), the SBC/revenue decline trajectory, and the divergence between GAAP and adjusted margins as key analytical threads."),
            ("Dashboard Development", "This Streamlit dashboard was built with AI assistance, creating interactive Plotly visualizations that allow dynamic what-if analysis impractical for a two-person team to build manually."),
        ]
        for title, body in points:
            with st.expander(f"**{title}**"): st.markdown(body)

    with tv2:
        st.markdown("### What We Accepted — Section 2.C")
        accepted = [
            "The **directional thesis** that Palantir is a legitimate AI platform leader, not merely a government contractor",
            "**Financial statement analysis** — ratio calculations, trend identification, DuPont decomposition are mathematically reliable",
            "The **Rule of 40+ assessment** — with score of 107, Palantir objectively meets elite software metrics",
            "**Balance sheet strength** — zero debt, $7.2B net cash is factual and strategically significant",
            "The **peer comparison framework** — while imperfect, it provides useful context for relative valuation",
            "**Monte Carlo outputs** as a probability distribution, not precise prediction",
        ]
        for item in accepted:
            st.markdown(f"✅ {item}")

    with tv3:
        st.markdown("### What We Discarded or Modified — Section 2.C")
        discarded = [
            ("Point-estimate DCF valuations", "We use sensitivity tables and scenario ranges. A single implied price creates false precision."),
            ("AI's implicit growth bias", "AI's base case projects 35–45% CAGR. We applied more conservative decay rates."),
            ("Adjusted metrics as primary", "We present GAAP and adjusted side by side. Neither alone tells the full story."),
            ("Simple peer average multiples", "The peer median implies ~$25. PLTR's premium exists for reasons worth examining — not dismissing."),
            ("Linear margin extrapolation", "Operating leverage has limits. We cap steady-state FCF margin assumptions at 28–32%."),
        ]
        for title, body in discarded:
            with st.expander(f"**{title}**"): st.markdown(body)

# ═══════════════════════════════════════════════════════════════════════════
sr()
st.markdown(f"""<div style="text-align:center; color:{B['muted']}; font-size:0.8rem; padding:20px 0;">
    MBAN5570 Accounting & Financial Analytics | Sobey School of Business, Saint Mary's University<br>
    Dr. Mohammad M. Rahaman | Equity Research Analytics — Palantir Technologies (PLTR)<br>
    <em>Data sources: SEC EDGAR, Palantir Investor Relations, Yahoo Finance</em>
</div>""", unsafe_allow_html=True)
