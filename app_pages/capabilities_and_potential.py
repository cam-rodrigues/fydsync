import streamlit as st


def run():
    # =====================================================
    # Page styling
    # =====================================================

    st.markdown(
        """
        <style>
            /* Main page spacing */
            .block-container {
                max-width: 1150px;
                padding-top: 2rem;
                padding-bottom: 3rem;
            }

            /* Page header */
            .page-header {
                padding: 2rem 2.2rem;
                margin-bottom: 1.5rem;
                background: linear-gradient(
                    135deg,
                    #102542 0%,
                    #213b5c 100%
                );
                border: 1px solid #2d496b;
                border-radius: 1rem;
                box-shadow: 0 8px 24px rgba(16, 37, 66, 0.12);
            }

            .page-label {
                margin-bottom: 0.55rem;
                color: #b9cde5;
                font-size: 0.72rem;
                font-weight: 700;
                letter-spacing: 0.1rem;
                text-transform: uppercase;
            }

            .page-header h1 {
                margin: 0;
                color: white;
                font-size: 2.15rem;
                font-weight: 750;
                line-height: 1.2;
                letter-spacing: -0.04rem;
            }

            .page-header p {
                max-width: 780px;
                margin: 0.8rem 0 0 0;
                color: #d8e4f2;
                font-size: 0.96rem;
                line-height: 1.6;
            }

            /* Section headings */
            .section-heading {
                margin-top: 1.2rem;
                margin-bottom: 0.2rem;
                color: #102542;
                font-size: 1.35rem;
                font-weight: 750;
            }

            .section-description {
                margin-bottom: 1rem;
                color: #64748b;
                font-size: 0.9rem;
                line-height: 1.5;
            }

            /* Native metric styling */
            [data-testid="stMetric"] {
                padding: 1rem 1.1rem;
                background-color: white;
                border: 1px solid #dce3ec;
                border-radius: 0.75rem;
                box-shadow: 0 2px 8px rgba(16, 37, 66, 0.04);
            }

            [data-testid="stMetricLabel"] {
                color: #64748b;
                font-size: 0.8rem;
                font-weight: 600;
            }

            [data-testid="stMetricValue"] {
                color: #102542;
                font-size: 1.75rem;
                font-weight: 750;
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

            /* Tabs */
            button[data-baseweb="tab"] {
                color: #64748b;
                font-weight: 600;
            }

            button[data-baseweb="tab"][aria-selected="true"] {
                color: #102542;
            }

            /* Information boxes */
            .status-box {
                padding: 0.9rem 1rem;
                margin-bottom: 0.8rem;
                background-color: #f7fafd;
                border: 1px solid #d6e1f3;
                border-left: 4px solid #2b6cb0;
                border-radius: 0.55rem;
            }

            .status-box strong {
                color: #102542;
            }

            .status-box p {
                margin: 0.25rem 0 0 0;
                color: #64748b;
                font-size: 0.86rem;
                line-height: 1.5;
            }

            /* Roadmap */
            .roadmap-box {
                padding: 1rem 1.1rem;
                margin-bottom: 0.8rem;
                background-color: white;
                border: 1px solid #dce3ec;
                border-radius: 0.7rem;
                box-shadow: 0 2px 8px rgba(16, 37, 66, 0.035);
            }

            .roadmap-phase {
                margin-bottom: 0.25rem;
                color: #2b6cb0;
                font-size: 0.7rem;
                font-weight: 750;
                letter-spacing: 0.06rem;
                text-transform: uppercase;
            }

            .roadmap-title {
                margin-bottom: 0.25rem;
                color: #102542;
                font-size: 0.95rem;
                font-weight: 700;
            }

            .roadmap-description {
                color: #64748b;
                font-size: 0.84rem;
                line-height: 1.5;
            }

            /* Footer note */
            .development-note {
                margin-top: 1.4rem;
                padding: 0.9rem 1rem;
                background-color: #edf3fa;
                border: 1px solid #cfdae8;
                border-left: 4px solid #2b6cb0;
                border-radius: 0.55rem;
                color: #526273;
                font-size: 0.82rem;
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
        <div class="page-header">
            <div class="page-label">Platform Overview</div>
            <h1>Roadmap</h1>
            <p>
                Review FidSync's current functionality, planned improvements,
                and long-term opportunities for expanding the platform.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # =====================================================
    # Summary metrics
    # =====================================================

    metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)

    with metric_col1:
        st.metric(
            label="Current Capabilities",
            value="6",
        )

    with metric_col2:
        st.metric(
            label="Potential Features",
            value="6",
        )

    with metric_col3:
        st.metric(
            label="Development Phases",
            value="4",
        )

    with metric_col4:
        st.metric(
            label="File Retention",
            value="0",
        )

    st.markdown("")

    # =====================================================
    # Tabs
    # =====================================================

    current_tab, potential_tab, roadmap_tab = st.tabs(
        [
            "Current Capabilities",
            "Future Potential",
            "Development Roadmap",
        ]
    )

    # =====================================================
    # Current capabilities tab
    # =====================================================

    with current_tab:
        st.markdown(
            """
            <div class="section-heading">Current capabilities</div>
            <div class="section-description">
                Core functionality already supported by FidSync and its
                existing tools.
            </div>
            """,
            unsafe_allow_html=True,
        )

        left_column, right_column = st.columns(2)

        with left_column:
            with st.expander(
                "Secure, Ephemeral Processing",
                expanded=True,
            ):
                st.write(
                    """
                    Uploaded information is processed during the active session.
                    Files are not intentionally retained after processing is
                    complete.
                    """
                )

                st.markdown(
                    """
                    **Key functions**

                    - In-memory data processing
                    - Temporary upload handling
                    - Reduced unnecessary file retention
                    - Session-based workflow
                    """
                )

            with st.expander("Automated Data Cleanup"):
                st.write(
                    """
                    Incoming spreadsheets and data files are standardized before
                    analysis so results remain consistent across different
                    formats.
                    """
                )

                st.markdown(
                    """
                    **Key functions**

                    - Removes unnecessary formatting residue
                    - Standardizes column names
                    - Normalizes values
                    - Prepares data for analysis
                    """
                )

            with st.expander("Advanced Record Matching"):
                st.write(
                    """
                    FidSync uses normalized text and fuzzy matching techniques to
                    connect records even when names, spacing, or formatting are
                    inconsistent.
                    """
                )

                st.markdown(
                    """
                    **Key functions**

                    - Fuzzy string matching
                    - Name normalization
                    - Duplicate identification
                    - Cross-file record reconciliation
                    """
                )

        with right_column:
            with st.expander(
                "Context-Aware Document Parsing",
                expanded=True,
            ):
                st.write(
                    """
                    The platform identifies important information within
                    semi-structured financial documents using text, layout, and
                    surrounding context.
                    """
                )

                st.markdown(
                    """
                    **Key functions**

                    - Fund name extraction
                    - Metric identification
                    - Commentary detection
                    - Table and document review
                    """
                )

            with st.expander("Customizable Logic Layers"):
                st.write(
                    """
                    Firm-specific rules can be incorporated into scoring,
                    screening, review, and exception-handling workflows.
                    """
                )

                st.markdown(
                    """
                    **Key functions**

                    - Compliance scoring rules
                    - Peer-group thresholds
                    - Override workflows
                    - Custom review criteria
                    """
                )

            with st.expander("Structured Output Generation"):
                st.write(
                    """
                    FidSync produces organized Excel outputs designed for easier
                    review, comparison, and presentation.
                    """
                )

                st.markdown(
                    """
                    **Key functions**

                    - Standardized report columns
                    - Conditional formatting
                    - Status indicators
                    - Review-ready Excel files
                    """
                )

        st.markdown(
            """
            <div class="development-note">
                <strong>Current-state note:</strong> Available functionality
                may differ slightly between tools. Results should be reviewed
                before being used for financial, investment, or compliance
                decisions.
            </div>
            """,
            unsafe_allow_html=True,
        )

    # =====================================================
    # Future potential tab
    # =====================================================

    with potential_tab:
        st.markdown(
            """
            <div class="section-heading">Future potential</div>
            <div class="section-description">
                Possible additions that could expand FidSync into a broader
                financial research, portfolio analysis, and workflow platform.
            </div>
            """,
            unsafe_allow_html=True,
        )

        future_col1, future_col2 = st.columns(2)

        with future_col1:
            st.markdown(
                """
                <div class="status-box">
                    <strong>Benchmark Comparison Tools</strong>
                    <p>
                        Compare funds against selected benchmarks, peer groups,
                        and historical periods using tables and visualizations.
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.markdown(
                """
                <div class="status-box">
                    <strong>Portfolio Diagnostics</strong>
                    <p>
                        Add risk-and-return charts, sector exposure analysis,
                        allocation reviews, and style-box mapping.
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.markdown(
                """
                <div class="status-box">
                    <strong>Assisted Recommendations</strong>
                    <p>
                        Surface possible review points using IPS requirements,
                        fund scores, historical trends, and peer changes.
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with future_col2:
            st.markdown(
                """
                <div class="status-box">
                    <strong>Enterprise Administration</strong>
                    <p>
                        Add role-based permissions, firm branding, audit logs,
                        administrative controls, and compliance review flags.
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.markdown(
                """
                <div class="status-box">
                    <strong>Platform Integrations</strong>
                    <p>
                        Connect approved custodians, CRMs, portfolio systems,
                        research databases, and proposal tools.
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.markdown(
                """
                <div class="status-box">
                    <strong>Workflow Automation</strong>
                    <p>
                        Create recurring review workflows, approval queues,
                        exception alerts, and standardized follow-up tasks.
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown("### Potential development priorities")

        priority_options = [
            "Benchmark comparison tools",
            "Portfolio diagnostics",
            "Platform integrations",
            "Enterprise administration",
            "Workflow automation",
            "Assisted recommendations",
        ]

        selected_priority = st.selectbox(
            "Select an area to review",
            options=priority_options,
        )

        priority_details = {
            "Benchmark comparison tools": (
                "This would likely be one of the most practical next additions "
                "because it builds directly on existing scorecard and fund data."
            ),
            "Portfolio diagnostics": (
                "This would broaden the platform beyond individual fund review "
                "and support portfolio-level analysis."
            ),
            "Platform integrations": (
                "Integrations could reduce manual uploads, but they would require "
                "security review, data access approval, and API support."
            ),
            "Enterprise administration": (
                "Administrative tools would become more important if FidSync were "
                "used by multiple teams or users."
            ),
            "Workflow automation": (
                "Workflow features could help standardize recurring reviews, "
                "approvals, and follow-up responsibilities."
            ),
            "Assisted recommendations": (
                "Recommendation support should remain review-based and should not "
                "replace advisor judgment or compliance oversight."
            ),
        }

        st.info(priority_details[selected_priority])

    # =====================================================
    # Roadmap tab
    # =====================================================

    with roadmap_tab:
        st.markdown(
            """
            <div class="section-heading">Development roadmap</div>
            <div class="section-description">
                A possible order for expanding FidSync while keeping the platform
                manageable, secure, and useful.
            </div>
            """,
            unsafe_allow_html=True,
        )

        roadmap_col1, roadmap_col2 = st.columns(2)

        with roadmap_col1:
            st.markdown(
                """
                <div class="roadmap-box">
                    <div class="roadmap-phase">Phase 1</div>
                    <div class="roadmap-title">
                        Strengthen existing tools
                    </div>
                    <div class="roadmap-description">
                        Improve validation, error handling, documentation,
                        consistency, and output quality across the current
                        platform.
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.markdown(
                """
                <div class="roadmap-box">
                    <div class="roadmap-phase">Phase 2</div>
                    <div class="roadmap-title">
                        Expand analysis
                    </div>
                    <div class="roadmap-description">
                        Add benchmark comparisons, historical tracking,
                        visualizations, and portfolio diagnostic tools.
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with roadmap_col2:
            st.markdown(
                """
                <div class="roadmap-box">
                    <div class="roadmap-phase">Phase 3</div>
                    <div class="roadmap-title">
                        Introduce shared workflows
                    </div>
                    <div class="roadmap-description">
                        Add user accounts, saved projects, permissions, review
                        queues, approvals, and audit history.
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.markdown(
                """
                <div class="roadmap-box">
                    <div class="roadmap-phase">Phase 4</div>
                    <div class="roadmap-title">
                        Connect external platforms
                    </div>
                    <div class="roadmap-description">
                        Evaluate approved integrations with custodians, CRMs,
                        reporting platforms, and research providers.
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown("### Estimated platform progress")

        st.progress(0.35)

        st.caption(
            "Illustrative progress only. The percentage can be updated as "
            "features are completed."
        )

        st.markdown(
            """
            <div class="development-note">
                <strong>Development note:</strong> Future capabilities are
                conceptual. Security review, data-access approval, testing,
                documentation, and compliance oversight would be required
                before implementation.
            </div>
            """,
            unsafe_allow_html=True,
        )
