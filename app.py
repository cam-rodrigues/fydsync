import importlib.util
import os

import streamlit as st


st.set_page_config(
    page_title="FidSync Beta",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

PAGES_DIR = "app_pages"


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
            padding-top: 1.25rem;
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

        /* ---------- Sidebar logo ---------- */

        .sidebar-logo-wrapper {
            margin: 0 0 1.75rem 0;
            padding: 0 0.5rem;
        }

        .sidebar-title-container {
            display: flex;
            align-items: center;
            gap: 0.45rem;
        }

        .sidebar-title {
            color: #102542;
            font-size: 1.75rem;
            font-weight: 800;
            line-height: 1;
            letter-spacing: -0.04rem;
        }

        .beta-badge {
            background-color: #2b6cb0;
            color: white;
            font-size: 0.52rem;
            font-weight: 700;
            padding: 0.17rem 0.35rem;
            border-radius: 0.3rem;
            letter-spacing: 0.04rem;
            opacity: 0;
            animation: fadeScaleUp 0.4s ease-out 0.25s forwards;
        }

        .logo-underline {
            width: 2.75rem;
            height: 3px;
            margin-top: 0.65rem;
            background-color: #2b6cb0;
            border-radius: 10px;
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

        /* ---------- Homepage ---------- */

        .hero {
            padding: 2.2rem 2.4rem;
            margin-bottom: 1.5rem;
            background: linear-gradient(135deg, #102542 0%, #213b5c 100%);
            border: 1px solid #2d496b;
            border-radius: 1rem;
            box-shadow: 0 8px 24px rgba(15, 37, 66, 0.12);
        }

        .hero-eyebrow {
            margin-bottom: 0.6rem;
            color: #b9cde5;
            font-size: 0.72rem;
            font-weight: 700;
            letter-spacing: 0.1rem;
            text-transform: uppercase;
        }

        .hero-title {
            margin: 0;
            color: white;
            font-size: 2.3rem;
            font-weight: 750;
            line-height: 1.15;
            letter-spacing: -0.06rem;
        }

        .hero-description {
            max-width: 750px;
            margin-top: 0.8rem;
            margin-bottom: 0;
            color: #d8e4f2;
            font-size: 1rem;
            line-height: 1.6;
        }

        .feature-card {
            min-height: 175px;
            padding: 1.25rem;
            background-color: white;
            border: 1px solid #dce3ec;
            border-radius: 0.8rem;
            box-shadow: 0 2px 8px rgba(15, 37, 66, 0.04);
        }

        .feature-card h3 {
            margin: 0 0 0.55rem 0;
            color: #102542;
            font-size: 1.02rem;
        }

        .feature-card p {
            margin: 0;
            color: #64748b;
            font-size: 0.88rem;
            line-height: 1.55;
        }

        .notice-box {
            margin-top: 1.5rem;
            padding: 0.9rem 1rem;
            background-color: #edf3fa;
            border: 1px solid #cfdae8;
            border-left: 4px solid #2b6cb0;
            border-radius: 0.55rem;
            color: #475569;
            font-size: 0.84rem;
        }

        @keyframes fadeScaleUp {
            from {
                opacity: 0;
                transform: scale(0.85);
            }

            to {
                opacity: 1;
                transform: scale(1);
            }
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# Navigation
# =========================================================

selected_page = st.query_params.get("page")


st.sidebar.markdown(
    """
    <div class="sidebar-logo-wrapper">
        <div class="sidebar-title-container">
            <div class="sidebar-title">FidSync</div>
            <div class="beta-badge">BETA</div>
        </div>
        <div class="logo-underline"></div>
    </div>
    """,
    unsafe_allow_html=True,
)


def nav_button(label: str, filename: str) -> None:
    """Create a sidebar navigation button with an active-page style."""

    is_active = selected_page == filename

    if is_active:
        st.sidebar.markdown('<div class="active-nav">', unsafe_allow_html=True)

    clicked = st.sidebar.button(
        label,
        key=f"nav_{filename}",
        use_container_width=True,
    )

    if is_active:
        st.sidebar.markdown("</div>", unsafe_allow_html=True)

    if clicked:
        st.query_params["page"] = filename
        st.rerun()


st.sidebar.markdown(
    '<div class="sidebar-section">Documentation</div>',
    unsafe_allow_html=True,
)
nav_button("Getting Started", "Getting_Started.py")
nav_button("Capabilities & Potential", "capabilities_and_potential.py")
nav_button("Resources", "resources.py")
nav_button("User Requests", "user_requests.py")

st.sidebar.markdown(
    '<div class="sidebar-section">Tools</div>',
    unsafe_allow_html=True,
)
nav_button("Article Analyzer", "article_analyzer.py")
nav_button("Company Lookup", "company_lookup.py")

st.sidebar.markdown(
    '<div class="sidebar-section">MPI Tools</div>',
    unsafe_allow_html=True,
)

with st.sidebar.expander("Open MPI tools", expanded=False):
    nav_button("Fund Scorecard", "fund_scorecard.py")
    nav_button("Scorecard Metrics", "fund_scorecard_metrics.py")
    nav_button("IPS Screening", "ips_screening.py")
    nav_button("Writeup", "write_up.py")
    nav_button("Writeup & Recommendation", "writeup_&_rec.py")

st.sidebar.markdown(
    '<div class="sidebar-section">Testing</div>',
    unsafe_allow_html=True,
)
nav_button("Fund Scorecard Test", "fund_scorecard_test.py")


# =========================================================
# Page routing
# =========================================================

legacy_redirects = {
    "company_scraper.py": "data_scanner.py",
}

if selected_page in legacy_redirects:
    selected_page = legacy_redirects[selected_page]
    st.query_params["page"] = selected_page
    st.rerun()


def load_page(filename: str) -> None:
    """Import and run a page from the app_pages directory."""

    page_path = os.path.join(PAGES_DIR, filename)

    if not os.path.exists(page_path):
        st.warning(f"Page '{filename}' was not found. Returning to the homepage.")
        st.query_params.clear()
        st.rerun()

    try:
        module_name = f"fidsync_page_{os.path.splitext(filename)[0]}"

        spec = importlib.util.spec_from_file_location(module_name, page_path)

        if spec is None or spec.loader is None:
            raise ImportError(f"Unable to create an import specification for {filename}.")

        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        if not hasattr(module, "run"):
            raise AttributeError(
                f"The page '{filename}' does not contain a run() function."
            )

        module.run()

    except Exception as error:
        st.error("This page could not be loaded.")
        st.exception(error)


# =========================================================
# Homepage
# =========================================================

def show_homepage() -> None:
    st.markdown(
        """
        <div class="hero">
            <div class="hero-eyebrow">Financial Data Toolkit</div>
            <h1 class="hero-title">Welcome to FidSync</h1>
            <p class="hero-description">
                Compare, analyze, and present financial data through one
                streamlined collection of research and reporting tools.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### Available tools")

    column1, column2, column3, column4 = st.columns(4)

    with column1:
        st.markdown(
            """
            <div class="feature-card">
                <h3>Fund Scorecards</h3>
                <p>
                    Evaluate fund performance, review key metrics, and identify
                    potential watchlist concerns.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with column2:
        st.markdown(
            """
            <div class="feature-card">
                <h3>Quarter Comparisons</h3>
                <p>
                    Compare reporting periods and track changes in fund criteria
                    and performance.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with column3:
        st.markdown(
            """
            <div class="feature-card">
                <h3>Article Analysis</h3>
                <p>
                    Convert financial articles and market news into organized,
                    structured summaries.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with column4:
        st.markdown(
            """
            <div class="feature-card">
                <h3>Company Research</h3>
                <p>
                    Quickly gather and organize company-level information across
                    firms and sectors.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        """
        <div class="notice-box">
            <strong>Beta notice:</strong> Some content is generated through
            automated processes and may contain inaccuracies. Verify important
            information against official sources before using it.
        </div>
        """,
        unsafe_allow_html=True,
    )


if selected_page:
    load_page(selected_page)
else:
    show_homepage()
