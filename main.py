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
    planningcorrect = False

    col1, col2 = st.columns(2)

    uploaded_file = col1.file_uploader('Please upload the input data', type='xlsx', accept_multiple_files=False)
    if uploaded_file is not None:
        filecorrect, df_bewoners, df_adressen, df_paar, df_buren, df_kookte, df_tafelgenoot = checkInput(uploaded_file)

    uploaded_file = col1.file_uploader('Please upload the planning of 2022', type='xlsx', accept_multiple_files=False)
    if uploaded_file is not None:
        planningcorrect2022, data2022 = checkPlanning(uploaded_file)
    
    uploaded_file = col2.file_uploader('Please upload the planning of 2023', type='xlsx', accept_multiple_files=False)
    if uploaded_file is not None:
        planningcorrect2023, data2023 = checkPlanning(uploaded_file)

    uploaded_file = col2.file_uploader('Please upload the planning of 2021', type='xlsx', accept_multiple_files=False)
    if uploaded_file is not None:
        planningcorrect2021, data2021 = checkPlanning(uploaded_file)

    if filecorrect and planningcorrect2021 and planningcorrect2022 and planningcorrect2023:
        rd.improvePlanning(data2023, data2021, data2022, df_paar)
        

def checkInput(uploaded_file):
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
        return True, df_bewoners, df_adressen, df_paar, df_buren, df_kookte, df_tafelgenoot
    else:
        st.error("Missing sheets")
        return False, pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame()
    
def checkPlanning(uploaded_file):
    """
    data = pd.read_excel("Running Dinner eerste oplossing 2022.xlsx")
    data2021 = pd.read_excel("Running Dinner eerste oplossing 2021.xlsx")
    data2022 = pd.read_excel("Running Dinner eerste oplossing 2022.xlsx")
    df_paar = pd.read_excel("Running Dinner dataset 2022.xlsx", sheet_name="Paar blijft bij elkaar", skiprows=1)
    """
    data = pd.read_excel(uploaded_file)
    # hier moet nog een inputcheck in 

main()