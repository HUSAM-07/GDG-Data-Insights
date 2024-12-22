import streamlit as st
from utils.data_loader import load_data
from utils.email_utils import get_email_list

st.title("📧 Email Management")

# Email Usage Guidelines
st.markdown("""
### 📧 Email Usage Guidelines

> **Privacy Notice:**
> - Always use BCC when sending mass emails to protect member privacy
> - This prevents recipients from seeing other members' email addresses
> - Helps avoid unauthorized email collection

> **Email Signature Requirement:**
> - All official communications must include the GDG signature
> - This maintains professionalism and brand consistency
> - Helps recipients identify official GDG communications
""")

# ... rest of email management code ... 