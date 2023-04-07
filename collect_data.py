import os
import requests
import pandas as pd
import json
import subprocess

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

num_found = 0

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
    max_file_size = 1000
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


def is_ip(ip):
    ip1 = ip.split(":")[0]
    ip_arr = ip1.split(".")
    print(ip_arr)
    for i in range(4):
        if not ip_arr[i].isnumeric():
            return False
    return len(ip_arr) == 4


def ip_match(mask, IP):
    min_ip = mask.split(' - ')[0].split('.')
    max_ip = mask.split(' - ')[1].split('.')
    ip = IP.split('.')
    for i in range(4):
        if int(ip[i]) < int(min_ip[i]) or int(ip[i]) > int(max_ip[i]):
            return False
    return True

        
def get_cdn(hostname):
    for i in CDN_map:
        #check for CNAME mapping
        if i in hostname:
            global num_found
            num_found += 1
            return CDN_map[i]
    
    #check for ip mapping
    if is_ip(hostname):
        for j in ip_AS_map:
            if ip_match(j, hostname):
                return ip_AS_map[j]

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
    ip_map = {}
    
    cname_matches = 0

    for i in json_list:
        if "answers" in json.loads(i)["data"]:
            hit = False
            for answer in json.loads(i)["data"]["answers"]:
                if answer["type"] == "CNAME":
                    ip_map[answer["name"]] = answer["answer"]
                    cname_matches += 1
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
    
    file = open("ip_map.txt", "w")
    file.close()
    file = open("ip_map.txt", "a")
    for i in ip_map:
        file.write(i + " " + get_cdn(ip_map[i]) + "\n")    
    print("Percent Found: " + str(100 * (num_found / cname_matches)))
    print("CName Matches Found: " + str(100 * (cname_matches / len(ip_map))))
    file.close()
    print("Completed ZDNS Requests...")

download_list()
rewrite_tranco_list()
download_ip_to_AS()
rewrite_ip_to_AS()
run_zdns_requests()
