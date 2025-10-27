import math
import matplotlib.pyplot as pyplot

vega_m_vega = 0
alt_m_vega = 28

scale_factor = 10 ** ((alt_m_vega - vega_m_vega) / -2.5)
print(scale_factor)

sed_filter = 'Vega_SED.dat'

sed_input = []

sedx = []
sedy = []

sed_pairs = []

# read in sed filter

with open(sed_filter, 'r') as sed:
    for line in sed:
        if line[0] != '#':
            if line[-1] == '\n':
                end = -1
            else:
                end = len(line)
            sed_input.append(list(filter(lambda num: num != "", line[0:end].split(" "))))
            sedx.append(float(sed_input[-1][0]))
            sedy.append(float(sed_input[-1][1]))
            sed_pairs.append((sedx[-1],sedy[-1]))

scale_for_ab = [(i[0], 10 ** ((28 - (2.5 * math.log(i[1], 10) - 48.6)) / -2.5)) for i in sed_pairs]

pyplot.plot([x[0] for x in scale_for_ab],[y[1] for y in scale_for_ab])
pyplot.xscale('log')
pyplot.yscale('log')
pyplot.show()