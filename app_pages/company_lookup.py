# app_pages/company_lookup.py

from datetime import date, timedelta
from html import escape
import random
import re

import pandas as pd
import streamlit as st
import yfinance as yf


# =========================================================
# Constants
# =========================================================

DEFAULT_HISTORY_DAYS = 180

SOLITAIRE_URL = "https://play-solitaire.com/"

HIDDEN_LOOKUP_ALIASES = {
    "SOLITARE": "SOLITAIRE",
}

KNOWN_LIMITATIONS = """
- Symbols must match Yahoo Finance formatting, including dashes or exchange suffixes.
- Some securities may have incomplete fundamentals or historical data.
- Yahoo Finance data may be delayed or temporarily unavailable.
"""


HIDDEN_LOOKUPS = {
    "SOLITAIRE": {
        "title": "Solitaire Holdings",
        "subtitle": "Workplace Wellness · NASDAQ: CARDS",
        "message": "Productivity has been temporarily suspended.",
        "metrics": {
            "Current Price": "One Break",
            "Market Cap": "52 Cards",
            "P/E Ratio": "Patience / Efficiency",
            "Dividend Yield": "Temporary Joy",
        },
        "details": {
            "Headquarters": "Windows XP",
            "Primary Asset": "A Well-Shuffled Deck",
            "Risk Factor": "One More Game",
            "Analyst Rating": "Touch Grass",
        },
        "description": (
            "Analysis indicates that you have been staring at financial data "
            "for too long. FidSync recommends stepping away from the screen, "
            "stretching, drinking some water, and touching some grass. "
            "Management has approved one game of Solitaire."
        ),
    },
}

LOADING_MESSAGES = [
    "Checking market data...",
    "Checking market data...",
    "Reviewing company fundamentals...",
    "Reviewing company fundamentals...",
    "Loading historical pricing...",
    "Calculating moving averages...",
    "Comparing financial metrics...",
    "Convincing Yahoo Finance to cooperate...",
    "Looking for the missing decimal place...",
    "Consulting the financial crystal ball...",
]


# =========================================================
# Formatting helpers
# =========================================================

def is_missing(value):
    """Safely determine whether a value is missing."""

    if value is None:
        return True

    try:
        result = pd.isna(value)

        if isinstance(result, bool):
            return result

    except (TypeError, ValueError):
        pass

    return False


def format_currency(value, decimals=2):
    """Format a numeric value as currency."""

    if is_missing(value):
        return "N/A"

    try:
        return f"${float(value):,.{decimals}f}"

    except (TypeError, ValueError):
        return "N/A"


def format_large_currency(value):
    """Format a large currency amount using abbreviated units."""

    if is_missing(value):
        return "N/A"

    try:
        numeric_value = float(value)

    except (TypeError, ValueError):
        return "N/A"

    if abs(numeric_value) >= 1_000_000_000_000:
        return f"${numeric_value / 1_000_000_000_000:.2f}T"

    if abs(numeric_value) >= 1_000_000_000:
        return f"${numeric_value / 1_000_000_000:.2f}B"

    if abs(numeric_value) >= 1_000_000:
        return f"${numeric_value / 1_000_000:.2f}M"

    return f"${numeric_value:,.0f}"


def format_number(value, decimals=2):
    """Format a general numeric value."""

    if is_missing(value):
        return "N/A"

    try:
        return f"{float(value):,.{decimals}f}"

    except (TypeError, ValueError):
        return "N/A"


def format_integer(value):
    """Format a value as a whole number."""

    if is_missing(value):
        return "N/A"

    try:
        return f"{int(float(value)):,}"

    except (TypeError, ValueError):
        return "N/A"


def format_percentage(value, decimals=2, decimal_input=True):
    """
    Format a percentage.

    Yahoo Finance generally returns percentage values as decimals.
    """

    if is_missing(value):
        return "N/A"

    try:
        percentage = float(value)

        if decimal_input:
            percentage *= 100

        return f"{percentage:.{decimals}f}%"

    except (TypeError, ValueError):
        return "N/A"


def safe_text(value, fallback="N/A"):
    """Return a clean string or the supplied fallback."""

    if value is None:
        return fallback

    cleaned_value = str(value).strip()

    return cleaned_value if cleaned_value else fallback


def first_available(*values):
    """Return the first value that is not None or missing."""

    for value in values:
        if not is_missing(value):
            return value

    return None


def validate_ticker(ticker):
    """Perform basic ticker-format validation."""

    if not ticker:
        return False

    # Supports AAPL, BRK-B, BTC-USD, SHOP.TO, 7203.T, and ^GSPC.
    # It also allows hidden alphabetic lookup terms.
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


def calculate_percentage_change(current_value, previous_value):
    """Calculate percentage change between two values."""

    if is_missing(current_value) or is_missing(previous_value):
        return None

    try:
        previous_value = float(previous_value)

        if previous_value == 0:
            return None

        return (
            (float(current_value) - previous_value)
            / previous_value
        ) * 100

    except (TypeError, ValueError, ZeroDivisionError):
        return None


# =========================================================
# Data retrieval
# =========================================================

@st.cache_data(ttl=900, show_spinner=False)
def retrieve_company_data(ticker):
    """
    Retrieve company information.

    Results are cached for 15 minutes to reduce repeated Yahoo Finance
    requests during Streamlit reruns.
    """

    stock = yf.Ticker(ticker)
    info = stock.info or {}

    return info


@st.cache_data(ttl=900, show_spinner=False)
def retrieve_price_history(ticker, start_date, end_date):
    """Retrieve historical price data for the selected range."""

    stock = yf.Ticker(ticker)

    # yfinance treats end dates as exclusive.
    inclusive_end_date = end_date + timedelta(days=1)

    history = stock.history(
        start=start_date,
        end=inclusive_end_date,
        auto_adjust=False,
    )

    if history.empty:
        return history

    history.index = pd.to_datetime(history.index)

    if getattr(history.index, "tz", None) is not None:
        history.index = history.index.tz_localize(None)

    if "Close" in history.columns:
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
        "company_lookup_input": "",
        "company_hidden_lookup_shown": "",
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def clear_search():
    """
    Clear the current search.

    This function is used as a button callback so the text-input value
    can be changed safely before Streamlit recreates the widget.
    """

    st.session_state.company_lookup_searched = False
    st.session_state.company_lookup_ticker = ""
    st.session_state.company_lookup_input = ""
    st.session_state.company_hidden_lookup_shown = ""


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

            [data-testid="stWidgetLabel"] p {
                color: #102542;
                font-weight: 650;
            }

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

            .stButton > button,
            [data-testid="stFormSubmitButton"] > button {
                min-height: 2.65rem;
                border-radius: 0.55rem;
                font-weight: 650;
            }

            div[data-testid="stButton"] button[kind="primary"],
            [data-testid="stFormSubmitButton"] button[kind="primary"] {
                background-color: #2b6cb0;
                border-color: #2b6cb0;
                color: white;
            }

            div[data-testid="stButton"] button[kind="primary"]:hover,
            [data-testid="stFormSubmitButton"] button[kind="primary"]:hover {
                background-color: #1f568f;
                border-color: #1f568f;
                color: white;
            }

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

            [data-testid="stVerticalBlockBorderWrapper"] {
                border-color: #dce3ec;
                border-radius: 0.75rem;
                background-color: white;
                box-shadow: 0 2px 8px rgba(16, 37, 66, 0.035);
            }

            button[data-baseweb="tab"] {
                color: #64748b;
                font-weight: 600;
            }

            button[data-baseweb="tab"][aria-selected="true"] {
                color: #102542;
            }

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

    with st.form("ticker_search_form", clear_on_submit=False):
        search_col, button_col = st.columns([5, 1.4])

        with search_col:
            ticker_input = st.text_input(
                "Ticker symbol",
                placeholder="Example: AAPL",
                max_chars=15,
                label_visibility="collapsed",
                key="company_lookup_input",
            )

        with button_col:
            search_clicked = st.form_submit_button(
                "Search",
                type="primary",
                use_container_width=True,
            )

    st.button(
        "Clear Search",
        use_container_width=False,
        on_click=clear_search,
    )

    if search_clicked:
        ticker = ticker_input.strip().upper()
        ticker = HIDDEN_LOOKUP_ALIASES.get(ticker, ticker)

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
        st.session_state.company_hidden_lookup_shown = ""
        st.rerun()

    with st.expander("Known limitations"):
        st.markdown(KNOWN_LIMITATIONS)


# =========================================================
# Company information
# =========================================================

def render_company_overview(ticker, info):
    company_name = safe_text(
        first_available(
            info.get("longName"),
            info.get("shortName"),
        ),
        fallback="Company Information",
    )

    quote_type = safe_text(
        info.get("quoteType"),
        fallback="Security",
    )

    exchange = safe_text(
        first_available(
            info.get("fullExchangeName"),
            info.get("exchange"),
        ),
        fallback="Exchange unavailable",
    )

    safe_company_name = escape(company_name)
    safe_ticker = escape(ticker)
    safe_quote_type = escape(quote_type)
    safe_exchange = escape(exchange)

    st.markdown(
        (
            '<div class="company-heading">'
            f"{safe_company_name} ({safe_ticker})"
            "</div>"
        ),
        unsafe_allow_html=True,
    )

    st.markdown(
        (
            '<div class="company-subheading">'
            f"{safe_quote_type} · {safe_exchange}"
            "</div>"
        ),
        unsafe_allow_html=True,
    )

    price = first_available(
        info.get("currentPrice"),
        info.get("regularMarketPrice"),
        info.get("navPrice"),
    )

    previous_close = info.get("previousClose")
    market_cap = info.get("marketCap")
    trailing_pe = info.get("trailingPE")
    dividend_yield = info.get("dividendYield")
    fifty_two_week_low = info.get("fiftyTwoWeekLow")
    fifty_two_week_high = info.get("fiftyTwoWeekHigh")

    price_delta = calculate_percentage_change(
        price,
        previous_close,
    )

    metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)

    with metric_col1:
        st.metric(
            "Current Price",
            format_currency(price),
            delta=(
                f"{price_delta:.2f}%"
                if price_delta is not None
                else None
            ),
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
            if not is_missing(dividend_yield)
            else "No Dividend"
        )

        st.metric(
            "Dividend Yield",
            dividend_display,
        )

    with metric_col8:
        st.metric(
            "Beta",
            format_number(info.get("beta")),
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
                st.write(
                    format_integer(
                        info.get("fullTimeEmployees")
                    )
                )

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
                    format_large_currency(
                        info.get("enterpriseValue")
                    ),
                    format_percentage(
                        info.get("profitMargins")
                    ),
                    format_percentage(
                        info.get("operatingMargins")
                    ),
                    format_percentage(
                        info.get("returnOnAssets")
                    ),
                    format_percentage(
                        info.get("returnOnEquity")
                    ),
                    format_percentage(
                        info.get("revenueGrowth")
                    ),
                    format_percentage(
                        info.get("earningsGrowth")
                    ),
                    format_integer(
                        info.get("averageVolume")
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

    if "Close" not in history.columns:
        st.warning(
            "Historical records were returned, but closing-price data "
            "was unavailable."
        )
        return

    valid_closes = history["Close"].dropna()

    if valid_closes.empty:
        st.warning(
            "Historical records were returned, but no valid closing "
            "prices were available."
        )
        return

    first_close = valid_closes.iloc[0]
    last_close = valid_closes.iloc[-1]

    period_change = calculate_percentage_change(
        last_close,
        first_close,
    )

    period_high = (
        history["High"].max()
        if "High" in history.columns
        else None
    )

    period_low = (
        history["Low"].min()
        if "Low" in history.columns
        else None
    )

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
            delta=(
                f"{period_change:.2f}%"
                if period_change is not None
                else None
            ),
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
        available_chart_columns = [
            column
            for column in ["Close", "MA20", "MA50"]
            if column in history.columns
        ]

        chart_data = history[
            available_chart_columns
        ].copy()

        chart_data = chart_data.rename(
            columns={
                "Close": "Closing Price",
                "MA20": "20-Day Average",
                "MA50": "50-Day Average",
            }
        )

        st.line_chart(
            chart_data,
            use_container_width=True,
        )

        st.caption(
            "Moving averages use the available observations within the "
            "selected range."
        )

    with volume_tab:
        if "Volume" in history.columns:
            st.bar_chart(
                history["Volume"],
                use_container_width=True,
            )

        else:
            st.info(
                "Trading-volume data is not available for this security."
            )

    with data_tab:
        frequency = st.selectbox(
            "View frequency",
            options=[
                "Daily",
                "Monthly",
                "Quarterly",
            ],
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

        display_data = display_data[
            display_columns
        ].copy()

        formatters = {
            column: "${:,.2f}"
            for column in [
                "Open",
                "High",
                "Low",
                "Close",
                "MA20",
                "MA50",
            ]
            if column in display_data.columns
        }

        if "Volume" in display_data.columns:
            formatters["Volume"] = "{:,.0f}"

        if "Dividends" in display_data.columns:
            formatters["Dividends"] = "${:,.4f}"

        if "Stock Splits" in display_data.columns:
            formatters["Stock Splits"] = "{:,.4f}"

        st.dataframe(
            display_data.style.format(
                formatters,
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

        downloaded = st.download_button(
            label="Download Historical Data as CSV",
            data=csv_data,
            file_name=(
                f"{ticker}_{frequency.lower()}_history.csv"
            ),
            mime="text/csv",
            use_container_width=True,
        )

        if downloaded:
            st.toast("Another spreadsheet enters the collection.")

    last_date = history.index[-1].strftime("%B %d, %Y")

    st.caption(
        f"Most recent observation in this range: {last_date}"
    )


# =========================================================
# Hidden lookup renderers
# =========================================================

def render_hidden_lookup(ticker):
    """Render a fictional profile for a hidden lookup."""

    lookup = HIDDEN_LOOKUPS.get(ticker)

    if not lookup:
        return False

    if st.session_state.company_hidden_lookup_shown != ticker:
        st.balloons()
        st.toast(lookup["message"])
        st.session_state.company_hidden_lookup_shown = ticker

    title = escape(lookup["title"])
    subtitle = escape(lookup["subtitle"])
    ticker_display = escape(ticker)

    st.markdown(
        (
            '<div class="company-heading">'
            f"{title} ({ticker_display})"
            "</div>"
        ),
        unsafe_allow_html=True,
    )

    st.markdown(
        (
            '<div class="company-subheading">'
            f"{subtitle}"
            "</div>"
        ),
        unsafe_allow_html=True,
    )

    metric_items = list(lookup["metrics"].items())
    metric_columns = st.columns(len(metric_items))

    for column, metric_item in zip(metric_columns, metric_items):
        label, value = metric_item

        with column:
            st.metric(label, value)

    profile_tab, description_tab = st.tabs(
        [
            "Company Profile",
            "Business Description",
        ]
    )

    with profile_tab:
        with st.container(border=True):
            detail_items = list(lookup["details"].items())
            left_column, right_column = st.columns(2)

            for index, detail_item in enumerate(detail_items):
                label, value = detail_item

                target_column = (
                    left_column
                    if index % 2 == 0
                    else right_column
                )

                with target_column:
                    st.markdown(f"**{label}**")
                    st.write(value)

    with description_tab:
        st.write(lookup["description"])

    if ticker == "SOLITAIRE":
        st.warning(
            "You have been staring at the screen for too long. "
            "Go touch some grass."
        )

        st.link_button(
            "Definitely Do Not Open Solitaire",
            SOLITAIRE_URL,
            use_container_width=True,
        )

        st.caption(
            "FidSync accepts no responsibility for productivity lost "
            "after clicking this button."
        )

    return True


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

        # Hidden Solitaire profile
        if ticker in HIDDEN_LOOKUPS:
            render_hidden_lookup(ticker)

        # Normal Yahoo Finance search
        else:
            try:
                with st.spinner(
                    random.choice(LOADING_MESSAGES)
                ):
                    company_info = retrieve_company_data(ticker)

                if not company_info:
                    st.error(
                        "No company information was returned. Confirm "
                        "the ticker and try again."
                    )

                else:
                    render_company_overview(
                        ticker,
                        company_info,
                    )


                    render_history_section(ticker)

            except Exception as error:
                st.error(
                    "The ticker data could not be retrieved. Confirm "
                    "the symbol and try again."
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
