import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# Page Configuration
st.set_page_config(
    page_title="GDG Members Analytics",
    page_icon="👥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Function to determine academic year from email
def get_academic_year(email):
    if pd.isna(email):
        return "Other"
    
    try:
        # Extract year from email (format: f20210150@dubai.bits-pilani.ac.in)
        year = email[1:5]  # Get the year part (2021)
        
        # Convert year to integer for comparison
        year_int = int(year)
        
        # Check if graduate (2020 or earlier)
        if year_int <= 2020:
            return "Graduate"
        
        # Current students
        if year == "2024":
            return "First Year"
        elif year == "2023":
            return "Second Year"
        elif year == "2022":
            return "Third Year"
        elif year == "2021":
            return "Fourth Year"
        else:
            return "Other"  # For administrative/professor emails
    except:
        return "Other"

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
    
    # Add Academic Year based on email
    df['Academic_Year'] = df['Email'].apply(get_academic_year)
    
    # Clean education level
    df['Education_Level'] = df['Under_Graduate'].fillna('Not Specified')
    
    return df, df_everybody, df_members

def get_email_list(df, column_name='Email IDs'):
    """Extract and format email addresses from dataframe"""
    emails = df[column_name].dropna().tolist()
    return '; '.join(emails)

def main():
    # Load data first
    df, df_everybody, df_members = load_data()
    
    # Quick Email Copy Button at Top
    st.header("🚀 Quick Actions")
    
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
    
    st.divider()
    
    quick_cols = st.columns([2, 2, 6])
    with quick_cols[0]:
        if st.button("📋 Copy All Emails", use_container_width=True):
            all_emails = get_email_list(df_everybody)
            st.code(all_emails, language=None)
            st.success("✅ Click the copy button above!")
    with quick_cols[1]:
        if st.button("📋 Copy Member Emails", use_container_width=True):
            member_emails = get_email_list(df_members)
            st.code(member_emails, language=None)
            st.success("✅ Click the copy button above!")
    
    st.divider()

    # Member Details Table
    st.header("👥 Member Details")
    
    # Search and Filter
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        search = st.text_input("🔍 Search by name or email", key="member_details_search")
    with col2:
        education_filter = st.multiselect(
            "Education Level",
            options=df['Education_Level'].unique(),
            default=df['Education_Level'].unique(),
            key="member_details_education"
        )
    with col3:
        sort_by = st.selectbox(
            "Sort by", 
            ["Name", "Email", "Education Level"],
            key="member_details_sort"
        )

    # Filter and sort data
    filtered_df = df[df['Education_Level'].isin(education_filter)]
    if search:
        filtered_df = filtered_df[
            filtered_df['Name'].str.contains(search, case=False, na=False) |
            filtered_df['Email'].str.contains(search, case=False, na=False)
        ]
    
    # Sort data
    if sort_by == "Name":
        filtered_df = filtered_df.sort_values("Name")
    elif sort_by == "Email":
        filtered_df = filtered_df.sort_values("Email")
    else:
        filtered_df = filtered_df.sort_values("Education_Level")

    # Display table with enhanced styling
    st.dataframe(
        filtered_df[['Name', 'Email', 'Education_Level']],
        use_container_width=True,
        height=400,
        column_config={
            "Name": st.column_config.TextColumn("Name", width="medium"),
            "Email": st.column_config.TextColumn("Email", width="large"),
            "Education_Level": st.column_config.TextColumn("Education", width="small")
        },
        hide_index=True
    )

    # Table actions
    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        st.download_button(
            "📥 Export to CSV",
            data=filtered_df.to_csv(index=False).encode('utf-8'),
            file_name='gdg_members.csv',
            mime='text/csv',
            use_container_width=True
        )
    with col2:
        if st.button("📋 Copy Filtered Emails", use_container_width=True):
            filtered_emails = '; '.join(filtered_df['Email'].dropna().tolist())
            st.code(filtered_emails, language=None)
            st.success("✅ Click the copy button above!")

    # Show table stats
    st.caption(f"Showing {len(filtered_df)} members out of {len(df)} total members")

    # Sidebar Navigation
    with st.sidebar:
        st.image("public/gdsc-logo-round.png", width=100)
        st.title("Navigation")
        
        page = st.radio(
            "Select Section",
            ["📧 Email Management", "📊 Analytics Dashboard", "👥 Member Directory"]
        )
        
        st.divider()
        
        # Filters (shown only for Analytics and Directory)
        if page in ["📊 Analytics Dashboard", "👥 Member Directory"]:
            st.header("Filters")
            
            # Education Level filter
            st.subheader("Education Level")
            select_all = st.checkbox("Select All", value=True)
            if select_all:
                education_level = df['Education_Level'].unique()
            else:
                education_level = st.multiselect(
                    "Choose levels:",
                    options=df['Education_Level'].unique(),
                    default=[],
                    key="sidebar_education"
                )
            
            # Year filter
            year_options = [
                "All Years",
                "First Year",
                "Second Year",
                "Third Year",
                "Fourth Year",
                "Other"
            ]
            
            year_filter = st.selectbox(
                "Academic Year",
                year_options
            )

    # Main Content Area
    if page == "📧 Email Management":
        st.header("📧 Email Management")
        
        # Email List Type Selector
        email_type = st.selectbox(
            "Select Email List",
            ["University-wide", "GDG Members"],
            format_func=lambda x: f"🌐 {x}" if x == "University-wide" else f"👥 {x}"
        )
        
        if email_type == "University-wide":
            all_emails = get_email_list(df_everybody)
            col1, col2 = st.columns([4, 1])
            with col1:
                st.text_area("University Emails", all_emails, height=200)
            with col2:
                st.write("")
                if st.button("📋 Copy All", use_container_width=True, key="copy_all_university"):
                    st.code(all_emails, language=None)
                    st.success("✅ Click the copy button above!")
                
                # Download option
                st.download_button(
                    "📥 Download List",
                    data=all_emails,
                    file_name="university_emails.txt",
                    mime="text/plain",
                    use_container_width=True
                )
        
        else:
            member_emails = get_email_list(df_members)
            col1, col2 = st.columns([4, 1])
            with col1:
                st.text_area("Member Emails", member_emails, height=200)
            with col2:
                st.write("")
                if st.button("📋 Copy All", use_container_width=True, key="copy_all_members"):
                    st.code(member_emails, language=None)
                    st.success("✅ Click the copy button above!")
                
                # Download option
                st.download_button(
                    "📥 Download List",
                    data=member_emails,
                    file_name="member_emails.txt",
                    mime="text/plain",
                    use_container_width=True
                )

    elif page == "📊 Analytics Dashboard":
        st.header("📊 Analytics Dashboard")
        
        # Apply filters
        filtered_df = df[df['Education_Level'].isin(education_level)]
        if year_filter != "All Years":
            filtered_df = filtered_df[filtered_df['Academic_Year'] == year_filter]
        
        # Metrics Row
        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.metric("Total Members", len(filtered_df))
        with m2:
            st.metric("Undergraduates", 
                     len(filtered_df[filtered_df['Education_Level'] == 'Under_Graduate']))
        with m3:
            st.metric("Graduates", 
                     len(filtered_df[filtered_df['Education_Level'] == 'Graduate']))
        with m4:
            st.metric("Active Members", 
                     len(df_members))
        
        # Charts
        chart_type = st.selectbox(
            "Select Visualization",
            ["Year-wise Distribution", "Education Distribution", "Email Domain Analysis", "Gender Distribution"]
        )
        
        if chart_type == "Year-wise Distribution":
            # Create two columns for the charts
            col1, col2 = st.columns(2)
            
            with col1:
                # GDG Members Distribution by Year
                member_emails = set(df_members['Email IDs'].dropna())
                year_dist_members = filtered_df[filtered_df['Email'].isin(member_emails)]['Academic_Year'].value_counts()
                
                fig_members = px.bar(
                    year_dist_members,
                    title='GDG Members Distribution by Year',
                    labels={'value': 'Number of Members', 'index': 'Academic Year'},
                    color_discrete_sequence=['#e5511b']  # GDG Orange color
                )
                fig_members.update_layout(showlegend=False)
                st.plotly_chart(fig_members, use_container_width=True)
                
                # Show percentages
                st.write("Membership Percentage by Year:")
                total_members = len(df_members)
                for year, count in year_dist_members.items():
                    percentage = (count / total_members) * 100
                    st.write(f"- {year}: {percentage:.1f}% ({count} members)")
            
            with col2:
                # Non-Members Distribution by Year
                non_member_emails = set(filtered_df['Email']) - set(df_members['Email IDs'].dropna())
                year_dist_non_members = filtered_df[filtered_df['Email'].isin(non_member_emails)]['Academic_Year'].value_counts()
                
                fig_non_members = px.bar(
                    year_dist_non_members,
                    title='Non-Members Distribution by Year',
                    labels={'value': 'Number of Non-Members', 'index': 'Academic Year'},
                    color_discrete_sequence=['#4285f4']  # Google Blue color
                )
                fig_non_members.update_layout(showlegend=False)
                st.plotly_chart(fig_non_members, use_container_width=True)
                
                # Show percentages
                st.write("Non-Member Percentage by Year:")
                total_non_members = len(non_member_emails)
                for year, count in year_dist_non_members.items():
                    percentage = (count / total_non_members) * 100
                    st.write(f"- {year}: {percentage:.1f}% ({count} non-members)")
            
            # Overall Statistics
            st.divider()
            st.subheader("📊 Year-wise Membership Rate")
            for year in set(year_dist_members.index) | set(year_dist_non_members.index):
                members = year_dist_members.get(year, 0)
                non_members = year_dist_non_members.get(year, 0)
                total = members + non_members
                if total > 0:
                    membership_rate = (members / total) * 100
                    st.write(f"**{year}**: {membership_rate:.1f}% membership rate ({members} members out of {total} students)")
        
        elif chart_type == "Education Distribution":
            fig = px.pie(
                filtered_df,
                names='Education_Level',
                title='Education Level Distribution',
                hole=0.4,
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            st.plotly_chart(fig, use_container_width=True)
            
        elif chart_type == "Email Domain Analysis":
            domain_counts = filtered_df['Email_Domain'].value_counts().head(10)
            fig = px.bar(
                domain_counts,
                title='Top 10 Email Domains',
                labels={'value': 'Count', 'index': 'Domain'}
            )
            st.plotly_chart(fig, use_container_width=True)
            
        else:  # Gender Distribution
            if 'Gender' in filtered_df.columns:
                gender_data = filtered_df['Gender'].value_counts()
                fig = px.pie(
                    values=gender_data.values,
                    names=gender_data.index,
                    title='Gender Distribution',
                    color_discrete_sequence=px.colors.qualitative.Set2
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("👉 Gender data is not available")

    else:  # Member Directory
        st.header("👥 Member Directory")
        
        # Search and Filter Options
        col1, col2 = st.columns([3, 1])
        with col1:
            search = st.text_input("🔍 Search by name or email", key="member_directory_search")
        with col2:
            sort_by = st.selectbox("Sort by", ["Name", "Email", "Education Level"])
        
        # Apply filters and search
        filtered_df = df[df['Education_Level'].isin(education_level)]
        if year_filter != "All Years":
            filtered_df = filtered_df[filtered_df['Academic_Year'] == year_filter]
        if search:
            filtered_df = filtered_df[
                filtered_df['Name'].str.contains(search, case=False, na=False) |
                filtered_df['Email'].str.contains(search, case=False, na=False)
            ]
        
        # Display member table
        st.dataframe(
            filtered_df[['Name', 'Email', 'Education_Level', 'Academic_Year']],
            use_container_width=True,
            height=400,
            column_config={
                "Name": st.column_config.TextColumn("Name", width="medium"),
                "Email": st.column_config.TextColumn("Email", width="large"),
                "Education_Level": st.column_config.TextColumn("Education", width="small"),
                "Academic_Year": st.column_config.TextColumn("Year", width="small")
            }
        )
        
        # Export option
        st.download_button(
            "📥 Export to CSV",
            data=filtered_df.to_csv(index=False).encode('utf-8'),
            file_name='gdg_members.csv',
            mime='text/csv'
        )

if __name__ == "__main__":
    main()