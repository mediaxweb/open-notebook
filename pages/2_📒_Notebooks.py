import streamlit as st
from humanize import naturaltime

from open_notebook.domain.notebook import Notebook
from pages.stream_app.chat import chat_sidebar
from pages.stream_app.note import add_note, note_card
from pages.stream_app.source import add_source, source_card
from pages.stream_app.utils import setup_page, setup_stream_state, hide_header_and_padding, convert_to_vn_time

setup_page("Open Notebook", only_check_mandatory_models=True)

hide_header_and_padding()

st.markdown(
        """
        <style>
            .st-key-back_button {
                text-align-last: end;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

def notebook_header(current_notebook: Notebook):
    # c1, c2, c3 = st.columns([8, 2, 2])
    # if c3.button("Refresh", icon="🔄"):
    #     st.rerun()
    
    # xếp dọc có thể sẽ đẹp hơn?
    c1, c2 = st.columns([7, 1])
    with c1:
        st.header(current_notebook.name)
    with c2:
        st.markdown("<div>", unsafe_allow_html=True)
        if st.button("⬅️ Quay lại", key="back_button"):
            st.session_state["current_notebook_id"] = None
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    
    current_description = current_notebook.description
    with st.expander(
        current_notebook.description
        if len(current_description) > 0
        else "Click để thêm mô tả",
    ):
        notebook_name = st.text_input("Tên", value=current_notebook.name)
        notebook_description = st.text_area(
            "Mô tả",
            value=current_description,
            placeholder="Mô tả ngữ cảnh chi tiết nhất có thể để AI đưa ra câu trả lời chính xác nhất!",
        )
        c1, c2, c3 = st.columns([1, 1, 1])
        if c1.button("Cập nhật", icon="💾", key="edit_notebook"):
            current_notebook.name = notebook_name
            current_notebook.description = notebook_description
            current_notebook.save()
            st.rerun()
        if not current_notebook.archived:
            if c2.button("Lưu trữ", icon="🗃️"):
                current_notebook.archived = True
                current_notebook.save()
                st.toast("Đã đưa sổ vào lưu trữ", icon="🗃️")
        else:
            if c2.button("Khôi phục", icon="🗃️"):
                current_notebook.archived = False
                current_notebook.save()
                st.toast("Đã khôi phục sổ!", icon="🗃️")
        if c3.button("Xóa", type="primary", icon="🗑️"):
            current_notebook.delete()
            st.session_state["current_notebook_id"] = None
            st.rerun()


def notebook_page(current_notebook: Notebook):
    # Guarantees that we have an entry for this notebook in the session state
    if current_notebook.id not in st.session_state:
        st.session_state[current_notebook.id] = {"notebook": current_notebook}

    # sets up the active session
    current_session = setup_stream_state(
        current_notebook=current_notebook,
    )

    sources = current_notebook.sources
    notes = current_notebook.notes

    notebook_header(current_notebook)

    work_tab = st.container()
    with work_tab:
        sources_tab, chat_tab, notes_tab = st.columns([2, 3, 2])
        with sources_tab:
            with st.container(border=True):
                st.subheader("Dữ liệu")
                if st.button("Thêm dữ liệu", icon="➕"):
                    add_source(current_notebook.id)
                for source in sources:
                    source_card(source=source, notebook_id=current_notebook.id)
                    
        with chat_tab:
            chat_sidebar(current_notebook=current_notebook, current_session=current_session)

        with notes_tab:
            with st.container(border=True):
                st.subheader("Ghi chú")
                if st.button("Thêm ghi chú", icon="📝"):
                    add_note(current_notebook.id)
                for note in notes:
                    note_card(note=note, notebook_id=current_notebook.id)


def notebook_list_item(notebook):
    with st.container(border=True):
        st.subheader(notebook.name)
        # st.caption(
        #     f"Created: {naturaltime(notebook.created)}, updated: {naturaltime(notebook.updated)}"
        # )
        st.caption(
            f"Ngày tạo: {convert_to_vn_time(notebook.created)}"
        )
        st.write(notebook.description)
        if st.button("Mở", key=f"open_notebook_{notebook.id}"):
            st.session_state["current_notebook_id"] = notebook.id
            st.rerun()


if "current_notebook_id" not in st.session_state:
    st.session_state["current_notebook_id"] = None

# todo: get the notebook, check if it exists and if it's archived
if st.session_state["current_notebook_id"]:
    current_notebook: Notebook = Notebook.get(st.session_state["current_notebook_id"])
    if not current_notebook:
        st.error("Notebook not found")
        st.stop()
    notebook_page(current_notebook)
    st.stop()

st.title("📒 Sổ tay của tôi")
st.caption(
    "Sổ tay là một cách tuyệt vời để sắp xếp suy nghĩ, ý tưởng và tài liệu của bạn. Bạn có thể tạo sổ tay cho các chủ đề và dự án nghiên cứu khác nhau v.v..."
)

with st.expander("➕ **Tạo sổ mới**"):
    new_notebook_title = st.text_input("Tên sổ")
    new_notebook_description = st.text_area(
        "Mô tả",
        placeholder="Mục đích của sổ, càng chi tiết càng tốt!",
    )
    if st.button("Tạo mới", icon="➕"):
        notebook = Notebook(
            name=new_notebook_title, description=new_notebook_description
        )
        notebook.save()
        st.toast("Tạo thành công!", icon="📒")

notebooks = Notebook.get_all(order_by="updated desc")
archived_notebooks = [nb for nb in notebooks if nb.archived]

for notebook in notebooks:
    if notebook.archived:
        continue
    notebook_list_item(notebook)

if len(archived_notebooks) > 0:
    with st.expander(f"**🗃️ Đã lưu trữ {len(archived_notebooks)} sổ**"):
        st.write("ℹ️ Sổ đã lưu vẫn có thể sử dụng")
        for notebook in archived_notebooks:
            notebook_list_item(notebook)
