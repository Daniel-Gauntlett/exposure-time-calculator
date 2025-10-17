import matplotlib.pyplot as pyplot

sed_filter = 'Vega_SED.dat'

pairs = []

x = []
y = []

with open(sed_filter, 'r') as sed:
    for line in sed:
        if line[0] != '#':
            if line[-1] == '\n':
                end = -1
            else:
                end = len(line)
            pairs.append(list(filter(lambda num: num != "", line[0:end].split(" "))))
            x.append(float(pairs[-1][0]))
            y.append(float(pairs[-1][1]))

pyplot.scatter(x,y,s=0.2)
pyplot.xscale('log')
pyplot.yscale('log')
pyplot.show()