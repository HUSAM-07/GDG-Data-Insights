import pandas as pd
import streamlit as st

def get_academic_year(email):
    if pd.isna(email):
        return "Other"
    
    try:
        year = email[1:5]
        year_int = int(year)
        
        if year_int <= 2020:
            return "Graduate"
        
        if year == "2024":
            return "First Year"
        elif year == "2023":
            return "Second Year"
        elif year == "2022":
            return "Third Year"
        elif year == "2021":
            return "Fourth Year"
        else:
            return "Other"
    except:
        return "Other"

@st.cache_data
def load_data():
    df = pd.read_csv("manual_data_collection.csv")
    df_everybody = pd.read_csv("everybody.csv")
    df_members = pd.read_csv("members_current.csv")
    
    df.columns = [col.strip() for col in df.columns]
    df['Email_Domain'] = df['Email'].apply(lambda x: x.split('@')[1] if pd.notna(x) else '')
    df['Academic_Year'] = df['Email'].apply(get_academic_year)
    df['Education_Level'] = df['Under_Graduate'].fillna('Not Specified')
    
    return df, df_everybody, df_members 