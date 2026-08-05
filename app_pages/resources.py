import html
import json
import math
from urllib.parse import quote

import streamlit as st
import streamlit.components.v1 as components


def get_logo_url(website_url):
    """Generate a Google favicon URL for a website."""
    encoded_url = quote(website_url, safe="")
    return (
        "https://www.google.com/s2/favicons"
        f"?domain_url={encoded_url}&sz=128"
    )


def run():
    # Remove this block if set_page_config() is already called
    # in your app's main entry file.
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
            {"name": "Bloomberg", "url": "https://www.bloomberg.com"},
            {"name": "Yahoo Finance", "url": "https://finance.yahoo.com"},
            {"name": "CNBC", "url": "https://www.cnbc.com"},
            {"name": "MarketWatch", "url": "https://www.marketwatch.com"},
            {"name": "Barron's", "url": "https://www.barrons.com"},
            {"name": "Reuters", "url": "https://www.reuters.com/finance"},
            {"name": "The Wall Street Journal", "url": "https://www.wsj.com"},
            {"name": "Forbes", "url": "https://www.forbes.com"},
            {"name": "Financial Times", "url": "https://www.ft.com"},
        ],
        "Market Data & Research": [
            {"name": "Morningstar", "url": "https://www.morningstar.com"},
            {"name": "TradingView", "url": "https://www.tradingview.com"},
            {"name": "Seeking Alpha", "url": "https://seekingalpha.com"},
            {"name": "Zacks", "url": "https://www.zacks.com"},
            {"name": "Finviz", "url": "https://finviz.com"},
            {"name": "Barchart", "url": "https://www.barchart.com"},
            {"name": "YCharts", "url": "https://ycharts.com"},
            {"name": "Macrotrends", "url": "https://www.macrotrends.net"},
        ],
        "Investment Firms": [
            {"name": "Fidelity", "url": "https://www.fidelity.com"},
            {"name": "Vanguard", "url": "https://investor.vanguard.com"},
            {"name": "Charles Schwab", "url": "https://www.schwab.com"},
            {"name": "J.P. Morgan", "url": "https://www.jpmorgan.com"},
            {"name": "Envestnet", "url": "https://www.envestnet.com"},
            {"name": "T. Rowe Price", "url": "https://www.troweprice.com"},
            {"name": "Edward Jones", "url": "https://www.edwardjones.com"},
        ],
        "Government & Regulatory": [
            {"name": "SEC", "url": "https://www.sec.gov"},
            {"name": "FINRA", "url": "https://www.finra.org"},
            {"name": "FDIC", "url": "https://www.fdic.gov"},
            {
                "name": "Federal Reserve",
                "url": "https://www.federalreserve.gov",
            },
            {
                "name": "CFPB",
                "url": "https://www.consumerfinance.gov",
            },
            {"name": "IRS", "url": "https://www.irs.gov"},
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
            {"name": "eMoney", "url": "https://emoneyadvisor.com"},
            {
                "name": "Khan Academy",
                "url": (
                    "https://www.khanacademy.org/"
                    "economics-finance-domain"
                ),
            },
            {"name": "SmartAsset", "url": "https://smartasset.com"},
            {"name": "Bankrate", "url": "https://www.bankrate.com"},
        ],
    }

    # -------------------------------------------------------------------------
    # Easter-egg messages
    # -------------------------------------------------------------------------
    # Only sites listed here receive the joke loading screen.
    # All other cards open normally.
    easter_eggs = {
        "Bloomberg": {
            "title": "Loading Bloomberg...",
            "message": (
                "Just kidding.<br>"
                "It’s probably behind a paywall anyway."
            ),
            "delay": 1900,
        },
        "Yahoo Finance": {
            "title": "Opening Yahoo Finance...",
            "message": (
                "Still somehow everyone’s second monitor."
            ),
            "delay": 1500,
        },
        "MarketWatch": {
            "title": "Opening MarketWatch...",
            "message": (
                "Watching the markets so you don’t have to."
            ),
            "delay": 1500,
        },
        "Barron's": {
            "title": "Loading premium insights...",
            "message": (
                "And, quite possibly, a premium paywall."
            ),
            "delay": 1750,
        },
        "The Wall Street Journal": {
            "title": "Opening The Wall Street Journal...",
            "message": (
                "Hope you remembered your subscription."
            ),
            "delay": 1750,
        },
        "Morningstar": {
            "title": "Opening Morningstar...",
            "message": "Morning, star.",
            "delay": 1350,
        },
        "TradingView": {
            "title": "Opening TradingView...",
            "message": "Candles detected.",
            "delay": 1350,
        },
        "SEC": {
            "title": "Contacting the SEC...",
            "message": (
                "No insider trading while you’re here."
            ),
            "delay": 1650,
        },
        "IRS": {
            "title": "Opening the IRS...",
            "message": (
                "They’re probably looking for you too."
            ),
            "delay": 1650,
        },
    }

    # -------------------------------------------------------------------------
    # Streamlit page styling
    # -------------------------------------------------------------------------
    st.markdown(
        """
        <style>
            .stMainBlockContainer {
                max-width: 1500px;
                padding-top: 1.4rem;
                padding-bottom: 3rem;
            }

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

            div[data-testid="stSelectbox"] > div > div {
                background: #f6f9fc;
                border-color: #d4dfeb;
                border-radius: 10px;
                min-height: 42px;
            }

            iframe[title="streamlit.components.v1.html"] {
                border: 0;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # -------------------------------------------------------------------------
    # Header
    # -------------------------------------------------------------------------
    st.markdown(
        """
        <div class="resources-eyebrow">Trusted links</div>
        <h1 class="resources-title">Resources</h1>
        <p class="resources-description">
            A curated collection of financial news, market research,
            investment, regulatory, and educational resources.
        </p>
        """,
        unsafe_allow_html=True,
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
            "Filter resources by category",
            options=["All categories", *categories.keys()],
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

        filtered_sites = [
            site
            for site in sites
            if (
                not normalized_query
                or normalized_query in site["name"].lower()
                or normalized_query in category.lower()
            )
        ]

        if filtered_sites:
            visible_categories[category] = filtered_sites

    # -------------------------------------------------------------------------
    # Render resource cards
    # -------------------------------------------------------------------------
    if not visible_categories:
        st.markdown(
            """
            <div style="
                background:#f7f9fc;
                border:1px dashed #bdcad8;
                border-radius:13px;
                color:#65788e;
                margin-top:2rem;
                padding:2.5rem 1rem;
                text-align:center;
            ">
                No resources match that search.
                Try another website name or category.
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    sections_html = ""

    for category, sites in visible_categories.items():
        cards_html = ""

        for site in sites:
            site_name = html.escape(site["name"])
            site_url = html.escape(site["url"], quote=True)
            logo_url = html.escape(
                get_logo_url(site["url"]),
                quote=True,
            )

            easter_egg = easter_eggs.get(site["name"])

            if easter_egg:
                title_json = html.escape(
                    json.dumps(easter_egg["title"]),
                    quote=True,
                )
                message_json = html.escape(
                    json.dumps(easter_egg["message"]),
                    quote=True,
                )
                url_json = html.escape(
                    json.dumps(site["url"]),
                    quote=True,
                )

                click_handler = (
                    "event.preventDefault();"
                    f"openWithToast({url_json},"
                    f"{title_json},"
                    f"{message_json},"
                    f"{int(easter_egg['delay'])});"
                )

                card_attributes = (
                    'href="#" '
                    f'onclick="{click_handler}"'
                )
            else:
                card_attributes = (
                    f'href="{site_url}" '
                    'target="_blank" '
                    'rel="noopener noreferrer"'
                )

            cards_html += f"""
                <a
                    class="resource-card"
                    {card_attributes}
                    aria-label="Open {site_name}"
                >
                    <span class="resource-arrow">↗</span>

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

    component_html = f"""
    <!doctype html>
    <html lang="en">
    <head>
        <meta charset="utf-8">
        <meta
            name="viewport"
            content="width=device-width, initial-scale=1"
        >

        <style>
            * {{
                box-sizing: border-box;
            }}

            html,
            body {{
                margin: 0;
                padding: 0;
                background: transparent;
                color: #173555;
                font-family:
                    Inter,
                    ui-sans-serif,
                    system-ui,
                    -apple-system,
                    BlinkMacSystemFont,
                    "Segoe UI",
                    sans-serif;
            }}

            .resource-section {{
                margin-top: 2.6rem;
            }}

            .resource-section:first-child {{
                margin-top: 2.15rem;
            }}

            .resource-section-header {{
                align-items: center;
                display: flex;
                justify-content: space-between;
                margin-bottom: 1rem;
            }}

            .resource-section-title {{
                color: #102d50;
                font-size: 1rem;
                font-weight: 750;
                letter-spacing: -0.01em;
                margin: 0;
            }}

            .resource-count {{
                background: #eaf0f6;
                border-radius: 999px;
                color: #5d7188;
                font-size: 0.7rem;
                font-weight: 700;
                padding: 0.25rem 0.55rem;
            }}

            .resource-grid {{
                display: grid;
                gap: 0.85rem;
                grid-template-columns:
                    repeat(auto-fill, minmax(165px, 1fr));
            }}

            .resource-card {{
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
                text-decoration: none;
                transition:
                    border-color 160ms ease,
                    box-shadow 160ms ease,
                    transform 160ms ease;
            }}

            .resource-card:hover {{
                border-color: #879fba;
                box-shadow:
                    0 8px 22px rgba(28, 54, 82, 0.10);
                transform: translateY(-3px);
            }}

            .resource-card:focus-visible {{
                outline: 3px solid rgba(43, 108, 176, 0.25);
                outline-offset: 2px;
            }}

            .resource-logo-area {{
                align-items: center;
                display: flex;
                height: 58px;
                justify-content: center;
                margin-bottom: 0.55rem;
                width: 100%;
            }}

            .resource-logo {{
                display: block;
                height: 46px;
                object-fit: contain;
                width: 46px;
            }}

            .resource-name {{
                color: #173555;
                font-size: 0.82rem;
                font-weight: 700;
                line-height: 1.3;
            }}

            .resource-arrow {{
                color: #98a9bb;
                font-size: 0.75rem;
                position: absolute;
                right: 0.65rem;
                top: 0.55rem;
                transition:
                    color 160ms ease,
                    transform 160ms ease;
            }}

            .resource-card:hover .resource-arrow {{
                color: #173555;
                transform: translate(2px, -2px);
            }}

            .resource-request {{
                align-items: center;
                background: #f4f7fb;
                border: 1px solid #d9e2ec;
                border-radius: 13px;
                display: flex;
                gap: 1rem;
                justify-content: space-between;
                margin-top: 2.75rem;
                padding: 1.15rem 1.3rem;
            }}

            .resource-request-title {{
                color: #173555;
                font-size: 0.9rem;
                font-weight: 750;
                margin-bottom: 0.2rem;
            }}

            .resource-request-text {{
                color: #6a7c90;
                font-size: 0.8rem;
                line-height: 1.5;
            }}

            .resource-request-icon {{
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
            }}

            /* Toast overlay */
            .toast-backdrop {{
                align-items: flex-start;
                background: rgba(16, 37, 66, 0.08);
                display: flex;
                inset: 0;
                justify-content: flex-end;
                opacity: 0;
                padding: 1rem;
                pointer-events: none;
                position: fixed;
                transition: opacity 180ms ease;
                z-index: 9998;
            }}

            .toast-backdrop.visible {{
                opacity: 1;
            }}

            .resource-toast {{
                background: rgba(255, 255, 255, 0.98);
                border: 1px solid #d7e1ec;
                border-radius: 14px;
                box-shadow:
                    0 18px 50px rgba(16, 37, 66, 0.20);
                max-width: 360px;
                opacity: 0;
                overflow: hidden;
                transform: translateY(-10px);
                transition:
                    opacity 180ms ease,
                    transform 180ms ease;
                width: min(360px, calc(100vw - 2rem));
            }}

            .toast-backdrop.visible .resource-toast {{
                opacity: 1;
                transform: translateY(0);
            }}

            .toast-content {{
                padding: 1rem 1.05rem 0.95rem;
            }}

            .toast-label {{
                color: #73869a;
                font-size: 0.64rem;
                font-weight: 800;
                letter-spacing: 0.1em;
                margin-bottom: 0.4rem;
                text-transform: uppercase;
            }}

            .toast-title {{
                color: #102d50;
                font-size: 0.95rem;
                font-weight: 750;
                line-height: 1.35;
            }}

            .toast-message {{
                color: #64748b;
                font-size: 0.82rem;
                line-height: 1.5;
                margin-top: 0.35rem;
            }}

            .toast-progress-track {{
                background: #e8eef5;
                height: 4px;
                overflow: hidden;
            }}

            .toast-progress {{
                background:
                    linear-gradient(90deg, #315f91, #789fc8);
                height: 100%;
                transform: scaleX(0);
                transform-origin: left;
            }}

            @keyframes toast-progress {{
                from {{
                    transform: scaleX(0);
                }}
                to {{
                    transform: scaleX(1);
                }}
            }}

            @media (max-width: 700px) {{
                .resource-grid {{
                    grid-template-columns:
                        repeat(2, minmax(0, 1fr));
                }}

                .resource-card {{
                    min-height: 125px;
                }}

                .resource-logo {{
                    height: 40px;
                    width: 40px;
                }}

                .resource-request {{
                    align-items: flex-start;
                }}

                .toast-backdrop {{
                    justify-content: center;
                }}
            }}
        </style>
    </head>

    <body>
        <main>
            {sections_html}

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

                <div class="resource-request-icon">＋</div>
            </div>
        </main>

        <div
            class="toast-backdrop"
            id="toastBackdrop"
            aria-live="polite"
            aria-hidden="true"
        >
            <div class="resource-toast">
                <div class="toast-content">
                    <div class="toast-label">
                        FidSync field note
                    </div>

                    <div
                        class="toast-title"
                        id="toastTitle"
                    ></div>

                    <div
                        class="toast-message"
                        id="toastMessage"
                    ></div>
                </div>

                <div class="toast-progress-track">
                    <div
                        class="toast-progress"
                        id="toastProgress"
                    ></div>
                </div>
            </div>
        </div>

        <script>
            let activeToastTimer = null;

            function openWithToast(url, title, message, delay) {{
                /*
                 * Open a blank tab immediately while the click still counts
                 * as a user gesture. Browsers may block a delayed window.open().
                 */
                const destinationTab = window.open(
                    "about:blank",
                    "_blank"
                );

                const backdrop =
                    document.getElementById("toastBackdrop");
                const titleElement =
                    document.getElementById("toastTitle");
                const messageElement =
                    document.getElementById("toastMessage");
                const progressElement =
                    document.getElementById("toastProgress");

                if (activeToastTimer) {{
                    window.clearTimeout(activeToastTimer);
                }}

                titleElement.textContent = title;
                messageElement.innerHTML = message;

                progressElement.style.animation = "none";
                void progressElement.offsetWidth;
                progressElement.style.animation =
                    `toast-progress ${{delay}}ms linear forwards`;

                backdrop.classList.add("visible");
                backdrop.setAttribute("aria-hidden", "false");

                activeToastTimer = window.setTimeout(() => {{
                    backdrop.classList.remove("visible");
                    backdrop.setAttribute("aria-hidden", "true");

                    if (destinationTab) {{
                        destinationTab.location.href = url;
                    }} else {{
                        /*
                         * Fallback if the browser blocked the blank tab.
                         */
                        window.open(url, "_blank");
                    }}
                }}, delay);
            }}
        </script>
    </body>
    </html>
    """

    # A generous height prevents the embedded grid from being cut off.
    # It is based on an estimated five cards per row.
    total_height = 60

    for sites in visible_categories.values():
        estimated_rows = math.ceil(len(sites) / 5)
        total_height += 72 + (estimated_rows * 152)

    total_height += 140

    components.html(
        component_html,
        height=total_height,
        scrolling=False,
    )


if __name__ == "__main__":
    run()
