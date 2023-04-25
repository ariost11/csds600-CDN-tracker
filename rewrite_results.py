import os
import requests
import pandas as pd
import json
import subprocess
import re


def run():
    file = open("results.txt", "r")
    lines = file.readlines()
    file.close()

    
    file = open("flipped_results.txt", "w")
    for line in lines:
        split = line.split("\n")[0].split(":")
        file.write(split[1] + ":" + split[0] + "\n")
    file.close()

run()
