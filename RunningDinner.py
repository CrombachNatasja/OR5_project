import pandas as pd
import numpy as np
import streamlit as st
import random
import time

uploaded_file = 

read_planning("Running Dinner eerste oplossing 2022.xlsx")

def read_planning(uploaded_file):
    data = pd.read_excel(uploaded_file)
    
def switch_voorgerecht(uploaded_file):
    df['Voor'] = df['Voor'].sample(frac=1).reset_index(drop=True)
    return

def switch_hoofd():
    df['Hoofd'] = df['Hoofd'].sample(frac=1).reset_index(drop=True)
    return
    
def switch_na():
    df['Na'] = df['Na'].sample(frac=1).reset_index(drop=True)
    return
    
def wie_kookt_wat():



def define_table_seating():
    points = []
    for  i in range(10):
    x = random.uniform(0,100)
    y = random.uniform(0,100)
    points.append((x,y))

def check_eisen():
    

start_time = time.time()
two_opt_tour = two_opt(tour,points)
end_time = time.time()
elapsed_time = end_time - start_time