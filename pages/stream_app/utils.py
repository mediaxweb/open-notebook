import re
from datetime import datetime
from typing import List, Union
from datetime import datetime
from zoneinfo import ZoneInfo
# from pathlib import Path

import streamlit as st
from loguru import logger

from open_notebook.database.migrate import MigrationManager
from open_notebook.domain.models import DefaultModels
from open_notebook.domain.notebook import ChatSession, Notebook
from open_notebook.graphs.chat import ThreadState, graph
from open_notebook.utils import (
    compare_versions,
    get_installed_version,
    get_version_from_github,
)

# custom css
# def load_css():
#     css_path = Path(__file__).parent / "styles.css"
#     with open(css_path) as f:
#         st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def convert_to_vn_time(utc_dt: datetime) -> str:
    vn_dt = utc_dt.astimezone(ZoneInfo("Asia/Ho_Chi_Minh"))
    return vn_dt.strftime("%H:%M - %d/%m/%Y")

def hide_header_and_padding():
    """
    Hides the header and removes padding from the sides of the Streamlit app.
    """
    st.markdown(
        """
        <style>
            .block-container {
                padding-top: 0rem;
                padding-bottom: 2rem;
                padding-left: 40px;
                padding-right: 40px;
            }   
            # header {visibility: hidden;}
            .stAppHeader {
                display: none;    
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def version_sidebar():
    with st.sidebar:
        try:
            current_version = get_installed_version("open-notebook")
        except Exception:
            # Fallback to reading directly from pyproject.toml
            import tomli

            with open("pyproject.toml", "rb") as f:
                pyproject = tomli.load(f)
                current_version = pyproject["project"]["version"]

        latest_version = get_version_from_github(
            "https://www.github.com/lfnovo/open-notebook", "main"
        )
        st.write(f"Open Notebook: {current_version}")
        if compare_versions(current_version, latest_version) < 0:
            st.warning(
                f"New version {latest_version} available. [Click here for upgrade instructions](https://github.com/lfnovo/open-notebook/blob/main/docs/SETUP.md#upgrading-open-notebook)"
            )


def create_session_for_notebook(notebook_id: str, session_name: str = None):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    title = f"Chat Session {current_time}" if not session_name else session_name
    chat_session = ChatSession(title=title)
    chat_session.save()
    chat_session.relate_to_notebook(notebook_id)
    return chat_session


def setup_stream_state(current_notebook: Notebook) -> ChatSession:
    """
    Sets the value of the current session_id for langgraph thread state.
    If there is no existing thread state for this session_id, it creates a new one.
    Finally, it acquires the existing state for the session from Langgraph state and sets it in the streamlit session state.
    """
    assert (
        current_notebook is not None and current_notebook.id
    ), "Current Notebook not selected properly"

    if "context_config" not in st.session_state[current_notebook.id]:
        st.session_state[current_notebook.id]["context_config"] = {}

    current_session_id = st.session_state[current_notebook.id].get("active_session")

    # gets the chat session if provided
    chat_session: Union[ChatSession, None] = (
        ChatSession.get(current_session_id) if current_session_id else None
    )

    # if there is no chat session, create one or get the first one
    if not chat_session:
        sessions: List[ChatSession] = current_notebook.chat_sessions
        if not sessions or len(sessions) == 0:
            logger.debug("Creating new chat session")
            chat_session = create_session_for_notebook(current_notebook.id)
        else:
            logger.debug("Getting last updated session")
            chat_session = sessions[0]

    if not chat_session or chat_session.id is None:
        raise ValueError("Problem acquiring chat session")
    # sets the active session for the notebook
    st.session_state[current_notebook.id]["active_session"] = chat_session.id

    # gets the existing state for the session from Langgraph state
    existing_state = graph.get_state(
        {"configurable": {"thread_id": chat_session.id}}
    ).values
    if not existing_state or len(existing_state.keys()) == 0:
        st.session_state[chat_session.id] = ThreadState(
            messages=[], context=None, notebook=None, context_config={}
        )
    else:
        st.session_state[chat_session.id] = existing_state

    st.session_state[current_notebook.id]["active_session"] = chat_session.id
    return chat_session


def check_migration():
    logger.critical("Running migration check")
    mm = MigrationManager()
    if mm.needs_migration:
        st.warning("The Open Notebook database needs a migration to run properly.")
        if st.button("Run Migration"):
            mm.run_migration_up()
            st.success("Migration successful")
            st.rerun()
        st.stop()


def check_models(only_mandatory=True, stop_on_error=True):
    default_models = DefaultModels()
    mandatory_models = [
        default_models.default_chat_model,
        default_models.default_transformation_model,
        default_models.default_embedding_model,
    ]
    all_models = mandatory_models + [
        default_models.default_speech_to_text_model,
        default_models.large_context_model,
    ]

    if not all(mandatory_models):
        st.error(
            "You are missing some default models and the app will not work as expected. Please, select them on the Models page."
        )
        if stop_on_error:
            st.stop()

    if not only_mandatory:
        if not all(all_models):
            st.warning(
                "You are missing some important optional models. The app might not work as expected. Please, select them on the Models page."
            )


def handle_error(func):
    """Decorator for consistent error handling"""

    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error in {func.__name__}: {str(e)}")
            logger.exception(e)
            st.error(f"An error occurred: {str(e)}")

    return wrapper


def setup_page(
    title: str,
    layout="wide",
    sidebar_state="expanded",
    only_check_mandatory_models=True,
    stop_on_model_error=True,
    icon = "app/static/quoc-huy.png",
):
    """Common page setup for all pages"""
    st.set_page_config(
        page_title=title, layout=layout, initial_sidebar_state=sidebar_state, page_icon=icon
    )
    check_migration()
    check_models(
        only_mandatory=only_check_mandatory_models, stop_on_error=stop_on_model_error
    )
    # version_sidebar()


def convert_source_references(text, display=False):
    """
    Converts or removes source references in brackets.

    Matches patterns like [source_insight:id], [note:id], [source:id], or [source_embedding:id]
    and either removes them or converts them to markdown links.
    If display=False, also removes any trailing period that follows a reference.

    Args:
        text (str): The input text containing source references
        display (bool, optional): If True, converts references to links; if False, removes them. Defaults to False.

    Returns:
        str: Text with source references converted or removed

    Examples:
        >>> text = "Here is a reference [source_insight:abc123]."
        >>> convert_source_references(text, display=True)
        'Here is a reference [source_insight:abc123](/?object_id=source_insight:abc123).'
        >>> convert_source_references(text, display=False)
        'Here is a reference '
    """

    # Pattern matches [type:id] where type can be source_insight, note, source, or source_embedding
    # The optional group (\.)? captures a period that might follow the reference
    pattern = r"\[((?:source_insight|note|source|source_embedding):[\w\d]+)\](\.)?"

    if display:
        # Convert to markdown links while preserving any trailing period
        def replace_match(match):
            """Helper function to create the markdown link"""
            source_ref = match.group(1)  # Gets the content inside brackets
            period = match.group(2) or ""  # Gets the period if it exists, otherwise empty string
            return f"[[{source_ref}]](/?object_id={source_ref}){period}"

        converted_text = re.sub(pattern, replace_match, text)
    else:
        # Remove references including any trailing period
        converted_text = re.sub(pattern, "", text)

    return converted_text
