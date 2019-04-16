#!/usr/bin/python

from __future__ import division
from __future__ import print_function
import os
import sys
import csv
import math
import numpy as np
import matplotlib.pyplot as plt

def visualise(t0, t1, val, scaler):
    distance = []
    price = []
    if os.path.isfile("data.csv"):
        with open("data.csv") as csvfile:
            f = csv.reader(csvfile, delimiter=',')
            for row in f:
                distance.append(row[0])
                price.append(row[1])
            distance.pop(0)
            price.pop(0)
            
            print(t0 + t1 * val / scaler)
            fig, plt1 = plt.subplots()
            plt1.plot(distance, price, "ro")
            plt1.plot([val], [t0 + t1 * val / scaler], marker='o', markersize=10, color="yellow")
            plt1.set_title('Price vs. Mileage')
            plt1.set_xlabel('Mileage')
            plt1.set_ylabel('Price')
            plt1.grid(True)
            plt1.plot([0, 248000], [float(t0) + ((float(t1) * 0)), float(t0) + ((float(t1) * 248000 / scaler))])

            plt.tight_layout()
            plt.savefig('results.png', dpi=300)
            plt.show()

def predict(t0, t1, val, scaler):
    price = float(t0) + (float(t1) * int(val) / float(scaler))
    print("This car is worth ", end='')
    print(price, end='')
    print(" euros.")
    visualise(float(t0), float(t1), int(val), float(scaler))

def getMileage(t0, t1, scaler):
    nb_type = False
    while nb_type == False:
        nb = raw_input("Please enter a mileage:\n")
        try:
            val = int(nb)
            nb_type = True
        except ValueError:
            try:
                val = float(nb)
                nb_type = True
            except ValueError:
                print("That's not an int, try again")
        if nb_type == True and val < 0:
            nb_type = False
    predict(t0, t1, val, scaler)

def treat(filename):
    if os.path.isfile(filename):
        with open(filename) as csvfile:
            f = csv.reader(csvfile, delimiter=',')
            for row in f:
                t0 = row[0]
                t1 = row[1]
                scaler = row[2]
                getMileage(t0, t1, scaler)
    else:
        getMileage(0, 0, 1)

def main(argv):
    i = 0
    if len(argv) == 0:
        treat("results.csv")
    elif len(argv) == 1:
        if argv[0].find('.csv') > 0: # a checker
            treat(argv[0])
        else:
            print("File " + argv[0] + " not well formated. Please give .csv files only.")
    else:
        print("This program can only accept one .csv file")

if __name__ == "__main__":
    main(sys.argv[1:])
