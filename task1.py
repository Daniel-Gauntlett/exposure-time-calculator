import matplotlib.pyplot as pyplot
import mathfunctions

sed_filter = 'Vega_SED.dat'

v_curve = 'kp1465'

h = 6.6 * (10 ** -27) # in ergs * s

c = 3 * (10 ** 18) # in angstroms / s

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

v_input = []
vx = []
vy = []
v_pairs = []

# read in v filter

with open(v_curve, 'r') as curve:
    for line in curve:
        if line[0] == ' ' and len(line) > 2 and line[1] != '"' and line[2] != '-':
            if line[-1] == '\n':
                end = -1
            else:
                end = len(line)
            v_input.append(list(filter(lambda num: num != "", line[0:end].split(" "))))
            vx.append(float(v_input[-1][0]))
            vy.append(float(v_input[-1][1]) / 100)
            v_pairs.append((vx[-1],vy[-1]))

# interpolate sed_pairs over v filter for proper multiplication

interpolated = mathfunctions.interpolate(sed_pairs, [pair[0] for pair in v_pairs])

# actually plot. interpolation done earlier for testing (commented line also for testing)

fig = pyplot.figure()
plot1 = fig.add_subplot(111)                
plot1.plot(sedx,sedy)
plot1.plot(vx,vy)
#plot1.plot([pair[0] for pair in interpolated],[pair[1] for pair in interpolated])
plot1.set_xlim(vx[0],vx[-1])
plot1.set_ylim(10 ** -10, 1)
pyplot.xscale('log')
pyplot.yscale('log')
pyplot.show()

# integrate

flux = mathfunctions.integrate([(interpolated[i][0], interpolated[i][1] * vy[i]) for i in range(len(v_pairs))], vx[0], vx[-1])
print(flux)


# instead get photon number
photonnumber = mathfunctions.integrate(
    [(interpolated[i][0], interpolated[i][1] * v_pairs[i][1] / (h * c / (interpolated[i][0]))) for i in range(len(v_pairs))], 
    v_pairs[0][0], v_pairs[-1][0])
print(photonnumber)