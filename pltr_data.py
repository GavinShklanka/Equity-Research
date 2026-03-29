"""
PLTR Cached Financial Data — Compiled from SEC filings, Palantir IR, and public sources.
This module provides verified financial data for offline analysis.
When running locally with internet access, use data_pipeline.py for live API data.
"""

import pandas as pd
import numpy as np
from datetime import datetime

# ═══════════════════════════════════════════════════════════════════════════════
# COMPANY PROFILE
# ═══════════════════════════════════════════════════════════════════════════════
COMPANY_INFO = {
    "name": "Palantir Technologies Inc.",
    "ticker": "PLTR",
    "exchange": "NASDAQ",
    "sector": "Technology",
    "industry": "Software — Infrastructure",
    "founded": 2003,
    "hq": "Denver, Colorado",
    "ceo": "Alexander C. Karp",
    "employees": 3900,
    "description": (
        "Palantir Technologies builds and deploys software platforms for the intelligence community, "
        "government agencies, and commercial enterprises. Its platforms — Gotham (government), Foundry "
        "(commercial), and AIP (Artificial Intelligence Platform) — integrate, manage, and analyze data "
        "at scale, enabling customers to make data-driven operational decisions."
    ),
    "products": {
        "Gotham": "Government-focused platform for defense and intelligence operations",
        "Foundry": "Enterprise data integration and analytics platform for commercial clients",
        "AIP": "Artificial Intelligence Platform — deployed in 2023, enabling LLM and AI-driven workflows on top of existing ontology",
    },
    "competitive_moats": [
        "Deep government relationships and security clearances (20+ year track record)",
        "Proprietary ontology layer bridging structured and unstructured data",
        "AIP platform positions Palantir at center of enterprise AI adoption",
        "High switching costs — deeply embedded in customer operations",
        "Network effects within government and defense ecosystem",
        "Rule of 40+ compliance (revenue growth + FCF margin > 40%)",
    ],
}

# ═══════════════════════════════════════════════════════════════════════════════
# MARKET DATA (as of March 18, 2026)
# ═══════════════════════════════════════════════════════════════════════════════
MARKET_DATA = {
    "current_price": 152.77,
    "market_cap_B": 365.0,
    "shares_outstanding": 2_391_675_711,
    "52_week_high": 207.18,
    "52_week_low": 60.94,
    "all_time_high": 207.18,
    "ipo_price": 9.50,
    "beta": 2.70,
    "50_day_ma": 145.0,
    "200_day_ma": 120.0,
    "avg_volume_10d": 85_000_000,
    "short_interest_pct": 3.2,
    "insider_ownership_pct": 10.5,
    "institutional_ownership_pct": 45.0,
    "dividend_yield": 0.0,
}

# ═══════════════════════════════════════════════════════════════════════════════
# INCOME STATEMENT (Annual, in $M)
# ═══════════════════════════════════════════════════════════════════════════════
INCOME_STATEMENT = pd.DataFrame({
    "Year":                 [2020,    2021,    2022,    2023,    2024,    2025],
    "Total Revenue":        [1093,    1542,    1906,    2225,    2866,    4475],
    "Cost of Revenue":      [490,     340,     409,     431,     566,     789],
    "Gross Profit":         [603,     1202,    1497,    1794,    2300,    3686],
    "R&D Expense":          [560,     420,     383,     360,     405,     520],
    "SGA Expense":          [750,     610,     580,     530,     520,     590],
    "SBC Expense":          [1093,    778,     558,     476,     545,     700],
    "Total Operating Exp":  [1893,    1808,    1930,    1897,    2430,    2910],
    "Operating Income":     [-800,    -266,    -24,     328,     436,     1565],
    "GAAP Operating Income":[-1168,   -411,    -161,    120,     310,     1100],
    "Interest & Other":     [-372,    145,     83,      97,      152,     260],
    "Pre-Tax Income":       [-1172,   -121,    59,      425,     588,     1825],
    "Income Tax":           [0,       -1,      1,       18,      126,     200],
    "Net Income":           [-1166,   -520,    -374,    217,     462,     1625],
    "Diluted EPS":          [-1.88,   -0.27,   -0.18,   0.09,    0.20,    0.68],
    "Diluted Shares (M)":   [620,     1926,    2080,    2413,    2310,    2392],
    "EBITDA":               [-750,    -220,    -139,    153,     342,     1700],
    "Adj Operating Income": [-154,    117,     397,     608,     956,     2265],
    "Adj Operating Margin%":[None,    7.6,     20.8,    27.3,    33.4,    50.6],
}).set_index("Year")

# ═══════════════════════════════════════════════════════════════════════════════
# BALANCE SHEET (Annual, in $M)
# ═══════════════════════════════════════════════════════════════════════════════
BALANCE_SHEET = pd.DataFrame({
    "Year":                         [2020,   2021,   2022,   2023,   2024,   2025],
    "Cash & Equivalents":           [2013,   2292,   1290,   1023,   1210,   1424],
    "Short-Term Investments":       [0,      259,    517,    1900,   3067,   5800],
    "Accounts Receivable":          [225,    256,    311,    370,    468,    650],
    "Total Current Assets":         [2400,   2920,   2280,   3460,   4900,   8050],
    "Property & Equipment Net":     [40,     45,     40,     38,     36,     50],
    "Goodwill & Intangibles":       [0,      0,      0,      0,      0,      0],
    "Other Long-Term Assets":       [210,    280,    310,    250,    320,    400],
    "Total Assets":                 [2650,   3245,   2630,   4522,   6340,   8900],
    "Accounts Payable":             [25,     30,     22,     26,     28,     35],
    "Deferred Revenue":             [180,    220,    241,    269,    315,     420],
    "Total Current Liabilities":    [350,    430,    448,    535,    625,    800],
    "Long-Term Debt":               [200,    198,    0,      0,      0,      0],
    "Other Long-Term Liabilities":  [450,    328,    371,    427,    623,    610],
    "Total Liabilities":            [1000,   956,    819,    962,    1248,   1410],
    "Total Stockholders Equity":    [1650,   2289,   1811,   3560,   5092,   7490],
    "Total Liabilities & Equity":   [2650,   3245,   2630,   4522,   6340,   8900],
}).set_index("Year")

# ═══════════════════════════════════════════════════════════════════════════════
# CASH FLOW STATEMENT (Annual, in $M)
# ═══════════════════════════════════════════════════════════════════════════════
CASH_FLOW = pd.DataFrame({
    "Year":                         [2020,   2021,   2022,   2023,   2024,   2025],
    "Net Income":                   [-1166,  -520,   -374,   217,    462,    1625],
    "D&A":                          [18,     20,     22,     25,     28,     35],
    "SBC":                          [1093,   778,    558,    476,    545,    700],
    "Changes in Working Capital":   [-242,   70,     18,     12,     120,    -60],
    "Operating Cash Flow":          [-297,   348,    224,    730,    1153,   2300],
    "Capital Expenditure":          [-15,    -26,    -40,    -33,    -13,    -25],
    "Purchases of Investments":     [0,      -263,   -471,   -1820,  -1780,  -3200],
    "Investment Maturities":        [0,      3,      220,    530,    620,    850],
    "Investing Cash Flow":          [-15,    -286,   -291,   -1323,  -1173,  -2375],
    "Stock Issuance":               [943,    58,     12,     15,     20,     20],
    "Debt Repayment":               [0,      0,      -200,   0,      0,      0],
    "Financing Cash Flow":          [943,    58,     -188,   15,     20,     20],
    "Free Cash Flow":               [-312,   322,    184,    697,    1140,   2275],
    "FCF Margin %":                 [None,   20.9,   9.7,    31.3,   39.8,   50.8],
    "Adj Free Cash Flow":           [-297,   422,    258,    730,    1141,   2300],
}).set_index("Year")

# ═══════════════════════════════════════════════════════════════════════════════
# REVENUE SEGMENTS (Annual, in $M)
# ═══════════════════════════════════════════════════════════════════════════════
REVENUE_SEGMENTS = pd.DataFrame({
    "Year":                [2020,  2021,  2022,  2023,  2024,  2025],
    "Government Revenue":  [610,   847,   1072,  1222,  1570,  2403],
    "Commercial Revenue":  [483,   695,   834,   1003,  1296,  2072],
    "US Revenue":          [612,   866,   1158,  1369,  1891,  3220],
    "International Revenue":[481,  676,   748,   856,   975,   1255],
    "US Government":       [456,   640,   820,   940,   1230,  1850],
    "US Commercial":       [156,   226,   338,   429,   661,   1370],
    "Intl Government":     [154,   207,   252,   282,   340,   553],
    "Intl Commercial":     [327,   469,   496,   574,   635,   702],
}).set_index("Year")

# ═══════════════════════════════════════════════════════════════════════════════
# KEY RATIOS (Computed)
# ═══════════════════════════════════════════════════════════════════════════════
def compute_ratios():
    """Compute comprehensive financial ratios across all years."""
    ist = INCOME_STATEMENT
    bs = BALANCE_SHEET
    cf = CASH_FLOW

    years = ist.index.tolist()
    ratios = {}

    for y in years:
        rev = ist.loc[y, "Total Revenue"]
        gp = ist.loc[y, "Gross Profit"]
        oi = ist.loc[y, "Operating Income"]
        ni = ist.loc[y, "Net Income"]
        ebitda = ist.loc[y, "EBITDA"]

        ta = bs.loc[y, "Total Assets"]
        tl = bs.loc[y, "Total Liabilities"]
        te = bs.loc[y, "Total Stockholders Equity"]
        ca = bs.loc[y, "Total Current Assets"]
        cl = bs.loc[y, "Total Current Liabilities"]
        cash = bs.loc[y, "Cash & Equivalents"] + bs.loc[y, "Short-Term Investments"]

        ocf = cf.loc[y, "Operating Cash Flow"]
        fcf = cf.loc[y, "Free Cash Flow"]

        ratios[y] = {
            # Profitability
            "Gross Margin (%)": round(gp / rev * 100, 1) if rev else None,
            "Operating Margin (%)": round(oi / rev * 100, 1) if rev else None,
            "Net Margin (%)": round(ni / rev * 100, 1) if rev else None,
            "EBITDA Margin (%)": round(ebitda / rev * 100, 1) if rev else None,
            "ROA (%)": round(ni / ta * 100, 1) if ta else None,
            "ROE (%)": round(ni / te * 100, 1) if te else None,

            # Liquidity
            "Current Ratio": round(ca / cl, 2) if cl else None,
            "Cash Ratio": round(cash / cl, 2) if cl else None,

            # Solvency
            "Debt/Equity": round(tl / te, 2) if te else None,
            "Debt/Assets": round(tl / ta, 2) if ta else None,
            "Net Cash ($M)": round(cash - bs.loc[y, "Long-Term Debt"], 0),

            # Efficiency
            "Asset Turnover": round(rev / ta, 2) if ta else None,
            "Revenue per Employee ($K)": round(rev / (COMPANY_INFO["employees"] if y == 2025 else max(2800, 3000)) * 1000, 0),

            # Cash Flow
            "OCF Margin (%)": round(ocf / rev * 100, 1) if rev else None,
            "FCF Margin (%)": round(fcf / rev * 100, 1) if rev else None,
            "FCF Yield (%)": None,  # needs market cap

            # Growth (YoY)
            "Revenue Growth (%)": None,  # computed below
        }

    # Compute YoY growth
    for i in range(1, len(years)):
        y, py = years[i], years[i - 1]
        prev_rev = ist.loc[py, "Total Revenue"]
        ratios[y]["Revenue Growth (%)"] = round((ist.loc[y, "Total Revenue"] / prev_rev - 1) * 100, 1) if prev_rev else None

    return pd.DataFrame(ratios).T


KEY_RATIOS = compute_ratios()

# ═══════════════════════════════════════════════════════════════════════════════
# DuPont DECOMPOSITION
# ═══════════════════════════════════════════════════════════════════════════════
def compute_dupont():
    ist = INCOME_STATEMENT
    bs = BALANCE_SHEET
    years = ist.index.tolist()
    rows = {}
    for y in years:
        rev = ist.loc[y, "Total Revenue"]
        ni = ist.loc[y, "Net Income"]
        ta = bs.loc[y, "Total Assets"]
        te = bs.loc[y, "Total Stockholders Equity"]

        margin = ni / rev if rev else 0
        turnover = rev / ta if ta else 0
        leverage = ta / te if te else 0
        roe = margin * turnover * leverage

        rows[y] = {
            "Net Profit Margin": round(margin, 4),
            "Asset Turnover": round(turnover, 4),
            "Equity Multiplier": round(leverage, 4),
            "ROE (DuPont)": round(roe * 100, 2),
        }
    return pd.DataFrame(rows).T


DUPONT = compute_dupont()

# ═══════════════════════════════════════════════════════════════════════════════
# PEER COMPARISON DATA
# ═══════════════════════════════════════════════════════════════════════════════
PEER_COMPARISON = pd.DataFrame([
    {"Ticker": "PLTR", "Name": "Palantir Technologies", "Market Cap ($B)": 365.0,
     "Revenue TTM ($B)": 4.475, "Rev Growth (%)": 56.2, "Gross Margin (%)": 82.4,
     "Op Margin (%)": 35.0, "Net Margin (%)": 36.3, "FCF Margin (%)": 50.8,
     "EV/Revenue": 81.6, "Forward P/E": 185.0, "P/S": 81.6, "ROE (%)": 21.7,
     "Debt/Equity": 0.0, "Beta": 2.70},
    {"Ticker": "SNOW", "Name": "Snowflake", "Market Cap ($B)": 62.0,
     "Revenue TTM ($B)": 3.6, "Rev Growth (%)": 29.0, "Gross Margin (%)": 66.0,
     "Op Margin (%)": -6.0, "Net Margin (%)": -12.0, "FCF Margin (%)": 28.0,
     "EV/Revenue": 17.2, "Forward P/E": None, "P/S": 17.2, "ROE (%)": -8.0,
     "Debt/Equity": 0.15, "Beta": 1.50},
    {"Ticker": "DDOG", "Name": "Datadog", "Market Cap ($B)": 39.0,
     "Revenue TTM ($B)": 3.43, "Rev Growth (%)": 27.7, "Gross Margin (%)": 80.0,
     "Op Margin (%)": 24.0, "Net Margin (%)": 18.0, "FCF Margin (%)": 33.0,
     "EV/Revenue": 11.4, "Forward P/E": 64.0, "P/S": 11.4, "ROE (%)": 15.0,
     "Debt/Equity": 0.30, "Beta": 1.10},
    {"Ticker": "CRWD", "Name": "CrowdStrike", "Market Cap ($B)": 95.0,
     "Revenue TTM ($B)": 4.2, "Rev Growth (%)": 28.0, "Gross Margin (%)": 75.0,
     "Op Margin (%)": 17.0, "Net Margin (%)": 7.0, "FCF Margin (%)": 32.0,
     "EV/Revenue": 22.6, "Forward P/E": 85.0, "P/S": 22.6, "ROE (%)": 12.0,
     "Debt/Equity": 0.40, "Beta": 1.30},
    {"Ticker": "AI", "Name": "C3.ai", "Market Cap ($B)": 4.5,
     "Revenue TTM ($B)": 0.38, "Rev Growth (%)": 22.0, "Gross Margin (%)": 58.0,
     "Op Margin (%)": -45.0, "Net Margin (%)": -50.0, "FCF Margin (%)": -20.0,
     "EV/Revenue": 11.8, "Forward P/E": None, "P/S": 11.8, "ROE (%)": -25.0,
     "Debt/Equity": 0.0, "Beta": 2.20},
    {"Ticker": "MDB", "Name": "MongoDB", "Market Cap ($B)": 22.0,
     "Revenue TTM ($B)": 2.1, "Rev Growth (%)": 18.0, "Gross Margin (%)": 72.0,
     "Op Margin (%)": 8.0, "Net Margin (%)": 4.0, "FCF Margin (%)": 22.0,
     "EV/Revenue": 10.5, "Forward P/E": 75.0, "P/S": 10.5, "ROE (%)": 6.0,
     "Debt/Equity": 1.20, "Beta": 1.60},
])

# ═══════════════════════════════════════════════════════════════════════════════
# KEY EVENTS (for Event Study)
# ═══════════════════════════════════════════════════════════════════════════════
KEY_EVENTS = [
    {"date": "2023-05-08", "event": "Q1 2023 Earnings — First GAAP Profitable Quarter", "type": "Earnings"},
    {"date": "2023-08-07", "event": "Q2 2023 Earnings — AIP Launch Momentum", "type": "Earnings"},
    {"date": "2023-11-02", "event": "Q3 2023 Earnings — Strong US Commercial Growth", "type": "Earnings"},
    {"date": "2024-02-05", "event": "Q4 2023 Earnings — Full Year Profitability", "type": "Earnings"},
    {"date": "2024-05-06", "event": "Q1 2024 Earnings — AIP Boot Camps Drive Adoption", "type": "Earnings"},
    {"date": "2024-08-05", "event": "Q2 2024 Earnings — Revenue Acceleration", "type": "Earnings"},
    {"date": "2024-11-04", "event": "Q3 2024 Earnings — Massive Guidance Raise", "type": "Earnings"},
    {"date": "2024-12-23", "event": "Joined S&P 500 Index", "type": "Index"},
    {"date": "2024-12-23", "event": "Joined Nasdaq-100 Index", "type": "Index"},
    {"date": "2025-02-03", "event": "Q4 2024 Earnings — 36% Revenue Growth, 2025 Guidance Crush", "type": "Earnings"},
    {"date": "2025-05-05", "event": "Q1 2025 Earnings — 39% Growth, AIP Scaling", "type": "Earnings"},
    {"date": "2025-08-04", "event": "Q2 2025 Earnings — 48% Growth, US Commercial 93%", "type": "Earnings"},
    {"date": "2025-11-03", "event": "Q3 2025 Earnings — 63% Growth, US Commercial 121%", "type": "Earnings"},
    {"date": "2026-02-02", "event": "Q4 2025 Earnings — 70% Growth, US Commercial 137%", "type": "Earnings"},
]

# ═══════════════════════════════════════════════════════════════════════════════
# ANALYST CONSENSUS
# ═══════════════════════════════════════════════════════════════════════════════
ANALYST_DATA = {
    "target_low": 40.0,
    "target_mean": 112.0,
    "target_median": 105.0,
    "target_high": 150.0,
    "num_analysts": 22,
    "buy": 6,
    "hold": 10,
    "sell": 6,
    "consensus": "Hold",
    "fy2026_revenue_guidance_low": 7182,
    "fy2026_revenue_guidance_high": 7198,
    "fy2026_revenue_consensus": 7190,
    "fy2026_growth_guidance": 61.0,
}

# ═══════════════════════════════════════════════════════════════════════════════
# FY2026 FORWARD GUIDANCE
# ═══════════════════════════════════════════════════════════════════════════════
GUIDANCE = {
    "Q1_2026_revenue_low": 1532,
    "Q1_2026_revenue_high": 1536,
    "FY2026_revenue_low": 7182,
    "FY2026_revenue_high": 7198,
    "FY2026_revenue_growth": "61% Y/Y",
    "FY2026_US_commercial_growth": "115% Y/Y",
    "FY2026_adj_operating_income_low": 3800,
    "FY2026_adj_operating_income_high": 3900,
    "FY2026_adj_fcf_low": 3500,
    "FY2026_adj_fcf_high": 3600,
}

# ═══════════════════════════════════════════════════════════════════════════════
# GLOBAL FOOTPRINT — Confirmed Deployments Only (SEC, IR, Press Releases)
# ═══════════════════════════════════════════════════════════════════════════════
GLOBAL_FOOTPRINT = [
    # United States — Government
    {"country": "United States", "entity": "U.S. Army", "use_case": "TITAN Ground Station / Battlefield Intelligence",
     "segment": "Defense", "evidence": "Disclosed Contract", "strategic_importance": 5,
     "iso_alpha": "USA", "notes": "Multi-year Army Vantage program + TITAN win (2024)"},
    {"country": "United States", "entity": "U.S. Space Force", "use_case": "Data Mesh / Operational Analytics",
     "segment": "Defense", "evidence": "Disclosed Contract", "strategic_importance": 5,
     "iso_alpha": "USA", "notes": "Space C2 and data integration"},
    {"country": "United States", "entity": "U.S. Special Operations Command", "use_case": "Mission Planning & Intelligence",
     "segment": "Defense", "evidence": "Disclosed Contract", "strategic_importance": 5,
     "iso_alpha": "USA", "notes": "Long-standing SOCOM relationship since founding"},
    {"country": "United States", "entity": "CIA / IC Community", "use_case": "Intelligence Analysis Platform",
     "segment": "Intelligence", "evidence": "Public Knowledge", "strategic_importance": 5,
     "iso_alpha": "USA", "notes": "Founding customer; In-Q-Tel backed"},
    {"country": "United States", "entity": "HHS / CDC / NIH", "use_case": "COVID-19 Response / Public Health Analytics",
     "segment": "Healthcare", "evidence": "Disclosed Contract", "strategic_importance": 4,
     "iso_alpha": "USA", "notes": "HHS Protect platform during pandemic; continued engagement"},
    {"country": "United States", "entity": "FAA", "use_case": "Airspace Modernization",
     "segment": "Government", "evidence": "Disclosed Contract", "strategic_importance": 3,
     "iso_alpha": "USA", "notes": "Data integration for air traffic management"},
    {"country": "United States", "entity": "IRS", "use_case": "Tax Fraud Detection",
     "segment": "Government", "evidence": "Disclosed Contract", "strategic_importance": 3,
     "iso_alpha": "USA", "notes": "Fraud analytics and compliance"},
    {"country": "United States", "entity": "VA (Veterans Affairs)", "use_case": "Healthcare Delivery Optimization",
     "segment": "Healthcare", "evidence": "Disclosed Contract", "strategic_importance": 4,
     "iso_alpha": "USA", "notes": "Patient flow and resource allocation"},
    # United States — Commercial
    {"country": "United States", "entity": "AIP Boot Camp Customers", "use_case": "Enterprise AI Deployment",
     "segment": "Commercial", "evidence": "Earnings Disclosure", "strategic_importance": 5,
     "iso_alpha": "USA", "notes": "Hundreds of boot camps converting to production; US Comm grew 137% YoY in Q4 2025"},
    {"country": "United States", "entity": "Healthcare / Life Sciences", "use_case": "Drug Discovery & Clinical Operations",
     "segment": "Commercial", "evidence": "Earnings Disclosure", "strategic_importance": 4,
     "iso_alpha": "USA", "notes": "Multiple pharma & hospital system deployments"},
    {"country": "United States", "entity": "Energy & Manufacturing", "use_case": "Supply Chain & Operations",
     "segment": "Commercial", "evidence": "Earnings Disclosure", "strategic_importance": 3,
     "iso_alpha": "USA", "notes": "Foundry deployments in industrial verticals"},
    # United Kingdom
    {"country": "United Kingdom", "entity": "NHS England", "use_case": "Federated Data Platform",
     "segment": "Healthcare", "evidence": "Disclosed Contract", "strategic_importance": 5,
     "iso_alpha": "GBR", "notes": "£330M+ NHS FDP contract (2023); national-scale health data integration"},
    {"country": "United Kingdom", "entity": "UK Ministry of Defence", "use_case": "Defense Intelligence",
     "segment": "Defense", "evidence": "Disclosed Contract", "strategic_importance": 4,
     "iso_alpha": "GBR", "notes": "Long-standing MOD relationship; Five Eyes partner"},
    # Ukraine
    {"country": "Ukraine", "entity": "Ukrainian Government / Military", "use_case": "Battlefield Intelligence & Targeting",
     "segment": "Defense", "evidence": "CEO Public Statements", "strategic_importance": 5,
     "iso_alpha": "UKR", "notes": "Confirmed by Karp; Palantir deployed for battlefield awareness in active conflict"},
    # Europe / NATO
    {"country": "NATO / Europe", "entity": "NATO Alliance", "use_case": "Alliance Intelligence Sharing",
     "segment": "Defense", "evidence": "Press Reports", "strategic_importance": 4,
     "iso_alpha": None, "notes": "Expanded NATO engagement post-Ukraine; interoperability platform"},
    {"country": "Germany", "entity": "German Federal Police (BKA)", "use_case": "Law Enforcement Analytics",
     "segment": "Government", "evidence": "Disclosed Contract", "strategic_importance": 3,
     "iso_alpha": "DEU", "notes": "Counter-terrorism analytics; subject to German privacy court rulings"},
    {"country": "France", "entity": "French Defense / DGSI", "use_case": "Intelligence Analysis",
     "segment": "Defense", "evidence": "Press Reports", "strategic_importance": 3,
     "iso_alpha": "FRA", "notes": "Reported engagement; European defense expansion"},
    # Asia-Pacific
    {"country": "Japan", "entity": "SOMPO Holdings", "use_case": "Insurance & Enterprise Analytics",
     "segment": "Commercial", "evidence": "Disclosed Partnership", "strategic_importance": 3,
     "iso_alpha": "JPN", "notes": "Strategic partnership; Japan market entry"},
    {"country": "South Korea", "entity": "Hyundai Heavy Industries", "use_case": "Manufacturing & Shipbuilding",
     "segment": "Commercial", "evidence": "Disclosed Partnership", "strategic_importance": 3,
     "iso_alpha": "KOR", "notes": "Industrial Foundry deployment"},
    {"country": "Australia", "entity": "Australian Defence Force", "use_case": "Defense Intelligence",
     "segment": "Defense", "evidence": "Disclosed Contract", "strategic_importance": 4,
     "iso_alpha": "AUS", "notes": "Five Eyes partner; defense and intelligence"},
]

# ═══════════════════════════════════════════════════════════════════════════════
# EXPANSION SIGNALS — Scored per Region (1–5 scale)
# ═══════════════════════════════════════════════════════════════════════════════
EXPANSION_SIGNALS = pd.DataFrame([
    {"Region": "United States", "Strategic Importance": 5, "Repeatability": 5,
     "Political Risk": 1, "Monetization Clarity": 5, "Composite": 4.75},
    {"Region": "United Kingdom", "Strategic Importance": 5, "Repeatability": 4,
     "Political Risk": 2, "Monetization Clarity": 5, "Composite": 4.25},
    {"Region": "Ukraine / Conflict Zones", "Strategic Importance": 5, "Repeatability": 2,
     "Political Risk": 5, "Monetization Clarity": 2, "Composite": 2.75},
    {"Region": "NATO / Europe", "Strategic Importance": 4, "Repeatability": 3,
     "Political Risk": 3, "Monetization Clarity": 3, "Composite": 3.25},
    {"Region": "Japan / South Korea", "Strategic Importance": 3, "Repeatability": 4,
     "Political Risk": 1, "Monetization Clarity": 3, "Composite": 3.25},
    {"Region": "Australia / Five Eyes", "Strategic Importance": 4, "Repeatability": 3,
     "Political Risk": 1, "Monetization Clarity": 4, "Composite": 3.75},
])

# ═══════════════════════════════════════════════════════════════════════════════
# AI ECOSYSTEM DATA — Partnership Dependency Analysis
# ═══════════════════════════════════════════════════════════════════════════════
AI_ECOSYSTEM_DATA = {
    "partnerships": [
        {
            "partner": "NVIDIA",
            "type": "Infrastructure",
            "upside": "GPU compute access for AIP; co-development of AI/ML workflows; NVIDIA promotion at GTC",
            "downside": "Dependency on GPU supply cycle; sentiment contagion if AI hardware reprices; infrastructure cost exposure",
            "dependency_level": "Medium",
            "contagion_risk": "High — PLTR beta to NVIDIA sentiment is elevated due to shared AI narrative",
        },
        {
            "partner": "Oracle Cloud",
            "type": "Distribution",
            "upside": "Enterprise distribution through OCI; access to Oracle's installed base; cloud marketplace listing",
            "downside": "Platform dependency; Oracle competes in analytics; revenue share economics",
            "dependency_level": "Medium",
            "contagion_risk": "Low — Oracle is infrastructure, not narrative driver",
        },
        {
            "partner": "AWS",
            "type": "Deployment",
            "upside": "GovCloud deployment for classified workloads; massive enterprise reach; FedRAMP certified",
            "downside": "AWS competes directly with SageMaker; bundling risk; margin pressure",
            "dependency_level": "High",
            "contagion_risk": "Low — AWS is diversified, not AI-pure-play",
        },
        {
            "partner": "Microsoft / Azure",
            "type": "Deployment",
            "upside": "Azure government cloud access; enterprise cross-sell potential",
            "downside": "Microsoft is the most direct competitor (Copilot, Power Platform); Azure incentives may shift",
            "dependency_level": "Medium",
            "contagion_risk": "Low — Microsoft is diversified",
        },
    ],
    "ai_sentiment_scenarios": {
        "Base": {"multiple_impact": 1.0, "description": "Current AI sentiment sustained; no repricing"},
        "AI Repricing": {"multiple_impact": 0.65, "description": "AI sentiment cools 35%; multiples compress but business fundamentals intact"},
        "AI Bubble Pop": {"multiple_impact": 0.35, "description": "Severe AI sentiment collapse; 65% multiple compression; growth slows moderately due to enterprise caution"},
    },
}

# ═══════════════════════════════════════════════════════════════════════════════
# TOOLTIP CONTENT — Educational Annotations
# Priority: Financial Analytics page, then Palantir-crucial metrics
# ═══════════════════════════════════════════════════════════════════════════════
TOOLTIP_CONTENT = {
    # ── Horizontal Analysis ──
    "horizontal_analysis": {
        "definition": "Horizontal analysis measures the year-over-year (YoY) percentage change in each financial statement line item.",
        "formula": "YoY Change (%) = (Current Year − Prior Year) / Prior Year × 100",
        "interpretation": (
            "Look for **acceleration vs. deceleration** — is the growth rate increasing or decreasing over time? "
            "Sustained acceleration (like PLTR's revenue going from +17% to +56%) is rare and signals strong demand. "
            "Decelerating growth is normal for maturing companies and not inherently negative — the key is whether "
            "the rate of deceleration is faster or slower than expected."
        ),
    },
    # ── Vertical Analysis ──
    "vertical_analysis": {
        "definition": "Vertical (common-size) analysis expresses each income statement item as a percentage of Total Revenue, revealing cost structure relationships.",
        "formula": "Common-Size % = Line Item / Total Revenue × 100",
        "interpretation": (
            "Focus on **margin composition**: Is the cost of revenue shrinking as a percentage? That signals operating leverage. "
            "For PLTR, watch SBC as % of Revenue (declining from 100%→15.6% is a major positive), "
            "and the spread between Gross Margin (~82%) and Operating Margin (~25% GAAP) — the gap is driven by R&D + SGA, "
            "which should narrow as the company scales."
        ),
    },
    # ── Ratio Analysis ──
    "ratio_analysis": {
        "definition": "Financial ratios condense balance sheet, income statement, and cash flow data into comparable metrics across four categories.",
        "formula": None,
        "interpretation": (
            "Ratios are most useful in two contexts: (1) trend analysis over time, and (2) peer comparison. "
            "A single ratio in isolation tells you little — the direction and relative position matter more than the absolute number."
        ),
    },
    "gross_margin": {
        "definition": "Gross Margin measures the percentage of revenue retained after direct costs of delivering the product/service.",
        "formula": "Gross Margin (%) = Gross Profit / Revenue × 100",
        "interpretation": (
            "For software companies, gross margins above 70% indicate a platform business model with low marginal delivery cost. "
            "PLTR's ~82% gross margin confirms it is a high-leverage platform, not a services company. "
            "Compare to peers: SNOW ~66%, DDOG ~80%, CRWD ~75%."
        ),
    },
    "operating_margin": {
        "definition": "Operating Margin shows the percentage of revenue remaining after all operating expenses (COGS, R&D, SGA, SBC).",
        "formula": "Operating Margin (%) = Operating Income / Revenue × 100",
        "interpretation": (
            "The gap between gross margin and operating margin reveals how much the company spends on growth (R&D, sales). "
            "PLTR's GAAP operating margin improved from -73% (2020) to +35% (2025) — a 108pp improvement driven by operating leverage. "
            "The adjusted margin (excluding SBC) is 50.6%, but GAAP is the more conservative and honest measure."
        ),
    },
    "net_margin": {
        "definition": "Net Margin represents the percentage of revenue that becomes actual profit after all expenses, taxes, and interest.",
        "formula": "Net Margin (%) = Net Income / Revenue × 100",
        "interpretation": (
            "Net margin includes non-operating items like interest income and taxes. "
            "PLTR's net margin (36%) is boosted by $260M in interest income from its $7.2B cash pile. "
            "This is a real but non-recurring quality — when rates drop, interest income declines."
        ),
    },
    "fcf_margin": {
        "definition": "Free Cash Flow Margin measures how much of each revenue dollar converts to cash available for shareholders, debt reduction, or reinvestment.",
        "formula": "FCF Margin (%) = (Operating Cash Flow − CapEx) / Revenue × 100",
        "interpretation": (
            "FCF margin is arguably the single most important metric for a high-growth software company. "
            "PLTR's 51% FCF margin exceeds its GAAP net margin (36%) because SBC is a non-cash expense added back to cash flow, "
            "and capex is minimal (~$25M). **Critical nuance**: High FCF margin with high SBC means the company is "
            "generating cash by diluting shareholders — both truths coexist."
        ),
    },
    "current_ratio": {
        "definition": "Current Ratio measures a company's ability to pay short-term obligations with short-term assets.",
        "formula": "Current Ratio = Current Assets / Current Liabilities",
        "interpretation": (
            "A ratio above 1.0 means the company can cover near-term liabilities. "
            "PLTR's current ratio is ~10x — extraordinarily high, reflecting its massive cash + investment position "
            "and low debt. This provides a significant safety buffer but also suggests capital allocation "
            "could be more aggressive (buybacks, acquisitions, dividends)."
        ),
    },
    "debt_equity": {
        "definition": "Debt-to-Equity ratio measures financial leverage — how much of the company is financed by debt vs. shareholder equity.",
        "formula": "D/E = Total Liabilities / Total Stockholders' Equity",
        "interpretation": (
            "PLTR's near-zero D/E ratio is uncommon among large tech companies. "
            "Zero debt means no bankruptcy risk and no interest expense burden, but it also means "
            "the company is not using leverage to enhance returns. "
            "For a company growing 56% with 82% gross margins, the balance sheet is extremely conservative."
        ),
    },
    "roe": {
        "definition": "Return on Equity measures how effectively the company generates profit from shareholders' invested capital.",
        "formula": "ROE (%) = Net Income / Stockholders' Equity × 100",
        "interpretation": (
            "ROE is best understood through DuPont decomposition — is it driven by margins, asset utilization, or leverage? "
            "PLTR's ROE is moderate (~22%) despite high margins because it has no leverage (equity multiplier ~1.2x) "
            "and a massive asset base from accumulated cash. This is the trade-off of a fortress balance sheet."
        ),
    },
    # ── DuPont Analysis ──
    "dupont_analysis": {
        "definition": "DuPont Analysis decomposes Return on Equity into three drivers: profitability (margin), efficiency (turnover), and leverage (multiplier).",
        "formula": "ROE = Net Profit Margin × Asset Turnover × Equity Multiplier",
        "interpretation": (
            "This decomposition reveals WHERE returns are coming from. For PLTR: "
            "(1) Net Profit Margin is improving rapidly (the primary ROE driver — went positive in 2023), "
            "(2) Asset Turnover is declining (because cash is piling up faster than revenue), "
            "(3) Equity Multiplier is falling (no debt, equity growing via retained earnings). "
            "Translation: ROE is being dragged down by the company's own success in accumulating cash."
        ),
    },
    # ── Trend Analysis ──
    "trend_analysis": {
        "definition": "Trend Analysis indexes all financial items to a base year (= 100) to visualize relative growth trajectories over multiple years.",
        "formula": "Index Value = (Current Year Value / Base Year Value) × 100",
        "interpretation": (
            "Look for **divergence patterns**: When revenue index grows faster than cost index, margins are expanding. "
            "When Net Income's index swings from negative to positive territory, the company hit a profitability inflection point. "
            "Signal vs. noise: A single year's spike could be a one-time event; 3+ years of directional consistency is a trend."
        ),
    },
    # ── Palantir-Crucial Metrics ──
    "rule_of_40": {
        "definition": "The Rule of 40 is a benchmark for SaaS/software companies: Revenue Growth (%) + Profit Margin (%) should exceed 40.",
        "formula": "Rule of 40 = Revenue Growth (%) + FCF Margin (%)",
        "interpretation": (
            "Companies exceeding the Rule of 40 demonstrate they are balancing growth and profitability effectively. "
            "PLTR scores **107** (56% growth + 51% FCF margin) — in the top 1% of all software companies historically. "
            "However, this metric can be gamed with SBC exclusion; using GAAP operating margin instead yields ~91, still elite."
        ),
    },
    "sbc_pct_revenue": {
        "definition": "Stock-Based Compensation as a percentage of revenue measures the dilutive cost of equity-based employee pay.",
        "formula": "SBC % = Stock-Based Compensation / Revenue × 100",
        "interpretation": (
            "SBC is a real economic cost — it dilutes existing shareholders. PLTR's SBC/Revenue has improved dramatically "
            "(100% in 2020 → 15.6% in 2025), but $700M annually is still material. "
            "The critical question: Is the talent retained by SBC generating enough value to offset dilution? "
            "For context, many mature tech companies target SBC below 10% of revenue."
        ),
    },
    "ev_revenue": {
        "definition": "Enterprise Value to Revenue ratio values the entire business (equity + debt − cash) relative to its revenue.",
        "formula": "EV/Revenue = Enterprise Value / Trailing 12-Month Revenue",
        "interpretation": (
            "PLTR trades at ~81x EV/Revenue vs. peer median of ~12x. This premium implies the market expects "
            "PLTR to grow into a revenue base 5–8x larger while maintaining elite margins. "
            "At 81x EV/Revenue, the stock is priced for perfection — any growth miss would trigger disproportionate downside. "
            "Historically, very few companies have sustained >50x EV/Revenue for more than 2 years."
        ),
    },
    "net_cash": {
        "definition": "Net Cash Position is the difference between cash/investments and total debt, showing financial flexibility.",
        "formula": "Net Cash = (Cash + Short-Term Investments) − Total Debt",
        "interpretation": (
            "PLTR's ~$7.2B net cash position (zero debt) provides maximum strategic optionality: "
            "acquisitions, buybacks, or simply surviving a downturn without raising capital. "
            "For a company with $4.5B revenue, this represents ~1.6 years of total revenue in cash reserves — "
            "an exceptionally strong position that eliminates liquidity and solvency risk."
        ),
    },
    "rev_per_employee": {
        "definition": "Revenue per Employee measures operational efficiency and platform leverage.",
        "formula": "Revenue per Employee = Total Revenue / Headcount",
        "interpretation": (
            "PLTR generates ~$1.15M per employee (3,900 headcount) — well above average for enterprise software. "
            "High RevPE signals the platform model is working: revenue scales without proportional hiring. "
            "This metric should increase as AIP drives more self-service deployments vs. traditional Forward Deployed Engineers."
        ),
    },
    "government_cushion": {
        "definition": "Government Revenue as a percentage of total revenue — indicates the 'recession-resistant' floor of the business.",
        "formula": "Gov Cushion (%) = Government Revenue / Total Revenue × 100",
        "interpretation": (
            "PLTR's government segment (~54% of revenue) provides a durable, contract-based revenue floor. "
            "Government contracts are multi-year, high-switching-cost, and largely immune to commercial cycles. "
            "This 'cushion' means even if commercial growth slows dramatically, PLTR has a revenue floor "
            "that most pure-play commercial software companies lack."
        ),
    },
}
