from matplotlib import pyplot as plt
import numpy as np

names = []
values = []

def add_to_lists():
    file = open("results-for-pi.txt", "r")
    lines = file.readlines()  
    other = 0  
    count = 0
    total = 800000
    for line in lines:
        if line.split("\n")[0].split(":")[1] == "Percent Matched":
            continue

        if count < 8:
            values.append(line.split("\n")[0].split(":")[0])
            names.append(line.split("\n")[0].split(":")[1])
            count += 1
        else:
            if not "Other" in names:
                names.append("Other")
            if line.split("\n")[0].split(":")[0].isnumeric():
                other += int(line.split("\n")[0].split(":")[0])
    values.append(other)
    file.close()

    for i in range(len(values)):
        names[i] = names[i] + ": " + str(round((int(values[i]) / total) * 100, 2)) + "%"

def plot_pi_chart():
    fig, ax = plt.subplots(figsize=(10, 7))
    colors = ["#808080", "#808080", "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b", "#e377c2"]

    wedges, texts = ax.pie(
        values,
        labels=names,
        startangle=90,
        colors=colors,
        wedgeprops={'linewidth': 1, 'edgecolor': 'black'},
        textprops={'fontsize': 12, 'fontweight': 'bold'}
    )

    plt.show()
    plt.savefig("figures/pi-chart.jpeg", dpi=300)


add_to_lists()
plot_pi_chart()