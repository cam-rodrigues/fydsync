import streamlit as st
import streamlit.components.v1 as components

def run():
    # ── Page setup ────────────────────────────────────────────────────────────
    st.set_page_config(page_title="Resources", layout="wide")

    # Reduce the large default gap above st.title()
    st.markdown(
        """
        <style>
            /* Trim top padding under the navbar / header */
            section.main > div {
                padding-top: 1rem !important;   /* tighter: adjust as you like */
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    # ── Heading & intro ───────────────────────────────────────────────────────
    st.title("Resources")
    st.markdown("Click any logo to open the site in a new tab.")

    # ── Trusted-site categories ───────────────────────────────────────────────
    categories = {
        "Financial News": [
            {"name": "Bloomberg", "url": "https://www.bloomberg.com", "logo": "https://logo.clearbit.com/bloomberg.com"},
            {"name": "Yahoo Finance", "url": "https://finance.yahoo.com", "logo": "https://logo.clearbit.com/yahoo.com"},
            {"name": "CNBC", "url": "https://www.cnbc.com", "logo": "https://logo.clearbit.com/cnbc.com"},
            {"name": "MarketWatch", "url": "https://www.marketwatch.com", "logo": "https://logo.clearbit.com/marketwatch.com"},
            {"name": "Barron's", "url": "https://www.barrons.com", "logo": "https://logo.clearbit.com/barrons.com"},
            {"name": "Reuters", "url": "https://www.reuters.com/finance", "logo": "https://logo.clearbit.com/reuters.com"},
            {"name": "The Wall Street Journal", "url": "https://www.wsj.com", "logo": "https://logo.clearbit.com/wsj.com"},
            {"name": "Forbes", "url": "https://www.forbes.com", "logo": "https://logo.clearbit.com/forbes.com"},
            {"name": "Financial Times", "url": "https://www.ft.com", "logo": "https://logo.clearbit.com/ft.com"},
        ],
        "Market Data & Research": [
            {"name": "Morningstar", "url": "https://www.morningstar.com", "logo": "https://logo.clearbit.com/morningstar.com"},
            {"name": "TradingView", "url": "https://www.tradingview.com", "logo": "https://logo.clearbit.com/tradingview.com"},
            {"name": "Seeking Alpha", "url": "https://seekingalpha.com", "logo": "https://logo.clearbit.com/seekingalpha.com"},
            {"name": "Zacks", "url": "https://www.zacks.com", "logo": "https://logo.clearbit.com/zacks.com"},
            {"name": "Finviz", "url": "https://finviz.com", "logo": "https://logo.clearbit.com/finviz.com"},
            {"name": "Barchart", "url": "https://www.barchart.com", "logo": "https://logo.clearbit.com/barchart.com"},
            {"name": "YCharts", "url": "https://ycharts.com", "logo": "https://logo.clearbit.com/ycharts.com"},
            {"name": "MacroTrends", "url": "https://www.macrotrends.net", "logo": "https://logo.clearbit.com/macrotrends.net"},
        ],
        "Investment Firms": [
            {"name": "Fidelity", "url": "https://www.fidelity.com", "logo": "https://logo.clearbit.com/fidelity.com"},
            {"name": "Vanguard", "url": "https://investor.vanguard.com", "logo": "https://logo.clearbit.com/vanguard.com"},
            {"name": "Charles Schwab", "url": "https://www.schwab.com", "logo": "https://logo.clearbit.com/schwab.com"},
            {"name": "TD Ameritrade", "url": "https://www.tdameritrade.com", "logo": "https://logo.clearbit.com/tdameritrade.com"},
            {"name": "J.P. Morgan", "url": "https://www.jpmorgan.com", "logo": "https://logo.clearbit.com/jpmorgan.com"},
            {"name": "Envestnet", "url": "https://www.envestnet.com", "logo": "https://logo.clearbit.com/envestnet.com"},
            {"name": "T. Rowe Price", "url": "https://www.troweprice.com", "logo": "https://logo.clearbit.com/troweprice.com"},
            {"name": "Edward Jones", "url": "https://www.edwardjones.com", "logo": "https://logo.clearbit.com/edwardjones.com"},
        ],
        "Government & Regulatory": [
            {"name": "SEC", "url": "https://www.sec.gov", "logo": "https://logo.clearbit.com/sec.gov"},
            {"name": "FINRA", "url": "https://www.finra.org", "logo": "https://logo.clearbit.com/finra.org"},
            {"name": "FDIC", "url": "https://www.fdic.gov", "logo": "https://logo.clearbit.com/fdic.gov"},
            {"name": "Federal Reserve", "url": "https://www.federalreserve.gov", "logo": "https://logo.clearbit.com/federalreserve.gov"},
            {"name": "CFPB", "url": "https://www.consumerfinance.gov", "logo": "https://logo.clearbit.com/consumerfinance.gov"},
            {"name": "IRS", "url": "https://www.irs.gov", "logo": "https://logo.clearbit.com/irs.gov"},
        ],
        "Education & Tools": [
            {"name": "Investopedia", "url": "https://www.investopedia.com", "logo": "https://logo.clearbit.com/investopedia.com"},
            {"name": "NerdWallet", "url": "https://www.nerdwallet.com", "logo": "https://logo.clearbit.com/nerdwallet.com"},
            {"name": "eMoney", "url": "https://emoneyadvisor.com", "logo": "https://logo.clearbit.com/emoneyadvisor.com"},
            {"name": "Khan Academy", "url": "https://www.khanacademy.org/economics-finance-domain", "logo": "https://logo.clearbit.com/khanacademy.org"},
            {"name": "SmartAsset", "url": "https://smartasset.com", "logo": "https://logo.clearbit.com/smartasset.com"},
            {"name": "Bankrate", "url": "https://www.bankrate.com", "logo": "https://logo.clearbit.com/bankrate.com"},
            {"name": "Mint", "url": "https://mint.intuit.com", "logo": "https://logo.clearbit.com/mint.intuit.com"},
        ],
    }

    # ── Shared CSS for grids and cards ───────────────────────────────────────
    css = """
    <style>
        .logo-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
            gap: 1.25rem;
            margin-bottom: 1.5rem;
        }
        .logo-box {
            background: #f0f4fa;
            border: 1px solid #cbd5e1;
            border-radius: 0.75rem;
            padding: 0.75rem;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: transform 0.2s ease, border-color 0.2s;
            box-shadow: 0 1px 2px rgba(0,0,0,0.03);
            height: 85px;
        }
        .logo-box:hover {
            transform: scale(1.06);
            border-color: #1c2e4a;
            cursor: pointer;
        }
        .logo-box img {
            max-width: 80%;
            max-height: 60px;
            height: auto;
        }
        .divider {
            border: none;
            border-top: 1px solid #d6e2ee;
            margin: 1.5rem 0 2rem 0;
        }
    </style>
    """

    # ── Render each category ────────────────────────────────────────────────
    for i, (category, sites) in enumerate(categories.items()):
        st.markdown(f"### {category}")

        # build the grid HTML
        html_block = css + '<div class="logo-grid">'
        for site in sites:
            html_block += (
                f'<a href="{site["url"]}" target="_blank" class="logo-box">'
                f'  <img src="{site["logo"]}" alt="{site["name"]} logo" title="{site["name"]}">'
                f'</a>'
            )
        html_block += '</div>'

        # dynamic height calculation (tweak row/offset as needed)
        rows = (len(sites) + 3) // 4
        height = 200 + rows * 110
        components.html(html_block, height=height, scrolling=False)

        if i < len(categories) - 1:
            st.markdown('<hr class="divider">', unsafe_allow_html=True)

    # ── Bottom callout ──────────────────────────────────────────────────────
    st.markdown(
        """
        <div style="margin-top: 2rem; padding: 1.2rem; background-color: #f9fbfe;
                    border: 1px solid #d6e2ee; border-radius: 0.5rem; font-size: 0.93rem;">
            Looking for a site that’s not listed here?
            <br>Please submit a <strong>user request</strong> and we’ll add it to the trusted resources.
        </div>
        """,
        unsafe_allow_html=True,
    )
