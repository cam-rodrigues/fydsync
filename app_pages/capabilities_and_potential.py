import streamlit as st


def run():
    st.markdown(
        """
        <style>
            /* ---------- Page layout ---------- */

            .capabilities-page {
                max-width: 1150px;
                margin: 0 auto;
                padding-bottom: 3rem;
            }

            /* ---------- Hero ---------- */

            .capabilities-hero {
                position: relative;
                overflow: hidden;
                padding: 2.4rem 2.6rem;
                margin-bottom: 1.5rem;
                background:
                    radial-gradient(
                        circle at top right,
                        rgba(115, 170, 133, 0.22),
                        transparent 35%
                    ),
                    linear-gradient(
                        135deg,
                        #18392b 0%,
                        #28533d 100%
                    );
                border: 1px solid #376047;
                border-radius: 1rem;
                box-shadow: 0 10px 30px rgba(24, 57, 43, 0.14);
            }

            .hero-label {
                margin-bottom: 0.65rem;
                color: #bfdbc8;
                font-size: 0.72rem;
                font-weight: 750;
                letter-spacing: 0.1rem;
                text-transform: uppercase;
            }

            .capabilities-hero h1 {
                margin: 0;
                color: white;
                font-size: 2.25rem;
                font-weight: 760;
                line-height: 1.15;
                letter-spacing: -0.055rem;
            }

            .capabilities-hero p {
                max-width: 780px;
                margin: 0.85rem 0 0 0;
                color: #deebe2;
                font-size: 0.98rem;
                line-height: 1.65;
            }

            /* ---------- Summary metrics ---------- */

            .summary-grid {
                display: grid;
                grid-template-columns: repeat(3, 1fr);
                gap: 1rem;
                margin-bottom: 2rem;
            }

            .summary-card {
                padding: 1.1rem 1.2rem;
                background: white;
                border: 1px solid #d8e4dc;
                border-radius: 0.75rem;
                box-shadow: 0 2px 8px rgba(24, 57, 43, 0.04);
            }

            .summary-number {
                color: #18392b;
                font-size: 1.65rem;
                font-weight: 800;
                line-height: 1;
            }

            .summary-label {
                margin-top: 0.45rem;
                color: #64748b;
                font-size: 0.78rem;
                font-weight: 600;
                letter-spacing: 0.02rem;
            }

            /* ---------- Section headings ---------- */

            .section-heading {
                margin: 2rem 0 0.25rem 0;
                color: #18392b;
                font-size: 1.35rem;
                font-weight: 750;
                letter-spacing: -0.025rem;
            }

            .section-description {
                margin: 0 0 1.15rem 0;
                color: #64748b;
                font-size: 0.9rem;
                line-height: 1.55;
            }

            /* ---------- Capability cards ---------- */

            .capability-grid {
                display: grid;
                grid-template-columns: repeat(2, minmax(0, 1fr));
                gap: 1rem;
                margin-bottom: 1.2rem;
            }

            .capability-card {
                min-height: 190px;
                padding: 1.25rem 1.3rem;
                background: white;
                border: 1px solid #d8e4dc;
                border-radius: 0.8rem;
                box-shadow: 0 3px 10px rgba(24, 57, 43, 0.045);
                transition:
                    transform 0.15s ease,
                    box-shadow 0.15s ease,
                    border-color 0.15s ease;
            }

            .capability-card:hover {
                transform: translateY(-2px);
                border-color: #a9c9b3;
                box-shadow: 0 8px 20px rgba(24, 57, 43, 0.08);
            }

            .card-header {
                display: flex;
                align-items: center;
                justify-content: space-between;
                gap: 0.75rem;
                margin-bottom: 0.75rem;
            }

            .capability-card h3 {
                margin: 0;
                color: #18392b;
                font-size: 1rem;
                font-weight: 720;
                line-height: 1.3;
            }

            .capability-card p {
                margin: 0;
                color: #64748b;
                font-size: 0.86rem;
                line-height: 1.6;
            }

            .card-category {
                margin-top: 1rem;
                color: #708078;
                font-size: 0.69rem;
                font-weight: 700;
                letter-spacing: 0.055rem;
                text-transform: uppercase;
            }

            /* ---------- Status badges ---------- */

            .status-badge {
                flex-shrink: 0;
                padding: 0.22rem 0.45rem;
                border-radius: 999px;
                font-size: 0.63rem;
                font-weight: 750;
                letter-spacing: 0.025rem;
                text-transform: uppercase;
                white-space: nowrap;
            }

            .status-live {
                background-color: #dcefe2;
                color: #26633d;
                border: 1px solid #b7dac2;
            }

            .status-development {
                background-color: #f5edcf;
                color: #735f16;
                border: 1px solid #e6d99f;
            }

            .status-future {
                background-color: #e9edf1;
                color: #53606d;
                border: 1px solid #d5dce3;
            }

            /* ---------- Roadmap ---------- */

            .roadmap {
                margin-top: 1rem;
                padding: 1.35rem 1.5rem;
                background: #f3f8f5;
                border: 1px solid #cfdfd4;
                border-radius: 0.8rem;
            }

            .roadmap-row {
                display: grid;
                grid-template-columns: 110px 1fr;
                gap: 1rem;
                padding: 0.9rem 0;
                border-bottom: 1px solid #dce8e0;
            }

            .roadmap-row:last-child {
                border-bottom: none;
            }

            .roadmap-phase {
                color: #3f7d5a;
                font-size: 0.75rem;
                font-weight: 750;
                letter-spacing: 0.04rem;
                text-transform: uppercase;
            }

            .roadmap-content strong {
                display: block;
                margin-bottom: 0.2rem;
                color: #18392b;
                font-size: 0.9rem;
            }

            .roadmap-content span {
                color: #64748b;
                font-size: 0.82rem;
                line-height: 1.5;
            }

            /* ---------- Disclaimer ---------- */

            .capability-notice {
                margin-top: 1.5rem;
                padding: 0.9rem 1rem;
                background-color: #edf6f0;
                border: 1px solid #c7ddce;
                border-left: 4px solid #3f7d5a;
                border-radius: 0.55rem;
                color: #526159;
                font-size: 0.82rem;
                line-height: 1.55;
            }

            /* ---------- Mobile ---------- */

            @media (max-width: 900px) {
                .summary-grid,
                .capability-grid {
                    grid-template-columns: 1fr;
                }

                .roadmap-row {
                    grid-template-columns: 1fr;
                    gap: 0.3rem;
                }

                .capabilities-hero {
                    padding: 1.8rem;
                }
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="capabilities-page">', unsafe_allow_html=True)

    # Hero
    st.markdown(
        """
        <div class="capabilities-hero">
            <div class="hero-label">Platform Overview</div>
            <h1>Capabilities and Future Potential</h1>
            <p>
                FidSync combines financial data preparation, fund analysis,
                document review, and reporting into a streamlined internal
                toolkit. The platform is designed to reduce repetitive work
                while preserving reviewability and human oversight.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Summary
    st.markdown(
        """
        <div class="summary-grid">
            <div class="summary-card">
                <div class="summary-number">6</div>
                <div class="summary-label">Current core capabilities</div>
            </div>

            <div class="summary-card">
                <div class="summary-number">5</div>
                <div class="summary-label">Expansion opportunities</div>
            </div>

            <div class="summary-card">
                <div class="summary-number">0</div>
                <div class="summary-label">Uploaded files retained</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Current capabilities
    st.markdown(
        """
        <div class="section-heading">Current capabilities</div>
        <div class="section-description">
            Functions already supported by the platform or its existing tools.
        </div>

        <div class="capability-grid">
            <div class="capability-card">
                <div class="card-header">
                    <h3>Secure, Ephemeral Processing</h3>
                    <span class="status-badge status-live">Available</span>
                </div>
                <p>
                    Processes uploaded information during the active session
                    without intentionally retaining user files after the task
                    is complete.
                </p>
                <div class="card-category">Security and privacy</div>
            </div>

            <div class="capability-card">
                <div class="card-header">
                    <h3>Automated Data Cleanup</h3>
                    <span class="status-badge status-live">Available</span>
                </div>
                <p>
                    Standardizes incoming spreadsheets by removing unnecessary
                    formatting residue, normalizing values, and preparing data
                    for consistent downstream analysis.
                </p>
                <div class="card-category">Data preparation</div>
            </div>

            <div class="capability-card">
                <div class="card-header">
                    <h3>Context-Aware Document Parsing</h3>
                    <span class="status-badge status-live">Available</span>
                </div>
                <p>
                    Identifies fund names, metrics, commentary, and supporting
                    context within semi-structured financial documents.
                </p>
                <div class="card-category">Document intelligence</div>
            </div>

            <div class="capability-card">
                <div class="card-header">
                    <h3>Advanced Record Matching</h3>
                    <span class="status-badge status-live">Available</span>
                </div>
                <p>
                    Uses normalized text and fuzzy matching techniques to connect
                    records across files even when naming conventions differ.
                </p>
                <div class="card-category">Data reconciliation</div>
            </div>

            <div class="capability-card">
                <div class="card-header">
                    <h3>Customizable Logic Layers</h3>
                    <span class="status-badge status-live">Available</span>
                </div>
                <p>
                    Supports firm-specific scoring rules, peer thresholds,
                    exceptions, overrides, and review workflows.
                </p>
                <div class="card-category">Business rules</div>
            </div>

            <div class="capability-card">
                <div class="card-header">
                    <h3>Structured Output Generation</h3>
                    <span class="status-badge status-live">Available</span>
                </div>
                <p>
                    Produces organized Excel reports with standardized columns,
                    status indicators, conditional formatting, and review-ready
                    presentation.
                </p>
                <div class="card-category">Reporting</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Potential features
    st.markdown(
        """
        <div class="section-heading">Expansion opportunities</div>
        <div class="section-description">
            Potential additions that could broaden FidSync into a more complete
            investment research and workflow platform.
        </div>

        <div class="capability-grid">
            <div class="capability-card">
                <div class="card-header">
                    <h3>Benchmark Comparison Tools</h3>
                    <span class="status-badge status-development">
                        In Development
                    </span>
                </div>
                <p>
                    Compare funds against benchmarks and peer groups across
                    multiple time periods, supported by visual trend analysis.
                </p>
                <div class="card-category">Performance analysis</div>
            </div>

            <div class="capability-card">
                <div class="card-header">
                    <h3>Portfolio Diagnostics</h3>
                    <span class="status-badge status-development">
                        In Development
                    </span>
                </div>
                <p>
                    Add risk-and-return charts, allocation breakdowns, sector
                    exposure analysis, and style mapping.
                </p>
                <div class="card-category">Portfolio analysis</div>
            </div>

            <div class="capability-card">
                <div class="card-header">
                    <h3>Assisted Recommendations</h3>
                    <span class="status-badge status-future">Future</span>
                </div>
                <p>
                    Surface possible review points using IPS requirements,
                    scoring history, portfolio context, and peer changes while
                    keeping final decisions with the advisor.
                </p>
                <div class="card-category">Decision support</div>
            </div>

            <div class="capability-card">
                <div class="card-header">
                    <h3>Enterprise Administration</h3>
                    <span class="status-badge status-future">Future</span>
                </div>
                <p>
                    Introduce role-based permissions, firm branding, audit logs,
                    administrative controls, and compliance review flags.
                </p>
                <div class="card-category">Platform management</div>
            </div>

            <div class="capability-card">
                <div class="card-header">
                    <h3>Platform Integrations</h3>
                    <span class="status-badge status-future">Future</span>
                </div>
                <p>
                    Connect approved data sources such as custodians, portfolio
                    systems, CRMs, research databases, and proposal platforms.
                </p>
                <div class="card-category">Integrations</div>
            </div>

            <div class="capability-card">
                <div class="card-header">
                    <h3>Workflow Automation</h3>
                    <span class="status-badge status-future">Future</span>
                </div>
                <p>
                    Create recurring review workflows, approval queues,
                    exception alerts, and standardized follow-up assignments.
                </p>
                <div class="card-category">Operations</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Roadmap
    st.markdown(
        """
        <div class="section-heading">Development roadmap</div>
        <div class="section-description">
            A possible sequence for expanding the platform without adding
            unnecessary complexity too quickly.
        </div>

        <div class="roadmap">
            <div class="roadmap-row">
                <div class="roadmap-phase">Phase 1</div>
                <div class="roadmap-content">
                    <strong>Strengthen existing tools</strong>
                    <span>
                        Improve validation, error handling, documentation,
                        consistency, and output quality.
                    </span>
                </div>
            </div>

            <div class="roadmap-row">
                <div class="roadmap-phase">Phase 2</div>
                <div class="roadmap-content">
                    <strong>Expand portfolio analysis</strong>
                    <span>
                        Add benchmark comparisons, historical tracking,
                        visualizations, and portfolio diagnostics.
                    </span>
                </div>
            </div>

            <div class="roadmap-row">
                <div class="roadmap-phase">Phase 3</div>
                <div class="roadmap-content">
                    <strong>Introduce shared workflows</strong>
                    <span>
                        Add accounts, saved projects, permissions, review
                        queues, and audit history.
                    </span>
                </div>
            </div>

            <div class="roadmap-row">
                <div class="roadmap-phase">Phase 4</div>
                <div class="roadmap-content">
                    <strong>Connect external platforms</strong>
                    <span>
                        Evaluate approved integrations with custodians, CRMs,
                        reporting systems, and research providers.
                    </span>
                </div>
            </div>
        </div>

        <div class="capability-notice">
            <strong>Development note:</strong> Future capabilities are conceptual
            and would require security review, data-access approval, testing,
            and compliance oversight before implementation.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("</div>", unsafe_allow_html=True)
