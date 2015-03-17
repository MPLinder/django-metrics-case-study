import csv
from collections import Counter




def parse():
    reader = csv.reader(open('metrics_ticket.csv', 'r'))
    # Skip first row.
    reader.next()
    c = Counter(row[9] for row in reader)
    writer = csv.writer(open('comp_counts.csv', 'w'), delimiter='\t')
    for label, num in c.most_common():
        writer.writerow((num, label))


if __name__ == "__main__":
   parse()

