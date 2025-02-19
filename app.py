# Importing Required modules/libs
import streamlit as st
import pandas as pd 
import os
from  io import BytesIO

# Setting up the app
st.set_page_config(page_title = "Data Sweeper By Arman", layout = "wide")
st.title("Data Sweeper")
st.write("Tranform your files between CSV and Excel formats with built in data cleaning and visualisation!")

uploaded_files = st.file_uploader("Upload your files (CSV or Excel):",type = ["csv","xlsv"], accept_multiple_files = True)

if uploaded_files : 
    for file in uploaded_files :
        file_ext = os.path.splitext(file.name)[-1].lower()

        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsv":
            df = pd.read_excel(file)
        else :
            st.error("Unsupported file type: {file_ext}")
            continue

        # displaying info about the file
        st.write(f"**File Name:**{file.name}")
        st.write(f"**File Size:**{(file.size)/1024}")

        # Showing 5 row of our data frame
        st.write("Preview the Head Of the DataFrame")
        st.dataframe(df.head())

        # Options For DATA Cleaning
        st.subheader("Data Cleaning Otions")
        if st.checkbox(f"Clean data for {file.name}"):
            col1 , col2 = st.columns(2)

            with col1 :
                if st.button(f"Remove Duplicates from {file.name}"): 
                    df.drop_duplicates(inplace = True)
                    st.write("Duplicates Removed!")


            with col2 : 
                if st.button(f"Fill Missing Values For {file.name}"):
                    numeric_cols = df.select_dtypes(include=["number"]).columns 
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write("Missing Values Have BEen Filled!")

        # choosing Specific columns to or convert
        st.subheader("select Columns to Convert")
        columns = st.multiselect(f"Choose Colums for  {file.name}" , df.columns,default = df.columns) 
        df = df[columns]

        # CReating soem Visulatizations
        st.subheader("Data Visualization")
        if st.checkbox(f"show visualization for {file.name}"):
            st.bar_chart(df.select_dtypes(include = "number").iloc[:,:2])

        # Converting the file -> CSV To Excel
        st.subheader("Conversion Options")
        conversion_type = st.radio(f"Convert {file.name} to:",["CSV","Excel"], key = file.name)
        if st.button(f"Convert {file.name}"):
            buffer = BytesIO()
            if conversion_type == "CSV":
                df.to_csv(buffer,index = False)
                file_name = file.name.replace(file_ext,"csv")
                mime_type = "text/csv"

            elif conversion_type == "Excel":
                df.to_excel(buffer,index = False)
                file_name = file.name.replace(file_ext,"xlsx")
                mime_type = "appliaction/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            buffer.seek(0)


            # Download Buttons
            st.download_button(
                label = f"Download {file.name} as {conversion_type}",
                data = buffer,
                file_name = file_name,
                mime =mime_type
            )
st.success("All Files Processed ")