import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# Set page configuration
st.set_page_config(
    page_title="GDG Members Analytics",
    page_icon="👥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Function to load and preprocess data
@st.cache_data
def load_data():
    df = pd.read_csv("manual_data_collection.csv")
    df_everybody = pd.read_csv("everybody.csv")
    df_members = pd.read_csv("members_current.csv")
    
    # Clean column names
    df.columns = [col.strip() for col in df.columns]
    
    # Extract email domain
    df['Email_Domain'] = df['Email'].apply(lambda x: x.split('@')[1] if pd.notna(x) else '')
    
    # Clean education level
    df['Education_Level'] = df['Under_Graduate'].fillna('Not Specified')
    
    return df, df_everybody, df_members

def get_email_list(df, column_name='Email IDs'):
    """Extract and format email addresses from dataframe"""
    emails = df[column_name].dropna().tolist()
    return '; '.join(emails)

def main():
    # Header with logo and title
    col1, col2 = st.columns([1, 4])
    with col1:
        st.image("public/gdsc-logo-round.png", width=100)
    with col2:
        st.title("GDG Members Analytics Dashboard")
    
    # Load data
    df, df_everybody, df_members = load_data()
    
    # Email Lists Section
    st.header("📧 Email Management")
    
    tabs = st.tabs(["🌐 University-wide", "👥 GDG Members"])
    
    with tabs[0]:
        st.subheader("University Email List")
        all_emails = get_email_list(df_everybody)
        col1, col2 = st.columns([3, 1])
        with col1:
            st.text_area("All University Emails", all_emails, height=150)
        with col2:
            st.write("")  # Spacing
            if st.button("📋 Copy Emails", key="uni_copy", use_container_width=True):
                st.code(all_emails, language=None)
                st.success("✅ Click the copy button above!")
    
    with tabs[1]:
        st.subheader("GDG Members Email List")
        member_emails = get_email_list(df_members)
        col1, col2 = st.columns([3, 1])
        with col1:
            st.text_area("Member Emails", member_emails, height=150)
        with col2:
            st.write("")  # Spacing
            if st.button("📋 Copy Emails", key="member_copy", use_container_width=True):
                st.code(member_emails, language=None)
                st.success("✅ Click the copy button above!")

    st.divider()

    # Sidebar filters
    with st.sidebar:
        st.header("📊 Analytics Filters")
        st.divider()
        
        # Education Level filter with select all option
        st.subheader("Education Level")
        select_all = st.checkbox("Select All", value=True)
        if select_all:
            education_level = df['Education_Level'].unique()
        else:
            education_level = st.multiselect(
                "Choose levels:",
                options=df['Education_Level'].unique(),
                default=[]
            )

    # Apply filters
    filtered_df = df[df['Education_Level'].isin(education_level)]

    # Key Metrics
    st.header("📈 Key Metrics")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="Total Members",
            value=len(filtered_df)
        )
    
    with col2:
        undergrad_count = len(filtered_df[filtered_df['Education_Level'] == 'Under_Graduate'])
        st.metric(
            label="Undergraduate Students",
            value=undergrad_count
        )
    
    with col3:
        grad_count = len(filtered_df[filtered_df['Education_Level'] == 'Graduate'])
        st.metric(
            label="Graduate Students",
            value=grad_count
        )

    st.divider()

    # Visualizations in tabs
    st.header("📊 Analytics")
    viz_tabs = st.tabs(["Education", "Email Domains", "Gender"])
    
    with viz_tabs[0]:
        fig_education = px.pie(
            filtered_df,
            names='Education_Level',
            title='Education Level Distribution',
            hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        st.plotly_chart(fig_education, use_container_width=True)
    
    with viz_tabs[1]:
        domain_counts = filtered_df['Email_Domain'].value_counts().head(10)
        fig_domains = px.bar(
            domain_counts,
            title='Top 10 Email Domains',
            labels={'value': 'Count', 'index': 'Domain'}
        )
        st.plotly_chart(fig_domains, use_container_width=True)
    
    with viz_tabs[2]:
        if 'Gender' in filtered_df.columns:
            gender_data = filtered_df['Gender'].value_counts()
            fig_gender = px.pie(
                values=gender_data.values,
                names=gender_data.index,
                title='Gender Distribution',
                color_discrete_sequence=px.colors.qualitative.Set2
            )
            st.plotly_chart(fig_gender, use_container_width=True)
        else:
            st.info("👉 Gender data is not available in the current dataset")

    st.divider()

    # Data Table with search
    st.header("📋 Member Details")
    
    # Search functionality
    search = st.text_input("🔍 Search by name or email")
    if search:
        filtered_df = filtered_df[
            filtered_df['Name'].str.contains(search, case=False, na=False) |
            filtered_df['Email'].str.contains(search, case=False, na=False)
        ]
    
    st.dataframe(
        filtered_df[['Name', 'Email', 'Education_Level']],
        use_container_width=True,
        height=400
    )
    
    st.divider()
    
    # Export section
    col1, col2 = st.columns([1, 4])
    with col1:
        st.download_button(
            label="📥 Export Data",
            data=filtered_df.to_csv(index=False).encode('utf-8'),
            file_name='gdg_members_data.csv',
            mime='text/csv',
            use_container_width=True
        )

if __name__ == "__main__":
    main()