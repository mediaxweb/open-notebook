import streamlit as st

def header():
     st.html(
    "<header style='background: white; padding-left: 0px; border-bottom: 0.5px solid #00000026; height: 80px; display: flex; justify-content: space-between; align-items: center; width: 100%;'>"
        "<div style='display: flex; align-items: center; gap: 11px; position: absolute; z-index: 10;'>"
            "<img src='app/static/quoc-huy.png' alt='Logo' style='width: 32px; height: auto;'>"
            "<span style='color: #CC5F33; font-weight: bold; font-size: 24px;'>Sổ Trí Tuệ</span>"
        "</div>"
        "<div style='position: relative; width: 592px; height: 100%; margin-left: auto;'>"
            "<div style='mask-image: linear-gradient(to right, transparent, black 40%, black 60%, transparent); -webkit-mask-image: linear-gradient(to right, transparent, black 40%, black 60%, transparent); width: 592px; height: 100%; background-image: url(\"app/static/nav-bar-bg.png\"); background-size: cover; opacity: 0.7; background-position-y:78%;'></div>"
        "</div>"
    "</header>"
    )