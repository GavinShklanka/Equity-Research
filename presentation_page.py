"""
PLTR Equity Research — Presentation Overview Page
Standalone module. render() accepts B, C, and helper functions from app.py.
"""
import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from pltr_data import INCOME_STATEMENT, CASH_FLOW, MARKET_DATA, PEER_COMPARISON, REVENUE_SEGMENTS


def render(B, C, sr, cbox, cap, ph, al):
    """Render the full Presentation page. Called from app.py page router."""

    # ═══════════════════════════════════════════════════════════════════════
    # SECTION 0 — MISSION STATEMENT
    # ═══════════════════════════════════════════════════════════════════════
    st.markdown(f"""
    <div style="background:{B['surface']};border-left:4px solid {B['maroon']};
         border-radius:8px;padding:24px 28px;margin-bottom:18px;">
      <div style="font-family:'Source Serif 4',Georgia,serif;color:{B['maroon']};
           font-size:1.3rem;font-weight:700;margin-bottom:6px;">
        MBAN5570 Equity Research Investigation
      </div>
      <div style="font-family:'Inter',sans-serif;color:{B['navy']};
           font-size:1.0rem;font-weight:600;margin-bottom:12px;">
        Palantir Technologies — The Exception Case
      </div>
      <div style="font-family:'Inter',sans-serif;color:{B['text']};
           font-size:0.9rem;line-height:1.65;">
        This investigation asks a single question: Is Palantir priced like no other software company
        because it IS structurally different — or because the market currently believes it is? Over six
        chapters, we examine the origins, platforms, financials, competitive landscape, and valuation of
        a company that has spent 17 years building infrastructure that most of its competitors cannot
        yet replicate.
      </div>
      <div style="margin-top:14px;display:flex;gap:10px;flex-wrap:wrap;">
        <span style="border:1px solid {B['gold']};color:{B['maroon']};border-radius:20px;
              padding:4px 14px;font-family:'Inter',sans-serif;font-size:0.78rem;font-weight:500;">MBAN5570</span>
        <span style="border:1px solid {B['gold']};color:{B['maroon']};border-radius:20px;
              padding:4px 14px;font-family:'Inter',sans-serif;font-size:0.78rem;font-weight:500;">Sobey School of Business</span>
        <span style="border:1px solid {B['gold']};color:{B['maroon']};border-radius:20px;
              padding:4px 14px;font-family:'Inter',sans-serif;font-size:0.78rem;font-weight:500;">Dr. Mohammad M. Rahaman</span>
      </div>
    </div>
    """, unsafe_allow_html=True)
    sr()

    # ═══════════════════════════════════════════════════════════════════════
    # SECTION 1 — FROM HARDWARE PRIMES TO SOFTWARE BRAIN
    # ═══════════════════════════════════════════════════════════════════════
    st.markdown("## From Hardware Primes to Software Brain")

    cbox("Context",
         "For 70 years, defense meant hardware. Lockheed Martin built the F-35. General Dynamics built "
         "the Abrams. Northrop Grumman built the B-21 Raider. The primes won wars by building the machines. "
         "Palantir's thesis is that the next era of defense is won by the software that operates them — and "
         "that no company has spent more time building that software in classified environments than Palantir.",
         "n")

    # Pull Palantir revenue and market cap from data
    try:
        pltr_rev_fy2024 = INCOME_STATEMENT.loc[2024, "Total Revenue"]
        pltr_rev_str = f"${pltr_rev_fy2024/1000:.1f}B" if pltr_rev_fy2024 >= 1000 else f"${pltr_rev_fy2024:.0f}M"
    except Exception:
        pltr_rev_str = "~$2.9B"

    pltr_mkt_cap_str = f"~${MARKET_DATA.get('market_cap_B', 365):.0f}B"

    comparison_data = pd.DataFrame([
        {"Company": "Lockheed Martin", "Category": "Hardware Prime", "Primary Product": "F-35 / Missiles",
         "Rev FY2024": "~$71B", "Mkt Cap": "~$105B"},
        {"Company": "General Dynamics", "Category": "Hardware Prime", "Primary Product": "Gulfstream / Abrams",
         "Rev FY2024": "~$48B", "Mkt Cap": "~$65B"},
        {"Company": "Northrop Grumman", "Category": "Hardware Prime", "Primary Product": "B-21 / ISR",
         "Rev FY2024": "~$41B", "Mkt Cap": "~$65B"},
        {"Company": "Raytheon (RTX)", "Category": "Hardware Prime", "Primary Product": "Missiles / Radar",
         "Rev FY2024": "~$80B", "Mkt Cap": "~$145B"},
        {"Company": "Palantir (PLTR)", "Category": "Software Brain",
         "Primary Product": "Gotham / Foundry / AIP / Apollo",
         "Rev FY2024": pltr_rev_str, "Mkt Cap": pltr_mkt_cap_str},
    ])
    st.dataframe(comparison_data, use_container_width=True, hide_index=True)

    cap("Palantir's market cap has exceeded the combined value of the three largest traditional defense "
        "primes despite having roughly 1/25th their revenue. The market is pricing software infrastructure "
        "— not hardware volume.",
        "The premium reflects a structural thesis: that marginal defense value is shifting from platform "
        "manufacturing to AI-driven decision intelligence. If correct, Palantir is early. If wrong, the "
        "multiple compresses severely.")

    cbox("Signal",
         "In August 2025, Palantir's market cap exceeded $443B — surpassing the combined total of "
         "Lockheed Martin, Raytheon, and Northrop Grumman. The market has already voted. The question "
         "is whether the fundamentals catch up.", "s")
    sr()

    # ═══════════════════════════════════════════════════════════════════════
    # SECTION 2 — THE FOUR-PLATFORM STACK
    # ═══════════════════════════════════════════════════════════════════════
    st.markdown("## The Four-Platform Stack")

    st.markdown(f"""<div style="font-family:'Inter',sans-serif;color:{B['text']};font-size:0.92rem;
        line-height:1.65;margin-bottom:16px;">
        Palantir does not sell a single product. It sells a vertically integrated software operating system
        for data-driven institutions. Understanding the four layers and how they interlock is prerequisite
        to evaluating the moat.
    </div>""", unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown("### Gotham")
        st.markdown(f'<span style="border:1px solid {B["navy"]};color:{B["navy"]};border-radius:20px;'
                    f'padding:3px 12px;font-size:0.75rem;font-weight:500;">Defense & Intelligence</span>',
                    unsafe_allow_html=True)
        st.markdown(
            "Launched 2008. Built with CIA analysts. Integrates classified data, detects patterns, "
            "supports targeting. Used by DoD, FBI, NSA, CIA, Europol, Ukraine military. Forward Deployed "
            "Engineers embed inside agencies for months — creating structural switching costs that are "
            "nearly impossible to reverse. IL5/IL6 accredited.")
        cbox("Competitors",
             "Leidos, CACI International, Booz Allen Hamilton, DataWalk, Babel Street. None match "
             "Gotham's combination of accreditation depth and time-in-field.", "n")

    with c2:
        st.markdown("### Foundry")
        st.markdown(f'<span style="border:1px solid {B["navy"]};color:{B["navy"]};border-radius:20px;'
                    f'padding:3px 12px;font-size:0.75rem;font-weight:500;">Commercial Enterprise</span>',
                    unsafe_allow_html=True)
        st.markdown(
            "Launched 2016. Commercial operating system for enterprise data — an ontology layer that "
            "connects every data source, workflow, and decision. Used by Airbus (4x A350 production), "
            "Ferrari (F1), NHS England, Morgan Stanley, Chevron, Samsung. Once Foundry owns the ontology "
            "layer, replacement cost is measured in years.")
        cbox("Competitors",
             "Microsoft Fabric + Azure OpenAI (distribution/bundling), Databricks (developer adoption), "
             "Snowflake Cortex (data economics), C3.ai (enterprise AI). None have Foundry's ontology-first "
             "architecture.", "n")

    with c3:
        st.markdown("### AIP")
        st.markdown(f'<span style="border:1px solid {B["gold"]};color:{B["gold"]};border-radius:20px;'
                    f'padding:3px 12px;font-size:0.75rem;font-weight:500;">AI Orchestration Layer</span>',
                    unsafe_allow_html=True)
        st.markdown(
            "Launched April 2023. LLMs and autonomous agents on top of Gotham and Foundry — operating on "
            "the customer's own classified data, behind their own firewall, with full audit trails. AIP is "
            "why US Commercial grew 137% YoY. Boot camp model converts pilots to production in weeks. "
            "TITAN (Army AI targeting) and Maven Smart System (NATO) run on AIP.")
        cbox("Competitors",
             "Microsoft Copilot (dominant commercial, weak in classified), Google Vertex AI (cloud-native, "
             "no air-gap), AWS Bedrock (similar gap), Anduril (defense-specific but narrower). AIP's "
             "classified deployment is the differentiator.", "n")

    with c4:
        st.markdown("### Apollo")
        st.markdown(f'<span style="border:1px solid {B["maroon"]};color:{B["maroon"]};border-radius:20px;'
                    f'padding:3px 12px;font-size:0.75rem;font-weight:500;">The Hidden Moat</span>',
                    unsafe_allow_html=True)
        st.markdown(
            "The least-discussed and most defensible product. Apollo allows Gotham, Foundry, and AIP to "
            "run anywhere simultaneously — commercial cloud, on-premise, air-gapped networks, classified "
            "government clouds, battlefield edge — from a single control plane. Every update cryptographically "
            "signed. FedRAMP High, IL5, IL6 certified. The infrastructure that makes the rest of the platform "
            "deployable in environments no competitor can access.")
        cbox("Competitors",
             "Spinnaker, Argo CD, Octopus Deploy, Flux CD, GitHub Actions — none hold IL6 authorization "
             "or native air-gapped support. No CD peer meets more than 2 of Apollo's 4 classified "
             "requirements simultaneously.", "n")

    cbox("Implication",
         "The four platforms are not four products. They are four layers of a single operating system. "
         "Gotham captures the government. Foundry captures the enterprise. AIP delivers the AI use case. "
         "Apollo ensures it all runs anywhere — including places competitors cannot reach. Replacing "
         "Palantir means replacing all four layers simultaneously.", "s")
    sr()

    # ═══════════════════════════════════════════════════════════════════════
    # SECTION 3 — APOLLO PEER EVALUATION (7 Parts)
    # ═══════════════════════════════════════════════════════════════════════
    st.markdown("## Apollo: Product Peer Evaluation")

    cbox("Research Note",
         "This section is grounded in a structured peer evaluation using a finance framework adapted "
         "to product analysis. Peers were selected based on shared buyer, shared core function, and shared "
         "competitive moment — not broad category association. The five peers are: Spinnaker/Armory, "
         "Argo CD, Octopus Deploy, Flux CD, and GitHub Actions. Hyperscalers were excluded because they "
         "provide the infrastructure Apollo deploys onto — not competing CD orchestration layers.", "n")

    # PART A — HEADLINE SCORECARD
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Market Position — Classified CD", "1 of 1", delta="No qualified competitor exists")
    k2.metric("IL6-Authorized CD Vendors", "< 6", delta="Apollo is the only CD-specific holder")
    k3.metric("Avg. Service Patch Speed", "3.5 min", delta="Across all environments incl. air-gapped")
    k4.metric("R&D Time Barrier to Replicate", "5 years", delta="Palantir's own documented build time")

    cap("These are not marketing claims. The IL6 figure comes from DISA authorization records. The "
        "3.5-minute patch speed was demonstrated during the Log4j crisis.",
        "The R&D time barrier is compounding, not static. Apollo continues embedding into customer "
        "infrastructure while any new entrant is still in accreditation.")
    sr()

    # PART B — THREE-SEGMENT CD MARKET
    st.markdown("### The CD Market Is Three Separate Markets")
    st.markdown(f"""<div style="font-family:'Inter',sans-serif;color:{B['text']};font-size:0.9rem;
        line-height:1.6;margin-bottom:12px;">
        Most CD analysis treats the market as a single competitive landscape.
        The peer evaluation found this is a category error. There are three distinct segments.
    </div>""", unsafe_allow_html=True)

    cd_market = pd.DataFrame([
        {"Segment": "Cloud-native / SaaS", "Description": "Connected, standard compliance",
         "Buyers": "Tech / SaaS / mid-market", "Key Req": "Speed, dev UX, GitOps",
         "Apollo Position": "Peripheral"},
        {"Segment": "Enterprise Hybrid", "Description": "On-prem + cloud, some compliance",
         "Buyers": "Large enterprise", "Key Req": "Multi-tenancy, audit",
         "Apollo Position": "Competitive but contested"},
        {"Segment": "Classified / Disconnected", "Description": "Air-gapped, sovereign, DDIL",
         "Buyers": "DoD / NATO / intel agencies", "Key Req": "IL5/IL6, disconnected ops",
         "Apollo Position": "DOMINANT — no competitor"},
    ])
    st.dataframe(cd_market, use_container_width=True, hide_index=True)

    cbox("Segmentation Insight",
         "Evaluating Apollo against Argo CD or GitHub Actions as head-to-head competitors is a category "
         "error — equivalent to comparing Goldman Sachs prime brokerage to Robinhood because both involve "
         "equities.", "n")
    sr()

    # PART C — FULL CAPABILITY MATRIX
    st.markdown("### Capability Matrix — Apollo vs 5 CD Peers")
    cap_matrix = pd.DataFrame([
        {"Capability": "Air-gapped deployment", "Apollo": "✅ Native", "Spinnaker/Armory": "❌",
         "Argo CD": "❌", "Octopus Deploy": "⚠️ Limited", "Flux CD": "❌", "GitHub Actions": "❌"},
        {"Capability": "DoD IL6 authorization", "Apollo": "✅ Authorized", "Spinnaker/Armory": "❌",
         "Argo CD": "❌", "Octopus Deploy": "❌", "Flux CD": "❌", "GitHub Actions": "❌"},
        {"Capability": "FedRAMP High", "Apollo": "✅ Certified", "Spinnaker/Armory": "❌",
         "Argo CD": "❌", "Octopus Deploy": "⚠️ In progress", "Flux CD": "❌", "GitHub Actions": "⚠️ Moderate"},
        {"Capability": "Cryptographic signing", "Apollo": "✅ End-to-end", "Spinnaker/Armory": "⚠️ Plugin",
         "Argo CD": "⚠️ Cosign", "Octopus Deploy": "⚠️ Partial", "Flux CD": "⚠️ Cosign", "GitHub Actions": "⚠️ Attestation"},
        {"Capability": "Compliance orchestration", "Apollo": "✅ Native", "Spinnaker/Armory": "⚠️ Gates",
         "Argo CD": "⚠️ Add-on", "Octopus Deploy": "⚠️ Add-on", "Flux CD": "❌", "GitHub Actions": "❌"},
        {"Capability": "Multi-cloud (all types)", "Apollo": "✅ All", "Spinnaker/Armory": "✅ Public",
         "Argo CD": "⚠️ K8s-only", "Octopus Deploy": "✅ Hybrid", "Flux CD": "⚠️ K8s-only", "GitHub Actions": "⚠️ Cloud-native"},
        {"Capability": "Canary / blue-green", "Apollo": "✅ Built-in", "Spinnaker/Armory": "✅ Core",
         "Argo CD": "✅ Rollouts", "Octopus Deploy": "⚠️ Supported", "Flux CD": "⚠️ Flagger", "GitHub Actions": "⚠️ Manual"},
        {"Capability": "Fleet observability", "Apollo": "✅ Native", "Spinnaker/Armory": "⚠️ Per-cluster",
         "Argo CD": "⚠️ Per-cluster", "Octopus Deploy": "✅ Strong", "Flux CD": "❌", "GitHub Actions": "❌"},
        {"Capability": "Open-source", "Apollo": "❌ Commercial", "Spinnaker/Armory": "✅",
         "Argo CD": "✅", "Octopus Deploy": "❌ Commercial", "Flux CD": "✅", "GitHub Actions": "✅ Free tier"},
        {"Capability": "Pricing", "Apollo": "Enterprise contract", "Spinnaker/Armory": "Free / Armory",
         "Argo CD": "Free / Codefresh", "Octopus Deploy": "Per-target", "Flux CD": "Free", "GitHub Actions": "Per-minute"},
    ])
    st.dataframe(cap_matrix, use_container_width=True, hide_index=True)

    cbox("Matrix Reading",
         "Apollo is the only product in this peer group that achieves a clean sweep across all four "
         "classified deployment requirements simultaneously: air-gapped support, IL6 authorization, "
         "cryptographic signing, and compliance-aware autonomous orchestration. No peer achieves more "
         "than two.", "s")
    sr()

    # PART D — MOAT SCORING (horizontal bar chart)
    st.markdown("### Structural Moat Scores")

    dimensions = [
        "Pricing accessibility",
        "Developer ecosystem",
        "Gov brand / distribution",
        "Technical replication cost",
        "Operational history advantage",
        "Switching cost — compliance",
        "Security accreditation barrier",
    ]
    scores = [10, 28, 80, 85, 88, 92, 96]
    bar_colors = [B["pos"] if s >= 80 else (B["gold"] if s >= 30 else B["neg"]) for s in scores]

    fig_moat = go.Figure(go.Bar(
        y=dimensions, x=scores, orientation='h',
        marker_color=bar_colors,
        text=[f"{s}" for s in scores], textposition="outside"
    ))
    fig_moat.add_vline(x=50, line_dash="dash", line_color=B["muted"], line_width=1)
    al(fig_moat, "Structural Moat — Dimension Scores (0–100)", 380)
    st.plotly_chart(fig_moat, use_container_width=True)

    cap("Apollo scores 80–96 on every dimension that matters for its primary market. The near-zero "
        "scores on developer ecosystem and self-serve pricing are deliberate market focus, not weaknesses.",
        "The moat asymmetry is key. High where it matters, low where it doesn't. Risk emerges only if "
        "Apollo attempts commercial expansion.")
    sr()

    # PART E — PROS, CONS, TRADE-OFFS
    with st.expander("✅ Structural Advantages (Durable)"):
        st.markdown("""
- Only IL6-authorized CD platform (< 6 vendors total)
- Native DDIL architecture (founding design requirement)
- Compliance encoding = compounding lock-in
- Log4j: patched 200+ environments incl. classified in hours
- 5 years proprietary R&D as hard time barrier
        """)

    with st.expander("⚠️ Real Limitations"):
        st.markdown("""
- Enterprise-only sales model (no free tier / self-serve)
- No Kustomize / cdk8s templating support
- Steep learning curve without specialized DevSecOps teams
- Revenue contribution not separately disclosed
- Hyperscaler encroachment risk on 5–7 year horizon
        """)

    with st.expander("⚪ Apparent Weaknesses = Market Trade-offs"):
        st.markdown("""
- Not open-source → security feature in classified environments
- No community ecosystem → irrelevant to core customers
- Overkill for simple deployments → intentional positioning
        """)

    sr()

    # PART F — RISK MATRIX
    st.markdown("### Risk Matrix")
    risk_data = pd.DataFrame([
        {"Risk": "Hyperscaler CD competition", "Severity": "MEDIUM", "Timeline": "5–7 yr",
         "Description": "AWS/Azure building classified infra, no CD product yet"},
        {"Risk": "DoD budget disruption", "Severity": "MEDIUM", "Timeline": "Recurring",
         "Description": "CRs can delay, cancellation unlikely given embedding"},
        {"Risk": "Open-source replication", "Severity": "LOW", "Timeline": "3–5 yr",
         "Description": "Still needs IL6 accreditation independently"},
        {"Risk": "Kustomize / GitOps gap", "Severity": "LOW", "Timeline": "Near-term",
         "Description": "Risks enterprise hybrid segment if unaddressed"},
        {"Risk": "IL6 authorization revocation", "Severity": "HIGH (low prob)", "Timeline": "Tail risk",
         "Description": "Would require major security incident"},
    ])

    def _color_severity(val):
        if "HIGH" in str(val):
            return f"color: {B['neg']}"
        elif "MEDIUM" in str(val):
            return f"color: {B['gold']}"
        elif "LOW" in str(val):
            return f"color: {B['pos']}"
        return ""

    styled_risk = risk_data.style.map(_color_severity, subset=["Severity"])
    st.dataframe(styled_risk, use_container_width=True, hide_index=True)
    sr()

    # PART G — EVALUATION VERDICT
    st.markdown(f"""
    <div style="background:{B['navy']};color:#FFFFFF;border-radius:8px;padding:24px 28px;margin-bottom:14px;">
      <div style="color:{B['gold']};font-family:monospace;font-variant:small-caps;font-size:0.85rem;
           font-weight:700;margin-bottom:8px;letter-spacing:0.04em;">
        PRODUCT EVALUATION FINDING: UNCONTESTED WITHIN ITS DEFINED MARKET
      </div>
      <div style="font-family:'Inter',sans-serif;font-size:0.9rem;line-height:1.65;">
        The peer evaluation finds that Palantir Apollo holds an effectively uncontested position within
        the classified, air-gapped, and disconnected continuous deployment market. This conclusion is
        grounded in three structural barriers unique to Apollo: DoD IL6 authorization, native DDIL
        architecture built over five years, and 20 years of operational history in national security
        contexts. No peer holds all three. The bear case is real but temporally distant.
      </div>
    </div>
    """, unsafe_allow_html=True)

    cbox("Investor Caveat",
         "This evaluation assesses Apollo as a product, not PLTR as a stock. Apollo's market position "
         "is strong — whether that position is correctly priced into Palantir's equity at current "
         "multiples is a separate and unresolved question.", "c")
    sr()

    # ═══════════════════════════════════════════════════════════════════════
    # SECTION 4 — COMPETITIVE LANDSCAPE
    # ═══════════════════════════════════════════════════════════════════════
    st.markdown("## The Competitive Landscape")

    cbox("Context",
         "Palantir has different competitors on every layer of its stack. No single company competes "
         "across all four platforms simultaneously. That is not an accident — it is the design.", "n")

    with st.expander("Government & Defense (Gotham competitors)"):
        gov_comp = pd.DataFrame([
            {"Company": "Booz Allen Hamilton", "Overlap": "High — C4ISR", "Accreditation": "IL5/IL6",
             "Key Difference": "Services-led"},
            {"Company": "Leidos Holdings", "Overlap": "High — DoD AI", "Accreditation": "IL5",
             "Key Difference": "Less ontology depth"},
            {"Company": "CACI International", "Overlap": "Medium — intel", "Accreditation": "IL4",
             "Key Difference": "Narrower scope"},
            {"Company": "Northrop Grumman", "Overlap": "Medium — C2/ISR", "Accreditation": "IL5/IL6",
             "Key Difference": "Hardware-led"},
            {"Company": "DataWalk", "Overlap": "Medium — investigative", "Accreditation": "Lower",
             "Key Difference": "No classified deploy"},
            {"Company": "Babel Street", "Overlap": "Low-Med — OSINT", "Accreditation": "Commercial",
             "Key Difference": "No gov depth"},
        ])
        st.dataframe(gov_comp, use_container_width=True, hide_index=True)
        cbox("Signal",
             "None of the Gotham competitors combine Palantir's accreditation level with its "
             "software-first architecture and FDE deployment model.", "s")

    with st.expander("Enterprise Data (Foundry competitors)"):
        ent_comp = pd.DataFrame([
            {"Company": "Microsoft Fabric + Azure OpenAI", "Overlap": "High",
             "Strength": "Distribution / bundling", "Palantir Advantage": "Ontology depth, classified"},
            {"Company": "Databricks", "Overlap": "High",
             "Strength": "Dev adoption, open source", "Palantir Advantage": "Operational workflows"},
            {"Company": "Snowflake", "Overlap": "Medium",
             "Strength": "Data economics", "Palantir Advantage": "Decision layer on top"},
            {"Company": "C3.ai", "Overlap": "Medium",
             "Strength": "Enterprise AI brand", "Palantir Advantage": "More comprehensive"},
            {"Company": "SAP (partnership)", "Overlap": "Low-Med",
             "Strength": "ERP integration", "Palantir Advantage": "AI layer above SAP"},
        ])
        st.dataframe(ent_comp, use_container_width=True, hide_index=True)
        cbox("Counterpoint",
             "Microsoft Fabric + Azure OpenAI is the most credible Foundry threat. Microsoft's "
             "distribution advantage could commoditize the commercial data platform layer faster "
             "than Palantir's ontology moat can respond.", "c")

    with st.expander("AI Platform (AIP competitors)"):
        ai_comp = pd.DataFrame([
            {"Company": "Microsoft Copilot / Azure OpenAI", "Overlap": "High",
             "Classified Deploy": "No (IL5+)", "Boot Camp": "No"},
            {"Company": "Google Vertex AI", "Overlap": "High",
             "Classified Deploy": "No (IL5+)", "Boot Camp": "No"},
            {"Company": "AWS Bedrock", "Overlap": "High",
             "Classified Deploy": "Partial (GovCloud)", "Boot Camp": "No"},
            {"Company": "Anduril Industries", "Overlap": "Medium (defense)",
             "Classified Deploy": "Yes", "Boot Camp": "No"},
            {"Company": "Scale AI", "Overlap": "Low-Medium",
             "Classified Deploy": "Limited", "Boot Camp": "No"},
        ])
        st.dataframe(ai_comp, use_container_width=True, hide_index=True)
        cbox("Signal",
             "AIP's classified deployment capability is not yet replicable by hyperscalers. Google "
             "withdrew from Project Maven in 2019. Palantir took the contract and never left.", "s")

    with st.expander("Deployment Infrastructure (Apollo peers)"):
        st.markdown(f"""<div style="font-family:'Inter',sans-serif;color:{B['text']};font-size:0.88rem;
            line-height:1.6;margin-bottom:12px;">
            <strong>Why hyperscalers are NOT the peer group:</strong> Azure Government provides the rack.
            Apollo decides what goes on it and when. They operate at different abstraction levels.
        </div>""", unsafe_allow_html=True)

        deploy_comp = pd.DataFrame([
            {"Tool": "Apollo", "Air-Gap": "✅ Native", "IL6": "✅ Yes", "Crypto Signing": "✅ Standard",
             "Compliance Orch": "✅ Native", "Fleet Obs": "✅ Native"},
            {"Tool": "Spinnaker", "Air-Gap": "❌", "IL6": "❌", "Crypto Signing": "⚠️ Plugin",
             "Compliance Orch": "⚠️ Gates", "Fleet Obs": "⚠️ Per-cluster"},
            {"Tool": "Argo CD", "Air-Gap": "❌", "IL6": "❌", "Crypto Signing": "⚠️ Cosign",
             "Compliance Orch": "⚠️ Add-on", "Fleet Obs": "⚠️ Per-cluster"},
            {"Tool": "Octopus", "Air-Gap": "⚠️ Limited", "IL6": "❌", "Crypto Signing": "⚠️ Partial",
             "Compliance Orch": "⚠️ Add-on", "Fleet Obs": "✅ Strong"},
            {"Tool": "Flux CD", "Air-Gap": "❌", "IL6": "❌", "Crypto Signing": "⚠️ Cosign",
             "Compliance Orch": "❌", "Fleet Obs": "❌"},
            {"Tool": "GitHub Actions", "Air-Gap": "❌", "IL6": "❌", "Crypto Signing": "⚠️ Attest",
             "Compliance Orch": "❌", "Fleet Obs": "❌"},
        ])
        st.dataframe(deploy_comp, use_container_width=True, hide_index=True)
        cbox("Legitimate Omission",
             "Second Front Systems' Game Warden is the most legitimate peer omission. It operates as "
             "a compliance wrapper rather than full autonomous deployment orchestration.", "n")
    sr()

    # ═══════════════════════════════════════════════════════════════════════
    # SECTION 5 — FINANCIAL EVIDENCE
    # ═══════════════════════════════════════════════════════════════════════
    st.markdown("## The Financial Evidence")

    st.markdown(f"""<div style="font-family:'Inter',sans-serif;color:{B['muted']};font-size:0.88rem;
        margin-bottom:14px;">
        FY2025 reported results. All data from Palantir IR and SEC filings.
    </div>""", unsafe_allow_html=True)

    ist = INCOME_STATEMENT
    cf = CASH_FLOW
    seg = REVENUE_SEGMENTS

    # Revenue FY2025
    rev_2025 = ist.loc[2025, "Total Revenue"]
    rev_2020 = ist.loc[2020, "Total Revenue"]
    rev_cagr = ((rev_2025 / rev_2020) ** (1 / 5) - 1) * 100

    # US Commercial Growth
    us_c_2025 = seg.loc[2025, "US Commercial"]
    us_c_2024 = seg.loc[2024, "US Commercial"]
    us_comm_growth = ((us_c_2025 / us_c_2024) - 1) * 100

    # FCF Margin
    fcf_margin_val = cf.loc[2025, "FCF Margin %"]

    # Gross Margin
    gross_margin_val = round(ist.loc[2025, "Gross Profit"] / ist.loc[2025, "Total Revenue"] * 100, 1)

    # EV/Revenue vs Peer
    peer = PEER_COMPARISON
    pex = peer[peer["Ticker"] != "PLTR"]
    pltr_evr = peer[peer["Ticker"] == "PLTR"]["EV/Revenue"].iloc[0]
    peer_median_evr = pex["EV/Revenue"].median()

    # Row 1 metrics
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Revenue FY2025", f"${rev_2025/1000:.1f}B")
    m2.metric("Revenue CAGR 2020–2025", f"{rev_cagr:.1f}%")
    m3.metric("US Commercial Growth YoY", f"{us_comm_growth:.0f}%")
    m4.metric("Rule of 40", "107")

    # Row 2 metrics
    m5, m6, m7, m8 = st.columns(4)
    m5.metric("FCF Margin", f"{fcf_margin_val:.1f}%")
    m6.metric("Gross Margin", f"{gross_margin_val:.1f}%")
    m7.metric("Net Cash", "$7.2B")
    m8.metric("EV/Revenue vs Peer Median", f"{pltr_evr:.0f}x vs {peer_median_evr:.0f}x")

    # Two mini charts
    ch1, ch2 = st.columns(2)
    with ch1:
        fig_rev = go.Figure(go.Bar(
            x=ist.index.tolist(), y=ist["Total Revenue"].tolist(),
            marker_color=C[0], text=[f"${v:,.0f}" for v in ist["Total Revenue"]],
            textposition="outside"
        ))
        al(fig_rev, "Revenue ($M) — 2020–2025", 260)
        st.plotly_chart(fig_rev, use_container_width=True)

    with ch2:
        fcf_pct = cf["FCF Margin %"].dropna()
        fig_fcf = go.Figure(go.Scatter(
            x=fcf_pct.index.tolist(), y=fcf_pct.values.tolist(),
            mode="lines+markers", line=dict(color=C[1], width=3),
            text=[f"{v:.1f}%" for v in fcf_pct.values], textposition="top center"
        ))
        al(fig_fcf, "FCF Margin (%) — 2021–2025", 260)
        st.plotly_chart(fig_fcf, use_container_width=True)

    cap("Simultaneously accelerating revenue growth AND expanding margins at $4.5B scale.",
        "Revenue CAGR of 32.5% with FCF margin expanding from negative to 51% = operating leverage at scale.")

    cbox("Bull Case Summary",
         "Rule of 40: 107. FCF margin: 51%. Gross margin: 82%. Zero debt. $7.2B net cash. US Commercial "
         "growing 137% YoY. 10-year $10B Army contract. NATO Maven Smart System deployed.", "s")

    cbox("Bear Case Summary",
         "EV/Revenue: 81x vs peer median 12x. SBC: $700M (15.6% of revenue). GAAP operating margin: "
         "25% vs adjusted 51%. Pre-IPO losses: $623M (2018), $576M (2019). The fundamentals are real. "
         "The price requires believing they persist for years.", "c")
    sr()

    # ═══════════════════════════════════════════════════════════════════════
    # SECTION 6 — CYBERSECURITY POSITIONING
    # ═══════════════════════════════════════════════════════════════════════
    st.markdown("## Where Palantir Sits in the Security Stack")

    cbox("Context",
         "Palantir does not sell firewalls, endpoint protection, or threat prevention. CrowdStrike, "
         "Palo Alto Networks, and Fortinet own that layer. Palantir operates above it — the intelligence "
         "and decision layer that ingests threat data, integrates it with operational data, and supports "
         "analyst decisions at speed.", "n")

    # Vertical stack diagram
    st.markdown(f"""
    <div style="max-width:600px;margin:16px auto;font-family:'Inter',sans-serif;">
      <div style="text-align:center;font-size:0.78rem;color:{B['muted']};margin-bottom:6px;">
        decisions flow down ↓
      </div>
      <div style="background:{B['maroon']};color:#FFFFFF;padding:14px;text-align:center;
           border-radius:8px 8px 0 0;font-weight:600;font-size:0.9rem;">
        Decision & Intelligence — PALANTIR
      </div>
      <div style="background:{B['navy']};color:#FFFFFF;padding:12px;text-align:center;
           font-size:0.85rem;">
        Data Integration & Ontology
      </div>
      <div style="background:{B['sfa']};color:{B['text']};padding:12px;text-align:center;
           font-size:0.85rem;">
        Threat Detection — CrowdStrike | Palo Alto | Fortinet
      </div>
      <div style="background:{B['border']};color:{B['text']};padding:12px;text-align:center;
           border-radius:0 0 8px 8px;font-size:0.85rem;">
        Infrastructure & Network
      </div>
      <div style="text-align:center;font-size:0.78rem;color:{B['muted']};margin-top:6px;">
        data flows up ↑
      </div>
    </div>
    """, unsafe_allow_html=True)

    cyber_comp = pd.DataFrame([
        {"Company": "CrowdStrike", "Category": "EDR", "Relationship to Palantir": "Different layer — feeds data TO Palantir"},
        {"Company": "Palo Alto", "Category": "Network security", "Relationship to Palantir": "Different layer"},
        {"Company": "Fortinet", "Category": "Firewall", "Relationship to Palantir": "Different layer"},
        {"Company": "MS Sentinel", "Category": "SIEM / SOAR", "Relationship to Palantir": "Partial overlap — bundle threat"},
        {"Company": "Splunk (Cisco)", "Category": "SIEM / analytics", "Relationship to Palantir": "Medium overlap"},
    ])
    st.dataframe(cyber_comp, use_container_width=True, hide_index=True)
    sr()

    # ═══════════════════════════════════════════════════════════════════════
    # SECTION 7 — THE "ONE OF ONE" ARGUMENT
    # ═══════════════════════════════════════════════════════════════════════
    st.markdown("## Is Palantir Genuinely One of One?")

    ph("Is there any other company positioned like Palantir?",
       "No direct analogue exists. The combination of classified accreditation, ontology-first "
       "architecture, FDE model, and Apollo infrastructure is not replicated by any single competitor.",
       "That is the bull case in one sentence. The bear case is that uniqueness has a price — and "
       "the price is already embedded in the stock.")

    one_of_one = pd.DataFrame([
        {"Criteria": "IL5/IL6 + FedRAMP High across all platforms", "Palantir": "✅ Yes",
         "Nearest Competitor": "Leidos (partial)"},
        {"Criteria": "Cloud + air-gap from single control plane", "Palantir": "✅ Yes",
         "Nearest Competitor": "None confirmed"},
        {"Criteria": "Ontology-first digital twin", "Palantir": "✅ Yes",
         "Nearest Competitor": "Databricks (different approach)"},
        {"Criteria": "LLM on classified data with audit trail", "Palantir": "✅ Yes",
         "Nearest Competitor": "None at IL5+"},
        {"Criteria": "20+ year classified track record", "Palantir": "✅ Yes",
         "Nearest Competitor": "Booz Allen (services not software)"},
    ])
    st.dataframe(one_of_one, use_container_width=True, hide_index=True)

    cbox("Verdict",
         "On all five structural criteria, no single competitor meets the same bar. It does not "
         "guarantee the stock price is justified — but it explains why the market treats Palantir "
         "differently.", "v")

    cbox("Counterpoint",
         "'One of one' is a moat argument, not a valuation argument. A company can be structurally "
         "unique and still be overpriced. Whether the moat justifies 81x revenue is the subject of "
         "the five investigation chapters that follow.", "c")
    sr()

    # ═══════════════════════════════════════════════════════════════════════
    # SECTION 8 — BRIDGE TO INVESTIGATION
    # ═══════════════════════════════════════════════════════════════════════
    st.markdown(f"""
    <div style="background:{B['maroon']};color:#FFFFFF;border-radius:10px;padding:28px 32px;
         margin-bottom:16px;">
      <div style="font-family:'Source Serif 4',Georgia,serif;font-size:1.25rem;font-weight:700;
           color:#FFFFFF;margin-bottom:10px;">
        The Investigation Begins
      </div>
      <div style="font-family:'Inter',sans-serif;font-size:0.92rem;line-height:1.65;color:#F5ECF0;">
        This page established the context. The six chapters that follow examine the evidence.
        Navigate using the sidebar to begin with The Market Puzzle.
      </div>
      <div style="margin-top:18px;display:flex;gap:10px;flex-wrap:wrap;">
        <span style="border:1px solid {B['gold']};color:#FFFFFF;border-radius:20px;background:transparent;
              padding:5px 16px;font-family:'Inter',sans-serif;font-size:0.82rem;">The Market Puzzle</span>
        <span style="border:1px solid {B['gold']};color:#FFFFFF;border-radius:20px;background:transparent;
              padding:5px 16px;font-family:'Inter',sans-serif;font-size:0.82rem;">What Palantir Does</span>
        <span style="border:1px solid {B['gold']};color:#FFFFFF;border-radius:20px;background:transparent;
              padding:5px 16px;font-family:'Inter',sans-serif;font-size:0.82rem;">The Bull Case</span>
      </div>
      <div style="margin-top:10px;display:flex;gap:10px;flex-wrap:wrap;">
        <span style="border:1px solid {B['gold']};color:#FFFFFF;border-radius:20px;background:transparent;
              padding:5px 16px;font-family:'Inter',sans-serif;font-size:0.82rem;">The Bear Case</span>
        <span style="border:1px solid {B['gold']};color:#FFFFFF;border-radius:20px;background:transparent;
              padding:5px 16px;font-family:'Inter',sans-serif;font-size:0.82rem;">The Valuation Test</span>
        <span style="border:1px solid {B['gold']};color:#FFFFFF;border-radius:20px;background:transparent;
              padding:5px 16px;font-family:'Inter',sans-serif;font-size:0.82rem;">The Verdict</span>
      </div>
      <div style="margin-top:16px;font-size:0.75rem;color:#C8A8B4;font-family:'Inter',sans-serif;">
        Data sources: SEC EDGAR, Palantir IR, NATO procurement, U.S. Army contracts, DISA records.
      </div>
    </div>
    """, unsafe_allow_html=True)
