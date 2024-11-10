import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(
    page_title="GDSC Registration Analytics",
    page_icon="📊",
    layout="wide"
)

# Function to load and preprocess data
@st.cache_data
def load_data():
    df = pd.read_csv("GDSC - Registration_Counter.csv")
    
    # Clean column names
    df.columns = [col.strip() for col in df.columns]
    
    # Extract email from first column
    df['Email'] = df.iloc[:, 0]
    
    # Extract name from GDSC ID
    df['Name'] = df['GDSC ID'].apply(lambda x: x.split('_')[0] if pd.notna(x) else '')
    
    # Add registration timestamp (for future use)
    df['Registration_Date'] = datetime.now().date()
    
    return df

# Main function to build the dashboard
def main():
    st.title("📊 GDSC Registration Analytics Dashboard")
    
    # Load data
    df = load_data()
    
    # Sidebar filters
    st.sidebar.header("Filters")
    
    # Group Type filter
    group_type = st.sidebar.multiselect(
        "Select Group Type",
        options=df['Group_Type'].unique(),
        default=df['Group_Type'].unique()
    )
    
    # Membership Duration filter
    membership_duration = st.sidebar.multiselect(
        "Select Membership Duration",
        options=df['Membership_Duration'].unique(),
        default=df['Membership_Duration'].unique()
    )
    
    # Apply filters
    filtered_df = df[
        (df['Group_Type'].isin(group_type)) &
        (df['Membership_Duration'].isin(membership_duration))
    ]
    
    # Key Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Registrations", len(filtered_df))
    
    with col2:
        total_groups = len(filtered_df[filtered_df['Group_Type'] == 'Group'])
        st.metric("Total Groups", total_groups)
    
    with col3:
        individual_registrations = len(filtered_df[filtered_df['Group_Type'] == 'Individual'])
        st.metric("Individual Registrations", individual_registrations)
    
    with col4:
        graduation_plans = len(filtered_df[filtered_df['Membership_Duration'] == 'Till Graduation'])
        st.metric("Graduation Plans", graduation_plans)
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Membership Type Distribution
        fig_membership = px.pie(
            filtered_df,
            names='Group_Type',
            title='Membership Type Distribution',
            hole=0.4
        )
        st.plotly_chart(fig_membership, use_container_width=True)
    
    with col2:
        # Duration Distribution
        fig_duration = px.pie(
            filtered_df,
            names='Membership_Duration',
            title='Membership Duration Distribution',
            hole=0.4
        )
        st.plotly_chart(fig_duration, use_container_width=True)
    
    # Registration Timeline (for future use when timestamps are available)
    st.subheader("Registration Timeline")
    timeline_data = filtered_df.groupby('Registration_Date').size().reset_index(name='count')
    fig_timeline = px.line(
        timeline_data,
        x='Registration_Date',
        y='count',
        title='Daily Registration Trend'
    )
    st.plotly_chart(fig_timeline, use_container_width=True)
    
    # Detailed Data View
    st.subheader("Detailed Registration Data")
    st.dataframe(
        filtered_df[['Name', 'Email', 'Group_Type', 'Membership_Duration', 'Payment_Method']],
        use_container_width=True
    )
    
    # Download filtered data
    st.download_button(
        label="Download Filtered Data",
        data=filtered_df.to_csv(index=False).encode('utf-8'),
        file_name='gdsc_registrations_filtered.csv',
        mime='text/csv'
    )

if __name__ == "__main__":
    main()