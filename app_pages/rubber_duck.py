# app_pages/rubber_duck.py

import random

import streamlit as st


DUCK_ISSUES = [
    "Choose one...",
    "There's an error",
    "Python isn't listening",
    "Something is behaving strangely",
]


DUCK_INTROS = {
    "There's an error": (
        "Oh no. Errors are rude, but they are usually trying to tell us "
        "exactly where the problem is."
    ),
    "Python isn't listening": (
        "Hmm. Python may be listening to a different file, an older version, "
        "or instructions that are not running where you think they are."
    ),
    "Something is behaving strangely": (
        "Suspicious. Let's slow this down and figure out what the app is "
        "actually doing."
    ),
}


DUCK_ADVICE = {
    "There's an error": [
        (
            "Read the traceback from the bottom upward and find the first "
            "line that points to your own file."
        ),
        (
            "Check the exact line named in the traceback for a misspelled "
            "variable, missing comma, unmatched quote, or indentation issue."
        ),
        (
            "Add st.write() immediately before the failing line so you can "
            "see the value and type Python is receiving."
        ),
        (
            "Comment out the newest code and restore it a few lines at a "
            "time until the error returns."
        ),
        (
            "Compare the broken version with the last version that worked. "
            "The smallest difference is usually the useful clue."
        ),
    ],
    "Python isn't listening": [
        (
            "Save the file, confirm you edited the exact file the router "
            "loads, and reboot the Streamlit app."
        ),
        (
            "Check the filename and capitalization. A second copy in another "
            "folder can make your changes appear invisible."
        ),
        (
            "Add st.success('NEW CODE IS RUNNING') temporarily to verify "
            "which file Streamlit is loading."
        ),
        (
            "Make sure the function containing your new code is actually "
            "being called."
        ),
        (
            "Open the deployed file on GitHub and confirm the latest commit "
            "contains your changes."
        ),
    ],
    "Something is behaving strangely": [
        (
            "Write down what you expected to happen and what actually "
            "happened. The difference is your first clue."
        ),
        (
            "Change only one thing at a time. Multiple fixes make it harder "
            "to tell which change mattered."
        ),
        (
            "Inspect the values immediately before the strange behavior "
            "using st.write()."
        ),
        (
            "Reduce the problem to the smallest possible example that still "
            "behaves incorrectly."
        ),
        (
            "Check whether a Streamlit rerun or Session State value is "
            "resetting the widget."
        ),
    ],
}


DUCK_ENCOURAGEMENT = [
    "Go try that. The duck will wait right here.",
    "You have a solid next step. Give it another shot.",
    "Try the suggestion, then come back if the bug is still being dramatic.",
    "The duck believes this is worth another attempt.",
]


def initialize_duck_state() -> None:
    """Initialize the debugger's session-state values."""

    defaults = {
        "duck_active_issue": "",
        "duck_advice_index": 0,
        "duck_struggle_count": 0,
        "duck_resolved": False,
        "duck_encouragement": random.choice(DUCK_ENCOURAGEMENT),
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def reset_duck() -> None:
    """Reset the debugger without mutating an instantiated widget."""

    st.session_state.duck_active_issue = ""
    st.session_state.duck_advice_index = 0
    st.session_state.duck_struggle_count = 0
    st.session_state.duck_resolved = False
    st.session_state.duck_encouragement = random.choice(
        DUCK_ENCOURAGEMENT
    )

    st.session_state.pop("duck_issue_choice", None)


def return_to_previous_page() -> None:
    """Return to whichever FidSync page opened the debugger."""

    previous_page = st.session_state.get(
        "duck_previous_page",
        "Getting_Started.py",
    )

    st.query_params["page"] = previous_page


def apply_styles() -> None:
    """Apply page-specific styling."""

    st.markdown(
        """
        <style>
            .block-container {
                max-width: 860px;
                padding-top: 2rem;
                padding-bottom: 3rem;
            }

            .duck-hero {
                padding: 2.1rem 2rem;
                margin-bottom: 1.5rem;
                text-align: center;
                background:
                    radial-gradient(
                        circle at top right,
                        rgba(117, 158, 203, 0.22),
                        transparent 38%
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

            .duck-icon {
                margin-bottom: 0.6rem;
                font-size: 5rem;
                line-height: 1;
            }

            .duck-title {
                color: #ffffff !important;
                -webkit-text-fill-color: #ffffff !important;
                font-size: 2rem;
                font-weight: 750;
                line-height: 1.2;
            }

            .duck-subtitle {
                margin-top: 0.7rem;
                color: #d8e4f2 !important;
                -webkit-text-fill-color: #d8e4f2 !important;
                font-size: 0.95rem;
                line-height: 1.6;
            }

            .duck-version {
                margin-top: 0.45rem;
                color: #9fb7d2 !important;
                -webkit-text-fill-color: #9fb7d2 !important;
                font-size: 0.72rem;
                font-weight: 650;
                letter-spacing: 0.06rem;
                text-transform: uppercase;
            }

            div[data-testid="stRadio"] {
                padding: 0.25rem 0 0.5rem 0;
            }

            div[data-testid="stAlert"] {
                border-radius: 0.75rem;
            }

            .stButton > button {
                border-radius: 0.6rem;
                font-weight: 650;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_header() -> None:
    """Render a compact single-line HTML header."""

    header_html = (
        '<div class="duck-hero">'
        '<div class="duck-icon">🦆</div>'
        '<div class="duck-title">Duck Debugger</div>'
        '<div class="duck-subtitle">'
        'Choose the closest description of the problem. '
        'The duck will keep offering suggestions until something works.'
        '</div>'
        '<div class="duck-version">Highly Experimental · v0.1</div>'
        '</div>'
    )

    st.markdown(
        header_html,
        unsafe_allow_html=True,
    )


def run() -> None:
    """Render the hidden Rubber Duck Debugger page."""

    initialize_duck_state()
    apply_styles()
    render_header()

    issue_choice = st.radio(
        "What's going wrong?",
        DUCK_ISSUES,
        key="duck_issue_choice",
    )

    if issue_choice != "Choose one...":
        if issue_choice != st.session_state.duck_active_issue:
            st.session_state.duck_active_issue = issue_choice
            st.session_state.duck_advice_index = 0
            st.session_state.duck_struggle_count = 0
            st.session_state.duck_resolved = False
            st.session_state.duck_encouragement = random.choice(
                DUCK_ENCOURAGEMENT
            )

        if st.session_state.duck_resolved:
            st.success("🦆 The duck knew you could do it.")
            st.caption(
                "Debugging is not about never getting stuck. "
                "It is about getting unstuck."
            )

            button_col1, button_col2 = st.columns(2)

            with button_col1:
                if st.button(
                    "Debug Another Problem",
                    key="duck_debug_another",
                    use_container_width=True,
                ):
                    reset_duck()
                    st.rerun()

            with button_col2:
                st.button(
                    "Return to FidSync",
                    key="duck_return_success",
                    use_container_width=True,
                    on_click=return_to_previous_page,
                )

        else:
            advice_list = DUCK_ADVICE[issue_choice]
            advice_index = (
                st.session_state.duck_advice_index
                % len(advice_list)
            )

            st.info(
                "🦆 " + DUCK_INTROS[issue_choice]
            )

            st.success(advice_list[advice_index])

            st.caption(
                st.session_state.duck_encouragement
            )

            fixed_col, struggling_col = st.columns(2)

            with fixed_col:
                if st.button(
                    "I Fixed It",
                    key="duck_fixed_it",
                    use_container_width=True,
                ):
                    st.session_state.duck_resolved = True
                    st.rerun()

            with struggling_col:
                if st.button(
                    "I'm Still Struggling",
                    key="duck_still_struggling",
                    use_container_width=True,
                ):
                    st.session_state.duck_advice_index += 1
                    st.session_state.duck_struggle_count += 1
                    st.session_state.duck_encouragement = random.choice(
                        DUCK_ENCOURAGEMENT
                    )
                    st.rerun()

            if st.session_state.duck_struggle_count >= 2:
                st.caption(
                    "The duck is still listening. Stubborn bugs do not mean "
                    "you are doing anything wrong."
                )

    st.divider()

    st.button(
        "Return to FidSync",
        key="duck_return_bottom",
        use_container_width=True,
        on_click=return_to_previous_page,
    )


if __name__ == "__main__":
    run()
