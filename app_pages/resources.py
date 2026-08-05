# app_pages/resources.py

from html import escape
from textwrap import dedent
from urllib.parse import urlparse

import streamlit as st
import streamlit.components.v1 as components


# =========================================================
# Resource data
# =========================================================

CATEGORIES = {
    "Financial News": [
        {
            "name": "Bloomberg",
            "url": "https://www.bloomberg.com",
            "logo": "https://logo.clearbit.com/bloomberg.com",
        },
        {
            "name": "Yahoo Finance",
            "url": "https://finance.yahoo.com",
            "logo": "https://logo.clearbit.com/yahoo.com",
        },
        {
            "name": "CNBC",
            "url": "https://www.cnbc.com",
            "logo": "https://logo.clearbit.com/cnbc.com",
        },
        {
            "name": "MarketWatch",
            "url": "https://www.marketwatch.com",
            "logo": "https://logo.clearbit.com/marketwatch.com",
        },
        {
            "name": "Barron's",
            "url": "https://www.barrons.com",
            "logo": "https://logo.clearbit.com/barrons.com",
        },
        {
            "name": "Reuters",
            "url": "https://www.reuters.com/finance",
            "logo": "https://logo.clearbit.com/reuters.com",
        },
        {
            "name": "The Wall Street Journal",
            "url": "https://www.wsj.com",
            "logo": "https://logo.clearbit.com/wsj.com",
        },
        {
            "name": "Forbes",
            "url": "https://www.forbes.com",
            "logo": "https://logo.clearbit.com/forbes.com",
        },
        {
            "name": "Financial Times",
            "url": "https://www.ft.com",
            "logo": "https://logo.clearbit.com/ft.com",
        },
    ],

    "Market Data & Research": [
        {
            "name": "Morningstar",
            "url": "https://www.morningstar.com",
            "logo": "https://logo.clearbit.com/morningstar.com",
        },
        {
            "name": "TradingView",
            "url": "https://www.tradingview.com",
            "logo": "https://logo.clearbit.com/tradingview.com",
        },
        {
            "name": "Seeking Alpha",
            "url": "https://seekingalpha.com",
            "logo": "https://logo.clearbit.com/seekingalpha.com",
        },
        {
            "name": "Zacks",
            "url": "https://www.zacks.com",
            "logo": "https://logo.clearbit.com/zacks.com",
        },
        {
            "name": "Finviz",
            "url": "https://finviz.com",
            "logo": "https://logo.clearbit.com/finviz.com",
        },
        {
            "name": "Barchart",
            "url": "https://www.barchart.com",
            "logo": "https://logo.clearbit.com/barchart.com",
        },
        {
            "name": "YCharts",
            "url": "https://ycharts.com",
            "logo": "https://logo.clearbit.com/ycharts.com",
        },
        {
            "name": "MacroTrends",
            "url": "https://www.macrotrends.net",
            "logo": "https://logo.clearbit.com/macrotrends.net",
        },
    ],

    "Investment Firms": [
        {
            "name": "Fidelity",
            "url": "https://www.fidelity.com",
            "logo": "https://logo.clearbit.com/fidelity.com",
        },
        {
            "name": "Vanguard",
            "url": "https://investor.vanguard.com",
            "logo": "https://logo.clearbit.com/vanguard.com",
        },
        {
            "name": "Charles Schwab",
            "url": "https://www.schwab.com",
            "logo": "https://logo.clearbit.com/schwab.com",
        },
        {
            "name": "TD Ameritrade",
            "url": "https://www.tdameritrade.com",
            "logo": "https://logo.clearbit.com/tdameritrade.com",
        },
        {
            "name": "J.P. Morgan",
            "url": "https://www.jpmorgan.com",
            "logo": "https://logo.clearbit.com/jpmorgan.com",
        },
        {
            "name": "Envestnet",
            "url": "https://www.envestnet.com",
            "logo": "https://logo.clearbit.com/envestnet.com",
        },
        {
            "name": "T. Rowe Price",
            "url": "https://www.troweprice.com",
            "logo": "https://logo.clearbit.com/troweprice.com",
        },
        {
            "name": "Edward Jones",
            "url": "https://www.edwardjones.com",
            "logo": "https://logo.clearbit.com/edwardjones.com",
        },
    ],

    "Government & Regulatory": [
        {
            "name": "SEC",
            "url": "https://www.sec.gov",
            "logo": "https://logo.clearbit.com/sec.gov",
        },
        {
            "name": "FINRA",
            "url": "https://www.finra.org",
            "logo": "https://logo.clearbit.com/finra.org",
        },
        {
            "name": "FDIC",
            "url": "https://www.fdic.gov",
            "logo": "https://logo.clearbit.com/fdic.gov",
        },
        {
            "name": "Federal Reserve",
            "url": "https://www.federalreserve.gov",
            "logo": "https://logo.clearbit.com/federalreserve.gov",
        },
        {
            "name": "CFPB",
            "url": "https://www.consumerfinance.gov",
            "logo": "https://logo.clearbit.com/consumerfinance.gov",
        },
        {
            "name": "IRS",
            "url": "https://www.irs.gov",
            "logo": "https://logo.clearbit.com/irs.gov",
        },
    ],

    "Education & Tools": [
        {
            "name": "Investopedia",
            "url": "https://www.investopedia.com",
            "logo": "https://logo.clearbit.com/investopedia.com",
        },
        {
            "name": "NerdWallet",
            "url": "https://www.nerdwallet.com",
            "logo": "https://logo.clearbit.com/nerdwallet.com",
        },
        {
            "name": "eMoney",
            "url": "https://emoneyadvisor.com",
            "logo": "https://logo.clearbit.com/emoneyadvisor.com",
        },
        {
            "name": "Khan Academy",
            "url": "https://www.khanacademy.org/economics-finance-domain",
            "logo": "https://logo.clearbit.com/khanacademy.org",
        },
        {
            "name": "SmartAsset",
            "url": "https://smartasset.com",
            "logo": "https://logo.clearbit.com/smartasset.com",
        },
        {
            "name": "Bankrate",
            "url": "https://www.bankrate.com",
            "logo": "https://logo.clearbit.com/bankrate.com",
        },
        {
            "name": "Mint",
            "url": "https://mint.intuit.com",
            "logo": "https://logo.clearbit.com/mint.intuit.com",
        },
    ],
}


CATEGORY_DESCRIPTIONS = {
    "Financial News": (
        "Market coverage, business reporting, and financial news "
        "from established publishers."
    ),
    "Market Data & Research": (
        "Research platforms, investment screening tools, charts, "
        "fund data, and market analytics."
    ),
    "Investment Firms": (
        "Custodians, asset managers, wealth-management platforms, "
        "and investment providers."
    ),
    "Government & Regulatory": (
        "Official regulatory guidance, filings, economic information, "
        "and consumer resources."
    ),
    "Education & Tools": (
        "Financial education, planning tools, calculators, and "
        "reference materials."
    ),
}


# =========================================================
# Helpers
# =========================================================

def get_domain(url):
    """Return a clean domain for display."""

    domain = urlparse(url).netloc.lower()

    if domain.startswith("www."):
        domain = domain[4:]

    return domain


def filter_resources(search_term, selected_category):
    """Filter categories and sites using the selected controls."""

    normalized_search = search_term.strip().lower()
    filtered_categories = {}

    for category, sites in CATEGORIES.items():
        if (
            selected_category != "All Categories"
            and category != selected_category
        ):
            continue

        matching_sites = []

        for site in sites:
            searchable_text = " ".join(
                [
                    site["name"],
                    category,
                    get_domain(site["url"]),
                ]
            ).lower()

            if (
                not normalized_search
                or normalized_search in searchable_text
            ):
                matching_sites.append(site)

        if matching_sites:
            filtered_categories[category] = matching_sites

    return filtered_categories


def build_resource_grid(sites):
    """Create the HTML for one category's resource-card grid."""

    cards = []

    for site in sites:
        name = escape(site["name"])
        url = escape(site["url"], quote=True)
        logo = escape(site["logo"], quote=True)
        domain = escape(get_domain(site["url"]))

        initial = escape(site["name"][:1].upper())

        cards.append(
            f"""
            <a
                href="{url}"
                target="_blank"
                rel="noopener noreferrer"
                class="resource-card"
                aria-label="Open {name}"
            >
                <div class="resource-logo-area">
                    <img
                        src="{logo}"
                        alt="{name} logo"
                        loading="lazy"
                        onerror="
                            this.style.display='none';
                            this.nextElementSibling.style.display='flex';
                        "
                    >
                    <div class="resource-logo-fallback">
                        {initial}
                    </div>
                </div>

                <div class="resource-information">
                    <div class="resource-name">
                        {name}
                    </div>

                    <div class="resource-domain">
                        {domain}
                    </div>
                </div>

                <div class="external-arrow">
                    ↗
                </div>
            </a>
            """
        )

    return (
        '<div class="resource-grid">'
        + "".join(cards)
        + "</div>"
    )


def render_resource_category(category, sites):
    """Render one category heading and its resource grid."""

    description = CATEGORY_DESCRIPTIONS.get(
        category,
        "Trusted financial and research resources.",
    )

    st.markdown(
        dedent(f"""
        <div class="category-heading-row">
            <div>
                <div class="category-title">
                    {escape(category)}
                </div>
                <div class="category-description">
                    {escape(description)}
                </div>
            </div>

            <div class="category-count">
                {len(sites)} resource{"s" if len(sites) != 1 else ""}
            </div>
        </div>
        """),
        unsafe_allow_html=True,
)

    grid_html = RESOURCE_COMPONENT_CSS + build_resource_grid(sites)

    row_count = max(1, (len(sites) + 3) // 4)
    component_height = 30 + (row_count * 158)

    components.html(
        grid_html,
        height=component_height,
        scrolling=False,
    )


# =========================================================
# Component styling
# =========================================================

RESOURCE_COMPONENT_CSS = """
<style>
    * {
        box-sizing: border-box;
    }

    body {
        margin: 0;
        padding: 0;
        background: transparent;
        font-family:
            Inter,
            -apple-system,
            BlinkMacSystemFont,
            "Segoe UI",
            sans-serif;
    }

    .resource-grid {
        display: grid;
        grid-template-columns:
            repeat(4, minmax(0, 1fr));
        gap: 14px;
        padding: 4px 2px 12px 2px;
    }

    .resource-card {
        min-height: 140px;
        padding: 18px 16px 15px 16px;
        position: relative;
        display: flex;
        flex-direction: column;
        align-items: flex-start;
        justify-content: space-between;
        overflow: hidden;
        background:
            linear-gradient(
                145deg,
                #ffffff 0%,
                #f8fbff 100%
            );
        border: 1px solid #d9e3ee;
        border-radius: 14px;
        color: inherit;
        text-decoration: none;
        box-shadow:
            0 2px 8px rgba(16, 37, 66, 0.045);
        transition:
            transform 0.16s ease,
            border-color 0.16s ease,
            box-shadow 0.16s ease,
            background-color 0.16s ease;
    }

    .resource-card:hover {
        transform: translateY(-3px);
        border-color: #9eb8d6;
        box-shadow:
            0 9px 22px rgba(16, 37, 66, 0.10);
        background:
            linear-gradient(
                145deg,
                #ffffff 0%,
                #f1f6fc 100%
            );
    }

    .resource-logo-area {
        width: 100%;
        height: 54px;
        display: flex;
        align-items: center;
        justify-content: flex-start;
        margin-bottom: 13px;
    }

    .resource-logo-area img {
        display: block;
        max-width: 112px;
        max-height: 47px;
        width: auto;
        height: auto;
        object-fit: contain;
    }

    .resource-logo-fallback {
        width: 44px;
        height: 44px;
        display: none;
        align-items: center;
        justify-content: center;
        border-radius: 11px;
        background-color: #e2ebf6;
        color: #164170;
        font-size: 19px;
        font-weight: 750;
    }

    .resource-information {
        width: 100%;
        min-width: 0;
    }

    .resource-name {
        margin-bottom: 4px;
        color: #102542;
        font-size: 14px;
        font-weight: 700;
        line-height: 1.25;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }

    .resource-domain {
        color: #718096;
        font-size: 11px;
        line-height: 1.35;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }

    .external-arrow {
        position: absolute;
        top: 12px;
        right: 13px;
        color: #91a5bb;
        font-size: 15px;
        transition:
            color 0.16s ease,
            transform 0.16s ease;
    }

    .resource-card:hover .external-arrow {
        color: #2b6cb0;
        transform: translate(1px, -1px);
    }

    @media (max-width: 850px) {
        .resource-grid {
            grid-template-columns:
                repeat(2, minmax(0, 1fr));
        }
    }

    @media (max-width: 500px) {
        .resource-grid {
            grid-template-columns: 1fr;
        }
    }
</style>
"""


# =========================================================
# Page styling
# =========================================================

def apply_page_styles():
    st.markdown(
        dedent("""
        <style>
            .block-container {
                max-width: 1200px;
                padding-top: 2rem;
                padding-bottom: 3rem;
            }

            .resources-header {
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

            .resources-header-label {
                margin-bottom: 0.55rem;
                color: #b9cde5 !important;
                font-size: 0.72rem;
                font-weight: 700;
                letter-spacing: 0.1rem;
                text-transform: uppercase;
            }

            .resources-header-title {
                margin: 0;
                color: #ffffff !important;
                -webkit-text-fill-color: #ffffff !important;
                font-size: 2.2rem;
                font-weight: 750;
                line-height: 1.2;
                letter-spacing: -0.05rem;
            }

            .resources-header-description {
                max-width: 780px;
                margin: 0.8rem 0 0 0;
                color: #d8e4f2 !important;
                -webkit-text-fill-color: #d8e4f2 !important;
                font-size: 0.97rem;
                line-height: 1.65;
            }

            .resource-stat-card {
                min-height: 96px;
                padding: 1rem 1.1rem;
                background-color: #ffffff;
                border: 1px solid #dce3ec;
                border-radius: 0.75rem;
                box-shadow:
                    0 2px 8px
                    rgba(16, 37, 66, 0.04);
            }

            .resource-stat-label {
                margin-bottom: 0.35rem;
                color: #718096;
                font-size: 0.75rem;
                font-weight: 650;
                letter-spacing: 0.025rem;
                text-transform: uppercase;
            }

            .resource-stat-value {
                color: #102542;
                font-size: 1.45rem;
                font-weight: 750;
            }

            .filter-section {
                margin-top: 1.5rem;
                margin-bottom: 1.4rem;
            }

            .filter-heading {
                margin-bottom: 0.2rem;
                color: #102542;
                font-size: 1.2rem;
                font-weight: 750;
            }

            .filter-description {
                margin-bottom: 0.8rem;
                color: #64748b;
                font-size: 0.85rem;
                line-height: 1.5;
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

            .category-heading-row {
                margin-top: 1.8rem;
                margin-bottom: 0.8rem;
                display: flex;
                align-items: flex-end;
                justify-content: space-between;
                gap: 1rem;
            }

            .category-title {
                color: #102542;
                font-size: 1.3rem;
                font-weight: 750;
                letter-spacing: -0.02rem;
            }

            .category-description {
                max-width: 720px;
                margin-top: 0.25rem;
                color: #64748b;
                font-size: 0.84rem;
                line-height: 1.5;
            }

            .category-count {
                flex-shrink: 0;
                padding: 0.35rem 0.6rem;
                background-color: #e8eff8;
                border: 1px solid #cbd8e7;
                border-radius: 999px;
                color: #365574;
                font-size: 0.72rem;
                font-weight: 700;
            }

            .empty-state {
                margin-top: 1.5rem;
                padding: 2.2rem 1.5rem;
                background-color: #f7fafd;
                border: 1px dashed #bdcada;
                border-radius: 0.8rem;
                text-align: center;
            }

            .empty-state-title {
                margin-bottom: 0.35rem;
                color: #102542;
                font-size: 1rem;
                font-weight: 700;
            }

            .empty-state-description {
                color: #64748b;
                font-size: 0.85rem;
            }

            .resources-callout {
                margin-top: 2rem;
                padding: 1.1rem 1.2rem;
                display: flex;
                align-items: center;
                justify-content: space-between;
                gap: 1.2rem;
                background:
                    linear-gradient(
                        135deg,
                        #f7fafd 0%,
                        #edf3fa 100%
                    );
                border: 1px solid #cfdae8;
                border-left: 4px solid #2b6cb0;
                border-radius: 0.7rem;
            }

            .resources-callout-title {
                margin-bottom: 0.25rem;
                color: #102542;
                font-size: 0.92rem;
                font-weight: 750;
            }

            .resources-callout-text {
                color: #5f7084;
                font-size: 0.82rem;
                line-height: 1.5;
            }

            .resources-notice {
                margin-top: 1rem;
                color: #7a8798;
                font-size: 0.74rem;
                line-height: 1.5;
            }

            @media (max-width: 700px) {
                .resources-header {
                    padding: 1.7rem;
                }

                .category-heading-row,
                .resources-callout {
                    align-items: flex-start;
                    flex-direction: column;
                }
            }
        </style>
        """),
        unsafe_allow_html=True,
)


# =========================================================
# Main page
# =========================================================

def run():
    apply_page_styles()

    total_resources = sum(
        len(sites)
        for sites in CATEGORIES.values()
    )

    st.markdown(
        dedent("""
        <div class="resources-header">
            <div class="resources-header-label">
                Research Directory
            </div>

            <div class="resources-header-title">
                Trusted Resources
            </div>

            <div class="resources-header-description">
                Browse financial news, market research, investment firms,
                regulatory agencies, and educational tools. Select any
                resource to open its official website in a new tab.
            </div>
        </div>
        """),
        unsafe_allow_html=True,
)

    metric_col1, metric_col2, metric_col3 = st.columns(3)

    with metric_col1:
        st.markdown(
            dedent(f"""
            <div class="resource-stat-card">
                <div class="resource-stat-label">
                    Resources
                </div>
                <div class="resource-stat-value">
                    {total_resources}
                </div>
            </div>
            """),
            unsafe_allow_html=True,
)

    with metric_col2:
        st.markdown(
            dedent(f"""
            <div class="resource-stat-card">
                <div class="resource-stat-label">
                    Categories
                </div>
                <div class="resource-stat-value">
                    {len(CATEGORIES)}
                </div>
            </div>
            """),
            unsafe_allow_html=True,
)

    with metric_col3:
        st.markdown(
            dedent("""
            <div class="resource-stat-card">
                <div class="resource-stat-label">
                    Link Behavior
                </div>
                <div class="resource-stat-value">
                    New Tab
                </div>
            </div>
            """),
            unsafe_allow_html=True,
)

    st.markdown(
        dedent("""
        <div class="filter-section">
            <div class="filter-heading">
                Find a resource
            </div>
            <div class="filter-description">
                Search by company, organization, category, or website domain.
            </div>
        </div>
        """),
        unsafe_allow_html=True,
)

    search_col, category_col = st.columns([2, 1])

    with search_col:
        search_term = st.text_input(
            "Search resources",
            placeholder="Example: SEC, research, Bloomberg...",
            label_visibility="collapsed",
        )

    with category_col:
        selected_category = st.selectbox(
            "Filter by category",
            options=[
                "All Categories",
                *CATEGORIES.keys(),
            ],
            label_visibility="collapsed",
        )

    filtered_categories = filter_resources(
        search_term,
        selected_category,
    )

    matching_resource_count = sum(
        len(sites)
        for sites in filtered_categories.values()
    )

    if search_term or selected_category != "All Categories":
        st.caption(
            f"Showing {matching_resource_count} matching "
            f"resource{'s' if matching_resource_count != 1 else ''}."
        )

    if not filtered_categories:
        st.markdown(
            dedent("""
            <div class="empty-state">
                <div class="empty-state-title">
                    No resources found
                </div>
                <div class="empty-state-description">
                    Try a different company name, category, or website domain.
                </div>
            </div>
            """),
            unsafe_allow_html=True,
)

    else:
        for category, sites in filtered_categories.items():
            render_resource_category(
                category,
                sites,
            )

    st.markdown(
        dedent("""
        <div class="resources-callout">
            <div>
                <div class="resources-callout-title">
                    Missing a useful resource?
                </div>

                <div class="resources-callout-text">
                    Submit a request and include the website name, URL,
                    and the category where it should appear.
                </div>
            </div>
        </div>

        <div class="resources-notice">
            External websites are maintained by their respective owners.
            FidSync does not control their content, availability, accuracy,
            or privacy practices.
        </div>
        """),
        unsafe_allow_html=True,
)
