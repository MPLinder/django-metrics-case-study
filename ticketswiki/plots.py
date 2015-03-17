import csv

import numpy
import pylab
import matplotlib.pyplot as plt


def pareto(path):
    limit = 30
    fig = plt.figure(figsize=(12,10))
    reader = csv.reader(open(path))
    counts, labels = zip(*reader)
    counts = map(int, counts)
    origcounts = counts
    counts = numpy.array(counts)[:limit]
    labels = labels[:limit]

    fig.subplots_adjust(bottom=0.3)

    for x, count in enumerate(counts):
        plt.bar(x+1, count, align='center')
    ax1 = fig.add_subplot(111)
    ax1.set_ylabel('Number of tickets')
    ax1.set_xlabel("Component")
    ax1.set_xbound(upper=limit+1)



    ax1.set_xticks(numpy.arange(limit+1))
    ax1.set_xticklabels([''] + list(labels), rotation=90, size='small')

    ax2 = ax1.twinx()
    ax2.set_ylabel('Cumulative Percent')
    total = sum(origcounts)
    running = 0
    percents = []
    for count in counts:
        running += count
        percents.append(float(running)/total*100)

    ax2.plot(numpy.arange(limit)+1, percents, 'go-', linewidth=2)
    ax2.set_xbound(upper=limit+1)
    ax2.set_ylim(ymin=0)
    ax2.set_yticks(range(0, 101, 10))
    ax2.set_xticks(numpy.arange(limit+1))
    ax2.set_xticklabels([''] + list(labels), rotation=90, size='small')


    plt.title("Tickets by (top %s) Components" % limit)
    plt.savefig("pareto_top%s.png" % limit)
    return


if __name__ == "__main__":
    pareto('comp_counts.csv')
