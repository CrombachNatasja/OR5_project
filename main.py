import pandas as pd
import numpy as np
import streamlit as st
import runningdinner as rd

def main():
    print("---------")
    st.set_page_config(layout="wide")
    st.title('Homepage')
    createUploaders()

def createUploaders():
    """
    Creates an interface with two columns where users can put in the needed documents.
    """
    filecorrect = False
    planningcorrect2021 = False
    planningcorrect2022 = False
    planningcorrect2023 = False
    finished = False

    col1, col2 = st.columns(2)

    uploaded_file = col1.file_uploader('Please upload the input data', type='xlsx', accept_multiple_files=False)
    if uploaded_file is not None:
        filecorrect, df_bewoners, df_adressen, df_paar, df_buren, df_kookte, df_tafelgenoot = checkInput(uploaded_file, col1)

    uploaded_file = col1.file_uploader('Please upload the planning of 2022', type='xlsx', accept_multiple_files=False)
    if uploaded_file is not None:
        planningcorrect2022, data2022 = checkPlanning(uploaded_file, col1)
    
    uploaded_file = col2.file_uploader('Please upload the planning of 2023', type='xlsx', accept_multiple_files=False)
    if uploaded_file is not None:
        planningcorrect2023, data2023 = checkPlanning(uploaded_file, col2)

    uploaded_file = col2.file_uploader('Please upload the planning of 2021', type='xlsx', accept_multiple_files=False)
    if uploaded_file is not None:
        planningcorrect2021, data2021 = checkPlanning(uploaded_file, col2)
    
    st.write('Voor welke gang wil je een verbetering doen?')
    voor = st.checkbox('Voorgerecht')
    hoofd = st.checkbox('Hoofdgerecht')
    na = st.checkbox('Nagerecht')

    if filecorrect and planningcorrect2021 and planningcorrect2022 and planningcorrect2023:
        if st.button("Start"):
            if voor:
                data2023 = rd.improve_planning('Voor',data2023, data2021, data2022, df_paar)
                st.success("Klaar met voorgerecht")
            if hoofd:
                data2023 = rd.improve_planning('Hoofd',data2023, data2021, data2022, df_paar)
                st.success("Klaar met hoofdgerecht")
            if na:
                data2023 = rd.improve_planning('Na',data2023, data2021, data2022, df_paar)
                st.success("Klaar met nagerecht")

def checkInput(uploaded_file, col):
    """
    Checks if all the necessary sheets are present in the dataframe.
    :output: The columns and a boolean
    """
    data = pd.read_excel(uploaded_file, sheet_name=None)
    allowed_sheets = ["Bewoners","Adressen","Paar blijft bij elkaar","Buren","Kookte vorig jaar","Tafelgenoot vorig jaar"]
    if all([i in allowed_sheets for i in data.keys()]):
        df_bewoners = pd.read_excel(uploaded_file, sheet_name="Bewoners")
        df_adressen = pd.read_excel(uploaded_file, sheet_name="Adressen")
        df_paar = pd.read_excel(uploaded_file, sheet_name="Paar blijft bij elkaar", skiprows=1)
        df_buren = pd.read_excel(uploaded_file, sheet_name="Buren", skiprows=1)
        df_kookte = pd.read_excel(uploaded_file, sheet_name="Kookte vorig jaar", skiprows=1)
        df_tafelgenoot = pd.read_excel(uploaded_file, sheet_name="Tafelgenoot vorig jaar", skiprows=1)
        print(df_bewoners.head())
        col.success("File is succesfully uploaded")
        return True, df_bewoners, df_adressen, df_paar, df_buren, df_kookte, df_tafelgenoot
    else:
        col.error("Missing sheets")
        return False, pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame()
    
def checkPlanning(uploaded_file, col):
    """
    Checks if the planning follows the format given
    :output: The planning and if it correct
    """
    data = pd.read_excel(uploaded_file)
    data = data.drop(data.columns[0], axis=1)
    # hier moet nog een inputcheck in 
    col.success("Good job")
    return True, data

main()