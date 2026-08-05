import html
import streamlit as st


def run():
    # Remove this line if set_page_config() is already called
    # in your app's main entry file.
    st.set_page_config(
        page_title="Resources",
        page_icon="🔗",
        layout="wide",
    )

    # -------------------------------------------------------------------------
    # Resource data
    # -------------------------------------------------------------------------
    categories = {
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
                "name": "Macrotrends",
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
                padding-top: 1.5rem;
                padding-bottom: 3rem;
            }

            /* Page heading */
            .resources-eyebrow {
                color: #64748b;
                font-size: 0.75rem;
                font-weight: 700;
                letter-spacing: 0.11em;
                margin-bottom: 0.35rem;
                text-transform: uppercase;
            }

            .resources-title {
                color: #172a46;
                font-size: clamp(2rem, 4vw, 3rem);
                font-weight: 750;
                letter-spacing: -0.04em;
                line-height: 1.05;
                margin: 0;
            }

            .resources-description {
                color: #64748b;
                font-size: 1rem;
                line-height: 1.6;
                margin: 0.7rem 0 1.75rem;
                max-width: 680px;
            }

            /* Streamlit input styling */
            div[data-testid="stTextInput"] input {
                border: 1px solid #d8e1eb;
                border-radius: 10px;
            }

            div[data-testid="stSelectbox"] > div > div {
                border-radius: 10px;
            }

            /* Category sections */
            .resource-section {
                margin-top: 2.2rem;
            }

            .resource-section-header {
                align-items: center;
                display: flex;
                justify-content: space-between;
                margin-bottom: 0.9rem;
            }

            .resource-section-title {
                color: #20334f;
                font-size: 1.08rem;
                font-weight: 700;
                letter-spacing: -0.015em;
                margin: 0;
            }

            .resource-count {
                background: #eef3f8;
                border-radius: 999px;
                color: #65758a;
                font-size: 0.72rem;
                font-weight: 650;
                padding: 0.25rem 0.55rem;
            }

            /* Card grid */
            .resource-grid {
                display: grid;
                gap: 0.9rem;
                grid-template-columns: repeat(
                    auto-fill,
                    minmax(175px, 1fr)
                );
            }

            .resource-card {
                align-items: center;
                background: #ffffff;
                border: 1px solid #dce4ed;
                border-radius: 14px;
                color: inherit;
                display: flex;
                flex-direction: column;
                min-height: 142px;
                padding: 1.15rem 0.9rem 0.95rem;
                position: relative;
                text-align: center;
                text-decoration: none !important;
                transition:
                    border-color 160ms ease,
                    box-shadow 160ms ease,
                    transform 160ms ease;
            }

            .resource-card:hover {
                border-color: #8da4be;
                box-shadow: 0 10px 25px rgba(31, 51, 75, 0.10);
                transform: translateY(-3px);
            }

            .resource-logo-area {
                align-items: center;
                display: flex;
                height: 66px;
                justify-content: center;
                margin-bottom: 0.65rem;
                width: 100%;
            }

            .resource-logo {
                display: block;
                max-height: 48px;
                max-width: 118px;
                object-fit: contain;
            }

            .resource-name {
                color: #273950;
                font-size: 0.86rem;
                font-weight: 650;
                line-height: 1.25;
            }

            .resource-arrow {
                color: #8fa0b3;
                font-size: 0.8rem;
                position: absolute;
                right: 0.7rem;
                top: 0.55rem;
                transition:
                    color 160ms ease,
                    transform 160ms ease;
            }

            .resource-card:hover .resource-arrow {
                color: #273950;
                transform: translate(2px, -2px);
            }

            /* Empty search state */
            .resource-empty {
                background: #f8fafc;
                border: 1px dashed #cbd5e1;
                border-radius: 14px;
                color: #64748b;
                padding: 2.5rem 1rem;
                text-align: center;
            }

            /* Bottom request card */
            .resource-request {
                align-items: center;
                background: #f5f8fc;
                border: 1px solid #dce5ef;
                border-radius: 14px;
                display: flex;
                gap: 0.9rem;
                justify-content: space-between;
                margin-top: 2.5rem;
                padding: 1.1rem 1.25rem;
            }

            .resource-request-title {
                color: #273950;
                font-size: 0.92rem;
                font-weight: 700;
                margin-bottom: 0.2rem;
            }

            .resource-request-text {
                color: #69798c;
                font-size: 0.82rem;
                line-height: 1.45;
            }

            .resource-request-icon {
                align-items: center;
                background: #ffffff;
                border: 1px solid #dce5ef;
                border-radius: 10px;
                color: #536b85;
                display: flex;
                flex: 0 0 38px;
                font-size: 1rem;
                height: 38px;
                justify-content: center;
            }

            @media (max-width: 640px) {
                .resource-grid {
                    grid-template-columns: repeat(2, minmax(0, 1fr));
                }

                .resource-card {
                    min-height: 128px;
                    padding-left: 0.6rem;
                    padding-right: 0.6rem;
                }

                .resource-logo {
                    max-width: 95px;
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
        <div class="resources-eyebrow">Trusted links</div>
        <h1 class="resources-title">Resources</h1>
        <p class="resources-description">
            A curated collection of financial news, market research,
            investment, regulatory, and educational resources.
        </p>
        """
    )

    # -------------------------------------------------------------------------
    # Search and category filters
    # -------------------------------------------------------------------------
    search_column, category_column = st.columns([2, 1], gap="medium")

    with search_column:
        search_query = st.text_input(
            "Search resources",
            placeholder="Search by website name...",
            label_visibility="collapsed",
        )

    with category_column:
        selected_category = st.selectbox(
            "Filter by category",
            options=["All categories", *categories.keys()],
            label_visibility="collapsed",
        )

    normalized_query = search_query.strip().lower()

    # -------------------------------------------------------------------------
    # Build the filtered resource list
    # -------------------------------------------------------------------------
    visible_categories = {}

    for category, sites in categories.items():
        if (
            selected_category != "All categories"
            and category != selected_category
        ):
            continue

        filtered_sites = [
            site
            for site in sites
            if not normalized_query
            or normalized_query in site["name"].lower()
            or normalized_query in category.lower()
        ]

        if filtered_sites:
            visible_categories[category] = filtered_sites

    # -------------------------------------------------------------------------
    # Render cards
    # -------------------------------------------------------------------------
    if not visible_categories:
        st.html(
            """
            <div class="resource-empty">
                No resources match that search.
                Try a different website name or category.
            </div>
            """
        )
    else:
        sections_html = ""

        for category, sites in visible_categories.items():
            cards_html = ""

            for site in sites:
                site_name = html.escape(site["name"])
                site_url = html.escape(site["url"], quote=True)
                logo_url = html.escape(site["logo"], quote=True)

                cards_html += f"""
                    <a
                        class="resource-card"
                        href="{site_url}"
                        target="_blank"
                        rel="noopener noreferrer"
                        aria-label="Open {site_name}"
                    >
                        <span class="resource-arrow">↗</span>

                        <div class="resource-logo-area">
                            <img
                                class="resource-logo"
                                src="{logo_url}"
                                alt="{site_name} logo"
                                loading="lazy"
                            >
                        </div>

                        <span class="resource-name">
                            {site_name}
                        </span>
                    </a>
                """

            sections_html += f"""
                <section class="resource-section">
                    <div class="resource-section-header">
                        <h2 class="resource-section-title">
                            {html.escape(category)}
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
                    Submit a user request and the site can be reviewed
                    for inclusion.
                </div>
            </div>

            <div class="resource-request-icon">＋</div>
        </div>
        """
    )
