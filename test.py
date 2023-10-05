import pandas as pd
import logging
import datetime
logging.basicConfig(filename='dinner.log', encoding='utf-8', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Define a custom timestamp format
timestamp_format = '%Y-%m-%d %H:%M:%S'

# Function to get the current timestamp
def get_current_timestamp():
    return datetime.datetime.now().strftime(timestamp_format)

data2021 = pd.read_excel("Running Dinner eerste oplossing 2021.xlsx")
data2022 = pd.read_excel("Running Dinner eerste oplossing 2022.xlsx")

#check dat iedereen ingedeeld is -> MOET
def is_everyone_plannend(data, course):
    """
    Checks if everyone is in the planning to eat every meal.
    :input: The dataframe with the current planning.
    :output: Boolean.
    """
    return not(data[course].isnull().values.any())

#check of dat huisadres max niet overschreidt bij wisselingen -> MOET
def max_people_not_exceeded(data, course):
    """
    Checks if the maximum people per adres per meal is not exceeded.
    :input: The dataframe with the current planning.
    :output: A boolean.
    """
    data_voor_kokers = data[data['kookt'] == course]
    unique_huisadres_values = data_voor_kokers['Huisadres'].unique()

    for huisadres in unique_huisadres_values:
        data_voor = data_voor_kokers[course].value_counts()[huisadres]
        if not (data_voor_kokers['aantal'] >= data_voor).all():
            return False
    
    return True

#check of dat de paren bij elkaar blijven -> MOET
def duo_check(data, course):
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

def together_before(r1,r2):
    """
    Checks if two participants have eaten together before.
    :r1: row of dataframe with the data of participant 1.
    :r2: row of dataframe with the data of participant 2.
    :output: boolean.
    """
    r2_compatible= r2["Voor"]
    r2_compatible = r2_compatible.replace("V","VW")
    r2_compatible = r2_compatible.replace("W", "WO")
    if r1["Voor"] == r2_compatible:
        return True
    r2_compatible= r2["Hoofd"]
    r2_compatible = r2_compatible.replace("V","VW")
    r2_compatible = r2_compatible.replace("W", "WO")
    if r1["Hoofd"] == r2_compatible:
        return True
    r2_compatible= r2["Na"]
    r2_compatible = r2_compatible.replace("V","VW")
    r2_compatible = r2_compatible.replace("W", "WO")
    if r1["Na"] == r2_compatible:
        return True
    return False

#Eis 2/3, belangrijkst 3x
#deelnemer 1 en 2 maximaal 1 keer samen zit aan een tafel tov van vorige jaren. Tellen hoevaak dit NIET het geval is -> int -> gewenst zo laag mogelijk
def check_previous_years(data,df):
    """
    Checks the amount of people that are grouped with the same people as the year before.
    :input: The dataframe with the current planning.
    :output: A score.
    """
    score = 0
    for index1, row1 in data.iterrows():
        for index2, row2 in data2021.iloc[(index1+1):].iterrows():
            together_or_not = together_before(row1,row2)
            if together_or_not == True and row1["Bewoner"] != row2["Bewoner"]:
                score += 1
    return score/2 # The score is divided by 2, because it matches all participants twice.

#Alle checks uitvoeren en score terug geven
def calculate_planning(data, course):
    """
    Checks if the planning is possible with the given constraints.
    If it is possible, it gives the planning score (the less, the better).
    :input: The dataframe with the current planning.
    :output: int.
    """
    everyone_planned = is_everyone_plannend(data, course)
    max_people = max_people_not_exceeded(data, course)
    duos = duo_check(data, course)
    #counter_2021 = check_previous_years(data,data2021)
    #counter_2022 = check_previous_years(data,data2022)

    if everyone_planned and max_people and duos:
        score = more_than_once_together(data)*6
        return score
    else:
        return 99999999999
    
def get_bewoner_pairs(data):
    """
    Generates a list with the participants that have to stay together during the evening.
    :input: The dataframe with the current planning.
    :output: A list.
    """
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
    """
    summary
    :input:
    :output:
    """
    for key, value in my_dict.items():
        if val == value:
            return key
 
    return "key doesn't exist"

def get_index_same_adres(index, data, bewoner_lijst, index2, course):
    """
    Find another index with the same address as the given index for the first course ('Voor')
    and ensure it does not match any data in the bewoner_lijst.
    :param index: The index for which you want to find a matching index.
    :param data: The dataframe with the current planning.
    :param bewoner_lijst: A dictionary mapping one participant to another.
    :return: The matching index or 0 if not found.
    """
    # Get the participant's address and table assignment for the first course ('Voor')
    address = data.at[index, course]

    # Filter the data to find potential matching participants with the same address
    potential_matches = data[(data[course] == address) & (index not in bewoner_lijst.keys()) & (index2 not in bewoner_lijst.keys())]

    # Check if there are potential matches other than the given index
    if len(potential_matches) > 1:
        # Remove the given index from potential matches if present
        potential_matches = potential_matches[potential_matches.index != index]
        potential_matches = potential_matches[potential_matches.index != index2]

        # Return the index of a matching participant
        return potential_matches.index[0]

    # If no matching index is found, return 0
    return 9999

def get_adress(index, data, course):
    address = data.at[index, course]
    return address

def read_planning(course, data):
    score = calculate_planning(data, course)
    logging.info(f"{get_current_timestamp()} - Starting with score: {score}")
    # Create a new dataframe for participants with "Kookt" == course
    participants_voor = data[data['kookt'] == course]

    # Filter participants with "Kookt" != course from the main dataframe
    data_save = data[data['kookt'] != course]
    data_save = data_save.reset_index(drop=True)
    bewoner_lijst = get_bewoner_pairs(data_save)

    for index1, row1 in data_save.iterrows():
        if index1 not in bewoner_lijst:
            old_adress = get_adress(index1, data_save, course)
            for index2, row2 in data_save.iloc[(index1+1):].iterrows():
                #als een van de paren wisselt, moet de ander ook wisselen. Iets van een koppeling tussen de twee hebben
                #if row1["Bewoner"] == onderdeel van paar -> ruil row1 en parner voor row2 en iemand met zelfde huisnummer
                new_adress = get_adress(index2, data_save, course)
                if old_adress != new_adress:
                    if index1 in bewoner_lijst.values():
                        key = get_key(index1, bewoner_lijst)
                        #get random index waar voor = voor van row2. Hierbij mag index3 niet gelijk zijn aan een van de paren of iemand die voor kookt
                        index3 = get_index_same_adres(index2, data_save, bewoner_lijst, index1, course)
                        if index3 != 9999:
                            data_save.at[index1, course] = new_adress #pair bewoner1
                            data_save.at[key, course] = new_adress #pair bewoner1
                            data_save.at[index2, course] = old_adress #Index2 bewoner die loopt
                            data_save.at[index3, course] = old_adress #Index van bewoner met hetzelfde adres als bewoner erboven
                    else:
                        data_save.at[index1, course] = new_adress
                        data_save.at[index2, course] = old_adress

                    data = pd.concat([data_save, participants_voor], ignore_index=True)
                    new_score = calculate_planning(data, course)

                    if new_score >= score:
                        if index1 in bewoner_lijst.values():
                            if index3 != 9999:
                                data_save.at[index1, course] = old_adress #Bewoner1
                                data_save.at[key, course] = old_adress #Bewoner2
                                data_save.at[index2, course] = new_adress #Index2 bewoner
                                data_save.at[index3, course] = new_adress
                        else:
                            data_save.at[index1, course] = old_adress
                            data_save.at[index2, course] = new_adress
                    else:
                        logging.info(f"{get_current_timestamp()} - Better score found: {new_score}")
                        old_adress = new_adress
                        score = new_score
    
    data = pd.concat([data_save, participants_voor], ignore_index=True)
    return data

def main():
    logging.info(f"{get_current_timestamp()} - Starting program...")
    data = pd.read_excel("Running Dinner eerste oplossing 2022.xlsx")
    data = data.drop(data.columns[0], axis=1)
    logging.info(f"{get_current_timestamp()} - Starting voor...")
    data = read_planning("Voor", data)
    logging.info(f"{get_current_timestamp()} - Starting hoofd...")
    data = read_planning("Hoofd", data)
    logging.info(f"{get_current_timestamp()} - Starting na...")
    data = read_planning("Na", data)

    data.to_excel("new_planning.xlsx")
    logging.info(f"{get_current_timestamp()}- Finished")
    logging.info(f"--------------------------------------------------------------------------------------")

main()