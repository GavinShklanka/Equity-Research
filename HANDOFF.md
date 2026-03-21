# PLTR Equity Research — Sonnet Handoff

## Project Context
- **Student**: Gavin, MBAN student at Saint Mary's University (Sobey School of Business)
- **Course**: MBAN5570 Accounting & Financial Analytics, Dr. Mohammad M. Rahaman
- **Project**: Equity Research Analytics (25% of grade), company = Palantir Technologies (PLTR)
- **Deliverables**: (1) Streamlit Dashboard, (2) White Paper (.docx, max 6 pages + exhibits), (3) Presentation Deck (.pptx, 10 min)

## What's Complete
1. **pltr_data.py** — Comprehensive cached financial data (IS, BS, CF 2020–2025, revenue segments, key ratios, DuPont, peer comparison, analyst data, guidance, key events)
2. **data_pipeline.py** — Live API pipeline (yfinance, SEC EDGAR) for when run locally with internet
3. **app.py** — Full 9-page Streamlit dashboard with premium dark theme CSS:
   - Executive Summary (KPIs, revenue/margin charts, investment thesis, analyst consensus)
   - Business Overview (products, revenue segments, competitive moats)
   - Financial Statements (IS, BS, CF with interactive charts, FCF waterfall)
   - Financial Analytics (Horizontal, Vertical, Ratio, DuPont, Trend analysis — all per MBAN5570)
   - Valuation Models (interactive DCF with sliders, comparable company, sensitivity heatmap, scenario analysis)
   - Risk & Monte Carlo (GBM simulation with configurable params, fan chart, distribution, risk factors)
   - Peer Comparison (radar chart, EV/Revenue, Rule of 40)
   - AI-Assisted Analysis (per course section 2.B)
   - Critical Evaluation (per course section 2.C: What AI got right/wrong/accepted/discarded)
4. **requirements.txt** — Python dependencies

## What Remains (TODO)
1. **White Paper (.docx)** — Max 6 pages + exhibits. Must use the docx SKILL. Content comes from dashboard analysis. Structure per course outline: Traditional Research → AI-Assisted → Critical Evaluation. Professor quote: "I am not looking for length. I am looking for clarity, structure, analytical discipline, and insight."
2. **Presentation Deck (.pptx)** — 10-minute presentation. Must use the pptx SKILL. Visual, concise, data-driven slides covering the equity research highlights.
3. **Final verification** — Test Streamlit runs locally, review all numbers for accuracy.

## Key Course Requirements (from outline)
- **Section 2.A** Traditional: Business Model, Governance, Competitive Advantage, Industry Analysis, Risk Factors, BS/IS/CF Analysis, Capital Allocation, Trend Analysis, Valuation, Forward Guidance, Shareholder Value (EPS + Dividend)
- **Section 2.B** AI-Assisted: Summarizing financials, identifying risks/trends, generating scenarios, extracting patterns, visualizations
- **Section 2.C** Critical Evaluation: What AI Got Right, Wrong, Accept, Discarded, How AI Enhances Research
- **Grading**: Rigor, clarity, sophistication, ability to interpret and communicate insights
- **Groups of 2, White Paper max 6 pages + exhibits**

## File Locations
- All project files: `/sessions/wizardly-wonderful-pasteur/mnt/rbc/SCHOOL/PLTR_Equity_Research/`
- Course materials: `/sessions/wizardly-wonderful-pasteur/mnt/uploads/`
- Skills: `/sessions/wizardly-wonderful-pasteur/mnt/.skills/skills/`

## Important Notes
- Dashboard uses cached data (pltr_data.py) because sandbox blocks yfinance API calls
- When Gavin runs locally: `cd PLTR_Equity_Research && pip install -r requirements.txt && streamlit run app.py`
- Gavin is bullish on PLTR but wants rigorous fundamental analysis, not anchoring bias
- Professor values clarity and insight over length
