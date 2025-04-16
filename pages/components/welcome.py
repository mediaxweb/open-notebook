import streamlit as st
from pages.stream_app.utils import hide_header_and_padding
from pages.components.header import header
from streamlit.components.v1 import html

def welcome():
    header()
    with st.container(key='kkkkkk'):
        # st.markdown("<div id='main-wrapper'>", unsafe_allow_html=True)
        st.html(
        "<div style='text-align: center; display: flex; flex-direction: column; align-items: center;'>"
            "<span style='font-size: 44px; font-weight: bold; color: #CC5F33;'>Sổ tay tri thức hỗ trợ cán bộ, công chức trong công việc</span>"
            "<span style='font-size: 24px; font-weight: 600;'>Trợ lý AI giúp tra cứu, phân tích và khai thác hiệu quả các tài liệu nội bộ.</span>"
        "</div>"
        )
        # st.subheader("Trợ lý viết và nghiên cứu của bạn, được hỗ trợ bởi AI, hoạt động hiệu quả nhất khi có các tài liệu do bạn cung cấp.")

        col1, col2, col3 = st.columns(3)

        with col1:
            # st.markdown("<div>", unsafe_allow_html=True)
            st.image("data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiBzdHJva2U9IiNjYzVmMzMiIHN0cm9rZS13aWR0aD0iMiIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIiBzdHJva2UtbGluZWpvaW49InJvdW5kIiBjbGFzcz0ibHVjaWRlIGx1Y2lkZS11cGxvYWQtaWNvbiBsdWNpZGUtdXBsb2FkIj48cGF0aCBkPSJNMjEgMTV2NGEyIDIgMCAwIDEtMiAySDVhMiAyIDAgMCAxLTItMnYtNCIvPjxwb2x5bGluZSBwb2ludHM9IjE3IDggMTIgMyA3IDgiLz48bGluZSB4MT0iMTIiIHgyPSIxMiIgeTE9IjMiIHkyPSIxNSIvPjwvc3ZnPg==", width=48)
            st.subheader("Chatbot trợ lý nghiên cứu tài liệu")
            st.caption("Tải lên các tài liệu quan trọng – Trợ lý AI sẽ hỗ trợ trả lời câu hỏi chi tiết cho các nội dung trong tài liệu mà bạn cung cấp.")
            # st.markdown("</div>", unsafe_allow_html=True)
            
        with col2:
            # st.markdown("<div>", unsafe_allow_html=True)
            st.image("data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiBzdHJva2U9IiNjYzVmMzMiIHN0cm9rZS13aWR0aD0iMiIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIiBzdHJva2UtbGluZWpvaW49InJvdW5kIiBjbGFzcz0ibHVjaWRlIGx1Y2lkZS1tZXNzYWdlLXNxdWFyZS10ZXh0LWljb24gbHVjaWRlLW1lc3NhZ2Utc3F1YXJlLXRleHQiPjxwYXRoIGQ9Ik0yMSAxNWEyIDIgMCAwIDEtMiAySDdsLTQgNFY1YTIgMiAwIDAgMSAyLTJoMTRhMiAyIDAgMCAxIDIgMnoiLz48cGF0aCBkPSJNMTMgOEg3Ii8+PHBhdGggZD0iTTE3IDEySDciLz48L3N2Zz4=", width=48)
            st.subheader("Nắm bắt nhanh nội dung các tài liệu")
            st.caption("Hệ thống giúp chuyển các tài liệu chuyên môn thành dạng dễ hiểu hơn như: Câu hỏi thường gặp, tóm tắt nội dung, thông tin nổi bật.")
            # st.markdown("</div>", unsafe_allow_html=True)

        with col3:
            # st.markdown("<div>", unsafe_allow_html=True)
            st.image("data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiBzdHJva2U9IiNjYzVmMzMiIHN0cm9rZS13aWR0aD0iMiIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIiBzdHJva2UtbGluZWpvaW49InJvdW5kIiBjbGFzcz0ibHVjaWRlIGx1Y2lkZS11c2Vycy1pY29uIGx1Y2lkZS11c2VycyI+PHBhdGggZD0iTTE2IDIxdi0yYTQgNCAwIDAgMC00LTRINmE0IDQgMCAwIDAtNCA0djIiLz48Y2lyY2xlIGN4PSI5IiBjeT0iNyIgcj0iNCIvPjxwYXRoIGQ9Ik0yMiAyMXYtMmE0IDQgMCAwIDAtMy0zLjg3Ii8+PHBhdGggZD0iTTE2IDMuMTNhNCA0IDAgMCAxIDAgNy43NSIvPjwvc3ZnPg==", width=48)
            st.subheader("Chia sẻ tri thức trong tổ chức")
            st.caption("Chia sẻ các tài liệu quan trọng trong nội bộ cơ quan để xây dựng kho tri thức dùng chung, nâng cao hiệu quả làm việc và quản lý.")
            # st.markdown("</div>", unsafe_allow_html=True)
        
        if st.button("Tạo sổ mới", type="primary"):
            st.switch_page("pages/2_📒_Notebooks.py")
        
        # st.markdown("</div>", unsafe_allow_html=True)
        

        hide_header_and_padding()

        st.markdown("""
            <style>
                .st-key-kkkkkk {
                    overflow: visible;
                    background-image: url("app/static/bg.png");
                    background-size: 600px 600px;
                    background-position: center;
                    background-repeat: no-repeat;
                    min-height: 600px;  
                }
                .h1 { 
                    color: #CC5F33 !important;
                }
                h3 { 
                    font-size: 24px !important;
                    font-weight: 600 !important;
                }

                .stColumn {
                    text-align: -webkit-center; 
                    background-color: #F7F7F7;
                    padding: 32px 24px 32px 24px;
                    border-radius: 16px;
                }
                .stButton {
                    # margin-top: 16px;
                    text-align-last: center;
                }
                .stButton > button {
                    min-width: 185px;
                    min-height: 48px;
                }
                .stVerticalBlock {
                    gap: 32px;
                }
                .stHorizontalBlock {
                    max-height: min-content;
                    gap: 24px;
                }
            </style>
        """, unsafe_allow_html=True)


