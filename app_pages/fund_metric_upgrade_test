import streamlit as st
import pdfplumber
import pandas as pd
import re
from difflib import get_close_matches
from io import BytesIO
from datetime import datetime
import xlsxwriter
from xlsxwriter.utility import xl_col_to_name


# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Fund Scorecard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ─────────────────────────────────────────────────────────────────────────────
# STYLING
# ─────────────────────────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
        .block-container {
            max-width: 1500px;
            padding-top: 1.6rem;
            padding-bottom: 3rem;
        }

        [data-testid="stAppViewContainer"] {
            background:
                radial-gradient(circle at top right, rgba(78, 105, 162, 0.10), transparent 28rem),
                #f7f8fb;
        }

        [data-testid="stSidebar"] {
            background: #111827;
        }

        [data-testid="stSidebar"] * {
            color: #f9fafb;
        }

        .hero {
            padding: 1.65rem 1.85rem;
            border: 1px solid #e5e7eb;
            border-radius: 18px;
            background: rgba(255, 255, 255, 0.94);
            box-shadow: 0 10px 30px rgba(15, 23, 42, 0.06);
            margin-bottom: 1.1rem;
        }

        .hero-kicker {
            color: #64748b;
            font-size: 0.78rem;
            font-weight: 700;
            letter-spacing: 0.12em;
            text-transform: uppercase;
            margin-bottom: 0.45rem;
        }

        .hero h1 {
            color: #0f172a;
            font-size: clamp(2rem, 3vw, 3rem);
            line-height: 1.05;
            margin: 0;
        }

        .hero p {
            color: #475569;
            font-size: 1rem;
            line-height: 1.6;
            max-width: 820px;
            margin: 0.8rem 0 0;
        }

        .section-label {
            color: #64748b;
            font-size: 0.76rem;
            font-weight: 700;
            letter-spacing: 0.11em;
            text-transform: uppercase;
            margin: 1.2rem 0 0.45rem;
        }

        div[data-testid="stMetric"] {
            border: 1px solid #e5e7eb;
            border-radius: 14px;
            background: white;
            padding: 0.9rem 1rem;
            box-shadow: 0 4px 14px rgba(15, 23, 42, 0.04);
        }

        div[data-testid="stFileUploader"] {
            border: 1px dashed #94a3b8;
            border-radius: 16px;
            background: white;
            padding: 0.5rem;
        }

        div[data-testid="stDataFrame"] {
            border: 1px solid #e5e7eb;
            border-radius: 14px;
            overflow: hidden;
        }

        .empty-state {
            text-align: center;
            border: 1px dashed #cbd5e1;
            border-radius: 18px;
            background: rgba(255,255,255,0.75);
            padding: 3.2rem 1rem;
            color: #64748b;
        }

        .empty-state strong {
            display: block;
            color: #1e293b;
            font-size: 1.1rem;
            margin-bottom: 0.35rem;
        }

        .stDownloadButton > button {
            width: 100%;
            border-radius: 10px;
            font-weight: 650;
        }

        .stButton > button {
            border-radius: 10px;
            font-weight: 650;
        }

        footer {
            visibility: hidden;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# ─────────────────────────────────────────────────────────────────────────────
# CONSTANTS
# ─────────────────────────────────────────────────────────────────────────────
METRIC_NAMES = [
    "Manager Tenure",
    "Excess Performance",
    "Peer Return Rank",
    "Expense Ratio Rank",
    "Sharpe Ratio Rank",
    "R-Squared",
    "Sortino Ratio Rank",
    "Tracking Error Rank",
    "Tracking Error (3Yr)",
    "Tracking Error (5Yr)",
]

STATUS_ORDER = ["Review", "Pass", "Not Reported"]


# ─────────────────────────────────────────────────────────────────────────────
# PARSING HELPERS
# ─────────────────────────────────────────────────────────────────────────────
def clean_text(value: str) -> str:
    """Normalize whitespace while preserving readable fund names."""
    return re.sub(r"\s+", " ", str(value or "")).strip()


def build_ticker_lookup(pdf) -> dict[str, str]:
    """Build a fund-name-to-ticker lookup from stacked and inline PDF formats."""
    lookup: dict[str, str] = {}

    for page in pdf.pages:
        page_text = page.extract_text() or ""
        lines = [line.strip() for line in page_text.splitlines() if line.strip()]

        # Stacked format:
        # Fund Name
        # TICKER
        for index in range(len(lines) - 1):
            name_line = clean_text(lines[index])
            ticker_line = clean_text(lines[index + 1])

            if (
                re.fullmatch(r"[A-Z]{2,7}X?", ticker_line)
                and len(name_line.split()) >= 2
                and not re.fullmatch(r"[A-Z]{2,7}X?", name_line)
            ):
                lookup[name_line] = ticker_line

        # Inline format:
        # Fund Name TICKER
        for line in lines:
            match = re.match(r"^(.*?)\s+([A-Z]{2,7}X?)$", line)
            if match:
                fund_name = clean_text(match.group(1))
                ticker = match.group(2).strip()

                if len(fund_name.split()) >= 2:
                    lookup[fund_name] = ticker

    return lookup


def get_fund_name(block: str, lookup: dict[str, str]) -> str:
    """Find the most likely fund name for one scorecard block."""
    block_lower = block.lower()

    # Best case: exact fund name appears in the block.
    exact_matches = [
        name for name in lookup
        if name.lower() in block_lower
    ]
    if exact_matches:
        return max(exact_matches, key=len)

    lines = [clean_text(line) for line in block.splitlines() if clean_text(line)]

    # Try the first several lines as likely title lines.
    for line in lines[:8]:
        if len(line.split()) < 2:
            continue

        matches = get_close_matches(line, lookup.keys(), n=1, cutoff=0.58)
        if matches:
            return matches[0]

    # Fall back to the line immediately before the first metric.
    for index, line in enumerate(lines):
        if any(metric.lower() in line.lower() for metric in METRIC_NAMES):
            if index > 0:
                fallback = lines[index - 1]
                fallback = re.sub(
                    r"(this|the)?\s*fund\s+(has|meets).*",
                    "",
                    fallback,
                    flags=re.IGNORECASE,
                ).strip(" -:")
                if fallback:
                    return fallback
            break

    return "UNKNOWN FUND"


def extract_metrics(block: str) -> dict[str, str]:
    """Extract Pass/Review statuses from a scorecard block."""
    metrics: dict[str, str] = {}

    for raw_line in block.splitlines():
        line = clean_text(raw_line)

        for metric in METRIC_NAMES:
            if line.lower().startswith(metric.lower()):
                status_match = re.search(r"\b(Pass|Review)\b", line, flags=re.IGNORECASE)
                if status_match:
                    metrics[metric] = status_match.group(1).title()
                break

    return metrics


def resolve_ticker(
    fund_name: str,
    ticker_lookup: dict[str, str],
) -> str:
    """Resolve a ticker using exact, fuzzy, and partial-name matching."""
    if fund_name in ticker_lookup:
        return ticker_lookup[fund_name]

    if fund_name == "UNKNOWN FUND":
        return "N/A"

    fuzzy_match = get_close_matches(
        fund_name,
        ticker_lookup.keys(),
        n=1,
        cutoff=0.55,
    )
    if fuzzy_match:
        return ticker_lookup[fuzzy_match[0]]

    fund_lower = fund_name.lower()
    for known_name, ticker in ticker_lookup.items():
        known_lower = known_name.lower()
        if fund_lower in known_lower or known_lower in fund_lower:
            return ticker

    return "N/A"


def parse_scorecard(pdf_file) -> tuple[pd.DataFrame, int, int]:
    """Parse the uploaded PDF and return results, page count, and ticker count."""
    rows: list[dict[str, str]] = []

    with pdfplumber.open(pdf_file) as pdf:
        total_pages = len(pdf.pages)
        ticker_lookup = build_ticker_lookup(pdf)

        # Known exception retained from the original app.
        if not any("Enhanced Commodity" in name for name in ticker_lookup):
            ticker_lookup["WisdomTree Enhanced Commodity Stgy Fd"] = "WTES"

        progress = st.progress(0, text="Reading PDF...")
        status = st.empty()

        for page_number, page in enumerate(pdf.pages, start=1):
            page_text = page.extract_text() or ""

            if not page_text.strip():
                progress.progress(
                    page_number / total_pages,
                    text=f"Skipping page {page_number} of {total_pages}",
                )
                continue

            # Split when the next fund-status statement begins.
            blocks = re.split(
                r"\n(?=[^\n]*?(?:Fund\s+)?(?:Meets Watchlist Criteria|has been placed on watchlist))",
                page_text,
                flags=re.IGNORECASE,
            )

            for block in blocks:
                if not block.strip():
                    continue

                metrics = extract_metrics(block)
                if not metrics:
                    continue

                fund_name = get_fund_name(block, ticker_lookup)
                ticker = resolve_ticker(fund_name, ticker_lookup)

                is_watchlist = bool(
                    re.search(r"placed on watchlist", block, flags=re.IGNORECASE)
                )

                row = {
                    "Fund Name": fund_name,
                    "Ticker": ticker,
                    "Meets Criteria": "No" if is_watchlist else "Yes",
                    **metrics,
                }
                rows.append(row)

            status.text(f"Processed page {page_number} of {total_pages}")
            progress.progress(
                page_number / total_pages,
                text=f"Processed page {page_number} of {total_pages}",
            )

        progress.empty()
        status.empty()

    df = pd.DataFrame(rows)

    if not df.empty:
        # Ensure a predictable column order.
        ordered_columns = ["Fund Name", "Ticker", "Meets Criteria"] + [
            metric for metric in METRIC_NAMES if metric in df.columns
        ]
        df = df.reindex(columns=ordered_columns)

        # Remove duplicate fund rows produced by repeated PDF sections.
        df = df.drop_duplicates().reset_index(drop=True)

        # Fill missing metric values for display and export.
        metric_columns = [
            column for column in df.columns
            if column not in {"Fund Name", "Ticker", "Meets Criteria"}
        ]
        df[metric_columns] = df[metric_columns].fillna("Not Reported")

    return df, total_pages, len(ticker_lookup)


# ─────────────────────────────────────────────────────────────────────────────
# EXPORT HELPERS
# ─────────────────────────────────────────────────────────────────────────────
def create_excel_export(df: pd.DataFrame) -> bytes:
    """Create a polished Excel workbook with summary and detail sheets."""
    output = BytesIO()
    clean_df = df.fillna("").astype(str)

    total_funds = len(clean_df)
    meets_count = int((clean_df["Meets Criteria"] == "Yes").sum())
    watchlist_count = int((clean_df["Meets Criteria"] == "No").sum())
    missing_tickers = int((clean_df["Ticker"] == "N/A").sum())

    summary_df = pd.DataFrame(
        {
            "Metric": [
                "Total Funds",
                "Meets Criteria",
                "Watchlist",
                "Missing Tickers",
                "Generated",
            ],
            "Value": [
                total_funds,
                meets_count,
                watchlist_count,
                missing_tickers,
                datetime.now().strftime("%B %d, %Y at %I:%M %p"),
            ],
        }
    )

    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        summary_df.to_excel(
            writer,
            index=False,
            sheet_name="Summary",
            startrow=3,
        )
        clean_df.to_excel(
            writer,
            index=False,
            sheet_name="Fund Criteria",
            startrow=3,
        )

        workbook = writer.book
        summary_ws = writer.sheets["Summary"]
        detail_ws = writer.sheets["Fund Criteria"]

        title_format = workbook.add_format(
            {
                "bold": True,
                "font_size": 18,
                "font_color": "#FFFFFF",
                "bg_color": "#1F3A5F",
                "align": "left",
                "valign": "vcenter",
            }
        )
        subtitle_format = workbook.add_format(
            {
                "font_size": 10,
                "font_color": "#64748B",
                "italic": True,
            }
        )
        header_format = workbook.add_format(
            {
                "bold": True,
                "bg_color": "#DCE6F1",
                "font_color": "#1F3A5F",
                "align": "center",
                "valign": "vcenter",
                "border": 1,
            }
        )
        text_format = workbook.add_format({"border": 1, "valign": "top"})
        center_format = workbook.add_format(
            {"border": 1, "align": "center", "valign": "vcenter"}
        )
        pass_format = workbook.add_format(
            {
                "bg_color": "#E2F0D9",
                "font_color": "#2E6B2E",
                "border": 1,
                "align": "center",
            }
        )
        review_format = workbook.add_format(
            {
                "bg_color": "#FCE4D6",
                "font_color": "#9C2F1B",
                "border": 1,
                "align": "center",
            }
        )
        neutral_format = workbook.add_format(
            {
                "bg_color": "#F2F2F2",
                "font_color": "#666666",
                "border": 1,
                "align": "center",
            }
        )

        # Summary sheet
        summary_ws.merge_range("A1:B1", "Fund Scorecard Summary", title_format)
        summary_ws.write(
            "A2",
            "Overview of the latest uploaded MPI scorecard.",
            subtitle_format,
        )
        summary_ws.set_row(0, 28)
        summary_ws.set_column("A:A", 24)
        summary_ws.set_column("B:B", 28)
        summary_ws.freeze_panes(4, 0)

        for column_index, column_name in enumerate(summary_df.columns):
            summary_ws.write(3, column_index, column_name, header_format)

        # Detail sheet
        last_column = xl_col_to_name(len(clean_df.columns) - 1)
        detail_ws.merge_range(
            f"A1:{last_column}1",
            "Fund Scorecard Metrics",
            title_format,
        )
        detail_ws.write(
            "A2",
            f"Generated {datetime.now().strftime('%B %d, %Y at %I:%M %p')}",
            subtitle_format,
        )
        detail_ws.set_row(0, 28)
        detail_ws.freeze_panes(4, 0)
        detail_ws.autofilter(f"A4:{last_column}{len(clean_df) + 4}")

        for column_index, column_name in enumerate(clean_df.columns):
            detail_ws.write(3, column_index, column_name, header_format)

            max_length = max(
                len(column_name),
                clean_df[column_name].map(len).max() if not clean_df.empty else 0,
            )
            width = min(max(max_length + 2, 12), 42)
            detail_ws.set_column(column_index, column_index, width)

        for row_index in range(len(clean_df)):
            for column_index, column_name in enumerate(clean_df.columns):
                value = clean_df.iloc[row_index, column_index]

                if value in {"Pass", "Yes"}:
                    cell_format = pass_format
                elif value in {"Review", "No"}:
                    cell_format = review_format
                elif value in {"Not Reported", "N/A", ""}:
                    cell_format = neutral_format
                elif column_name in {"Ticker", "Meets Criteria"}:
                    cell_format = center_format
                else:
                    cell_format = text_format

                detail_ws.write(
                    row_index + 4,
                    column_index,
                    value,
                    cell_format,
                )

    output.seek(0)
    return output.getvalue()


def style_dataframe(df: pd.DataFrame):
    """Apply lightweight status highlighting inside Streamlit."""
    def highlight(value):
        if value in {"Pass", "Yes"}:
            return "background-color: #e8f3e5; color: #2e5f2e;"
        if value in {"Review", "No"}:
            return "background-color: #fbe9e2; color: #8a2f1d;"
        if value in {"Not Reported", "N/A"}:
            return "background-color: #f1f3f5; color: #6b7280;"
        return ""

    return df.style.map(highlight)


# ─────────────────────────────────────────────────────────────────────────────
# APP
# ─────────────────────────────────────────────────────────────────────────────
def run():
    st.markdown(
        """
        <div class="hero">
            <div class="hero-kicker">Investment Analysis Tool</div>
            <h1>Fund Scorecard</h1>
            <p>
                Upload an MPI-style PDF to identify fund watchlist status,
                review individual metric results, and export a presentation-ready report.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.sidebar:
        st.subheader("Scorecard Settings")
        st.caption("Use the filters after uploading a PDF.")

        uploaded_pdf = st.file_uploader(
            "Upload MPI PDF",
            type=["pdf"],
            help="Select a text-based MPI fund scorecard PDF.",
        )

        st.divider()
        st.caption(
            "The parser looks for Pass and Review labels associated with "
            "the standard scorecard metrics."
        )

    if uploaded_pdf is None:
        st.markdown(
            """
            <div class="empty-state">
                <strong>No scorecard uploaded</strong>
                Choose an MPI PDF from the sidebar to begin.
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    try:
        with st.spinner("Analyzing the scorecard..."):
            df, page_count, ticker_count = parse_scorecard(uploaded_pdf)
    except Exception as error:
        st.error("The PDF could not be processed.")
        with st.expander("Technical details"):
            st.code(str(error))
        return

    if df.empty:
        st.warning(
            "No fund entries were detected. The PDF may be scanned, use a different "
            "layout, or not contain recognizable Pass/Review metric labels."
        )
        return

    metric_columns = [
        column for column in df.columns
        if column not in {"Fund Name", "Ticker", "Meets Criteria"}
    ]

    total_funds = len(df)
    meets_count = int((df["Meets Criteria"] == "Yes").sum())
    watchlist_count = int((df["Meets Criteria"] == "No").sum())
    missing_tickers = int((df["Ticker"] == "N/A").sum())
    review_count = int((df[metric_columns] == "Review").sum().sum()) if metric_columns else 0

    st.markdown('<div class="section-label">Overview</div>', unsafe_allow_html=True)

    metric_1, metric_2, metric_3, metric_4, metric_5 = st.columns(5)
    metric_1.metric("Funds Found", total_funds)
    metric_2.metric("Meets Criteria", meets_count)
    metric_3.metric("Watchlist", watchlist_count)
    metric_4.metric("Review Flags", review_count)
    metric_5.metric("Missing Tickers", missing_tickers)

    st.caption(
        f"Processed {page_count} PDF page{'s' if page_count != 1 else ''} "
        f"and built a lookup containing {ticker_count} fund names."
    )

    st.markdown('<div class="section-label">Filters</div>', unsafe_allow_html=True)

    filter_col_1, filter_col_2, filter_col_3 = st.columns([1.2, 1.2, 2])

    criteria_options = ["All", "Meets Criteria", "Watchlist"]
    criteria_filter = filter_col_1.selectbox(
        "Criteria Status",
        criteria_options,
    )

    metric_filter = filter_col_2.selectbox(
        "Metric Status",
        ["All", "Pass", "Review", "Not Reported"],
    )

    search_text = filter_col_3.text_input(
        "Search Fund or Ticker",
        placeholder="Type a fund name or ticker...",
    )

    filtered_df = df.copy()

    if criteria_filter == "Meets Criteria":
        filtered_df = filtered_df[filtered_df["Meets Criteria"] == "Yes"]
    elif criteria_filter == "Watchlist":
        filtered_df = filtered_df[filtered_df["Meets Criteria"] == "No"]

    if metric_filter != "All" and metric_columns:
        filtered_df = filtered_df[
            filtered_df[metric_columns].eq(metric_filter).any(axis=1)
        ]

    if search_text.strip():
        query = search_text.strip()
        filtered_df = filtered_df[
            filtered_df["Fund Name"].str.contains(query, case=False, na=False)
            | filtered_df["Ticker"].str.contains(query, case=False, na=False)
        ]

    tab_results, tab_review, tab_export = st.tabs(
        ["All Results", "Review Queue", "Export"]
    )

    with tab_results:
        st.caption(
            f"Showing {len(filtered_df)} of {len(df)} fund entries."
        )
        st.dataframe(
            style_dataframe(filtered_df),
            use_container_width=True,
            hide_index=True,
            height=min(650, 82 + len(filtered_df) * 35),
        )

    with tab_review:
        review_mask = df["Meets Criteria"].eq("No")
        if metric_columns:
            review_mask = review_mask | df[metric_columns].eq("Review").any(axis=1)

        review_df = df[review_mask].copy()

        if review_df.empty:
            st.success("No watchlist funds or metric review flags were found.")
        else:
            st.caption(
                f"{len(review_df)} fund entr{'y' if len(review_df) == 1 else 'ies'} "
                "require attention."
            )
            st.dataframe(
                style_dataframe(review_df),
                use_container_width=True,
                hide_index=True,
                height=min(650, 82 + len(review_df) * 35),
            )

    with tab_export:
        st.subheader("Download Results")
        st.caption(
            "Exports include all detected funds, regardless of the active filters."
        )

        csv_data = df.to_csv(index=False).encode("utf-8")
        excel_data = create_excel_export(df)

        export_col_1, export_col_2 = st.columns(2)

        export_col_1.download_button(
            "Download CSV",
            data=csv_data,
            file_name="fund_scorecard_results.csv",
            mime="text/csv",
            use_container_width=True,
        )

        export_col_2.download_button(
            "Download Excel Report",
            data=excel_data,
            file_name="fund_scorecard_report.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True,
        )

        if missing_tickers:
            st.warning(
                f"{missing_tickers} fund entr{'y has' if missing_tickers == 1 else 'ies have'} "
                "an unresolved ticker. Review those rows before using the report."
            )


if __name__ == "__main__":
    run()
