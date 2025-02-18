import streamlit as st
import pandas as pd
from io import BytesIO

def load_csv(file):
    df = pd.read_csv(file, encoding='ISO-8859-1', header=None)
    df = df.iloc[2:].reset_index(drop=True)
    df.columns = df.iloc[0]
    df = df[1:].reset_index(drop=True)
    df['full_name'] = df['First Name'] + ' ' + df['Last Name']
    return df

def load_excel(file):
    df = pd.read_excel(file)
    df['full_name'] = df['First Name'] + ' ' + df['Last Name']
    return df

def compare_files(df1, df2):
    missing_names = df1[~df1['full_name'].isin(df2['full_name'])].reset_index()
    missing_names = missing_names.rename(columns={'index': 'row_number'})
    return missing_names

def to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Missing Names')
    output.seek(0)
    return output

def main():
    st.title("File Comparison Tool")
    
    st.write("Upload the old file (CSV) and the new file (Excel) to find missing names.")
    
    old_file = st.file_uploader("Upload old CSV file", type=['csv'])
    new_file = st.file_uploader("Upload new Excel file", type=['xlsx'])
    
    if old_file and new_file:
        df_old = load_csv(old_file)
        df_new = load_excel(new_file)
        
        missing_names = compare_files(df_new, df_old)
        
        if missing_names.empty:
            st.success("No missing names found!")
        else:
            st.write("Missing Names:")
            st.dataframe(missing_names)
            
            excel_data = to_excel(missing_names)
            st.download_button(label="Download Missing Names", 
                               data=excel_data, 
                               file_name="missing_names.xlsx", 
                               mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

if __name__ == "__main__":
    main()
