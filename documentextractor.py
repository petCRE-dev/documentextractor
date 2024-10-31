import streamlit as st
import asyncio
import json
import os
from extraction import analyze_document
from dotenv import load_dotenv
from streamlit_ace import st_ace
import time

import urllib
import base64

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

@st.dialog("test",width="large",)
def display_pdf():
    
    if st.session_state["uploaded_file"] !=None:
        base64_pdf = base64.b64encode(st.session_state["uploaded_file"].read()).decode('utf-8')
 
        # Embedding PDF in HTML
        pdf_display = F'<iframe src="data:application/pdf;base64,{base64_pdf}"  width="100%" height="200" type="application/pdf"></iframe>'
        
        # Displaying File
        st.markdown(pdf_display, unsafe_allow_html=True) 
        
        
    
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
            st.rerun()
        else:
            st.error("Ungültiges Username oder Password")


else:
    left,right = st.columns([0.5,0.5],gap="small")
    with right:
        st.button("Logout", on_click=logout, type="secondary", use_container_width=True)
    with left:
        st.button("Reset", on_click=reset, type="primary", use_container_width=True)
       

    
    st.header("Extrahierung von Text aus Dokumente")
    st.markdown('Klicke <a href="https://www.markdownguide.org/cheat-sheet/" target="_blank">hier</a>, um den Markdown Cheat-sheet zu öffnen!',unsafe_allow_html=True)
    # Fixed top buttons
    button_placeholder = st.empty()
    st.subheader("Resultat:")
    st.session_state["uploaded_file"] = st.sidebar.file_uploader("File hochladen", type=["pdf"])

    if "analysis_result" not in st.session_state:
        st.session_state["analysis_result"] = ""
        st.session_state["is_editing"] = False

    if st.session_state["uploaded_file"] != None:
        
        
        st.sidebar.button("view",on_click=display_pdf)
       

        with button_placeholder.container():
            analyze_button = st.button("Dokument analysieren")
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
                st.rerun()
        else:
            md_content  = st_ace( value=st.session_state["analysis_result"],placeholder='', height=400, language='markdown', theme='eclipse', keybinding='vscode', min_lines=12, max_lines=None, font_size=14, tab_size=4, wrap=True, show_gutter=True, show_print_margin=False, readonly=False, annotations=None, markers=None, auto_update=False, key=None)
            with button_placeholder.container():
                
                save_button = st.button("Änderungen speichern",disabled=st.session_state["analysis_result"]==md_content)
                cancel_button = st.button("Abbrechen",type="primary")
            if save_button:
                st.session_state["analysis_result"]=md_content
                st.session_state["is_editing"] = False
                st.rerun()
            if cancel_button:
                st.session_state["is_editing"] = False
                st.rerun()
                
        download_button=st.download_button("dokument herunterladen",data=st.session_state["analysis_result"],file_name="resultat.md",use_container_width=True,type="primary")
        if download_button:
            st.balloons()
            time.sleep(2.5)
            reset()
            st.rerun()
    
  
        