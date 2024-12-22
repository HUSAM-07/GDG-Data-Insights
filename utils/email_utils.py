def get_email_list(df, column_name='Email IDs'):
    """Extract and format email addresses from dataframe"""
    emails = df[column_name].dropna().tolist()
    return '; '.join(emails) 