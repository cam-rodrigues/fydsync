# app_pages/user_requests.py

from datetime import datetime
import re
import uuid

import streamlit as st

from utils.system.google_sheets import log_to_google_sheets


REQUEST_TYPES = [
    "Feature Request",
    "Bug Report",
    "General Question",
    "Data or Output Issue",
    "Other",
]

PRIORITY_OPTIONS = [
    "Low",
    "Normal",
    "High",
]


def is_valid_email(email: str) -> bool:
    """Return True when the email has a basic valid structure."""

    if not email:
        return True

    pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
    return re.match(pattern, email.strip()) is not None


def create_request_id() -> str:
    """Create a short reference number for the submission."""

    return f"FS-{uuid.uuid4().hex[:8].upper()}"


def run():
    # =====================================================
    # Page styling
    # =====================================================

    st.markdown(
        """
        <style>
            .block-container {
                max-width: 1050px;
                padding-top: 2rem;
                padding-bottom: 3rem;
            }

            /* Page header */
            .request-header {
                padding: 2.1rem 2.3rem;
                margin-bottom: 1.5rem;
                background:
                    radial-gradient(
                        circle at top right,
                        rgba(117, 158, 203, 0.20),
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

            .request-header-label {
                margin-bottom: 0.55rem;
                color: #b9cde5;
                font-size: 0.72rem;
                font-weight: 700;
                letter-spacing: 0.1rem;
                text-transform: uppercase;
            }

            .request-header h1 {
                margin: 0;
                color: white;
                font-size: 2.15rem;
                font-weight: 750;
                line-height: 1.2;
                letter-spacing: -0.045rem;
            }

            .request-header p {
                max-width: 760px;
                margin: 0.8rem 0 0 0;
                color: #d8e4f2;
                font-size: 0.96rem;
                line-height: 1.6;
            }

            /* Intro information */
            .request-intro {
                padding: 1rem 1.1rem;
                margin-bottom: 1.2rem;
                background-color: #f7fafd;
                border: 1px solid #d6e1f3;
                border-left: 4px solid #2b6cb0;
                border-radius: 0.65rem;
                color: #526273;
                font-size: 0.85rem;
                line-height: 1.55;
            }

            /* Form container */
            [data-testid="stForm"] {
                padding: 1.5rem 1.6rem;
                background-color: white;
                border: 1px solid #dce3ec;
                border-radius: 0.9rem;
                box-shadow: 0 3px 12px rgba(16, 37, 66, 0.05);
            }

            /* Input labels */
            [data-testid="stWidgetLabel"] p {
                color: #102542;
                font-size: 0.86rem;
                font-weight: 650;
            }

            /* Inputs */
            [data-baseweb="input"] > div,
            [data-baseweb="textarea"] > div,
            [data-baseweb="select"] > div {
                border-color: #ccd8e6;
                border-radius: 0.55rem;
            }

            [data-baseweb="input"] > div:focus-within,
            [data-baseweb="textarea"] > div:focus-within,
            [data-baseweb="select"] > div:focus-within {
                border-color: #2b6cb0;
                box-shadow: 0 0 0 1px #2b6cb0;
            }

            /* Submit button */
            [data-testid="stFormSubmitButton"] button {
                min-height: 2.7rem;
                padding: 0.55rem 1.3rem;
                background-color: #2b6cb0;
                color: white;
                border: 1px solid #2b6cb0;
                border-radius: 0.55rem;
                font-weight: 700;
            }

            [data-testid="stFormSubmitButton"] button:hover {
                background-color: #1f568f;
                border-color: #1f568f;
                color: white;
            }

            /* Section labels */
            .form-section-title {
                margin-top: 0.2rem;
                margin-bottom: 0.2rem;
                color: #102542;
                font-size: 1.05rem;
                font-weight: 720;
            }

            .form-section-description {
                margin-bottom: 0.8rem;
                color: #64748b;
                font-size: 0.82rem;
                line-height: 1.5;
            }

            /* Submission confirmation */
            .confirmation-card {
                padding: 1.3rem 1.4rem;
                margin-top: 1.2rem;
                background-color: #f5f9fd;
                border: 1px solid #cfdae8;
                border-radius: 0.8rem;
                box-shadow: 0 2px 8px rgba(16, 37, 66, 0.04);
            }

            .confirmation-label {
                margin-bottom: 0.35rem;
                color: #2b6cb0;
                font-size: 0.7rem;
                font-weight: 750;
                letter-spacing: 0.06rem;
                text-transform: uppercase;
            }

            .confirmation-id {
                margin-bottom: 0.9rem;
                color: #102542;
                font-size: 1.2rem;
                font-weight: 750;
            }

            .confirmation-row {
                display: grid;
                grid-template-columns: 130px 1fr;
                gap: 0.8rem;
                padding: 0.45rem 0;
                border-bottom: 1px solid #e2e8f0;
                color: #526273;
                font-size: 0.84rem;
                line-height: 1.5;
            }

            .confirmation-row:last-child {
                border-bottom: none;
            }

            .confirmation-row strong {
                color: #102542;
            }

            /* Footer note */
            .privacy-note {
                margin-top: 1rem;
                color: #718096;
                font-size: 0.78rem;
                line-height: 1.5;
            }

            @media (max-width: 700px) {
                .confirmation-row {
                    grid-template-columns: 1fr;
                    gap: 0.15rem;
                }

                .request-header {
                    padding: 1.7rem;
                }
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
        <div class="request-header">
            <div class="request-header-label">Support & Feedback</div>
            <h1>Submit a Request</h1>
            <p>
                Report a problem, suggest a feature, ask a question, or share
                feedback about your experience using FidSync.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="request-intro">
            Provide as much detail as possible so the request can be reviewed
            efficiently. For technical issues, include the tool used, the input
            type, the expected result, and what actually occurred.
        </div>
        """,
        unsafe_allow_html=True,
    )

    # =====================================================
    # Request form
    # =====================================================

    with st.form("user_request_form", clear_on_submit=False):
        st.markdown(
            """
            <div class="form-section-title">Contact information</div>
            <div class="form-section-description">
                Your email is optional, but it may be needed if additional
                information is required.
            </div>
            """,
            unsafe_allow_html=True,
        )

        contact_col1, contact_col2 = st.columns(2)

        with contact_col1:
            name = st.text_input(
                "Your name",
                placeholder="Enter your name",
            )

        with contact_col2:
            email = st.text_input(
                "Your email",
                placeholder="name@example.com",
            )

        st.markdown(
            """
            <div class="form-section-title">Request details</div>
            <div class="form-section-description">
                Select the category that most closely matches your request.
            </div>
            """,
            unsafe_allow_html=True,
        )

        detail_col1, detail_col2 = st.columns(2)

        with detail_col1:
            request_type = st.selectbox(
                "Type of request",
                options=REQUEST_TYPES,
            )

        with detail_col2:
            priority = st.selectbox(
                "Priority",
                options=PRIORITY_OPTIONS,
                index=1,
                help=(
                    "Use High only when the issue prevents you from completing "
                    "an important workflow."
                ),
            )

        tool_name = st.selectbox(
            "Related tool",
            options=[
                "General platform",
                "Fund Scorecard",
                "Scorecard Metrics",
                "IPS Screening",
                "Writeup",
                "Writeup & Recommendation",
                "Article Analyzer",
                "Company Lookup",
                "Other",
            ],
        )

        subject = st.text_input(
            "Request title",
            placeholder="Briefly summarize the request",
            max_chars=120,
        )

        message = st.text_area(
            "Description",
            height=190,
            placeholder=(
                "Describe what you need, what happened, and any relevant steps "
                "that could help reproduce the issue."
            ),
        )

        uploaded_file = st.file_uploader(
            "Optional screenshot or supporting file",
            type=["png", "jpg", "jpeg", "pdf", "txt", "csv", "xlsx"],
            help=(
                "Do not upload passwords, account numbers, Social Security "
                "numbers, or confidential client information."
            ),
        )

        confirmation = st.checkbox(
            "I have removed confidential or sensitive information from my submission."
        )

        submitted = st.form_submit_button(
            "Submit Request",
            use_container_width=True,
        )

    # =====================================================
    # Submission handling
    # =====================================================

    if submitted:
        errors = []

        cleaned_name = name.strip()
        cleaned_email = email.strip()
        cleaned_subject = subject.strip()
        cleaned_message = message.strip()

        if not cleaned_name:
            errors.append("Enter your name.")

        if cleaned_email and not is_valid_email(cleaned_email):
            errors.append("Enter a valid email address or leave the field blank.")

        if not cleaned_subject:
            errors.append("Enter a short request title.")

        if not cleaned_message:
            errors.append("Enter a description of your request.")

        if len(cleaned_message) < 20:
            errors.append(
                "Add a little more detail so the request can be reviewed properly."
            )

        if not confirmation:
            errors.append(
                "Confirm that confidential or sensitive information has been removed."
            )

        if errors:
            st.error("The request could not be submitted yet.")

            for error in errors:
                st.write(f"• {error}")

            return

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        request_id = create_request_id()

        # Combine the additional fields with the main message if the existing
        # Google Sheets function only accepts the original six arguments.
        formatted_message = (
            f"Request ID: {request_id}\n"
            f"Subject: {cleaned_subject}\n"
            f"Priority: {priority}\n"
            f"Related Tool: {tool_name}\n\n"
            f"{cleaned_message}"
        )

        try:
            success = log_to_google_sheets(
                cleaned_name,
                cleaned_email,
                request_type,
                formatted_message,
                uploaded_file,
                timestamp,
            )
        except Exception as error:
            success = False
            st.error("The request could not be submitted.")
            st.exception(error)

        if success:
            st.success("Your request was submitted successfully.")

            file_name = uploaded_file.name if uploaded_file else "No file attached"
            email_display = cleaned_email if cleaned_email else "Not provided"

            st.markdown(
                f"""
                <div class="confirmation-card">
                    <div class="confirmation-label">Request reference</div>
                    <div class="confirmation-id">{request_id}</div>

                    <div class="confirmation-row">
                        <strong>Submitted</strong>
                        <span>{timestamp}</span>
                    </div>

                    <div class="confirmation-row">
                        <strong>Name</strong>
                        <span>{cleaned_name}</span>
                    </div>

                    <div class="confirmation-row">
                        <strong>Email</strong>
                        <span>{email_display}</span>
                    </div>

                    <div class="confirmation-row">
                        <strong>Request type</strong>
                        <span>{request_type}</span>
                    </div>

                    <div class="confirmation-row">
                        <strong>Priority</strong>
                        <span>{priority}</span>
                    </div>

                    <div class="confirmation-row">
                        <strong>Related tool</strong>
                        <span>{tool_name}</span>
                    </div>

                    <div class="confirmation-row">
                        <strong>Title</strong>
                        <span>{cleaned_subject}</span>
                    </div>

                    <div class="confirmation-row">
                        <strong>File</strong>
                        <span>{file_name}</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            with st.expander("View submitted description"):
                st.write(cleaned_message)

            st.caption(
                "Keep the request reference number in case you need to follow up."
            )

        elif "error" not in locals():
            st.error(
                "There was an error saving your request. Review your connection "
                "and try again."
            )

    st.markdown(
        """
        <div class="privacy-note">
            Submitted information may be stored in the connected request log.
            Avoid including confidential client data, credentials, account
            numbers, or other restricted information.
        </div>
        """,
        unsafe_allow_html=True,
    )
