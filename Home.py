import streamlit as st
from utils.data_loader import load_data

st.set_page_config(
    page_title="GDG Members Analytics",
    page_icon="👥",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.image("public/gdsc-logo-round.png", width=150)
st.title("GDG Members Analytics")

st.markdown("""
### Welcome to GDG Members Analytics! 👋

This application helps you manage and analyze GDG membership data efficiently.

#### Available Features:
- **📧 Email Management**: Easily manage and export email lists
- **📊 Analytics Dashboard**: Visualize membership data and trends
- **👥 Member Directory**: Search and filter member information

#### Getting Started:
Use the sidebar navigation to explore different sections of the application.

#### Need Help?
Contact the GDG Tech Team for support.
""")

# Load data in background
load_data() 