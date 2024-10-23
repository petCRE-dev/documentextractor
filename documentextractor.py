import streamlit as st
import asyncio
import json
import os
from extraction import analyze_document
from dotenv import load_dotenv


load_dotenv()

# Streamlit app setup
st.set_page_config(page_title="PDF Document Analysis", layout="wide")

if "analysis_result" not in st.session_state:
    st.session_state["analysis_result"] = ""
    st.session_state["is_editing"] = False
if "is_editing" not in st.session_state:
    st.session_state["is_editing"] = False   
if "authenticated" not in st.session_state:
    st.session_state["authenticated"]=False
if "uploaded_file" not in st.session_state:
    st.session_state["uploaded_file"]=None  
# Streamlit app setup


def login():
    st.session_state["authenticated"]=True
def logout():
    st.session_state["authenticated"] = False
def reset():
    for key in list(st.session_state.keys()):
        if key != "authenticated":
            del st.session_state[key]
    
    
if not st.session_state["authenticated"]:
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        if username ==  os.getenv("USERNAME") and password ==  os.getenv("PASSWORD"):
            login()
        else:
            st.error("Ungültiges Username oder Password")


else:
    left,right = st.columns([0.5,0.5],gap="small")
    with right:
        st.button("Logout", on_click=logout, type="primary", use_container_width=True)
    with left:
        st.button("Reset", on_click=reset, type="secondary", use_container_width=True)
       

    
    st.title("Extrahierung von Text aus Dokumente")

    # Fixed top buttons
    button_placeholder = st.empty()

    st.session_state["uploaded_file"] = st.sidebar.file_uploader("File hochladen", type=["pdf"])

    if "analysis_result" not in st.session_state:
        st.session_state["analysis_result"] = ""
        st.session_state["is_editing"] = False

    if st.session_state["uploaded_file"] != None:
        with button_placeholder.container():
            analyze_button = st.button("Analyze Document")
        if analyze_button:
            with st.spinner("Dokument wird analysiert..."):
                analysis_text = asyncio.run(analyze_document(st.session_state["uploaded_file"]))
                st.session_state["analysis_result"] = analysis_text
                st.session_state["is_editing"] = False

    if st.session_state["analysis_result"]:
        if not st.session_state["is_editing"]:
            st.markdown(st.session_state["analysis_result"])
            with button_placeholder.container():
                edit_button = st.button("✏️ Bearbeiten")
            if edit_button:
                st.session_state["is_editing"] = True
        else:
            edited_text = st.text_area("Resultat", value=st.session_state["analysis_result"], height=400)
            with button_placeholder.container():
                save_button = st.button("Änderungen speichern")
                cancel_button = st.button("Abbrechen",type="primary")
            if save_button:
                st.session_state["analysis_result"] = edited_text
                st.session_state["is_editing"] = False
            if cancel_button:
                st.session_state["is_editing"] = False
    
  
        