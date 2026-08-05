import html
from urllib.parse import quote

import streamlit as st


def get_logo_url(website_url):
    """Generate a favicon URL for a website."""
    encoded_url = quote(website_url, safe="")

    return (
        "https://www.google.com/s2/favicons"
        f"?domain_url={encoded_url}&sz=128"
    )


def run():
    # Remove this if set_page_config() is already called
    # in your main Streamlit file.
    st.set_page_config(
        page_title="Resources",
        page_icon="🔗",
        layout="wide",
    )

    # -------------------------------------------------------------------------
    # Resources
    # -------------------------------------------------------------------------
    categories = {
        "Financial News": [
            {
                "name": "Bloomberg",
                "url": "https://www.bloomberg.com",
            },
            {
                "name": "Yahoo Finance",
                "url": "https://finance.yahoo.com",
            },
            {
                "name": "CNBC",
                "url": "https://www.cnbc.com",
            },
            {
                "name": "MarketWatch",
                "url": "https://www.marketwatch.com",
            },
            {
                "name": "Barron's",
                "url": "https://www.barrons.com",
            },
            {
                "name": "Reuters",
                "url": "https://www.reuters.com/finance",
            },
            {
                "name": "The Wall Street Journal",
                "url": "https://www.wsj.com",
            },
            {
                "name": "Forbes",
                "url": "https://www.forbes.com",
            },
            {
                "name": "Financial Times",
                "url": "https://www.ft.com",
            },
        ],

        "Market Data & Research": [
            {
                "name": "Morningstar",
                "url": "https://www.morningstar.com",
            },
            {
                "name": "TradingView",
                "url": "https://www.tradingview.com",
            },
            {
                "name": "Seeking Alpha",
                "url": "https://seekingalpha.com",
            },
            {
                "name": "Zacks",
                "url": "https://www.zacks.com",
            },
            {
                "name": "Finviz",
                "url": "https://finviz.com",
            },
            {
                "name": "Barchart",
                "url": "https://www.barchart.com",
            },
            {
                "name": "YCharts",
                "url": "https://ycharts.com",
            },
            {
                "name": "Macrotrends",
                "url": "https://www.macrotrends.net",
            },
        ],

        "Investment Firms": [
            {
                "name": "Fidelity",
                "url": "https://www.fidelity.com",
            },
            {
                "name": "Vanguard",
                "url": "https://investor.vanguard.com",
            },
            {
                "name": "Charles Schwab",
                "url": "https://www.schwab.com",
            },
            {
                "name": "J.P. Morgan",
                "url": "https://www.jpmorgan.com",
            },
            {
                "name": "Envestnet",
                "url": "https://www.envestnet.com",
            },
            {
                "name": "T. Rowe Price",
                "url": "https://www.troweprice.com",
            },
            {
                "name": "Edward Jones",
                "url": "https://www.edwardjones.com",
            },
        ],

        "Government & Regulatory": [
            {
                "name": "SEC",
                "url": "https://www.sec.gov",
            },
            {
                "name": "FINRA",
                "url": "https://www.finra.org",
            },
            {
                "name": "FDIC",
                "url": "https://www.fdic.gov",
            },
            {
                "name": "Federal Reserve",
                "url": "https://www.federalreserve.gov",
            },
            {
                "name": "CFPB",
                "url": "https://www.consumerfinance.gov",
            },
            {
                "name": "IRS",
                "url": "https://www.irs.gov",
            },
        ],

        "Education & Tools": [
            {
                "name": "Investopedia",
                "url": "https://www.investopedia.com",
            },
            {
                "name": "NerdWallet",
                "url": "https://www.nerdwallet.com",
            },
            {
                "name": "eMoney",
                "url": "https://emoneyadvisor.com",
            },
            {
                "name": "Khan Academy",
                "url": (
                    "https://www.khanacademy.org/"
                    "economics-finance-domain"
                ),
            },
            {
                "name": "SmartAsset",
                "url": "https://smartasset.com",
            },
            {
                "name": "Bankrate",
                "url": "https://www.bankrate.com",
            },
        ],
    }

    # -------------------------------------------------------------------------
    # Page styling
    # -------------------------------------------------------------------------
    st.html(
        """
        <style>
            /* Main page spacing */
            .stMainBlockContainer {
                max-width: 1500px;
                padding-top: 1.4rem;
                padding-bottom: 3rem;
            }

            /* Header */
            .resources-eyebrow {
                color: #58708e;
                font-size: 0.7rem;
                font-weight: 750;
                letter-spacing: 0.13em;
                margin-bottom: 0.45rem;
                text-transform: uppercase;
            }

            .resources-title {
                color: #102d50;
                font-size: clamp(2.1rem, 4vw, 3rem);
                font-weight: 750;
                letter-spacing: -0.04em;
                line-height: 1.05;
                margin: 0;
            }

            .resources-description {
                color: #65788e;
                font-size: 0.95rem;
                line-height: 1.65;
                margin: 0.75rem 0 1.8rem;
                max-width: 700px;
            }

            /* Search field */
            div[data-testid="stTextInput"] input {
                background: #f6f9fc;
                border: 1px solid #d4dfeb;
                border-radius: 10px;
                color: #173555;
                min-height: 42px;
            }

            div[data-testid="stTextInput"] input:focus {
                border-color: #7892ad;
                box-shadow: 0 0 0 1px #7892ad;
            }

            /* Category dropdown */
            div[data-testid="stSelectbox"] > div > div {
                background: #f6f9fc;
                border-color: #d4dfeb;
                border-radius: 10px;
                min-height: 42px;
            }

            /* Category sections */
            .resource-section {
                margin-top: 2.6rem;
            }

            .resource-section-header {
                align-items: center;
                display: flex;
                justify-content: space-between;
                margin-bottom: 1rem;
            }

            .resource-section-title {
                color: #102d50;
                font-size: 1rem;
                font-weight: 750;
                letter-spacing: -0.01em;
                margin: 0;
            }

            .resource-count {
                background: #eaf0f6;
                border-radius: 999px;
                color: #5d7188;
                font-size: 0.7rem;
                font-weight: 700;
                padding: 0.25rem 0.55rem;
            }

            /* Resource grid */
            .resource-grid {
                display: grid;
                gap: 0.85rem;
                grid-template-columns: repeat(
                    auto-fill,
                    minmax(165px, 1fr)
                );
            }

            /* Individual card */
            .resource-card {
                align-items: center;
                background: #ffffff;
                border: 1px solid #d7e1ec;
                border-radius: 13px;
                color: inherit;
                display: flex;
                flex-direction: column;
                justify-content: center;
                min-height: 135px;
                padding: 1.05rem 0.8rem 0.9rem;
                position: relative;
                text-align: center;
                text-decoration: none !important;
                transition:
                    border-color 160ms ease,
                    box-shadow 160ms ease,
                    transform 160ms ease;
            }

            .resource-card:hover {
                border-color: #879fba;
                box-shadow: 0 8px 22px rgba(28, 54, 82, 0.10);
                transform: translateY(-3px);
            }

            /* Logo container */
            .resource-logo-area {
                align-items: center;
                display: flex;
                height: 58px;
                justify-content: center;
                margin-bottom: 0.55rem;
                width: 100%;
            }

            /* Square favicon */
            .resource-logo {
                display: block;
                height: 46px;
                object-fit: contain;
                width: 46px;
            }

            /* Website name */
            .resource-name {
                color: #173555;
                font-size: 0.82rem;
                font-weight: 700;
                line-height: 1.3;
            }

            /* External-link arrow */
            .resource-arrow {
                color: #98a9bb;
                font-size: 0.75rem;
                position: absolute;
                right: 0.65rem;
                top: 0.55rem;
                transition:
                    color 160ms ease,
                    transform 160ms ease;
            }

            .resource-card:hover .resource-arrow {
                color: #173555;
                transform: translate(2px, -2px);
            }

            /* Empty search result */
            .resource-empty {
                background: #f7f9fc;
                border: 1px dashed #bdcad8;
                border-radius: 13px;
                color: #65788e;
                margin-top: 2rem;
                padding: 2.5rem 1rem;
                text-align: center;
            }

            /* Bottom request box */
            .resource-request {
                align-items: center;
                background: #f4f7fb;
                border: 1px solid #d9e2ec;
                border-radius: 13px;
                display: flex;
                gap: 1rem;
                justify-content: space-between;
                margin-top: 2.75rem;
                padding: 1.15rem 1.3rem;
            }

            .resource-request-title {
                color: #173555;
                font-size: 0.9rem;
                font-weight: 750;
                margin-bottom: 0.2rem;
            }

            .resource-request-text {
                color: #6a7c90;
                font-size: 0.8rem;
                line-height: 1.5;
            }

            .resource-request-icon {
                align-items: center;
                background: #ffffff;
                border: 1px solid #d8e2ec;
                border-radius: 10px;
                color: #526b85;
                display: flex;
                flex: 0 0 38px;
                font-size: 1rem;
                height: 38px;
                justify-content: center;
            }

            /* Mobile layout */
            @media (max-width: 700px) {
                .resource-grid {
                    grid-template-columns: repeat(
                        2,
                        minmax(0, 1fr)
                    );
                }

                .resource-card {
                    min-height: 125px;
                }

                .resource-logo {
                    height: 40px;
                    width: 40px;
                }

                .resource-request {
                    align-items: flex-start;
                }
            }
        </style>
        """
    )

    # -------------------------------------------------------------------------
    # Header
    # -------------------------------------------------------------------------
    st.html(
        """
        <div class="resources-eyebrow">
            Trusted links
        </div>

        <h1 class="resources-title">
            Resources
        </h1>

        <p class="resources-description">
            A curated collection of financial news, market research,
            investment, regulatory, and educational resources.
        </p>
        """
    )

    # -------------------------------------------------------------------------
    # Search and filter controls
    # -------------------------------------------------------------------------
    search_column, category_column = st.columns(
        [2, 1],
        gap="medium",
    )

    with search_column:
        search_query = st.text_input(
            "Search resources",
            placeholder="Search by website name...",
            label_visibility="collapsed",
        )

    with category_column:
        selected_category = st.selectbox(
            "Filter resources by category",
            options=[
                "All categories",
                *categories.keys(),
            ],
            label_visibility="collapsed",
        )

    normalized_query = search_query.strip().lower()

    # -------------------------------------------------------------------------
    # Filter resources
    # -------------------------------------------------------------------------
    visible_categories = {}

    for category, sites in categories.items():
        if (
            selected_category != "All categories"
            and category != selected_category
        ):
            continue

        filtered_sites = []

        for site in sites:
            matches_name = (
                normalized_query in site["name"].lower()
            )

            matches_category = (
                normalized_query in category.lower()
            )

            if (
                not normalized_query
                or matches_name
                or matches_category
            ):
                filtered_sites.append(site)

        if filtered_sites:
            visible_categories[category] = filtered_sites

    # -------------------------------------------------------------------------
    # Render resources
    # -------------------------------------------------------------------------
    if not visible_categories:
        st.html(
            """
            <div class="resource-empty">
                No resources match that search.
                Try another website name or category.
            </div>
            """
        )

    else:
        sections_html = ""

        for category, sites in visible_categories.items():
            cards_html = ""

            for site in sites:
                site_name = html.escape(site["name"])

                site_url = html.escape(
                    site["url"],
                    quote=True,
                )

                logo_url = html.escape(
                    get_logo_url(site["url"]),
                    quote=True,
                )

                cards_html += f"""
                    <a
                        class="resource-card"
                        href="{site_url}"
                        target="_blank"
                        rel="noopener noreferrer"
                        aria-label="Open {site_name}"
                    >
                        <span class="resource-arrow">
                            ↗
                        </span>

                        <div class="resource-logo-area">
                            <img
                                class="resource-logo"
                                src="{logo_url}"
                                alt="{site_name} icon"
                                loading="lazy"
                            >
                        </div>

                        <span class="resource-name">
                            {site_name}
                        </span>
                    </a>
                """

            category_name = html.escape(category)

            sections_html += f"""
                <section class="resource-section">
                    <div class="resource-section-header">
                        <h2 class="resource-section-title">
                            {category_name}
                        </h2>

                        <span class="resource-count">
                            {len(sites)}
                        </span>
                    </div>

                    <div class="resource-grid">
                        {cards_html}
                    </div>
                </section>
            """

        st.html(sections_html)

    # -------------------------------------------------------------------------
    # Bottom callout
    # -------------------------------------------------------------------------
    st.html(
        """
        <div class="resource-request">
            <div>
                <div class="resource-request-title">
                    Missing a trusted resource?
                </div>

                <div class="resource-request-text">
                    Submit a user request and the site can be
                    reviewed for inclusion.
                </div>
            </div>

            <div class="resource-request-icon">
                ＋
            </div>
        </div>
        """
    )


# Use this only if this file is run directly.
if __name__ == "__main__":
    run()
