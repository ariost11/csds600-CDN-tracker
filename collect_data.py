import os
import requests
import pandas as pd
import json
import subprocess

CDN_map = { 
  ".clients.turbobytes.net":"TurboBytes",
  ".turbobytes-cdn.com":"TurboBytes",
  ".afxcdn.net":"afxcdn.net",
  ".akamai.net":"Akamai",
  ".akamaiedge.net":"Akamai",
  ".akadns.net":"Akamai",
  ".akamaitechnologies.com":"Akamai",
  ".gslb.tbcache.com":"Alimama",
  ".cloudfront.net":"Amazon Cloudfront",
  ".anankecdn.com.br":"Ananke",
  ".att-dsa.net":"AT&T",
  ".azioncdn.net":"Azion",
  ".belugacdn.com":"BelugaCDN",
  ".bluehatnetwork.com":"Blue Hat Network",
  ".systemcdn.net":"EdgeCast",
  ".cachefly.net":"Cachefly",
  ".cdn77.net":"CDN77",
  ".cdn77.org":"CDN77",
  ".panthercdn.com":"CDNetworks",
  ".cdngc.net":"CDNetworks",
  ".gccdn.net":"CDNetworks",
  ".gccdn.cn":"CDNetworks",
  ".cdnify.io":"CDNify",
  ".ccgslb.com":"ChinaCache",
  ".ccgslb.net":"ChinaCache",
  ".c3cache.net":"ChinaCache",
  ".chinacache.net":"ChinaCache",
  ".c3cdn.net":"ChinaCache",
  ".lxdns.com":"ChinaNetCenter",
  ".speedcdns.com":"QUANTIL/ChinaNetCenter",
  ".mwcloudcdn.com":"QUANTIL/ChinaNetCenter",
  ".cloudflare.com":"Cloudflare",
  ".cloudflare.net":"Cloudflare",
  ".edgecastcdn.net":"EdgeCast",
  ".adn.":"EdgeCast",
  ".wac.":"EdgeCast",
  ".wpc.":"EdgeCast",
  ".fastly.net":"Fastly",
  ".fastlylb.net":"Fastly",
  ".google.":"Google",
  "googlesyndication.":"Google",
  "youtube.":"Google",
  ".googleusercontent.com":"Google",
  ".l.doubleclick.net":"Google",
  "d.gcdn.co":"G-core",
  ".hiberniacdn.com":"Hibernia",
  ".hwcdn.net":"Highwinds",
  ".incapdns.net":"Incapsula",
  ".inscname.net":"Instartlogic",
  ".insnw.net":"Instartlogic",
  ".internapcdn.net":"Internap",
  ".kxcdn.com":"KeyCDN",
  ".lswcdn.net":"LeaseWeb CDN",
  ".footprint.net":"Level3",
  ".llnwd.net":"Limelight",
  ".lldns.net":"Limelight",
  ".netdna-cdn.com":"MaxCDN",
  ".netdna-ssl.com":"MaxCDN",
  ".netdna.com":"MaxCDN",
  ".stackpathdns.com":"StackPath",
  ".mncdn.com":"Medianova",
  ".instacontent.net":"Mirror Image",
  ".mirror-image.net":"Mirror Image",
  ".cap-mii.net":"Mirror Image",
  ".rncdn1.com":"Reflected Networks",
  ".simplecdn.net":"Simple CDN",
  ".swiftcdn1.com":"SwiftCDN",
  ".swiftserve.com":"SwiftServe",
  ".gslb.taobao.com":"Taobao",
  ".cdn.bitgravity.com":"Tata communications",
  ".cdn.telefonica.com":"Telefonica",
  ".vo.msecnd.net":"Windows Azure",
  ".ay1.b.yahoo.com":"Yahoo",
  ".yimg.":"Yahoo",
  ".zenedge.net":"Zenedge",
  ".b-cdn.net":"BunnyCDN",
  ".ksyuncdn.com":"Kingsoft"
}


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
    
    file = open("ip_map.txt", "w")
    file.close()
    file = open("ip_map.txt", "a")
    count = 0
    for i in ip_map:
        added = False
        for j in CDN_map:
            if j in ip_map[i]:
                file.write(i + " " + CDN_map[j] + "\n")
                added = True
                count = count + 1
                break
        if not added:
            file.write(i + " " + ip_map[i] + "\n")
    file.write("Count: " + str(count) + "\n")
    file.close()
    print("Completed ZDNS Requests...")

download_list()
rewrite_tranco_list()
download_ip_to_AS()
run_zdns_requests()
