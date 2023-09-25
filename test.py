import pandas as pd

#check dat iedereen ingedeeld is -> MOET
def is_everyone_plannend(data):
    """
    Checks if everyone is in the planning to eat every meal.
    :input: The dataframe with the current planning.
    :output: A boolean.
    """
    return not(data['Voor'].isnull().values.any())

#check of dat huisadres max niet overschreidt bij wisselingen -> MOET
def max_people_not_exceeded(data):
    """
    Checks if the maximum people per adres per meal is not exceeded.
    :input: The dataframe with the current planning.
    :output: A boolean.
    """
    data_voor_kokers = data.loc[data['kookt'] == "Voor"]
    for index, row in data_voor_kokers.iterrows():
        data_voor = data['Voor'].value_counts()[row['Huisadres']]
        if not(row['aantal'] >= data_voor):
            return False
    return True

def duo_check(data):
    """
    Checks if the duos that need to stay together are placed together.
    :input: The dataframe with the current planning.
    :output: A boolean.
    """
    df_paar = pd.read_excel("Running Dinner dataset 2022.xlsx", sheet_name="Paar blijft bij elkaar", skiprows=1)
    for index, rows in df_paar.iterrows():
        bewoner1 = rows["Bewoner1"]
        bewoner2 = rows["Bewoner2"]
        
        bewoner1_index = data.index[data['Bewoner'] == bewoner1].tolist()[0]
        bewoner2_index = data.index[data['Bewoner'] == bewoner2].tolist()[0]

        if not(data.iloc[bewoner1_index]['Voor'] == data.iloc[bewoner2_index]['Voor'] and data.iloc[bewoner1_index]['Hoofd'] == data.iloc[bewoner2_index]['Hoofd'] and data.iloc[bewoner1_index]['Na'] == data.iloc[bewoner2_index]['Na']):
            return False
    
    return True

#Eis 1, belangrijkst 6x
#deelnemer 1 en 2 maximaal 1 keer samen zit aan een tafel. Tellen hoevaak dit NIET het geval is -> int -> gewenst zo laag mogelijk
def more_than_once_together(data):
    """
    Counts how many times two people are eating their meal together, gives a higher score when it is more than once.
    :input: The dataframe with the current planning.
    :output: int.
    """
    score = 0
    for index1, row1 in data.iterrows():
        for index2, row2 in data.iloc[(index1+1):].iterrows():
            count = 0
            if row1["Voor"] == row2["Voor"]:
                count += 1
            if row1["Hoofd"] == row2["Hoofd"]:
                count += 1
            if row1["Na"] == row2["Na"]:
                count += 1
        
            if count > 1:
                score += 1

    return score

#Alle checks uitvoeren en score terug geven
def calculate_planning(data):
    """
    Checks if the planning is possible with the given constraints.
    If it is possible, it gives the planning score (the less, the better).
    :input: The dataframe with the current planning.
    :output: int.
    """
    everyone_planned = is_everyone_plannend(data)
    max_people = max_people_not_exceeded(data)
    duos = duo_check(data)

    if everyone_planned and max_people and duos:
        score = more_than_once_together(data)*6
        return score
    else:
        return None

def read_planning():
    data = pd.read_excel("Running Dinner eerste oplossing 2022.xlsx")
    df_paar = pd.read_excel("Running Dinner dataset 2022.xlsx", sheet_name="Paar blijft bij elkaar", skiprows=1)
    data_save = data
    """
    score = calculate_planning(data_save)
    #uit het dataframe de mensen die het voorrecht koken eruit filteren, zo voorkom je dat die mee gaan wisselen

    for index1, row1 in data_save.iterrows():
        for index2, row2 in data_save.iloc[(index1+1):].iterrows():
            #als een van de paren wisselt, moet de ander ook wisselen. Iets van een koppeling tussen de twee hebben
            #if row1["Bewoner"] == onderdeel van paar -> ruil row1 en parner voor row2 en iemand met zelfde huisnummer
            if row1["Bewoner"] in df_paar:
                print(row1["Bewoner"])

            data_save.at[index1, "Voor"] = row2["Voor"]
            data_save.at[index2, "Voor"] = row1["Voor"]

            new_score = calculate_planning(data_save)

            if new_score is None or new_score >= score:
                data_save.at[index1, "Voor"] = row1["Voor"]
                data_save.at[index2, "Voor"] = row2["Voor"]
            else:
                score = new_score
        """
    data_save.to_excel("new_planning.xlsx")

read_planning()

#Eis 4, 3x
#deelnemers die in 2022 bij elkaar zaten liever niet ook in 2023 bij elkaar -> gewenst -> int hoevaak

#Eis 5, 1x
#deelnemers die in 2021 bij elkaar zaten liever niet ook in 2023 bij elkaar -> gewenst -> int hoevaak