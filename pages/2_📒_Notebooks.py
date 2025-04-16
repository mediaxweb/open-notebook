import streamlit as st
from humanize import naturaltime

from open_notebook.domain.notebook import Notebook
from pages.stream_app.chat import chat_sidebar
from pages.stream_app.note import add_note, note_card
from pages.stream_app.source import add_source, source_card
from pages.stream_app.utils import setup_page, setup_stream_state, hide_header_and_padding, convert_to_vn_time
from pages.components.header import header

setup_page("Sổ trí tuệ", only_check_mandatory_models=True)



def notebook_header(current_notebook: Notebook):
    # c1, c2, c3 = st.columns([8, 2, 2])
    # if c3.button("Refresh", icon="🔄"):
    #     st.rerun()
    
    # xếp dọc có thể sẽ đẹp hơn?
    # c1, c2 = st.columns([7, 1])

    # with c1:
    #     st.header(current_notebook.name)
    # with c2:
    #     st.markdown("<div>", unsafe_allow_html=True)
    #     if st.button("⬅️ Quay lại", key="back_button"):
    #         st.session_state["current_notebook_id"] = None
    #         st.rerun()
    #     st.markdown("</div>", unsafe_allow_html=True)

    # if st.button("⬅️ Quay lại", key="back_button"):
    #     st.session_state["current_notebook_id"] = None
    #     st.rerun()

    # with st.container(key="header"):
    #     if st.button("Quay lại", icon=':material/arrow_back:', key="back_button"):
    #         st.session_state["current_notebook_id"] = None
    #         st.rerun()
    
    #     st.html(
    #     f"""
    #         <div style="display: flex; align-items: center; gap: 11px; width: fit-content" class="header-title">
    #             <img src="app/static/quoc-huy.png" width="32" height="32"/>
    #             <span style="font-size: 24px; font-weight: 600; line-height: 32px;">
    #                 {current_notebook.name}
    #             </span>
    #         </div>
    #     """)

    st.html(
        f"""
            <div style="display: flex; align-items: center; gap: 11px; width: fit-content; margin-top:16px" class="header-title">
                <img src="app/static/quoc-huy.png" width="32" height="32"/>
                <span style="font-size: 24px; font-weight: 600; line-height: 32px;">
                    {current_notebook.name}
                </span>
            </div>
        """)
        
    current_description = current_notebook.description
    # with st.expander(
    #     # current_notebook.description
    #     # if len(current_description) > 0
    #     # else "Click để thêm mô tả",
    #     "Xem thông tin sổ"
    # ):
    #     notebook_name = st.text_input("Tên", value=current_notebook.name)
    #     notebook_description = st.text_area(
    #         "Mô tả",
    #         value=current_description,
    #         placeholder="Mô tả ngữ cảnh chi tiết nhất có thể để AI đưa ra câu trả lời chính xác nhất!",
    #     )
    #     c1, c2, c3 = st.columns([1, 1, 1])
    #     if c1.button("Cập nhật", icon=":material/save_as:", key="edit_notebook"):
    #         current_notebook.name = notebook_name
    #         current_notebook.description = notebook_description
    #         current_notebook.save()
    #         st.rerun()
    #     if not current_notebook.archived:
    #         if c2.button("Lưu trữ", icon=":material/archive:"):
    #             current_notebook.archived = True
    #             current_notebook.save()
    #             st.toast("Đã đưa sổ vào lưu trữ", icon="🗃️")
    #     else:
    #         if c2.button("Khôi phục", icon=":material/unarchive:"):
    #             current_notebook.archived = False
    #             current_notebook.save()
    #             st.toast("Đã khôi phục sổ!", icon="🗃️")
    #     if c3.button("Xóa", type="primary", icon=":material/delete:"):
    #         current_notebook.delete()
    #         st.session_state["current_notebook_id"] = None
    #         st.rerun()


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
        sources_tab, chat_tab, notes_tab = st.columns([2, 4, 2])
        with sources_tab:
            with st.container(border=True, key="sources_tab"):
                with st.container(key="sources_tab_header"):
                    st.subheader("Tài liệu", divider="gray")
                    if st.button("Thêm tài liệu", icon=":material/add:", type="primary", use_container_width=True):
                        add_source(current_notebook.id)
            
                if len(sources) == 0:
                    with st.container(key="no_sources"):
                        st.image("data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiBzdHJva2U9IiNkNmQ2ZDYiIHN0cm9rZS13aWR0aD0iMiIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIiBzdHJva2UtbGluZWpvaW49InJvdW5kIiBjbGFzcz0ibHVjaWRlIGx1Y2lkZS1maWxlLXRleHQtaWNvbiBsdWNpZGUtZmlsZS10ZXh0Ij48cGF0aCBkPSJNMTUgMkg2YTIgMiAwIDAgMC0yIDJ2MTZhMiAyIDAgMCAwIDIgMmgxMmEyIDIgMCAwIDAgMi0yVjdaIi8+PHBhdGggZD0iTTE0IDJ2NGEyIDIgMCAwIDAgMiAyaDQiLz48cGF0aCBkPSJNMTAgOUg4Ii8+PHBhdGggZD0iTTE2IDEzSDgiLz48cGF0aCBkPSJNMTYgMTdIOCIvPjwvc3ZnPg==", width=52)
                        st.caption('Các nguồn đã lưu sẽ xuất hiện ở đây. Nhấp vào Thêm nguồn ở trên để thêm tệp PDF, trang web, văn bản, video hoặc âm thanh. Hoặc nhập tệp trực tiếp từ Google Drive.')

                for source in sources:
                    source_card(source=source, notebook_id=current_notebook.id)
                    
        with chat_tab:
            chat_sidebar(current_notebook=current_notebook, current_session=current_session)

        with notes_tab:
            with st.container(border=True, key="notes_tab"):
                with st.container(key="notes_tab_header"):
                    st.subheader("Ghi chú", divider="gray")
                    if st.button("Thêm ghi chú", type="secondary", use_container_width=True):
                        add_note(current_notebook.id)
                if len(notes) == 0:
                    with st.container(key="no_notes"):
                        st.image("data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiBzdHJva2U9IiNkNmQ2ZDYiIHN0cm9rZS13aWR0aD0iMiIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIiBzdHJva2UtbGluZWpvaW49InJvdW5kIiBjbGFzcz0ibHVjaWRlIGx1Y2lkZS1maWxlLXRleHQtaWNvbiBsdWNpZGUtZmlsZS10ZXh0Ij48cGF0aCBkPSJNMTUgMkg2YTIgMiAwIDAgMC0yIDJ2MTZhMiAyIDAgMCAwIDIgMmgxMmEyIDIgMCAwIDAgMi0yVjdaIi8+PHBhdGggZD0iTTE0IDJ2NGEyIDIgMCAwIDAgMiAyaDQiLz48cGF0aCBkPSJNMTAgOUg4Ii8+PHBhdGggZD0iTTE2IDEzSDgiLz48cGF0aCBkPSJNMTYgMTdIOCIvPjwvc3ZnPg==", width=52)
                        st.caption('Các ghi chú đã lưu sẽ xuất hiện ở đây. Nhấp vào Thêm ghi chú ở trên để thêm ghi chú mới, hoặc trực tiếp thêm ghi chú từ phần hỏi đáp.')

                for note in notes:
                    note_card(note=note, notebook_id=current_notebook.id)

    st.markdown("""
        <style>
            .st-key-sources_tab > :first-child {
                # border-bottom: 1px solid #E4E4E7;
                position: sticky;
                top: 0;
                z-index: 10;
                background-color: white;
            }
            # .st-key-sources_tab_header > :first-child {
            #     border-bottom: 1px solid #E4E4E7;
            # }
            # .st-key-sources_tab > :nth-child(2) {
            #     position: sticky;
            #     top: 0;
            #     z-index: 10;
            #     background-color: white;
            # }
            .st-key-notes_tab > :first-child {
                # border-bottom: 1px solid #E4E4E7;
                position: sticky;
                top: 0;
                z-index: 10;
                background-color: white;
            }
            # .st-key-notes_tab_header > :first-child {
            #     border-bottom: 1px solid #E4E4E7;
            # }
            .st-key-chat_tab > :first-child {
                # border-bottom: 1px solid #E4E4E7;
                # position: sticky;
                # top: 0;
                # z-index: 10;
                # background-color: white;
                height: fit-content;
 
                display: flex;
                align-items: center;
                justify-content: center;
                font-weight: bold;
                flex-shrink: 0;
            }
            .st-key-chat_tab > :nth-child(2) {
                flex: 1;
                overflow-y: auto;
            }

            .st-key-chat_tab > :last-child {
                # border-bottom: 1px solid #E4E4E7;
                # position: sticky;
                # bottom: 0;
                # z-index: 10;
                # background-color: white;
                height: fit-content;
 
                display: flex;
                align-items: end;
                justify-content: center;
                font-weight: bold;
                flex-shrink: 0;
            }
            # .st-key-chat_tab_header > :first-child {
            #     border-bottom: 1px solid #E4E4E7;
            # }
            .st-key-sources_tab {
                padding-bottom: 15px;
                # gap: 0px;
            }
            .st-key-notes_tab {
                padding-bottom: 15px;
            }
            .st-key-chat_tab {
                overflow: hidden;
                padding-bottom: 15px;
            }
            # .st-key-chat_tab {
            #     # min-height: calc(100vh - 100px);
            #     # max-height: calc(100vh - 100px);
            #     # overflow-y: auto;
            #     # overflow-x: visible;
            #     # background-image: url("app/static/bg.png");
            #     # background-size: 600px 600px;
            #     # background-position: center;
            #     # background-repeat: no-repeat;
            # }
            .stApp {
                background-color: #F9F5F4;
            }
            # .stVerticalBlock {
            #     # background-color: white;
            #     # min-height: calc(100vh - 100px);
            #     max-height: calc(100vh - 100px);
            #     overflow-y: auto;
            #     # overflow-x: visible;
            # }
            .st-key-no_sources {
                display: flex;
                justify-content: center;
                height: 100%;
                align-items: center;
                text-align: -webkit-center;
                # margin-bottom: 48px;
            }
            .st-key-no_notes {
                display: flex;
                justify-content: center;
                height: 100%;
                align-items: center;
                text-align: -webkit-center;
                # margin-bottom: 48px;
            }
            .st-key-header {
                margin-top: 16px;
            }
            .st-key-back_button {
                z-index: 10;
                text-align-last: end;
            }
            # .stAppViewContainer {
            #     background-image: url("app/static/bg.png");
            #     background-size: 600px 600px;
            #     background-position: center;
            #     background-repeat: no-repeat;
            # }
            # .stColumn {
            #     background-color: white;    
            # }
            div:has(> div > .st-key-chat_tab) {
                background-color: white; 
                # background-image: url("app/static/bg.png");
                # background-size: calc(100vh - 250px) auto;
                # background-position: center;
                # background-repeat: no-repeat;
                min-height: calc(100vh - 100px);
                max-height: calc(100vh - 100px);
                overflow-y: auto;  
                padding: 0px 15px 0px 15px; 
            }
            div:has(> div > .st-key-chat_tab_body) {
                background-color: white; 
                background-image: url("app/static/bg.png");
                background-size: calc(100vh - 250px) auto;
                background-position: center;
                background-repeat: no-repeat;
            }
            div:has(> div > .st-key-sources_tab) {
                background-color: white;    
                min-height: calc(100vh - 100px);
                max-height: calc(100vh - 100px);
                overflow-y: auto;
                padding: 0px 15px 0px 15px;
            }
            div:has(> div > .st-key-notes_tab) {
                background-color: white;    
                min-height: calc(100vh - 100px);
                max-height: calc(100vh - 100px);
                overflow-y: auto;
                padding: 0px 15px 0px 15px;
            }
            div:has(> .st-key-sources_tab) {
                height: calc(100vh - 215px);
            }
            div:has(> .st-key-notes_tab) {
                height: calc(100vh - 215px);
            }
            div:has(> .st-key-chat_tab) {
                height: calc(100vh - 105px);
            }
            div:has(> div > .st-key-no_sources) {
                flex: 1; 
                display: flex;
                align-items: center;
                justify-content: center;
            }
            div:has(> div > .st-key-no_notes) {
                flex: 1; 
                display: flex;
                align-items: center;
                justify-content: center;
            }
            .stChatMessage {
                # border-bottom: none;
            }
            .stExpander {
                background-color: white;
            }
            .stButton > button {
                min-width: 100px;
                min-height: 40px;
                color: #CC5F33;
                border-color: #CC5F33;
                border-radius: 4px;
            }
            div[class*="st-key-source"] > div > button {
                border-color: rgba(49, 51, 63, 0.2) !important;
                color: inherit !important;
            }
            div[class*="st-key-edit_note"] > div > button {
                border-color: rgba(49, 51, 63, 0.2) !important;
                color: inherit !important;
            }
            div[class*="st-key-render_save"] > div > button {
                border-color: rgba(49, 51, 63, 0.2) !important;
                color: inherit !important;
            }
            # .stVerticalBlock > div[data-testid="stVerticalBlockBorderWrapper"] {
            #     border-radius: 4px;    
            # }
            div.stSelectbox > div[data-baseweb="select"] > div {
                background-color: #F9F5F4;
                border-radius: 4px;
            }
            button[kind="primary"] {
                color: white;
            }
            .stHeading > hr {
                height: 1px !important;    
            }
            .stHeading > div > div > h3 {
                font-size: 24px !important;
                font-weight: 500 !important;
            }
            .stChatMessage:has([data-testid="stChatMessageAvatarUser"]) {
                display: flex;
                flex-direction: row-reverse;
                align-itmes: end;
            }

            [data-testid="stChatMessageAvatarUser"] + [data-testid="stChatMessageContent"] {
                text-align: right;
            }
            # @media (min-width: 48rem) {
            #     .header-title {
            #         margin-top: -52px;
            #     }
            # }
        </style>
        
    """, unsafe_allow_html=True)
    with open( "style.css" ) as css:
        st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)

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

if st.session_state["current_notebook_id"] is None:
    header()

# todo: get the notebook, check if it exists and if it's archived
if st.session_state["current_notebook_id"]:
    current_notebook: Notebook = Notebook.get(st.session_state["current_notebook_id"])
    if not current_notebook:
        st.error("Notebook not found")
        st.stop()
    notebook_page(current_notebook)
    hide_header_and_padding()
    st.stop()

st.title("Sổ tay tri thức của tỉnh")
st.caption(
    "Sổ tay là công cụ hữu ích giúp tổ chức, lưu trữ và truy xuất các tài liệu, ý tưởng, quy trình làm việc của các phòng ban . Quý đơn vị có thể tạo các sổ tay riêng cho từng chủ đề, lĩnh vực hoặc dự án phục vụ quản lý và nghiên cứu."
)
# st.divider()

with st.expander("**Tạo sổ mới**", icon=":material/add:"):
    new_notebook_title = st.text_input("Tên sổ", placeholder="Tên sổ mới")
    new_notebook_description = st.text_area(
        "Mô tả",
        placeholder="Mô tả về sổ",
    )
    if st.button("Tạo mới", icon=":material/add:"):
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

# if len(archived_notebooks) > 0:
#     with st.expander(f"**🗃️ Đã lưu trữ {len(archived_notebooks)} sổ**"):
#         st.write("ℹ️ Sổ đã lưu vẫn có thể sử dụng")
#         for notebook in archived_notebooks:
#             notebook_list_item(notebook)

hide_header_and_padding()
st.markdown(
        """
        <style>
            # .st-key-back_button {
            #     text-align-last: end;
            # }
            .stButton > button {
                min-width: 100px;
                min-height: 40px;
                border-radius: 4px;
                color: #CC5F33;
                border-color: #CC5F33;
            }
            .stVerticalBlockBorderWrapper {
                border-radius: 4px !important;
            }
            h1 {
                color: #CC5F33 !important;
                font-size: 40px !important;
                font-weight: 600 !important;
                padding: 16px 0px 8px 0px !important;
            }
            h3 {
                font-size: 24px !important;
                font-weight: 500 !important;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )
with open( "style.css" ) as css:
    st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)