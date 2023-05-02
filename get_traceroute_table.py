names = ["France Telecom - Orange", "SIFY-AS-IN Sify Limited", "Akamai", "LEVEL3", "Amazon Cloudfront", "Cloudflare", "Fastly"]

def rewrite_traceroute():
    file = open("figures/traceroutes.txt", "w")
    file.close()
    for name in names:
        exclude = ["192.150", "169.229", "128.32", "137.164", "*", "to"]
        file = open("active_data/traceroutes/" + name + "_top50k.txt", "r")
        lines = file.readlines()
        map = {}
        for line in lines:
            ip = line.split("\n")[0].split(": ")[0]
            quantity = line.split("\n")[0].split(": ")[1]
            if not any(excluded_str in ip for excluded_str in exclude):
                if not ip in map:
                    map[ip] = 0
                map[ip] += int(quantity)
        top_30 = list(dict(sorted(map.items(), key=lambda item: item[1], reverse=True)).items())[0:30]
        file.close()
        file = open("figures/traceroutes.txt", "a")
        file.write(name + "\n")
        for entry in top_30:
            file.write(entry[0] + ": " + str(entry[1]) + "\n")
        file.close()

rewrite_traceroute()