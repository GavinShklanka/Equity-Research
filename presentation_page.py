"""
PLTR Equity Research — Presentation Page (10-Step Stepper)
Standalone module. render() accepts B, C, and helpers from app.py.
"""
import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from pltr_data import (
    INCOME_STATEMENT, CASH_FLOW, MARKET_DATA, PEER_COMPARISON,
    REVENUE_SEGMENTS, BALANCE_SHEET,
)

STEP_TITLES = [
    "Mission Briefing",
    "From Hardware Primes to Software Brain",
    "The Four-Platform Stack",
    "Apollo: The Hidden Moat",
    "Apollo: Peer Evaluation Findings",
    "Apollo: Moat Scores & Risk Matrix",
    "The Competitive Landscape",
    "The Financial Evidence",
    "Where Palantir Sits in the Security Stack",
    "Is Palantir One of One?",
]
TOTAL = 10


def render(B, C, sr, cbox, cap, ph, al):
    if "pres_step" not in st.session_state:
        st.session_state.pres_step = 0
    step = st.session_state.pres_step

    # ── Progress bar ──
    st.progress(step / (TOTAL - 1))

    # ── Step title ──
    st.markdown(f"""
    <div style="font-family:'Source Serif 4',Georgia,serif;font-size:1.5rem;color:{B['navy']};
         font-weight:700;margin:8px 0 4px 0;">{STEP_TITLES[step]}</div>
    <div style="font-family:Inter,sans-serif;font-size:0.78rem;color:{B['muted']};
         margin-bottom:16px;">Step {step + 1} of {TOTAL}</div>
    """, unsafe_allow_html=True)

    # ── Dot indicators ──
    dot_cols = st.columns(TOTAL)
    for i, dc in enumerate(dot_cols):
        with dc:
            if st.button("●" if i == step else "○", key=f"dot_{i}",
                         help=STEP_TITLES[i], use_container_width=True):
                st.session_state.pres_step = i
                st.rerun()
    sr()

    # ── Step routing ──
    funcs = [_s0, _s1, _s2, _s3, _s4, _s5, _s6, _s7, _s8, _s9]
    funcs[step](B, C, sr, cbox, cap, ph, al)

    # ── Nav buttons ──
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
# STEP 0 — MISSION BRIEFING
# ═══════════════════════════════════════════════════════════════════════════
def _s0(B, C, sr, cbox, cap, ph, al):
    st.markdown(f"""
    <div style="background:{B['surface']};border-left:4px solid {B['maroon']};
         border-radius:8px;padding:28px 32px;margin-bottom:18px;">
      <div style="font-family:'Source Serif 4',Georgia,serif;color:{B['maroon']};
           font-size:1.4rem;font-weight:700;margin-bottom:6px;">
        MBAN5570 Equity Research Investigation</div>
      <div style="font-family:Inter,sans-serif;color:{B['navy']};
           font-size:1.05rem;font-weight:600;margin-bottom:14px;">
        Palantir Technologies — The Exception Case</div>
      <div style="font-family:Inter,sans-serif;color:{B['text']};
           font-size:0.92rem;line-height:1.8;">
        This investigation asks a single question: Is Palantir priced like no other software company
        because it IS structurally different — or because the market currently believes it is? Over six
        chapters, we examine the origins, platforms, financials, competitive landscape, and valuation of
        a company that has spent 17 years building infrastructure that most of its competitors cannot
        yet replicate.</div>
      <div style="margin-top:16px;display:flex;gap:10px;flex-wrap:wrap;">
        <span style="border:1px solid {B['gold']};color:{B['maroon']};border-radius:20px;
              padding:4px 14px;font-family:Inter,sans-serif;font-size:0.78rem;">MBAN5570</span>
        <span style="border:1px solid {B['gold']};color:{B['maroon']};border-radius:20px;
              padding:4px 14px;font-family:Inter,sans-serif;font-size:0.78rem;">Sobey School of Business</span>
        <span style="border:1px solid {B['gold']};color:{B['maroon']};border-radius:20px;
              padding:4px 14px;font-family:Inter,sans-serif;font-size:0.78rem;">Dr. Mohammad M. Rahaman</span>
      </div>
    </div>""", unsafe_allow_html=True)
    r1, r2 = st.columns(2)
    with r1:
        st.markdown(f"""<div style="font-family:Inter,sans-serif;font-size:0.8rem;color:{B['muted']};line-height:2.0;">
         1 · Mission Briefing<br> 2 · Primes to Software Brain<br> 3 · Four-Platform Stack<br>
         4 · Apollo: Hidden Moat<br> 5 · Apollo: Peer Evaluation</div>""", unsafe_allow_html=True)
    with r2:
        st.markdown(f"""<div style="font-family:Inter,sans-serif;font-size:0.8rem;color:{B['muted']};line-height:2.0;">
         6 · Moat Scores &amp; Risk<br> 7 · Competitive Landscape<br> 8 · Financial Evidence<br>
         9 · Security Stack<br>10 · One of One</div>""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════
# STEP 1 — FROM HARDWARE PRIMES TO SOFTWARE BRAIN
# ═══════════════════════════════════════════════════════════════════════════
def _s1(B, C, sr, cbox, cap, ph, al):
    cbox("Context",
         "For 70 years, defense meant hardware. Lockheed Martin built the F-35. General Dynamics built "
         "the Abrams. Northrop Grumman built the B-21 Raider. The primes won wars by building the machines. "
         "Palantir's thesis is that the next era of defense is won by the software that operates them — and "
         "that no company has spent more time building that software in classified environments than Palantir.", "n")
    try:
        pr = INCOME_STATEMENT.loc[2024, "Total Revenue"]
        prs = f"${pr/1000:.1f}B" if pr >= 1000 else f"${pr:.0f}M"
    except Exception:
        prs = "~$2.9B"
    pm = f"~${MARKET_DATA.get('market_cap_B', 365):.0f}B"
    data = pd.DataFrame([
        {"Company": "Lockheed Martin", "Category": "Hardware Prime", "Product": "F-35, missiles",
         "Rev FY2024": "~$71B", "Mkt Cap": "~$105B"},
        {"Company": "General Dynamics", "Category": "Hardware Prime", "Product": "Gulfstream, Abrams",
         "Rev FY2024": "~$48B", "Mkt Cap": "~$65B"},
        {"Company": "Northrop Grumman", "Category": "Hardware Prime", "Product": "B-21, ISR",
         "Rev FY2024": "~$41B", "Mkt Cap": "~$65B"},
        {"Company": "Raytheon (RTX)", "Category": "Hardware Prime", "Product": "Missiles, radar",
         "Rev FY2024": "~$80B", "Mkt Cap": "~$145B"},
        {"Company": "Palantir (PLTR)", "Category": "Software Brain",
         "Product": "Gotham/Foundry/AIP/Apollo", "Rev FY2024": prs, "Mkt Cap": pm},
    ])
    st.dataframe(data, use_container_width=True, hide_index=True)
    cap("Palantir's market cap has exceeded the combined value of the three largest defense primes "
        "despite 1/25th their revenue.",
        "The premium reflects a thesis: marginal defense value is shifting from platform manufacturing "
        "to AI-driven decision intelligence. If correct, Palantir is early. If wrong, the multiple compresses severely.")
    cbox("Signal",
         "In August 2025, Palantir's market cap exceeded $443B — surpassing Lockheed, Raytheon, and "
         "Northrop combined. The market has already voted. The question is whether the fundamentals catch up.", "s")


# ═══════════════════════════════════════════════════════════════════════════
# STEP 2 — THE FOUR-PLATFORM STACK
# ═══════════════════════════════════════════════════════════════════════════
def _s2(B, C, sr, cbox, cap, ph, al):
    st.markdown(f"""<div style="font-family:Inter,sans-serif;color:{B['text']};font-size:0.92rem;
        line-height:1.65;margin-bottom:16px;">
        Palantir does not sell a single product. It sells a vertically integrated software operating system
        for data-driven institutions. Understanding the four layers is prerequisite to evaluating the moat.
    </div>""", unsafe_allow_html=True)
    _pill = lambda c, t: f'<span style="border:1px solid {c};color:{c};border-radius:20px;padding:3px 12px;font-size:0.75rem;">{t}</span>'
    r1a, r1b = st.columns(2)
    with r1a:
        st.markdown(f"<div style='font-family:Source Serif 4,Georgia,serif;color:{B['navy']};font-size:1.1rem;font-weight:700;'>Gotham</div>", unsafe_allow_html=True)
        st.markdown(_pill(B["navy"], "Defense & Intelligence"), unsafe_allow_html=True)
        st.markdown("Launched 2008. Built with CIA analysts. Integrates classified data, detects patterns, "
                     "supports targeting. Used by DoD, FBI, NSA, CIA, Europol, Ukraine military. FDE model "
                     "embeds engineers inside agencies. IL5/IL6 accredited. The government moat.")
    with r1b:
        st.markdown(f"<div style='font-family:Source Serif 4,Georgia,serif;color:{B['navy']};font-size:1.1rem;font-weight:700;'>Foundry</div>", unsafe_allow_html=True)
        st.markdown(_pill(B["navy"], "Commercial Enterprise"), unsafe_allow_html=True)
        st.markdown("Launched 2016. Ontology layer connecting every data source, workflow, and decision. "
                     "Airbus quadrupled A350 production. Ferrari F1. NHS England. Morgan Stanley. "
                     "Replacement cost measured in years.")
    r2a, r2b = st.columns(2)
    with r2a:
        st.markdown(f"<div style='font-family:Source Serif 4,Georgia,serif;color:{B['navy']};font-size:1.1rem;font-weight:700;'>AIP</div>", unsafe_allow_html=True)
        st.markdown(_pill(B["gold"], "AI Orchestration"), unsafe_allow_html=True)
        st.markdown("Launched April 2023. LLMs on classified customer data behind their firewall with "
                     "audit trails. US Commercial grew 137% YoY. Boot camp converts pilots to production "
                     "in weeks. TITAN and Maven Smart System run on AIP.")
    with r2b:
        st.markdown(f"<div style='font-family:Source Serif 4,Georgia,serif;color:{B['maroon']};font-size:1.1rem;font-weight:700;'>Apollo</div>", unsafe_allow_html=True)
        st.markdown(_pill(B["maroon"], "The Hidden Moat"), unsafe_allow_html=True)
        st.markdown("Continuous deployment across commercial cloud, on-prem, air-gapped, classified, "
                     "battlefield edge — single control plane. Pull model. Cryptographically signed. "
                     "FedRAMP High, IL5, IL6.")
    cbox("Implication", "These are four layers of a single operating system. Replacing Palantir means "
         "replacing all four simultaneously.", "s")


# ═══════════════════════════════════════════════════════════════════════════
# STEP 3 — APOLLO: THE HIDDEN MOAT
# ═══════════════════════════════════════════════════════════════════════════
def _s3(B, C, sr, cbox, cap, ph, al):
    cbox("Why This Matters",
         "Most Palantir analysis focuses on Gotham's contracts and AIP's growth rate. Apollo is "
         "underanalyzed — and may be the most important competitive factor.", "n")
    lc, rc = st.columns([3, 2])
    with lc:
        st.dataframe(pd.DataFrame([
            {"Capability": "Air-gapped", "Apollo": "✅ Yes", "AWS Outposts": "Partial", "Azure Arc": "Partial", "OpenShift": "Partial"},
            {"Capability": "Classified (IL5/IL6)", "Apollo": "✅ Yes", "AWS Outposts": "No", "Azure Arc": "No", "OpenShift": "No"},
            {"Capability": "FedRAMP High", "Apollo": "✅ Yes", "AWS Outposts": "Yes", "Azure Arc": "Yes", "OpenShift": "No"},
            {"Capability": "Foundry-aware", "Apollo": "✅ Yes", "AWS Outposts": "No", "Azure Arc": "No", "OpenShift": "No"},
            {"Capability": "Crypto signing", "Apollo": "✅ Yes", "AWS Outposts": "No", "Azure Arc": "No", "OpenShift": "Partial"},
            {"Capability": "Pull-model", "Apollo": "✅ Yes", "AWS Outposts": "No", "Azure Arc": "No", "OpenShift": "No"},
            {"Capability": "Battlefield edge", "Apollo": "✅ Yes", "AWS Outposts": "No", "Azure Arc": "No", "OpenShift": "No"},
        ]), use_container_width=True, hide_index=True)
    with rc:
        st.markdown(f"""
        <div style="background:{B['sfa']};border-radius:10px;padding:20px 22px;font-family:Inter,sans-serif;">
          <div style="font-size:0.82rem;color:{B['muted']};margin-bottom:12px;font-weight:600;letter-spacing:0.04em;">APOLLO AT A GLANCE</div>
          <div style="font-size:0.85rem;color:{B['text']};line-height:2.2;">
            <strong>Accreditations</strong> → FedRAMP High | IL5 | IL6<br>
            <strong>Environments</strong> → Cloud + On-Prem + Air-Gap + Edge<br>
            <strong>Architecture</strong> → Pull Model<br>
            <strong>Security</strong> → Cryptographic signing<br>
            <strong>Speed</strong> → &lt; 90 min field deployment<br>
            <strong>Competition</strong> → 0 direct classified competitors
          </div>
        </div>""", unsafe_allow_html=True)
    cbox("Verdict", "Apollo is what hyperscalers cannot copy quickly. Microsoft and AWS can match AIP features. "
         "They cannot replicate years of classified accreditation and ontology-native architecture.", "v")


# ═══════════════════════════════════════════════════════════════════════════
# STEP 4 — APOLLO: PEER EVALUATION FINDINGS
# ═══════════════════════════════════════════════════════════════════════════
def _s4(B, C, sr, cbox, cap, ph, al):
    cbox("Research Note",
         "Peers selected by shared buyer and function — not category. Hyperscalers excluded: they "
         "provide the rack, Apollo decides what goes on it. Comparing Apollo to Azure is like "
         "comparing FedEx to an Amazon warehouse.", "n")
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Market Position — Classified CD", "1 of 1", delta="No qualified competitor")
    k2.metric("IL6-Authorized CD Vendors", "< 6", delta="Apollo only CD-specific")
    k3.metric("Avg. Patch Speed", "3.5 min", delta="All environments incl. air-gapped")
    k4.metric("R&D Barrier to Replicate", "5 years", delta="Palantir's documented build time")
    sr()
    st.dataframe(pd.DataFrame([
        {"Segment": "Cloud-native / SaaS", "Description": "Connected, standard compliance", "Apollo Position": "Peripheral"},
        {"Segment": "Enterprise Hybrid", "Description": "On-prem + cloud, some compliance", "Apollo Position": "Competitive but contested"},
        {"Segment": "Classified / Disconnected", "Description": "Air-gapped, DDIL, IL5/IL6", "Apollo Position": "DOMINANT — no competitor"},
    ]), use_container_width=True, hide_index=True)
    cbox("Segmentation Insight",
         "Evaluating Apollo against Argo CD or GitHub Actions head-to-head is a category error — "
         "equivalent to comparing Goldman Sachs prime brokerage to Robinhood because both involve equities.", "n")
    sr()
    st.dataframe(pd.DataFrame([
        {"Capability": "Air-gapped deployment", "Apollo": "✅ Native", "Spinnaker/Armory": "❌", "Argo CD": "❌", "Octopus Deploy": "⚠️ Limited", "Flux CD": "❌", "GitHub Actions": "❌"},
        {"Capability": "DoD IL6 authorization", "Apollo": "✅ Authorized", "Spinnaker/Armory": "❌", "Argo CD": "❌", "Octopus Deploy": "❌", "Flux CD": "❌", "GitHub Actions": "❌"},
        {"Capability": "FedRAMP High", "Apollo": "✅ Certified", "Spinnaker/Armory": "❌", "Argo CD": "❌", "Octopus Deploy": "⚠️ In progress", "Flux CD": "❌", "GitHub Actions": "⚠️ Moderate"},
        {"Capability": "Cryptographic signing", "Apollo": "✅ End-to-end", "Spinnaker/Armory": "⚠️ Plugin", "Argo CD": "⚠️ Cosign", "Octopus Deploy": "⚠️ Partial", "Flux CD": "⚠️ Cosign", "GitHub Actions": "⚠️ Attestation"},
        {"Capability": "Compliance orchestration", "Apollo": "✅ Native", "Spinnaker/Armory": "⚠️ Gates", "Argo CD": "⚠️ Add-on", "Octopus Deploy": "⚠️ Add-on", "Flux CD": "❌", "GitHub Actions": "❌"},
        {"Capability": "Multi-cloud (all types)", "Apollo": "✅ All", "Spinnaker/Armory": "✅ Public", "Argo CD": "⚠️ K8s-only", "Octopus Deploy": "✅ Hybrid", "Flux CD": "⚠️ K8s-only", "GitHub Actions": "⚠️ Cloud-native"},
        {"Capability": "Canary / blue-green", "Apollo": "✅ Built-in", "Spinnaker/Armory": "✅ Core", "Argo CD": "✅ Rollouts", "Octopus Deploy": "⚠️ Supported", "Flux CD": "⚠️ Flagger", "GitHub Actions": "⚠️ Manual"},
        {"Capability": "Fleet observability", "Apollo": "✅ Native", "Spinnaker/Armory": "⚠️ Per-cluster", "Argo CD": "⚠️ Per-cluster", "Octopus Deploy": "✅ Strong", "Flux CD": "❌", "GitHub Actions": "❌"},
        {"Capability": "Open-source", "Apollo": "❌ Commercial", "Spinnaker/Armory": "✅", "Argo CD": "✅", "Octopus Deploy": "❌ Commercial", "Flux CD": "✅", "GitHub Actions": "✅ Free tier"},
        {"Capability": "Pricing", "Apollo": "Enterprise contract", "Spinnaker/Armory": "Free / Armory", "Argo CD": "Free / Codefresh", "Octopus Deploy": "Per-target", "Flux CD": "Free", "GitHub Actions": "Per-minute"},
    ]), use_container_width=True, hide_index=True)
    cbox("Matrix Reading", "Apollo is the only product with a clean sweep across all four classified requirements: "
         "air-gapped, IL6, crypto signing, compliance orchestration. No peer achieves more than two.", "s")


# ═══════════════════════════════════════════════════════════════════════════
# STEP 5 — APOLLO: MOAT SCORES & RISK MATRIX
# ═══════════════════════════════════════════════════════════════════════════
def _s5(B, C, sr, cbox, cap, ph, al):
    dims = ["Pricing accessibility", "Developer ecosystem", "Gov. brand & distribution",
            "Technical replication cost", "Operational history advantage",
            "Switching cost — compliance", "Security accreditation barrier"]
    scores = [10, 28, 80, 85, 88, 92, 96]
    colors = [B["pos"] if s >= 80 else (B["gold"] if s >= 30 else B["neg"]) for s in scores]
    fig = go.Figure(go.Bar(y=dims, x=scores, orientation='h', marker_color=colors,
                           text=[str(s) for s in scores], textposition="outside"))
    fig.add_vline(x=50, line_dash="dash", line_color=B["muted"], line_width=1)
    fig.add_annotation(x=96, y="Security accreditation barrier", text="Classified CD defining barrier",
                       showarrow=True, arrowhead=2, ax=80, ay=-20, font=dict(size=10, color=B["navy"]))
    fig.add_annotation(x=10, y="Pricing accessibility", text="Intentional — not Apollo's market",
                       showarrow=True, arrowhead=2, ax=100, ay=20, font=dict(size=10, color=B["muted"]))
    al(fig, "Apollo Structural Moat Scoring (out of 100)", 380)
    st.plotly_chart(fig, use_container_width=True)
    cap("80–96 on every dimension that matters. Near-zero where it doesn't. A classified DoD customer cannot use community plugins.",
        "Moat asymmetry is key. Risk emerges only if Apollo expands into segments where low scores become relevant.")

    with st.expander("✅ Structural Advantages (Durable)"):
        st.markdown(f"""
**Only IL6-authorized CD platform.** Fewer than six vendors of any type hold DoD IL6 authorization.
No CD-specific peer holds this accreditation. It is not a product feature — it is a structural permission
granted by the DoD after years of demonstrated compliance, and cannot be bypassed by competing on product
quality alone.

**Native DDIL architecture.** Apollo's Remote Hub was specifically designed for Denied, Disrupted,
Intermittent, and Limited connectivity — the operating condition of deployed military systems. This was
the founding design requirement that triggered Apollo's construction.

**Compliance encoding creates compounding lock-in.** Every year a customer operates Apollo, more of their
compliance rules, downtime windows, CVE SLAs, and approval chains become encoded in the platform. This
institutional knowledge is not portable — it would need to be rebuilt from scratch on any replacement.

**Demonstrated crisis performance.** Apollo patched Log4j vulnerabilities across 200+ environments —
including air-gapped and classified — within hours of the exploit going public. No peer can claim
equivalent operational proof in classified environments.

**Five years of proprietary R&D as a hard time barrier.** Palantir's own documentation states that
building Apollo took five years longer than anticipated. Any competitor choosing to build a comparable
system faces the same timeline — with Apollo already deeply embedded throughout.
""")

    with st.expander("⚠️ Real Limitations (Genuine Constraints)"):
        st.markdown(f"""
**Enterprise-only sales model creates addressable market ceiling.** No free tier. No self-serve. No trial.
This structurally excludes the entire long tail of cloud-native startups and mid-market companies. Apollo
cannot address this market without fundamentally changing its go-to-market model.

**No Kustomize or cdk8s templating support.** For Kubernetes-native teams with GitOps-centric workflows,
this is a real gap that creates migration friction. If this gap widens, Apollo risks ceding the enterprise
hybrid segment to Octopus Deploy or Argo CD.

**Steep learning curve.** Apollo's sophistication is a liability for organizations without specialized
DevSecOps teams. For straightforward multi-cloud deployments, operational overhead is disproportionate
versus simpler alternatives.

**Revenue contribution not separately disclosed.** Palantir does not break out Apollo revenue from overall
platform revenue. This creates analytical opacity that limits investor confidence in Apollo as a standalone
product investment thesis.

**Hyperscaler encroachment risk on 5–7 year horizon.** Microsoft Azure Government holds IL6 cloud
infrastructure authorization. AWS GovCloud is investing heavily. Neither currently offers a CD orchestration
layer comparable to Apollo — but their resources mean this threat cannot be dismissed on long enough time
horizons.
""")

    with st.expander("⚪ Apparent Weaknesses That Are Actually Market Trade-offs"):
        st.markdown(f"""
**Not open-source** — In classified government environments, open-source software with unknown contributors
is a security liability, not an advantage. Apollo's proprietary status is a feature in this market, not a
limitation.

**No community ecosystem** — Community-contributed plugins cannot be used in accredited environments. The
absence of an open-source community is irrelevant to Apollo's core customers.

**'Overkill for simple deployments'** — Apollo is expensive and complex for single-cloud SaaS. This is
correct and intentional. Evaluating Apollo against that use case is like faulting a submarine for being
slow on a highway.
""")

    sr()
    risk = pd.DataFrame([
        {"Risk": "Hyperscaler CD competition", "Severity": "MEDIUM", "Timeline": "5–7 yr",
         "Description": "AWS/Azure building classified infra, no CD product yet. Accreditation alone = 3–5 yr."},
        {"Risk": "DoD budget disruption", "Severity": "MEDIUM", "Timeline": "Recurring",
         "Description": "CRs can delay. Cancellation unlikely given embedding depth."},
        {"Risk": "Open-source replication", "Severity": "LOW", "Timeline": "3–5 yr",
         "Description": "Still needs IL6 accreditation independently."},
        {"Risk": "Kustomize / GitOps gap", "Severity": "LOW", "Timeline": "Near-term",
         "Description": "Risks enterprise hybrid segment if unaddressed."},
        {"Risk": "IL6 authorization revocation", "Severity": "HIGH (low prob)", "Timeline": "Tail risk",
         "Description": "Would require major security incident. 20-year track record."},
    ])
    def _sc(v):
        if "HIGH" in str(v): return f"color: {B['neg']}"
        if "MEDIUM" in str(v): return f"color: {B['gold']}"
        if "LOW" in str(v): return f"color: {B['pos']}"
        return ""
    st.dataframe(risk.style.map(_sc, subset=["Severity"]), use_container_width=True, hide_index=True)
    sr()
    st.markdown(f"""
    <div style="background:{B['navy']};color:#FFF;border-radius:8px;padding:24px 28px;margin-bottom:14px;">
      <div style="color:{B['gold']};font-family:monospace;font-variant:small-caps;font-size:0.85rem;
           font-weight:700;margin-bottom:8px;letter-spacing:0.04em;">
        PRODUCT EVALUATION FINDING: UNCONTESTED WITHIN ITS DEFINED MARKET</div>
      <div style="font-family:Inter,sans-serif;font-size:0.9rem;line-height:1.75;">
        The peer evaluation finds Apollo holds an effectively uncontested position within the classified,
        air-gapped, and disconnected CD market. Grounded in three structural barriers unique to Apollo:
        DoD IL6 authorization (one of fewer than six holders across any software category), native DDIL
        architecture built over five years of proprietary R&amp;D, and 20 years of operational history in
        national security contexts. No peer holds all three. The bear case is real but temporally distant.</div>
    </div>""", unsafe_allow_html=True)
    cbox("Investor Caveat", "This evaluates Apollo as a product, not PLTR as a stock. A strong product in a narrow "
         "market is not automatically a strong investment at any price.", "c")


# ═══════════════════════════════════════════════════════════════════════════
# STEP 6 — THE COMPETITIVE LANDSCAPE
# ═══════════════════════════════════════════════════════════════════════════
def _s6(B, C, sr, cbox, cap, ph, al):
    cbox("Context", "Palantir has different competitors on every layer of its stack. No single company competes "
         "across all four platforms simultaneously. That is not an accident — it is the design.", "n")
    with st.expander("Government & Defense (Gotham competitors)"):
        st.dataframe(pd.DataFrame([
            {"Company": "Booz Allen Hamilton", "Overlap": "High — C4ISR", "Accreditation": "IL5/IL6", "Key Difference": "Services-led, not pure software"},
            {"Company": "Leidos Holdings", "Overlap": "High — DoD AI, ISR", "Accreditation": "IL5", "Key Difference": "Less ontology depth"},
            {"Company": "CACI International", "Overlap": "Medium — intel", "Accreditation": "IL4", "Key Difference": "Narrower scope"},
            {"Company": "Northrop Grumman", "Overlap": "Medium — C2, ISR", "Accreditation": "IL5/IL6", "Key Difference": "Hardware-led"},
            {"Company": "DataWalk", "Overlap": "Medium — investigative", "Accreditation": "Lower", "Key Difference": "No classified deployment"},
            {"Company": "Babel Street", "Overlap": "Low-Med — OSINT", "Accreditation": "Commercial", "Key Difference": "No government depth"},
        ]), use_container_width=True, hide_index=True)
        cbox("Signal", "None combine Palantir's accreditation with its software-first architecture and FDE model.", "s")
    with st.expander("Enterprise Data (Foundry competitors)"):
        st.dataframe(pd.DataFrame([
            {"Company": "Microsoft Fabric + Azure OpenAI", "Overlap": "High", "Strength": "Distribution, bundling", "Palantir Advantage": "Ontology depth, classified access"},
            {"Company": "Databricks", "Overlap": "High", "Strength": "Developer adoption, open source", "Palantir Advantage": "Operational workflows"},
            {"Company": "Snowflake", "Overlap": "Medium", "Strength": "Data economics", "Palantir Advantage": "Decision layer on top"},
            {"Company": "C3.ai", "Overlap": "Medium", "Strength": "Enterprise AI branding", "Palantir Advantage": "More comprehensive"},
            {"Company": "SAP (Palantir partner)", "Overlap": "Low-Medium", "Strength": "ERP integration", "Palantir Advantage": "AI layer above SAP"},
        ]), use_container_width=True, hide_index=True)
        cbox("Counterpoint", "Microsoft Fabric + Azure OpenAI is the most credible Foundry threat. Distribution power "
             "could commoditize the commercial data layer.", "c")
    with st.expander("AI Platform (AIP competitors)"):
        st.dataframe(pd.DataFrame([
            {"Company": "Microsoft Copilot/Azure OpenAI", "Overlap": "High", "Classified Deploy": "No (IL5+)", "Bootcamp Equiv": "No"},
            {"Company": "Google Vertex AI", "Overlap": "High", "Classified Deploy": "No (IL5+)", "Bootcamp Equiv": "No"},
            {"Company": "AWS Bedrock", "Overlap": "High", "Classified Deploy": "Partial (GovCloud)", "Bootcamp Equiv": "No"},
            {"Company": "Anduril Industries", "Overlap": "Medium (defense)", "Classified Deploy": "Yes", "Bootcamp Equiv": "No"},
            {"Company": "Scale AI", "Overlap": "Low-Medium", "Classified Deploy": "Limited", "Bootcamp Equiv": "No"},
        ]), use_container_width=True, hide_index=True)
        cbox("Signal", "Google withdrew from Project Maven in 2019. Palantir took the contract and never left. "
             "That institutional trust is not purchasable.", "s")
    with st.expander("Deployment Infrastructure (Apollo — Correct Peer Group)"):
        st.markdown(f"""<div style="font-family:Inter,sans-serif;color:{B['text']};font-size:0.88rem;line-height:1.6;margin-bottom:12px;">
            <strong>Why hyperscalers are NOT the peer group:</strong> Azure Government, AWS GovCloud, and Oracle Cloud
            Isolated Region are infrastructure providers — compute, storage, networking. Apollo is the deployment
            orchestration layer on top. Azure provides the rack. Apollo decides what goes on it and when.</div>""", unsafe_allow_html=True)
        st.dataframe(pd.DataFrame([
            {"Tool": "Apollo", "Air-Gap": "✅ Native", "IL6": "✅ Yes", "Crypto": "✅ Standard", "Compliance": "✅ Native", "Fleet Obs": "✅ Native"},
            {"Tool": "Spinnaker", "Air-Gap": "❌", "IL6": "❌", "Crypto": "⚠️ Plugin", "Compliance": "⚠️ Gates", "Fleet Obs": "⚠️ Per-cluster"},
            {"Tool": "Argo CD", "Air-Gap": "❌", "IL6": "❌", "Crypto": "⚠️ Cosign", "Compliance": "⚠️ Add-on", "Fleet Obs": "⚠️ Per-cluster"},
            {"Tool": "Octopus", "Air-Gap": "⚠️ Limited", "IL6": "❌", "Crypto": "⚠️ Partial", "Compliance": "⚠️ Add-on", "Fleet Obs": "✅ Strong"},
            {"Tool": "Flux CD", "Air-Gap": "❌", "IL6": "❌", "Crypto": "⚠️ Cosign", "Compliance": "❌", "Fleet Obs": "❌"},
            {"Tool": "GitHub Actions", "Air-Gap": "❌", "IL6": "❌", "Crypto": "⚠️ Attest", "Compliance": "❌", "Fleet Obs": "❌"},
        ]), use_container_width=True, hide_index=True)
        cbox("Legitimate Omission", "Second Front Systems' Game Warden — FedRAMP-authorized DevSecOps — is the most legitimate "
             "peer omission. It operates as a compliance wrapper rather than full autonomous deployment orchestration.", "n")


# ═══════════════════════════════════════════════════════════════════════════
# STEP 7 — THE FINANCIAL EVIDENCE
# ═══════════════════════════════════════════════════════════════════════════
def _s7(B, C, sr, cbox, cap, ph, al):
    st.markdown(f"""<div style="font-family:Inter,sans-serif;color:{B['muted']};font-size:0.88rem;margin-bottom:14px;">
        FY2025 reported results. All data from Palantir IR and SEC filings.</div>""", unsafe_allow_html=True)
    ist, cf, seg = INCOME_STATEMENT, CASH_FLOW, REVENUE_SEGMENTS
    rev25 = ist.loc[2025, "Total Revenue"]
    rev20 = ist.loc[2020, "Total Revenue"]
    cagr = ((rev25 / rev20) ** (1/5) - 1) * 100
    usc25, usc24 = seg.loc[2025, "US Commercial"], seg.loc[2024, "US Commercial"]
    usg = ((usc25 / usc24) - 1) * 100
    fcfm = cf.loc[2025, "FCF Margin %"]
    gm = round(ist.loc[2025, "Gross Profit"] / ist.loc[2025, "Total Revenue"] * 100, 1)
    nc = BALANCE_SHEET.loc[2025, "Cash & Equivalents"] + BALANCE_SHEET.loc[2025, "Short-Term Investments"] - BALANCE_SHEET.loc[2025, "Long-Term Debt"]
    peer = PEER_COMPARISON
    pex = peer[peer["Ticker"] != "PLTR"]
    pevr = peer[peer["Ticker"] == "PLTR"]["EV/Revenue"].iloc[0]
    pmed = pex["EV/Revenue"].median()
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Revenue FY2025", f"${rev25/1000:.1f}B")
    m2.metric("Revenue CAGR 2020–2025", f"{cagr:.1f}%")
    m3.metric("US Commercial Growth YoY", f"{usg:.0f}%")
    m4.metric("Rule of 40", "107")
    m5, m6, m7, m8 = st.columns(4)
    m5.metric("FCF Margin", f"{fcfm:.1f}%")
    m6.metric("Gross Margin", f"{gm:.1f}%")
    m7.metric("Net Cash", f"${nc/1000:.1f}B")
    m8.metric("EV/Revenue vs Peers", f"{pevr:.0f}x vs {pmed:.0f}x")
    c1, c2 = st.columns(2)
    with c1:
        fig = go.Figure(go.Bar(x=ist.index.tolist(), y=ist["Total Revenue"].tolist(),
              marker_color=C[0], text=[f"${v:,.0f}" for v in ist["Total Revenue"]], textposition="outside"))
        al(fig, "Revenue ($M) — 2020–2025", 280)
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        fp = cf["FCF Margin %"].dropna()
        fig2 = go.Figure(go.Scatter(x=fp.index.tolist(), y=fp.values.tolist(),
               mode="lines+markers", line=dict(color=C[1], width=3)))
        al(fig2, "FCF Margin (%) — 2021–2025", 280)
        st.plotly_chart(fig2, use_container_width=True)
    cap("Simultaneously accelerating revenue growth AND expanding margins at $4.5B scale.",
        "Revenue CAGR of 32.5% with FCF margin expanding from negative to 51% = operating leverage at scale. The question is duration.")
    cbox("Bull", "Rule of 40: 107. FCF: 51%. Zero debt. $7.2B cash. US Commercial 137% YoY. "
         "10-year $10B Army contract. NATO Maven Smart System.", "s")
    cbox("Bear", "81x EV/Rev vs 12x peer median. SBC: $700M (15.6%). GAAP margin 25% vs adjusted 51%. "
         "Pre-IPO losses: $623M (2018), $576M (2019). The price requires years of persistence.", "c")


# ═══════════════════════════════════════════════════════════════════════════
# STEP 8 — WHERE PALANTIR SITS IN THE SECURITY STACK
# ═══════════════════════════════════════════════════════════════════════════
def _s8(B, C, sr, cbox, cap, ph, al):
    cbox("Context", "Palantir is not a cybersecurity company. CrowdStrike, Palo Alto, Fortinet own threat "
         "detection. Palantir operates above — the intelligence layer that makes their output actionable at scale.", "n")
    st.markdown(f"""
    <div style="max-width:600px;margin:16px auto;font-family:Inter,sans-serif;">
      <div style="text-align:center;font-size:0.78rem;color:{B['muted']};margin-bottom:6px;">decisions flow down ↓</div>
      <div style="background:{B['maroon']};color:#FFF;padding:14px;text-align:center;border-radius:8px 8px 0 0;font-weight:600;font-size:0.9rem;">
        Decision &amp; Intelligence — PALANTIR</div>
      <div style="background:{B['navy']};color:#FFF;padding:12px;text-align:center;font-size:0.85rem;">
        Data Integration &amp; Ontology — FOUNDRY</div>
      <div style="background:{B['sfa']};color:{B['text']};padding:12px;text-align:center;font-size:0.85rem;">
        Threat Detection — CrowdStrike | Palo Alto | Fortinet</div>
      <div style="background:{B['border']};color:{B['text']};padding:12px;text-align:center;border-radius:0 0 8px 8px;font-size:0.85rem;">
        Infrastructure &amp; Network — Cloud / Hardware</div>
      <div style="text-align:center;font-size:0.78rem;color:{B['muted']};margin-top:6px;">data flows up ↑</div>
    </div>""", unsafe_allow_html=True)
    st.dataframe(pd.DataFrame([
        {"Company": "CrowdStrike", "Category": "EDR", "vs Palantir": "Different layer — feeds data TO Palantir"},
        {"Company": "Palo Alto", "Category": "Network security", "vs Palantir": "Different layer — budget not function"},
        {"Company": "Fortinet", "Category": "Firewall", "vs Palantir": "Different layer"},
        {"Company": "MS Sentinel", "Category": "SIEM/SOAR", "vs Palantir": "Partial overlap — Microsoft bundle threat"},
        {"Company": "Splunk (Cisco)", "Category": "SIEM/analytics", "vs Palantir": "Medium overlap — enterprise data"},
    ]), use_container_width=True, hide_index=True)
    cbox("Implication", "Palantir is less exposed to the cybersecurity cycle than it appears. The real commercial "
         "threat is Microsoft bundling Copilot into the same data layer.", "n")


# ═══════════════════════════════════════════════════════════════════════════
# STEP 9 — IS PALANTIR ONE OF ONE?
# ═══════════════════════════════════════════════════════════════════════════
def _s9(B, C, sr, cbox, cap, ph, al):
    ph("Is there any other company positioned like Palantir?",
       "No direct analogue exists.",
       "That is the bull case. The bear case: uniqueness has a price — already embedded in the stock.")
    st.markdown(f"""
    <table style="width:100%;border-collapse:collapse;font-family:Inter,sans-serif;font-size:0.88rem;margin:12px 0;">
      <thead><tr style="border-bottom:2px solid {B['border']};">
        <th style="text-align:left;padding:8px;color:{B['muted']};">#</th>
        <th style="text-align:left;padding:8px;color:{B['muted']};">Criterion</th>
        <th style="text-align:center;padding:8px;color:{B['muted']};">Palantir</th>
        <th style="text-align:left;padding:8px;color:{B['muted']};">Nearest</th>
      </tr></thead>
      <tbody>
        <tr style="border-bottom:1px solid {B['border']};"><td style="padding:8px;">1</td><td style="padding:8px;">IL5/IL6 + FedRAMP High across all platforms</td>
          <td style="padding:8px;text-align:center;background:{B['pos']};color:#fff;border-radius:4px;">✅</td><td style="padding:8px;background:{B['sfa']};">Leidos (partial)</td></tr>
        <tr style="border-bottom:1px solid {B['border']};"><td style="padding:8px;">2</td><td style="padding:8px;">Cloud + air-gap from single control plane</td>
          <td style="padding:8px;text-align:center;background:{B['pos']};color:#fff;border-radius:4px;">✅</td><td style="padding:8px;background:{B['sfa']};">None confirmed</td></tr>
        <tr style="border-bottom:1px solid {B['border']};"><td style="padding:8px;">3</td><td style="padding:8px;">Ontology-first digital twin</td>
          <td style="padding:8px;text-align:center;background:{B['pos']};color:#fff;border-radius:4px;">✅</td><td style="padding:8px;background:{B['sfa']};">Databricks (diff approach)</td></tr>
        <tr style="border-bottom:1px solid {B['border']};"><td style="padding:8px;">4</td><td style="padding:8px;">LLM on classified data with audit trail</td>
          <td style="padding:8px;text-align:center;background:{B['pos']};color:#fff;border-radius:4px;">✅</td><td style="padding:8px;background:{B['sfa']};">None at IL5+</td></tr>
        <tr><td style="padding:8px;">5</td><td style="padding:8px;">20+ year classified track record</td>
          <td style="padding:8px;text-align:center;background:{B['pos']};color:#fff;border-radius:4px;">✅</td><td style="padding:8px;background:{B['sfa']};">Booz Allen (services)</td></tr>
      </tbody>
    </table>""", unsafe_allow_html=True)
    cbox("Verdict", "On all five criteria, no competitor meets the same bar. That explains why the market "
         "treats Palantir differently.", "v")
    cbox("Counterpoint", "'One of one' is a moat argument, not a valuation argument. Whether the moat justifies "
         "81x revenue is the subject of the five chapters that follow.", "c")
    sr()
    st.markdown(f"""
    <div style="background:{B['maroon']};color:#FFF;border-radius:10px;padding:28px 32px;margin-bottom:16px;">
      <div style="font-family:'Source Serif 4',Georgia,serif;font-size:1.2rem;font-weight:700;margin-bottom:10px;">
        The Investigation Begins</div>
      <div style="font-family:Inter,sans-serif;font-size:0.92rem;line-height:1.65;color:rgba(255,255,255,0.85);">
        This page established the context. Navigate to The Market Puzzle to begin the evidence.</div>
      <div style="margin-top:18px;display:flex;gap:10px;flex-wrap:wrap;">
        <span style="border:1px solid {B['gold']};color:#FFF;border-radius:20px;background:transparent;padding:5px 16px;font-family:Inter,sans-serif;font-size:0.82rem;">The Market Puzzle</span>
        <span style="border:1px solid {B['gold']};color:#FFF;border-radius:20px;background:transparent;padding:5px 16px;font-family:Inter,sans-serif;font-size:0.82rem;">What Palantir Does</span>
        <span style="border:1px solid {B['gold']};color:#FFF;border-radius:20px;background:transparent;padding:5px 16px;font-family:Inter,sans-serif;font-size:0.82rem;">The Bull Case</span>
      </div>
      <div style="margin-top:10px;display:flex;gap:10px;flex-wrap:wrap;">
        <span style="border:1px solid {B['gold']};color:#FFF;border-radius:20px;background:transparent;padding:5px 16px;font-family:Inter,sans-serif;font-size:0.82rem;">The Bear Case</span>
        <span style="border:1px solid {B['gold']};color:#FFF;border-radius:20px;background:transparent;padding:5px 16px;font-family:Inter,sans-serif;font-size:0.82rem;">The Valuation Test</span>
        <span style="border:1px solid {B['gold']};color:#FFF;border-radius:20px;background:transparent;padding:5px 16px;font-family:Inter,sans-serif;font-size:0.82rem;">The Verdict</span>
      </div>
      <div style="margin-top:16px;font-size:0.75rem;color:rgba(200,168,180,0.85);font-family:Inter,sans-serif;">
        Data sources: SEC EDGAR, Palantir IR, DISA records, NATO procurement, U.S. Army contracts</div>
    </div>""", unsafe_allow_html=True)
