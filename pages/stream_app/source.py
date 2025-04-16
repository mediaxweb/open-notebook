import asyncio
import os
from pathlib import Path

import streamlit as st
from humanize import naturaltime
from loguru import logger

from open_notebook.config import UPLOADS_FOLDER
from open_notebook.domain.models import model_manager
from open_notebook.domain.notebook import Source
from open_notebook.domain.transformation import Transformation
from open_notebook.exceptions import UnsupportedTypeException
from open_notebook.graphs.source import source_graph
from pages.components import source_panel

from pages.stream_app.utils import convert_to_vn_time

from .consts import source_context_icons


@st.dialog("Dữ liệu", width="large")
def source_panel_dialog(source_id, notebook_id=None):
    source_panel(source_id, notebook_id=notebook_id, modal=True)


@st.dialog("Thêm dữ liệu", width="large")
def add_source(notebook_id):
    if not model_manager.speech_to_text:
        st.warning(
            "Since there is no speech to text model selected, you can't upload audio/video files."
        )
    source_link = None
    source_file = None
    source_text = None
    source_type = st.radio("Type", ["Đường dẫn", "Tải lên", "Văn bản"])
    req = {}
    transformations = Transformation.get_all()
    if source_type == "Đường dẫn":
        source_link = st.text_input("Đường dẫn", placeholder="https://example.com/file.pdf")
        req["url"] = source_link
    elif source_type == "Tải lên":
        source_file = st.file_uploader("Tải lên")
        req["delete_source"] = st.checkbox("Xóa file sau khi xử lý", value=True)

    else:
        source_text = st.text_area("Văn bản")
        req["content"] = source_text

    transformations = Transformation.get_all()
    default_transformations = [t for t in transformations if t.apply_default]
    apply_transformations = st.multiselect(
        "Chuyển đổi nội dung",
        options=transformations,
        format_func=lambda t: t.name,
        default=default_transformations,
    )
    run_embed = st.checkbox(
        "Mã hóa nội dung để phục vụ tìm kiếm vector",
        help="Có thể sẽ mất thêm chi phí và thời gian.",
    )
    if st.button("Bắt đầu xử lý", key="add_source"):
        logger.debug("Adding source")
        with st.status("Đang xử lý...", expanded=True):
            st.write("Đang xử lý dữ liệu...")
            try:
                if source_type == "Tải lên" and source_file is not None:
                    st.write("Đang tải lên...")
                    file_name = source_file.name
                    file_extension = Path(file_name).suffix
                    base_name = Path(file_name).stem

                    # Generate unique filename
                    new_path = os.path.join(UPLOADS_FOLDER, file_name)
                    counter = 0
                    while os.path.exists(new_path):
                        counter += 1
                        new_file_name = f"{base_name}_{counter}{file_extension}"
                        new_path = os.path.join(UPLOADS_FOLDER, new_file_name)

                    req["file_path"] = str(new_path)
                    # Save the file
                    with open(new_path, "wb") as f:
                        f.write(source_file.getbuffer())

                asyncio.run(
                    source_graph.ainvoke(
                        {
                            "content_state": req,
                            "notebook_id": notebook_id,
                            "apply_transformations": apply_transformations,
                            "embed": run_embed,
                        }
                    )
                )
            except UnsupportedTypeException as e:
                st.warning(
                    "Nội dung này chưa được hỗ trợ."
                )
                # st.error(e)
                # st.link_button(
                #     "Go to Github Issues",
                #     url="https://www.github.com/lfnovo/open-notebook/issues",
                # )
                st.stop()

            except Exception as e:
                st.exception(e)
                return

        st.rerun()


def source_card(source, notebook_id):
    # todo: more descriptive icons
    icon = ":material/attachment:"

    with st.container(border=True):
        title = (source.title if source.title else "Không có tiêu đề").strip()
        st.markdown((f"{icon}**{title}**"))
        context_state = st.selectbox(
            "Context",
            label_visibility="collapsed",
            options=source_context_icons,
            index=1,
            key=f"source_{source.id}",
        )
        # st.caption(
        #     f"Updated: {convert_to_vn_time(source.updated)}, **{len(source.insights)}** insights"
        # )
        st.caption(
            f"Ngày tạo: {convert_to_vn_time(source.updated)}"
        )
        if st.button("Xem chi tiết", icon=":material/bookmarks:", key=source.id):
            source_panel_dialog(source.id, notebook_id)

    st.session_state[notebook_id]["context_config"][source.id] = context_state


def source_list_item(source_id, score=None):
    source: Source = Source.get(source_id)
    if not source:
        st.error("Source not found")
        return
    icon = ":material/attachment:"

    with st.expander(
        f"{icon} [{score:.2f}] **{source.title}** {naturaltime(source.updated)}"
    ):
        for insight in source.insights:
            st.markdown(f"**{insight.insight_type}**")
            st.write(insight.content)
        if st.button("Edit source", icon="📝", key=f"x_edit_source_{source.id}"):
            source_panel_dialog(source_id=source.id)
