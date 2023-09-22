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
        createPlanning(df2022_bewoners, df2022_adressen, df2022_paar, df2022_buren, df2022_kookte, df2022_tafelgenoot)

def checkinput(uploaded_file):
    data = pd.read_excel(uploaded_file, sheet_name=None)
    allowed_sheets = ["Bewoners","Adressen","Paar blijft bij elkaar","Buren","Kookte vorig jaar","Tafelgenoot vorig jaar"]
    if all([i in allowed_sheets for i in data.keys()]):
        df2022_bewoners = pd.read_excel(uploaded_file, sheet_name="Bewoners")
        df2022_adressen = pd.read_excel(uploaded_file, sheet_name="Adressen")
        df2022_paar = pd.read_excel(uploaded_file, sheet_name="Paar blijft bij elkaar", skiprows=1)
        df2022_paar = pd.read_excel(uploaded_file, sheet_name="Paar blijft bij elkaar", skiprows=1)  
        df2022_buren = pd.read_excel(uploaded_file, sheet_name="Buren", skiprows=1)
        df2022_kookte = pd.read_excel(uploaded_file, sheet_name="Kookte vorig jaar", skiprows=1)
        df2022_tafelgenoot = pd.read_excel(uploaded_file, sheet_name="Tafelgenoot vorig jaar", skiprows=1)
        return True, df2022_bewoners, df2022_adressen, df2022_paar, df2022_buren, df2022_kookte, df2022_tafelgenoot
    else:
        st.error("Missing sheets")
        return False, pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame()
    
def createPlanning(df2022_bewoners, df2022_adressen, df2022_paar, df2022_buren, df2022_kookte, df2022_tafelgenoot):
    st.write("planning is generating")

main()