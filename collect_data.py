import os
import requests
import pandas as pd
import json
import subprocess

CDN_map = { 
  "alibaba":"Alibaba Cloud",
  "ateme":"ATEME",
  "baidu":"Baidu",
  "edgenext":"BaishanCloud",
  "baishan":"BaishanCloud",
  "broad":"Broadpeak",
  "broadpeak":"Broadpeak",
  "byteplus":"BytePlus",
  "bytedance":"ByteDance",
  "cdnsun":"CDNsun",
  "cdn-sun":"CDNsun",
  "ccom":"China Telecom",
  "c-com":"China Telecom",
  "comcast":"Comcast Technology Solutions",
  "edgio":"Edgio",
  "gcore":"Gcore",
  "g-core":"Gcore",
  "g-connect":"GlobalConnect",
  "gconnect":"GlobalConnect",
  "globalconnect":"GlobalConnect",
  "global-connect":"GlobalConnect",
  "huawei":"Huawei Cloud",
  "j-stream":"Jet-Stream Cloud",
  "jet-stream":"Jet-Stream Cloud",
  "jetstream":"Jet-Stream Cloud",
  "jstream":"Jet-Stream Cloud",
  "lumen":"Lumen",
  "m-streaming":"MainStreaming",
  "mstreaming":"MainStreaming",
  "mazure":"Microsoft Azure",
  "ngenix":"Ngenix",
  "qwilt":"Qwilt",
  "tencent":"Tencent Cloud",
  "tcloud":"Tencent Cloud",
  "t-cloud":"Tencent Cloud",
  "tencent-cloud":"Tencent Cloud",
  "varnish":"Varnish Software",
  "vecima":"Vecima",
  "velocix":"Velocix",
  ".clients.turbobytes.":"TurboBytes",
  ".turbobytes-cdn.":"TurboBytes",
  ".afxcdn.":"afxcdn.net",
  ".akamai.":"Akamai",
  ".akamaiedge.":"Akamai",
  ".akadns.":"Akamai",
  ".akamaitechnologies.":"Akamai",
  ".gslb.tbcache.":"Alimama",
  ".cloudfront.":"Amazon Cloudfront",
  ".anankecdn.":"Ananke",
  ".att-dsa.":"AT&T",
  ".azioncdn.":"Azion",
  ".belugacdn.":"BelugaCDN",
  ".bluehatnetwork.":"Blue Hat Network",
  ".systemcdn.":"EdgeCast",
  ".cachefly.":"Cachefly",
  ".cdn77.":"CDN77",
  ".cdn77.":"CDN77",
  ".panthercdn.":"CDNetworks",
  ".cdngc.":"CDNetworks",
  ".gccdn.":"CDNetworks",
  ".gccdn.":"CDNetworks",
  ".cdnify.":"CDNify",
  ".ccgslb.":"ChinaCache",
  ".ccgslb.":"ChinaCache",
  ".c3cache.":"ChinaCache",
  ".chinacache.":"ChinaCache",
  ".c3cdn.":"ChinaCache",
  ".lxdns.":"ChinaNetCenter",
  ".speedcdns.":"QUANTIL/ChinaNetCenter",
  ".mwcloudcdn.":"QUANTIL/ChinaNetCenter",
  ".cloudflare.":"Cloudflare",
  ".cloudflare.":"Cloudflare",
  ".edgecastcdn.":"EdgeCast",
  ".adn.":"EdgeCast",
  ".wac.":"EdgeCast",
  ".wpc.":"EdgeCast",
  ".fastly.":"Fastly",
  ".fastlylb.":"Fastly",
  ".google.":"Google",
  "googlesyndication.":"Google",
  "youtube.":"Google",
  ".googleusercontent.":"Google",
  ".l.doubleclick.":"Google",
  "d.gcdn.":"G-core",
  ".hiberniacdn.":"Hibernia",
  ".hwcdn.":"Highwinds",
  ".incapdns.":"Incapsula",
  ".inscname.":"Instartlogic",
  ".insnw.":"Instartlogic",
  ".internapcdn.":"Internap",
  ".kxcdn.":"KeyCDN",
  ".lswcdn.":"LeaseWeb CDN",
  ".footprint.":"Level3",
  ".llnwd.":"Limelight",
  ".lldns.":"Limelight",
  ".netdna-cdn.":"MaxCDN",
  ".netdna-ssl.":"MaxCDN",
  ".netdna.":"MaxCDN",
  ".stackpathdns.":"StackPath",
  ".mncdn.":"Medianova",
  ".instacontent.":"Mirror Image",
  ".mirror-image.":"Mirror Image",
  ".cap-mii.":"Mirror Image",
  ".rncdn1.":"Reflected Networks",
  ".simplecdn.":"Simple CDN",
  ".swiftcdn1.":"SwiftCDN",
  ".swiftserve.":"SwiftServe",
  ".gslb.taobao.":"Taobao",
  ".cdn.bitgravity.":"Tata communications",
  ".cdn.telefonica.":"Telefonica",
  ".vo.msecnd.":"Windows Azure",
  ".ay1.b.yahoo.":"Yahoo",
  ".yimg.":"Yahoo",
  ".zenedge.":"Zenedge",
  ".b-cdn.":"BunnyCDN",
  ".ksyuncdn.":"Kingsoft"
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
    max_file_size = 100
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

        
def match(mask, IP):
    min_ip = mask.split(' - ')[0].split('.')
    max_ip = mask.split(' - ')[1].split('.')
    range4 = range(int(min_ip[-2]), int(max_ip[-2]) + 1)
    range3 = range(int(min_ip[-1]), int(max_ip[-1]) + 1)

    ip = IP.split(".")
    if ((int(ip[-2]) in range3) and (int(ip[-1]) in range4)):
        return True

    return False

def match2(mask, IP):
    min_ip = mask.split(' - ')[0].split('.')
    max_ip = mask.split(' - ')[1].split('.')
    ip = IP.split('.')
    for i in range(4):
        if int(ip[i]) < int(min_ip[i]) or int(ip[i]) > int(max_ip[i]):
            return False
    return True
  

def rewrite_ip_to_AS():
    print("Reformating ip:AS List...")
    file = pd.read_table("ip_to_AS.tsv", header=None, usecols=[0,1,4])
    for i in range(len(file.index)):
        mask = file.iloc[i, 0] + " - " + file.iloc[i, 1]
        if len(mask.split(".")[0]) <= 3:
            ip_AS_map[mask] = file.iloc[i, 2]
    print(ip_AS_map)
    print("Finished Formatting ip:AS List...")

        
def get_cdn(hostname):
    for i in CDN_map:
        #check for CNAME mapping
        if i in hostname:
            global num_found
            num_found += 1
            return CDN_map[i]
    
        #check for IP mapping
        for j in ip_AS_map:
            if match2(j, i):
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
        file.write(i + " " + get_cdn(i) + "\n")    
    print("Percent Found: " + str(100 * (num_found / cname_matches)))
    print("CName Matches Found: " + str(100 * (cname_matches / len(ip_map))))
    file.close()
    print("Completed ZDNS Requests...")

download_list()
rewrite_tranco_list()
download_ip_to_AS()
rewrite_ip_to_AS()
run_zdns_requests()
