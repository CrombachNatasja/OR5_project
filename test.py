import pandas as pd
import numpy as np
import streamlit as st

#check dat iedereen ingedeeld is -> MOET
def is_everyone_plannend(data):
    return not(data['Voor'].isnull().values.any())

#check of dat huisadres max niet overschreidt bij wisselingen -> MOET

def read_planning():
    data = pd.read_excel("Running Dinner eerste oplossing 2022.xlsx")
    data_save = data
    if is_everyone_plannend(data_save):
        print("True")
    #score = int op basis van de checks

    #uit het dataframe de mensen die het voorrecht koken eruit filteren, zo voorkom je dat die mee gaan wisselen

    #for index1, row1 in data.iterrows():
        #for index2, row2 in data.iterrows():
            #als een van de paren wisselt, moet de ander ook wisselen. Iets van een koppeling tussen de twee hebben
            #value_row1 = data.at[row1, "Voor"]
            #value_row2 = data.at[row2, "Voor"]

            #new_score = int of basis van dezelfde checks
            #if new_score < score als wisselen van values beter is, wissel ze
            #score = new_score
            #data.at[row1, "Voor"] = value_row2
            #data.at[row2, "Voor"] = value_row1
            #else, niks doen want niet wisselen is beter

read_planning()

#check of de duo's bij elkaar blijven -> MOET

#Eis 1, belangrijkst 6x
#deelnemer 1 en 2 maximaal 1 keer samen zit aan een tafel. Tellen hoevaak dit NIET het geval is -> int -> gewenst zo laag mogelijk

#Eis 4, 3x
#deelnemers die in 2022 bij elkaar zaten liever niet ook in 2023 bij elkaar -> gewenst -> int hoevaak

#Eis 5, 1x
#deelnemers die in 2021 bij elkaar zaten liever niet ook in 2023 bij elkaar -> gewenst -> int hoevaak