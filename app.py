import streamlit as st   
import pandas as pd    
import os
from io import BytesIO

st.set_page_config(page_title="Data Sweeper", layout='wide') 

# Custom CSS
st.markdown(
    """
    <style>
    .stApp{
        background-color:black;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title and Description
st.title("💿 Data Sweeper Sterling Integrator By Manjula Chohan")
st.write("Transform your files between CSV and Excel formats with built-in data cleaning for the project in quarter 3!")

# File uploader
uploaded_files = st.file_uploader("Upload your file (accepts CSV or Excel):", type=["csv", "xlsx"], accept_multiple_files=True)

if uploaded_files:
    for index, file in enumerate(uploaded_files):
        file_ext = os.path.splitext(file.name)[-1].lower()
        safe_name = "".join(c if c.isalnum() else "_" for c in file.name)  # Sanitize filename

        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"Unsupported file type: {file_ext}")
            continue

        # File details
        st.write("🔍 Preview the head of the DataFrame")
        st.dataframe(df.head())

        # Data Cleaning Options
        st.subheader("🛠 Data Cleaning Options")
        if st.checkbox(f"Clean data for {file.name}", key=f"clean_{safe_name}_{index}"):
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button(f"Remove duplicates from {file.name}", key=f"dedup_{safe_name}_{index}"):
                    df.drop_duplicates(inplace=True)
                    st.write("✅ Duplicates removed!")
            
            with col2:
                if st.button(f"Fill missing values for {file.name}", key=f"fillna_{safe_name}_{index}"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write("✅ Missing values have been filled!")

        st.subheader("🎯 Select Columns to Keep")
        columns = st.multiselect(f"Choose columns for {file.name}", df.columns, default=df.columns, key=f"columns_{safe_name}_{index}")
        df = df[columns]  
        
        # Data Visualization
        st.subheader("📊 Data Visualization")
        if st.checkbox(f"Show visualization for {file.name}", key=f"viz_{safe_name}_{index}"):
            st.bar_chart(df.select_dtypes(include='number').iloc[:, :2])

        # Conversion Options
        st.subheader("🔄 Conversion Options")
        conversion_type = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key=f"convert_{safe_name}_{index}")
        
        if st.button(f"Convert {file.name}", key=f"convert_btn_{safe_name}_{index}"):
            buffer = BytesIO()
            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
                file_name = safe_name + ".csv"
                mime_type = "text/csv"
            else:
                df.to_excel(buffer, index=False, engine="openpyxl")
                file_name = safe_name + ".xlsx"
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            
            buffer.seek(0)

            st.download_button(
                label=f"Download {file_name} as {conversion_type}",
                data=buffer,
                file_name=file_name,
                mime=mime_type
            )

st.success("🎉 All files processed successfully!")