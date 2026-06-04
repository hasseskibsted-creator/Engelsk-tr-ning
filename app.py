import streamlit as st
import google.generativeai as genai

st.write("Starter diagnostik...")

try:
    api_key = st.secrets["API_KEY"]
    st.write("API-nøgle fundet i Streamlit Secrets.")
    
    genai.configure(api_key=api_key)
    
    st.write("Følgende modeller er tilgængelige for din nøgle:")
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            st.write(m.name)
            
except Exception as e:
    st.write("Systemet melder følgende fejl:")
    st.write(e)
