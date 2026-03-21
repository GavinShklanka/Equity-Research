"""
PLTR Equity Research — Core Data Pipeline
Pulls historical prices, financial statements, key metrics from yfinance & SEC EDGAR.
"""

import yfinance as yf
import pandas as pd
import numpy as np
import requests
import json
from datetime import datetime, timedelta
from functools import lru_cache

# ── Config ──────────────────────────────────────────────────────────────────
TICKER = "PLTR"
PEERS = ["SNOW", "DDOG", "AI", "CRWD", "MDB"]  # Comparable companies
SEC_HEADERS = {"User-Agent": "GavinResearch gavin@research.edu"}
EDGAR_CIK = "0001321655"  # Palantir's CIK


# ── yfinance Data Fetcher ───────────────────────────────────────────────────
class PLTRDataPipeline:
    def __init__(self, ticker=TICKER):
        self.ticker_str = ticker
        self.ticker = yf.Ticker(ticker)
        self._info = None

    @property
    def info(self):
        if self._info is None:
            self._info = self.ticker.info
        return self._info

    # ── Price Data ──────────────────────────────────────────────────────────
    def get_historical_prices(self, period="5y", interval="1d"):
        """Fetch OHLCV price history."""
        df = self.ticker.history(period=period, interval=interval)
        df.index = df.index.tz_localize(None) if df.index.tz else df.index
        return df

    def get_intraday_prices(self, period="5d", interval="15m"):
        """Fetch intraday price data."""
        df = self.ticker.history(period=period, interval=interval)
        df.index = df.index.tz_localize(None) if df.index.tz else df.index
        return df

    # ── Financial Statements ────────────────────────────────────────────────
    def get_income_statement(self, quarterly=False):
        """Income Statement — Annual or Quarterly."""
        return self.ticker.quarterly_financials.T if quarterly else self.ticker.financials.T

    def get_balance_sheet(self, quarterly=False):
        """Balance Sheet — Annual or Quarterly."""
        return self.ticker.quarterly_balance_sheet.T if quarterly else self.ticker.balance_sheet.T

    def get_cash_flow(self, quarterly=False):
        """Cash Flow Statement — Annual or Quarterly."""
        return self.ticker.quarterly_cashflow.T if quarterly else self.ticker.cashflow.T

    # ── Key Metrics & Ratios ────────────────────────────────────────────────
    def get_key_metrics(self):
        """Extract key financial metrics from yfinance info."""
        i = self.info
        metrics = {
            "Company": i.get("shortName", self.ticker_str),
            "Sector": i.get("sector", "N/A"),
            "Industry": i.get("industry", "N/A"),
            "Market Cap": i.get("marketCap", 0),
            "Enterprise Value": i.get("enterpriseValue", 0),
            "Trailing P/E": i.get("trailingPE", None),
            "Forward P/E": i.get("forwardPE", None),
            "PEG Ratio": i.get("pegRatio", None),
            "Price/Sales (TTM)": i.get("priceToSalesTrailing12Months", None),
            "Price/Book": i.get("priceToBook", None),
            "EV/Revenue": i.get("enterpriseToRevenue", None),
            "EV/EBITDA": i.get("enterpriseToEbitda", None),
            "Profit Margin": i.get("profitMargins", None),
            "Operating Margin": i.get("operatingMargins", None),
            "ROE": i.get("returnOnEquity", None),
            "ROA": i.get("returnOnAssets", None),
            "Revenue (TTM)": i.get("totalRevenue", 0),
            "Revenue Growth (YoY)": i.get("revenueGrowth", None),
            "Earnings Growth": i.get("earningsGrowth", None),
            "Free Cash Flow": i.get("freeCashflow", 0),
            "Total Cash": i.get("totalCash", 0),
            "Total Debt": i.get("totalDebt", 0),
            "Current Ratio": i.get("currentRatio", None),
            "Quick Ratio": i.get("quickRatio", None),
            "Debt/Equity": i.get("debtToEquity", None),
            "Beta": i.get("beta", None),
            "52-Week High": i.get("fiftyTwoWeekHigh", None),
            "52-Week Low": i.get("fiftyTwoWeekLow", None),
            "50-Day MA": i.get("fiftyDayAverage", None),
            "200-Day MA": i.get("twoHundredDayAverage", None),
            "Shares Outstanding": i.get("sharesOutstanding", 0),
            "Float": i.get("floatShares", 0),
            "Insider Ownership": i.get("heldPercentInsiders", None),
            "Institutional Ownership": i.get("heldPercentInstitutions", None),
            "Short Ratio": i.get("shortRatio", None),
            "Dividend Yield": i.get("dividendYield", None),
            "EPS (TTM)": i.get("trailingEps", None),
            "Forward EPS": i.get("forwardEps", None),
            "Target Mean Price": i.get("targetMeanPrice", None),
            "Recommendation": i.get("recommendationKey", "N/A"),
        }
        return metrics

    # ── Analyst Recommendations ─────────────────────────────────────────────
    def get_analyst_recommendations(self):
        """Fetch analyst recommendations history."""
        try:
            return self.ticker.recommendations
        except Exception:
            return pd.DataFrame()

    def get_analyst_price_targets(self):
        """Get analyst price target data."""
        i = self.info
        return {
            "Current Price": i.get("currentPrice", i.get("regularMarketPrice", None)),
            "Target Low": i.get("targetLowPrice", None),
            "Target Mean": i.get("targetMeanPrice", None),
            "Target Median": i.get("targetMedianPrice", None),
            "Target High": i.get("targetHighPrice", None),
            "Number of Analysts": i.get("numberOfAnalystOpinions", None),
        }

    # ── Insider & Institutional Holdings ────────────────────────────────────
    def get_institutional_holders(self):
        try:
            return self.ticker.institutional_holders
        except Exception:
            return pd.DataFrame()

    def get_insider_transactions(self):
        try:
            return self.ticker.insider_transactions
        except Exception:
            return pd.DataFrame()

    # ── Peer Comparison ─────────────────────────────────────────────────────
    def get_peer_comparison(self, peers=None):
        """Pull key metrics for PLTR and peer companies for comparable analysis."""
        if peers is None:
            peers = PEERS
        all_tickers = [self.ticker_str] + peers
        rows = []
        for t in all_tickers:
            try:
                info = yf.Ticker(t).info
                rows.append({
                    "Ticker": t,
                    "Name": info.get("shortName", t),
                    "Market Cap ($B)": round(info.get("marketCap", 0) / 1e9, 2),
                    "Revenue ($B)": round(info.get("totalRevenue", 0) / 1e9, 2),
                    "Revenue Growth": info.get("revenueGrowth", None),
                    "Profit Margin": info.get("profitMargins", None),
                    "Operating Margin": info.get("operatingMargins", None),
                    "EV/Revenue": info.get("enterpriseToRevenue", None),
                    "EV/EBITDA": info.get("enterpriseToEbitda", None),
                    "P/S": info.get("priceToSalesTrailing12Months", None),
                    "Forward P/E": info.get("forwardPE", None),
                    "ROE": info.get("returnOnEquity", None),
                    "Free Cash Flow ($B)": round(info.get("freeCashflow", 0) / 1e9, 2),
                    "Debt/Equity": info.get("debtToEquity", None),
                    "Beta": info.get("beta", None),
                })
            except Exception:
                continue
        return pd.DataFrame(rows)

    # ── SEC EDGAR Filings ───────────────────────────────────────────────────
    def get_sec_filings(self, form_type="10-K", count=10):
        """Fetch recent SEC filings metadata from EDGAR."""
        url = f"https://efts.sec.gov/LATEST/search-index?q=%22palantir%22&dateRange=custom&startdt=2020-01-01&enddt=2026-12-31&forms={form_type}"
        try:
            # Use the company filings endpoint
            cik = EDGAR_CIK.lstrip("0")
            url = f"https://data.sec.gov/submissions/CIK{EDGAR_CIK}.json"
            resp = requests.get(url, headers=SEC_HEADERS, timeout=10)
            resp.raise_for_status()
            data = resp.json()
            recent = data.get("filings", {}).get("recent", {})
            if not recent:
                return pd.DataFrame()
            df = pd.DataFrame(recent)
            if form_type:
                df = df[df["form"] == form_type]
            return df.head(count)[["accessionNumber", "filingDate", "form", "primaryDocument"]]
        except Exception as e:
            return pd.DataFrame({"error": [str(e)]})


# ── Financial Analytics Engine ──────────────────────────────────────────────
class FinancialAnalytics:
    """
    Implements analytical methods from MBAN5570:
    Horizontal, Vertical, Ratio, Trend, DuPont, and Graphical Analysis.
    """

    def __init__(self, pipeline: PLTRDataPipeline):
        self.pipe = pipeline
        self._is = None
        self._bs = None
        self._cf = None

    @property
    def income_stmt(self):
        if self._is is None:
            self._is = self.pipe.get_income_statement()
        return self._is

    @property
    def balance_sheet(self):
        if self._bs is None:
            self._bs = self.pipe.get_balance_sheet()
        return self._bs

    @property
    def cash_flow(self):
        if self._cf is None:
            self._cf = self.pipe.get_cash_flow()
        return self._cf

    # ── Horizontal Analysis (Year-over-Year % Change) ───────────────────────
    def horizontal_analysis(self, statement="income"):
        """YoY percentage change for each line item."""
        df = self._get_statement(statement)
        if df.empty:
            return df
        df_sorted = df.sort_index()
        return df_sorted.pct_change() * 100

    # ── Vertical Analysis (Common-Size) ─────────────────────────────────────
    def vertical_analysis(self, statement="income"):
        """Express each item as % of a base (Revenue for IS, Total Assets for BS)."""
        df = self._get_statement(statement)
        if df.empty:
            return df
        if statement == "income":
            base_col = self._find_column(df, ["Total Revenue", "Revenue"])
        elif statement == "balance":
            base_col = self._find_column(df, ["Total Assets"])
        else:
            base_col = self._find_column(df, ["Total Cash From Operating Activities", "Operating Cash Flow"])
        if base_col is None:
            return df
        base = df[base_col].replace(0, np.nan)
        return df.div(base, axis=0) * 100

    # ── Ratio Analysis ──────────────────────────────────────────────────────
    def ratio_analysis(self):
        """Comprehensive ratio analysis across all four quadrants."""
        bs = self.balance_sheet
        ist = self.income_stmt
        cf = self.cash_flow

        ratios = {}
        for idx in ist.index:
            year = str(idx.year) if hasattr(idx, 'year') else str(idx)
            r = {}

            # Helper to safely get values
            def get(df, names, default=0):
                for n in names if isinstance(names, list) else [names]:
                    if n in df.columns:
                        val = df.loc[idx, n] if idx in df.index else default
                        return val if pd.notna(val) else default
                return default

            revenue = get(ist, ["Total Revenue", "Revenue"])
            cogs = abs(get(ist, ["Cost Of Revenue", "Cost Of Goods Sold"]))
            gross_profit = get(ist, ["Gross Profit"])
            operating_income = get(ist, ["Operating Income", "EBIT"])
            net_income = get(ist, ["Net Income", "Net Income Common Stockholders"])
            ebitda = get(ist, ["EBITDA", "Normalized EBITDA"])

            total_assets = get(bs, ["Total Assets"])
            total_liab = get(bs, ["Total Liabilities Net Minority Interest", "Total Liab"])
            total_equity = get(bs, ["Total Stockholders Equity", "Stockholders Equity"])
            current_assets = get(bs, ["Current Assets", "Total Current Assets"])
            current_liab = get(bs, ["Current Liabilities", "Total Current Liabilities"])
            cash = get(bs, ["Cash And Cash Equivalents", "Cash"])
            receivables = get(bs, ["Net Receivables", "Accounts Receivable"])
            inventory = get(bs, ["Inventory"])

            op_cf = get(cf, ["Total Cash From Operating Activities", "Operating Cash Flow"])
            capex = abs(get(cf, ["Capital Expenditure", "Capital Expenditures"]))
            fcf = op_cf - capex

            # Profitability
            r["Gross Margin (%)"] = (gross_profit / revenue * 100) if revenue else None
            r["Operating Margin (%)"] = (operating_income / revenue * 100) if revenue else None
            r["Net Margin (%)"] = (net_income / revenue * 100) if revenue else None
            r["ROA (%)"] = (net_income / total_assets * 100) if total_assets else None
            r["ROE (%)"] = (net_income / total_equity * 100) if total_equity else None

            # Liquidity
            r["Current Ratio"] = (current_assets / current_liab) if current_liab else None
            r["Quick Ratio"] = ((current_assets - inventory) / current_liab) if current_liab else None
            r["Cash Ratio"] = (cash / current_liab) if current_liab else None

            # Solvency
            r["Debt/Equity"] = (total_liab / total_equity) if total_equity else None
            r["Debt/Assets"] = (total_liab / total_assets) if total_assets else None

            # Efficiency
            r["Asset Turnover"] = (revenue / total_assets) if total_assets else None
            r["Receivables Turnover"] = (revenue / receivables) if receivables else None

            # Cash Flow
            r["FCF Margin (%)"] = (fcf / revenue * 100) if revenue else None
            r["Operating CF / Net Income"] = (op_cf / net_income) if net_income else None

            ratios[year] = r

        return pd.DataFrame(ratios).T

    # ── DuPont Analysis ─────────────────────────────────────────────────────
    def dupont_analysis(self):
        """3-factor DuPont decomposition: ROE = Margin × Turnover × Leverage."""
        ist = self.income_stmt
        bs = self.balance_sheet
        results = {}
        for idx in ist.index:
            if idx not in bs.index:
                continue
            year = str(idx.year) if hasattr(idx, 'year') else str(idx)

            def get(df, names, default=0):
                for n in names if isinstance(names, list) else [names]:
                    if n in df.columns:
                        val = df.loc[idx, n]
                        return val if pd.notna(val) else default
                return default

            revenue = get(ist, ["Total Revenue", "Revenue"])
            net_income = get(ist, ["Net Income", "Net Income Common Stockholders"])
            total_assets = get(bs, ["Total Assets"])
            total_equity = get(bs, ["Total Stockholders Equity", "Stockholders Equity"])

            margin = (net_income / revenue) if revenue else 0
            turnover = (revenue / total_assets) if total_assets else 0
            leverage = (total_assets / total_equity) if total_equity else 0
            roe = margin * turnover * leverage

            results[year] = {
                "Net Profit Margin": round(margin, 4),
                "Asset Turnover": round(turnover, 4),
                "Equity Multiplier": round(leverage, 4),
                "ROE (DuPont)": round(roe, 4),
            }
        return pd.DataFrame(results).T

    # ── Trend Analysis ──────────────────────────────────────────────────────
    def trend_analysis(self, statement="income", base_year_idx=0):
        """Index all items to a base year = 100."""
        df = self._get_statement(statement).sort_index()
        if df.empty:
            return df
        base = df.iloc[base_year_idx].replace(0, np.nan)
        return (df.div(base, axis=1) * 100)

    # ── Helpers ─────────────────────────────────────────────────────────────
    def _get_statement(self, name):
        mapping = {"income": self.income_stmt, "balance": self.balance_sheet, "cash": self.cash_flow}
        return mapping.get(name, pd.DataFrame())

    def _find_column(self, df, candidates):
        for c in candidates:
            if c in df.columns:
                return c
        return None


# ── Valuation Engine ────────────────────────────────────────────────────────
class ValuationEngine:
    """DCF, Comparable Company, and DDM models."""

    def __init__(self, pipeline: PLTRDataPipeline):
        self.pipe = pipeline

    def dcf_valuation(self, projection_years=5, revenue_growth_rates=None,
                      fcf_margin=0.25, wacc=0.10, terminal_growth=0.03):
        """
        Discounted Cash Flow model.
        Projects future FCFs from revenue growth assumptions and discounts back.
        """
        metrics = self.pipe.get_key_metrics()
        current_revenue = metrics.get("Revenue (TTM)", 0)
        shares = metrics.get("Shares Outstanding", 1)

        if revenue_growth_rates is None:
            base_growth = metrics.get("Revenue Growth (YoY)", 0.25) or 0.25
            # Decay growth rate over projection period
            revenue_growth_rates = [max(base_growth * (0.85 ** i), terminal_growth + 0.02)
                                    for i in range(projection_years)]

        # Project revenues and FCFs
        projected = []
        rev = current_revenue
        for i, g in enumerate(revenue_growth_rates):
            rev = rev * (1 + g)
            fcf = rev * fcf_margin
            pv_factor = 1 / (1 + wacc) ** (i + 1)
            projected.append({
                "Year": i + 1,
                "Revenue Growth": g,
                "Revenue": rev,
                "FCF Margin": fcf_margin,
                "FCF": fcf,
                "PV Factor": pv_factor,
                "PV of FCF": fcf * pv_factor,
            })

        df = pd.DataFrame(projected)
        sum_pv_fcf = df["PV of FCF"].sum()

        # Terminal value (Gordon Growth)
        terminal_fcf = projected[-1]["FCF"] * (1 + terminal_growth)
        terminal_value = terminal_fcf / (wacc - terminal_growth)
        pv_terminal = terminal_value / (1 + wacc) ** projection_years

        enterprise_value = sum_pv_fcf + pv_terminal
        # Adjust for net cash
        net_cash = metrics.get("Total Cash", 0) - metrics.get("Total Debt", 0)
        equity_value = enterprise_value + net_cash
        price_per_share = equity_value / shares if shares else 0

        return {
            "projections": df,
            "sum_pv_fcf": sum_pv_fcf,
            "terminal_value": terminal_value,
            "pv_terminal_value": pv_terminal,
            "enterprise_value": enterprise_value,
            "net_cash": net_cash,
            "equity_value": equity_value,
            "implied_price": price_per_share,
            "current_price": metrics.get("52-Week High", 0),  # fallback
            "shares_outstanding": shares,
            "assumptions": {
                "wacc": wacc,
                "terminal_growth": terminal_growth,
                "fcf_margin": fcf_margin,
                "revenue_growth_rates": revenue_growth_rates,
            }
        }

    def sensitivity_analysis(self, base_dcf=None, wacc_range=None, tg_range=None):
        """
        2D sensitivity table: WACC vs Terminal Growth Rate → Implied Share Price.
        """
        if wacc_range is None:
            wacc_range = [0.08, 0.09, 0.10, 0.11, 0.12]
        if tg_range is None:
            tg_range = [0.02, 0.025, 0.03, 0.035, 0.04]

        if base_dcf is None:
            base_dcf = self.dcf_valuation()

        table = {}
        for w in wacc_range:
            row = {}
            for tg in tg_range:
                result = self.dcf_valuation(
                    wacc=w, terminal_growth=tg,
                    fcf_margin=base_dcf["assumptions"]["fcf_margin"],
                    revenue_growth_rates=base_dcf["assumptions"]["revenue_growth_rates"]
                )
                row[f"TG={tg:.1%}"] = round(result["implied_price"], 2)
            table[f"WACC={w:.1%}"] = row
        return pd.DataFrame(table).T

    def comparable_valuation(self):
        """EV/Revenue and EV/EBITDA multiples-based valuation using peer medians."""
        peers_df = self.pipe.get_peer_comparison()
        if peers_df.empty:
            return {}

        metrics = self.pipe.get_key_metrics()
        pltr_rev = metrics.get("Revenue (TTM)", 0)
        shares = metrics.get("Shares Outstanding", 1)
        net_cash = metrics.get("Total Cash", 0) - metrics.get("Total Debt", 0)

        # Get peer medians (exclude PLTR)
        peer_only = peers_df[peers_df["Ticker"] != self.pipe.ticker_str]
        median_ev_rev = peer_only["EV/Revenue"].median()
        median_ev_ebitda = peer_only["EV/EBITDA"].median()

        # Implied EV from multiples
        ev_from_rev = pltr_rev * median_ev_rev if median_ev_rev else 0
        price_from_rev = (ev_from_rev + net_cash) / shares if shares else 0

        return {
            "peers_data": peers_df,
            "median_ev_revenue": median_ev_rev,
            "median_ev_ebitda": median_ev_ebitda,
            "pltr_revenue": pltr_rev,
            "implied_ev_from_revenue": ev_from_rev,
            "implied_price_from_revenue": price_from_rev,
            "net_cash": net_cash,
        }


# ── Monte Carlo Simulation (per MBAN5570 Risk Modelling) ───────────────────
class MonteCarloSimulator:
    """
    Implements GBM-based Monte Carlo simulation.
    dS = S * μ * dt + S * σ * ε * √Δt
    """

    def __init__(self, pipeline: PLTRDataPipeline):
        self.pipe = pipeline

    def run_gbm_simulation(self, n_simulations=1000, n_days=252, seed=42):
        """
        Geometric Brownian Motion simulation for PLTR stock price.
        Returns simulated price paths and summary statistics.
        """
        np.random.seed(seed)
        prices = self.pipe.get_historical_prices(period="2y")
        if prices.empty:
            return {}

        log_returns = np.log(prices["Close"] / prices["Close"].shift(1)).dropna()
        mu = log_returns.mean() * 252  # Annualized drift
        sigma = log_returns.std() * np.sqrt(252)  # Annualized volatility
        S0 = prices["Close"].iloc[-1]
        dt = 1 / 252

        # Simulate
        paths = np.zeros((n_simulations, n_days + 1))
        paths[:, 0] = S0

        for t in range(1, n_days + 1):
            z = np.random.standard_normal(n_simulations)
            paths[:, t] = paths[:, t - 1] * np.exp((mu - 0.5 * sigma ** 2) * dt + sigma * np.sqrt(dt) * z)

        final_prices = paths[:, -1]
        return {
            "paths": paths,
            "S0": S0,
            "mu": mu,
            "sigma": sigma,
            "final_prices": final_prices,
            "mean_price": np.mean(final_prices),
            "median_price": np.median(final_prices),
            "std_price": np.std(final_prices),
            "percentile_5": np.percentile(final_prices, 5),
            "percentile_25": np.percentile(final_prices, 25),
            "percentile_75": np.percentile(final_prices, 75),
            "percentile_95": np.percentile(final_prices, 95),
            "prob_above_current": np.mean(final_prices > S0),
            "n_simulations": n_simulations,
            "n_days": n_days,
        }

    def scenario_analysis(self, scenarios=None):
        """
        Run DCF under Bull / Base / Bear scenarios.
        """
        ve = ValuationEngine(self.pipe)
        if scenarios is None:
            scenarios = {
                "Bull": {"revenue_growth_rates": [0.35, 0.30, 0.28, 0.25, 0.22],
                         "fcf_margin": 0.30, "wacc": 0.09, "terminal_growth": 0.04},
                "Base": {"revenue_growth_rates": [0.25, 0.22, 0.20, 0.18, 0.16],
                         "fcf_margin": 0.25, "wacc": 0.10, "terminal_growth": 0.03},
                "Bear": {"revenue_growth_rates": [0.15, 0.12, 0.10, 0.10, 0.08],
                         "fcf_margin": 0.18, "wacc": 0.12, "terminal_growth": 0.02},
            }

        results = {}
        for name, params in scenarios.items():
            dcf = ve.dcf_valuation(**params)
            results[name] = {
                "Implied Price": dcf["implied_price"],
                "Enterprise Value": dcf["enterprise_value"],
                "Revenue Growth (Y1)": params["revenue_growth_rates"][0],
                "FCF Margin": params["fcf_margin"],
                "WACC": params["wacc"],
                "Terminal Growth": params["terminal_growth"],
            }
        return pd.DataFrame(results).T


# ── Event Study Analytics (per MBAN5570) ────────────────────────────────────
class EventStudyAnalytics:
    """
    Implements AR, CAR, CAAR methodology.
    Market Model: E(R_j | R_M,t) = α + β × R_M,t
    """

    def __init__(self, pipeline: PLTRDataPipeline, market_ticker="SPY"):
        self.pipe = pipeline
        self.market = yf.Ticker(market_ticker)

    def run_event_study(self, event_date, event_window=(-10, 10), estimation_window=100):
        """
        Run event study around a specific date.
        Returns Abnormal Returns (AR) and Cumulative AR (CAR).
        """
        # Get price data
        start = pd.Timestamp(event_date) - pd.Timedelta(days=estimation_window + abs(event_window[0]) + 50)
        end = pd.Timestamp(event_date) + pd.Timedelta(days=abs(event_window[1]) + 10)

        stock = self.pipe.get_historical_prices(period="max")
        market = self.market.history(period="max")
        stock.index = stock.index.tz_localize(None) if stock.index.tz else stock.index
        market.index = market.index.tz_localize(None) if market.index.tz else market.index

        stock_ret = stock["Close"].pct_change().dropna()
        market_ret = market["Close"].pct_change().dropna()

        # Align
        common = stock_ret.index.intersection(market_ret.index)
        stock_ret = stock_ret.loc[common]
        market_ret = market_ret.loc[common]

        event_dt = pd.Timestamp(event_date)
        # Find nearest trading day
        idx_loc = common.get_indexer([event_dt], method="nearest")[0]

        # Estimation period
        est_end = idx_loc + event_window[0] - 1
        est_start = est_end - estimation_window

        if est_start < 0:
            return {"error": "Not enough data for estimation window"}

        est_stock = stock_ret.iloc[est_start:est_end]
        est_market = market_ret.iloc[est_start:est_end]

        # Market model regression
        from numpy.polynomial.polynomial import polyfit
        beta, alpha = np.polyfit(est_market.values, est_stock.values, 1)

        # Event window
        ev_start = idx_loc + event_window[0]
        ev_end = idx_loc + event_window[1] + 1
        ev_stock = stock_ret.iloc[ev_start:ev_end]
        ev_market = market_ret.iloc[ev_start:ev_end]

        # Abnormal returns
        expected = alpha + beta * ev_market
        ar = ev_stock - expected
        car = ar.cumsum()

        return {
            "alpha": alpha,
            "beta": beta,
            "AR": ar,
            "CAR": car,
            "event_date": event_date,
            "event_window": event_window,
        }


# ── Quick Test ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("Initializing PLTR Data Pipeline...")
    pipe = PLTRDataPipeline()
    metrics = pipe.get_key_metrics()
    print(f"\n{metrics['Company']} — Key Snapshot:")
    for k, v in list(metrics.items())[:15]:
        print(f"  {k}: {v}")

    print("\nFetching financial statements...")
    is_df = pipe.get_income_statement()
    print(f"  Income Statement: {is_df.shape}")
    bs_df = pipe.get_balance_sheet()
    print(f"  Balance Sheet: {bs_df.shape}")
    cf_df = pipe.get_cash_flow()
    print(f"  Cash Flow: {cf_df.shape}")

    print("\nRunning analytics...")
    analytics = FinancialAnalytics(pipe)
    ratios = analytics.ratio_analysis()
    print(f"  Ratio Analysis: {ratios.shape}")
    dupont = analytics.dupont_analysis()
    print(f"  DuPont Analysis:\n{dupont}")

    print("\nDone! Pipeline ready.")
