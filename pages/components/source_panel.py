import asyncio

import streamlit as st
import streamlit_scrollable_textbox as stx  # type: ignore
from humanize import naturaltime

from open_notebook.domain.models import model_manager
from open_notebook.domain.notebook import Source
from open_notebook.domain.transformation import Transformation
from open_notebook.graphs.transformation import graph as transform_graph
from pages.stream_app.utils import check_models, convert_to_vn_time


def source_panel(source_id: str, notebook_id=None, modal=False):
    check_models(only_mandatory=False)
    source: Source = Source.get(source_id)
    if not source:
        raise ValueError(f"Source not found: {source_id}")

    current_title = source.title if source.title else "Không có tiêu đề"
    source.title = st.text_input("Tiêu đề", value=current_title)
    if source.title != current_title:
        st.toast("Cập nhật thành công!")
        source.save()

    process_tab, source_tab = st.tabs(["Xử lý dữ liệu", "Nguồn"])
    with process_tab:
        c1, c2 = st.columns([4, 2])
        with c1:
            title = st.empty()
            if source.title:
                title.subheader(source.title)
            if source.asset and source.asset.url:
                from_src = f"from URL: {source.asset.url}"
            elif source.asset and source.asset.file_path:
                from_src = f"from file: {source.asset.file_path}"
            else:
                from_src = "from text"
            # st.caption(f"Created {naturaltime(source.created)}, {from_src}")
            st.caption(f"Ngày tạo {convert_to_vn_time(source.created)}")
            for insight in source.insights:
                with st.expander(f"**{insight.insight_type}**"):
                    st.markdown(insight.content)
                    x1, x2 = st.columns(2)
                    if x1.button(
                        "Xóa", type="primary", key=f"delete_insight_{insight.id}"
                    ):
                        insight.delete()
                        st.rerun(scope="fragment" if modal else "app")
                        st.toast("Đã xóa thành công!")
                    if notebook_id:
                        if x2.button(
                            "Tạo ghi chú", icon="📝", key=f"save_note_{insight.id}"
                        ):
                            insight.save_as_note(notebook_id)
                            st.toast("Đã lưu ghi chú.")

        with c2:
            transformations = Transformation.get_all(order_by="name asc")
            with st.container(border=True):
                transformation = st.selectbox(
                    "Chuyển đổi nội dung",
                    transformations,
                    key=f"transformation_{source.id}",
                    format_func=lambda x: x.name,
                )
                st.caption(transformation.description)
                if st.button("Xử lý"):
                    asyncio.run(
                        transform_graph.ainvoke(
                            input=dict(source=source, transformation=transformation)
                        )
                    )
                    st.rerun(scope="fragment" if modal else "app")

            if not model_manager.embedding_model:
                help = (
                    "No embedding model found. Please, select one on the Models page."
                )
            else:
                help = "Mã hóa vectors cho phép tìm kiếm nhanh hơn và chính xác hơn."

            if source.embedded_chunks == 0 and st.button(
                "Mã hóa vectors",
                icon="🦾",
                help=help,
                disabled=model_manager.embedding_model is None,
            ):
                source.vectorize()
                st.success("Mã hóa hoàn tất!")

            with st.container(border=True):
                st.caption(
                    "Xóa nguồn sẽ xóa tất cả các thông tin liên quan."
                )
                if st.button(
                    "Xóa", type="primary", key=f"bt_delete_source_{source.id}"
                ):
                    source.delete()
                    st.rerun()

    with source_tab:
        st.subheader("Nội dung")
        stx.scrollableTextbox(source.full_text, height=300)
