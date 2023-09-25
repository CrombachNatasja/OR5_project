import pandas as pd
import numpy as np
import streamlit as st
import random

def main():
    print("---------")
    st.set_page_config(layout="wide")
    st.title('Homepage')
    createUploaders()

def createUploaders():
    filecorrect = False
    planningcorrect = False

    col1, col2 = st.columns(2)

    uploaded_file = col1.file_uploader('Please upload the input data', type='xlsx', accept_multiple_files=False)
    if uploaded_file is not None:
        filecorrect, df_bewoners, df_adressen, df_paar, df_buren, df_kookte, df_tafelgenoot = checkInput(uploaded_file)
    
    uploaded_file = col2.file_uploader('Please upload the planning', type='xlsx', accept_multiple_files=False)
    if uploaded_file is not None:
        planningcorrect, df_planning = checkPlanning(uploaded_file)

    if filecorrect and planningcorrect:
        improvePlanning(df_bewoners, df_adressen, df_paar, df_buren, df_kookte, df_tafelgenoot, df_planning)

def checkInput(uploaded_file):
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
    data = pd.read_excel(uploaded_file)
    # hier moet nog een inputcheck in 

def improvePlanning(df_bewoners, df_adressen, df_paar, df_buren, df_kookte, df_tafelgenoot, df_planning):
    for index, row in df_planning.iterrows():
        results = df_planning.loc[df_planning["Voor"] == row["Voor"]]
        


    """
    Eisen aan de planning van het Running Dinner
    De planning van het Running Dinner moet aan de volgende voorwaarden voldoen:
        • Elke deelnemer eet elk gerecht en eet elk gerecht op een ander huisadres.
        • Ieder huishouden dat niet vrijgesteld is van koken, bereidt één van de drie gerechten. Sommige
        deelnemers hoeven niet te koken en ontvangen op hun huisadres dus voor geen enkele gerecht gasten.
        • Wanneer een deelnemer een bepaalde gang moet koken is deze deelnemer voor die gang
        ingedeeld op diens eigen adres.
        • Het aantal tafelgenoten dat op een bepaald huisadres eet, voldoet aan de bij het adres horende
        minimum en maximum groepsgrootte.
        • Een heel klein aantal groepjes van deelnemers, vaak één of twee duos, zit tijdens het gehele Running
        Dinner voor elke gang bij elkaar aan tafel.

    Wensen aan planning Running Dinner
    In volgorde van afnemend belang moet zo goed mogelijk rekening worden gehouden met de volgende wensen:
        1. Twee verschillende deelnemers zijn zo weinig mogelijk keer elkaars tafelgenoten; het liefst
        maximaal één keer. Dit geldt zeker voor deelnemers uit hetzelfde huishouden.
        2. Een huishouden dat in 2022 een hoofdgerecht bereid heeft, bereidt tijdens de komende Running
        Dinner geen hoofdgerecht.
        3. Indien mogelijk wordt er rekening gehouden met een door de gastheer of vrouw opgegeven voorkeursgang.
        4. Twee deelnemers die in 2022 bij elkaar aan tafel zaten, zijn in 2023 liefst niet elkaars tafelgenoot.
        5. Twee tafelgenoten zijn bij voorkeur niet elkaars directe buren.
        6. Twee deelnemers die in 2021 bij elkaar aan tafel zaten, zijn in 2023 liefst niet elkaars tafelgenoot.
    """

main()