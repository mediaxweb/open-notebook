import streamlit as st

from open_notebook.domain.transformation import DefaultPrompts, Transformation
from open_notebook.graphs.transformation import graph as transformation_graph
from pages.components.model_selector import model_selector
from pages.stream_app.utils import setup_page, hide_header_and_padding

setup_page("Xử lý dữ liệu", icon="🧩")
hide_header_and_padding()

transformations_tab, playground_tab = st.tabs(["🧩 Xử lý dữ liệu", "🛝 Playground"])


if "transformations" not in st.session_state:
    st.session_state.transformations = Transformation.get_all(order_by="name asc")
else:
    # work-around for streamlit losing typing on session state
    st.session_state.transformations = [
        Transformation(**trans.model_dump())
        for trans in st.session_state.transformations
    ]

with transformations_tab:
    st.header("🧩 Xử lý dữ liệu")

    st.markdown(
        "Là những prompt chỉ dẫn mô hinh Ai xử lý, phân tích nội dung gốc, từ đó đưa ra các thông tin như nội dung chính, tóm tắt... "
    )
    default_prompts: DefaultPrompts = DefaultPrompts()
    with st.expander("**⚙️ Prompt mặc định**"):
        default_prompts.transformation_instructions = st.text_area(
            "Prompt mặc định",
            default_prompts.transformation_instructions,
            height=300,
        )
        st.caption("Những thay đổi sẽ được áp dụng cho tất cả các prompt xử lý dữ liệu.")
        if st.button("Cập nhật", key="save_default_prompt"):
            default_prompts.update()
            st.toast("Cập nhật thành công!")
    if st.button("Tạo mới Prompt mới", icon="➕", key="new_transformation"):
        new_transformation = Transformation(
            name="New Tranformation",
            title="New Transformation Title",
            description="New Transformation Description",
            prompt="New Transformation Prompt",
            apply_default=False,
        )
        st.session_state.transformations.insert(0, new_transformation)
        st.rerun()

    st.divider()
    st.markdown("Prompt đã tạo")
    if len(st.session_state.transformations) == 0:
        st.markdown(
            "Chưa có Prompt nào. Bấm 'Tạo mới' để tạo một Prompt mới. "
        )
    else:
        for idx, transformation in enumerate(st.session_state.transformations):
            transform_expander = f"**{transformation.name}**" + (
                " - mặc định" if transformation.apply_default else ""
            )
            with st.expander(
                transform_expander,
                expanded=(transformation.id is None),
            ):
                name = st.text_input(
                    "Tên",
                    transformation.name,
                    key=f"{transformation.id}_name",
                )
                title = st.text_input(
                    "Tiêu đề (đây sẽ là tiêu đề của tất cả các thẻ được tạo bởi chuyển đổi này). ví dụ 'Chủ đề chính'",
                    transformation.title,
                    key=f"{transformation.id}_title",
                )
                description = st.text_area(
                    "Mô tả (hiển thị như một gợi ý trong giao diện người dùng để bạn biết bạn đang chọn gì)",
                    transformation.description,
                    key=f"{transformation.id}_description",
                )
                prompt = st.text_area(
                    "Prompt",
                    transformation.prompt,
                    key=f"{transformation.id}_prompt",
                    height=300,
                )
                # st.markdown(
                #     "You can use the prompt to summarize, expand, extract insights and much more. Example: `Translate this text to French`. For inspiration, check out this [great resource](https://github.com/danielmiessler/fabric/tree/main/patterns)."
                # )

                apply_default = st.checkbox(
                    "Đặt làm mặc định khi thêm mới dữ liệu",
                    transformation.apply_default,
                    key=f"{transformation.id}_apply_default",
                )
                if st.button("Lưu", key=f"{transformation.id}_save"):
                    transformation.name = name
                    transformation.title = title
                    transformation.description = description
                    transformation.prompt = prompt
                    transformation.apply_default = apply_default
                    st.toast(f"Lưu thành công prompt '{name}'!")
                    transformation.save()
                    st.rerun()

                if transformation.id:
                    with st.popover("Tùy chọn khác"):
                        if st.button(
                            "Thử nghiệm",
                            icon="🛝",
                            key=f"{transformation.id}_playground",
                        ):
                            st.stop()
                        if st.button(
                            "Xóa", icon="❌", key=f"{transformation.id}_delete"
                        ):
                            transformation.delete()
                            st.session_state.transformations.remove(transformation)
                            st.toast(f"Đã xóa prompt '{transformation.name}'!")
                            st.rerun()

with playground_tab:
    st.title("🛝 Thử nghiệm")

    transformation = st.selectbox(
        "Pick a transformation",
        st.session_state.transformations,
        format_func=lambda x: x.name,
    )

    model = model_selector(
        "Pick a pattern model",
        key="model",
        help="This is the model that will be used to run the transformation",
        model_type="language",
    )

    input_text = st.text_area("Enter some text", height=200)

    if st.button("Run"):
        output = transformation_graph.invoke(
            dict(
                input_text=input_text,
                transformation=transformation,
            ),
            config=dict(configurable={"model_id": model.id}),
        )
        st.markdown(output["output"])
