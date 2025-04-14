import streamlit as st



def welcome():
    
    st.title("📒 Open Notebook")
    st.html(
    "<div style='text-align: center; display: flex; flex-direction: column; align-items: center;'>"
        "<span style='font-size: 44px; font-weight: bold;'>Tạo sổ tay đầu tiên của bạn</span>"
        "<span style='font-size: 24px; font-weight: 600;'>Trợ lý AI hỗ trợ viết và nghiên cứu, phát huy tối đa hiệu quả khi có các tài liệu do bạn cung cấp.</span>"
    "</div>"
    )
    # st.subheader("Trợ lý viết và nghiên cứu của bạn, được hỗ trợ bởi AI, hoạt động hiệu quả nhất khi có các tài liệu do bạn cung cấp.")

    col1, col2, col3 = st.columns(3)

    with col1:
        # st.html(
        # "<div style='text-align: center; display: flex; flex-direction: column; align-items: center;'>"
        #     "<img src='data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiIGNsYXNzPSJsdWNpZGUgbHVjaWRlLXVwbG9hZC1pY29uIGx1Y2lkZS11cGxvYWQiPjxwYXRoIGQ9Ik0yMSAxNXY0YTIgMiAwIDAgMS0yIDJINWEyIDIgMCAwIDEtMi0ydi00Ii8+PHBvbHlsaW5lIHBvaW50cz0iMTcgOCAxMiAzIDcgOCIvPjxsaW5lIHgxPSIxMiIgeDI9IjEyIiB5MT0iMyIgeTI9IjE1Ii8+PC9zdmc+'></img>"
        #     "<p>Tải lên tài liệu</p>"
        #     "<p'>Tải lên các tài liệu của bạn, hệ thống sẽ hỗ trợ trả lời các câu hỏi chi tiết hoặc cung cấp thông tin trọng yếu.</p>"
        # "</div>"
        # )

        st.markdown("<div>", unsafe_allow_html=True)
        st.image("data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiIGNsYXNzPSJsdWNpZGUgbHVjaWRlLXVwbG9hZC1pY29uIGx1Y2lkZS11cGxvYWQiPjxwYXRoIGQ9Ik0yMSAxNXY0YTIgMiAwIDAgMS0yIDJINWEyIDIgMCAwIDEtMi0ydi00Ii8+PHBvbHlsaW5lIHBvaW50cz0iMTcgOCAxMiAzIDcgOCIvPjxsaW5lIHgxPSIxMiIgeDI9IjEyIiB5MT0iMyIgeTI9IjE1Ii8+PC9zdmc+", width=48)
        st.subheader("Một chatbot dựa trên các nguồn của bạn")
        st.text("Tải tài liệu lên và Open Notebook sẽ trả lời các câu hỏi chi tiết hoặc hiển thị những thông tin quan trọng")
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col2:
        st.markdown("<div>", unsafe_allow_html=True)
        st.image("data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiIGNsYXNzPSJsdWNpZGUgbHVjaWRlLW1lc3NhZ2Utc3F1YXJlLXRleHQtaWNvbiBsdWNpZGUtbWVzc2FnZS1zcXVhcmUtdGV4dCI+PHBhdGggZD0iTTIxIDE1YTIgMiAwIDAgMS0yIDJIN2wtNCA0VjVhMiAyIDAgMCAxIDItMmgxNGEyIDIgMCAwIDEgMiAyeiIvPjxwYXRoIGQ9Ik0xMyA4SDciLz48cGF0aCBkPSJNMTcgMTJINyIvPjwvc3ZnPg==", width=48)
        st.subheader("Nhanh chóng nắm được nội dung của tài liệu bất kỳ")
        st.text("Biến các tài liệu chuyên môn thành định dạng dễ hiểu hơn như Câu hỏi thường gặp hoặc Tóm tắt thông tin.")
        st.markdown("</div>", unsafe_allow_html=True)

    with col3:
        st.markdown("<div>", unsafe_allow_html=True)
        st.image("data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiIGNsYXNzPSJsdWNpZGUgbHVjaWRlLXVzZXJzLWljb24gbHVjaWRlLXVzZXJzIj48cGF0aCBkPSJNMTYgMjF2LTJhNCA0IDAgMCAwLTQtNEg2YTQgNCAwIDAgMC00IDR2MiIvPjxjaXJjbGUgY3g9IjkiIGN5PSI3IiByPSI0Ii8+PHBhdGggZD0iTTIyIDIxdi0yYTQgNCAwIDAgMC0zLTMuODciLz48cGF0aCBkPSJNMTYgMy4xM2E0IDQgMCAwIDEgMCA3Ljc1Ii8+PC9zdmc+", width=48)
        st.subheader("Chia sẻ thông tin của bạn với mọi người")
        st.text("Thêm tài liệu quan trọng vào sổ tay và chia sẻ với tổ chức để xây dựng cơ sở tri thức chung.")
        st.markdown("</div>", unsafe_allow_html=True)
        
    # Nút tạo mới
    col_center = st.columns([2, 1, 2])[1]
    with col_center:
        if st.button("Tạo sổ mới", use_container_width=True, type="primary"):
            st.switch_page("pages/2_📒_Notebooks.py")

        # st.markdown('<div class="centered">', unsafe_allow_html=True)
        # st.markdown('<a class="link-try" href="#">Dùng thử sổ tay mẫu</a>', unsafe_allow_html=True)
        # st.markdown('</div>', unsafe_allow_html=True)


