# app_pages/rubber_duck.py

import random

import streamlit as st


DUCK_ISSUES = [
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
        "Read the traceback from the bottom upward and find the first line "
        "that points to your own file.",
        "Check the exact line named in the traceback for a misspelled "
        "variable, missing comma, unmatched quote, or indentation issue.",
        "Add one st.write() immediately before the failing line so you can "
        "see the value and type Python is receiving.",
        "Comment out the newest code and restore it a few lines at a time "
        "until the error returns.",
        "Compare the broken version with the last version that worked. The "
        "smallest difference is usually the useful clue.",
        "Copy the technical error into a note and identify the exception "
        "type, file name, and line number.",
    ],
    "Python isn't listening": [
        "Save the file, confirm you edited the exact file the router loads, "
        "and reboot the Streamlit app.",
        "Check the filename and capitalization. A second copy in another "
        "folder can make your changes appear invisible.",
        "Add st.success('NEW CODE IS RUNNING') temporarily to verify which "
        "file Streamlit is loading.",
        "Make sure the function containing your new code is actually being "
        "called.",
        "Open the deployed file on GitHub and confirm the latest commit "
        "contains your changes.",
        "Try a fresh browser session. Session State or caching may be holding "
        "onto an older value.",
    ],
    "Something is behaving strangely": [
        "Write down what you expected to happen and what actually happened. "
        "The difference is your first clue.",
        "Change only one thing at a time. Multiple fixes make it harder to "
        "tell which change mattered.",
        "Inspect the values immediately before the strange behavior using "
        "st.write().",
        "Reduce the problem to the smallest possible example that still "
        "behaves incorrectly.",
        "Check whether a Streamlit rerun or Session State value is resetting "
        "the widget.",
        "Test the same action in a private window to separate code problems "
        "from browser-session problems.",
    ],
}


DUCK_CONVERSATION = [
    (
        "Okay...",
        "Let's try something simpler. What was the last thing you changed "
        "before it broke?"
    ),
    (
        "Hmm...",
        "Can you make the bug happen with the smallest possible example? "
        "Removing extra code is progress, even before the bug is fixed."
    ),
    (
        "I have a question.",
        "Are you completely sure the file you are editing is the file that "
        "is actually running?"
    ),
    (
        "New theory.",
        "Add one print() or st.write(). Not five. One. Then run it again."
    ),
    (
        "At this point...",
        "The duck would like to respectfully blame caching. Not officially. "
        "But emotionally."
    ),
    (
        "...",
        "The duck has stopped pretending this is a quick fix. We are in this "
        "together now."
    ),
    (
        "Debugging glasses activated.",
        "Read the traceback again, but this time pretend it was written for "
        "someone else. What would you tell them to check first?"
    ),
    (
        "Emergency protocol.",
        "Save the file. Restart Streamlit. Confirm the file path. Read the "
        "traceback. Then take one sip of water."
    ),
    (
        "Diagnosis update.",
        "This bug appears to be advanced. That still does not make it "
        "invincible."
    ),
    (
        "Morale report.",
        "Developer morale: 12%. Duck morale: 98%. Continue carefully."
    ),
]


DUCK_REACTIONS = [
    "🦆",
    "🤔🦆",
    "🧐🦆",
    "😐🦆",
    "🥴🦆",
    "👑🦆",
]


DUCK_TITLES = [
    (0, "Rubber Duck"),
    (2, "Senior Duck"),
    (4, "Principal Duck"),
    (7, "Distinguished Duck"),
    (11, "Legendary Duck"),
    (17, "Duck of Infinite Patience"),
]


DUCK_STATUS_NAMES = {
    "🦆": "Calm",
    "🤔🦆": "Thinking",
    "🧐🦆": "Reviewing the Evidence",
    "😐🦆": "Slightly Concerned",
    "🥴🦆": "Questioning Reality",
    "👑🦆": "Debug Master",
}


STRUGGLING_LABELS = [
    "I'm Still Struggling",
    "Still Broken",
    "Nope",
    "The Bug Won",
    "Duck, Please",
    "Nothing Changed",
]


def initialize_duck_state() -> None:
    """Initialize the debugger's session-state values."""

    defaults = {
        "duck_active_issue": "",
        "duck_advice_index": 0,
        "duck_struggle_count": 0,
        "duck_resolved": False,
        "duck_achievement_shown": False,
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def reset_duck() -> None:
    """Reset the debugger safely."""

    st.session_state.duck_active_issue = ""
    st.session_state.duck_advice_index = 0
    st.session_state.duck_struggle_count = 0
    st.session_state.duck_resolved = False
    st.session_state.duck_achievement_shown = False
    st.session_state.pop("duck_issue_choice", None)


def return_to_previous_page() -> None:
    """Return to whichever FidSync page opened the debugger."""

    previous_page = st.session_state.get(
        "duck_previous_page",
        "Getting_Started.py",
    )
    st.query_params["page"] = previous_page


def get_duck_reaction(struggle_count: int) -> str:
    """Return a more dramatic duck as the struggle count grows."""

    if struggle_count >= 15:
        return DUCK_REACTIONS[-1]
    if struggle_count >= 10:
        return DUCK_REACTIONS[4]
    if struggle_count >= 7:
        return DUCK_REACTIONS[2]
    if struggle_count >= 5:
        return DUCK_REACTIONS[3]
    if struggle_count >= 2:
        return DUCK_REACTIONS[1]
    return DUCK_REACTIONS[0]


def get_duck_title(struggle_count: int) -> str:
    """Return the duck's increasingly senior title."""

    current_title = DUCK_TITLES[0][1]

    for threshold, title in DUCK_TITLES:
        if struggle_count >= threshold:
            current_title = title

    return current_title


def get_struggling_label(struggle_count: int) -> str:
    """Return a changing label for the struggle button."""

    index = min(
        struggle_count,
        len(STRUGGLING_LABELS) - 1,
    )
    return STRUGGLING_LABELS[index]


def apply_styles() -> None:
    """Apply page styling."""

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

            .duck-status-bar {
                display: flex;
                align-items: center;
                justify-content: space-between;
                gap: 1rem;
                margin: 0 0 1.2rem 0;
                padding: 0.65rem 0.9rem;
                background-color: #f7fafd;
                border: 1px solid #d6e2ee;
                border-radius: 0.7rem;
                color: #50657b;
                font-size: 0.82rem;
                line-height: 1.4;
            }

            .duck-status-left {
                display: flex;
                align-items: center;
                gap: 0.45rem;
                min-width: 0;
            }

            .duck-status-name {
                color: #102542;
                font-weight: 750;
            }

            .duck-attempt {
                flex-shrink: 0;
                color: #365574;
                font-weight: 700;
            }

            .duck-dialogue {
                margin: 0.8rem 0 1rem 0;
                padding: 1.15rem 1.2rem;
                background: linear-gradient(135deg, #f7fafd, #edf3fa);
                border: 1px solid #cfdae8;
                border-left: 4px solid #2b6cb0;
                border-radius: 0.75rem;
            }

            .duck-dialogue-title {
                margin-bottom: 0.35rem;
                color: #102542;
                font-size: 0.98rem;
                font-weight: 750;
            }

            .duck-dialogue-text {
                color: #50657b;
                font-size: 0.9rem;
                line-height: 1.6;
            }

            .duck-achievement {
                margin-top: 1rem;
                padding: 1rem;
                text-align: center;
                background-color: #fff9e8;
                border: 1px solid #ead9a7;
                border-radius: 0.75rem;
            }

            .duck-achievement-title {
                color: #755c14;
                font-size: 0.72rem;
                font-weight: 750;
                letter-spacing: 0.07rem;
                text-transform: uppercase;
            }

            .duck-achievement-name {
                margin-top: 0.25rem;
                color: #4f431f;
                font-size: 1.05rem;
                font-weight: 750;
            }

            .stButton > button {
                border-radius: 0.6rem;
                font-weight: 650;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_header(struggle_count: int) -> None:
    """Render the page header."""

    duck_title = get_duck_title(struggle_count)

    header_html = (
        '<div class="duck-hero">'
        f'<div class="duck-icon">{get_duck_reaction(struggle_count)}</div>'
        f'<div class="duck-title">{duck_title}</div>'
        '<div class="duck-subtitle">'
        'Choose the closest description below. The duck will keep changing '
        'its approach until something works.'
        '</div>'
        '<div class="duck-version">Highly Experimental · v0.3</div>'
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
    render_header(st.session_state.duck_struggle_count)

    st.markdown("### What's going wrong?")
    st.caption("Choose the option that most closely matches the problem.")

    issue_choice = st.radio(
        "Problem type",
        DUCK_ISSUES,
        index=None,
        key="duck_issue_choice",
        label_visibility="collapsed",
    )

    if issue_choice is None:
        st.info(
            "Choose one of the three options above and the duck will begin."
        )

    elif issue_choice != st.session_state.duck_active_issue:
        st.session_state.duck_active_issue = issue_choice
        st.session_state.duck_advice_index = 0
        st.session_state.duck_struggle_count = 0
        st.session_state.duck_resolved = False
        st.session_state.duck_achievement_shown = False
        st.rerun()

    elif st.session_state.duck_resolved:
        st.success("🦆 The duck knew you could do it.")

        st.markdown("## Case closed.")

        st.write(
            "Debugging is not about never getting stuck. "
            "It is about getting unstuck."
        )

        st.markdown(
            """
            <div class="duck-dialogue">
                <div class="duck-dialogue-title">
                    Final Report
                </div>
                <div class="duck-dialogue-text">
                    Bug status: resolved.<br>
                    Duck satisfaction: 100%.<br>
                    Developer confidence: +15.<br>
                    Patience: +50.<br>
                    Coffee consumed: unknown.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
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
        struggle_count = st.session_state.duck_struggle_count

        duck_reaction = get_duck_reaction(struggle_count)
        duck_status_name = DUCK_STATUS_NAMES[duck_reaction]
        duck_title = get_duck_title(struggle_count)

        status_html = (
            '<div class="duck-status-bar">'
            '<div class="duck-status-left">'
            f'<span>{duck_reaction}</span>'
            f'<span class="duck-status-name">{duck_title}</span>'
            f'<span>· {duck_status_name}</span>'
            '</div>'
            f'<div class="duck-attempt">Attempt {struggle_count + 1}</div>'
            '</div>'
        )

        st.markdown(
            status_html,
            unsafe_allow_html=True,
        )

        if struggle_count == 0:
            dialogue_title = "Initial Assessment"
            dialogue_text = DUCK_INTROS[issue_choice]
        else:
            conversation_index = min(
                struggle_count - 1,
                len(DUCK_CONVERSATION) - 1,
            )
            dialogue_title, dialogue_text = DUCK_CONVERSATION[
                conversation_index
            ]

        dialogue_html = (
            '<div class="duck-dialogue">'
            f'<div class="duck-dialogue-title">{dialogue_title}</div>'
            f'<div class="duck-dialogue-text">{dialogue_text}</div>'
            '</div>'
        )
        st.markdown(dialogue_html, unsafe_allow_html=True)

        st.info("Try this next:")
        st.success(advice_list[advice_index])
        st.caption("Go try it. The duck will keep your place.")

        if struggle_count == 7:
            st.info("🧐 Debugging glasses activated.")
        elif struggle_count == 8:
            st.warning(
                "Emergency protocol: save, restart, verify the file path, "
                "read the traceback, and take one sip of water."
            )
        elif struggle_count == 9:
            st.info("✨ This bug appears to be advanced.")
        elif struggle_count >= 10:
            morale = max(1, 100 - (struggle_count * 9))
            st.progress(
                morale / 100,
                text=f"Developer morale: {morale}% · Duck morale: 98%",
            )

        if struggle_count >= 12:
            st.markdown(
                """
                <div class="duck-achievement">
                    <div class="duck-achievement-title">
                        Achievement Unlocked
                    </div>
                    <div class="duck-achievement-name">
                        🏆 Persistent Debugger
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
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
                st.rerun()

        if struggle_count >= 2:
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
