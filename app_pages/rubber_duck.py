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
        (
            "Copy the technical error into a note and identify the exception "
            "type, file name, and line number. Those three clues usually narrow "
            "the search quickly."
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
        (
            "Try a fresh browser session. Session State or caching may be "
            "holding onto an older value."
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
        (
            "Test the same action in a private window. That helps separate "
            "code problems from browser-session problems."
        ),
    ],
}


DUCK_ENCOURAGEMENT = [
    "Go try that. The duck will wait right here.",
    "You have a solid next step. Give it another shot.",
    "Try the suggestion, then come back if the bug is still being dramatic.",
    "The duck believes this is worth another attempt.",
    "One careful test at a time.",
]


DUCK_MOODS = [
    "Calm",
    "Concerned",
    "Deeply Suspicious",
    "Reviewing the Evidence",
    "Blaming the Cache",
    "Questioning Excel",
    "Emotionally Invested",
]


DUCK_DIAGNOSES = {
    "There's an error": [
        "Likely cause: a typo with excellent camouflage.",
        "Likely cause: one missing comma ruined the afternoon.",
        "Likely cause: the traceback is being more helpful than it looks.",
        "Likely cause: indentation has chosen violence.",
    ],
    "Python isn't listening": [
        "Likely cause: the wrong file is running.",
        "Likely cause: the latest change never made it into the deployed build.",
        "Likely cause: Session State remembers too much.",
        "Likely cause: caching is pretending nothing changed.",
    ],
    "Something is behaving strangely": [
        "Likely cause: Streamlit reran at the worst possible moment.",
        "Likely cause: the app is doing exactly what it was told.",
        "Likely cause: two widgets are quietly fighting.",
        "Likely cause: Excel is involved somehow.",
    ],
}


STRUGGLING_LABELS = [
    "I'm Still Struggling",
    "Still Broken",
    "Nope",
    "The Bug Won",
    "Duck, Please",
]


DUCK_PROGRESS_MESSAGES = {
    2: "🦆 The duck has moved closer to the screen.",
    4: "🦆 The duck is now emotionally invested.",
    6: "🦆 The duck would like to formally blame caching.",
}


def initialize_duck_state() -> None:
    """Initialize the debugger's session-state values."""

    defaults = {
        "duck_active_issue": "",
        "duck_advice_index": 0,
        "duck_struggle_count": 0,
        "duck_resolved": False,
        "duck_encouragement": random.choice(DUCK_ENCOURAGEMENT),
        "duck_diagnosis": "",
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
    st.session_state.duck_diagnosis = ""

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
                max-width: 900px;
                padding-top: 2rem;
                padding-bottom: 3rem;
            }

            .duck-hero {
                padding: 2.2rem 2rem;
                margin-bottom: 1.4rem;
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
                margin-bottom: 0.55rem;
                font-size: 5.2rem;
                line-height: 1;
            }

            .duck-title {
                color: #ffffff !important;
                -webkit-text-fill-color: #ffffff !important;
                font-size: 2rem;
                font-weight: 760;
                line-height: 1.2;
            }

            .duck-subtitle {
                max-width: 650px;
                margin: 0.7rem auto 0;
                color: #d8e4f2 !important;
                -webkit-text-fill-color: #d8e4f2 !important;
                font-size: 0.96rem;
                line-height: 1.6;
            }

            .duck-version {
                margin-top: 0.5rem;
                color: #9fb7d2 !important;
                -webkit-text-fill-color: #9fb7d2 !important;
                font-size: 0.71rem;
                font-weight: 650;
                letter-spacing: 0.07rem;
                text-transform: uppercase;
            }

            .duck-case-card {
                margin: 0.8rem 0 1rem 0;
                padding: 1rem 1.1rem;
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

            .duck-case-label {
                margin-bottom: 0.25rem;
                color: #718096;
                font-size: 0.7rem;
                font-weight: 700;
                letter-spacing: 0.07rem;
                text-transform: uppercase;
            }

            .duck-case-value {
                color: #102542;
                font-size: 0.92rem;
                font-weight: 700;
                line-height: 1.45;
            }

            div[data-testid="stRadio"] {
                padding: 0.2rem 0 0.5rem 0;
            }

            div[data-testid="stAlert"] {
                border-radius: 0.75rem;
            }

            div[data-testid="stMetric"] {
                background: #ffffff;
                border: 1px solid #dce3ec;
                border-radius: 0.75rem;
                padding: 0.85rem 1rem;
                box-shadow: 0 2px 8px rgba(16, 37, 66, 0.04);
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
    """Render the Duck Debugger header."""

    header_html = (
        '<div class="duck-hero">'
        '<div class="duck-icon">🦆</div>'
        '<div class="duck-title">Duck Debugger</div>'
        '<div class="duck-subtitle">'
        'Choose the closest description of the problem. '
        'The duck will keep offering suggestions until something works.'
        '</div>'
        '<div class="duck-version">Highly Experimental · v0.2</div>'
        '</div>'
    )

    st.markdown(
        header_html,
        unsafe_allow_html=True,
    )


def get_duck_mood(struggle_count: int) -> str:
    """Return a mood based on how many attempts have been made."""

    mood_index = min(
        struggle_count,
        len(DUCK_MOODS) - 1,
    )

    return DUCK_MOODS[mood_index]


def get_struggling_label(struggle_count: int) -> str:
    """Return a more dramatic button label as attempts increase."""

    label_index = min(
        struggle_count,
        len(STRUGGLING_LABELS) - 1,
    )

    return STRUGGLING_LABELS[label_index]


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
            st.session_state.duck_diagnosis = random.choice(
                DUCK_DIAGNOSES[issue_choice]
            )

        if st.session_state.duck_resolved:
            st.markdown(
                """
                <div class="duck-case-card">
                    <div class="duck-case-label">
                        Case Status
                    </div>
                    <div class="duck-case-value">
                        Closed successfully.
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.success("🦆 The duck knew you could do it.")

            st.markdown(
                "### Case closed."
            )

            st.write(
                "Debugging is not about never getting stuck. "
                "It is about getting unstuck."
            )

            st.caption(
                "Official cause: persistence."
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

            mood_col, attempts_col = st.columns(2)

            with mood_col:
                st.metric(
                    "Duck Mood",
                    get_duck_mood(
                        st.session_state.duck_struggle_count
                    ),
                )

            with attempts_col:
                st.metric(
                    "Attempts",
                    st.session_state.duck_struggle_count + 1,
                )

            diagnosis_html = (
                '<div class="duck-case-card">'
                '<div class="duck-case-label">Preliminary Diagnosis</div>'
                f'<div class="duck-case-value">'
                f'{st.session_state.duck_diagnosis}'
                '</div>'
                '</div>'
            )

            st.markdown(
                diagnosis_html,
                unsafe_allow_html=True,
            )

            st.info(
                "🦆 " + DUCK_INTROS[issue_choice]
            )

            st.success(advice_list[advice_index])

            st.caption(
                st.session_state.duck_encouragement
            )

            struggle_count = st.session_state.duck_struggle_count

            if struggle_count in DUCK_PROGRESS_MESSAGES:
                st.info(
                    DUCK_PROGRESS_MESSAGES[struggle_count]
                )
            elif struggle_count > 6:
                st.info(
                    "🦆 The duck has opened a second monitor."
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
                    get_struggling_label(struggle_count),
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
