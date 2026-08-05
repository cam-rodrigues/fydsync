import streamlit as st
import pdfplumber
import pandas as pd
import re
from difflib import get_close_matches
from io import BytesIO
import xlsxwriter
from xlsxwriter.utility import xl_col_to_name
from datetime import datetime
import random
import hashlib


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

STATUS_COLUMNS = {"Fund Name", "Ticker", "Meets Criteria"}


LOADING_MESSAGES = [
    "Pricing optimism...",
    "Finding missing decimals...",
    "Looking for the merged cell...",
    "Checking if it's actually a typo...",
    "Consulting Warren Buffett...",
    "Counting zeros...",
    "Reading footnotes...",
    "Pretending this is instant...",
    "Summoning Yahoo Finance...",
    "Reassuring the cache...",
    "Politely asking Excel to cooperate...",
    "Reconciling reality with spreadsheets...",
    "Adjusting for market drama...",
    "Verifying suspiciously round numbers...",
    "Organizing the chaos...",
    "Finding funds that forgot their ticker...",
    "Doing math so you don't have to...",
    "Checking for hidden surprises...",
    "Making the PDF slightly less mysterious...",
    "Untangling formatting decisions...",
    "Searching for lost commas...",
    "Reviewing the review flags...",
    "Following the breadcrumbs...",
    "Reading between the rows...",
    "Making sense of the scorecards...",
    "Negotiating with the PDF...",
    "Waiting for page numbers to behave...",
    "Calibrating financial jargon...",
    "Dusting off the spreadsheets...",
    "Double-checking everything twice...",
]

TICKER_LOADING_MESSAGES = [
    "Matching funds to tickers...",
    "Looking up symbols...",
    "Finding funds that forgot their ticker...",
    "Summoning Yahoo Finance...",
    "Checking the fine print for ticker clues...",
    "Translating fund names into symbols...",
]

PARSING_LOADING_MESSAGES = [
    "Reading footnotes...",
    "Checking if it's actually a typo...",
    "Negotiating with the PDF...",
    "Looking for the merged cell...",
    "Finding missing decimals...",
    "Counting zeros...",
    "Reading between the rows...",
    "Making the PDF slightly less mysterious...",
    "Searching for lost commas...",
    "Waiting for page numbers to behave...",
]

CLEANUP_LOADING_MESSAGES = [
    "Organizing the chaos...",
    "Reviewing the review flags...",
    "Reconciling reality with spreadsheets...",
    "Verifying suspiciously round numbers...",
    "Double-checking everything twice...",
    "Calibrating financial jargon...",
]

EXPORT_LOADING_MESSAGES = [
    "Teaching Excel some manners...",
    "Formatting cells...",
    "Adding just enough color...",
    "Politely asking Excel to cooperate...",
    "Reassuring the cache...",
    "Almost ready...",
]


def random_loading_message(pool=None):
    return random.choice(pool or LOADING_MESSAGES)



def clean_text(value):
    return re.sub(r"\s+", " ", str(value or "")).strip()


# --- Ticker Lookup (stacked + inline formats) ---
def build_ticker_lookup(pdf):
    lookup = {}

    for page in pdf.pages:
        page_text = page.extract_text() or ""
        lines = [clean_text(line) for line in page_text.splitlines() if clean_text(line)]

        # Stacked format:
        # Fund Name
        # TICKER
        for i in range(len(lines) - 1):
            name_line = lines[i]
            ticker_line = lines[i + 1]

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


# --- Extract fund name from block ---
def get_fund_name(block, lookup):
    block_lower = block.lower()

    exact_matches = [name for name in lookup if name.lower() in block_lower]
    if exact_matches:
        return max(exact_matches, key=len)

    lines = [clean_text(line) for line in block.splitlines() if clean_text(line)]

    for line in lines[:8]:
        if len(line.split()) < 2:
            continue

        matches = get_close_matches(line, lookup.keys(), n=1, cutoff=0.58)
        if matches:
            return matches[0]

    for i, line in enumerate(lines):
        if any(metric.lower() in line.lower() for metric in METRIC_NAMES):
            if i > 0:
                fallback_name = re.sub(
                    r"(This|The)?\s*fund\s+(has|meets).*",
                    "",
                    lines[i - 1],
                    flags=re.IGNORECASE,
                ).strip(" -:")
                if fallback_name:
                    return fallback_name
            break

    return "UNKNOWN FUND"


def extract_metrics(block):
    metrics = {}

    for raw_line in block.splitlines():
        line = clean_text(raw_line)

        for metric_name in METRIC_NAMES:
            if line.lower().startswith(metric_name.lower()):
                status_match = re.search(r"\b(Pass|Review)\b", line, flags=re.IGNORECASE)
                if status_match:
                    metrics[metric_name] = status_match.group(1).title()
                break

    return metrics


def resolve_ticker(fund_name, ticker_lookup):
    if fund_name in ticker_lookup:
        return ticker_lookup[fund_name]

    if fund_name == "UNKNOWN FUND":
        return "N/A"

    match = get_close_matches(fund_name, ticker_lookup.keys(), n=1, cutoff=0.55)
    if match:
        return ticker_lookup[match[0]]

    fund_name_lower = fund_name.lower()
    for known_name, ticker in ticker_lookup.items():
        known_name_lower = known_name.lower()
        if fund_name_lower in known_name_lower or known_name_lower in fund_name_lower:
            return ticker

    return "N/A"


def style_results(df):
    def color_status(value):
        if value in {"Pass", "Yes"}:
            return "background-color: #EAF4EA; color: #286231; font-weight: 600;"
        if value in {"Review", "No"}:
            return "background-color: #FCEBE8; color: #9B3328; font-weight: 600;"
        if value in {"Not Reported", "N/A", "UNKNOWN FUND"}:
            return "background-color: #F2F4F7; color: #667085;"
        return ""

    return df.style.map(color_status)


def create_excel_export(df):
    output = BytesIO()
    df_cleaned = df.fillna("").astype(str)

    total_funds = len(df_cleaned)
    meets_count = int((df_cleaned["Meets Criteria"] == "Yes").sum())
    watchlist_count = int((df_cleaned["Meets Criteria"] == "No").sum())
    unresolved_count = int((df_cleaned["Ticker"] == "N/A").sum())

    summary_df = pd.DataFrame({
        "Summary": ["Total Funds", "Meets Criteria", "Watchlist", "Unresolved Tickers"],
        "Count": [total_funds, meets_count, watchlist_count, unresolved_count],
    })

    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        summary_df.to_excel(writer, index=False, sheet_name="Summary", startrow=3)
        df_cleaned.to_excel(writer, index=False, sheet_name="Fund Criteria", startrow=3)

        workbook = writer.book
        summary_sheet = writer.sheets["Summary"]
        worksheet = writer.sheets["Fund Criteria"]

        title_format = workbook.add_format({
            "bold": True,
            "font_size": 18,
            "font_color": "#FFFFFF",
            "bg_color": "#203864",
            "align": "left",
            "valign": "vcenter",
        })
        subtitle_format = workbook.add_format({
            "italic": True,
            "font_color": "#667085",
        })
        header_format = workbook.add_format({
            "bold": True,
            "bg_color": "#D9E2F3",
            "font_color": "#203864",
            "align": "center",
            "valign": "vcenter",
            "border": 1,
        })
        pass_format = workbook.add_format({
            "bg_color": "#E2F0D9",
            "font_color": "#286231",
            "border": 1,
            "align": "center",
        })
        review_format = workbook.add_format({
            "bg_color": "#FCE4D6",
            "font_color": "#9C0006",
            "border": 1,
            "align": "center",
        })
        neutral_format = workbook.add_format({
            "bg_color": "#F2F2F2",
            "font_color": "#666666",
            "border": 1,
            "align": "center",
        })
        normal_format = workbook.add_format({"border": 1, "valign": "top"})
        center_format = workbook.add_format({"border": 1, "align": "center"})

        # Summary sheet
        summary_sheet.merge_range("A1:B1", "Fund Scorecard Summary", title_format)
        summary_sheet.write("A2", datetime.now().strftime("Generated %B %d, %Y at %I:%M %p"), subtitle_format)
        summary_sheet.set_row(0, 28)
        summary_sheet.set_column("A:A", 24)
        summary_sheet.set_column("B:B", 18)
        summary_sheet.freeze_panes(4, 0)
        for col_num, col_name in enumerate(summary_df.columns):
            summary_sheet.write(3, col_num, col_name, header_format)

        # Detail sheet
        last_col = xl_col_to_name(len(df_cleaned.columns) - 1)
        last_row = len(df_cleaned) + 4
        worksheet.merge_range(f"A1:{last_col}1", "Fund Scorecard Metrics", title_format)
        worksheet.write("A2", datetime.now().strftime("Generated %B %d, %Y at %I:%M %p"), subtitle_format)
        worksheet.set_row(0, 28)
        worksheet.freeze_panes(4, 0)
        worksheet.autofilter(f"A4:{last_col}{last_row}")

        for col_num, col_name in enumerate(df_cleaned.columns):
            values = df_cleaned[col_name].astype(str)
            max_value_length = values.map(len).max() if not values.empty else 0
            max_len = min(max(max_value_length, len(col_name)) + 2, 42)
            worksheet.set_column(col_num, col_num, max_len)
            worksheet.write(3, col_num, col_name, header_format)

        for row_num in range(len(df_cleaned)):
            for col_num, col_name in enumerate(df_cleaned.columns):
                value = df_cleaned.iloc[row_num, col_num]

                if value in {"Pass", "Yes"}:
                    cell_format = pass_format
                elif value in {"Review", "No"}:
                    cell_format = review_format
                elif value in {"N/A", "Not Reported", "", "UNKNOWN FUND"}:
                    cell_format = neutral_format
                elif col_name in {"Ticker", "Meets Criteria"}:
                    cell_format = center_format
                else:
                    cell_format = normal_format

                worksheet.write(row_num + 4, col_num, value, cell_format)

    output.seek(0)
    return output.getvalue()


# --- Main App ---
def run():
    st.set_page_config(page_title="Fund Scorecard Metrics", layout="wide")

    st.markdown(
        """
        <style>
            .block-container {
                max-width: 1450px;
                padding-top: 2rem;
                padding-bottom: 3rem;
            }

            h1 {
                color: #16243A;
                letter-spacing: -0.03em;
                margin-bottom: 0.3rem;
            }

            .app-subtitle {
                color: #667085;
                font-size: 1rem;
                line-height: 1.55;
                margin-bottom: 1.35rem;
                max-width: 860px;
            }

            .section-label {
                color: #475467;
                font-size: 0.77rem;
                font-weight: 700;
                letter-spacing: 0.08em;
                text-transform: uppercase;
                margin-top: 1.3rem;
                margin-bottom: 0.5rem;
            }

            div[data-testid="stFileUploader"] {
                border: 1px solid #D0D5DD;
                border-radius: 14px;
                background: #FFFFFF;
                padding: 0.4rem;
            }

            div[data-testid="stMetric"] {
                background: #FFFFFF;
                border: 1px solid #E4E7EC;
                border-radius: 12px;
                padding: 0.85rem 1rem;
                box-shadow: 0 3px 12px rgba(16, 24, 40, 0.04);
            }

            div[data-testid="stDataFrame"] {
                border: 1px solid #E4E7EC;
                border-radius: 12px;
                overflow: hidden;
            }

            .stDownloadButton > button {
                border-radius: 9px;
                font-weight: 600;
            }

            div[data-testid="stExpander"] {
                border: 1px solid #E4E7EC;
                border-radius: 12px;
                overflow: hidden;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.title("Fund Scorecard Metrics")
    st.markdown(
        """
        <div class="app-subtitle">
            Upload an MPI-style PDF fund scorecard. The app will identify each fund,
            determine its watchlist status, and organize the metric results into a
            review-ready table and downloadable report.
        </div>
        """,
        unsafe_allow_html=True,
    )

    pdf_file = st.file_uploader(
        "Upload MPI PDF",
        type=["pdf"],
        help="Upload a text-based MPI fund scorecard PDF.",
    )

    if not pdf_file:
        st.info("Upload an MPI fund scorecard PDF to begin.")
        return

    pdf_bytes = pdf_file.getvalue()
    pdf_key = hashlib.sha256(pdf_bytes).hexdigest()

    # Streamlit reruns the script after button clicks. Keep the processed
    # dataframe in session state so downloading does not parse the PDF again.
    if st.session_state.get("processed_pdf_key") != pdf_key:
        rows = []

        try:
            with pdfplumber.open(BytesIO(pdf_bytes)) as pdf:
                total_pages = len(pdf.pages)
                status_text = st.empty()
                status_text.caption(random_loading_message(TICKER_LOADING_MESSAGES))
                progress = st.progress(0, text="Preparing fund lookup...")
                ticker_lookup = build_ticker_lookup(pdf)

                if not any("Enhanced Commodity" in name for name in ticker_lookup):
                    ticker_lookup["WisdomTree Enhanced Commodity Stgy Fd"] = "WTES"

                for i, page in enumerate(pdf.pages):
                    txt = page.extract_text() or ""

                    if not txt.strip():
                        progress.progress(
                            (i + 1) / total_pages,
                            text=f"Page {i + 1} of {total_pages}",
                        )
                        status_text.caption(
                            f"{random_loading_message(PARSING_LOADING_MESSAGES)} "
                            f"Skipping page {i + 1}: no readable text found."
                        )
                        continue

                    blocks = re.split(
                        r"\n(?=[^\n]*?(?:Fund\s+)?(?:Meets Watchlist Criteria|has been placed on watchlist))",
                        txt,
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
                        placed_on_watchlist = bool(
                            re.search(r"placed on watchlist", block, flags=re.IGNORECASE)
                        )

                        rows.append({
                            "Fund Name": fund_name,
                            "Ticker": ticker,
                            "Meets Criteria": "No" if placed_on_watchlist else "Yes",
                            **metrics,
                        })

                    progress.progress(
                        (i + 1) / total_pages,
                        text=f"Page {i + 1} of {total_pages}",
                    )
                    status_text.caption(
                        random_loading_message(PARSING_LOADING_MESSAGES)
                    )

                progress.empty()
                status_text.empty()

        except Exception as error:
            st.error("The PDF could not be processed.")
            with st.expander("Technical details"):
                st.code(str(error))
            return

        cleanup_status = st.empty()
        cleanup_status.caption(random_loading_message(CLEANUP_LOADING_MESSAGES))

        df = pd.DataFrame(rows)

        if df.empty:
            cleanup_status.empty()
            st.warning(
                "No fund entries were found. The PDF may be scanned, use a different layout, "
                "or not contain recognizable Pass/Review labels."
            )
            return

        ordered_columns = ["Fund Name", "Ticker", "Meets Criteria"] + [
            metric for metric in METRIC_NAMES if metric in df.columns
        ]
        df = df.reindex(columns=ordered_columns)
        df = df.drop_duplicates().reset_index(drop=True)

        metric_columns = [column for column in df.columns if column not in STATUS_COLUMNS]
        if metric_columns:
            df[metric_columns] = df[metric_columns].fillna("Not Reported")

        cleanup_status.empty()

        st.session_state.processed_pdf_key = pdf_key
        st.session_state.processed_pdf_df = df

        # A new upload invalidates any previously prepared downloads.
        st.session_state.pop("export_pdf_key", None)
        st.session_state.pop("export_csv", None)
        st.session_state.pop("export_excel", None)
    else:
        df = st.session_state.processed_pdf_df.copy()
        metric_columns = [column for column in df.columns if column not in STATUS_COLUMNS]

    total_funds = len(df)
    meets_count = int((df["Meets Criteria"] == "Yes").sum())
    watchlist_count = int((df["Meets Criteria"] == "No").sum())
    unresolved_tickers = int((df["Ticker"] == "N/A").sum())
    review_flags = int((df[metric_columns] == "Review").sum().sum()) if metric_columns else 0

    st.success(f"Successfully found {total_funds} fund entries.")

    st.markdown('<div class="section-label">Overview</div>', unsafe_allow_html=True)
    metric_1, metric_2, metric_3, metric_4 = st.columns(4)
    metric_1.metric("Total Funds", total_funds)
    metric_2.metric("Meets Criteria", meets_count)
    metric_3.metric("Watchlist", watchlist_count)
    metric_4.metric("Review Flags", review_flags)

    st.markdown('<div class="section-label">Results</div>', unsafe_allow_html=True)

    filter_col_1, filter_col_2 = st.columns([1, 2])
    criteria_filter = filter_col_1.selectbox(
        "Filter by status",
        ["All Funds", "Meets Criteria", "Watchlist"],
    )
    search_term = filter_col_2.text_input(
        "Search fund or ticker",
        placeholder="Start typing a fund name or ticker...",
    )

    filtered_df = df.copy()
    if criteria_filter == "Meets Criteria":
        filtered_df = filtered_df[filtered_df["Meets Criteria"] == "Yes"]
    elif criteria_filter == "Watchlist":
        filtered_df = filtered_df[filtered_df["Meets Criteria"] == "No"]

    if search_term.strip():
        query = search_term.strip()
        filtered_df = filtered_df[
            filtered_df["Fund Name"].str.contains(query, case=False, na=False)
            | filtered_df["Ticker"].str.contains(query, case=False, na=False)
        ]

    st.caption(f"Showing {len(filtered_df)} of {len(df)} fund entries.")
    st.dataframe(
        style_results(filtered_df),
        use_container_width=True,
        hide_index=True,
        height=min(680, 76 + max(len(filtered_df), 1) * 35),
    )

    if unresolved_tickers:
        st.warning(
            f"{unresolved_tickers} fund {'has' if unresolved_tickers == 1 else 'have'} "
            "an unresolved ticker and should be reviewed before export."
        )

    with st.expander("Download Results", expanded=False):
        st.caption("Downloads include all detected funds, not only the currently filtered rows.")

        if st.session_state.get("export_pdf_key") != pdf_key:
            export_status = st.empty()
            export_status.caption(random_loading_message(EXPORT_LOADING_MESSAGES))

            st.session_state.export_csv = df.to_csv(index=False).encode("utf-8")
            st.session_state.export_excel = create_excel_export(df)
            st.session_state.export_pdf_key = pdf_key

            export_status.empty()

        csv = st.session_state.export_csv
        excel_data = st.session_state.export_excel

        download_col_1, download_col_2 = st.columns(2)
        download_col_1.download_button(
            "Download as CSV",
            data=csv,
            file_name="fund_criteria_results.csv",
            mime="text/csv",
            use_container_width=True,
        )
        download_col_2.download_button(
            "Download as Excel",
            data=excel_data,
            file_name="fund_criteria_results.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True,
        )


if __name__ == "__main__":
    run()
