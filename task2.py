import matplotlib.pyplot as pyplot
import mathfunctions

sed_filter = 'Vega_SED.dat'

v_curve = 'scidoc1534.txt'

h = 6.6 * (10 ** -27) # in ergs * s

c = 3 * (10 ** 18) # in angstroms / s

sed_input = []

sedx = []
sedy = []

sed_pairs = []

# read in sed filter

v_input = []
vx = []
vy = []
v_pairs = []

# read in v filter

with open(v_curve, 'r') as curve:
    for line in curve:
        if line[0] != '#':
            if line[-1] == '\n':
                end = -1
            else:
                end = len(line)
            v_input.append(list(filter(lambda num: num != "", line[0:end].split(" "))))
            vx.append(float(v_input[-1][0]) * 10)
            vy.append(float(v_input[-1][1]) / 100)
            v_pairs.append((vx[-1],vy[-1]))

# create ab filter zero point

interpolated = [(i, 3.63 * (10 ** -20) * c / (i ** 2)) for i in vx]

# integrate

flux = mathfunctions.integrate([(interpolated[i][0], interpolated[i][1] * vy[i]) for i in range(len(v_pairs))], vx[0], vx[-1])
print(flux)


# instead get photon number
photonnumber = mathfunctions.integrate([(interpolated[i][0], interpolated[i][1] * vy[i] / (h * c / (interpolated[i][0]))) for i in range(len(v_pairs))], vx[0], vx[-1])
print(photonnumber)