# app.py

from datetime import datetime, timedelta
import importlib.util
import os
import random

import streamlit as st
from streamlit_autorefresh import st_autorefresh
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

BREAK_REMINDER_MINUTES = 60
BREAK_CHECK_INTERVAL_MS = 60 * 1000

BREAK_REMINDER_MESSAGES = [
    ("Coffee break", "Step away for a few minutes and give your eyes a reset.", "☕"),
    ("Screen break", "Look at something farther away and relax your focus.", "👀"),
    ("Hydration check", "Grab some water and move around for a minute.", "💧"),
    ("Posture reset", "Drop your shoulders, unclench your jaw, and sit back.", "🧘"),
    ("Stretch break", "Stand up and stretch before returning to the spreadsheets.", "🧍"),
    ("Quick reset", "The work will still be here after a short break.", "⏸️"),
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
        "break_reminders_enabled": True,
        "break_reminder_interval_minutes": BREAK_REMINDER_MINUTES,
        "last_break_reminder": datetime.now(),
        "break_reminder_count": 0,
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


def reset_break_timer() -> None:
    """Restart the break-reminder timer from the current moment."""

    st.session_state.last_break_reminder = datetime.now()


def check_break_reminder() -> None:
    """Show a reminder after the configured amount of active app time."""

    if not st.session_state.break_reminders_enabled:
        return

    now = datetime.now()
    interval_minutes = st.session_state.break_reminder_interval_minutes
    reminder_interval = timedelta(minutes=interval_minutes)

    if now - st.session_state.last_break_reminder < reminder_interval:
        return

    title, message, icon = random.choice(BREAK_REMINDER_MESSAGES)

    st.toast(
        f"{title}: {message}",
        icon=icon,
    )

    st.session_state.last_break_reminder = now
    st.session_state.break_reminder_count += 1


# Rerun once per minute so the app can check whether a reminder is due.
# This does not display a reminder every minute.
st_autorefresh(
    interval=BREAK_CHECK_INTERVAL_MS,
    key="fidsync_break_reminder_refresh",
)

check_break_reminder()


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
    "fund_scorecard_test.py",
)


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

    st.divider()

    st.toggle(
        "Break reminders",
        key="break_reminders_enabled",
        help=(
            "Show a short wellness reminder after the selected amount "
            "of active app time."
        ),
        on_change=reset_break_timer,
    )

    reminder_interval = st.selectbox(
        "Reminder interval",
        options=[30, 45, 60, 90],
        format_func=lambda minutes: f"Every {minutes} minutes",
        key="break_reminder_interval_minutes",
        disabled=not st.session_state.break_reminders_enabled,
        on_change=reset_break_timer,
    )

    if st.session_state.break_reminders_enabled:
        st.caption(
            f"Reminders shown this session: "
            f"{st.session_state.break_reminder_count}"
        )

        if st.button(
            "Reset Break Timer",
            key="reset_break_timer_button",
            use_container_width=True,
        ):
            reset_break_timer()
            st.toast("Break timer restarted.", icon="⏱️")

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
        st.error("This page could not be loaded.")

        with st.expander(
            "View technical details",
            expanded=False,
        ):
            st.exception(error)


# =========================================================
# Run selected page
# =========================================================

load_page(selected_page)
