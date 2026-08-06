import re
import streamlit as st
import pdfplumber
from calendar import month_name
import pandas as pd
from rapidfuzz import fuzz
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_VERTICAL_ANCHOR
from io import BytesIO
import yfinance as yf

# ─── Performance Table ───────────────────────────────────────────────────────

def extract_performance_table(pdf, performance_page, fund_names, end_page=None):
    end = end_page if end_page is not None else len(pdf.pages) + 1
    lines = []
    for pnum in range(performance_page - 1, end - 1):
        txt = pdf.pages[pnum].extract_text() or ""
        lines += [ln.strip() for ln in txt.splitlines() if ln.strip()]
    num_rx = re.compile(r"\(?-?\d+\.\d+%?\)?")
    perf_data = []
    for name in fund_names:
        item = {"Fund Scorecard Name": name}
        idx = next((i for i, ln in enumerate(lines) if name in ln), None)
        if idx is None:
            scores = [(i, fuzz.token_sort_ratio(name.lower(), ln.lower())) for i, ln in enumerate(lines)]
            best_i, best_score = max(scores, key=lambda x: x[1])
            if best_score > 60:
                idx = best_i
            else:
                continue
        raw = num_rx.findall(lines[idx - 1]) if idx >= 1 else []
        if len(raw) < 8 and idx >= 2:
            raw = num_rx.findall(lines[idx - 2]) + raw
        clean = [n.strip("()%").rstrip("%") for n in raw]
        clean += [None] * (8 - len(clean))
        item["QTD"] = clean[0]
        item["1Yr"] = clean[2]
        item["3Yr"] = clean[3]
        item["5Yr"] = clean[4]
        item["10Yr"] = clean[5]
        item["Net Expense Ratio"] = clean[-2]
        bench_raw = []
        if idx + 1 < len(lines):
            bench_raw = num_rx.findall(lines[idx + 1])
        if len(bench_raw) < 1 and idx + 2 < len(lines):
            bench_raw = num_rx.findall(lines[idx + 2])
        bench_clean = [n.strip("()%").rstrip("%") for n in bench_raw]
        item["Bench QTD"] = bench_clean[0] if bench_clean else None
        item["Bench 3Yr"] = bench_clean[3] if len(bench_clean) > 3 else None
        item["Bench 5Yr"] = bench_clean[4] if len(bench_clean) > 4 else None
        perf_data.append(item)
    return perf_data

# ─── Utility ────────────────────────────────────────────────────────────────

def extract_report_date(text):
    dates = re.findall(r'(\d{1,2})/(\d{1,2})/(20\d{2})', text or "")
    for month, day, year in dates:
        m, d = int(month), int(day)
        quarter_map = {(3,31): "1st", (6,30): "2nd", (9,30): "3rd", (12,31): "4th"}
        if (m, d) in quarter_map:
            return f"{quarter_map[(m, d)]} QTR, {year}"
        return f"As of {month_name[m]} {d}, {year}"
    return None

# ─── Page 1 Extraction ─────────────────────────────────────────────────────

def process_page1(text):
    report_date = extract_report_date(text)
    st.session_state['report_date'] = report_date if report_date else None
    m = re.search(r"Total Options:\s*(\d+)", text or "")
    st.session_state['total_options'] = int(m.group(1)) if m else None
    m = re.search(r"Prepared For:\s*\n(.*)", text or "")
    st.session_state['prepared_for'] = m.group(1).strip() if m else None
    m = re.search(r"Prepared By:\s*(.*)", text or "")
    pb = m.group(1).strip() if m else ""
    if not pb or "mpi stylus" in pb.lower():
        pb = "Procyon Partners, LLC"
    st.session_state['prepared_by'] = pb

# ─── Info Card ─────────────────────────────────────────────────────────────

def show_report_summary():
    report_date    = st.session_state.get('report_date', 'N/A')
    total_options  = st.session_state.get('total_options', 'N/A')
    prepared_for   = st.session_state.get('prepared_for', 'N/A')
    prepared_by    = st.session_state.get('prepared_by', 'N/A')
    st.markdown(f"""
        <div style="
            background: linear-gradient(120deg, #e6f0fb 80%, #c8e0f6 100%);
            color: #244369;
            border-radius: 1.5rem;
            box-shadow: 0 4px 24px rgba(44,85,130,0.11), 0 2px 8px rgba(36,67,105,0.09);
            padding: 1.2rem 2.3rem 1.2rem 2.3rem;
            margin-bottom: 2rem;
            font-size: 1.08rem;
            border: 1.2px solid #b5d0eb;">
            <div style="color:#244369;">
                <b>Report Date:</b> {report_date} <br>
                <b>Total Options:</b> {total_options} <br>
                <b>Prepared For:</b> {prepared_for} <br>
                <b>Prepared By:</b> {prepared_by}
            </div>
        </div>
    """, unsafe_allow_html=True)

# ─── Table of Contents Extraction ──────────────────────────────────────────

def process_toc(text):
    perf = re.search(r"Fund Performance[^\d]*(\d{1,3})", text or "")
    cy   = re.search(r"Fund Performance: Calendar Year\s+(\d{1,3})", text or "")
    r3yr = re.search(r"Risk Analysis: MPT Statistics \(3Yr\)\s+(\d{1,3})", text or "")
    r5yr = re.search(r"Risk Analysis: MPT Statistics \(5Yr\)\s+(\d{1,3})", text or "")
    sc   = re.search(r"Fund Scorecard\s+(\d{1,3})", text or "")
    sc_prop = re.search(r"Fund Scorecard:\s*Proposed Funds\s+(\d{1,3})", text or "")
    fs   = re.search(r"Fund Factsheets\s+(\d{1,3})", text or "")
    fs_prop = re.search(r"Fund Factsheets:\s*Proposed Funds\s+(\d{1,3})", text or "")
    st.session_state['performance_page'] = int(perf.group(1)) if perf else None
    st.session_state['calendar_year_page'] = int(cy.group(1)) if cy else None
    st.session_state['r3yr_page'] = int(r3yr.group(1)) if r3yr else None
    st.session_state['r5yr_page'] = int(r5yr.group(1)) if r5yr else None
    st.session_state['scorecard_page'] = int(sc.group(1)) if sc else None
    st.session_state['scorecard_proposed_page'] = int(sc_prop.group(1)) if sc_prop else None
    st.session_state['factsheets_page'] = int(fs.group(1)) if fs else None
    st.session_state['factsheets_proposed_page'] = int(fs_prop.group(1)) if fs_prop else None

# ─── IPS Investment Screening ──────────────────────────────────────────────

def infer_fund_type_guess(ticker):
    try:
        if not ticker:
            return ""
        info = yf.Ticker(ticker).info
        name = (info.get("longName") or info.get("shortName") or "").lower()
        summary = (info.get("longBusinessSummary") or "").lower()
        if "index" in name or "index" in summary:
            return "Passive"
        if "track" in summary and "index" in summary:
            return "Passive"
        if "actively managed" in summary or "actively-managed" in summary:
            return "Active"
        if "outperform" in summary or "manager selects" in summary:
            return "Active"
        return ""
    except Exception:
        return ""

def extract_scorecard_blocks(pdf, scorecard_page):
    metric_labels = [
        "Manager Tenure", "Excess Performance (3Yr)", "Excess Performance (5Yr)",
        "Peer Return Rank (3Yr)", "Peer Return Rank (5Yr)", "Expense Ratio Rank",
        "Sharpe Ratio Rank (3Yr)", "Sharpe Ratio Rank (5Yr)", "R-Squared (3Yr)",
        "R-Squared (5Yr)", "Sortino Ratio Rank (3Yr)", "Sortino Ratio Rank (5Yr)",
        "Tracking Error Rank (3Yr)", "Tracking Error Rank (5Yr)"
    ]
    pages, fund_blocks, fund_name, metrics = [], [], None, []
    for p in pdf.pages[scorecard_page-1:]:
        pages.append(p.extract_text() or "")
    lines = "\n".join(pages).splitlines()
    for line in lines:
        if not any(metric in line for metric in metric_labels) and line.strip():
            if fund_name and metrics:
                fund_blocks.append({"Fund Name": fund_name, "Metrics": metrics})
            fund_name = re.sub(
                r"Fund (Meets Watchlist Criteria|has been placed on watchlist for not meeting .* out of 14 criteria)",
                "",
                line.strip()
            ).strip()
            metrics = []
        for metric in metric_labels:
            if metric in line:
                m = re.match(r"^(.*?)\s+(Pass|Review|Fail)\s*(.*)", line.strip())
                if m:
                    metric_name, status, info = m.groups()
                    metrics.append({"Metric": metric_name, "Status": status, "Info": info.strip()})
    if fund_name and metrics:
        fund_blocks.append({"Fund Name": fund_name, "Metrics": metrics})
    return fund_blocks

def extract_fund_tickers(pdf, performance_page, fund_names, factsheets_page=None):
    def normalize_name(name):
        cleaned = re.sub(
            r"has been placed on watchlist for not meeting .*? criteria",
            "",
            name,
            flags=re.IGNORECASE
        )
        cleaned = re.sub(r"[^A-Za-z0-9 ]+", "", cleaned)
        return cleaned.strip().lower()

    end_page = factsheets_page - 1 if factsheets_page else len(pdf.pages)
    all_lines = []
    for p in pdf.pages[performance_page - 1:end_page]:
        txt = p.extract_text() or ""
        all_lines.extend([ln.strip() for ln in txt.splitlines() if ln.strip()])

    candidate_pairs = []
    ticker_rx = re.compile(r"\b([A-Z]{2,5})\b")
    for ln in all_lines:
        matches = ticker_rx.findall(ln)
        if not matches:
            continue
        for ticker in set(matches):
            parts = ln.rsplit(ticker, 1)
            if len(parts) >= 1:
                raw_name = parts[0].strip()
                if not raw_name:
                    continue
                norm_raw = normalize_name(raw_name)
                if not norm_raw:
                    continue
                candidate_pairs.append((norm_raw, ticker, raw_name))

    assigned = {}
    used_tickers = set()
    norm_expected_list = [(name, normalize_name(name)) for name in fund_names]

    for fund_name, norm_expected in norm_expected_list:
        best = (None, None, 0)
        for norm_raw, ticker, raw_name in candidate_pairs:
            if ticker in used_tickers:
                continue
            score = fuzz.token_sort_ratio(norm_expected, norm_raw)
            if score > best[2]:
                best = (ticker, raw_name, score)
        if best[2] >= 70:
            assigned[fund_name] = best[0]
            used_tickers.add(best[0])
        else:
            assigned[fund_name] = ""

    for name in fund_names:
        if assigned.get(name):
            continue
        norm_expected = normalize_name(name)
        for norm_raw, ticker, raw_name in candidate_pairs:
            if ticker in used_tickers:
                continue
            if norm_expected in norm_raw or norm_raw in norm_expected:
                assigned[name] = ticker
                used_tickers.add(ticker)
                break
        if not assigned.get(name):
            for ln in all_lines:
                if name.lower() in ln.lower():
                    m = re.search(r"\b([A-Z]{2,5})\b", ln)
                    if m:
                        assigned[name] = m.group(1)
                        break

    return {k: (v if v else "") for k, v in assigned.items()}

def scorecard_to_ips(fund_blocks, fund_types, tickers):
    metrics_order = [
        "Manager Tenure", "Excess Performance (3Yr)", "Excess Performance (5Yr)",
        "Peer Return Rank (3Yr)", "Peer Return Rank (5Yr)", "Expense Ratio Rank",
        "Sharpe Ratio Rank (3Yr)", "Sharpe Ratio Rank (5Yr)", "R-Squared (3Yr)",
        "R-Squared (5Yr)", "Sortino Ratio Rank (3Yr)", "Sortino Ratio Rank (5Yr)",
        "Tracking Error Rank (3Yr)", "Tracking Error Rank (5Yr)",
    ]
    active_map  = [0,1,3,6,10,2,4,7,11,5,None]
    passive_map = [0,8,3,6,12,9,4,7,13,5,None]
    ips_labels = [f"IPS Investment Criteria {i+1}" for i in range(11)]
    ips_results, raw_results = [], []
    for fund in fund_blocks:
        fund_name = fund["Fund Name"]
        fund_type = fund_types.get(fund_name, "Passive" if "index" in fund_name.lower() else "Active")
        metrics = fund["Metrics"]
        scorecard_status = [next((m["Status"] for m in metrics if m["Metric"] == label), None) for label in metrics_order]
        idx_map = passive_map if fund_type == "Passive" else active_map
        ips_status = [scorecard_status[m_idx] if m_idx is not None else "Pass" for m_idx in idx_map]
        review_fail = sum(1 for status in ips_status if status in ["Review","Fail"])
        watch_status = "FW" if review_fail >= 6 else "IW" if review_fail >= 5 else "NW"
        def iconify(status): return "✔" if status == "Pass" else "✗" if status in ("Review", "Fail") else ""
        row = {
            "Fund Name": fund_name,
            "Ticker": tickers.get(fund_name, ""),
            "Fund Type": fund_type,
            **{ips_labels[i]: iconify(ips_status[i]) for i in range(11)},
            "IPS Watch Status": watch_status,
        }
        ips_results.append(row)
        raw_results.append({
            "Fund Name": fund_name,
            "Ticker": tickers.get(fund_name, ""),
            "Fund Type": fund_type,
            **{ips_labels[i]: ips_status[i] for i in range(11)},
            "IPS Watch Status": watch_status,
        })
    return pd.DataFrame(ips_results), pd.DataFrame(raw_results)

def watch_status_color(val):
    if val == "FW":
        return "background-color:#f8d7da; color:#c30000; font-weight:600;"
    if val == "IW":
        return "background-color:#fff3cd; color:#B87333; font-weight:600;"
    if val == "NW":
        return "background-color:#d6f5df; color:#217a3e; font-weight:600;"
    return ""

def step3_5_6_scorecard_and_ips(pdf, scorecard_page, performance_page, factsheets_page, total_options):
    # --- 1. Extract scorecard blocks ---
    fund_blocks = extract_scorecard_blocks(pdf, scorecard_page)
    fund_names = [fund["Fund Name"] for fund in fund_blocks]
    if not fund_blocks:
        st.error("Could not extract fund scorecard blocks. Check the PDF and page number.")
        return

    # --- 2. Extract tickers ---
    tickers = extract_fund_tickers(pdf, performance_page, fund_names, factsheets_page)

    # --- Prepare inferred fund type guesses/defaults ---
    inferred_guesses = []
    for name in fund_names:
        guess = ""
        if tickers.get(name):
            guess = infer_fund_type_guess(tickers.get(name, "")) or ""
        inferred_guesses.append("Passive" if guess.lower() == "passive" else ("Passive" if "index" in name.lower() else "Active"))

    df_types_base = pd.DataFrame({
        "Fund Name":       fund_names,
        "Ticker":          [tickers.get(n, "") for n in fund_names],
        "Inferred Type":   inferred_guesses,
        "Fund Type":       inferred_guesses,
    })

    if "show_edit_fund_type" not in st.session_state:
        st.session_state["show_edit_fund_type"] = False
    toggle_label = "Hide Fund Type Editor" if st.session_state["show_edit_fund_type"] else "Edit Fund Type"
    if st.button(toggle_label, key="toggle_edit_fund_type"):
        st.session_state["show_edit_fund_type"] = not st.session_state["show_edit_fund_type"]

    if st.session_state["show_edit_fund_type"]:
        st.markdown("### Fund Type Overrides")
        st.caption("Edit any fund type here; once you modify at least one, your edits take precedence over inferred types.")
        edited_types = st.data_editor(
            df_types_base,
            column_config={
                "Fund Type": st.column_config.SelectboxColumn("Fund Type", options=["Active", "Passive"]),
            },
            disabled=["Fund Name", "Ticker", "Inferred Type"],
            hide_index=True,
            key="data_editor_fundtype_ips",
            use_container_width=True,
        )
        manual_override = any(
            row["Fund Type"] != row["Inferred Type"]
            for _, row in edited_types.iterrows()
        )
        if manual_override:
            fund_types = {row["Fund Name"]: row["Fund Type"] for _, row in edited_types.iterrows()}
        else:
            fund_types = {row["Fund Name"]: row["Inferred Type"] for _, row in edited_types.iterrows()}
    else:
        fund_types = {name: inferred_guesses[i] for i, name in enumerate(fund_names)}

    # --- 4. IPS conversion ---
    df_icon, df_raw = scorecard_to_ips(fund_blocks, fund_types, tickers)

    # --- IPS Results ---
    section_label("IPS Screening Results")
    st.markdown(
        '<div style="display:flex; gap:1rem; margin-bottom:0.5rem;">'
        '<div style="padding:4px 10px; background:#d6f5df; border-radius:4px; font-weight:600;">NW: No Watch</div>'
        '<div style="padding:4px 10px; background:#fff3cd; border-radius:4px; font-weight:600;">IW: Informal Watch</div>'
        '<div style="padding:4px 10px; background:#f8d7da; border-radius:4px; font-weight:600;">FW: Formal Watch</div>'
        '</div>', unsafe_allow_html=True
    )

    if df_icon.empty:
        st.info("No IPS screening data available.")
    else:
        display_columns = {f"IPS Investment Criteria {i+1}": str(i+1) for i in range(11)}
        display_df = df_icon.rename(columns=display_columns)

        def iconify(s):
            if s == "Pass":
                return "✔"
            if s in ("Review", "Fail"):
                return "✗"
            return ""

        compact_df = display_df.copy()
        for i in range(1, 12):
            orig = f"IPS Investment Criteria {i}"
            if orig in compact_df.columns:
                compact_df[str(i)] = compact_df[orig].apply(iconify)
                compact_df.drop(columns=[orig], inplace=True)
        cols_order = ["Fund Name", "Ticker", "Fund Type"] + [str(i) for i in range(1, 12)] + ["IPS Watch Status"]
        compact_df = compact_df[[c for c in cols_order if c in compact_df.columns]]

        def watch_style(val):
            if val == "NW":
                return "background-color:#d6f5df; color:#217a3e; font-weight:600;"
            if val == "IW":
                return "background-color:#fff3cd; color:#B87333; font-weight:600;"
            if val == "FW":
                return "background-color:#f8d7da; color:#c30000; font-weight:600;"
            return ""

        styled = compact_df.style.applymap(watch_style, subset=["IPS Watch Status"])
        st.dataframe(styled, use_container_width=True, hide_index=True)

    # --- Persist state downstream ---
    st.session_state["fund_blocks"] = fund_blocks
    st.session_state["fund_types"] = fund_types
    st.session_state["fund_tickers"] = tickers
    st.session_state["ips_icon_table"] = df_icon
    st.session_state["ips_raw_table"] = df_raw

    perf_data = extract_performance_table(pdf, performance_page, fund_names, factsheets_page)
    for itm in perf_data:
        itm["Ticker"] = tickers.get(itm["Fund Scorecard Name"], "")
    st.session_state["fund_performance_data"] = perf_data
    st.session_state["tickers"] = tickers

# ─── Side-by-side Info Card Functions ──────────────────────────────────────────

def get_ips_fail_card_html():
    df = st.session_state.get("ips_icon_table")
    if df is None or df.empty:
        return "", ""
    fail_df = df[df["IPS Watch Status"].isin(["FW", "IW"])][["Fund Name", "IPS Watch Status"]]
    if fail_df.empty:
        return "", ""
    table_html = fail_df.rename(columns={
        "Fund Name": "Fund",
        "IPS Watch Status": "Watch Status"
    }).to_html(index=False, border=0, justify="center", classes="ips-fail-table")
    card_html = f"""
    <div style='
        background: linear-gradient(120deg, #e6f0fb 85%, #c8e0f6 100%);
        color: #23395d;
        border-radius: 1.3rem;
        box-shadow: 0 2px 14px rgba(44,85,130,0.08), 0 1px 4px rgba(36,67,105,0.07);
        padding: 1.6rem 2.0rem 1.6rem 2.0rem;
        border: 1.5px solid #b5d0eb;
        font-size:1rem;
        max-width:100%;
        margin-bottom:1.2rem;
    '>
        <div style='font-weight:700; color:#23395d; font-size:1.15rem; margin-bottom:0.5rem; letter-spacing:-0.5px;'>
            Funds on Watch
        </div>
        <div style='font-size:1rem; margin-bottom:1rem; color:#23395d;'>
            The following funds failed five or more IPS criteria and are currently on watch.
        </div>
        {table_html}
    </div>
    """
    css = """
    <style>
    .ips-fail-table {
        width: 100%;
        border-collapse: collapse;
        margin-top: 0.7em;
        font-family: 'Inter', 'Segoe UI', Arial, sans-serif;
    }
    .ips-fail-table th, .ips-fail-table td {
        border: none;
        padding: 0.48em 1.1em;
        text-align: left;
        font-size: 1.07em;
    }
    .ips-fail-table th {
        background: #244369;
        color: #fff;
        font-weight: 700;
        letter-spacing: 0.01em;
    }
    .ips-fail-table td {
        color: #244369;
    }
    .ips-fail-table tr:nth-child(even) {background: #e6f0fb;}
    .ips-fail-table tr:nth-child(odd)  {background: #f8fafc;}
    </style>
    """
    return card_html, css

def get_proposed_fund_card_html():
    df = st.session_state.get("proposed_funds_confirmed_df")
    if df is None or df.empty:
        card_html = """
        <div style='
            background: linear-gradient(120deg, #e6f0fb 85%, #c8e0f6 100%);
            color: #23395d;
            border-radius: 1.3rem;
            box-shadow: 0 2px 14px rgba(44,85,130,0.08), 0 1px 4px rgba(36,67,105,0.07);
            padding: 1.6rem 2.0rem;
            border: 1.5px solid #b5d0eb;
            font-size:1rem;
            max-width:100%;
            margin-bottom:1.2rem;
        '>
            <div style='font-weight:700; color:#23395d; font-size:1.15rem; margin-bottom:0.5rem; letter-spacing:-0.5px;'>
                Confirmed Proposed Funds
            </div>
            <div style='font-size:1rem; margin-bottom:1rem; color:#23395d;'>
                No confirmed proposed funds were found on the Proposed Funds scorecard page.
            </div>
        </div>
        """
        css = ""
        return card_html, css

    display_df = df[["Fund Scorecard Name", "Ticker"]].rename(columns={
        "Fund Scorecard Name": "Fund",
    })
    table_html = display_df.to_html(index=False, border=0, justify="center", classes="proposed-fund-table")
    card_html = f"""
    <div style='
        background: linear-gradient(120deg, #e6f0fb 85%, #c8e0f6 100%);
        color: #23395d;
        border-radius: 1.3rem;
        box-shadow: 0 2px 14px rgba(44,85,130,0.08), 0 1px 4px rgba(36,67,105,0.07);
        padding: 1.6rem 2.0rem;
        border: 1.5px solid #b5d0eb;
        font-size:1rem;
        max-width:100%;
        margin-bottom:1.2rem;
    '>
        <div style='font-weight:700; color:#23395d; font-size:1.15rem; margin-bottom:0.5rem; letter-spacing:-0.5px;'>
            Confirmed Proposed Funds
        </div>
        <div style='font-size:1rem; margin-bottom:1rem; color:#23395d;'>
            The following funds were identified on the Proposed Funds scorecard page.
        </div>
        {table_html}
    </div>
    """
    css = """
    <style>
    .proposed-fund-table {
        width: 100%;
        border-collapse: collapse;
        margin-top: 0.7em;
        font-family: 'Inter', 'Segoe UI', Arial, sans-serif;
    }
    .proposed-fund-table th, .proposed-fund-table td {
        border: none;
        padding: 0.48em 1.1em;
        text-align: left;
        font-size: 1em;
    }
    .proposed-fund-table th {
        background: #244369;
        color: #fff;
        font-weight: 700;
        letter-spacing: 0.01em;
    }
    .proposed-fund-table td {
        color: #23395d;
    }
    .proposed-fund-table tr:nth-child(even) {background: #e6f0fb;}
    .proposed-fund-table tr:nth-child(odd)  {background: #f8fafc;}
    </style>
    """
    return card_html, css

def get_watch_summary_card_html():
    df = st.session_state.get("ips_icon_table")
    if df is None or df.empty:
        return "", ""
    counts = df["IPS Watch Status"].value_counts().to_dict()
    summary = {
        "No Watch": counts.get("NW", 0),
        "Informal Watch": counts.get("IW", 0),
        "Formal Watch": counts.get("FW", 0),
    }
    card_html = f"""
    <div style="
        background: linear-gradient(120deg, #e6f0fb 82%, #d0ebfa 100%);
        color: #244369;
        border-radius: 1.2rem;
        box-shadow: 0 2px 14px rgba(44,85,130,0.08), 0 1px 4px rgba(36,67,105,0.07);
        padding: 1.3rem 2rem 1.1rem 2rem;
        margin-bottom: 2rem;
        font-size: 1.07rem;
        border: 1.2px solid #b5d0eb;
        max-width: 520px;
    ">
      <div style="font-size:1.13rem; font-weight:700; color:#223d63; margin-bottom:0.7rem;">
        Watch Summary
      </div>
      <div style="display:flex; gap:1.5rem; align-items:center; justify-content: flex-start; margin-bottom:0.3rem;">
        <div style="background:#d6f5df; color:#217a3e; border-radius:0.55rem; padding:0.5rem 1.2rem; font-size:1.1rem; font-weight:600; min-width:105px; text-align:center;">
            No Watch<br><span style="font-size:1.4rem; font-weight:700;">{summary["No Watch"]}</span>
        </div>
        <div style="background:#fff3cd; color:#B87333; border-radius:0.55rem; padding:0.5rem 1.2rem; font-size:1.1rem; font-weight:600; min-width:105px; text-align:center;">
            Informal Watch<br><span style="font-size:1.4rem; font-weight:700;">{summary["Informal Watch"]}</span>
        </div>
        <div style="background:#f8d7da; color:#c30000; border-radius:0.55rem; padding:0.5rem 1.2rem; font-size:1.1rem; font-weight:600; min-width:105px; text-align:center;">
            Formal Watch<br><span style="font-size:1.4rem; font-weight:700;">{summary["Formal Watch"]}</span>
        </div>
      </div>
    </div>
    """
    css = ""
    return card_html, css

# ─── Proposed Funds Extraction ─────────────────────────────────────────────

def extract_proposed_scorecard_blocks(pdf):
    prop_page = st.session_state.get("scorecard_proposed_page")
    if not prop_page:
        st.session_state["proposed_funds_confirmed_df"] = pd.DataFrame()
        return pd.DataFrame()
    page = pdf.pages[prop_page - 1]
    lines = [ln.strip() for ln in (page.extract_text() or "").splitlines() if ln.strip()]
    if not lines:
        st.session_state["proposed_funds_confirmed_df"] = pd.DataFrame()
        return pd.DataFrame()
    perf_data = st.session_state.get("fund_performance_data", [])
    if not perf_data:
        st.session_state["proposed_funds_confirmed_df"] = pd.DataFrame()
        return pd.DataFrame()
    candidate_funds = []
    for item in perf_data:
        name = item.get("Fund Scorecard Name", "").strip()
        ticker = item.get("Ticker", "").strip().upper()
        if name:
            candidate_funds.append({"Fund Scorecard Name": name, "Ticker": ticker})
    results = []
    for fund in candidate_funds:
        name = fund["Fund Scorecard Name"]
        ticker = fund["Ticker"]
        best_score = 0
        best_line = ""
        for line in lines:
            score_name = fuzz.token_sort_ratio(name.lower(), line.lower())
            score_ticker = fuzz.token_sort_ratio(ticker.lower(), line.lower()) if ticker else 0
            score = max(score_name, score_ticker)
            if score > best_score:
                best_score = score
                best_line = line
        found = best_score >= 70
        results.append({
            "Fund Scorecard Name": name,
            "Ticker": ticker,
            "Found on Proposed": "✅" if found else "❌",
            "Match Score": best_score,
            "Matched Line": best_line if found else ""
        })
    df = pd.DataFrame(results)
    df_confirmed = df[df["Found on Proposed"] == "✅"].copy()
    st.session_state["proposed_funds_confirmed_df"] = df_confirmed
    return df_confirmed



def apply_page_style():
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


def section_label(text):
    st.markdown(
        f'<div class="section-label">{text}</div>',
        unsafe_allow_html=True,
    )


# ─── Main App ───────────────────────────────────────────────────────────────

def run():
    apply_page_style()

    st.title("IPS Investment Screening")
    st.markdown(
        """
        <div class="app-subtitle">
            Upload an MPI-style PDF fund scorecard. The app will evaluate each
            fund against the IPS Investment Criteria, confirm fund classifications,
            and organize the screening results for review.
        </div>
        """,
        unsafe_allow_html=True,
    )

    pdf_file = st.file_uploader(
        "Upload MPI PDF",
        type=["pdf"],
        help="Upload a text-based MPI fund scorecard PDF.",
        key="ips_screening_pdf_uploader",
    )
    if not uploaded:
        st.info("Upload an MPI fund scorecard PDF to begin.")
        return

    with pdfplumber.open(uploaded) as pdf:
        # Step 1
        first = pdf.pages[0].extract_text() or ""
        process_page1(first)

        section_label("Report Overview")
        show_report_summary()

        # Step 2
        with st.expander("Table of Contents", expanded=False):
            toc_text = "".join((pdf.pages[i].extract_text() or "") for i in range(min(3, len(pdf.pages))))
            process_toc(toc_text)

        # IPS Screening
        sp = st.session_state.get('scorecard_page')
        tot = st.session_state.get('total_options')
        pp = st.session_state.get('performance_page')
        factsheets_page = st.session_state.get('factsheets_page')
        if sp and tot is not None and pp:
            step3_5_6_scorecard_and_ips(pdf, sp, pp, factsheets_page, tot)
        else:
            st.error("Missing scorecard, performance page, or total options")

        # Proposed & Fail cards
        extract_proposed_scorecard_blocks(pdf)
        fail_card_html, fail_css = get_ips_fail_card_html()
        proposed_card_html, proposed_css = get_proposed_fund_card_html()
        watch_summary_card_html, watch_summary_css = get_watch_summary_card_html()

        col1, col2 = st.columns(2, gap="large")
        with col1:
            if proposed_card_html:
                st.markdown(proposed_card_html, unsafe_allow_html=True)
            if watch_summary_card_html:
                st.markdown(watch_summary_card_html, unsafe_allow_html=True)
        with col2:
            if fail_card_html:
                st.markdown(fail_card_html, unsafe_allow_html=True)

        # CSS injection once
        st.markdown(f"{fail_css}\n{proposed_css}\n{watch_summary_css}", unsafe_allow_html=True)

if __name__ == "__main__":
    run()
