"""
PLTR Equity Research — Presentation Page (7-Step Merged Stepper)
"Beyond the Numbers" — mirrors 5-slide PPT deck.
"""
import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from pltr_data import (
    INCOME_STATEMENT, CASH_FLOW, MARKET_DATA, PEER_COMPARISON,
    REVENUE_SEGMENTS, BALANCE_SHEET,
)

STEP_TITLES = [
    "Mission Briefing",
    "The First Software Prime",
    "The Gotham Data Moat",
    "Apollo: What Nobody Else Has",
    "Apollo: Peer Evaluation & Risk",
    "Intelligence Infrastructure, Not SaaS",
    "The Digital Twin Flywheel",
]
TOTAL = 7


def render(B, C, sr, cbox, cap, ph, al):
    if "pres_step" not in st.session_state:
        st.session_state.pres_step = 0
    step = st.session_state.pres_step

    st.progress(step / (TOTAL - 1))
    st.markdown(f"""
    <div style="font-family:'Source Serif 4',Georgia,serif;font-size:1.5rem;color:{B['navy']};
         font-weight:700;margin:8px 0 4px 0;">{STEP_TITLES[step]}</div>
    <div style="font-family:Inter,sans-serif;font-size:0.78rem;color:{B['muted']};
         margin-bottom:12px;">Step {step + 1} of {TOTAL}</div>
    """, unsafe_allow_html=True)

    dot_cols = st.columns(TOTAL)
    for i, dc in enumerate(dot_cols):
        with dc:
            if st.button("●" if i == step else "○", key=f"dot_{i}",
                         help=STEP_TITLES[i], use_container_width=True):
                st.session_state.pres_step = i
                st.rerun()
    sr()

    [_s0, _s1, _s2, _s3, _s4, _s5, _s6][step](B, C, sr, cbox, cap, ph, al)

    sr()
    nl, _, nr = st.columns([1, 3, 1])
    with nl:
        if step > 0 and st.button("← Back", use_container_width=True, key="nav_back"):
            st.session_state.pres_step -= 1
            st.rerun()
    with nr:
        if step < TOTAL - 1:
            if st.button("Next →", use_container_width=True, key="nav_next"):
                st.session_state.pres_step += 1
                st.rerun()
        else:
            st.button("Begin Investigation →", use_container_width=True, key="nav_end")


# ═══════════════════════════════════════════════════════════════════════════
# STEP 0 — MISSION + BUY
# ═══════════════════════════════════════════════════════════════════════════
def _s0(B, C, sr, cbox, cap, ph, al):
    lc, rc = st.columns([3, 1])
    with lc:
        st.markdown(f"""
        <div style="background:{B['surface']};border-left:4px solid {B['maroon']};
             border-radius:8px;padding:24px 28px;">
          <div style="font-family:'Source Serif 4',Georgia,serif;color:{B['maroon']};
               font-size:1.3rem;font-weight:700;margin-bottom:4px;">BEYOND THE NUMBERS</div>
          <div style="font-family:Inter,sans-serif;color:{B['navy']};
               font-size:1.0rem;font-weight:600;margin-bottom:10px;">
            Why Palantir Is a National Security Necessity — Not Just a Software Stock</div>
          <div style="font-family:Inter,sans-serif;color:{B['text']};font-size:0.88rem;line-height:1.6;">
            Is Palantir priced like no other software company because it IS structurally different
            — or because the market currently believes it is?</div>
          <div style="margin-top:12px;display:flex;gap:8px;flex-wrap:wrap;">
            <span style="border:1px solid {B['gold']};color:{B['maroon']};border-radius:20px;
                  padding:3px 12px;font-family:Inter,sans-serif;font-size:0.75rem;">MBAN5570</span>
            <span style="border:1px solid {B['gold']};color:{B['maroon']};border-radius:20px;
                  padding:3px 12px;font-family:Inter,sans-serif;font-size:0.75rem;">Sobey School of Business</span>
            <span style="border:1px solid {B['gold']};color:{B['maroon']};border-radius:20px;
                  padding:3px 12px;font-family:Inter,sans-serif;font-size:0.75rem;">Dr. Mohammad M. Rahaman</span>
          </div>
        </div>""", unsafe_allow_html=True)
    with rc:
        st.markdown(f"""
        <div style="background:{B['pos']};border-radius:10px;padding:20px;text-align:center;margin-top:4px;">
          <div style="color:#FFF;font-size:2.2rem;font-weight:800;letter-spacing:0.08em;">BUY</div>
          <div style="color:#FFF;font-size:0.85rem;margin-top:4px;">PLTR · NYSE</div>
          <div style="color:rgba(255,255,255,0.7);font-size:0.75rem;margin-top:2px;">April 2026</div>
        </div>""", unsafe_allow_html=True)

    p1, p2, p3 = st.columns(3)
    for col, title, body in [
        (p1, "STRUCTURAL MOAT", "17 years of classified infrastructure no competitor can replicate"),
        (p2, "FINANCIAL INFLECTION", "Rule of 40: 107. FCF 51%. Zero debt. $7.2B net cash."),
        (p3, "CATEGORY CREATION", "Not SaaS — the non-optional decision layer of a $5T+ defense complex"),
    ]:
        with col:
            st.markdown(f"""
            <div style="background:{B['surface']};border-top:3px solid {B['maroon']};
                 border-radius:0 0 6px 6px;padding:14px 16px;margin-top:10px;">
              <div style="font-family:Inter,sans-serif;font-size:0.72rem;font-weight:700;
                   color:{B['maroon']};letter-spacing:0.06em;margin-bottom:4px;">{title}</div>
              <div style="font-family:Inter,sans-serif;font-size:0.82rem;color:{B['text']};
                   line-height:1.5;">{body}</div>
            </div>""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════
# STEP 1 — THE FIRST SOFTWARE PRIME
# ═══════════════════════════════════════════════════════════════════════════
def _s1(B, C, sr, cbox, cap, ph, al):
    lc, rc = st.columns(2)
    with lc:
        st.markdown(f"""
        <div style="font-family:Inter,sans-serif;">
          <div style="background:{B['border']};border-radius:6px;padding:12px 14px;margin-bottom:6px;">
            <div style="font-size:0.72rem;font-weight:700;color:{B['navy']};letter-spacing:0.05em;margin-bottom:3px;">THE BODY</div>
            <div style="font-size:0.85rem;color:{B['text']};">Lockheed, RTX, Northrop — build the platforms, missiles, satellites</div>
          </div>
          <div style="text-align:center;color:{B['muted']};font-size:0.8rem;padding:4px 0;">↓ data flows up · decisions flow down ↓</div>
          <div style="background:{B['maroon']};border-radius:6px;padding:12px 14px;margin-bottom:8px;">
            <div style="font-size:0.72rem;font-weight:700;color:{B['gold']};letter-spacing:0.05em;margin-bottom:3px;">THE BRAIN</div>
            <div style="font-size:0.85rem;color:#FFF;">Palantir integrates classified data into a single actionable picture — then supports the decision</div>
          </div>
          <div style="font-size:0.85rem;color:{B['navy']};font-weight:700;line-height:1.4;">
            The primes build the weapons. Palantir decides when, where, and how to use them.</div>
        </div>""", unsafe_allow_html=True)
    with rc:
        fig = go.Figure(go.Bar(
            x=["1996", "2010", "2024", "2035 (proj.)"],
            y=[1186, 2003, 2676, 5650],
            marker_color=[C[0], C[0], C[0], B["gold"]],
            text=["$1.2T", "$2.0T", "$2.7T", "$5.7T"], textposition="outside"))
        al(fig, "Global Military Spending ($B, 2023 prices)", 220)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown(f"""<div style="font-family:Inter,sans-serif;font-size:0.72rem;color:{B['muted']};margin-top:-8px;">
            Source: SIPRI (1996–2024); NATO Hague 5% Pledge (2035)</div>""", unsafe_allow_html=True)
        st.markdown(f"""<div style="font-family:Inter,sans-serif;font-size:0.8rem;color:{B['muted']};
            font-style:italic;margin-top:4px;">
            All NATO Allies met 2% GDP by March 2026. Hague pledge commits to 5% by 2035.
            Palantir is embedded in the institutions that control this capital.</div>""", unsafe_allow_html=True)

    cols = st.columns(5)
    primes = [("LMT", "Hardware", "~$71B rev", "~$105B cap"),
              ("GD", "Hardware", "~$48B rev", "~$65B cap"),
              ("NOC", "Hardware", "~$41B rev", "~$65B cap"),
              ("RTX", "Hardware", "~$80B rev", "~$145B cap"),
              ("PLTR", "Software Brain", "$4.5B rev", f"~${MARKET_DATA.get('market_cap_B',365):.0f}B cap")]
    for i, (tick, cat, rev, mcap) in enumerate(primes):
        is_pltr = i == 4
        bg = B["maroon"] if is_pltr else B["surface"]
        tc = "#FFF" if is_pltr else B["text"]
        with cols[i]:
            st.markdown(f"""<div style="background:{bg};border-radius:6px;padding:8px 10px;text-align:center;
                 font-family:Inter,sans-serif;">
              <div style="font-size:0.85rem;font-weight:700;color:{tc};">{tick}</div>
              <div style="font-size:0.7rem;color:{'rgba(255,255,255,0.7)' if is_pltr else B['muted']};">{cat}</div>
              <div style="font-size:0.72rem;color:{tc};margin-top:2px;">{rev}</div>
              <div style="font-size:0.72rem;color:{tc};">{mcap}</div>
            </div>""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════
# STEP 2 — THE GOTHAM DATA MOAT
# ═══════════════════════════════════════════════════════════════════════════
def _s2(B, C, sr, cbox, cap, ph, al):
    lc, rc = st.columns([2, 3])
    with lc:
        events = [
            ("2003", True, "Founded (CIA / In-Q-Tel seed)"),
            ("2008", True, "Gotham launched — first classified deployment"),
            ("2011", False, "FBI, NSA integration"),
            ("2014", False, "Europol counter-terrorism"),
            ("2016", False, "Foundry launched (commercial pivot)"),
            ("2019", True, "Google exits Maven → Palantir takes it"),
            ("2020", False, "IPO — first audited financials"),
            ("2022", True, "IL6 provisional authorization (DISA)"),
            ("2023", True, "AIP launched, TITAN contract begins"),
            ("2024", True, "$10B 10-year Army contract"),
            ("2025", False, "Market cap exceeds $443B"),
            ("2026", True, "NATO Maven Smart System operational"),
        ]
        lines = []
        for yr, major, desc in events:
            dot_color = B["maroon"] if major else B["muted"]
            weight = "700" if major else "400"
            lines.append(f"""<div style="display:flex;align-items:flex-start;margin-bottom:3px;">
              <div style="min-width:36px;font-size:0.72rem;font-weight:700;color:{B['maroon']};">{yr}</div>
              <div style="width:8px;height:8px;border-radius:50%;background:{dot_color};margin:3px 8px 0 0;flex-shrink:0;"></div>
              <div style="font-size:0.75rem;color:{B['text']};font-weight:{weight};line-height:1.3;">{desc}</div>
            </div>""")
        st.markdown(f"""<div style="font-family:Inter,sans-serif;border-left:2px solid {B['border']};
             padding-left:8px;">{''.join(lines)}</div>""", unsafe_allow_html=True)

    with rc:
        for border_c, title, body in [
            (B["navy"], "Active Theater Deployment",
             "DoD · FBI · NSA · CIA · Europol · Ukraine military · NATO Maven Smart System. Forward Deployed Engineers embed inside agencies for months."),
            (B["maroon"], "Classified Data Advantage",
             "Operational data at IL5/IL6 — highest access tier. No hyperscaler has this access. Google withdrew from Maven. AWS/Azure cannot deploy at IL6+."),
            (B["pos"], "Why It's Durable",
             "Switching cost = years of re-accreditation + rebuilding the classified ontology. 20 years of track record is institutional — not replicable by better code."),
        ]:
            st.markdown(f"""<div style="background:{B['surface']};border-left:4px solid {border_c};
                 border-radius:6px;padding:10px 14px;margin-bottom:8px;font-family:Inter,sans-serif;">
              <div style="font-size:0.78rem;font-weight:700;color:{B['navy']};margin-bottom:3px;">{title}</div>
              <div style="font-size:0.8rem;color:{B['text']};line-height:1.45;">{body}</div>
            </div>""", unsafe_allow_html=True)
        st.markdown(f"""<div style="font-size:0.72rem;color:{B['muted']};font-family:Inter,sans-serif;margin-top:4px;">
            Palantir IR · DISA authorization records · NATO procurement · Presentation research</div>""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════
# STEP 3 — APOLLO: WHAT NOBODY ELSE HAS
# ═══════════════════════════════════════════════════════════════════════════
def _s3(B, C, sr, cbox, cap, ph, al):
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Market Position", "1 of 1", delta="No qualified competitor")
    k2.metric("IL6-Auth CD Vendors", "< 6", delta="Apollo only CD-specific")
    k3.metric("Avg. Patch Speed", "3.5 min", delta="Log4j crisis benchmark")
    k4.metric("R&D Time Barrier", "5 years", delta="Palantir's documented build")

    lc, rc = st.columns([3, 2])
    with lc:
        st.markdown(f"""<div style="background:{B['surface']};border-left:4px solid {B['maroon']};
             border-radius:6px;padding:12px 14px;font-family:Inter,sans-serif;font-size:0.85rem;
             color:{B['text']};line-height:1.55;">
            Apollo is the continuous deployment infrastructure that allows Gotham, Foundry, and AIP to run
            anywhere simultaneously — commercial cloud, on-prem, air-gapped classified networks, battlefield
            edge devices — from a single control plane. Pull model. Cryptographically signed. FedRAMP High,
            IL5, IL6.</div>""", unsafe_allow_html=True)
    with rc:
        st.dataframe(pd.DataFrame([
            {"Capability": "Air-gapped", "Apollo": "✅", "AWS Out": "Partial", "Azure Arc": "Partial", "OpenShift": "Partial"},
            {"Capability": "IL5/IL6", "Apollo": "✅", "AWS Out": "❌", "Azure Arc": "❌", "OpenShift": "❌"},
            {"Capability": "FedRAMP High", "Apollo": "✅", "AWS Out": "✅", "Azure Arc": "✅", "OpenShift": "❌"},
            {"Capability": "Foundry-aware", "Apollo": "✅", "AWS Out": "❌", "Azure Arc": "❌", "OpenShift": "❌"},
            {"Capability": "Crypto sign", "Apollo": "✅", "AWS Out": "❌", "Azure Arc": "❌", "OpenShift": "Partial"},
            {"Capability": "Pull-model", "Apollo": "✅", "AWS Out": "❌", "Azure Arc": "❌", "OpenShift": "❌"},
        ]), use_container_width=True, hide_index=True)

    st.markdown(f"""<div style="font-family:Inter,sans-serif;font-size:0.88rem;color:{B['navy']};
         font-weight:700;margin-top:6px;">
        Apollo is what hyperscalers cannot copy quickly. They can match AIP features.
        They cannot replicate years of classified accreditation.</div>""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════
# STEPS 4–6 — PLACEHOLDERS (Pass 2 fills these)
# ═══════════════════════════════════════════════════════════════════════════
def _s4(B, C, sr, cbox, cap, ph, al):
    lc, rc = st.columns([3, 2])
    with lc:
        st.dataframe(pd.DataFrame([
            {"Capability": "Air-gapped", "Apollo": "✅ Native", "Spinnaker": "❌", "Argo CD": "❌", "Octopus": "⚠️", "Flux CD": "❌", "GH Actions": "❌"},
            {"Capability": "IL6 auth", "Apollo": "✅", "Spinnaker": "❌", "Argo CD": "❌", "Octopus": "❌", "Flux CD": "❌", "GH Actions": "❌"},
            {"Capability": "FedRAMP High", "Apollo": "✅", "Spinnaker": "❌", "Argo CD": "❌", "Octopus": "⚠️", "Flux CD": "❌", "GH Actions": "⚠️"},
            {"Capability": "Crypto signing", "Apollo": "✅ E2E", "Spinnaker": "⚠️", "Argo CD": "⚠️", "Octopus": "⚠️", "Flux CD": "⚠️", "GH Actions": "⚠️"},
            {"Capability": "Compliance orch", "Apollo": "✅", "Spinnaker": "⚠️", "Argo CD": "⚠️", "Octopus": "⚠️", "Flux CD": "❌", "GH Actions": "❌"},
            {"Capability": "Fleet obs", "Apollo": "✅", "Spinnaker": "⚠️", "Argo CD": "⚠️", "Octopus": "✅", "Flux CD": "❌", "GH Actions": "❌"},
        ]), use_container_width=True, hide_index=True)
        st.markdown(f"""<div style="font-family:Inter,sans-serif;font-size:0.85rem;color:{B['navy']};
             font-weight:700;margin-top:6px;">
            Clean sweep on all 4 classified requirements. No peer exceeds 2.</div>""", unsafe_allow_html=True)
    with rc:
        fig = go.Figure(go.Bar(
            x=[10, 28, 80, 85, 88, 92, 96],
            y=["Pricing", "Dev ecosystem", "Gov. distribution", "Replication cost", "Ops history", "Switching cost", "Accreditation"],
            orientation='h',
            marker_color=[B["neg"], B["neg"], B["gold"], B["pos"], B["pos"], B["pos"], B["pos"]],
            text=[10, 28, 80, 85, 88, 92, 96], textposition="inside"))
        fig.add_shape(type="line", x0=50, x1=50, y0=-0.5, y1=6.5, line=dict(color=B["muted"], width=1, dash="dash"))
        al(fig, "", 260)
        st.plotly_chart(fig, use_container_width=True)

    st.dataframe(pd.DataFrame([
        {"Risk": "Hyperscaler CD", "Severity": "MEDIUM", "Timeline": "5–7 yr"},
        {"Risk": "DoD budget disruption", "Severity": "MEDIUM", "Timeline": "Recurring"},
        {"Risk": "Open-source replication", "Severity": "LOW", "Timeline": "3–5 yr"},
        {"Risk": "Kustomize gap", "Severity": "LOW", "Timeline": "Near-term"},
        {"Risk": "IL6 revocation", "Severity": "HIGH ↓", "Timeline": "Tail risk"}
    ]).style.map(lambda x: f"color: {B['neg']}" if "HIGH" in str(x) else (f"color: {B['gold']}" if "MEDIUM" in str(x) else (f"color: {B['pos']}" if "LOW" in str(x) else "")), subset=["Severity"]), use_container_width=True, hide_index=True)

    st.markdown(f"""<div style="background:{B['navy']};color:#FFF;border-radius:6px;padding:10px;
         text-align:center;font-family:Inter,sans-serif;font-size:0.85rem;font-weight:700;margin-top:8px;">
        UNCONTESTED WITHIN ITS DEFINED MARKET</div>""", unsafe_allow_html=True)

def _s5(B, C, sr, cbox, cap, ph, al):
    c1, c2, c3 = st.columns(3)
    c1.markdown(f"""<div style="background:{B['surface']};border-left:4px solid {B['neg']};
         border-radius:6px;padding:8px 12px;font-family:Inter,sans-serif;font-size:0.78rem;">
         <strong style="color:{B['neg']}">WRONG</strong> · <span style="text-decoration:line-through;">SaaS peer group → 82× looks irrational</span></div>""", unsafe_allow_html=True)
    c2.markdown(f"""<div style="background:{B['surface']};border-left:4px solid {B['gold']};
         border-radius:6px;padding:8px 12px;font-family:Inter,sans-serif;font-size:0.78rem;">
         <strong style="color:{B['gold']}">CLOSER</strong> · Defense prime + software margins = no historical comp</div>""", unsafe_allow_html=True)
    c3.markdown(f"""<div style="background:{B['surface']};border-left:4px solid {B['pos']};
         border-radius:6px;padding:8px 12px;font-family:Inter,sans-serif;font-size:0.78rem;font-weight:700;">
         <strong style="color:{B['pos']}">CORRECT</strong> · Non-optional decision layer of a $5T+ defense complex</div>""", unsafe_allow_html=True)

    st.write("")
    lc, rc = st.columns([1, 1])
    with lc:
        growth = st.slider("Revenue growth (%/yr)", 10, 50, 30, 5, key="val_growth", help="How fast does Palantir grow each year?")
        margin = st.slider("Cash kept per dollar (%)", 20, 65, 50, 5, key="val_margin", help="How much profit does Palantir keep?")
        base_rev = 4475
        years = 5
        proj_rev = base_rev * (1 + growth/100) ** years
        proj_fcf = proj_rev * (margin / 100)
        terminal_ev = proj_fcf * 25
        shares = 2350
        implied = terminal_ev / shares
        current = MARKET_DATA.get('current_price', 152.77)
        upside = (implied - current) / current * 100
        up_color = B["pos"] if upside > 0 else B["neg"]

        st.markdown(f"""<div style="font-family:Inter,sans-serif;">
          <div style="color:{B['text']};font-size:0.9rem;">FY2030 Revenue → ${proj_rev:,.0f}M</div>
          <div style="color:{B['navy']};font-weight:700;font-size:1.1rem;margin:4px 0;">Implied Price → ${implied:,.0f}</div>
          <div style="color:{up_color};font-weight:700;font-size:0.9rem;">vs Today → {upside:+.0f}%</div>
          <div style="color:{B['text']};font-size:0.8rem;margin-top:12px;line-height:1.4;">
            If Palantir grows {growth}% per year and keeps {margin}¢ of every dollar,
            the stock is worth ~${implied:.0f} in 5 years.</div>
        </div>""", unsafe_allow_html=True)

    with rc:
        vol = st.slider("Uncertainty (%)", 10, 80, 40, 10, key="val_vol", help="Higher = wider range of possible outcomes")
        np.random.seed(42)
        n = 5000
        g = np.random.normal(growth/100, vol/100, (n, years))
        sims = base_rev * np.cumprod(1 + g, axis=1)[:, -1]
        sim_prices = (sims * (margin/100) * 25) / shares
        
        fig = go.Figure()
        fig.add_trace(go.Histogram(x=sim_prices, nbinsx=40, marker_color=C[0], opacity=0.7))
        fig.add_vline(x=current, line_dash="dash", line_color=B["neg"], annotation_text="Current")
        med = float(np.median(sim_prices))
        fig.add_vline(x=med, line_dash="dash", line_color=B["pos"], annotation_text="Median")
        al(fig, "", 220)
        fig.update_layout(xaxis_title="Implied Price ($)", yaxis_visible=False, showlegend=False, margin=dict(t=10, b=10, l=10, r=10))
        st.plotly_chart(fig, use_container_width=True)
        
        prob = (sim_prices > current).mean() * 100
        pc = B["pos"] if prob >= 60 else B["gold"] if prob >= 40 else B["neg"]
        st.markdown(f"""
        <div style="display:flex;justify-content:space-between;font-family:Inter,sans-serif;font-size:0.75rem;text-align:center;">
          <div><div style="color:{B['muted']};">Median</div><div style="font-weight:700;color:{B['text']};">${med:,.0f}</div></div>
          <div><div style="color:{B['muted']};">% > Current</div><div style="font-weight:700;color:{pc};">{prob:.0f}%</div></div>
          <div><div style="color:{B['muted']};">10th–90th</div><div style="font-weight:700;color:{B['text']};">${np.percentile(sim_prices,10):,.0f}–${np.percentile(sim_prices,90):,.0f}</div></div>
        </div>""", unsafe_allow_html=True)

    with st.expander("Peer multiple comparison"):
        st.dataframe(pd.DataFrame([
            {"Company": "Palantir", "Type": "Software Prime", "EV/Rev": "82×", "FCF Margin": "51%", "Rule of 40": "107"},
            {"Company": "Snowflake", "Type": "SaaS", "EV/Rev": "15×", "FCF Margin": "28%", "Rule of 40": "54"},
            {"Company": "Databricks", "Type": "SaaS (private)", "EV/Rev": "~18×", "FCF Margin": "N/A", "Rule of 40": "N/A"},
            {"Company": "C3.ai", "Type": "SaaS", "EV/Rev": "12×", "FCF Margin": "-15%", "Rule of 40": "7"},
            {"Company": "Booz Allen", "Type": "Defense", "EV/Rev": "2×", "FCF Margin": "8%", "Rule of 40": "21"},
            {"Company": "Leidos", "Type": "Defense", "EV/Rev": "1.5×", "FCF Margin": "7%", "Rule of 40": "16"},
        ]), use_container_width=True, hide_index=True)


def _s6(B, C, sr, cbox, cap, ph, al):
    lc, rc = st.columns([1, 1])
    with lc:
        st.markdown(f"""
        <div style="font-family:Inter,sans-serif;margin-bottom:16px;">
          <div style="background:{B['surface']};border-left:4px solid {B['navy']};border-radius:6px;padding:8px 12px;font-size:0.78rem;">
            <strong style="color:{B['maroon']}">①</strong> <strong style="color:{B['navy']}">DATA INTEGRATION</strong><br>
            <span style="color:{B['text']}">Foundry connects every source into a single ontology layer</span>
          </div>
          <div style="text-align:center;color:{B['muted']};font-size:0.8rem;padding:2px 0;">↓</div>
          <div style="background:{B['surface']};border-left:4px solid {B['navy']};border-radius:6px;padding:8px 12px;font-size:0.78rem;">
            <strong style="color:{B['maroon']}">②</strong> <strong style="color:{B['navy']}">DIGITAL TWIN CREATED</strong><br>
            <span style="color:{B['text']}">The ontology becomes the company's operational model</span>
          </div>
          <div style="text-align:center;color:{B['muted']};font-size:0.8rem;padding:2px 0;">↓</div>
          <div style="background:{B['surface']};border-left:4px solid {B['navy']};border-radius:6px;padding:8px 12px;font-size:0.78rem;">
            <strong style="color:{B['maroon']}">③</strong> <strong style="color:{B['navy']}">AIP DEPLOYED ON TOP</strong><br>
            <span style="color:{B['text']}">LLMs on customer's own data, behind their firewall</span>
          </div>
          <div style="text-align:center;color:{B['muted']};font-size:0.8rem;padding:2px 0;">↓</div>
          <div style="background:{B['surface']};border-left:4px solid {B['navy']};border-radius:6px;padding:8px 12px;font-size:0.78rem;">
            <strong style="color:{B['maroon']}">④</strong> <strong style="color:{B['navy']}">COMPOUNDING LOCK-IN</strong><br>
            <span style="color:{B['text']}">Replacement = rebuild ontology + retrain org + re-accredit AI</span>
          </div>
          <div style="text-align:center;color:{B['muted']};font-size:0.75rem;padding:2px 0;">↻ loops back to ①</div>
        </div>
        <div style="display:flex;gap:4px;flex-wrap:wrap;">
            <span style="background:{B.get('surface_alt', B.get('border', '#E0E0E0'))};color:{B['text']};border-radius:12px;padding:2px 8px;font-size:0.75rem;">Airbus — 4× A350</span>
            <span style="background:{B.get('surface_alt', B.get('border', '#E0E0E0'))};color:{B['text']};border-radius:12px;padding:2px 8px;font-size:0.75rem;">NHS England</span>
            <span style="background:{B.get('surface_alt', B.get('border', '#E0E0E0'))};color:{B['text']};border-radius:12px;padding:2px 8px;font-size:0.75rem;">Morgan Stanley</span>
            <span style="background:{B.get('surface_alt', B.get('border', '#E0E0E0'))};color:{B['text']};border-radius:12px;padding:2px 8px;font-size:0.75rem;">Chevron</span>
            <span style="background:{B.get('surface_alt', B.get('border', '#E0E0E0'))};color:{B['text']};border-radius:12px;padding:2px 8px;font-size:0.75rem;">Ferrari F1</span>
        </div>
        """, unsafe_allow_html=True)

    with rc:
        f1, f2 = st.columns(2)
        with f1:
            fig1 = go.Figure(go.Bar(x=["FY2023", "FY2024", "FY2025"], y=[70, 100, 137], marker_color=B["pos"], text=[70, 100, 137], textposition="inside"))
            al(fig1, "US Commercial Growth YoY (%)", 140)
            fig1.update_layout(margin=dict(t=25, b=0, l=0, r=0))
            st.plotly_chart(fig1, use_container_width=True)
        with f2:
            rev_years = ["2020","2021","2022","2023","2024","2025"]
            revenues = [1093, 1542, 1906, 2225, 2866, 4475]
            if "Total Revenue" in INCOME_STATEMENT:
                revenues[-len(INCOME_STATEMENT["Total Revenue"]):] = list(INCOME_STATEMENT["Total Revenue"].values)
            fig2 = go.Figure(go.Bar(x=rev_years, y=revenues, marker_color=C[0]))
            al(fig2, "Revenue ($M)", 140)
            fig2.update_layout(margin=dict(t=25, b=0, l=0, r=0))
            st.plotly_chart(fig2, use_container_width=True)
            
        st.markdown(f"""
        <div style="background:{B['pos']};border-radius:10px;padding:16px 24px;text-align:center;margin-top:12px;font-family:Inter,sans-serif;">
            <div style="color:#FFF;font-size:1.8rem;font-weight:800;letter-spacing:0.12em;">BUY</div>
            <div style="color:#FFF;font-size:0.85rem;margin:4px 0;">PALANTIR TECHNOLOGIES (PLTR)</div>
            <div style="color:rgba(255,255,255,0.9);font-size:0.78rem;">The moat is structural. The price requires conviction.</div>
        </div>
        """, unsafe_allow_html=True)
        
    st.write("")
    with st.expander("Investment thesis — 6 pillars"):
        pcols = st.columns(3)
        pillars = [
            ("01", "Structural Moat", "IL6-only CD platform. 20+ yr classified. Replacing PLTR = replacing 4 layers."),
            ("02", "Financial Inflection", "Rule of 40 = 107. FCF 51%. CAGR 32.6%. Zero debt, $7.2B cash."),
            ("03", "AI Tailwind", "AIP April 2023. US Commercial 137% YoY. Boot camp converts in weeks."),
            ("04", "Defense Supercycle", "$10B Army contract. NATO Maven. Global defense $2.7T→$5.6T by 2035."),
            ("05", "No True Peer", "All 5 structural criteria: zero competitors meet the bar."),
            ("06", "Risks Manageable", "Bear case temporally distant (5–7 yr). SBC declining as % rev. GAAP profitable.")
        ]
        for i, (num, ptitle, pbody) in enumerate(pillars):
            with pcols[i % 3]:
                st.markdown(f"""
                <div style="background:{B['surface']};border-top:3px solid {B['maroon']};border-radius:0 0 6px 6px;padding:10px;margin-bottom:8px;font-family:Inter,sans-serif;">
                    <span style="color:{B['maroon']};font-weight:700;font-size:1.1rem;margin-right:6px;">{num}</span>
                    <span style="color:{B['navy']};font-weight:700;font-size:0.85rem;">{ptitle}</span>
                    <div style="color:{B['text']};font-size:0.78rem;margin-top:4px;line-height:1.4;">{pbody}</div>
                </div>
                """, unsafe_allow_html=True)
                
    with st.expander("'One of One' structural evidence"):
        df = pd.DataFrame([
            {"#": 1, "Criterion": "IL5/IL6 + FedRAMP High across all platforms", "Palantir": "✅", "Nearest": "Leidos (partial)"},
            {"#": 2, "Criterion": "Cloud + air-gap from single control plane", "Palantir": "✅", "Nearest": "None confirmed"},
            {"#": 3, "Criterion": "Ontology-first digital twin", "Palantir": "✅", "Nearest": "Databricks (diff)"},
            {"#": 4, "Criterion": "LLM on classified data with audit trail", "Palantir": "✅", "Nearest": "None at IL5+"},
            {"#": 5, "Criterion": "20+ yr classified track record", "Palantir": "✅", "Nearest": "Booz Allen (services)"}
        ])
        st.dataframe(df.style.map(lambda x: f"background-color: {B['pos'][:7]}33" if "✅" in str(x) else "", subset=["Palantir"]), use_container_width=True, hide_index=True)
        
    st.markdown(f"""<div style="font-family:Inter,sans-serif;font-size:0.72rem;color:{B['muted']};text-align:center;margin-top:16px;">
        Data: SEC EDGAR · Palantir IR · DISA · NATO · U.S. Army | MBAN5570 · Sobey School of Business · Dr. Mohammad M. Rahaman
    </div>""", unsafe_allow_html=True)
