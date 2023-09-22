import pandas as pd
import streamlit as st

def main():
    st.set_page_config(layout="wide")
    st.title('Homepage')
    createUploaders()

def createUploaders():
    filecorrect = False
    uploaded_file = st.file_uploader('Please upload the input data from last year', type='xlsx', accept_multiple_files=False)
    if uploaded_file is not None:
        filecorrect, df2022_bewoners, df2022_adressen, df2022_paar, df2022_buren, df2022_kookte, df2022_tafelgenoot = checkinput(uploaded_file)
    
    if filecorrect:
        st.write("goodjob")
        createPlanning(df2022_bewoners, df2022_adressen, df2022_paar, df2022_buren, df2022_kookte, df2022_tafelgenoot)

def checkinput(uploaded_file):
    data = pd.ExcelFile(uploaded_file)
    wrong_sheets = 0
    if "Bewoners" in data.sheet_names:
        df2022_bewoners = pd.read_excel(uploaded_file, sheet_name="Bewoners")
    else:
        st.error("Sheet 'Bewoners' does not exist in the uploaded file")
        wrong_sheets = wrong_sheets + 1
    if "Adressen" in data.sheet_names:    
        df2022_adressen = pd.read_excel(uploaded_file, sheet_name="Adressen")
    else:
        st.error("Sheet 'Adressen' does not exist in the uploaded file")
        wrong_sheets = wrong_sheets + 1
    if "Paar blijft bij elkaar" in data.sheet_names:    
        df2022_paar = pd.read_excel(uploaded_file, sheet_name="Paar blijft bij elkaar", skiprows=1)
    else:
        st.error("Sheet 'Paar blijft bij elkaar' does not exist in the uploaded file")
        wrong_sheets = wrong_sheets + 1
    if "Buren" in data.sheet_names:    
        df2022_buren = pd.read_excel(uploaded_file, sheet_name="Buren", skiprows=1)
    else:
        st.error("Sheet 'Buren' does not exist in the uploaded file")
        wrong_sheets = wrong_sheets + 1
    if "Kookte vorig jaar" in data.sheet_names:    
        df2022_kookte = pd.read_excel(uploaded_file, sheet_name="Kookte vorig jaar", skiprows=1)
    else:
        st.error("Sheet 'Kookte vorig jaar' does not exist in the uploaded file")
        wrong_sheets = wrong_sheets + 1
    if "Tafelgenoot vorig jaar" in data.sheet_names:    
        df2022_tafelgenoot = pd.read_excel(uploaded_file, sheet_name="Tafelgenoot vorig jaar", skiprows=1)
    else:
        st.error("Sheet 'Tafelgenoot vorig jaar' does not exist in the uploaded file")
        wrong_sheets = wrong_sheets + 1

    if wrong_sheets == 0:
        return True, df2022_bewoners, df2022_adressen, df2022_paar, df2022_buren, df2022_kookte, df2022_tafelgenoot
    else:
        return False, pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame()
    
def createPlanning(df2022_bewoners, df2022_adressen, df2022_paar, df2022_buren, df2022_kookte, df2022_tafelgenoot):
    st.write("planning is generating")

main()