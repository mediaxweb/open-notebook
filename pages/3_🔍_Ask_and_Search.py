import asyncio

import streamlit as st

from open_notebook.domain.models import DefaultModels, model_manager
from open_notebook.domain.notebook import Note, Notebook, text_search, vector_search
from open_notebook.graphs.ask import graph as ask_graph
from pages.components.model_selector import model_selector
from pages.stream_app.utils import convert_source_references, setup_page, hide_header_and_padding

setup_page("Tìm kiếm", icon="🔍")

hide_header_and_padding()

ask_tab, search_tab = st.tabs(["Đặt câu hỏi với cơ sở tri thức (thử nghiệm)", "Tìm kiếm"])

if "search_results" not in st.session_state:
    st.session_state["search_results"] = []

if "ask_results" not in st.session_state:
    st.session_state["ask_results"] = {}


async def process_ask_query(question, strategy_model, answer_model, final_answer_model):
    async for chunk in ask_graph.astream(
        input=dict(
            question=question,
        ),
        config=dict(
            configurable=dict(
                strategy_model=strategy_model.id,
                answer_model=answer_model.id,
                final_answer_model=final_answer_model.id,
            )
        ),
        stream_mode="updates",
    ):
        yield (chunk)


def results_card(item):
    score = item.get("relevance", item.get("similarity", item.get("score", 0)))
    with st.container(border=True):
        st.markdown(
            f"[{score:.2f}] **[{item['title']}](/?object_id={item['parent_id']})**"
        )
        if "matches" in item:
            with st.expander("Matches"):
                for match in item["matches"]:
                    st.markdown(match)


with ask_tab:
    st.subheader("Đặt câu hỏi với cơ sở tri thức (thử nghiệm)")
    st.caption(
        "Mô hình LLM sẽ trả lời câu hỏi của bạn dựa trên các tài liệu trong cơ sở tri thức của bạn. "
    )
    question = st.text_input("Câu hỏi", "")
    default_model = DefaultModels().default_chat_model
    strategy_model = model_selector(
        "Mô hình Chiến lược Truy vấn",
        "strategy_model",
        selected_id=default_model,
        model_type="language",
        help="Mô hình LLM sẽ xử lý các truy vấn chiến lược",
    )
    answer_model = model_selector(
        "Mô hình Trả lời Cá nhân",
        "answer_model",
        model_type="language",
        selected_id=default_model,
        help="Mô hình LLM sẽ xử lý các truy vấn cá nhân",
    )
    final_answer_model = model_selector(
        "Mô hình Trả lời Cuối cùng",
        "final_answer_model",
        model_type="language",
        selected_id=default_model,
        help="Mô hình LLM sẽ xử lý câu trả lời cuối cùng",
    )
    if not model_manager.embedding_model:
        st.warning(
            "You can't use this feature because you have no embedding model selected. Please set one up in the Models page."
        )
    ask_bt = st.button("Hỏi") if model_manager.embedding_model else None
    placeholder = st.container()

    async def stream_results():
        async for chunk in process_ask_query(
            question, strategy_model, answer_model, final_answer_model
        ):
            if "agent" in chunk:
                with placeholder.expander(
                    f"Agent Strategy: {chunk['agent']['strategy'].reasoning}"
                ):
                    for search in chunk["agent"]["strategy"].searches:
                        st.markdown(f"Tìm kiếm: **{search.term}**")
                        st.markdown(f"Yêu cầu: {search.instructions}")
            elif "provide_answer" in chunk:
                for answer in chunk["provide_answer"]["answers"]:
                    with placeholder.expander("Trả lời"):
                        st.markdown(convert_source_references(answer))
            elif "write_final_answer" in chunk:
                st.session_state["ask_results"]["answer"] = chunk["write_final_answer"][
                    "final_answer"
                ]
                with placeholder.container(border=True):
                    st.markdown(
                        convert_source_references(
                            chunk["write_final_answer"]["final_answer"]
                        )
                    )

    if ask_bt:
        placeholder.write(f"Câu hỏi: {question}")
        st.session_state["ask_results"]["question"] = question
        st.session_state["ask_results"]["answer"] = None

        asyncio.run(stream_results())

    if st.session_state["ask_results"].get("answer"):
        with st.container(border=True):
            with st.form("save_note_form"):
                notebook = st.selectbox(
                    "Notebook", Notebook.get_all(), format_func=lambda x: x.name
                )
                if st.form_submit_button("Thêm câu trả lời vào ghi chú"):
                    note = Note(
                        title=st.session_state["ask_results"]["question"],
                        content=st.session_state["ask_results"]["answer"],
                    )
                    note.save()
                    note.add_to_notebook(notebook.id)
                    st.success("Tạo thành công!")


with search_tab:
    with st.container(border=True):
        st.subheader("🔍 Tìm kiếm")
        st.caption("Tìm kiếm trong cơ sở tri thức của bạn cho các từ khóa hoặc khái niệm cụ thể")
        search_term = st.text_input("Tìm kiếm", "")
        if not model_manager.embedding_model:
            st.warning(
                "You can't use vector search because you have no embedding model selected. Only text search will be available."
            )
            search_type = "Text Search"
        else:
            search_type = st.radio("Kiểu tìm kiếm", ["Văn bản", "Vector"])
        search_sources = st.checkbox("Tìm trong nguồn tài liệu", value=True)
        search_notes = st.checkbox("Tìm trong ghi chú", value=True)
        if st.button("Tìm"):
            if search_type == "Văn bản":
                st.write(f"Tìm kiếm: {search_term}")
                st.session_state["search_results"] = text_search(
                    search_term, 100, search_sources, search_notes
                )
            elif search_type == "Vector":
                st.write(f"Tìm kiếm: {search_term}")
                st.session_state["search_results"] = vector_search(
                    search_term, 100, search_sources, search_notes
                )
        for item in st.session_state["search_results"]:
            results_card(item)
