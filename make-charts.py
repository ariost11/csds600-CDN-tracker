import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import numpy as np

names = ["France Telecom - Orange", "SIFY-AS-IN Sify Limited", "Akamai", "LEVEL3", "Amazon Cloudfront", "Cloudflare", "Fastly"]
labels_k = ["Orange - France T.", "Sify", "Akamai", "LEVEL3", "Amazon Cloudfront", "CloudFlare", "Fastly"]

pings_data_50k = []
pings_data_300k = []
pings_data_800k = []

curls_data_50k = []
curls_data_300k = []
curls_data_800k = []

domainnames_data_50k = []
domainnames_data_300k = []
domainnames_data_800k = []

def get_pings():
    for name in names:
        #50k
        file = open("active_data/pings/" + name + "_top50k.txt", "r")
        lines = file.readlines()
        avg_50k = []
        for line in lines:
            if "rtt" in line:
                avg_50k.append(line.split("\n")[0].split(" = ")[1].split("/")[1])
        file.close()
        pings_data_50k.append(np.array(avg_50k).astype(float))

        #300k
        file = open("active_data/pings/" + name + "_top300k.txt", "r")
        lines = file.readlines()
        avg_300k = []
        for line in lines:
            if "rtt" in line:
                avg_300k.append(line.split("\n")[0].split(" = ")[1].split("/")[1])
        file.close()
        pings_data_300k.append(np.array(avg_300k).astype(float))

        #800k
        file = open("active_data/pings/" + name + "_top800k.txt", "r")
        lines = file.readlines()
        avg_800k = []
        for line in lines:
            if "rtt" in line:
                avg_800k.append(line.split("\n")[0].split(" = ")[1].split("/")[1])
        file.close()
        pings_data_800k.append(np.array(avg_800k).astype(float))

        data = [np.array(avg_50k).astype(float), np.array(avg_300k).astype(float), np.array(avg_800k).astype(float)]
        labels = ["Top 50k", "Top 300k", "All 800K"]
        make_plots(data, labels, name, "pings")
    make_plots(pings_data_50k, labels_k, "comparing_50k", "pings")
    make_plots(pings_data_300k, labels_k, "comparing_300k", "pings")
    make_plots(pings_data_800k, labels_k, "comparing_800k", "pings")
    ping_variance_plot()


def get_domainlookups():
    for name in names:
        #50k
        file = open("active_data/domainlookups/" + name + "_top50k.txt", "r")
        lines = file.readlines()
        avg_50k = []
        for line in lines:
            if "Query time: " in line:
                avg_50k.append(line.split("\n")[0].split("Query time: ")[1].split(" ")[0])
        file.close()
        domainnames_data_50k.append(np.array(avg_50k).astype(float))

        file = open("active_data/domainlookups/" + name + "_top300k.txt", "r")
        lines = file.readlines()
        avg_300k = []
        for line in lines:
            if "Query time: " in line:
                avg_300k.append(line.split("\n")[0].split("Query time: ")[1].split(" ")[0])
        file.close()
        domainnames_data_300k.append(np.array(avg_300k).astype(float))

        file = open("active_data/domainlookups/" + name + "_top800k.txt", "r")
        lines = file.readlines()
        avg_800k = []
        for line in lines:
            if "Query time: " in line:
                avg_800k.append(line.split("\n")[0].split("Query time: ")[1].split(" ")[0])
        file.close()
        domainnames_data_800k.append(np.array(avg_800k).astype(float))

        data = [np.array(avg_50k).astype(float), np.array(avg_300k).astype(float), np.array(avg_800k).astype(float)]
        labels = ["Top 50k", "Top 300k", "All 800K"]
        make_plots(data, labels, name, "domainlookups")
    make_plots(domainnames_data_50k, labels_k, "comparing_50k", "domainlookups")
    make_plots(domainnames_data_300k, labels_k, "comparing_300k", "domainlookups")
    make_plots(domainnames_data_800k, labels_k, "comparing_800k", "domainlookups")
    domainnames_variance_plot()


def get_curls():
    for name in names:
        #50k
        file = open("active_data/curls/" + name + "_top50k.txt", "r")
        lines = file.readlines()
        avg_50k = []
        for line in lines:
            if " 200 " in line:
                avg_50k.append(line.split("\n")[0].split(" ")[2])
        file.close()
        curls_data_50k.append(np.array(avg_50k).astype(float))

        file = open("active_data/curls/" + name + "_top300k.txt", "r")
        lines = file.readlines()
        avg_300k = []
        for line in lines:
            if " 200 " in line:
                avg_300k.append(line.split("\n")[0].split(" ")[2])
        file.close()
        curls_data_300k.append(np.array(avg_300k).astype(float))

        file = open("active_data/curls/" + name + "_top800k.txt", "r")
        lines = file.readlines()
        avg_800k = []
        for line in lines:
            if " 200 " in line:
                avg_800k.append(line.split("\n")[0].split(" ")[2])
        file.close()
        curls_data_800k.append(np.array(avg_800k).astype(float))

        data = [np.array(avg_50k).astype(float), np.array(avg_300k).astype(float), np.array(avg_800k).astype(float)]
        labels = ["Top 50k", "Top 300k", "All 800K"]
        make_plots(data, labels, name, "curls")
    make_plots(curls_data_50k, labels_k, "comparing_50k", "curls")
    make_plots(curls_data_300k, labels_k, "comparing_300k", "curls")
    make_plots(curls_data_800k, labels_k, "comparing_800k", "curls")
    curl_variance_plot()

def make_plots(data, labels, name, test):
    fig, ax = plt.subplots(figsize=(15, 9))

    ax.boxplot(
        data, 
        positions=np.arange(1, len(labels) + 1), 
        showmeans=True, 
        meanline=False, 
        medianprops=dict(linestyle='-', linewidth=2.5, color='purple'), 
        meanprops=dict(marker='o', markerfacecolor='blue', markersize=10)
    )
    ax.set_xticklabels(labels, fontsize=35)
    ax.tick_params(axis='both', which='major', labelsize=20)
    ax.set_ylabel(test + " Average", fontsize=30)
    ax.grid(axis='y')

    plt.savefig("figures/" + test + "/" + name + ".jpeg", dpi=300)
    plt.close()


def ping_variance_plot():
    datasets = []

    for data in pings_data_50k:
        datasets.append(np.array(data).astype(float))
    for data in pings_data_300k:
        datasets.append(np.array(data).astype(float))
    for data in pings_data_800k:
        datasets.append(np.array(data).astype(float))

    iqr_values = [np.percentile(data, 75) - np.percentile(data, 25) for data in datasets]

    fig, ax = plt.subplots(figsize=(12, 6))

    colors = ['#0072B2', '#D55E00', '#009E73']
    for i in range(0, 21, 3):
        x = np.array([i, i + 1, i + 2])
        y = np.array([iqr_values[i], iqr_values[i + 1], iqr_values[i + 2]])
        ax.bar(x, y, color=colors)
        border1 = Rectangle((i - 0.5, 0), 0, 160, edgecolor='black', lw=2)
        border2 = Rectangle((i + 2.5, 0), 0, 160, edgecolor='black', lw=2)
        ax.add_patch(border1)
        ax.add_patch(border2)
        
    ax.set_xlim([-1, 21])
    ax.set_xticks(np.arange(0, 21, 3) + 1)
    ax.set_xticklabels(labels_k, fontsize=12)
    ax.tick_params(axis='x', length=0)
    ax.set_ylabel("Interquartile Range", fontsize=20)

    plt.tight_layout()
    plt.show()
    plt.savefig("figures/pings/IQR.jpeg")
    plt.close()

def domainnames_variance_plot():
    datasets = []

    for data in domainnames_data_50k:
        datasets.append(np.array(data).astype(float))
    for data in domainnames_data_300k:
        datasets.append(np.array(data).astype(float))
    for data in domainnames_data_800k:
        datasets.append(np.array(data).astype(float))

    iqr_values = [np.percentile(data, 75) - np.percentile(data, 25) for data in datasets]

    fig, ax = plt.subplots(figsize=(12, 6))

    colors = ['#0072B2', '#D55E00', '#009E73']
    for i in range(0, 21, 3):
        x = np.array([i, i + 1, i + 2])
        y = np.array([iqr_values[i], iqr_values[i + 1], iqr_values[i + 2]])
        ax.bar(x, y, color=colors)
        border1 = Rectangle((i - 0.5, 0), 0, 300, edgecolor='black', lw=2)
        border2 = Rectangle((i + 2.5, 0), 0, 300, edgecolor='black', lw=2)
        ax.add_patch(border1)
        ax.add_patch(border2)
        
    ax.set_xlim([-1, 21])
    ax.set_xticks(np.arange(0, 21, 3) + 1)
    ax.set_xticklabels(labels_k, fontsize=12)
    ax.tick_params(axis='x', length=0)
    ax.set_ylabel("Interquartile Range", fontsize=20)

    plt.tight_layout()
    plt.show()
    plt.savefig("figures/domainlookups/IQR.jpeg")
    plt.close()

def curl_variance_plot():
    datasets = []

    for data in curls_data_50k:
        datasets.append(np.array(data).astype(float))
    for data in curls_data_300k:
        datasets.append(np.array(data).astype(float))
    for data in curls_data_800k:
        datasets.append(np.array(data).astype(float))

    iqr_values = [np.percentile(data, 75) - np.percentile(data, 25) for data in datasets]

    fig, ax = plt.subplots(figsize=(12, 6))

    colors = ['#0072B2', '#D55E00', '#009E73']
    for i in range(0, 21, 3):
        x = np.array([i, i + 1, i + 2])
        y = np.array([iqr_values[i], iqr_values[i + 1], iqr_values[i + 2]])
        ax.bar(x, y, color=colors)
        border1 = Rectangle((i - 0.5, 0), 0, 0.4, edgecolor='black', lw=2)
        border2 = Rectangle((i + 2.5, 0), 0, 0.4, edgecolor='black', lw=2)
        ax.add_patch(border1)
        ax.add_patch(border2)
        
    ax.set_xlim([-1, 21])
    ax.set_xticks(np.arange(0, 21, 3) + 1)
    ax.set_xticklabels(labels_k, fontsize=12)
    ax.tick_params(axis='x', length=0)
    ax.set_ylabel("Interquartile Range", fontsize=20)

    plt.tight_layout()
    plt.show()
    plt.savefig("figures/curls/IQR.jpeg")
    plt.close()

get_pings()
get_domainlookups()
get_curls()