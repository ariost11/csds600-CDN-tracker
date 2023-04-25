import os
import requests
import pandas as pd
import json
import subprocess
import re
import random

top_seven = ["France Telecom - Orange", "SIFY-AS-IN Sify Limited", "Akamai", "LEVEL3", "Amazon Cloudfront", "Cloudflare", "Fastly"]

top50k = {}
top300k = {}
top800k = {}

def load_dictionaries():
    top50k["France Telecom - Orange"] = []
    top300k["France Telecom - Orange"] = []
    top800k["France Telecom - Orange"] = []

    top50k["SIFY-AS-IN Sify Limited"] = []
    top300k["SIFY-AS-IN Sify Limited"] = []
    top800k["SIFY-AS-IN Sify Limited"] = []

    top50k["Akamai"] = []
    top300k["Akamai"] = []
    top800k["Akamai"] = []

    top50k["LEVEL3"] = []
    top300k["LEVEL3"] = []
    top800k["LEVEL3"] = []

    top50k["Amazon Cloudfront"] = []
    top300k["Amazon Cloudfront"] = []
    top800k["Amazon Cloudfront"] = []

    top50k["Cloudflare"] = []
    top300k["Cloudflare"] = []
    top800k["Cloudflare"] = []

    top50k["Fastly"] = []
    top300k["Fastly"] = []
    top800k["Fastly"] = []


def rewrite_zdns_responses():
    file = open("zdns_response.txt", "r")
    lines = file.readlines()
    file.close()

    line_num = 0
    for line in lines:
        split = line.split("\n")[0].split(": ")
        if split[2] in top_seven:
            if line_num < 50000:
                top50k[split[2]].append(split[0] + "\t" + split[1].split(", ")[1].split(":")[0])
            if line_num < 300000:
                top300k[split[2]].append(split[0] + "\t" + split[1].split(", ")[1].split(":")[0])
            top800k[split[2]].append(split[0] + "\t" + split[1].split(", ")[1].split(":")[0])
        line_num += 1

    #setting each list to a 1% sublist
    for name in top_seven:
        top50k[name] = random.sample(top50k[name], round(30 if (len(top50k[name]) / 100) < 30 else (len(top50k[name]) / 100)))
        top300k[name] = random.sample(top300k[name], round(30 if (len(top300k[name]) / 100) < 30 else (len(top300k[name]) / 100)))
        top800k[name] = random.sample(top800k[name], round(30 if (len(top800k[name]) / 100) < 30 else (len(top800k[name]) / 100)))


def reset_dir():
    if os.path.exists("active_data"):
        os.system("rm -rf active_data")
    os.system("mkdir active_data")


def domain_lookup_times():
    if os.path.exists("active_data/domainlookups/"):
        os.system("rm -rf active_data/domainlookups/")
    os.system("mkdir active_data/domainlookups")

    print("Running Domain Lookups...")
    for name in top_seven:

        print("Domain Lookups on " + name + "...")
        file = open("active_data/domainlookups/" + name + "_top50k.txt", "w")
        file.close()
        file = open("active_data/domainlookups/" + name + "_top50k.txt", "a")
        for tuple in top50k[name]:
            hostname = tuple.split("\t")[0]
            
            command = "dig " + hostname + " | grep time"
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
            output,error = process.communicate()
            result = output.decode().split("\n")[0]

            file.write(hostname + " " + result + "\n")
        file.close()

        file = open("active_data/domainlookups/" + name + "_top300k.txt", "w")
        file.close()
        file = open("active_data/domainlookups/" + name + "_top300k.txt", "a")
        for tuple in top300k[name]:
            hostname = tuple.split("\t")[0]
            
            command = "dig " + hostname + " | grep time"
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
            output,error = process.communicate()
            result = output.decode().split("\n")[0]

            file.write(hostname + " " + result + "\n")
        file.close()

        file = open("active_data/domainlookups/" + name + "_top800k.txt", "w")
        file.close()
        file = open("active_data/domainlookups/" + name + "_top800k.txt", "a")
        for tuple in top800k[name]:
            hostname = tuple.split("\t")[0]
            
            command = "dig " + hostname + " | grep time"
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
            output,error = process.communicate()
            result = output.decode().split("\n")[0]

            file.write(hostname + " " + result + "\n")
        file.close()


def pings():
    if os.path.exists("active_data/pings/"):
        os.system("rm -rf active_data/pings/")
    os.system("mkdir active_data/pings")

    print("Running pings...")
    for name in top_seven:

        print("Pings on " + name + "...")
        file = open("active_data/pings/" + name + "_top50k.txt", "w")
        file.close()
        file = open("active_data/pings/" + name + "_top50k.txt", "a")
        for tuple in top50k[name]:
            hostname = tuple.split("\t")[0]
            ip = tuple.split("\t")[1]
            
            command = "ping " + ip + " -c 5 -i .2 | grep rtt"
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
            output,error = process.communicate()
            result = output.decode().split("\n")[0]

            file.write(hostname + " " + result + "\n")
        file.close()

        file = open("active_data/pings/" + name + "_top300k.txt", "w")
        file.close()
        file = open("active_data/pings/" + name + "_top300k.txt", "a")
        for tuple in top300k[name]:
            hostname = tuple.split("\t")[0]
            ip = tuple.split("\t")[1]
            
            command = "ping " + ip + " -c 5 -i .2 | grep rtt"
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
            output,error = process.communicate()
            result = output.decode().split("\n")[0]

            file.write(hostname + " " + result + "\n")
        file.close()

        file = open("active_data/pings/" + name + "_top800k.txt", "w")
        file.close()
        file = open("active_data/pings/" + name + "_top800k.txt", "a")
        for tuple in top800k[name]:
            hostname = tuple.split("\t")[0]
            ip = tuple.split("\t")[1]
            
            command = "ping " + ip + " -c 5 -i .2 | grep rtt"
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
            output,error = process.communicate()
            result = output.decode().split("\n")[0]

            file.write(hostname + " " + result + "\n")
        file.close()


def first_byte():
    #TODO: Fix the commands
    if os.path.exists("active_data/firstbyte/"):
        os.system("rm -rf active_data/firstbyte/")
    os.system("mkdir active_data/firstbyte")

    print("Running Time to First Byte...")
    for name in top_seven:

        print("Time to First Byte on " + name + "...")
        file = open("active_data/firstbyte/" + name + "_top50k.txt", "w")
        file.close()
        file = open("active_data/firstbyte/" + name + "_top50k.txt", "a")
        for tuple in top50k[name]:
            ip = tuple.split("\t")[1]
            hostname = tuple.split("\t")[0]
            
            command = "curl http://" + ip + " - H Host: " + hostname + " | grep time"
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
            output,error = process.communicate()
            result = output.decode().split("\n")[0]

            file.write(hostname + " " + result + "\n")
        file.close()

        file = open("active_data/firstbyte/" + name + "_top300k.txt", "w")
        file.close()
        file = open("active_data/firstbyte/" + name + "_top300k.txt", "a")
        for tuple in top300k[name]:
            ip = tuple.split("\t")[1]
            hostname = tuple.split("\t")[0]
            
            command = "dig " + hostname + " | grep time"
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
            output,error = process.communicate()
            result = output.decode().split("\n")[0]

            file.write(hostname + " " + result + "\n")
        file.close()

        file = open("active_data/firstbyte/" + name + "_top800k.txt", "w")
        file.close()
        file = open("active_data/firstbyte/" + name + "_top800k.txt", "a")
        for tuple in top800k[name]:
            ip = tuple.split("\t")[1]
            hostname = tuple.split("\t")[0]
            
            command = "dig " + hostname + " | grep time"
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
            output,error = process.communicate()
            result = output.decode().split("\n")[0]

            file.write(hostname + " " + result + "\n")
        file.close()


def traceroutes():
    if os.path.exists("active_data/traceroutes/"):
        os.system("rm -rf active_data/traceroutes/")
    os.system("mkdir active_data/traceroutes")

    print("Running traceroutes...")
    for name in top_seven:

        print("Traceroutes on " + name + "...")
        file = open("active_data/traceroutes/" + name + "_top50k.txt", "w")
        file.close()
        file = open("active_data/traceroutes/" + name + "_top50k.txt", "a")

        map = {}
        for tuple in top50k[name]:
            hostname = tuple.split("\t")[0]
            ip = tuple.split("\t")[1]
            
            command = "traceroute -n -q 1 " + ip + " -w 1 -m 64 | awk '{print $2}'"
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
            output,error = process.communicate()
            results = output.decode().split("\n")
            results = results[:len(results) - 1]

            for result in results:
                if not result in map:
                    map[result] = 0
                map[result] += 1
        
        for key in map:
            file.write(key + ": " + str(map[key]) + "\n")
        file.close()

load_dictionaries()
rewrite_zdns_responses()
reset_dir()
domain_lookup_times()
pings()
traceroutes()