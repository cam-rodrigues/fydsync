import streamlit as st


def run():
    # =====================================================
    # Page styling
    # =====================================================

    st.markdown(
        """
        <style>
            .block-container {
                max-width: 1150px;
                padding-top: 2rem;
                padding-bottom: 3rem;
            }

            /* Page header */
            .getting-started-header {
                padding: 2.2rem 2.4rem;
                margin-bottom: 1.5rem;
                background:
                    radial-gradient(
                        circle at top right,
                        rgba(117, 158, 203, 0.2),
                        transparent 35%
                    ),
                    linear-gradient(
                        135deg,
                        #102542 0%,
                        #213b5c 100%
                    );
                border: 1px solid #2d496b;
                border-radius: 1rem;
                box-shadow: 0 8px 24px rgba(16, 37, 66, 0.12);
            }

            .header-label {
                margin-bottom: 0.55rem;
                color: #b9cde5;
                font-size: 0.72rem;
                font-weight: 700;
                letter-spacing: 0.1rem;
                text-transform: uppercase;
            }

            .getting-started-header h1 {
                margin: 0;
                color: white;
                font-size: 2.2rem;
                font-weight: 750;
                line-height: 1.2;
                letter-spacing: -0.05rem;
            }

            .getting-started-header p {
                max-width: 780px;
                margin: 0.8rem 0 0 0;
                color: #d8e4f2;
                font-size: 0.97rem;
                line-height: 1.65;
            }

            /* Section headings */
            .section-heading {
                margin-top: 1.2rem;
                margin-bottom: 0.2rem;
                color: #102542;
                font-size: 1.35rem;
                font-weight: 750;
                letter-spacing: -0.02rem;
            }

            .section-description {
                margin-bottom: 1rem;
                color: #64748b;
                font-size: 0.9rem;
                line-height: 1.55;
            }

            /* Metrics */
            [data-testid="stMetric"] {
                min-height: 115px;
                padding: 1rem 1.1rem;
                background-color: white;
                border: 1px solid #dce3ec;
                border-radius: 0.75rem;
                box-shadow: 0 2px 8px rgba(16, 37, 66, 0.04);
            }

            [data-testid="stMetricLabel"] {
                color: #64748b;
                font-size: 0.78rem;
                font-weight: 600;
            }

            [data-testid="stMetricValue"] {
                color: #102542;
                font-size: 1.55rem;
                font-weight: 750;
            }

            /* Tabs */
            button[data-baseweb="tab"] {
                color: #64748b;
                font-weight: 600;
            }

            button[data-baseweb="tab"][aria-selected="true"] {
                color: #102542;
            }

            /* Expanders */
            [data-testid="stExpander"] {
                margin-bottom: 0.65rem;
                background-color: white;
                border: 1px solid #dce3ec;
                border-radius: 0.75rem;
                box-shadow: 0 2px 8px rgba(16, 37, 66, 0.035);
                overflow: hidden;
            }

            [data-testid="stExpander"] summary {
                color: #102542;
                font-weight: 650;
            }

            [data-testid="stExpander"] summary:hover {
                color: #2b6cb0;
            }

            /* Tool cards */
            .tool-card {
                min-height: 175px;
                padding: 1.15rem 1.2rem;
                margin-bottom: 0.85rem;
                background-color: white;
                border: 1px solid #dce3ec;
                border-radius: 0.75rem;
                box-shadow: 0 2px 8px rgba(16, 37, 66, 0.04);
            }

            .tool-category {
                margin-bottom: 0.4rem;
                color: #2b6cb0;
                font-size: 0.68rem;
                font-weight: 750;
                letter-spacing: 0.06rem;
                text-transform: uppercase;
            }

            .tool-card h3 {
                margin: 0 0 0.45rem 0;
                color: #102542;
                font-size: 1rem;
                font-weight: 700;
            }

            .tool-card p {
                margin: 0;
                color: #64748b;
                font-size: 0.84rem;
                line-height: 1.55;
            }

            /* Workflow step cards */
            .step-card {
                padding: 1rem 1.1rem;
                margin-bottom: 0.75rem;
                background-color: white;
                border: 1px solid #dce3ec;
                border-left: 4px solid #2b6cb0;
                border-radius: 0.7rem;
                box-shadow: 0 2px 8px rgba(16, 37, 66, 0.035);
            }

            .step-number {
                margin-bottom: 0.2rem;
                color: #2b6cb0;
                font-size: 0.68rem;
                font-weight: 750;
                letter-spacing: 0.06rem;
                text-transform: uppercase;
            }

            .step-title {
                margin-bottom: 0.25rem;
                color: #102542;
                font-size: 0.95rem;
                font-weight: 700;
            }

            .step-description {
                color: #64748b;
                font-size: 0.83rem;
                line-height: 1.5;
            }

            /* Security note */
            .security-note {
                padding: 1rem 1.1rem;
                margin-top: 1rem;
                background-color: #edf3fa;
                border: 1px solid #cfdae8;
                border-left: 4px solid #2b6cb0;
                border-radius: 0.6rem;
                color: #526273;
                font-size: 0.83rem;
                line-height: 1.55;
            }

            /* Support box */
            .support-box {
                padding: 1.2rem 1.3rem;
                margin-top: 1rem;
                background-color: #f7fafd;
                border: 1px solid #d6e1f3;
                border-radius: 0.75rem;
            }

            .support-box strong {
                color: #102542;
            }

            .support-box p {
                margin: 0.35rem 0 0 0;
                color: #64748b;
                font-size: 0.86rem;
                line-height: 1.55;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # =====================================================
    # Header
    # =====================================================

    st.markdown(
        """
        <div class="getting-started-header">
            <div class="header-label">Getting Started</div>
            <h1>Welcome to FidSync</h1>
            <p>
                Learn what the platform does, explore the available tools,
                and follow the recommended workflow for reviewing and
                exporting financial information.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # =====================================================
    # Overview metrics
    # =====================================================

    metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)

    with metric_col1:
        st.metric(
            label="Available Tools",
            value="4",
        )

    with metric_col2:
        st.metric(
            label="Supported Inputs",
            value="PDF, Excel & URL",
        )

    with metric_col3:
        st.metric(
            label="Export Options",
            value="Excel, CSV & PDF",
        )

    with metric_col4:
        st.metric(
            label="Platform Status",
            value="Beta",
        )

    st.markdown("")

    # =====================================================
    # Main tabs
    # =====================================================

    overview_tab, workflow_tab, security_tab, tips_tab = st.tabs(
        [
            "Platform Overview",
            "How to Use",
            "Data & Security",
            "Tips & Support",
        ]
    )

    # =====================================================
    # Platform overview
    # =====================================================

    with overview_tab:
        st.markdown(
            """
            <div class="section-heading">What is FidSync?</div>
            <div class="section-description">
                A centralized toolkit for investment due diligence, fund
                oversight, financial research, and reporting workflows.
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.write(
            """
            FidSync is designed for institutional advisors, plan consultants,
            analysts, and other financial professionals who regularly review
            investment information across multiple documents and data sources.

            The platform combines document processing, fund evaluation,
            financial research, and structured output tools into one unified
            internal application.
            """
        )

        st.markdown(
            """
            <div class="section-heading">Available tools</div>
            <div class="section-description">
                Select any tool from the sidebar to begin a new workflow.
            </div>
            """,
            unsafe_allow_html=True,
        )

        tool_col1, tool_col2 = st.columns(2)

        with tool_col1:
            st.markdown(
                """
                <div class="tool-card">
                    <div class="tool-category">Fund Analysis</div>
                    <h3>Fund Scorecard</h3>
                    <p>
                        Evaluate investment options using watchlist criteria,
                        peer comparisons, scoring logic, and automated
                        Pass or Review status markings.
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.markdown(
                """
                <div class="tool-card">
                    <div class="tool-category">Data Extraction</div>
                    <h3>Data Scanner</h3>
                    <p>
                        Extract structured investment metrics from PDFs and
                        Excel files, including peer ranks, returns, risk
                        statistics, and related fund information.
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with tool_col2:
            st.markdown(
                """
                <div class="tool-card">
                    <div class="tool-category">Research</div>
                    <h3>Article Analyzer</h3>
                    <p>
                        Review financial articles using company and ticker
                        detection, sentiment analysis, structured summaries,
                        and exportable research insights.
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.markdown(
                """
                <div class="tool-card">
                    <div class="tool-category">Company Research</div>
                    <h3>Company Lookup</h3>
                    <p>
                        Collect and organize publicly available company
                        information, including summaries, financial insights,
                        disclosures, and relevant website content.
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.info(
            "Additional tools may appear in the sidebar as the platform "
            "continues to expand."
        )

    # =====================================================
    # How to use
    # =====================================================

    with workflow_tab:
        st.markdown(
            """
            <div class="section-heading">Recommended workflow</div>
            <div class="section-description">
                Most FidSync tools follow the same five-step process.
            </div>
            """,
            unsafe_allow_html=True,
        )

        workflow_col1, workflow_col2 = st.columns(2)

        with workflow_col1:
            st.markdown(
                """
                <div class="step-card">
                    <div class="step-number">Step 1</div>
                    <div class="step-title">Choose a tool</div>
                    <div class="step-description">
                        Use the sidebar to select the module that matches your
                        task. Each tool provides instructions for its specific
                        workflow.
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.markdown(
                """
                <div class="step-card">
                    <div class="step-number">Step 2</div>
                    <div class="step-title">Provide the required input</div>
                    <div class="step-description">
                        Upload a supported PDF or Excel file, enter a URL, paste
                        investment options, or provide the requested search
                        information.
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.markdown(
                """
                <div class="step-card">
                    <div class="step-number">Step 3</div>
                    <div class="step-title">Run the analysis</div>
                    <div class="step-description">
                        FidSync processes the input, identifies relevant
                        information, and organizes the results for review.
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with workflow_col2:
            st.markdown(
                """
                <div class="step-card">
                    <div class="step-number">Step 4</div>
                    <div class="step-title">Review the results</div>
                    <div class="step-description">
                        Confirm fund names, mappings, scores, metrics, summaries,
                        and any flags before relying on the output.
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.markdown(
                """
                <div class="step-card">
                    <div class="step-number">Step 5</div>
                    <div class="step-title">Export or refine</div>
                    <div class="step-description">
                        Download the available Excel, CSV, or PDF output. Where
                        supported, adjust mappings or override matches before
                        creating the final report.
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.markdown(
                """
                <div class="step-card">
                    <div class="step-number">Final Review</div>
                    <div class="step-title">Verify important information</div>
                    <div class="step-description">
                        Compare material results against official statements,
                        source documents, or approved firm systems before using
                        them in client or compliance work.
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with st.expander("Example workflow"):
            st.markdown(
                """
                **Example: reviewing a fund scorecard**

                1. Open the Fund Scorecard tool.
                2. Upload the current scorecard or supporting fund data.
                3. Paste the plan's investment options in the requested order.
                4. Review the identified matches and any flagged exceptions.
                5. Generate and download the completed Excel report.
                6. Verify the output against the original source material.
                """
            )

    # =====================================================
    # Data and security
    # =====================================================

    with security_tab:
        st.markdown(
            """
            <div class="section-heading">Data handling and security</div>
            <div class="section-description">
                Important information about how files and inputs are handled
                during platform use.
            </div>
            """,
            unsafe_allow_html=True,
        )

        security_col1, security_col2 = st.columns(2)

        with security_col1:
            with st.expander(
                "Session-based processing",
                expanded=True,
            ):
                st.write(
                    """
                    Uploaded information is processed during the active
                    application session. The platform is designed to avoid
                    unnecessary retention of uploaded files.
                    """
                )

            with st.expander("Personal information"):
                st.write(
                    """
                    Users should avoid uploading personally identifiable,
                    confidential, or restricted client information unless the
                    specific tool and environment have been approved for that
                    purpose.
                    """
                )

        with security_col2:
            with st.expander(
                "External services",
                expanded=True,
            ):
                st.write(
                    """
                    Some tools may depend on external websites, APIs, libraries,
                    or third-party services. Data transmission depends on the
                    configuration of the individual tool.
                    """
                )

            with st.expander("Output review"):
                st.write(
                    """
                    Generated reports and summaries should be treated as
                    working materials until they have been reviewed and
                    verified by an authorized user.
                    """
                )

        st.markdown(
            """
            <div class="security-note">
                <strong>Important:</strong> Only state that files are never
                stored, transmitted, or logged if you have verified that this
                is true for every tool, hosting environment, API, and library
                used by the application.
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.warning(
            "Do not upload Social Security numbers, account numbers, client "
            "credentials, passwords, or other highly sensitive information."
        )

    # =====================================================
    # Tips and support
    # =====================================================

    with tips_tab:
        st.markdown(
            """
            <div class="section-heading">Tips for better results</div>
            <div class="section-description">
                Small preparation steps can improve matching, extraction,
                and reporting accuracy.
            </div>
            """,
            unsafe_allow_html=True,
        )

        tip_col1, tip_col2 = st.columns(2)

        with tip_col1:
            with st.expander(
                "Use clean source files",
                expanded=True,
            ):
                st.markdown(
                    """
                    - Use original or clearly exported PDFs when possible.
                    - Avoid scans with blurry text or handwritten notes.
                    - Remove unrelated pages before uploading.
                    - Use consistent Excel headers and column formats.
                    """
                )

            with st.expander("Prepare investment lists carefully"):
                st.markdown(
                    """
                    - Enter one investment option per line.
                    - Keep the list in the same order as the source file.
                    - Include full fund names when possible.
                    - Review ticker symbols and share classes.
                    """
                )

        with tip_col2:
            with st.expander(
                "Review automated matches",
                expanded=True,
            ):
                st.markdown(
                    """
                    - Confirm similar fund names manually.
                    - Check share classes and ticker symbols.
                    - Review low-confidence or unmatched records.
                    - Use overrides only when the correct match is known.
                    """
                )

            with st.expander("Prepare exports"):
                st.markdown(
                    """
                    - Review calculations before downloading.
                    - Confirm date ranges and reporting periods.
                    - Use PDF output for print-ready presentation.
                    - Use Excel or CSV when further editing is required.
                    """
                )

        st.markdown(
            """
            <div class="support-box">
                <strong>Support and feedback</strong>
                <p>
                    FidSync is actively evolving. To report a bug, suggest a
                    feature, or request assistance, open the User Requests tool
                    from the sidebar and provide as much detail as possible.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("### Before submitting a request")

        st.markdown(
            """
            Include the following information when possible:

            - The tool you were using
            - The file type or input format
            - What you expected to happen
            - What actually happened
            - Any visible error message
            - A screenshot with confidential information removed
            """
        )
