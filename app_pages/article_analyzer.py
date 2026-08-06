# app_pages/article_analyzer.py

import os
import random
import re

import streamlit as st


# =========================================================
# Constants
# =========================================================

SUMMARY_CHARACTER_LIMIT = 1000

INPUT_METHODS = [
    "Paste URL",
    "Paste Text",
    "Upload PDF",
]


ANALYSIS_LOADING_MESSAGES = [
    "Retrieving and processing the article...",
    "Retrieving and processing the article...",
    "Separating the article from the advertisements...",
    "Looking for the important paragraph...",
    "Counting words so you do not have to...",
    "Removing suspicious amounts of whitespace...",
    "Consulting the editorial department...",
    "Trying to find the point of the article...",
]


PDF_LOADING_MESSAGES = [
    "Extracting text from the PDF...",
    "Extracting text from the PDF...",
    "Reading the fine print...",
    "Checking every page for actual text...",
    "Attempting diplomatic relations with the PDF...",
    "Looking for selectable text...",
]


SOLITAIRE_URL = "https://play-solitaire.com/"

HIDDEN_COMMAND_ALIASES = {
    "SOLITARE": "SOLITAIRE",
}

HIDDEN_ARTICLE_COMMANDS = {
    "SOLITAIRE": {
        "title": "Screen-Time Analysis Complete",
        "authors": "FidSync Wellness Department",
        "publish_date": "Immediately",
        "source": "Definitely Serious Research",
        "text": (
            "Analysis indicates that you have been staring at financial data "
            "for too long. FidSync recommends stepping away from the screen, "
            "stretching, drinking some water, and touching some grass. "
            "Alternatively, management has approved one game of Solitaire."
        ),
        "message": "Productivity has been temporarily suspended.",
    },
}


# =========================================================
# Article processing
# =========================================================

@st.cache_data(show_spinner=False)
def clean_article_text(text):
    """
    Normalize extracted article text by removing repeated spaces
    and excessive blank lines.
    """

    if not text:
        return ""

    text = text.replace("\x00", "")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n\s*\n\s*\n+", "\n\n", text)

    return text.strip()


@st.cache_data(show_spinner=False)
def summarize_article(text):
    """
    Create a basic extractive preview by limiting the article text
    to the configured number of characters.
    """

    cleaned_text = clean_article_text(text)

    if len(cleaned_text) > SUMMARY_CHARACTER_LIMIT:
        return (
            cleaned_text[:SUMMARY_CHARACTER_LIMIT].rstrip()
            + "..."
        )

    return cleaned_text


@st.cache_data(show_spinner=False)
def get_text_statistics(text):
    """Calculate basic statistics for the extracted article."""

    cleaned_text = clean_article_text(text)

    words = re.findall(r"\b[\w'-]+\b", cleaned_text)
    sentences = re.split(r"(?<=[.!?])\s+", cleaned_text)

    sentence_count = len(
        [
            sentence
            for sentence in sentences
            if sentence.strip()
        ]
    )

    word_count = len(words)
    character_count = len(cleaned_text)

    estimated_reading_time = (
        max(1, round(word_count / 225))
        if word_count
        else 0
    )

    return {
        "Words": word_count,
        "Characters": character_count,
        "Sentences": sentence_count,
        "Reading Time": f"{estimated_reading_time} min",
    }


def clean_author_metadata(authors):
    """
    Remove obvious date, time, and reading-length fragments that may
    be incorrectly detected as author names.
    """

    if not authors or authors == "Not detected":
        return "Not detected"

    invalid_terms = {
        "mon",
        "monday",
        "tue",
        "tues",
        "tuesday",
        "wed",
        "wednesday",
        "thu",
        "thurs",
        "thursday",
        "fri",
        "friday",
        "sat",
        "saturday",
        "sun",
        "sunday",
        "january",
        "february",
        "march",
        "april",
        "may",
        "june",
        "july",
        "august",
        "september",
        "october",
        "november",
        "december",
        "am",
        "pm",
        "pdt",
        "pst",
        "est",
        "edt",
        "cst",
        "cdt",
        "min read",
        "minute read",
    }

    author_parts = [
        part.strip()
        for part in authors.split(",")
        if part.strip()
    ]

    cleaned_parts = []

    for part in author_parts:
        normalized = part.lower().strip()

        if normalized in invalid_terms:
            continue

        if re.fullmatch(
            r"\d+\s*min(?:ute)?s?\s*read",
            normalized,
        ):
            continue

        if re.fullmatch(
            r"\d{1,2}:\d{2}\s*(am|pm)?",
            normalized,
        ):
            continue

        cleaned_parts.append(part)

    if not cleaned_parts:
        return "Not detected"

    return ", ".join(cleaned_parts)


@st.cache_data(show_spinner=False, ttl=1800)
def extract_article_from_url(url):
    """Download and extract article text from a webpage."""

    from newspaper import Article

    article = Article(url)
    article.download()
    article.parse()

    raw_authors = (
        ", ".join(article.authors)
        if article.authors
        else "Not detected"
    )

    return {
        "text": clean_article_text(article.text),
        "title": article.title or "Untitled Article",
        "authors": clean_author_metadata(raw_authors),
        "publish_date": (
            article.publish_date.strftime("%B %d, %Y")
            if article.publish_date
            else "Not detected"
        ),
        "source": url,
    }


@st.cache_data(show_spinner=False)
def extract_text_from_pdf(pdf_bytes):
    """Extract readable text from every page of an uploaded PDF."""

    from io import BytesIO
    import pdfplumber

    extracted_pages = []

    with pdfplumber.open(BytesIO(pdf_bytes)) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()

            if page_text:
                extracted_pages.append(page_text)

    return clean_article_text(
        "\n\n".join(extracted_pages)
    )


def detect_hidden_article_command(
    input_mode,
    article_input,
):
    """Detect an exact hidden command entered through pasted text."""

    if input_mode != "Paste Text":
        return None

    command = clean_article_text(
        article_input or ""
    ).upper()

    # Correct supported misspellings or aliases.
    command = HIDDEN_COMMAND_ALIASES.get(
        command,
        command,
    )

    if command in HIDDEN_ARTICLE_COMMANDS:
        return command

    return None


def load_hidden_article(command):
    """Load a fictional hidden article into session state."""

    hidden_article = HIDDEN_ARTICLE_COMMANDS[command]

    st.session_state.article_title = (
        hidden_article["title"]
    )

    st.session_state.article_authors = (
        hidden_article["authors"]
    )

    st.session_state.article_publish_date = (
        hidden_article["publish_date"]
    )

    st.session_state.article_source = (
        hidden_article["source"]
    )

    st.session_state.article_text = (
        hidden_article["text"]
    )

    st.session_state.article_summary = summarize_article(
        hidden_article["text"]
    )

    st.session_state.article_analyzed = True
    st.session_state.article_hidden_command = command

    if (
        st.session_state.article_last_hidden_animation
        != command
    ):
        st.balloons()
        st.toast(hidden_article["message"])

        st.session_state.article_last_hidden_animation = (
            command
        )


# =========================================================
# PDF export
# =========================================================

def prepare_text_for_pdf(text):
    """
    Replace unsupported characters so standard FPDF fonts do not
    fail when generating the PDF.
    """

    replacements = {
        "\u2018": "'",
        "\u2019": "'",
        "\u201c": '"',
        "\u201d": '"',
        "\u2013": "-",
        "\u2014": "-",
        "\u2026": "...",
        "\u00a0": " ",
        "\u2022": "-",
    }

    for original, replacement in replacements.items():
        text = text.replace(
            original,
            replacement,
        )

    return (
        text.encode(
            "latin-1",
            errors="replace",
        )
        .decode("latin-1")
    )


@st.cache_data(show_spinner=False)
def export_summary_to_pdf(
    summary,
    title="Article Summary",
):
    """Create and cache PDF bytes containing the article summary."""

    from fpdf import FPDF

    safe_title = prepare_text_for_pdf(title)
    safe_summary = prepare_text_for_pdf(summary)

    pdf = FPDF()
    pdf.add_page()

    pdf.set_auto_page_break(
        auto=True,
        margin=15,
    )

    pdf.set_title(safe_title)
    pdf.set_author("FidSync")

    pdf.set_font(
        "Arial",
        style="B",
        size=16,
    )

    pdf.multi_cell(
        0,
        10,
        txt=safe_title,
        align="L",
    )

    pdf.ln(2)

    pdf.set_draw_color(
        43,
        108,
        176,
    )

    pdf.set_line_width(0.7)

    pdf.line(
        pdf.get_x(),
        pdf.get_y(),
        195,
        pdf.get_y(),
    )

    pdf.ln(7)

    pdf.set_font(
        "Arial",
        size=11,
    )

    pdf.multi_cell(
        0,
        7,
        txt=safe_summary,
        align="L",
    )

    pdf.ln(7)

    pdf.set_font(
        "Arial",
        style="I",
        size=8,
    )

    pdf.set_text_color(
        95,
        110,
        125,
    )

    pdf.multi_cell(
        0,
        5,
        txt=(
            "Generated by FidSync. Verify important information "
            "against the original source."
        ),
    )

    pdf_output = pdf.output(dest="S")

    if isinstance(pdf_output, str):
        return pdf_output.encode("latin-1")

    return bytes(pdf_output)


# =========================================================
# Session state
# =========================================================

def initialize_session_state():
    """Create persistent state values used by the analyzer."""

    default_values = {
        "article_text": "",
        "article_title": "",
        "article_authors": "",
        "article_publish_date": "",
        "article_source": "",
        "article_summary": "",
        "article_analyzed": False,
        "article_error": "",
        "article_hidden_command": "",
        "article_last_hidden_animation": "",
    }

    for key, value in default_values.items():
        if key not in st.session_state:
            st.session_state[key] = value


def clear_analysis():
    """
    Clear the current article and results.

    Achievement progress remains available for the session.
    """

    st.session_state.article_text = ""
    st.session_state.article_title = ""
    st.session_state.article_authors = ""
    st.session_state.article_publish_date = ""
    st.session_state.article_source = ""
    st.session_state.article_summary = ""
    st.session_state.article_analyzed = False
    st.session_state.article_error = ""
    st.session_state.article_hidden_command = ""
    st.session_state.article_last_hidden_animation = ""


# =========================================================
# Styling
# =========================================================

def apply_page_styles():
    st.markdown(
        """
        <style>
            .block-container {
                max-width: 1150px;
                padding-top: 2rem;
                padding-bottom: 3rem;
            }

            .analyzer-header {
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
                box-shadow:
                    0 8px 24px
                    rgba(16, 37, 66, 0.12);
            }

            .analyzer-header-label {
                margin-bottom: 0.55rem;
                color: #b9cde5;
                font-size: 0.72rem;
                font-weight: 700;
                letter-spacing: 0.1rem;
                text-transform: uppercase;
            }

            .analyzer-header h1 {
                margin: 0;
                color: white;
                font-size: 2.2rem;
                font-weight: 750;
                line-height: 1.2;
                letter-spacing: -0.05rem;
            }

            .analyzer-header p {
                max-width: 780px;
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

            .input-instructions {
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

            [data-testid="stMetric"] {
                min-height: 105px;
                padding: 0.95rem 1rem;
                background-color: white;
                border: 1px solid #dce3ec;
                border-radius: 0.75rem;
                box-shadow:
                    0 2px 8px
                    rgba(16, 37, 66, 0.04);
            }

            [data-testid="stMetricLabel"] {
                color: #64748b;
                font-size: 0.78rem;
                font-weight: 600;
            }

            [data-testid="stMetricValue"] {
                color: #102542;
                font-size: 1.45rem;
                font-weight: 750;
            }

            [data-testid="stWidgetLabel"] p {
                color: #102542;
                font-weight: 650;
            }

            [data-baseweb="input"] > div,
            [data-baseweb="textarea"] > div,
            [data-baseweb="select"] > div {
                border-color: #ccd8e6;
                border-radius: 0.55rem;
            }

            [data-baseweb="input"] > div:focus-within,
            [data-baseweb="textarea"] > div:focus-within,
            [data-baseweb="select"] > div:focus-within {
                border-color: #2b6cb0;
                box-shadow:
                    0 0 0 1px #2b6cb0;
            }

            .stButton > button {
                min-height: 2.65rem;
                border-radius: 0.55rem;
                font-weight: 650;
            }

            div[data-testid="stButton"]
            button[kind="primary"] {
                background-color: #2b6cb0;
                border-color: #2b6cb0;
                color: white;
            }

            div[data-testid="stButton"]
            button[kind="primary"]:hover {
                background-color: #1f568f;
                border-color: #1f568f;
                color: white;
            }

            .summary-card-label {
                margin-bottom: 0.5rem;
                color: #2b6cb0;
                font-size: 0.7rem;
                font-weight: 750;
                letter-spacing: 0.06rem;
                text-transform: uppercase;
            }

            [data-testid="stDownloadButton"] > button {
                min-height: 2.65rem;
                background-color: #2b6cb0;
                color: white;
                border: 1px solid #2b6cb0;
                border-radius: 0.55rem;
                font-weight: 700;
            }

            [data-testid="stDownloadButton"]
            > button:hover {
                background-color: #1f568f;
                border-color: #1f568f;
                color: white;
            }

            .analyzer-disclaimer {
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
                .analyzer-header {
                    padding: 1.7rem;
                }
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


# =========================================================
# Input interface
# =========================================================

def render_input_section():
    st.markdown(
        """
        <div class="section-heading">Add an article</div>
        <div class="section-description">
            Select an input method and provide the article you want to analyze.
        </div>
        """,
        unsafe_allow_html=True,
    )

    input_mode = st.selectbox(
        "Article input method",
        options=INPUT_METHODS,
        help=(
            "Use a URL for an online article, paste text directly, "
            "or upload a text-based PDF."
        ),
    )

    article_input = None

    if input_mode == "Paste URL":
        st.markdown(
            """
            <div class="input-instructions">
                Enter the direct URL of a publicly accessible article.
                Some websites may block automated article extraction or
                require a subscription.
            </div>
            """,
            unsafe_allow_html=True,
        )

        article_input = st.text_input(
            "Article URL",
            placeholder="https://example.com/article",
        )

    elif input_mode == "Paste Text":
        st.markdown(
            """
            <div class="input-instructions">
                Paste the full article text below. Headings and paragraph
                breaks may improve readability in the extracted result.
            </div>
            """,
            unsafe_allow_html=True,
        )

        article_input = st.text_area(
            "Full article text",
            height=320,
            placeholder="Paste the article here...",
        )

    elif input_mode == "Upload PDF":
        st.markdown(
            """
            <div class="input-instructions">
                Upload a PDF containing selectable text. Image-only or scanned
                PDFs may not return readable content without OCR.
            </div>
            """,
            unsafe_allow_html=True,
        )

        article_input = st.file_uploader(
            "Upload article PDF",
            type=["pdf"],
            help="Only PDF files are accepted.",
        )

        if article_input:
            file_size_mb = (
                article_input.size
                / (1024 * 1024)
            )

            st.caption(
                f"Selected file: {article_input.name} "
                f"({file_size_mb:.2f} MB)"
            )

    action_col1, action_col2 = st.columns(
        [3, 1]
    )

    with action_col1:
        analyze_clicked = st.button(
            "Analyze Article",
            type="primary",
            use_container_width=True,
        )

    with action_col2:
        clear_clicked = st.button(
            "Clear",
            use_container_width=True,
        )

    if clear_clicked:
        clear_analysis()
        st.rerun()

    if analyze_clicked:
        process_article_input(
            input_mode=input_mode,
            article_input=article_input,
        )


def process_article_input(
    input_mode,
    article_input,
):
    """Validate and process the selected article input."""

    clear_analysis()

    hidden_command = detect_hidden_article_command(
        input_mode,
        article_input,
    )

    if hidden_command:
        load_hidden_article(hidden_command)

        return

    if input_mode == "Paste URL":
        url = (
            article_input or ""
        ).strip()

        if not url:
            st.error(
                "Enter an article URL before analyzing."
            )
            return

        if not re.match(
            r"^https?://",
            url,
            flags=re.IGNORECASE,
        ):
            st.error(
                "Enter a complete URL beginning "
                "with http:// or https://."
            )
            return

        try:
            with st.spinner(
                random.choice(
                    ANALYSIS_LOADING_MESSAGES
                )
            ):
                article_data = (
                    extract_article_from_url(url)
                )

            if not article_data["text"]:
                st.error(
                    "No readable article text was found at this URL. "
                    "Try pasting the article text directly."
                )
                return

            st.session_state.article_text = (
                article_data["text"]
            )

            st.session_state.article_title = (
                article_data["title"]
            )

            st.session_state.article_authors = (
                article_data["authors"]
            )

            st.session_state.article_publish_date = (
                article_data["publish_date"]
            )

            st.session_state.article_source = (
                article_data["source"]
            )

        except Exception as error:
            st.session_state.article_error = str(
                error
            )

            st.error(
                "The article could not be retrieved. The website may block "
                "automated access, require a subscription, or use an "
                "unsupported page structure."
            )

            with st.expander(
                "View technical details"
            ):
                st.code(str(error))

            return

    elif input_mode == "Paste Text":
        pasted_text = clean_article_text(
            article_input or ""
        )

        if not pasted_text:
            st.error(
                "Paste article text before analyzing."
            )
            return

        if len(pasted_text) < 100:
            st.warning(
                "The submitted text is very short. The resulting summary "
                "may not contain enough context."
            )

        st.session_state.article_text = pasted_text
        st.session_state.article_title = "Pasted Article"
        st.session_state.article_authors = "Not provided"
        st.session_state.article_publish_date = "Not provided"
        st.session_state.article_source = "Pasted text"

    elif input_mode == "Upload PDF":
        if article_input is None:
            st.error(
                "Upload a PDF before analyzing."
            )
            return

        try:
            with st.spinner(
                random.choice(
                    PDF_LOADING_MESSAGES
                )
            ):
                pdf_bytes = article_input.getvalue()

                extracted_text = (
                    extract_text_from_pdf(
                        pdf_bytes
                    )
                )

            if not extracted_text:
                st.error(
                    "No readable text was found in this PDF. It may be "
                    "scanned, image-based, password-protected, or empty."
                )
                return

            st.session_state.article_text = extracted_text

            st.session_state.article_title = (
                os.path.splitext(
                    article_input.name
                )[0]
            )

            st.session_state.article_authors = "Not detected"
            st.session_state.article_publish_date = "Not detected"
            st.session_state.article_source = article_input.name

        except Exception as error:
            st.session_state.article_error = str(
                error
            )

            st.error(
                "The uploaded PDF could not be processed."
            )

            with st.expander(
                "View technical details"
            ):
                st.code(str(error))

            return

    st.session_state.article_summary = summarize_article(
        st.session_state.article_text
    )

    st.session_state.article_analyzed = True



# =========================================================
# Results
# =========================================================

def render_results():
    if not st.session_state.article_analyzed:
        return

    article_text = (
        st.session_state.article_text
    )

    summary = (
        st.session_state.article_summary
    )

    statistics = get_text_statistics(
        article_text
    )

    st.markdown(
        """
        <div class="section-heading">Analysis results</div>
        <div class="section-description">
            Review the extracted article details and generated summary.
        </div>
        """,
        unsafe_allow_html=True,
    )

    metric_col1, metric_col2, metric_col3, metric_col4 = (
        st.columns(4)
    )

    with metric_col1:
        st.metric(
            "Words",
            f"{statistics['Words']:,}",
        )

    with metric_col2:
        st.metric(
            "Characters",
            f"{statistics['Characters']:,}",
        )

    with metric_col3:
        st.metric(
            "Sentences",
            f"{statistics['Sentences']:,}",
        )

    with metric_col4:
        st.metric(
            "Estimated Reading",
            statistics["Reading Time"],
        )

    title = (
        st.session_state.article_title
        or "Untitled Article"
    )

    authors = (
        st.session_state.article_authors
        or "Not detected"
    )

    publish_date = (
        st.session_state.article_publish_date
        or "Not detected"
    )

    source = (
        st.session_state.article_source
        or "Not provided"
    )

    with st.container(border=True):
        st.markdown("#### Article details")

        detail_col1, detail_col2 = st.columns(
            [1, 4]
        )

        with detail_col1:
            st.markdown("**Title**")

        with detail_col2:
            st.write(title)

        detail_col1, detail_col2 = st.columns(
            [1, 4]
        )

        with detail_col1:
            st.markdown("**Author**")

        with detail_col2:
            st.write(authors)

        detail_col1, detail_col2 = st.columns(
            [1, 4]
        )

        with detail_col1:
            st.markdown("**Published**")

        with detail_col2:
            st.write(publish_date)

        detail_col1, detail_col2 = st.columns(
            [1, 4]
        )

        with detail_col1:
            st.markdown("**Source**")

        with detail_col2:
            st.write(source)

    if st.session_state.article_hidden_command == "SOLITAIRE":
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

    summary_tab, source_tab, details_tab = st.tabs(
        [
            "Summary",
            "Extracted Text",
            "Text Details",
        ]
    )

    with summary_tab:
        st.markdown(
            """
            <div class="summary-card-label">
                Generated Summary
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.write(summary)

        summary_length = len(summary)
        original_length = len(article_text)

        if original_length:
            retained_percentage = min(
                100,
                round(
                    (
                        summary_length
                        / original_length
                    )
                    * 100
                ),
            )
        else:
            retained_percentage = 0

        st.caption(
            f"Summary length: {summary_length:,} characters · "
            f"Approximately {retained_percentage}% of extracted text"
        )

    with source_tab:
        st.text_area(
            "Extracted article text",
            value=article_text,
            height=420,
            disabled=True,
        )

    with details_tab:
        import pandas as pd

        comma_count = article_text.count(",")

        details_dataframe = pd.DataFrame(
            {
                "Measurement": [
                    "Word count",
                    "Character count",
                    "Sentence count",
                    "Comma count",
                    "Estimated reading time",
                    "Summary character limit",
                ],
                "Value": [
                    f"{statistics['Words']:,}",
                    f"{statistics['Characters']:,}",
                    f"{statistics['Sentences']:,}",
                    f"{comma_count:,}",
                    statistics["Reading Time"],
                    f"{SUMMARY_CHARACTER_LIMIT:,}",
                ],
            }
        )

        st.dataframe(
            details_dataframe,
            use_container_width=True,
            hide_index=True,
        )

    render_export_section(
        summary,
        title,
    )


def render_export_section(
    summary,
    title,
):
    st.markdown(
        """
        <div class="section-heading">Export summary</div>
        <div class="section-description">
            Generate a formatted PDF containing the current summary.
        </div>
        """,
        unsafe_allow_html=True,
    )

    try:
        pdf_data = export_summary_to_pdf(
            summary=summary,
            title=title,
        )

        safe_filename = re.sub(
            r"[^A-Za-z0-9_-]+",
            "_",
            title,
        ).strip("_")

        if not safe_filename:
            safe_filename = "article_summary"

        st.download_button(
            label="Download Summary as PDF",
            data=pdf_data,
            file_name=(
                f"{safe_filename}_summary.pdf"
            ),
            mime="application/pdf",
            use_container_width=True,
        )

    except Exception as error:
        st.error(
            "The PDF could not be generated."
        )

        with st.expander(
            "View technical details"
        ):
            st.code(str(error))


# =========================================================
# Main application
# =========================================================

def main():
    initialize_session_state()
    apply_page_styles()

    st.markdown(
        """
        <div class="analyzer-header">
            <div class="analyzer-header-label">
                Research Tool
            </div>
            <h1>Article Analyzer</h1>
            <p>
                Extract and review article content from a webpage, pasted text,
                or PDF. Generate a concise preview and export the result as a
                formatted PDF.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    render_input_section()
    render_results()

    st.markdown(
        """
        <div class="analyzer-disclaimer">
            <strong>Automation notice:</strong> Extracted content and generated
            summaries may be incomplete or inaccurate. Review the original
            article and verify important information against official sources.
        </div>
        """,
        unsafe_allow_html=True,
    )


# =========================================================
# Required for multipage setup
# =========================================================

def run():
    main()
