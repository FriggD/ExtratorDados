# -----------------------------------------------------------------------
# Lib import
import argparse, sys
import pandas as pd
import os
import csv
import concurrent.futures
import time


file = open("bovindv01.ped", 'r')

duplicated = []
animais = []
for index, line in enumerate(file):

    split = line.split(' ')
    if split[1] in animais:
        print(f"Animal {split[1]} duplicado!")
        duplicated.append(split[1])
    else:
        animais.append(split[1])
        
    if len(split) != 69992:
        print(f"{split[1]} na linha {index} possui tamanho: {len(split)}")
        time.sleep(0.3)