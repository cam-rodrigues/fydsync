import streamlit as st
import pdfplumber
import pandas as pd
import re
from difflib import get_close_matches
from io import BytesIO
import xlsxwriter
from xlsxwriter.utility import xl_col_to_name
from datetime import datetime


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


def clean_text(value):
    return re.sub(r"\s+", " ", str(value or "")).strip()


# --- Ticker Lookup (stacked + inline formats) ---
def build_ticker_lookup(pdf):
    lookup = {}

    for page in pdf.pages:
        page_text = page.extract_text() or ""
        lines = [line.strip() for line in page_text.splitlines() if line.strip()]

        # Stacked format:
        # Fund Name
        # TICKER
        for i in range(len(lines) - 1):
            name_line = clean_text(lines[i])
            ticker_line = clean_text(lines[i + 1])

            if (
                re.fullmatch(r"[A-Z]{2,7}X?", ticker_line)
                and len(name_line.split()) >= 2
                and not re.fullmatch(r"[A-Z]{2,7}X?", name_line)
            ):
                lookup[name_line] = ticker_line

        # Inline format:
        # Fund Name TICKER
        for line in lines:
            match = re.match(r"^(.*?)\s+([A-Z]{2,7}X?)$", line.strip())

            if match:
                fund_name = clean_text(match.group(1))
                ticker = match.group(2).strip()

                if len(fund_name.split()) >= 2:
                    lookup[fund_name] = ticker

    return lookup


# --- Extract fund name from block ---
def get_fund_name(block, lookup):
    block_lower = block.lower()

    # Prefer the longest exact fund-name match in the block.
    exact_matches = [
        name for name in lookup
        if name.lower() in block_lower
    ]

    if exact_matches:
        return max(exact_matches, key=len)

    lines = [clean_text(line) for line in block.splitlines() if clean_text(line)]
    top_lines = lines[:8]

    # Try likely title lines near the top of the block.
    for line in top_lines:
        if len(line.split()) < 2:
            continue

        matches = get_close_matches(line, lookup.keys(), n=1, cutoff=0.58)

        if matches:
            return matches[0]

    # Fall back to the line immediately before the first metric.
    for i, line in enumerate(lines):
        if any(metric.lower() in line.lower() for metric in METRIC_NAMES):
            if i > 0:
                fallback_name = lines[i - 1].strip()
                fallback_name = re.sub(
                    r"(This|The)?\s*fund\s+(has|meets).*",
                    "",
                    fallback_name,
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
                status_match = re.search(
                    r"\b(Pass|Review)\b",
                    line,
                    flags=re.IGNORECASE,
                )

                if status_match:
                    metrics[metric_name] = status_match.group(1).title()

                break

    return metrics


def resolve_ticker(fund_name, ticker_lookup):
    if fund_name in ticker_lookup:
        return ticker_lookup[fund_name]

    if fund_name == "UNKNOWN FUND":
        return "N/A"

    match = get_close_matches(
        fund_name,
        ticker_lookup.keys(),
        n=1,
        cutoff=0.55,
    )

    if match:
        return ticker_lookup[match[0]]

    fund_name_lower = fund_name.lower()

    for known_name, ticker in ticker_lookup.items():
        known_name_lower = known_name.lower()

        if (
            fund_name_lower in known_name_lower
            or known_name_lower in fund_name_lower
        ):
            return ticker

    return "N/A"


def create_excel_export(df):
    output = BytesIO()
    df_cleaned = df.fillna("").astype(str)

    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df_cleaned.to_excel(
            writer,
            index=False,
            sheet_name="Fund Criteria",
            startrow=2,
        )

        workbook = writer.book
        worksheet = writer.sheets["Fund Criteria"]

        header_format = workbook.add_format({
            "bold": True,
            "bg_color": "#D9E1F2",
            "font_color": "#1F4E78",
            "align": "center",
            "valign": "vcenter",
            "border": 1,
            "bottom": 2,
        })

        status_format_pass = workbook.add_format({
            "bg_color": "#C6EFCE",
            "font_color": "#006100",
            "border": 1,
            "align": "center",
        })

        status_format_review = workbook.add_format({
            "bg_color": "#FFC7CE",
            "font_color": "#9C0006",
            "border": 1,
            "align": "center",
        })

        neutral_format = workbook.add_format({
            "bg_color": "#E7E6E6",
            "font_color": "#666666",
            "border": 1,
            "align": "center",
        })

        normal_format = workbook.add_format({
            "border": 1,
            "valign": "top",
        })

        center_format = workbook.add_format({
            "border": 1,
            "align": "center",
            "valign": "vcenter",
        })

        updated_format = workbook.add_format({
            "italic": True,
            "font_color": "#444444",
        })

        worksheet.write(
            "A1",
            datetime.now().strftime("Last Updated: %B %d, %Y"),
            updated_format,
        )

        for col_num, col_name in enumerate(df_cleaned.columns):
            values = df_cleaned[col_name].astype(str)
            max_value_length = values.map(len).max() if not values.empty else 0
            max_len = max(max_value_length, len(col_name)) + 2

            # Prevent extremely wide columns caused by long PDF text.
            max_len = min(max_len, 45)

            worksheet.set_column(col_num, col_num, max_len)
            worksheet.write(2, col_num, col_name, header_format)

        last_col = xl_col_to_name(len(df_cleaned.columns) - 1)
        last_row = len(df_cleaned) + 3

        worksheet.autofilter(f"A3:{last_col}{last_row}")
        worksheet.freeze_panes(3, 0)

        for row_num in range(len(df_cleaned)):
            for col_num, col_name in enumerate(df_cleaned.columns):
                value = df_cleaned.iloc[row_num, col_num]

                if value in {"Pass", "Yes"}:
                    cell_format = status_format_pass
                elif value in {"Review", "No"}:
                    cell_format = status_format_review
                elif value in {"N/A", "Not Reported", ""}:
                    cell_format = neutral_format
                elif col_name in {"Ticker", "Meets Criteria"}:
                    cell_format = center_format
                else:
                    cell_format = normal_format

                worksheet.write(
                    row_num + 3,
                    col_num,
                    value,
                    cell_format,
                )

    output.seek(0)
    return output.getvalue()


# --- Main App ---
def run():
    st.set_page_config(page_title="Fund Scorecard Metrics", layout="wide")
    st.title("Fund Scorecard Metrics")

    st.markdown("""
    Upload an MPI-style PDF fund scorecard below. The app will extract each fund, determine if it meets the watchlist criteria, and display a detailed breakdown of metric statuses.
    """)

    pdf_file = st.file_uploader("Upload MPI PDF", type=["pdf"])

    if pdf_file:
        rows = []

        try:
            with pdfplumber.open(pdf_file) as pdf:
                total_pages = len(pdf.pages)
                status_text = st.empty()
                progress = st.progress(0)

                ticker_lookup = build_ticker_lookup(pdf)

                if not any(
                    "Enhanced Commodity" in name
                    for name in ticker_lookup
                ):
                    ticker_lookup[
                        "WisdomTree Enhanced Commodity Stgy Fd"
                    ] = "WTES"

                for i, page in enumerate(pdf.pages):
                    txt = page.extract_text() or ""

                    if not txt.strip():
                        progress.progress((i + 1) / total_pages)
                        status_text.text(
                            f"Skipping page {i + 1} of {total_pages} (no text found)..."
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
                        ticker = resolve_ticker(
                            fund_name,
                            ticker_lookup,
                        )

                        placed_on_watchlist = bool(
                            re.search(
                                r"placed on watchlist",
                                block,
                                flags=re.IGNORECASE,
                            )
                        )

                        rows.append({
                            "Fund Name": fund_name,
                            "Ticker": ticker,
                            "Meets Criteria": (
                                "No"
                                if placed_on_watchlist
                                else "Yes"
                            ),
                            **metrics,
                        })

                    progress.progress((i + 1) / total_pages)
                    status_text.text(
                        f"Processed page {i + 1} of {total_pages}"
                    )

                progress.empty()
                status_text.empty()

        except Exception as error:
            st.error("The PDF could not be processed.")

            with st.expander("Technical details"):
                st.code(str(error))

            return

        df = pd.DataFrame(rows)

        if not df.empty:
            ordered_columns = [
                "Fund Name",
                "Ticker",
                "Meets Criteria",
            ] + [
                metric
                for metric in METRIC_NAMES
                if metric in df.columns
            ]

            df = df.reindex(columns=ordered_columns)

            # Remove duplicate rows that can occur when the same fund block
            # appears more than once in the PDF text extraction.
            df = df.drop_duplicates().reset_index(drop=True)

            metric_columns = [
                column
                for column in df.columns
                if column not in {
                    "Fund Name",
                    "Ticker",
                    "Meets Criteria",
                }
            ]

            if metric_columns:
                df[metric_columns] = df[metric_columns].fillna(
                    "Not Reported"
                )

            st.success(f"Found {len(df)} fund entries.")
            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True,
            )

            unresolved_tickers = int(
                (df["Ticker"] == "N/A").sum()
            )

            if unresolved_tickers:
                st.warning(
                    f"{unresolved_tickers} fund "
                    f"{'has' if unresolved_tickers == 1 else 'have'} "
                    "an unresolved ticker."
                )

            with st.expander("Download Results"):
                csv = df.to_csv(index=False).encode("utf-8")

                st.download_button(
                    "Download as CSV",
                    data=csv,
                    file_name="fund_criteria_results.csv",
                    mime="text/csv",
                )

                excel_data = create_excel_export(df)

                st.download_button(
                    "Download as Excel",
                    data=excel_data,
                    file_name="fund_criteria_results.xlsx",
                    mime=(
                        "application/"
                        "vnd.openxmlformats-officedocument."
                        "spreadsheetml.sheet"
                    ),
                )

        else:
            st.warning(
                "No fund entries found in the uploaded PDF. "
                "The file may be scanned or use an unsupported layout."
            )

    else:
        st.info("Please upload an MPI fund scorecard PDF to begin.")


if __name__ == "__main__":
    run()
