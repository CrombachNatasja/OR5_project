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
    
    
euclidean_distance(𝑖,𝑗): returns euclidean distance between points 𝑖 and 𝑗 in 𝐼
total_distance(𝜋,𝐼): returns total distance of tour 𝜋 visiting all 𝑛 locations in 𝐼={0,…,𝑛−1}
create_random_tour(𝐼): returns a randomly generated tour visiting all locations all locations in 𝐼
two_opt(𝜋,𝐼): returns a tour visiting all locations in 𝐼 locally optimal with regard to the 2-exchange neighborhood, starting from an initial tour 𝜋
simulated_annealing(𝜋,𝐼): returns a 2-optimal tour visiting all locations in 𝐼, starting from an initial tour 𝜋 and applying simulated annealing (parameters: initial temperature 𝑇_0, cooling rate 𝑐. Smallest possible temperature 𝜖
