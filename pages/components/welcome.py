import streamlit as st
from pages.stream_app.utils import hide_header_and_padding
from pages.components.header import header
from streamlit.components.v1 import html

def welcome():
    
    
    # st.title("Sổ trí tuệ")

    # st.html(
    # "<header style='padding-left: 0px; border-bottom: 1px solid #00000026; height: 80px; display: flex; justify-content: space-between; align-items: center;'>"
    #     "<div style='display: flex; align-items: center; gap: 11px;'>"
    #         "<img src='app/static/quoc-huy.png' alt='Logo' style='width: 32px; height: auto;'>"
    #         "<h1 class='h1'>Sổ trí tuệ</h1>"
    #     "</div>"
    #     "<div style='position: relative; width: 592px; height: 100%;'>"
    #         "<div style='mask-image: linear-gradient(to right, transparent, black 40%, black 60%, transparent); -webkit-mask-image: linear-gradient(to right, transparent, black 40%, black 60%, transparent); width: 592px; height: 100%; background-image: url(\"app/static/nav-bar-bg.png\"); background-size: cover; opacity: 0.7; background-position-y:78%;'></div>"
    #     "</div>"
    # "</header>"
    # )
    header()
    with st.container(key='kkkkkk'):
        # st.markdown("<div id='main-wrapper'>", unsafe_allow_html=True)
        st.html(
        "<div style='text-align: center; display: flex; flex-direction: column; align-items: center;'>"
            "<span style='font-size: 44px; font-weight: bold; color: #CC5F33;'>Tạo sổ tay đầu tiên của bạn</span>"
            "<span style='font-size: 24px; font-weight: 600;'>Trợ lý AI hỗ trợ viết và nghiên cứu, phát huy tối đa hiệu quả khi có các tài liệu do bạn cung cấp.</span>"
        "</div>"
        )
        # st.subheader("Trợ lý viết và nghiên cứu của bạn, được hỗ trợ bởi AI, hoạt động hiệu quả nhất khi có các tài liệu do bạn cung cấp.")

        col1, col2, col3 = st.columns(3)

        with col1:
            # st.markdown("<div>", unsafe_allow_html=True)
            st.image("data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiBzdHJva2U9IiNjYzVmMzMiIHN0cm9rZS13aWR0aD0iMiIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIiBzdHJva2UtbGluZWpvaW49InJvdW5kIiBjbGFzcz0ibHVjaWRlIGx1Y2lkZS11cGxvYWQtaWNvbiBsdWNpZGUtdXBsb2FkIj48cGF0aCBkPSJNMjEgMTV2NGEyIDIgMCAwIDEtMiAySDVhMiAyIDAgMCAxLTItMnYtNCIvPjxwb2x5bGluZSBwb2ludHM9IjE3IDggMTIgMyA3IDgiLz48bGluZSB4MT0iMTIiIHgyPSIxMiIgeTE9IjMiIHkyPSIxNSIvPjwvc3ZnPg==", width=48)
            st.subheader("Một chatbot dựa trên các nguồn của bạn")
            st.text("Tải tài liệu lên và Sổ trí tuệ sẽ trả lời các câu hỏi chi tiết hoặc hiển thị những thông tin quan trọng")
            # st.markdown("</div>", unsafe_allow_html=True)
            
        with col2:
            # st.markdown("<div>", unsafe_allow_html=True)
            st.image("data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiBzdHJva2U9IiNjYzVmMzMiIHN0cm9rZS13aWR0aD0iMiIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIiBzdHJva2UtbGluZWpvaW49InJvdW5kIiBjbGFzcz0ibHVjaWRlIGx1Y2lkZS1tZXNzYWdlLXNxdWFyZS10ZXh0LWljb24gbHVjaWRlLW1lc3NhZ2Utc3F1YXJlLXRleHQiPjxwYXRoIGQ9Ik0yMSAxNWEyIDIgMCAwIDEtMiAySDdsLTQgNFY1YTIgMiAwIDAgMSAyLTJoMTRhMiAyIDAgMCAxIDIgMnoiLz48cGF0aCBkPSJNMTMgOEg3Ii8+PHBhdGggZD0iTTE3IDEySDciLz48L3N2Zz4=", width=48)
            st.subheader("Nhanh chóng nắm được nội dung của tài liệu bất kỳ")
            st.text("Biến các tài liệu chuyên môn thành định dạng dễ hiểu hơn như Câu hỏi thường gặp hoặc Tóm tắt thông tin.")
            # st.markdown("</div>", unsafe_allow_html=True)

        with col3:
            # st.markdown("<div>", unsafe_allow_html=True)
            st.image("data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiBzdHJva2U9IiNjYzVmMzMiIHN0cm9rZS13aWR0aD0iMiIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIiBzdHJva2UtbGluZWpvaW49InJvdW5kIiBjbGFzcz0ibHVjaWRlIGx1Y2lkZS11c2Vycy1pY29uIGx1Y2lkZS11c2VycyI+PHBhdGggZD0iTTE2IDIxdi0yYTQgNCAwIDAgMC00LTRINmE0IDQgMCAwIDAtNCA0djIiLz48Y2lyY2xlIGN4PSI5IiBjeT0iNyIgcj0iNCIvPjxwYXRoIGQ9Ik0yMiAyMXYtMmE0IDQgMCAwIDAtMy0zLjg3Ii8+PHBhdGggZD0iTTE2IDMuMTNhNCA0IDAgMCAxIDAgNy43NSIvPjwvc3ZnPg==", width=48)
            st.subheader("Chia sẻ thông tin của bạn với mọi người")
            st.text("Thêm tài liệu quan trọng vào sổ tay và chia sẻ với tổ chức để xây dựng cơ sở tri thức chung.")
            # st.markdown("</div>", unsafe_allow_html=True)
        
        if st.button("Tạo sổ mới", type="primary"):
            st.switch_page("pages/2_📒_Notebooks.py")
        
        # st.markdown("</div>", unsafe_allow_html=True)
        
    # Nút tạo mới
    # col_center = st.columns([2, 1, 2])[1]
    # with col_center:
    #     if st.button("Tạo sổ mới", use_container_width=True, type="primary"):
    #         st.switch_page("pages/2_📒_Notebooks.py")
    

        # st.markdown('<div class="centered">', unsafe_allow_html=True)
        # st.markdown('<a class="link-try" href="#">Dùng thử sổ tay mẫu</a>', unsafe_allow_html=True)
        # st.markdown('</div>', unsafe_allow_html=True)

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
                    gap: 24px;
                }
                .stHorizontalBlock {
                    max-height: min-content;
                    gap: 24px;
                }
            </style>
        """, unsafe_allow_html=True)


