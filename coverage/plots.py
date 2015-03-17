import numpy
import pylab

import matplotlib.pyplot as plt


def select(data, ignore_empty):
    if ignore_empty:
        select = data[:,1] > 0
    else:
        select = numpy.ones(len(data))
    return select


def histogram(path, cumulative=False, ignore_empty=True):
    fig = plt.figure()
    data = numpy.genfromtxt(path)
    plt.hist(data[select(data, ignore_empty), 3], bins=20, range=(0,100), cumulative=cumulative)
    title = "The %s distribution of percent line coverage per module" % ('cumulative' if cumulative else '')
    if ignore_empty:
        title += "\n(ignoring zero length modules)"
    plt.title(title)
    plt.xlabel("Percent line coverage")
    plt.ylabel("Number of modules")
    plt.xticks(range(0, 101, 10))
    plt.grid(True)

    name = 'hist'
    if cumulative:
        name += '_cumulative'
    plt.savefig("plots/%s.png" % name)


def pie(path, split=95):
    fig = plt.figure(figsize=(8,8))
    data = numpy.genfromtxt(path)
    non_empty = data[select(data, True)]
    num_above_split = sum(non_empty[:,3] >= split)
    num_below_split = len(non_empty) - num_above_split
    if split == 100:
        labels = ['less than %s%%' % split, '100%']
    else:
        labels = ['less than %s%%' % split, '%s%% or greater' % split]
    plt.pie([num_below_split, num_above_split],
            labels=labels,
            colors=['red', 'green'],
            explode=[0.05, 0],
            autopct='%1.1f%%',
            shadow=True,
    )
    title = "Modules with line coverage\n%s/under %s%%" % ('at' if split == 100 else 'over', split)
    plt.title(title)
    plt.savefig("plots/pie_%s.png" % split)


def trend(path):
    from datetime import date
    fig = plt.figure(figsize=(10,8))
    data = numpy.genfromtxt('covtrend.txt')
    dates = [date(year=int(year), month=int(month), day=int(day)) for month, day, year in data[:,:3]]
    percents = data[:,-1]
    plt.plot_date(dates, percents, 'go-', label='coverage', linewidth=2)
    plt.xlabel("Date")
    plt.ylabel("Percent line coverage")
    plt.title("Trend of percent line coverage, from run of unit test suite\n(major releases marked with vertical lines)")
    plt.yticks(range(0, 101, 10))
    plt.xticks(size='small')
    plt.grid(True)
    plot_releases(dates)
    plt.savefig("plots/trend.png")


def plot_releases(dates=None):
    """Plot vertical lines at major release dates.

    If dates is given, it should be a list of dates, in order.  If given,
    only releases that fall between the first and last dates will be rendered.
    """
    from datetime import date, timedelta
    data = numpy.genfromtxt('releases.txt')
    releases = [date(year=int(year), month=int(month), day=int(day)) for month, day, year in data[:,:3]]
    release_names = [items.split()[3] for items in open('releases.txt').readlines()]
    for release, name in zip(releases, release_names):
        if release >= dates[0] and release <= dates[-1]:
            plt.axvline(release, linewidth=2)
            plt.annotate("%s\nrelease" % name, (release + timedelta(days=15), 23))
    

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        sys.exit("Script takes exactly one argument, which should be the path to a cleaned coverage.py report file.")
    path = sys.argv[1]
    histogram(path, False, True)
    histogram(path, True, True)
    pie(path)
    pie(path, split=100)
    trend('covtrend.txt')

