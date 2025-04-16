from typing import Union

import humanize
import streamlit as st
from langchain_core.runnables import RunnableConfig

from open_notebook.domain.base import ObjectModel
from open_notebook.domain.notebook import ChatSession, Note, Notebook, Source
from open_notebook.graphs.chat import graph as chat_graph
from open_notebook.plugins.podcasts import PodcastConfig
from open_notebook.utils import token_count
from pages.stream_app.utils import (
    convert_source_references,
)
from streamlit_chat import message

from .note import make_note_from_chat


# todo: build a smarter, more robust context manager function
def build_context(notebook_id):
    st.session_state[notebook_id]["context"] = dict(note=[], source=[])

    for id, status in st.session_state[notebook_id]["context_config"].items():
        if not id:
            continue

        item_type, item_id = id.split(":")
        if item_type not in ["note", "source"]:
            continue

        if "not in" in status:
            continue

        try:
            item: Union[Note, Source] = ObjectModel.get(id)
        except Exception:
            continue

        if "insights" in status:
            st.session_state[notebook_id]["context"][item_type] += [
                item.get_context(context_size="short")
            ]
        elif "full content" in status:
            st.session_state[notebook_id]["context"][item_type] += [
                item.get_context(context_size="long")
            ]

    return st.session_state[notebook_id]["context"]


def execute_chat(txt_input, context, current_session):
    current_state = st.session_state[current_session.id]
    current_state["messages"] += [txt_input]
    current_state["context"] = context
    result = chat_graph.invoke(
        input=current_state,
        config=RunnableConfig(configurable={"thread_id": current_session.id}),
    )
    current_session.save()
    return result

def chat_sidebar(current_notebook: Notebook, current_session: ChatSession):
    context = build_context(notebook_id=current_notebook.id)
    tokens = token_count(
        str(context) + str(st.session_state[current_session.id]["messages"])
    )
    
    with st.container(border=True, key="chat_tab"):
        with st.container(key="chat_tab_header"):
            st.subheader("Hỏi đáp", divider="gray")

            # request = st.chat_input("Đặt câu hỏi")
            # # removing for now since it's not multi-model capable right now
            # if request:
            #     response = execute_chat(
            #         txt_input=request,
            #         context=context,
            #         current_session=current_session,
            #     )
            #     st.session_state[current_session.id]["messages"] = response["messages"]

        with st.container(key="chat_tab_body"):
            messages = st.session_state[current_session.id]["messages"][::-1]
            if not messages:
                st.markdown(
                '<div class="empty-chat" style="height: 100%; text-align: center; padding: 20px; display: flex; flex-direction: column; align-items: center;">'
                    '<img src="data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiBzdHJva2U9IiNjYzVmMzMiIHN0cm9rZS13aWR0aD0iMiIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIiBzdHJva2UtbGluZWpvaW49InJvdW5kIiBjbGFzcz0ibHVjaWRlIGx1Y2lkZS11cGxvYWQtaWNvbiBsdWNpZGUtdXBsb2FkIj48cGF0aCBkPSJNMjEgMTV2NGEyIDIgMCAwIDEtMiAySDVhMiAyIDAgMCAxLTItMnYtNCIvPjxwb2x5bGluZSBwb2ludHM9IjE3IDggMTIgMyA3IDgiLz48bGluZSB4MT0iMTIiIHgyPSIxMiIgeTE9IjMiIHkyPSIxNSIvPjwvc3ZnPg=="' \
                        'alt="No messages"'
                        'width="40" height="40"'
                    '/>'
                    '<span>Thêm tài nguồn để bắt đầu</span>'
                '</div>'
                """
                <style>
                    .st-key-chat_tab > :nth-child(2) * {
                        height: 100%;
                </style>
                """
                , unsafe_allow_html=True)

            else:
                for msg in messages:
                    if msg.type not in ["human", "ai"]:
                        continue
                    if not msg.content:
                        continue

                    with st.chat_message(name=msg.type):
                        st.markdown(convert_source_references(msg.content))
                        if msg.type == "ai":
                            if st.button("Tạo ghi chú", key=f"render_save_{msg.id}", icon=":material/bookmarks:"):
                                make_note_from_chat(
                                    content=msg.content,
                                    notebook_id=current_notebook.id,
                                )
                                st.rerun()

        with st.container(key="chat_tab_input"):
            request = st.chat_input("Đặt câu hỏi")
                # removing for now since it's not multi-model capable right now
            if request:
                response = execute_chat(
                    txt_input=request,
                    context=context,
                    current_session=current_session,
                )
                st.session_state[current_session.id]["messages"] = response["messages"]
                st.rerun()

# def chat_sidebar(current_notebook: Notebook, current_session: ChatSession):
#     context = build_context(notebook_id=current_notebook.id)
#     tokens = token_count(
#         str(context) + str(st.session_state[current_session.id]["messages"])
#     )
    
#     with st.container(border=True, key="chat_tab"):
#         st.subheader("Hỏi đáp")

#         for msg in st.session_state[current_session.id]["messages"]:
#             if msg.type not in ["human", "ai"]:
#                 continue
#             if not msg.content:
#                 continue

#             with st.chat_message(name=msg.type):
#                 st.markdown(convert_source_references(msg.content))
#                 if msg.type == "ai":
#                     if st.button("Tạo ghi chú", key=f"render_save_{msg.id}", icon=":material/add:"):
#                         make_note_from_chat(
#                             content=msg.content,
#                             notebook_id=current_notebook.id,
#                         )
#                         st.rerun()
        
#         request = st.chat_input("Đặt câu hỏi")
#         if request:
#             response = execute_chat(
#                 txt_input=request,
#                 context=context,
#                 current_session=current_session,
#             )
#             st.session_state[current_session.id]["messages"] = response["messages"]
#             st.rerun()
