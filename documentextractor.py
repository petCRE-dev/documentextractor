import streamlit as st
import asyncio
import json
from extraction import analyze_document


if "analysis_result" not in st.session_state:
    st.session_state["analysis_result"] = ""
    st.session_state["is_editing"] = False
if "is_editing" not in st.session_state:
    st.session_state["is_editing"] = False
# Streamlit app setup

st.title("PDF Document Analysis with Azure AI")

uploaded_file = st.sidebar.file_uploader("Upload a PDF file", type=["pdf"],accept_multiple_files=False)
with st.container():

    if uploaded_file is not None:
        if st.button("Analyze Document"):
            with st.spinner("Analyzing document..."):
                analysis_text = asyncio.run(analyze_document(uploaded_file))
                st.session_state["analysis_result"] = analysis_text
                st.session_state["is_editing"] = False
                uploaded_file = None

    if st.session_state["analysis_result"]:
        if not st.session_state["is_editing"]:
            st.markdown(st.session_state["analysis_result"])
            if st.button("Edit Document"):
                st.session_state["is_editing"] = True
        else:
            edited_text = st.text_area("Edit Analysis Result", value=st.session_state["analysis_result"], height=400)
            if st.button("Save Changes"):
                st.session_state["analysis_result"] = edited_text
                st.session_state["is_editing"] = False
            if st.button("Cancel Editing"):
                st.session_state["is_editing"] = False