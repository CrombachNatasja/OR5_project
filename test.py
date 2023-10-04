import pandas as pd

data = pd.read_excel("Running Dinner eerste oplossing 2022.xlsx")

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
    data_voor_kokers = data[data['kookt'] == "Voor"]
    unique_huisadres_values = data_voor_kokers['Huisadres'].unique()

    for huisadres in unique_huisadres_values:
        data_voor = data_voor_kokers['Voor'].value_counts()[huisadres]
        if not (data_voor_kokers['aantal'] >= data_voor).all():
            return False
    
    return True

#check of dat de paren bij elkaar blijven -> MOET
def duo_check(data):
    """
    Checks if the duos that need to stay together are placed together.
    :input: The dataframe with the current planning.
    :output: A boolean.
    """
    pairs = True
    df_paar = pd.read_excel("Running Dinner dataset 2022.xlsx", sheet_name="Paar blijft bij elkaar", skiprows=1)

    # Create a set to keep track of pairs that were already checked
    checked_pairs = set()

    for index, rows in df_paar.iterrows():
        bewoner1 = rows["Bewoner1"]
        bewoner2 = rows["Bewoner2"]

        # Check if this pair has already been checked to avoid double-checking
        pair_key = frozenset([bewoner1, bewoner2])
        if pair_key in checked_pairs:
            continue

        # Search for the indices of bewoner1 and bewoner2
        bewoner1_indices = data.index[data['Bewoner'] == bewoner1].tolist()
        bewoner2_indices = data.index[data['Bewoner'] == bewoner2].tolist()

        # Check if both bewoner1 and bewoner2 exist in the dataset
        if bewoner1_indices and bewoner2_indices:
            for bewoner1_index in bewoner1_indices:
                for bewoner2_index in bewoner2_indices:
                    # Check if the indices are within bounds
                    if bewoner1_index < len(data) and bewoner2_index < len(data):
                        # Check if the pairs have matching attributes (Voor, Hoofd, Na)
                        if not (
                            data.iloc[bewoner1_index]["Voor"] == data.iloc[bewoner2_index]["Voor"]
                            and data.iloc[bewoner1_index]["Hoofd"] == data.iloc[bewoner2_index]["Hoofd"]
                            and data.iloc[bewoner1_index]["Na"] == data.iloc[bewoner2_index]["Na"]
                        ):
                            pairs = False
                            break
            # Mark this pair as checked to avoid double-checking
            checked_pairs.add(pair_key)
        else:
            # If either bewoner1 or bewoner2 was not found, consider it a violation
            pairs = False

    return pairs

#Eis 1, belangrijkst 6x
#deelnemer 1 en 2 maximaal 1 keer samen zit aan een tafel. Tellen hoevaak dit NIET het geval is -> int -> gewenst zo laag mogelijk
def more_than_once_together(data):
    """
    Counts how many times two people are eating their meal together, gives a higher score when it is more than once.
    :input: The dataframe with the current planning.
    :output: int.
    """
    score = 0
    data_course = pd.DataFrame()

    # Concatenate the Voor, Hoofd, and Na columns into a single combination column
    data_course['CourseCombination'] = data['Voor'] + '-' + data['Hoofd'] + '-' + data['Na']

    # Group by the CourseCombination and count occurrences
    counts = data_course['CourseCombination'].value_counts()

    # Filter to include only combinations where count is greater than one
    score = counts[counts > 1]

    return score.sum()

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
        return 99999999999
    
def get_bewoner_pairs(data):
    df_paar = pd.read_excel("Running Dinner dataset 2022.xlsx", sheet_name="Paar blijft bij elkaar", skiprows=1)
    bewoner_lijst = {}
    for index, rows in df_paar.iterrows():
        bewoner1 = rows["Bewoner1"]
        bewoner2 = rows["Bewoner2"]
        
        bewoner1_index = data.index[data['Bewoner'] == bewoner1].tolist()[0]
        bewoner2_index = data.index[data['Bewoner'] == bewoner2].tolist()[0]

        bewoner_lijst[bewoner1_index] = bewoner2_index
    
    return bewoner_lijst

def get_key(val, my_dict):
   
    for key, value in my_dict.items():
        if val == value:
            return key
 
    return "key doesn't exist"

def get_index_same_adres(index, data, bewoner_lijst):
    """
    Find another index with the same address as the given index for the first course ('Voor')
    and ensure it does not match any data in the bewoner_lijst.
    :param index: The index for which you want to find a matching index.
    :param data: The dataframe with the current planning.
    :param bewoner_lijst: A dictionary mapping one participant to another.
    :return: The matching index or 0 if not found.
    """
    # Get the participant's address and table assignment for the first course ('Voor')
    address = data.at[index, 'Voor']

    # Filter the data to find potential matching participants with the same address
    potential_matches = data[(data['Voor'] == address) & (index not in bewoner_lijst.keys())]

    # Check if there are potential matches other than the given index
    if len(potential_matches) > 1:
        # Remove the given index from potential matches if present
        potential_matches = potential_matches[potential_matches.index != index]

        # Return the index of the first matching participant
        return potential_matches.index[0]

    # If no matching index is found, return 0
    return 9999

def read_planning():
    data = pd.read_excel("Running Dinner eerste oplossing 2022.xlsx")
    data = data.drop(data.columns[0], axis=1)
    score = calculate_planning(data)
    
    # Create a new dataframe for participants with "Kookt" == "Voor"
    participants_voor = data[data['kookt'] == "Voor"]

    # Filter participants with "Kookt" != "Voor" from the main dataframe
    data_save = data[data['kookt'] != "Voor"]
    data_save = data_save.reset_index(drop=True)
    bewoner_lijst = get_bewoner_pairs(data_save)

    print("Start switching...")
    #uit het dataframe de mensen die het voorrecht koken eruit filteren, zo voorkom je dat die mee gaan wisselen

    for index1, row1 in data_save.iterrows():
        if index1 not in bewoner_lijst:
            old_adress = row1["Voor"]
            for index2, row2 in data_save.iloc[(index1+1):].iterrows():
                #als een van de paren wisselt, moet de ander ook wisselen. Iets van een koppeling tussen de twee hebben
                #if row1["Bewoner"] == onderdeel van paar -> ruil row1 en parner voor row2 en iemand met zelfde huisnummer
                new_adress = row2["Voor"]
                
                if index1 in bewoner_lijst.values():
                    key = get_key(index1, bewoner_lijst)
                    #get random index waar voor = voor van row2. Hierbij mag index3 niet gelijk zijn aan een van de paren of iemand die voor kookt
                    index3 = get_index_same_adres(index2, data_save, bewoner_lijst)
                    if index3 != 9999:
                        data_save.loc[index1, "Voor"] = new_adress #pair bewoner1
                        data_save.loc[key, "Voor"] = new_adress #pair bewoner1
                        data_save.loc[index2, "Voor"] = old_adress #Index2 bewoner die loopt
                        data_save.loc[index3, "Voor"] = old_adress #Index van bewoner met hetzelfde adres als bewoner erboven
                else:
                    data_save.loc[index1, "Voor"] = new_adress
                    data_save.loc[index2, "Voor"] = old_adress

                final_data = pd.concat([data_save, participants_voor], ignore_index=True)
                new_score = calculate_planning(final_data)
                if new_score >= score:
                    if index1 in bewoner_lijst.values():
                        if index3 != 9999:
                            data_save.loc[index1, "Voor"] = old_adress #Bewoner1
                            data_save.loc[key, "Voor"] = old_adress #Bewoner2
                            data_save.loc[index2, "Voor"] = new_adress #Index2 bewoner
                            data_save.loc[index3, "Voor"] = new_adress 
                    else:
                        data_save.loc[index1, "Voor"] = old_adress
                        data_save.loc[index2, "Voor"] = new_adress
                else:
                    print("Better score found:", new_score)
                    old_adress = new_adress
                    score = new_score
    
    final_data = pd.concat([data_save, participants_voor], ignore_index=True)
    final_data.to_excel("new_planning.xlsx")
    print("Finished")

read_planning()

#Eis 4, 3x
#deelnemers die in 2022 bij elkaar zaten liever niet ook in 2023 bij elkaar -> gewenst -> int hoevaak

#Eis 5, 1x
#deelnemers die in 2021 bij elkaar zaten liever niet ook in 2023 bij elkaar -> gewenst -> int hoevaak
def check_2021(data):
    """
    Checks the amount of people that are grouped with the same people as the year before.
    :input: The dataframe with the current planning.
    :output: A score.
    """
    last_year = pd.read_excel("Running Dinner eerste oplossing 2021.xlsx")
    score = 0
    for index1, row1 in data.iterrows():
        for index2, row2 in last_year.iloc[(index1+1):].iterrows():
            count = 0
            for index, rows in last_year.iterrows():
            bewoner1 = rows["Bewoner1"]
        
            bewoner1_index = data.index[data['Bewoner'] == bewoner1].tolist()[0]
            if
                data.iloc[bewoner1_index]['Bewoner'] == data.iloc[bewoner2_index]['Voor'] :
                count += 1
            if 
                count += 1
            if 
                count += 1
        
            if count > 1:
                score += 1

    return score 

check_2021(data)