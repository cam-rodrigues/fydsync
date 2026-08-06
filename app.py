# app.py

from datetime import datetime
from zoneinfo import ZoneInfo
import importlib.util
import os
import random
import uuid
from urllib.parse import urlencode

import streamlit as st


# =========================================================
# File paths
# =========================================================

PAGES_DIR = "app_pages"
ASSETS_DIR = "assets"

APP_VERSION = "0.9"
APP_STAGE = "Beta"
APP_TIMEZONE = ZoneInfo("America/New_York")

ICON_PATH = os.path.join(
    ASSETS_DIR,
    "fidsync_icon.png",
)

SIDEBAR_LOGO_PATH = os.path.join(
    ASSETS_DIR,
    "fidsync_logo.png",
)

DEFAULT_PAGE = "Getting_Started.py"
DUCK_DEBUGGER_PAGE = "rubber_duck.py"

PAGE_GROUPS = {
    "Documentation": {
        "Getting Started": "Getting_Started.py",
        "Roadmap": "roadmap.py",
        "User Requests": "user_requests.py",
    },
    "Research": {
        "Resources": "resources.py",
        "Article Analysis": "article_analyzer.py",
        "Company Research": "company_lookup.py",
    },
    "Analyst Tools": {
        "Fund Scorecard": "fund_scorecard_metrics.py",
        "IPS Screening": "ips_screening.py",
        "Writeup": "write_up.py",
        "Writeup & Rec": "writeup_&_rec.py",
    },
    "Development": {
        "Sandbox": "testing.py",
    },
}

ALLOWED_PAGES = {
    filename
    for pages in PAGE_GROUPS.values()
    for filename in pages.values()
}
ALLOWED_PAGES.add(DUCK_DEBUGGER_PAGE)

LEGACY_REDIRECTS = {
    "company_scraper.py": "company_lookup.py",
    "data_scanner.py": "company_lookup.py",
}

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
        "last_startup_message": None,
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

    now = datetime.now(APP_TIMEZONE)

    if now.hour < 8:
        message_group = "early"
    elif now.hour < 12:
        message_group = "morning"
    elif now.hour < 17:
        message_group = "afternoon"
    else:
        message_group = "evening"

    available_messages = list(TIME_MESSAGES[message_group])

    if now.weekday() == 4:
        available_messages.extend(TIME_MESSAGES["friday"])

    previous_message = st.session_state.last_startup_message
    non_repeating_messages = [
        message
        for message in available_messages
        if message != previous_message
    ]

    selected_message = random.choice(
        non_repeating_messages or available_messages
    )

    st.toast(
        selected_message,
        icon="🕒",
    )

    st.session_state.last_startup_message = selected_message
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
    """Very rarely show a nonblocking fake error in developer mode."""
    if st.session_state.fake_error_checked:
        return

    st.session_state.fake_error_checked = True

    if (
        st.session_state.app_secret_mode
        and random.random() < 0.05
    ):
        st.toast(
            random.choice(FAKE_ERROR_MESSAGES),
            icon="🚨",
        )
        st.toast(
            random.choice(FAKE_RECOVERY_MESSAGES),
            icon="✅",
        )


# Read developer mode before startup messages run.
handle_secret_query_mode()

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
            border-right: 1px solid #d7e0eb;
        }

        [data-testid="stSidebar"] > div:first-child {
            padding-top: 0.4rem;
        }

        [data-testid="stSidebar"] [data-testid="stSidebarContent"] {
            padding-left: 0.85rem;
            padding-right: 0.85rem;
            padding-bottom: 0.85rem;
        }

        [data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
            gap: 0.25rem;
        }

        /* Sidebar logo */

        [data-testid="stSidebar"] [data-testid="stImage"] {
            margin: 0 auto 0.05rem auto;
        }

        [data-testid="stSidebar"] [data-testid="stImage"] img {
            display: block;
            width: 88%;
            max-width: 220px;
            height: auto;
            margin: 0 auto;
            object-fit: contain;
        }

        .sidebar-build-label {
            margin-top: -0.1rem;
            margin-bottom: 0.35rem;
            color: #718096;
            font-size: 0.66rem;
            font-weight: 650;
            letter-spacing: 0.035rem;
            text-align: center;
        }

        .sidebar-logo-divider {
            height: 1px;
            margin: 0.4rem 0 0.65rem 0;
            background-color: #d7e0eb;
        }

        /* Custom navigation */

        .sidebar-nav-section {
            margin: 0.9rem 0 0.28rem 0;
        }

        .sidebar-nav-section:first-of-type {
            margin-top: 0.35rem;
        }

        .sidebar-nav-heading {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            margin: 0 0 0.3rem 0.3rem;
            color: #7b8798;
            font-size: 0.63rem;
            font-weight: 750;
            letter-spacing: 0.085rem;
            line-height: 1;
            text-transform: uppercase;
        }

        .sidebar-nav-heading::after {
            content: "";
            flex: 1;
            height: 1px;
            margin-right: 0.2rem;
            background-color: #dbe3ed;
        }

        .sidebar-nav-list {
            display: flex;
            flex-direction: column;
            gap: 0.12rem;
        }

        .sidebar-nav-link {
            position: relative;
            display: flex;
            align-items: center;
            min-height: 2.05rem;
            padding: 0.32rem 0.62rem 0.32rem 0.8rem;
            color: #334155 !important;
            font-size: 0.83rem;
            font-weight: 500;
            line-height: 1.15;
            text-decoration: none !important;
            border: 1px solid transparent;
            border-radius: 0.45rem;
            background-color: transparent;
            transition:
                background-color 0.14s ease,
                border-color 0.14s ease,
                color 0.14s ease,
                transform 0.14s ease;
        }

        .sidebar-nav-link:hover {
            color: #102542 !important;
            background-color: #e7edf5;
            border-color: #d3ddea;
            transform: translateX(2px);
        }

        .sidebar-nav-link.active {
            color: #102542 !important;
            background-color: #dce7f5;
            border-color: #b8c9df;
            font-weight: 675;
        }

        .sidebar-nav-link.active::before {
            content: "";
            position: absolute;
            left: 0.28rem;
            top: 0.38rem;
            bottom: 0.38rem;
            width: 3px;
            border-radius: 999px;
            background-color: #102542;
        }

        /* Native controls below navigation */

        [data-testid="stSidebar"] .stButton > button {
            min-height: 2.15rem;
            border-radius: 0.48rem;
            padding: 0.35rem 0.65rem;
            font-size: 0.8rem;
            font-weight: 600;
            box-shadow: none;
        }

        [data-testid="stSidebar"] details {
            margin-top: 0.75rem;
            background-color: rgba(255, 255, 255, 0.55);
            border: 1px solid #d6dfeb;
            border-radius: 0.5rem;
        }

        [data-testid="stSidebar"] details summary {
            min-height: 2.2rem;
            padding: 0.32rem 0.62rem;
            color: #334155;
            font-size: 0.8rem;
            font-weight: 600;
            border-radius: 0.5rem;
        }

        [data-testid="stSidebar"] details summary:hover {
            background-color: #e7edf5;
        }

        [data-testid="stSidebar"] details [data-testid="stVerticalBlock"] {
            gap: 0.25rem;
            padding: 0.1rem 0.25rem 0.4rem 0.25rem;
        }

        [data-testid="stSidebar"] hr {
            margin: 0.55rem 0;
        }

        [data-testid="stSidebar"] [data-testid="stCaptionContainer"] p {
            margin: 0.08rem 0;
            font-size: 0.72rem;
            line-height: 1.35;
        }

        .version-label {
            margin-bottom: 0.25rem;
            color: #102542;
            font-size: 0.84rem;
            font-weight: 700;
        }

        .version-note {
            margin-bottom: 0.35rem;
            color: #64748b;
            font-size: 0.73rem;
            line-height: 1.4;
        }

        .developer-status {
            margin-top: 0.4rem;
            padding: 0.5rem 0.6rem;
            background-color: #dce7f5;
            border: 1px solid #b8c9df;
            border-radius: 0.45rem;
            color: #102542;
            font-size: 0.72rem;
            font-weight: 650;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# Navigation state
# =========================================================

requested_page = st.query_params.get("page")

if requested_page in LEGACY_REDIRECTS:
    redirected_page = LEGACY_REDIRECTS[requested_page]
    st.query_params["page"] = redirected_page
    st.rerun()

if requested_page in ALLOWED_PAGES:
    selected_page = requested_page
else:
    selected_page = DEFAULT_PAGE

    if requested_page:
        st.query_params["page"] = DEFAULT_PAGE


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
    f"""
    <div class="sidebar-build-label">
        Internal {APP_STAGE} · Build {APP_VERSION}
    </div>
    <div class="sidebar-logo-divider"></div>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# Navigation helper
# =========================================================

def build_page_url(filename: str) -> str:
    """Build a page URL while preserving developer mode."""

    params = {"page": filename}

    if st.session_state.app_secret_mode:
        params["mode"] = "developer"

    return f"?{urlencode(params)}"


def nav_link(label: str, filename: str) -> str:
    """Return one custom sidebar navigation link."""

    active_class = " active" if selected_page == filename else ""
    page_url = build_page_url(filename)

    return (
        f'<a class="sidebar-nav-link{active_class}" '
        f'href="{page_url}" target="_self">'
        f"{label}"
        "</a>"
    )


# =========================================================
# Sidebar navigation
# =========================================================

for section_name, pages in PAGE_GROUPS.items():
    links_html = "".join(
        nav_link(label, filename)
        for label, filename in pages.items()
    )

    st.sidebar.markdown(
        f"""
        <div class="sidebar-nav-section">
            <div class="sidebar-nav-heading">
                {section_name}
            </div>
            <div class="sidebar-nav-list">
                {links_html}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def open_duck_debugger() -> None:
    """Open the hidden Rubber Duck Debugger page."""

    st.session_state.duck_previous_page = selected_page
    st.query_params["page"] = DUCK_DEBUGGER_PAGE


# =========================================================
# Sidebar Easter egg panel
# =========================================================

with st.sidebar.expander(
    f"Version {APP_VERSION} {APP_STAGE}",
    expanded=False,
):
    st.markdown(
        f"""
        <div class="version-label">FidSync {APP_STAGE}</div>
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
            current_page_path = os.path.join(
                PAGES_DIR,
                selected_page,
            )

            missing_registered_pages = sorted(
                filename
                for filename in ALLOWED_PAGES
                if not os.path.exists(
                    os.path.join(PAGES_DIR, filename)
                )
            )

            st.write(
                "Pages directory:",
                "Found" if os.path.isdir(PAGES_DIR) else "Missing",
            )
            st.write(
                "Current page file:",
                "Found" if os.path.exists(current_page_path) else "Missing",
            )
            st.write("Current page:", selected_page)
            st.write("Current timezone:", str(APP_TIMEZONE))
            st.write(
                "Registered pages:",
                len(ALLOWED_PAGES),
            )

            if missing_registered_pages:
                st.warning(
                    "Missing registered page files: "
                    + ", ".join(missing_registered_pages)
                )
            else:
                st.success("All registered page files were found.")

            st.metric(
                "System Checks",
                st.session_state.app_system_check_clicks,
            )

            st.caption(
                "Disable developer mode by adding "
                "`?mode=normal` to the URL."
            )




# =========================================================
# Page loader
# =========================================================

def load_page(filename: str) -> None:
    """Import and run one registered page."""

    if filename not in ALLOWED_PAGES:
        st.error("That page is not registered.")
        st.query_params["page"] = DEFAULT_PAGE
        st.rerun()

    page_path = os.path.abspath(
        os.path.join(
            PAGES_DIR,
            filename,
        )
    )
    pages_root = os.path.abspath(PAGES_DIR)

    if os.path.commonpath([pages_root, page_path]) != pages_root:
        st.error("That page path is not allowed.")
        st.query_params["page"] = DEFAULT_PAGE
        st.rerun()

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
        error_reference = uuid.uuid4().hex[:8].upper()

        st.error(
            "This page could not be loaded. "
            f"Error reference: `{error_reference}`"
        )

        action_col, debugger_col = st.columns(2)

        with action_col:
            if st.button(
                "Return to Getting Started",
                key=f"return_home_{error_reference}",
                use_container_width=True,
            ):
                st.query_params["page"] = DEFAULT_PAGE
                st.rerun()

        with debugger_col:
            if st.button(
                "Open Debugger",
                key=f"open_debugger_{error_reference}",
                use_container_width=True,
            ):
                st.session_state.duck_previous_page = filename
                st.query_params["page"] = DUCK_DEBUGGER_PAGE
                st.rerun()

        with st.expander(
            "View technical details",
            expanded=False,
        ):
            st.caption(f"Error reference: {error_reference}")
            st.exception(error)


# =========================================================
# Run selected page
# =========================================================

load_page(selected_page)
