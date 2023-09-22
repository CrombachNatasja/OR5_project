import random
import time

random.seed(42)

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