import os
import requests
import pandas as pd
import json
import subprocess

def download_list():
    if not os.path.isfile("download_list.csv"):
        print("Downloading Tranco List...")
        url = "https://tranco-list.eu/download/Z2XKG/full"
        r = requests.get(url, allow_redirects=True)
        open("download_list.csv", "wb").write(r.content)
        print("Finished Downloading List...")
    else:
        print("Already Has Trando List Downloaded...")

def rewrite_tranco_list():
    if not os.path.isfile("tranco_list.txt"):
        print("Reformating Tranco List...")
        file = pd.read_csv("download_list.csv", header=None)
        with open("tranco_list.txt", "a") as f:
            max_file_size = 50
            for i in range(max_file_size if len(file.index) > max_file_size else len(file.index)):
                f.write("www." + file.iloc[i, 1] + "\n")
        print("Finished Reformating List...")
    else:
        print("Already Has Formatted Tranco List...")


def run_zdns_requests():
    print("Running ZDNS Requests...")
    #get JSONs
    command = "cat tranco_list.txt | ./zdns --iterative --udp-only A"
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    output,error = process.communicate()
    json_list = output.decode().split("\n")
    json_list = json_list[:len(json_list) - 1]

    #store in dictionary
    ip_map = {}

    for i in json_list:
        if "answers" in json.loads(i)["data"]:
            hit = False
            for answer in json.loads(i)["data"]["answers"]:
                if answer["type"] == "CNAME":
                    ip_map[answer["name"]] = answer["answer"]
                    hit = True
                    break
            if not hit:
                if "resolver" in json.loads(i)["data"]:
                    ip_map[json.loads(i)["name"]] = json.loads(i)["data"]["resolver"]
                else:
                    ip_map[json.loads(i)["name"]] = "NA"
        else:
            if "resolver" in json.loads(i)["data"]:
                ip_map[json.loads(i)["name"]] = json.loads(i)["data"]["resolver"]
            else:
                ip_map[json.loads(i)["name"]] = "NA"

    #for e in json_list:
        #ip_map[json.loads(e)["name"]] = json.loads(e)["data"]["resolver"]
    for i in ip_map:
        print(i + " " + ip_map[i])
    print("Completed ZDNS Requests...")

download_list()
rewrite_tranco_list()
run_zdns_requests()
