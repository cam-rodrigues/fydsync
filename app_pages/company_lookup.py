# app_pages/company_lookup.py

from datetime import date, timedelta
import re

import pandas as pd
import streamlit as st
import yfinance as yf


# =========================================================
# Constants
# =========================================================

DEFAULT_HISTORY_DAYS = 180

KNOWN_LIMITATIONS = """
- The ticker must be valid and supported by Yahoo Finance.
- Use dashes rather than dots for tickers such as `BRK-B`.
- Some international securities require exchange suffixes such as `.TO`, `.T`, or `.NS`.
- Delisted, micro-cap, and newly listed securities may return incomplete data.
- Cryptocurrency symbols such as `BTC-USD` may return price data but limited fundamentals.
- ETF and mutual fund fundamentals may be limited or unavailable.
- Yahoo Finance may occasionally delay, restrict, or omit certain fields.
"""


# =========================================================
# Formatting helpers
# =========================================================

def format_currency(value, decimals=2):
    """Format a numeric value as currency."""

    if value is None or pd.isna(value):
        return "N/A"

    try:
        return f"${float(value):,.{decimals}f}"
    except (TypeError, ValueError):
        return "N/A"


def format_large_currency(value):
    """Format a large currency amount using abbreviated units."""

    if value is None or pd.isna(value):
        return "N/A"

    try:
        value = float(value)
    except (TypeError, ValueError):
        return "N/A"

    if abs(value) >= 1_000_000_000_000:
        return f"${value / 1_000_000_000_000:.2f}T"

    if abs(value) >= 1_000_000_000:
        return f"${value / 1_000_000_000:.2f}B"

    if abs(value) >= 1_000_000:
        return f"${value / 1_000_000:.2f}M"

    return f"${value:,.0f}"


def format_number(value, decimals=2):
    """Format a general numeric value."""

    if value is None or pd.isna(value):
        return "N/A"

    try:
        return f"{float(value):,.{decimals}f}"
    except (TypeError, ValueError):
        return "N/A"


def format_percentage(value, decimals=2, decimal_input=True):
    """
    Format a percentage.

    Yahoo Finance usually returns dividend yield as a decimal, so
    decimal_input=True multiplies the value by 100.
    """

    if value is None or pd.isna(value):
        return "N/A"

    try:
        percentage = float(value)

        if decimal_input:
            percentage *= 100

        return f"{percentage:.{decimals}f}%"

    except (TypeError, ValueError):
        return "N/A"


def safe_text(value, fallback="N/A"):
    """Return a clean string or a fallback value."""

    if value is None:
        return fallback

    value = str(value).strip()

    return value if value else fallback


def validate_ticker(ticker):
    """Perform basic ticker-format validation."""

    if not ticker:
        return False

    # Supports formats such as AAPL, BRK-B, BTC-USD, SHOP.TO, and 7203.T
    pattern = r"^[A-Z0-9^][A-Z0-9.\-=^]{0,14}$"

    return re.fullmatch(pattern, ticker) is not None


def build_location(info):
    """Build a headquarters string from available address fields."""

    address_parts = [
        info.get("address1"),
        info.get("address2"),
        info.get("city"),
        info.get("state"),
        info.get("zip"),
        info.get("country"),
    ]

    return ", ".join(
        str(part).strip()
        for part in address_parts
        if part and str(part).strip()
    )


# =========================================================
# Data retrieval
# =========================================================

@st.cache_data(ttl=900, show_spinner=False)
def retrieve_company_data(ticker):
    """
    Retrieve company information.

    The cache lasts 15 minutes to reduce repeated Yahoo Finance
    requests during Streamlit reruns.
    """

    stock = yf.Ticker(ticker)
    info = stock.info or {}

    return info


@st.cache_data(ttl=900, show_spinner=False)
def retrieve_price_history(ticker, start_date, end_date):
    """Retrieve historical price data for the selected range."""

    stock = yf.Ticker(ticker)

    # yfinance treats the end date as exclusive, so add one day.
    inclusive_end_date = end_date + timedelta(days=1)

    history = stock.history(
        start=start_date,
        end=inclusive_end_date,
        auto_adjust=False,
    )

    if history.empty:
        return history

    history.index = pd.to_datetime(history.index)

    # Remove timezone information to make display/export simpler.
    if getattr(history.index, "tz", None) is not None:
        history.index = history.index.tz_localize(None)

    history["MA20"] = history["Close"].rolling(
        window=20,
        min_periods=1,
    ).mean()

    history["MA50"] = history["Close"].rolling(
        window=50,
        min_periods=1,
    ).mean()

    return history


# =========================================================
# Session state
# =========================================================

def initialize_session_state():
    """Create session-state values used by the lookup tool."""

    defaults = {
        "company_lookup_searched": False,
        "company_lookup_ticker": "",
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def clear_search():
    """Clear the current ticker search."""

    st.session_state.company_lookup_searched = False
    st.session_state.company_lookup_ticker = ""


# =========================================================
# Styling
# =========================================================

def apply_page_styles():
    st.markdown(
        """
        <style>
            .block-container {
                max-width: 1200px;
                padding-top: 2rem;
                padding-bottom: 3rem;
            }

            /* Page header */
            .lookup-header {
                padding: 2.2rem 2.4rem;
                margin-bottom: 1.5rem;
                background:
                    radial-gradient(
                        circle at top right,
                        rgba(117, 158, 203, 0.22),
                        transparent 36%
                    ),
                    linear-gradient(
                        135deg,
                        #102542 0%,
                        #213b5c 100%
                    );
                border: 1px solid #2d496b;
                border-radius: 1rem;
                box-shadow: 0 8px 24px rgba(16, 37, 66, 0.12);
            }

            .lookup-header-label {
                margin-bottom: 0.55rem;
                color: #b9cde5;
                font-size: 0.72rem;
                font-weight: 700;
                letter-spacing: 0.1rem;
                text-transform: uppercase;
            }

            .lookup-header h1 {
                margin: 0;
                color: white;
                font-size: 2.2rem;
                font-weight: 750;
                line-height: 1.2;
                letter-spacing: -0.05rem;
            }

            .lookup-header p {
                max-width: 790px;
                margin: 0.8rem 0 0 0;
                color: #d8e4f2;
                font-size: 0.97rem;
                line-height: 1.65;
            }

            /* Section headings */
            .section-heading {
                margin-top: 1.25rem;
                margin-bottom: 0.2rem;
                color: #102542;
                font-size: 1.3rem;
                font-weight: 750;
                letter-spacing: -0.02rem;
            }

            .section-description {
                margin-bottom: 1rem;
                color: #64748b;
                font-size: 0.88rem;
                line-height: 1.55;
            }

            /* Search instructions */
            .lookup-instructions {
                padding: 0.9rem 1rem;
                margin-bottom: 1rem;
                background-color: #f7fafd;
                border: 1px solid #d6e1f3;
                border-left: 4px solid #2b6cb0;
                border-radius: 0.6rem;
                color: #526273;
                font-size: 0.84rem;
                line-height: 1.55;
            }

            /* Input labels */
            [data-testid="stWidgetLabel"] p {
                color: #102542;
                font-weight: 650;
            }

            /* Inputs */
            [data-baseweb="input"] > div,
            [data-baseweb="select"] > div {
                border-color: #ccd8e6;
                border-radius: 0.55rem;
            }

            [data-baseweb="input"] > div:focus-within,
            [data-baseweb="select"] > div:focus-within {
                border-color: #2b6cb0;
                box-shadow: 0 0 0 1px #2b6cb0;
            }

            /* Buttons */
            .stButton > button {
                min-height: 2.65rem;
                border-radius: 0.55rem;
                font-weight: 650;
            }

            div[data-testid="stButton"] button[kind="primary"] {
                background-color: #2b6cb0;
                border-color: #2b6cb0;
                color: white;
            }

            div[data-testid="stButton"] button[kind="primary"]:hover {
                background-color: #1f568f;
                border-color: #1f568f;
                color: white;
            }

            /* Company title */
            .company-heading {
                margin-top: 0.6rem;
                margin-bottom: 0.2rem;
                color: #102542;
                font-size: 1.75rem;
                font-weight: 760;
                letter-spacing: -0.035rem;
            }

            .company-subheading {
                margin-bottom: 1rem;
                color: #64748b;
                font-size: 0.88rem;
            }

            /* Metrics */
            [data-testid="stMetric"] {
                min-height: 108px;
                padding: 0.95rem 1rem;
                background-color: white;
                border: 1px solid #dce3ec;
                border-radius: 0.75rem;
                box-shadow: 0 2px 8px rgba(16, 37, 66, 0.04);
            }

            [data-testid="stMetricLabel"] {
                color: #64748b;
                font-size: 0.77rem;
                font-weight: 600;
            }

            [data-testid="stMetricValue"] {
                color: #102542;
                font-size: 1.35rem;
                font-weight: 750;
            }

            /* Native bordered containers */
            [data-testid="stVerticalBlockBorderWrapper"] {
                border-color: #dce3ec;
                border-radius: 0.75rem;
                background-color: white;
                box-shadow: 0 2px 8px rgba(16, 37, 66, 0.035);
            }

            /* Tabs */
            button[data-baseweb="tab"] {
                color: #64748b;
                font-weight: 600;
            }

            button[data-baseweb="tab"][aria-selected="true"] {
                color: #102542;
            }

            /* Expanders */
            [data-testid="stExpander"] {
                margin-bottom: 0.65rem;
                background-color: white;
                border: 1px solid #dce3ec;
                border-radius: 0.75rem;
                box-shadow: 0 2px 8px rgba(16, 37, 66, 0.035);
                overflow: hidden;
            }

            [data-testid="stExpander"] summary {
                color: #102542;
                font-weight: 650;
            }

            /* Download button */
            [data-testid="stDownloadButton"] > button {
                min-height: 2.65rem;
                background-color: #2b6cb0;
                color: white;
                border: 1px solid #2b6cb0;
                border-radius: 0.55rem;
                font-weight: 700;
            }

            [data-testid="stDownloadButton"] > button:hover {
                background-color: #1f568f;
                border-color: #1f568f;
                color: white;
            }

            /* Disclaimer */
            .lookup-disclaimer {
                margin-top: 1.5rem;
                padding: 0.9rem 1rem;
                background-color: #edf3fa;
                border: 1px solid #cfdae8;
                border-left: 4px solid #2b6cb0;
                border-radius: 0.55rem;
                color: #526273;
                font-size: 0.8rem;
                line-height: 1.55;
            }

            @media (max-width: 700px) {
                .lookup-header {
                    padding: 1.7rem;
                }
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


# =========================================================
# Search interface
# =========================================================

def render_search_section():
    st.markdown(
        """
        <div class="section-heading">Search for a security</div>
        <div class="section-description">
            Enter a Yahoo Finance-supported stock, ETF, mutual fund,
            index, or cryptocurrency symbol.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="lookup-instructions">
            Enter the ticker exactly as it appears on Yahoo Finance. Examples:
            <strong>AAPL</strong>, <strong>MSFT</strong>,
            <strong>BRK-B</strong>, <strong>SPY</strong>, or
            <strong>BTC-USD</strong>.
        </div>
        """,
        unsafe_allow_html=True,
    )

    search_col, button_col, clear_col = st.columns([5, 1.4, 1])

    with search_col:
        ticker_input = st.text_input(
            "Ticker symbol",
            value=st.session_state.company_lookup_ticker,
            placeholder="Example: AAPL",
            max_chars=15,
            label_visibility="collapsed",
        )

    with button_col:
        search_clicked = st.button(
            "Search",
            type="primary",
            use_container_width=True,
        )

    with clear_col:
        clear_clicked = st.button(
            "Clear",
            use_container_width=True,
        )

    if clear_clicked:
        clear_search()
        st.rerun()

    if search_clicked:
        ticker = ticker_input.strip().upper()

        if not ticker:
            st.warning("Enter a ticker symbol before searching.")
            return

        if not validate_ticker(ticker):
            st.warning(
                "Enter a valid ticker using letters, numbers, periods, "
                "dashes, or supported Yahoo Finance symbols."
            )
            return

        st.session_state.company_lookup_ticker = ticker
        st.session_state.company_lookup_searched = True
        st.rerun()

    with st.expander("Known limitations"):
        st.markdown(KNOWN_LIMITATIONS)


# =========================================================
# Company information
# =========================================================

def render_company_overview(ticker, info):
    company_name = safe_text(
        info.get("longName") or info.get("shortName"),
        fallback="Company Information",
    )

    quote_type = safe_text(info.get("quoteType"), fallback="Security")
    exchange = safe_text(
        info.get("fullExchangeName") or info.get("exchange"),
        fallback="Exchange unavailable",
    )

    st.markdown(
        f'<div class="company-heading">{company_name} ({ticker})</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        f'<div class="company-subheading">{quote_type} · {exchange}</div>',
        unsafe_allow_html=True,
    )

    price = (
        info.get("currentPrice")
        or info.get("regularMarketPrice")
        or info.get("navPrice")
    )

    previous_close = info.get("previousClose")
    market_cap = info.get("marketCap")
    trailing_pe = info.get("trailingPE")
    dividend_yield = info.get("dividendYield")
    fifty_two_week_low = info.get("fiftyTwoWeekLow")
    fifty_two_week_high = info.get("fiftyTwoWeekHigh")

    metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)

    with metric_col1:
        st.metric(
            "Current Price",
            format_currency(price),
        )

    with metric_col2:
        st.metric(
            "Previous Close",
            format_currency(previous_close),
        )

    with metric_col3:
        st.metric(
            "Market Cap",
            format_large_currency(market_cap),
        )

    with metric_col4:
        st.metric(
            "P/E Ratio (TTM)",
            format_number(trailing_pe),
        )

    metric_col5, metric_col6, metric_col7, metric_col8 = st.columns(4)

    with metric_col5:
        st.metric(
            "52-Week Low",
            format_currency(fifty_two_week_low),
        )

    with metric_col6:
        st.metric(
            "52-Week High",
            format_currency(fifty_two_week_high),
        )

    with metric_col7:
        dividend_display = (
            format_percentage(dividend_yield)
            if dividend_yield is not None
            else "No Dividend"
        )

        st.metric(
            "Dividend Yield",
            dividend_display,
        )

    with metric_col8:
        beta = info.get("beta")

        st.metric(
            "Beta",
            format_number(beta),
        )

    profile_tab, fundamentals_tab, description_tab = st.tabs(
        [
            "Company Profile",
            "Additional Metrics",
            "Business Description",
        ]
    )

    with profile_tab:
        with st.container(border=True):
            profile_col1, profile_col2 = st.columns(2)

            with profile_col1:
                st.markdown("**Sector**")
                st.write(safe_text(info.get("sector")))

                st.markdown("**Industry**")
                st.write(safe_text(info.get("industry")))

                st.markdown("**Employees**")
                employees = info.get("fullTimeEmployees")

                if employees is not None:
                    try:
                        st.write(f"{int(employees):,}")
                    except (TypeError, ValueError):
                        st.write("N/A")
                else:
                    st.write("N/A")

            with profile_col2:
                st.markdown("**Headquarters**")
                headquarters = build_location(info)
                st.write(headquarters or "N/A")

                st.markdown("**Website**")
                website = info.get("website")

                if website:
                    st.link_button(
                        "Visit Company Website",
                        website,
                        use_container_width=True,
                    )
                else:
                    st.write("N/A")

    with fundamentals_tab:
        additional_metrics = pd.DataFrame(
            {
                "Metric": [
                    "Forward P/E",
                    "Price-to-Book",
                    "Enterprise Value",
                    "Profit Margin",
                    "Operating Margin",
                    "Return on Assets",
                    "Return on Equity",
                    "Revenue Growth",
                    "Earnings Growth",
                    "Average Volume",
                ],
                "Value": [
                    format_number(info.get("forwardPE")),
                    format_number(info.get("priceToBook")),
                    format_large_currency(info.get("enterpriseValue")),
                    format_percentage(info.get("profitMargins")),
                    format_percentage(info.get("operatingMargins")),
                    format_percentage(info.get("returnOnAssets")),
                    format_percentage(info.get("returnOnEquity")),
                    format_percentage(info.get("revenueGrowth")),
                    format_percentage(info.get("earningsGrowth")),
                    (
                        f"{int(info.get('averageVolume')):,}"
                        if info.get("averageVolume") is not None
                        else "N/A"
                    ),
                ],
            }
        )

        st.dataframe(
            additional_metrics,
            use_container_width=True,
            hide_index=True,
        )

    with description_tab:
        business_summary = safe_text(
            info.get("longBusinessSummary"),
            fallback="No business description is available.",
        )

        st.write(business_summary)


# =========================================================
# Historical charts
# =========================================================

def render_history_section(ticker):
    st.markdown(
        """
        <div class="section-heading">Historical performance</div>
        <div class="section-description">
            Choose a date range to review closing prices, moving averages,
            trading volume, and downloadable history.
        </div>
        """,
        unsafe_allow_html=True,
    )

    today = date.today()
    default_start = today - timedelta(days=DEFAULT_HISTORY_DAYS)

    date_col1, date_col2 = st.columns(2)

    with date_col1:
        start_date = st.date_input(
            "Start date",
            value=default_start,
            max_value=today,
            key=f"{ticker}_start_date",
        )

    with date_col2:
        end_date = st.date_input(
            "End date",
            value=today,
            min_value=start_date,
            max_value=today,
            key=f"{ticker}_end_date",
        )

    if start_date > end_date:
        st.error("The start date must be before the end date.")
        return

    try:
        with st.spinner(f"Loading historical data for {ticker}..."):
            history = retrieve_price_history(
                ticker,
                start_date,
                end_date,
            )

    except Exception as error:
        st.error("Historical price data could not be retrieved.")

        with st.expander("View technical details"):
            st.code(str(error))

        return

    if history.empty:
        st.warning(
            "No historical data is available for the selected date range."
        )
        return

    first_close = history["Close"].dropna().iloc[0]
    last_close = history["Close"].dropna().iloc[-1]

    if first_close:
        period_change = ((last_close / first_close) - 1) * 100
    else:
        period_change = 0

    period_high = history["High"].max()
    period_low = history["Low"].min()

    history_metric1, history_metric2, history_metric3, history_metric4 = (
        st.columns(4)
    )

    with history_metric1:
        st.metric(
            "Period Start",
            format_currency(first_close),
        )

    with history_metric2:
        st.metric(
            "Period End",
            format_currency(last_close),
            delta=f"{period_change:.2f}%",
        )

    with history_metric3:
        st.metric(
            "Period High",
            format_currency(period_high),
        )

    with history_metric4:
        st.metric(
            "Period Low",
            format_currency(period_low),
        )

    chart_tab, volume_tab, data_tab = st.tabs(
        [
            "Price & Moving Averages",
            "Trading Volume",
            "Historical Data",
        ]
    )

    with chart_tab:
        chart_data = history[
            ["Close", "MA20", "MA50"]
        ].copy()

        chart_data.columns = [
            "Closing Price",
            "20-Day Average",
            "50-Day Average",
        ]

        st.line_chart(
            chart_data,
            use_container_width=True,
        )

        st.caption(
            "Moving averages use the available observations within the "
            "selected range."
        )

    with volume_tab:
        st.bar_chart(
            history["Volume"],
            use_container_width=True,
        )

    with data_tab:
        frequency = st.selectbox(
            "View frequency",
            options=["Daily", "Monthly", "Quarterly"],
            index=0,
            key=f"{ticker}_history_frequency",
        )

        if frequency == "Monthly":
            display_data = history.resample("ME").last()

        elif frequency == "Quarterly":
            display_data = history.resample("QE").last()

        else:
            display_data = history.copy()

        display_columns = [
            column
            for column in [
                "Open",
                "High",
                "Low",
                "Close",
                "Volume",
                "Dividends",
                "Stock Splits",
                "MA20",
                "MA50",
            ]
            if column in display_data.columns
        ]

        display_data = display_data[display_columns].copy()

        st.dataframe(
            display_data.style.format(
                {
                    "Open": "${:,.2f}",
                    "High": "${:,.2f}",
                    "Low": "${:,.2f}",
                    "Close": "${:,.2f}",
                    "Volume": "{:,.0f}",
                    "Dividends": "${:,.4f}",
                    "Stock Splits": "{:,.4f}",
                    "MA20": "${:,.2f}",
                    "MA50": "${:,.2f}",
                },
                na_rep="N/A",
            ),
            use_container_width=True,
        )

        csv_data = (
            display_data
            .reset_index()
            .to_csv(index=False)
            .encode("utf-8")
        )

        st.download_button(
            label="Download Historical Data as CSV",
            data=csv_data,
            file_name=f"{ticker}_{frequency.lower()}_history.csv",
            mime="text/csv",
            use_container_width=True,
        )

    last_date = history.index[-1].strftime("%B %d, %Y")

    st.caption(f"Most recent observation in this range: {last_date}")


# =========================================================
# Main page
# =========================================================

def run():
    initialize_session_state()
    apply_page_styles()

    st.markdown(
        """
        <div class="lookup-header">
            <div class="lookup-header-label">Market Research Tool</div>
            <h1>Ticker Information Lookup</h1>
            <p>
                Search for a publicly traded security, review company
                fundamentals, explore historical prices, and export selected
                market data for further analysis.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    render_search_section()

    if (
        st.session_state.company_lookup_searched
        and st.session_state.company_lookup_ticker
    ):
        ticker = st.session_state.company_lookup_ticker

        try:
            with st.spinner(f"Retrieving information for {ticker}..."):
                company_info = retrieve_company_data(ticker)

            # Yahoo Finance may return an empty dictionary for an invalid ticker.
            if not company_info:
                st.error(
                    "No company information was returned. Confirm the ticker "
                    "and try again."
                )
            else:
                render_company_overview(
                    ticker,
                    company_info,
                )

                render_history_section(ticker)

        except Exception as error:
            st.error(
                "The ticker data could not be retrieved. Confirm the symbol "
                "and try again."
            )

            with st.expander("View technical details"):
                st.code(str(error))

    st.markdown(
        """
        <div class="lookup-disclaimer">
            <strong>Data notice:</strong> Market prices and company information
            are retrieved through Yahoo Finance and may be delayed, incomplete,
            or inaccurate. Verify important financial information against
            official company filings, exchange data, or approved research
            sources before relying on it.
        </div>
        """,
        unsafe_allow_html=True,
    )
