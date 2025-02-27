import streamlit as st #for web app
import pandas as pd
import os 
from io import BytesIO #for file upload

# Set up our app:
st.set_page_config(page_title="Q3 Assignment 01", layout="wide")

# 🌱 Growth Mindset Introduction
st.title("🚀 Growth Mindset Challenge")

st.write("""
## 🌱 What is a Growth Mindset?  
A *growth mindset* is the belief that intelligence, talents, and abilities *can be developed* through dedication, learning, and persistence.  
People with a growth mindset *embrace challenges, learn from failures, and continuously improve* their skills.  

On the other hand, a *fixed mindset* makes people believe that intelligence and talent are *static* – meaning, they can’t be changed.  

### 🔥 Why is a Growth Mindset Important?  
Having a growth mindset can transform your life. It helps you:  
✅ *Embrace challenges* instead of avoiding them  
✅ *Learn from criticism* rather than feeling discouraged  
✅ *Keep going despite failures* instead of giving up  
✅ *See effort as the key to success*  
✅ *Develop resilience* and overcome difficulties  

""")

st.title("Data Sweeper")
st.write("Transform your files between CSV and Excel formats with built-in data cleaning and visualization!")


uploaded_files = st.file_uploader("Upload your files (CSV or Excel):", type=["csv", "xlsx"], accept_multiple_files=True)

if uploaded_files:
    for uploaded_file in uploaded_files:
        file_ext = os.path.splitext(uploaded_file.name)[-1].lower()

        if file_ext == ".csv":
            df = pd.read_csv(uploaded_file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(uploaded_file)
        else:
            st.error("Unsupported file format. Please upload a CSV or Excel file.")    
            continue

        # Display info about the file:
        st.write(f"File name: {uploaded_file.name}")
        st.write(f"File size: {uploaded_file.size/1024} bytes")

        # Display the first 5 rows of the DataFrame:
        st.write("Preview of the first 5 rows:")
        st.dataframe(df.head())

        # Options for data cleaning
        st.subheader("Data Cleaning Options")
        if st.checkbox(f"Clean data for {uploaded_file.name}"):
            col1 , col2 = st.columns(2)
            with col1: 
                if st.button(f"Remove duplicates from {uploaded_file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.write("Duplicates Removed!")
            with col2:        
                if st.button(f"Fill missing values from {uploaded_file.name}"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write("Missing values filled!")

        # chose specific columns to keep or convert 
        st.subheader("Select columns to keep or convert") 
        columns = st.multiselect(f"Chose columns for {uploaded_file.name}", df.columns , default=df.columns)
        df = df[columns]          

        # create some visualization:
        st.subheader("📊Data Visualization")
        if st.checkbox(f"Show Visualization for {uploaded_file.name}"):
            st.bar_chart(df.select_dtypes(include='number').iloc[:, :2])

        # convert the file --> CSV To Excel:
        st.subheader("🔄Conversion Options")
        conversion_type = st.radio(f"Convert {uploaded_file.name} to", ("CSV", "Excel"))
        if st.button(f"Convert {uploaded_file.name} to {conversion_type}"):    
            buffer = BytesIO()
            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
                uploaded_file.name = uploaded_file.name.replace(file_ext, ".csv")
                mime_type = "text/csv"

            elif conversion_type == "Excel":
                df.to_excel(buffer, index=False)    
                uploaded_file.name = uploaded_file.name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

            buffer.seek(0)

            # Download the converted file:
            st.download_button(
                label=f"Download {uploaded_file.name} as {conversion_type}",
                data=buffer,
                file_name = uploaded_file.name,
                mime=mime_type
            )    

st.success("All files processed")