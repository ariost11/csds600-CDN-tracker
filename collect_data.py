import os
import requests
import pandas as pd
import json
import subprocess
import re

CDN_map = { 
  "akadns": "Akamai",
  "akagtm": "Akamai",
  "akahost": "Akamai",
  "akamai": "Akamai",
  "akaquill": "Akamai",
  "akasecure": "Akamai",
  "akascripcn": "Akamai",
  "edgekey": "Akamai",
  "edgesuite": "Akamai",
  "alibaba": "Alibaba Cloud",
  "aliyun": "Alibaba Cloud",
  "aliyuncs": "Alibaba Cloud",
  "cdngslb": "Alibaba Cloud",
  "alicdn": "Alibaba Cloud",
  "alikunlun": "Alibaba Cloud",
  "kunlunaq": "Alibaba Cloud",
  "kunlunar": "Alibaba Cloud",
  "kunluncan": "Alibaba Cloud",
  "kunlunsl": "Alibaba Cloud",
  "kunlunso": "Alibaba Cloud",
  "queniuaa": "Alibaba Cloud",
  "queniuak": "Alibaba Cloud",
  "queniubg": "Alibaba Cloud",
  "queniucf": "Alibaba Cloud",
  "queniuco": "Alibaba Cloud",
  "queniufm": "Alibaba Cloud",
  "queniuhy": "Alibaba Cloud",
  "queniuiq": "Alibaba Cloud",
  "queniukr": "Alibaba Cloud",
  "queniukw": "Alibaba Cloud",
  "queniulf": "Alibaba Cloud",
  "queniurc": "Alibaba Cloud",
  "queniuso": "Alibaba Cloud",
  "queniusy": "Alibaba Cloud",
  "queniusz": "Alibaba Cloud",
  "queniutc": "Alibaba Cloud",
  "queniuuf": "Alibaba Cloud",
  "queniuum": "Alibaba Cloud",
  "queniuyk": "Alibaba Cloud",
  "cloudfront": "Amazon Cloudfront",
  "apple": "Apple CDN",
  "msedge": "Azure Front Door",
  "baidu": "Baidu",
  "bdimb": "Baidu",
  "bdstatic": "Baidu",
  "gshifen": "Baidu",
  "popin": "Baidu",
  "shifen": "Baidu",
  "bcebos": "Baidu",
  "bdydns": "Baidu",
  "baicdnx": "BaishanCloud",
  "baishan": "BaishanCloud",
  "bsgslb": "BaishanCloud",
  "b-cdn": "Bunny",
  "bunny": "Bunny",
  "cachefly": "CacheFly",
  "cdn77": "CDN77",
  "panthercdn": "CDNetworks",
  "cdngc": "CDNetworks",
  "gccdn": "CDNetworks",
  "cdnify": "CDNify",
  "cloudflare": "Cloudflare",
  "alphacdn": "Edgio",
  "chicdn": "Edgio",
  "deltacdn": "Edgio",
  "delvenetworks": "Edgio",
  "edg": "Edgio",
  "edgecast": "Edgio",
  "edgecastcdn": "Edgio",
  "edgecastdns": "Edgio",
  "epsiloncdn": "Edgio",
  "gammacdn": "Edgio",
  "iotacdn": "Edgio",
  "kappacdn": "Edgio",
  "limelight": "Edgio",
  "lldns": "Edgio",
  "llnw-trials": "Edgio",
  "llnw": "Edgio",
  "llnw": "Edgio",
  "llnwd": "Edgio",
  "llnwi": "Edgio",
  "mucdn": "Edgio",
  "nucdn": "Edgio",
  "omegacdn": "Edgio",
  "omicroncdn": "Edgio",
  "phicdn": "Edgio",
  "rhocdn": "Edgio",
  "sigmacdn": "Edgio",
  "systemcdn": "Edgio",
  "taucdn": "Edgio",
  "thetacdn": "Edgio",
  "upsiloncdn": "Edgio",
  "verizondigitalmedia": "Edgio",
  "xicdn": "Edgio",
  "zetacdn": "Edgio",
  "fastly": "Fastly",
  "secretcdn": "Fastly",
  "google": "Google Edge",
  "cdnhwc1": "Huawei",
  "cdnhwc2": "Huawei",
  "cdnhwc3": "Huawei",
  "cdnhwc4": "Huawei",
  "cdnhwc5": "Huawei",
  "cdnhwc6": "Huawei",
  "cdnhwc7": "Huawei",
  "cdnhwc8": "Huawei",
  "livehwc3": "Huawei",
  "keycdn": "KeyCDN",
  "kxcdn": "KeyCDN",
  "ks-cdn": "Kingsoft",
  "ksycdn": "Kingsoft",
  "ksyuncdn": "Kingsoft",
  "footprint": "Lumen",
  "fbcdn": "Meta CDN",
  "netflix": "Netflix CDN",
  "nflx": "Netflix CDN",
  "highwinds": "StackPath",
  "hwcdn": "StackPath",
  "stackpath": "StackPath",
  "steamcontent": "Steam CDN",
  "myqcloud": "Tencent Cloud CDN",
  "ovscdns": "Tencent Cloud CDN",
  "qcloudcdn": "Tencent Cloud CDN",
  "cdn20": "Wangsu",
  "cdn30": "Wangsu",
  "cdnetworks": "Wangsu",
  "cdngslb": "Wangsu",
  "cdnvideo": "Wangsu",
  "chinanetcenter": "Wangsu",
  "gccdn": "Wangsu",
  "lxdns": "Wangsu",
  "qtlcdn": "Wangsu",
  "quantil": "Wangsu",
  "wangsu": "Wangsu",
  "wscdns": "Wangsu",
  "wscloudcdn": "Wangsu",
  "wsdvs": "Wangsu",
  "wsglb0": "Wangsu",
  "wswebcdn": "Wangsu",
  "wswebpic": "Wangsu",
  "wtxcdn": "Wangsu",
  "warnermediacdn": "Warner Brothers Discovery CDN",
  "yahoo": "Yahoo"
}

ip_AS_map = {}
cdn_list = {}
max_file_size = 800000

def download_list():
    if not os.path.isfile("download_list.csv"):
        print("Downloading Tranco List...")
        url = "https://tranco-list.eu/download/Z2XKG/full"
        r = requests.get(url, allow_redirects=True)
        open("download_list.csv", "wb").write(r.content)
        print("Finished Downloading Tranco List...")
    else:
        print("Already Has Tranco List Downloaded...")

def rewrite_tranco_list():
    if not os.path.isfile("tranco_list.txt"):
        print("Reformating Tranco List...")
        file = pd.read_csv("download_list.csv", header=None)
        with open("tranco_list.txt", "a") as f:
            for i in range(max_file_size if len(file.index) > max_file_size else len(file.index)):
                f.write("www." + file.iloc[i, 1] + "\n")
        print("Finished Reformating Tranco List...")
    else:
        print("Already Has Formatted Tranco List...")


def download_ip_to_AS():
    if not os.path.isfile("ip_to_AS.tsv"):
        print("Downloading ip:AS List...")
        url = "https://iptoasn.com/data/ip2asn-combined.tsv.gz"
        r = requests.get(url, allow_redirects=True)
        open("ip_to_AS.tsv.gz", "wb").write(r.content)
        os.system("gzip -d ip_to_AS.tsv.gz")
        print("Finished Downloading ip:AS List...")
    else:
        print("Already Has ip:AS List Downloaded...")
 

def rewrite_ip_to_AS():
    print("Reformating ip:AS List...")
    file = pd.read_table("ip_to_AS.tsv", header=None, usecols=[0,1,4])
    for i in range(len(file.index)):
        mask = file.iloc[i, 0] + " - " + file.iloc[i, 1]
        if len(mask.split(".")[0]) <= 3:
            ip_AS_map[mask] = file.iloc[i, 2]
    print("Finished Formatting ip:AS List...")


def ip_match(mask, IP):
    min_ip = mask.split(' - ')[0].replace(".", "")
    max_ip = mask.split(' - ')[1].replace(".", "")
    ip = IP.split(":")[0].replace(".", "")
    return ip > min_ip and ip < max_ip


def get_cdn(hostname_arr):
    if hostname_arr[0] != None: #CNAME mapping exists
        for i in CDN_map:
            if i in hostname_arr[0]:
                if not str(CDN_map[i]) in cdn_list:
                    cdn_list[str(CDN_map[i])] = []
                cdn_list[str(CDN_map[i])].append(str(hostname_arr[0])) 
                return CDN_map[i]
    if any(i.isdigit() for i in hostname_arr[1]):
        for j in ip_AS_map:
            if ip_match(j, hostname_arr[1]):
                #get matching CDN if exists:
                matched_cdn = match_as_desc_to_cdn(str(ip_AS_map[j]))
                if not matched_cdn in cdn_list:
                    cdn_list[matched_cdn] = []
                cdn_list[matched_cdn].append(str(hostname_arr[1]))
                return matched_cdn
    else: 
        return "Not Found"
    

def run_zdns_requests():
    print("Running ZDNS Requests...")
    #get JSONs
    command = "cat tranco_list.txt | ./zdns --iterative --udp-only A"
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    output,error = process.communicate()
    json_list = output.decode().split("\n")
    json_list = json_list[:len(json_list) - 1]

    #store in dictionary
    zdns_response = {}

    for i in json_list:
        entry = [None] * 2
        if "answers" in json.loads(i)["data"]: #zdns request got a response of some sort
            for answer in json.loads(i)["data"]["answers"]:
                if "type" in answer and answer["type"] == "CNAME": #zdns request got a CNAME response
                    entry[0] = answer["answer"]
            #adding IP from A response
            if "resolver" in json.loads(i)["data"]:
                entry[1] = json.loads(i)["data"]["resolver"]
        else: #zdns request doesn't have a data field but still got a response
            if "resolver" in json.loads(i)["data"]:
                entry[1] = json.loads(i)["data"]["resolver"]
                
        zdns_response[json.loads(i)["name"]] = entry
    
    file = open("zdns_response.txt", "w")
    file.close()
    file = open("zdns_response.txt", "a")
    for i in zdns_response:
        file.write(i + ": (" + str(zdns_response[i][0]) + ", " + str(zdns_response[i][1]) + "): " + str(get_cdn(zdns_response[i])) + "\n")
    file.close()
    print("Completed ZDNS Requests...")


def match_as_desc_to_cdn(as_desc):
    for i in CDN_map.values():
        if i.split(" ")[0].lower() in as_desc.lower():
            return i
    return as_desc


def output_results():
    print("Formatting Data...")
    file = open("results.txt", "w")
    file.close()
    file = open("results.txt", "a")
    matched = 0
    for i in cdn_list:
        matched += len(cdn_list[i])
        file.write(i + ":" + str(len(cdn_list[i])) + "\n")
    file.write("Not Found:" + str(max_file_size - matched) + "\n")
    file.write("Percent Matched: " + str((matched / max_file_size) * 100) + "\n")
    file.close()
    print("Completed Formatting Data...")


download_list()
rewrite_tranco_list()
download_ip_to_AS()
rewrite_ip_to_AS()
run_zdns_requests()
output_results()
