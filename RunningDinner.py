import pandas as pd
import logging
import datetime
logging.basicConfig(filename='dinner.log', encoding='utf-8', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

#Define a custom timestamp format
timestamp_format = '%Y-%m-%d %H:%M:%S'

#Function to get the current timestamp
def get_current_timestamp():
    return datetime.datetime.now().strftime(timestamp_format)

#check dat iedereen ingedeeld is -> MOET
def is_everyone_plannend(data, course):
    """
    Checks if everyone is in the planning to eat every meal.
    :input: The dataframe with the current planning.
    :output: Boolean.
    """
    return not(data[course].isnull().values.any())

#check of dat huisaddress max niet overschreidt bij wisselingen -> MOET
def max_people_not_exceeded(data, course):
    """
    Checks if the maximum people per address per meal is not exceeded.
    :input: The dataframe with the current planning.
    :output: A boolean.
    """
    data_voor_kokers = data[data['kookt'] == course]
    unique_huisaddress_values = data_voor_kokers['Huisadres'].unique()

    for huisaddress in unique_huisaddress_values:
        data_voor = data_voor_kokers[course].value_counts()[huisaddress]
        if not (data_voor_kokers['aantal'] >= data_voor).all():
            return False
    
    return True

#check of dat de paren bij elkaar blijven -> MOET
def duo_check(data, df_paar):
    """
    Checks if the duos that need to stay together are placed together.
    :input: The dataframe with the current planning.
    :output: A boolean.
    """
    pairs = True

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
def check_previous_years(data,data2021):
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
def calculate_planning(data, data2021, data2022, course, df_paar):
    """
    Checks if the planning is possible with the given constraints.
    If it is possible, it gives the planning score (the less, the better).
    :input: The dataframe with the current planning.
    :output: int.
    """
    everyone_planned = is_everyone_plannend(data, course)
    max_people = max_people_not_exceeded(data, course)
    duos = duo_check(data, df_paar)
    counter_2021 = check_previous_years(data,data2021)
    counter_2022 = check_previous_years(data,data2022)

    if everyone_planned and max_people and duos:
        score = more_than_once_together(data)*6 + counter_2022*3 + counter_2021*1
        return score
    else:
        return 99999999999
    
def get_bewoner_pairs(data, df_paar):
    """
    Generates a list with the participants that have to stay together during the evening.
    :param data: The dataframe with the current planning.
    :return: A list.
    """
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
    Function to return a key from a dictionary based on value
    :param val: the value belonging to a key
    :param my_dict: the dictionary in which you want the key from
    :return: the key belonging to the value. if it does not exist return that it does not exist
    """
    for key, value in my_dict.items():
        if val == value:
            return key
 
    return "key doesn't exist"

def get_index_same_address(index, data, bewoner_lijst, index2, course):
    """
    Find another index with the same address as the given index for the course
    and ensure it does not match any data in the bewoner_lijst.
    :param index: The index for which you want to find a matching index.
    :param data: The dataframe with the current planning.
    :param bewoner_lijst: A dictionary mapping one participant to another.
    :return: The matching index or 0 if not found.
    """
    #Get the participant's address and table assignment for the course
    address = data.at[index, course]

    #Filter the data to find potential matching participants with the same address
    potential_matches = data[(data[course] == address) & (index not in bewoner_lijst.keys()) & (index2 not in bewoner_lijst.keys())]

    #Check if there are potential matches other than the given index
    if len(potential_matches) > 1:
        #Remove the given index from potential matches if present
        potential_matches = potential_matches[potential_matches.index != index]
        potential_matches = potential_matches[potential_matches.index != index2]

        #Return the index of a matching participant
        return potential_matches.index[0]

    #If no matching index is found, return 0
    return 9999

def get_address(index, data, course):
    """"
    Returns the address of the index
    :param index: the index of the bewoner
    :param data: DataFrame for the planning
    :param course: the course for which the address is required
    :return: the address
    """
    address = data.at[index, course]
    return address

def read_planning(course, data, data2021, data2022, df_paar):
    """
    Function that applies the switching algorithm and based on scores keeps or discard the change
    :param course: For which course (Voor, hoofd or na) it switches
    :param data: DataFrame which holds the planning
    :return: DataFrame where the algorithm is applied
    """
    #bereken de startscore waarmee de huidige planning begint
    score = calculate_planning(data, data2021, data2022, course, df_paar)
    logging.info(f"{get_current_timestamp()} - Starting with score: {score}")
    #filter de personen eruit die wel koken. Deze moeten namelijk op het address blijven
    participants_voor = data[data['kookt'] == course]

    #filter de personen eruit die niet het gerecht koken
    data_save = data[data['kookt'] != course]
    data_save = data_save.reset_index(drop=True)
    #vraag de paren op die bij elkaar moeten blijven
    bewoner_lijst = get_bewoner_pairs(data_save, df_paar)

    for index1, row1 in data_save.iterrows():
        #als het tweede gedeelte van het paar komt kan deze geskipt worden.
        if index1 not in bewoner_lijst:
            old_address = get_address(index1, data_save, course)
            #index+1 zodat je bekeken situaties niet meer terugkomen
            for index2, row2 in data_save.iloc[(index1+1):].iterrows():
                #als een van de paren wisselt, moet de ander ook wisselen. Iets van een koppeling tussen de twee hebben
                #if row1["Bewoner"] == onderdeel van paar -> ruil index1 en parner voor index2 en iemand met zelfde huisnummer
                new_address = get_address(index2, data_save, course)
                #als address niet hetzelfde is wisselen, anders heeft het toch geen zin
                if old_address != new_address:
                    #als bewoner 1 onderdeel is van een paar
                    if index1 in bewoner_lijst.values():
                        key = get_key(index1, bewoner_lijst)
                        #get index waar address = address van index2. Hierbij mag index3 niet gelijk zijn aan een van de paren of iemand die voor kookt
                        index3 = get_index_same_address(index2, data_save, bewoner_lijst, index1, course)
                        if index3 != 9999:
                            data_save.at[index1, course] = new_address #pair bewoner1
                            data_save.at[key, course] = new_address #pair bewoner1
                            data_save.at[index2, course] = old_address #Index2 bewoner die loopt
                            data_save.at[index3, course] = old_address #Index van bewoner met hetzelfde address als bewoner erboven
                    else:
                        data_save.at[index1, course] = new_address
                        data_save.at[index2, course] = old_address

                    #voeg de data die gewisseld worden samen met de andere personen die voorgerecht komen om de score te bepalen
                    data = pd.concat([data_save, participants_voor], ignore_index=True)
                    #bereken de score op de nieuwe planning
                    new_score = calculate_planning(data, data2021, data2022, course, df_paar)

                    #als de niewe score niet beter is of de planning niet voldoet aan de eisen, wissel de addressen terug
                    if new_score >= score:
                        if index1 in bewoner_lijst.values():
                            if index3 != 9999:
                                data_save.at[index1, course] = old_address #Bewoner1
                                data_save.at[key, course] = old_address #Bewoner2
                                data_save.at[index2, course] = new_address #Index2 bewoner
                                data_save.at[index3, course] = new_address
                        else:
                            data_save.at[index1, course] = old_address
                            data_save.at[index2, course] = new_address
                    else:
                        #wel voldoen? bewaar het nieuwe address en de nieuwe lagere score
                        logging.info(f"{get_current_timestamp()} - Better score found: {new_score}")
                        old_address = new_address
                        score = new_score
    
    data = pd.concat([data_save, participants_voor], ignore_index=True)
    return data

def improve_planning(data2023, data2021, data2022, df_paar):
    """
    Performs all steps needed to generate an Excel sheet with the new planning.
    """
    logging.info(f"{get_current_timestamp()} - Starting program...")

    data = data.drop(data.columns[0], axis=1)
    logging.info(f"{get_current_timestamp()} - Starting voor...")
    data = read_planning("Voor", data2023, data2021, data2022, df_paar)
    logging.info(f"{get_current_timestamp()} - Starting hoofd...")
    data = read_planning("Hoofd", data2023, data2021, data2022, df_paar)
    logging.info(f"{get_current_timestamp()} - Starting na...")
    data = read_planning("Na", data2023, data2021, data2022, df_paar)

    data.to_excel("new_planning.xlsx")
    logging.info(f"{get_current_timestamp()}- Finished")
    logging.info(f"--------------------------------------------------------------------------------------")