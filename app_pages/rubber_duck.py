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
        "Suspicious. Let’s slow this down and figure out what the app is "
        "actually doing."
    ),
}


DUCK_ADVICE = {
    "There's an error": [
        (
            "Read the traceback from the bottom upward and find the first "
            "line pointing to your own file."
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
            "Compare the broken version to the last version that worked. "
            "The smallest difference is probably the useful clue."
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


def initialize_duck_state():
    defaults = {
        "duck_active_issue": "",
        "duck_advice_index": 0,
        "duck_struggle_count": 0,
        "duck_resolved": False,
        "duck_celebrated": False,
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def reset_duck():
    st.session_state.duck_active_issue = ""
    st.session_state.duck_advice_index = 0
    st.session_state.duck_struggle_count = 0
    st.session_state.duck_resolved = False
    st.session_state.duck_celebrated = False

    if "duck_issue_choice" in st.session_state:
        del st.session_state["duck_issue_choice"]


def return_to_previous_page():
    previous_page = st.session_state.get(
        "duck_previous_page",
        "Getting_Started.py",
    )

    st.query_params["page"] = previous_page
    st.rerun()


def run():
    initialize_duck_state()

    st.markdown(
        """
        <style>
            .block-container {
                max-width: 850px;
                padding-top: 2rem;
                padding-bottom: 3rem;
            }

            .duck-header {
                padding: 2rem;
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
                margin-bottom: 0.65rem;
                font-size: 5rem;
                line-height: 1;
            }

            .duck-title {
                color: #ffffff !important;
                -webkit-text-fill-color: #ffffff !important;
                font-size: 2rem;
                font-weight: 750;
            }

            .duck-description {
                max-width: 600px;
                margin: 0.65rem auto 0;
                color: #d8e4f2 !important;
                -webkit-text-fill-color: #d8e4f2 !important;
                font-size: 0.95rem;
                line-height: 1.6;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="duck-header">
            <div class="duck-icon">🦆</div>

            <div class="duck-title">
                Rubber Duck Debugger
            </div>

            <div class="duck-description">
                Choose the closest description of the problem. The duck will
                offer suggestions until something works.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    issue_choice = st.radio(
        "What’s going wrong?",
        DUCK_ISSUES,
        key="duck_issue_choice",
    )

    if issue_choice != "Choose one...":
        if issue_choice != st.session_state.duck_active_issue:
            st.session_state.duck_active_issue = issue_choice
            st.session_state.duck_advice_index = 0
            st.session_state.duck_struggle_count = 0
            st.session_state.duck_resolved = False
            st.session_state.duck_celebrated = False

        if st.session_state.duck_resolved:
            if not st.session_state.duck_celebrated:
                st.balloons()
                st.session_state.duck_celebrated = True

            st.success("🦆 The duck knew you could do it.")
            st.caption("The official diagnosis was persistence.")

            button_col1, button_col2 = st.columns(2)

            with button_col1:
                if st.button(
                    "Debug Another Problem",
                    use_container_width=True,
                ):
                    reset_duck()
                    st.rerun()

            with button_col2:
                if st.button(
                    "Return to FidSync",
                    use_container_width=True,
                ):
                    return_to_previous_page()

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
                random.choice(DUCK_ENCOURAGEMENT)
            )

            fixed_col, struggling_col = st.columns(2)

            with fixed_col:
                if st.button(
                    "I Fixed It",
                    use_container_width=True,
                ):
                    st.session_state.duck_resolved = True
                    st.rerun()

            with struggling_col:
                if st.button(
                    "I’m Still Struggling",
                    use_container_width=True,
                ):
                    st.session_state.duck_advice_index += 1
                    st.session_state.duck_struggle_count += 1
                    st.rerun()

            if st.session_state.duck_struggle_count >= 2:
                st.caption(
                    "The duck is still listening. Stubborn bugs do not mean "
                    "you are doing anything wrong."
                )

    st.divider()

    if st.button(
        "Return to FidSync",
        key="duck_return_bottom",
        use_container_width=True,
    ):
        return_to_previous_page()


if __name__ == "__main__":
    run()
