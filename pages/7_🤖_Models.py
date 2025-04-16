import os

import streamlit as st

from open_notebook.config import CONFIG
from open_notebook.domain.models import DefaultModels, Model, model_manager
from open_notebook.models import MODEL_CLASS_MAP
from pages.components.model_selector import model_selector
from pages.stream_app.utils import setup_page, hide_header_and_padding

setup_page("Mô hình", only_check_mandatory_models=False, stop_on_model_error=False, icon="🤖")

hide_header_and_padding()

st.title("🤖 Mô hình")

model_tab, model_defaults_tab = st.tabs(["Mô hình", "Mô hình mặc định"])

provider_status = {}

model_types = [
    # "vision",
    "language",
    "embedding",
    "text_to_speech",
    "speech_to_text",
]

provider_status["ollama"] = os.environ.get("OLLAMA_API_BASE") is not None
provider_status["openai"] = os.environ.get("OPENAI_API_KEY") is not None
provider_status["groq"] = os.environ.get("GROQ_API_KEY") is not None
provider_status["xai"] = os.environ.get("XAI_API_KEY") is not None
provider_status["vertexai"] = (
    os.environ.get("VERTEX_PROJECT") is not None
    and os.environ.get("VERTEX_LOCATION") is not None
    and os.environ.get("GOOGLE_APPLICATION_CREDENTIALS") is not None
)
provider_status["vertexai-anthropic"] = (
    os.environ.get("VERTEX_PROJECT") is not None
    and os.environ.get("VERTEX_LOCATION") is not None
    and os.environ.get("GOOGLE_APPLICATION_CREDENTIALS") is not None
)
provider_status["gemini"] = os.environ.get("GEMINI_API_KEY") is not None
provider_status["openrouter"] = (
    os.environ.get("OPENROUTER_API_KEY") is not None
    and os.environ.get("OPENAI_API_KEY") is not None
    and os.environ.get("OPENROUTER_BASE_URL") is not None
)
provider_status["anthropic"] = os.environ.get("ANTHROPIC_API_KEY") is not None
provider_status["elevenlabs"] = os.environ.get("ELEVENLABS_API_KEY") is not None
provider_status["litellm"] = (
    provider_status["ollama"]
    or provider_status["vertexai"]
    or provider_status["vertexai-anthropic"]
    or provider_status["anthropic"]
    or provider_status["openai"]
    or provider_status["gemini"]
)

available_providers = [k for k, v in provider_status.items() if v]
unavailable_providers = [k for k, v in provider_status.items() if not v]


def generate_new_models(models, suggested_models):
    # Create a set of existing model keys for efficient lookup
    existing_model_keys = {
        f"{model.provider}-{model.name}-{model.type}" for model in models
    }

    new_models = []

    # Iterate through suggested models by provider
    for provider, types in suggested_models.items():
        # Iterate through each type (language, embedding, etc.)
        for type_, model_list in types.items():
            for model_name in model_list:
                model_key = f"{provider}-{model_name}-{type_}"

                # Check if model already exists
                if model_key not in existing_model_keys:
                    if provider_status.get(provider):
                        new_models.append(
                            {
                                "name": model_name,
                                "type": type_,
                                "provider": provider,
                            }
                        )

    return new_models


default_models = DefaultModels()
all_models = Model.get_all()

with model_tab:
    st.subheader("Thêm mô hình")

    provider = st.selectbox("Nhà cung cấp", available_providers)
    if len(unavailable_providers) > 0:
        st.caption(
            f"Nhà cung cấp không khả dụng: {', '.join(unavailable_providers)}."
        )

    # Filter model types based on provider availability in MODEL_CLASS_MAP
    available_model_types = []
    for model_type in model_types:
        if model_type in MODEL_CLASS_MAP and provider in MODEL_CLASS_MAP[model_type]:
            available_model_types.append(model_type)

    if not available_model_types:
        st.error(f"Không có loại mô hình tương thích nào với nhà cung cấp: {provider}")
    else:
        model_type = st.selectbox(
            "Loại mô hình",
            available_model_types,
            help='Sử dụng "language" cho các mô hình sinh văn bản, "text_to_speech" cho các mô hình TTS để tạo podcast, v.v.',
        )
        if model_type == "text_to_speech" and provider == "gemini":
            model_name = "gemini-default"
            st.markdown("Gemini models are pre-configured. Using the default model.")
        else:
            model_name = st.text_input(
                "Tên mô hình", "", help="gpt-4o-mini, claude, gemini, llama3, v.v."
            )
        if st.button("Lưu"):
            model = Model(name=model_name, provider=provider, type=model_type)
            model.save()
            st.success("Lưu thành công!")

    st.divider()
    suggested_models = CONFIG.get("suggested_models", [])
    recommendations = generate_new_models(all_models, suggested_models)
    if len(recommendations) > 0:
        with st.expander("💁‍♂️ Mô hình đề xuất"):
            for recommendation in recommendations:
                st.markdown(
                    f"**{recommendation['name']}** ({recommendation['provider']}, {recommendation['type']})"
                )
                if st.button("Thêm", key=f"add_{recommendation['name']}"):
                    new_model = Model(**recommendation)
                    new_model.save()
                    st.rerun()
    st.subheader("Mô hình thiết lập sẵn")
    model_types_available = {
        # "vision": False,
        "language": False,
        "embedding": False,
        "text_to_speech": False,
        "speech_to_text": False,
    }
    for model in all_models:
        model_types_available[model.type] = True
        with st.container(border=True):
            st.markdown(f"{model.name} ({model.provider}, {model.type})")
            if st.button("Xóa", key=f"delete_{model.id}"):
                model.delete()
                st.rerun()

    for model_type, available in model_types_available.items():
        if not available:
            st.warning(f"No models available for {model_type}")

with model_defaults_tab:
    text_generation_models = [model for model in all_models if model.type == "language"]

    text_to_speech_models = [
        model for model in all_models if model.type == "text_to_speech"
    ]

    speech_to_text_models = [
        model for model in all_models if model.type == "speech_to_text"
    ]
    vision_models = [model for model in all_models if model.type == "vision"]
    embedding_models = [model for model in all_models if model.type == "embedding"]
    # st.write(
    #     "In this section, you can select the default models to be used on the various content operations done by Open Notebook. Some of these can be overriden in the different modules."
    # )
    defs = {}
    # Handle chat model selection
    selected_model = model_selector(
        "Mô hình chat",
        "default_chat_model",
        selected_id=default_models.default_chat_model,
        help="Mô hình này sẽ được sử dụng cho chat.",
        model_type="language",
    )
    if selected_model:
        default_models.default_chat_model = selected_model.id
    st.divider()
    # Handle transformation model selection
    selected_model = model_selector(
        "Mô hình xử lý dữ liệu",
        "default_transformation_model",
        selected_id=default_models.default_transformation_model,
        help="Mô hình này sẽ được sử dụng cho việc xử lý, chuyển đổi dữ liệu",
        model_type="language",
    )
    if selected_model:
        default_models.default_transformation_model = selected_model.id
    # st.caption("You can use a cheap model here like gpt-4o-mini, llama3, etc.")
    st.divider()

    # Handle tools model selection
    selected_model = model_selector(
        "Mô hình công cụ",
        "default_tools_model",
        selected_id=default_models.default_tools_model,
        help="Mô hình này sẽ được sử dụng cho việc gọi công cụ. Hiện tại, tốt nhất là sử dụng Open AI và Anthropic.",
        model_type="language",
    )
    if selected_model:
        default_models.default_tools_model = selected_model.id
    st.caption("Khuyến nghị sử dụng: gpt-4o, claude, v.v.")
    st.divider()

    # Handle large context model selection
    selected_model = model_selector(
        "Mô hình ngữ cảnh lớn",
        "large_context_model",
        selected_id=default_models.large_context_model,
        help="Mô hình này sẽ được sử dụng trong trường hợp ngữ cảnh lớn.",
        model_type="language",
    )
    if selected_model:
        default_models.large_context_model = selected_model.id
    st.caption("Khuyến nghị sử dụng: Gemini")
    st.divider()

    # Handle text-to-speech model selection
    selected_model = model_selector(
        "Mô hình chuyển văn bản thành giọng nói",
        "default_text_to_speech_model",
        selected_id=default_models.default_text_to_speech_model,
        help="Mô hình này sẽ được sử dụng để chuyển văn bản thành giọng nói (podcasts, v.v.)",
        model_type="text_to_speech",
    )
    st.caption("Bạn có thể ghi đè mô hình này trên các podcast khác")
    if selected_model:
        default_models.default_text_to_speech_model = selected_model.id
    st.divider()

    # Handle speech-to-text model selection
    selected_model = model_selector(
        "Mô hình chuyển đổi giọng nói thành văn bản",
        selected_id=default_models.default_speech_to_text_model,
        help="Mô hình này sẽ được sử dụng để chuyển đổi giọng nói thành văn bản (chuyển đổi âm thanh, v.v.)",
        model_type="speech_to_text",
        key="default_speech_to_text_model",
    )

    if selected_model:
        default_models.default_speech_to_text_model = selected_model.id

    st.divider()
    # Handle embedding model selection
    selected_model = model_selector(
        "Mô hình nhúng (mã hóa)",
        "default_embedding_model",
        selected_id=default_models.default_embedding_model,
        help="Mô hình này sẽ được sử dụng cho việc nhúng (tìm kiếm ngữ nghĩa, v.v.)",
        model_type="embedding",
    )
    if selected_model:
        default_models.default_embedding_model = selected_model.id
    st.warning(
        "Lưu ý: Mô hình nhúng sẽ không thể thay đổi nếu đã được sử dụng để mã hóa dữ liệu. Nếu thay đổi, những dữ liệu đó sẽ cần phải mã hóa lại."
    )

    for k, v in defs.items():
        if v:
            defs[k] = v.id

    if st.button("Lưu Mặc Định"):
        default_models.patch(defs)
        model_manager.refresh_defaults()
        st.success("Đã lưu!")
