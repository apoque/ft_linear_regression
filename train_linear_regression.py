#!/usr/bin/python

from __future__ import division
import os
import sys
import csv
import math
import numpy as np
import matplotlib.pyplot as plt

xCost = []
yCost = []
scaler = 100000
limitImprovement = 0.01

def calcCost(iteration, distance, price, t0, t1):
    i = 0
    tmpcost = 0
    while i < len(distance):
        tmpcost += pow(t0 + (t1 * (float(distance[i]) / scaler)) - (float(price[i])), 2)
        i+= 1
    xCost.append(iteration)
    yCost.append(math.sqrt((1 / len(distance)) * tmpcost))

def getDerivates(distance, price, t0, t1):
    i = 0
    sum0 = 0
    sum1 = 0
    while i < len(distance):
        sum0 += t0 + (t1 * (float(distance[i]) / scaler)) - (float(price[i]))
        sum1 += (t0 + t1 * (float(distance[i]) / scaler) - (float(price[i]))) * ((float(distance[i]) / scaler))
        i += 1
    return [sum0, sum1]

def gradientDescent(distance, price):
    n = len(distance)
    i = 0
    learning_rate = 0.1
    t0_updated = 0
    t1_updated = 0
    while i < 2 or (yCost[len(yCost) - 2] - yCost[len(yCost) - 1]) > limitImprovement:
        derivates = getDerivates(distance, price, t0_updated, t1_updated)
        t0_updated = t0_updated - learning_rate * (1 / n) * derivates[0]
        t1_updated = t1_updated - learning_rate * (1 / n) * derivates[1]
        calcCost(i, distance, price, t0_updated, t1_updated)
        #learning_rate *= 0.9999
        i += 1
    print(learning_rate)
    print(yCost[len(yCost) - 1])
    print(t0_updated)
    print(t1_updated)
    return [t0_updated, t1_updated]

def treat(filename):
    distance = []
    price = []
    if os.path.isfile(filename):
        with open(filename) as csvfile:
            f = csv.reader(csvfile, delimiter=',')
            for row in f:
                distance.append(row[0])
                price.append(row[1])
            distance.pop(0)
            price.pop(0)
            t = gradientDescent(distance, price)
            fig, plt1 = plt.subplots(2, 1)
            
            plt1[0].plot(distance, price, "ro")
            plt1[0].set_title('Price vs. Mileage')
            plt1[0].set_xlabel('Mileage')
            plt1[0].set_ylabel('Price')
            plt1[0].grid(True)
            plt1[0].plot([0, 248000], [t[0] + ((t[1] * 0)), t[0] + ((t[1] * 248000 / scaler))])
            
            plt1[1].set_title('Cost Function')
            plt1[1].set_xlabel('Iterations')
            plt1[1].set_ylabel('Cost')
            plt1[1].grid(True)
            plt1[1].plot(xCost, yCost)

            plt.tight_layout()
            plt.savefig('results.png', dpi=300)
            plt.show()

            with open('results.csv', 'wb') as csvfile:
                filewriter = csv.writer(csvfile, delimiter=',',
                quotechar='|', quoting=csv.QUOTE_MINIMAL)
                filewriter.writerow([t[0], t[1], scaler])

def main(argv):
    i = 0
    if len(argv) == 0:
        treat("data.csv")
    elif len(argv) == 1:
        if argv[0].find('.csv') > 0: # a checker
            treat(argv[0])
        else:
            print("File " + argv[0] + " not well formated. Please give .csv files only.")
    else:
        print("This program can only accept one .csv file")

if __name__ == "__main__":
    main(sys.argv[1:])
