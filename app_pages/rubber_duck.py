# app_pages/rubber_duck.py

import random

import streamlit as st


DUCK_ISSUES = [
    "There's an error",
    "My changes aren't showing up",
    "The app keeps doing the wrong thing",
    "Something looks weird",
    "It's painfully slow",
    "The numbers don't make sense",
    "I honestly have no idea",
]


DUCK_INTROS = {
    "There's an error": (
        "Errors are rude, but they usually leave evidence. Let's begin with "
        "the part of the traceback that points to your own code."
    ),
    "My changes aren't showing up": (
        "The code may be correct while the app is still running another file, "
        "an older version, cached output, or a stored Session State value."
    ),
    "The app keeps doing the wrong thing": (
        "The app is following some instruction perfectly. Our job is to find "
        "the instruction that does not match what you intended."
    ),
    "Something looks weird": (
        "Visual problems are usually caused by layout, styling, container "
        "width, or one rule overriding another. Let's isolate the layer."
    ),
    "It's painfully slow": (
        "Slow code needs timing evidence. We will find the expensive step "
        "instead of guessing which part is responsible."
    ),
    "The numbers don't make sense": (
        "Incorrect results usually begin earlier than they first become "
        "visible. Let's check the data one transformation at a time."
    ),
    "I honestly have no idea": (
        "That is a valid starting point. We do not need the diagnosis yet; "
        "we only need one repeatable observation."
    ),
}


DUCK_ADVICE = {
    "There's an error": [
        "Read the traceback from the bottom upward. Find the first line that "
        "points to a file you wrote, then inspect that exact line.",
        "Check the named line for a misspelled variable, missing comma, "
        "unmatched quote, incorrect indentation, or a value with the wrong type.",
        "Add one st.write() directly before the failing line. Display both the "
        "value and its type, then repeat the same action.",
        "Temporarily comment out the newest code. Restore it a few lines at a "
        "time until the error returns.",
        "Compare the broken version with the last version that worked. Focus on "
        "the smallest difference instead of rereading the entire file.",
        "Write down the exception type, file name, line number, and exact action "
        "that causes it. That turns the error into a reproducible case.",
    ],
    "My changes aren't showing up": [
        "Save the file and confirm you edited the exact file loaded by the page "
        "router. Then restart the Streamlit app.",
        "Check the filename, capitalization, and folder. A duplicate file can "
        "make correct changes appear invisible.",
        "Temporarily add st.success('NEW CODE IS RUNNING') near the top of the "
        "page to verify which file Streamlit is loading.",
        "Confirm the function containing your new code is actually called. Code "
        "inside an unused function will never appear.",
        "Check the deployed file or latest GitHub commit and confirm it contains "
        "the same change as your local copy.",
        "Open a private browser window or clear the relevant Session State value "
        "to separate code problems from stored browser-session behavior.",
        "Temporarily disable the relevant cache decorator. If the change appears, "
        "the app was reusing an older cached result.",
    ],
    "The app keeps doing the wrong thing": [
        "Write one sentence describing what should happen and one describing "
        "what actually happens. Make the difference as specific as possible.",
        "Follow the action from the widget to its callback and then to each "
        "Session State assignment. Look for a later line that changes it again.",
        "Add one st.write() immediately before the incorrect behavior. Display "
        "the exact inputs the app is using at that moment.",
        "Check every condition involved in the behavior. Print which branch of "
        "the if/elif/else block actually runs.",
        "Perform the action once and watch for a Streamlit rerun. A value may be "
        "correct briefly and then reset during the next run.",
        "Remove unrelated callbacks and state updates until the smallest version "
        "of the feature still performs the wrong action.",
        "Check for reused widget keys. Two widgets sharing a key can produce "
        "behavior that appears unrelated to either widget.",
    ],
    "Something looks weird": [
        "Temporarily remove custom CSS. If the layout becomes normal, add the "
        "rules back one section at a time.",
        "Inspect the page at a narrower and wider browser size. The issue may be "
        "a fixed width, overflowing content, or columns becoming too cramped.",
        "Check for repeated margins, padding, dividers, captions, or empty "
        "containers. The visual problem may simply be stacked spacing.",
        "Use the browser inspector to find which CSS rule is controlling the "
        "element. Look for a rule that is crossed out or unexpectedly inherited.",
        "Test the page in both light and dark mode. Hard-coded text or background "
        "colors can disappear or clash in one mode.",
        "Replace the suspicious section with plain st.write() content. If that "
        "looks correct, rebuild the styling around the working structure.",
        "Check whether the same button, heading, or divider is rendered in more "
        "than one conditional branch.",
    ],
    "It's painfully slow": [
        "Time the major steps separately. Record how long loading, cleaning, "
        "calculating, charting, and exporting each take.",
        "Check whether a large file, API call, or database query runs again on "
        "every Streamlit rerun.",
        "Cache expensive read-only work with st.cache_data, but do not cache code "
        "that must reflect immediate changes or user-specific state.",
        "Look for loops that repeatedly filter, append to, or rebuild a dataframe. "
        "Try to perform the operation once on the full column instead.",
        "Display the dataframe shape before expensive operations. You may be "
        "processing far more rows or columns than expected.",
        "Temporarily remove charts, formatting, and export creation. Add them back "
        "one at a time to identify the slow layer.",
        "Check whether clicking a download button rebuilds the file. Prepare the "
        "download data only when its inputs change, not on every rerun.",
    ],
    "The numbers don't make sense": [
        "Choose one incorrect row and calculate the expected result manually. "
        "Use that row as the test case for every step.",
        "Display the row count and key totals before and after each merge, filter, "
        "groupby, or pivot. Find the first step where they change unexpectedly.",
        "Check the column data types. Numbers stored as text can sort, compare, "
        "and calculate incorrectly.",
        "Inspect missing values, zeros, duplicates, and negative numbers in the "
        "columns used by the calculation.",
        "Check whether percentages are represented as 5, 0.05, or the text '5%'. "
        "A scale mismatch can make a correct formula look wildly wrong.",
        "Verify the merge keys and merge type. Duplicate keys can multiply rows "
        "and inflate totals without producing an error.",
        "Round only for display. Rounding during intermediate calculations can "
        "create differences that grow across many rows.",
        "Compare the source value, cleaned value, and final value side by side for "
        "one record to identify where the number first changes.",
    ],
    "I honestly have no idea": [
        "Repeat the problem and write down the exact clicks or inputs required to "
        "make it happen. Reproducibility is the first clue.",
        "Describe the last moment when the app still behaves normally. Then note "
        "the first moment when something feels wrong.",
        "Ask which category is closest: an error, an invisible change, a wrong "
        "action, a visual issue, slowness, or incorrect data.",
        "Undo or comment out only the most recent change, then test again. Do not "
        "change anything else during that test.",
        "Add one checkpoint at the beginning of the feature and one at the end. "
        "Confirm whether the code reaches both places.",
        "Try the same action with the smallest possible input. A simpler example "
        "often reveals whether the issue is code, data, or state.",
        "Restart the app and repeat the problem in a private browser window. This "
        "separates persistent code problems from temporary session behavior.",
        "Explain the feature out loud from input to output. The step you cannot "
        "explain clearly is probably the next place to inspect.",
    ],
}


DUCK_CONVERSATION = [
    (
        "Let's narrow it down.",
        "What was the last thing you changed before the problem appeared? Start "
        "there, even if the change seems unrelated.",
    ),
    (
        "Smaller is better.",
        "Can you reproduce the problem with less code? Removing unrelated pieces "
        "is progress, even before the bug is fixed.",
    ),
    (
        "File check.",
        "Are you completely sure the file you are editing is the file that is "
        "actually running? The duck has been fooled by duplicate files before.",
    ),
    (
        "New theory.",
        "Add one print() or st.write(). Not five. One useful checkpoint, then run "
        "the exact same action again.",
    ),
    (
        "Caching has entered the conversation.",
        "The duck would like to blame caching. Not officially, but with growing "
        "confidence.",
    ),
    (
        "This is no longer a quick fix.",
        "That is fine. A stubborn bug is still just a sequence of smaller facts "
        "you have not isolated yet.",
    ),
    (
        "Debugging glasses activated.",
        "Read the evidence as though someone else sent it to you. What would you "
        "tell them to verify first?",
    ),
    (
        "Emergency protocol.",
        "Save the file. Restart Streamlit. Confirm the path. Reproduce the issue. "
        "Check the evidence. Then take one sip of water.",
    ),
    (
        "Advanced bug confirmed.",
        "Advanced does not mean invincible. It means the next test needs to be "
        "more specific than the last one.",
    ),
    (
        "Morale report.",
        "Developer morale is under review. Duck morale remains suspiciously high.",
    ),
]


DUCK_REACTIONS = ["🦆", "🤔🦆", "😐🦆", "🧐🦆", "🥴🦆", "👑🦆"]


DUCK_STATUS_NAMES = {
    "🦆": "Calm",
    "🤔🦆": "Thinking",
    "😐🦆": "Slightly Concerned",
    "🧐🦆": "Reviewing the Evidence",
    "🥴🦆": "Questioning Reality",
    "👑🦆": "Still Committed",
}


STRUGGLING_LABELS = [
    "Try Another Idea",
    "Still Broken",
    "No Change",
    "Duck, Please",
    "We Need a New Theory",
    "Escalate This Bug",
]


def initialize_duck_state() -> None:
    """Initialize all session-state values used by the debugger."""

    defaults = {
        "duck_active_issue": None,
        "duck_advice_order": [],
        "duck_advice_position": 0,
        "duck_struggle_count": 0,
        "duck_resolved": False,
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def build_advice_order(issue: str) -> list[int]:
    """Return a shuffled list of advice indexes for the selected issue."""

    order = list(range(len(DUCK_ADVICE[issue])))
    random.shuffle(order)
    return order


def start_issue(issue: str) -> None:
    """Start a fresh debugging session for the selected issue."""

    st.session_state.duck_active_issue = issue
    st.session_state.duck_advice_order = build_advice_order(issue)
    st.session_state.duck_advice_position = 0
    st.session_state.duck_struggle_count = 0
    st.session_state.duck_resolved = False


def reset_duck() -> None:
    """Reset the debugger to its untouched state."""

    st.session_state.duck_active_issue = None
    st.session_state.duck_advice_order = []
    st.session_state.duck_advice_position = 0
    st.session_state.duck_struggle_count = 0
    st.session_state.duck_resolved = False
    st.session_state.pop("duck_issue_choice", None)
    st.session_state.pop("duck_issue_change", None)


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
        return DUCK_REACTIONS[5]
    if struggle_count >= 10:
        return DUCK_REACTIONS[4]
    if struggle_count >= 7:
        return DUCK_REACTIONS[3]
    if struggle_count >= 4:
        return DUCK_REACTIONS[2]
    if struggle_count >= 2:
        return DUCK_REACTIONS[1]
    return DUCK_REACTIONS[0]


def get_struggling_label(struggle_count: int) -> str:
    """Return a changing label for the next-advice button."""

    index = min(struggle_count, len(STRUGGLING_LABELS) - 1)
    return STRUGGLING_LABELS[index]


def get_current_advice(issue: str) -> str:
    """Return the current suggestion from the shuffled advice order."""

    order = st.session_state.duck_advice_order
    if not order:
        order = build_advice_order(issue)
        st.session_state.duck_advice_order = order

    position = st.session_state.duck_advice_position % len(order)
    advice_index = order[position]
    return DUCK_ADVICE[issue][advice_index]


def advance_duck() -> None:
    """Move to another suggestion and increase the attempt count."""

    issue = st.session_state.duck_active_issue
    st.session_state.duck_struggle_count += 1
    st.session_state.duck_advice_position += 1

    if (
        issue
        and st.session_state.duck_advice_position
        >= len(st.session_state.duck_advice_order)
    ):
        st.session_state.duck_advice_order = build_advice_order(issue)
        st.session_state.duck_advice_position = 0


def apply_styles() -> None:
    """Apply page-specific styling without changing the app sidebar."""

    st.markdown(
        """
        <style>
            .block-container {
                max-width: 860px;
                padding-top: 1.6rem;
                padding-bottom: 2.5rem;
            }

            .duck-hero {
                position: relative;
                overflow: hidden;
                padding: 1.7rem 1.6rem;
                margin-bottom: 1.25rem;
                text-align: center;
                background:
                    radial-gradient(
                        circle at 84% 12%,
                        rgba(147, 184, 225, 0.27),
                        transparent 31%
                    ),
                    linear-gradient(135deg, #102542 0%, #213b5c 100%);
                border: 1px solid #2d496b;
                border-radius: 0.95rem;
                box-shadow: 0 10px 28px rgba(16, 37, 66, 0.12);
            }

            .duck-icon {
                margin-bottom: 0.35rem;
                font-size: 4rem;
                line-height: 1;
            }

            .duck-title {
                color: #ffffff !important;
                -webkit-text-fill-color: #ffffff !important;
                font-size: 1.75rem;
                font-weight: 760;
                line-height: 1.2;
            }

            .duck-subtitle {
                max-width: 620px;
                margin: 0.55rem auto 0;
                color: #d8e4f2 !important;
                -webkit-text-fill-color: #d8e4f2 !important;
                font-size: 0.92rem;
                line-height: 1.55;
            }

            .duck-version {
                margin-top: 0.5rem;
                color: #9fb7d2 !important;
                -webkit-text-fill-color: #9fb7d2 !important;
                font-size: 0.67rem;
                font-weight: 700;
                letter-spacing: 0.07rem;
                text-transform: uppercase;
            }

            .duck-status-bar {
                display: flex;
                align-items: center;
                justify-content: space-between;
                gap: 0.85rem;
                margin: 0.9rem 0 0.85rem;
                padding: 0.6rem 0.8rem;
                background-color: #f7fafd;
                border: 1px solid #d6e2ee;
                border-radius: 0.65rem;
                color: #50657b;
                font-size: 0.79rem;
                line-height: 1.35;
            }

            .duck-status-left {
                display: flex;
                align-items: center;
                gap: 0.4rem;
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
                margin: 0 0 0.9rem;
                padding: 1rem 1.05rem;
                background: linear-gradient(135deg, #f8fbfe, #edf3fa);
                border: 1px solid #cfdae8;
                border-left: 4px solid #2b6cb0;
                border-radius: 0.7rem;
            }

            .duck-dialogue-title {
                margin-bottom: 0.28rem;
                color: #102542;
                font-size: 0.93rem;
                font-weight: 760;
            }

            .duck-dialogue-text {
                color: #50657b;
                font-size: 0.88rem;
                line-height: 1.55;
            }

            .duck-next-step {
                margin: 0.75rem 0 0.45rem;
                padding: 1rem 1.05rem;
                background-color: #ffffff;
                border: 1px solid #cbd9e7;
                border-radius: 0.72rem;
                box-shadow: 0 4px 14px rgba(16, 37, 66, 0.06);
            }

            .duck-next-label {
                margin-bottom: 0.32rem;
                color: #2b6cb0;
                font-size: 0.69rem;
                font-weight: 800;
                letter-spacing: 0.07rem;
                text-transform: uppercase;
            }

            .duck-next-text {
                color: #253b52;
                font-size: 0.95rem;
                font-weight: 600;
                line-height: 1.55;
            }

            .duck-achievement {
                margin: 0.9rem 0;
                padding: 0.85rem;
                text-align: center;
                background-color: #fff9e8;
                border: 1px solid #ead9a7;
                border-radius: 0.7rem;
            }

            .duck-achievement-title {
                color: #755c14;
                font-size: 0.68rem;
                font-weight: 800;
                letter-spacing: 0.07rem;
                text-transform: uppercase;
            }

            .duck-achievement-name {
                margin-top: 0.2rem;
                color: #4f431f;
                font-size: 0.98rem;
                font-weight: 750;
            }

            div[data-testid="stRadio"] > div {
                gap: 0.45rem;
            }

            div[data-testid="stRadio"] label {
                padding: 0.35rem 0;
            }

            .stButton > button {
                min-height: 2.7rem;
                border-radius: 0.58rem;
                font-weight: 680;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_header(struggle_count: int) -> None:
    """Render the compact page header."""

    reaction = get_duck_reaction(struggle_count)

    st.markdown(
        f"""
        <div class="duck-hero">
            <div class="duck-icon">{reaction}</div>
            <div class="duck-title">Rubber Duck Debugger</div>
            <div class="duck-subtitle">
                Choose the closest problem below. The duck will give you one
                specific test at a time and change its approach when the problem
                is still broken.
            </div>
            <div class="duck-version">Highly Experimental · v0.5</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_issue_selector() -> None:
    """Render the initial issue selector."""

    st.markdown("### What kind of problem are you dealing with?")
    st.caption("Select the closest match. You can change it later.")

    issue_choice = st.radio(
        "Problem type",
        DUCK_ISSUES,
        index=None,
        key="duck_issue_choice",
        label_visibility="collapsed",
    )

    if issue_choice is None:
        st.markdown(
            """
            <div class="duck-dialogue">
                <div class="duck-dialogue-title">The duck is ready.</div>
                <div class="duck-dialogue-text">
                    Nothing has started yet. Choose one option above when you
                    are ready to begin debugging.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    if issue_choice != st.session_state.duck_active_issue:
        start_issue(issue_choice)
        st.rerun()


def render_status(struggle_count: int) -> None:
    """Render a small status strip above the active debugging content."""

    reaction = get_duck_reaction(struggle_count)
    status_name = DUCK_STATUS_NAMES[reaction]

    st.markdown(
        f"""
        <div class="duck-status-bar">
            <div class="duck-status-left">
                <span>{reaction}</span>
                <span class="duck-status-name">{status_name}</span>
            </div>
            <div class="duck-attempt">Attempt {struggle_count + 1}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_active_session(issue: str) -> None:
    """Render the active debugging workflow."""

    struggle_count = st.session_state.duck_struggle_count
    render_status(struggle_count)

    st.caption(f"Current problem: {issue}")

    if struggle_count == 0:
        dialogue_title = "Initial assessment"
        dialogue_text = DUCK_INTROS[issue]
    else:
        conversation_index = min(
            struggle_count - 1,
            len(DUCK_CONVERSATION) - 1,
        )
        dialogue_title, dialogue_text = DUCK_CONVERSATION[conversation_index]

    st.markdown(
        f"""
        <div class="duck-dialogue">
            <div class="duck-dialogue-title">{dialogue_title}</div>
            <div class="duck-dialogue-text">{dialogue_text}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    current_advice = get_current_advice(issue)
    st.markdown(
        f"""
        <div class="duck-next-step">
            <div class="duck-next-label">Try this next</div>
            <div class="duck-next-text">{current_advice}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.caption("Test only this step, then tell the duck what happened.")

    if struggle_count >= 10:
        morale = max(3, 100 - (struggle_count * 8))
        st.progress(
            morale / 100,
            text=f"Developer morale: {morale}% · Duck morale: 98%",
        )

    if struggle_count >= 12:
        st.markdown(
            """
            <div class="duck-achievement">
                <div class="duck-achievement-title">Achievement unlocked</div>
                <div class="duck-achievement-name">🏆 Persistent Debugger</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    fixed_col, struggling_col = st.columns(2)

    with fixed_col:
        if st.button(
            "It Worked",
            key="duck_fixed_it",
            type="primary",
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
            advance_duck()
            st.rerun()

    if struggle_count >= 2:
        st.caption(
            "A stubborn bug does not mean you are doing anything wrong. It only "
            "means the last test ruled something out."
        )

    with st.expander("Change the problem type"):
        new_issue = st.radio(
            "Choose a different problem",
            DUCK_ISSUES,
            index=DUCK_ISSUES.index(issue),
            key="duck_issue_change",
        )
        if new_issue != issue:
            start_issue(new_issue)
            st.session_state.duck_issue_choice = new_issue
            st.rerun()


def render_success() -> None:
    """Render the resolved state."""

    struggle_count = st.session_state.duck_struggle_count
    reaction = get_duck_reaction(max(struggle_count, 2))

    st.success("The problem is fixed. The duck accepts partial credit.")
    st.markdown("## Case closed")
    st.write(
        "Debugging is not about never getting stuck. It is about testing one "
        "useful theory at a time until the problem has nowhere left to hide."
    )

    st.markdown(
        f"""
        <div class="duck-dialogue">
            <div class="duck-dialogue-title">{reaction} Final report</div>
            <div class="duck-dialogue-text">
                Bug status: resolved.<br>
                Attempts recorded: {struggle_count + 1}.<br>
                Duck satisfaction: 100%.<br>
                Developer confidence: restored.<br>
                Coffee consumed: unknown.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    another_col, return_col = st.columns(2)

    with another_col:
        if st.button(
            "Debug Another Problem",
            key="duck_debug_another",
            type="primary",
            use_container_width=True,
        ):
            reset_duck()
            st.rerun()

    with return_col:
        st.button(
            "Return to FidSync",
            key="duck_return_success",
            use_container_width=True,
            on_click=return_to_previous_page,
        )


def render_bottom_return() -> None:
    """Render the page return button outside the resolved screen."""

    st.divider()
    st.button(
        "Return to FidSync",
        key="duck_return_bottom",
        use_container_width=True,
        on_click=return_to_previous_page,
    )


def run() -> None:
    """Render the hidden Rubber Duck Debugger page."""

    initialize_duck_state()
    apply_styles()
    render_header(st.session_state.duck_struggle_count)

    if st.session_state.duck_resolved:
        render_success()
    elif st.session_state.duck_active_issue:
        render_active_session(st.session_state.duck_active_issue)
        render_bottom_return()
    else:
        render_issue_selector()
        render_bottom_return()


if __name__ == "__main__":
    run()
