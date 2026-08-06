# app.py

from datetime import datetime
from zoneinfo import ZoneInfo
import importlib.util
import os
import random
import time

import streamlit as st


# =========================================================
# File paths
# =========================================================

PAGES_DIR = "app_pages"
ASSETS_DIR = "assets"

ICON_PATH = os.path.join(
    ASSETS_DIR,
    "fidsync_icon.png",
)

SIDEBAR_LOGO_PATH = os.path.join(
    ASSETS_DIR,
    "fidsync_logo.png",
)

WORDMARK_PATH = os.path.join(
    ASSETS_DIR,
    "fidsync_wordmark.png",
)

DEFAULT_PAGE = "Getting_Started.py"

TIME_MESSAGES = {
    "early": [
        "Early start detected. Coffee may be required.",
        "You are beating the market to work today.",
        "The spreadsheets appreciate your punctuality.",
    ],
    "morning": [
        "Good morning. The markets are open.",
        "Fresh coffee. Fresh data.",
        "Morning research mode activated.",
    ],
    "afternoon": [
        "Afternoon research session underway.",
        "Hope lunch treated you well.",
        "Spreadsheet endurance test: continuing.",
    ],
    "evening": [
        "Do not forget to take a break.",
        "Don't strain your eyes.",
        "Maybe it's time for a coffee break.",
    ],
    "friday": [
        "Friday detected. The weekend is almost priced in.",
        "Friday afternoon. Productivity may fluctuate.",
        "Markets close soon. So should your laptop.",
    ],
}

RARE_STARTUP_MESSAGES = [
    "Somewhere, a workbook named FINAL_final_v9_REAL.xlsx still exists.",
    "Merged cells remain the leading cause of sadness.",
    "No spreadsheets were harmed during startup.",
    "The financial crystal ball is still unavailable.",
    "Everything eventually becomes a CSV.",
]


FAKE_ERROR_MESSAGES = [
    "ERROR",
    "CRITICAL ERROR",
    "PANIC",
    "Unexpected Spreadsheet Behavior",
    "Financial Reality Distortion Detected",
]

FAKE_RECOVERY_MESSAGES = [
    "Just kidding. Everything is fine.",
    "False alarm.",
    "The spreadsheets survived.",
    "Crisis successfully avoided.",
    "No data was harmed.",
    "Carry on.",
]

# =========================================================
# Page configuration
# =========================================================

st.set_page_config(
    page_title="FidSync Beta",
    page_icon=ICON_PATH,
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# Session state
# =========================================================

def initialize_app_state() -> None:
    """Initialize app-wide session values."""

    defaults = {
        "app_system_check_clicks": 0,
        "app_secret_mode": False,
        "app_diagnostics_unlocked": False,
        "time_greeting_shown": False,
        "rare_startup_message_checked": False,
        "fake_error_checked": False,
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


initialize_app_state()


# =========================================================
# App-wide Easter egg helpers
# =========================================================

def handle_secret_query_mode() -> None:
    """
    Enable or disable developer mode using a URL parameter.

    Examples:
        ?mode=developer
        ?mode=normal
    """

    requested_mode = st.query_params.get("mode")

    if requested_mode == "developer":
        st.session_state.app_secret_mode = True
        st.session_state.app_diagnostics_unlocked = True

    elif requested_mode == "normal":
        st.session_state.app_secret_mode = False


def handle_system_check() -> None:
    """Handle repeated clicks on the sidebar system-check button."""

    st.session_state.app_system_check_clicks += 1
    click_count = st.session_state.app_system_check_clicks

    if click_count == 1:
        st.toast("System check complete.")

    elif click_count == 2:
        st.toast("System remains checked.")

    elif click_count == 3:
        st.toast("Still checking.")

    elif click_count == 4:
        st.toast("One more check should probably do it.")

    elif click_count == 5:
        st.session_state.app_secret_mode = True
        st.session_state.app_diagnostics_unlocked = True

        st.balloons()
        st.toast("Hidden diagnostics unlocked.")

    else:
        st.toast(
            f"System has now been checked {click_count} times."
        )


# =========================================================
# Startup message helpers
# =========================================================

def show_time_greeting() -> None:
    """Show one time-based greeting per browser session."""
    if st.session_state.time_greeting_shown:
        return

    # FIX: Explicitly use datetime.datetime.now() to avoid naming collisions
    now = datetime.now(ZoneInfo("America/New_York"))

    if now.weekday() == 4:
        message_group = "friday"
    elif now.hour < 8:
        message_group = "early"
    elif now.hour < 12:
        message_group = "morning"
    elif now.hour < 17:
        message_group = "afternoon"
    else:
        message_group = "evening"

    st.toast(
        random.choice(TIME_MESSAGES[message_group]),
        icon="🕒",
    )
    st.session_state.time_greeting_shown = True


def maybe_show_rare_startup_message() -> None:
    """Give each session one small chance to receive a rare message."""
    if st.session_state.rare_startup_message_checked:
        return

    st.session_state.rare_startup_message_checked = True

    if random.random() < 0.01:
        st.toast(
            random.choice(RARE_STARTUP_MESSAGES),
            icon="✨",
        )


def maybe_show_fake_error() -> None:
    """Very rarely show a fake error for fun."""
    if st.session_state.fake_error_checked:
        return

    st.session_state.fake_error_checked = True

    # NOTE: Keep the percentage low (0.5%) so it doesn't constantly block your app flow
    if random.random() < 0.005:
        placeholder = st.empty()
        placeholder.error(random.choice(FAKE_ERROR_MESSAGES))
        time.sleep(1.2)  # Short delay so they can read the panic
        placeholder.success(random.choice(FAKE_RECOVERY_MESSAGES))
        time.sleep(1.2)  # Short delay to see the relief
        placeholder.empty()


# Run startup messages once per browser session.
show_time_greeting()
maybe_show_rare_startup_message()
maybe_show_fake_error()


# =========================================================
# Styling
# =========================================================

st.markdown(
    """
    <style>
        /* ---------- App ---------- */

        .stApp {
            background-color: #f8fafc;
        }

        .block-container {
            max-width: 1250px;
            padding-top: 2.5rem;
            padding-bottom: 3rem;
        }

        /* ---------- Sidebar ---------- */

        [data-testid="stSidebar"] {
            background-color: #f4f6fa;
            border-right: 2px solid #d7e0eb;
        }

        [data-testid="stSidebar"] > div:first-child {
            padding-top: 0.65rem;
        }

        /* Sidebar logo image */

        [data-testid="stSidebar"] [data-testid="stImage"] {
            margin-bottom: 0.15rem;
        }

        [data-testid="stSidebar"] [data-testid="stImage"] img {
            display: block;
            max-width: 100%;
            height: auto;
            object-fit: contain;
        }

        .sidebar-build-label {
            margin-top: -0.15rem;
            margin-bottom: 0.8rem;
            color: #718096;
            font-size: 0.7rem;
            font-weight: 600;
            letter-spacing: 0.03rem;
            text-align: center;
        }

        .sidebar-logo-divider {
            height: 1px;
            margin: 0.7rem 0 0.95rem 0;
            background-color: #d7e0eb;
        }

        /* Navigation buttons */

        [data-testid="stSidebar"] .stButton {
            margin-bottom: 0.25rem;
        }

        [data-testid="stSidebar"] .stButton > button {
            width: 100%;
            min-height: 2.5rem;
            justify-content: flex-start;
            background-color: transparent;
            color: #334155;
            border: 1px solid transparent;
            border-radius: 0.55rem;
            padding: 0.45rem 0.75rem;
            font-size: 0.88rem;
            font-weight: 500;
            text-align: left;
            transition:
                background-color 0.15s ease,
                border-color 0.15s ease,
                color 0.15s ease;
        }

        [data-testid="stSidebar"] .stButton > button:hover {
            background-color: #e4ebf5;
            border-color: #cbd7e6;
            color: #102542;
        }

        /* Active navigation button */

        [data-testid="stSidebar"] .active-nav .stButton > button {
            background-color: #dce7f5;
            border-color: #b8c9df;
            color: #102542;
            font-weight: 650;
        }

        /* ---------- Sidebar section labels ---------- */

        .sidebar-section {
            margin: 1.6rem 0 0.45rem 0.25rem;
            color: #7a8798;
            font-size: 0.7rem;
            font-weight: 700;
            letter-spacing: 0.08rem;
            text-transform: uppercase;
        }

        [data-testid="stSidebar"] details {
            background-color: transparent;
            border: none;
        }

        [data-testid="stSidebar"] details summary {
            color: #334155;
            font-size: 0.88rem;
            font-weight: 600;
        }

        /* ---------- Version panel ---------- */

        .version-label {
            margin-bottom: 0.5rem;
            color: #102542;
            font-size: 0.9rem;
            font-weight: 700;
        }

        .version-note {
            color: #64748b;
            font-size: 0.78rem;
            line-height: 1.5;
        }

        .developer-status {
            margin-top: 0.7rem;
            padding: 0.65rem 0.75rem;
            background-color: #dce7f5;
            border: 1px solid #b8c9df;
            border-radius: 0.5rem;
            color: #102542;
            font-size: 0.78rem;
            font-weight: 650;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# Navigation state
# =========================================================

handle_secret_query_mode()

requested_page = st.query_params.get("page")

# If no page is specified, Getting Started is the homepage.
selected_page = requested_page or DEFAULT_PAGE


# =========================================================
# Sidebar logo
# =========================================================

if os.path.exists(SIDEBAR_LOGO_PATH):
    st.sidebar.image(
        SIDEBAR_LOGO_PATH,
        use_container_width=True,
    )
else:
    st.sidebar.error(
        "The FidSync sidebar logo could not be found at "
        f"`{SIDEBAR_LOGO_PATH}`."
    )

st.sidebar.markdown(
    """
    <div class="sidebar-build-label">
        Internal Beta · Build 0.9
    </div>
    <div class="sidebar-logo-divider"></div>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# Navigation helper
# =========================================================

def nav_button(label: str, filename: str) -> None:
    """Create a sidebar navigation button with an active-page style."""

    is_active = selected_page == filename

    if is_active:
        st.sidebar.markdown(
            '<div class="active-nav">',
            unsafe_allow_html=True,
        )

    clicked = st.sidebar.button(
        label,
        key=f"nav_{filename}",
        use_container_width=True,
    )

    if is_active:
        st.sidebar.markdown(
            "</div>",
            unsafe_allow_html=True,
        )

    if clicked:
        # Preserve other query parameters, such as developer mode.
        st.query_params["page"] = filename
        st.rerun()


# =========================================================
# Sidebar navigation
# =========================================================

st.sidebar.markdown(
    '<div class="sidebar-section">Documentation</div>',
    unsafe_allow_html=True,
)

nav_button(
    "Getting Started",
    "Getting_Started.py",
)

nav_button(
    "Capabilities & Potential",
    "capabilities_and_potential.py",
)

nav_button(
    "Resources",
    "resources.py",
)

nav_button(
    "User Requests",
    "user_requests.py",
)


st.sidebar.markdown(
    '<div class="sidebar-section">Tools</div>',
    unsafe_allow_html=True,
)

nav_button(
    "Article Analyzer",
    "article_analyzer.py",
)

nav_button(
    "Company Lookup",
    "company_lookup.py",
)


st.sidebar.markdown(
    '<div class="sidebar-section">MPI Tools</div>',
    unsafe_allow_html=True,
)

with st.sidebar.expander(
    "Open MPI tools",
    expanded=False,
):
    nav_button(
        "Fund Scorecard",
        "fund_scorecard.py",
    )

    nav_button(
        "Scorecard Metrics",
        "fund_scorecard_metrics.py",
    )

    nav_button(
        "IPS Screening",
        "ips_screening.py",
    )

    nav_button(
        "Writeup",
        "write_up.py",
    )

    nav_button(
        "Writeup & Recommendation",
        "writeup_&_rec.py",
    )


st.sidebar.markdown(
    '<div class="sidebar-section">Testing</div>',
    unsafe_allow_html=True,
)

nav_button(
    "Fund Scorecard Test",
    "fund_metric_upgrade_test.py",
)


def open_duck_debugger() -> None:
    """Open the hidden Rubber Duck Debugger page."""

    st.session_state.duck_previous_page = selected_page
    st.query_params["page"] = "rubber_duck.py"


# =========================================================
# Sidebar Easter egg panel
# =========================================================

with st.sidebar.expander(
    "Version 0.9 Beta",
    expanded=False,
):
    st.markdown(
        """
        <div class="version-label">FidSync Beta</div>
        <div class="version-note">
            Built with Python, Streamlit, spreadsheets, and
            cautious optimism.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.caption("Platform status: Operational")
    st.caption("Crystal ball: Unreliable")
    st.caption("Merged-cell tolerance: Low")
    # ---------------------------------------------------------
    # Rubber Duck Debugger
    # ---------------------------------------------------------
    st.divider()
    
    st.button(
        "Debugger",
        key="open_duck_debugger_button",
        use_container_width=True,
        on_click=open_duck_debugger,
    )

    st.divider()

    if st.button(
        "Run System Check",
        key="app_system_check",
        use_container_width=True,
    ):
        handle_system_check()

    if st.session_state.app_secret_mode:
        st.markdown(
            """
            <div class="developer-status">
                Developer mode is active.
            </div>
            """,
            unsafe_allow_html=True,
        )

        with st.expander(
            "Developer diagnostics",
            expanded=False,
        ):
            st.write("Navigation engine: Operational")
            st.write("Page loader: Ready")
            st.write("Spreadsheet containment: Stable")
            st.write("Financial crystal ball: Unreliable")

            st.metric(
                "System Checks",
                st.session_state.app_system_check_clicks,
            )

            st.caption(
                "Disable developer mode by adding "
                "`?mode=normal` to the URL."
            )


# =========================================================
# Legacy redirects
# =========================================================

legacy_redirects = {
    "company_scraper.py": "data_scanner.py",
}

if selected_page in legacy_redirects:
    selected_page = legacy_redirects[selected_page]
    st.query_params["page"] = selected_page
    st.rerun()


# =========================================================
# Page loader
# =========================================================

def load_page(filename: str) -> None:
    """Import and run a page from the app_pages directory."""

    page_path = os.path.join(
        PAGES_DIR,
        filename,
    )

    if not os.path.exists(page_path):
        st.warning(
            f"Page '{filename}' was not found. "
            "Returning to Getting Started."
        )

        # Remove only the page parameter so other settings remain.
        if "page" in st.query_params:
            del st.query_params["page"]

        st.rerun()

    try:
        module_name = (
            f"fidsync_page_"
            f"{os.path.splitext(filename)[0]}"
        )

        spec = importlib.util.spec_from_file_location(
            module_name,
            page_path,
        )

        if spec is None or spec.loader is None:
            raise ImportError(
                "Unable to create an import specification "
                f"for {filename}."
            )

        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        if not hasattr(module, "run"):
            raise AttributeError(
                f"The page '{filename}' does not contain "
                "a run() function."
            )

        module.run()

    except Exception as error:
        st.error("This page could not be loaded. Open debugger for help.")

        with st.expander(
            "View technical details",
            expanded=False,
        ):
            st.exception(error)


# =========================================================
# Run selected page
# =========================================================

load_page(selected_page)
