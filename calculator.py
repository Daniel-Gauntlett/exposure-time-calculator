import mathfunctions
import math
pi = 3.1415926535897932384626
e = 2.718281828459
c = 3 * 10 ** 10

def normalize(star_template,star_mag,wavelengthunit,energyunit,zeropoint):
    star_input = []
    starx = []
    stary = []
    starpairs = []
    with open(star_template, 'r') as curve:
        for line in curve:
            if len(line.strip()) > 0 and line.strip()[0] not in ["#", '"', "-"]:
                if line[-1] == '\n':
                    end = -1
                else:
                    end = len(line)
                star_input.append(list(filter(lambda num: num != "", line[0:end].split(" "))))
                starx.append(float(star_input[-1][0]))
                stary.append(float(star_input[-1][1]))
                starpairs.append((starx[-1] * wavelengthunit,stary[-1] * energyunit))
    
    scaled = [(starpairs[i][0], starpairs[i][1] * 10 ** ((star_mag - (- 2.5 * math.log10(starpairs[i][1] * ((starpairs[i][0] ** 2) / c)) - zeropoint)) / -2.5)) for i in range(len(starpairs))]
    return scaled

def starfilter(starpairs,starfilter,filterunit):
    # read in sed filter
    sed_input = []
    sedx = []
    sedy = []
    sed_pairs = []
    with open(starfilter, 'r') as sed:
        for line in sed:
            if len(line.strip()) > 0 and line.strip()[0] not in ["#", '"', "-"]:
                if line[-1] == '\n':
                    end = -1
                else:
                    end = len(line)
                sed_input.append(list(filter(lambda num: num != "", line[0:end].split(" "))))
                sedx.append(float(sed_input[-1][0]))
                sedy.append(float(sed_input[-1][1]))
                sed_pairs.append((sedx[-1] * filterunit,sedy[-1]))

    # interpolate star_pairs over v filter for proper multiplication
    interpolated = mathfunctions.interpolate(starpairs, [pair[0] for pair in sed_pairs])
    flux = mathfunctions.integrate([(interpolated[i][0], interpolated[i][1] * sed_pairs[i][1]) for i in range(len(interpolated))], sed_pairs[0][0], sed_pairs[-1][0])
    return flux

def extinction_correction(k, airmass):
    return 10 ** (k * airmass / -2.5)

def aperture_fraction(radius, FWHM):
    return 1 - e ** (0 - (radius ** 2) / (2 * (FWHM/2.35) ** 2))

def area(diameter):
    return (pi * diameter / 4) ** 2

def main():
    config = open("config.txt")
    settings = {}
    for line in config:
        if line[0] != "#" and len(line) > 1:
            templine = line.strip().split("=")
            try:
                if not templine[0] in ["filter", "star_template"]:
                    settings[templine[0]] = eval(templine[1])
                else:
                    settings[templine[0]] = templine[1]
            except:
                settings[templine[0]] = templine[1]
    # step 1: normalize template
    template = normalize(settings["star_template"],settings["target_mag"],settings["star_wavelength_unit"],settings["star_energy_unit"],settings["zero_point"])
    # step 2: filter
    flux = starfilter(template,settings["filter"],settings["filter_wavelength_unit"])
    # step 3: extinction correction
    ext_corr = extinction_correction(settings["k"],settings["airmass"])
    # step 4: fraction in aperture
    if settings["target_profile"] == "point":
        fwhm = settings["seeing"]
    elif settings["target_profile"] == "extend":
        fwhm = settings["fwhm"]
    else:
        print("Error: invalid profile provided.")
        return
    aper_frac = aperture_fraction(settings["diameter"] / 2, fwhm)
    # step 5: QE
    qe = settings["QE"]
    # step 6: telescope area
    telescope_area = area(settings["diameter"])
    nstar = flux * ext_corr * aper_frac * qe * telescope_area
    nd = settings["dark_current"]
    npix = pi * ((0.67 * fwhm / settings["pixel_scale"]) ** 2)
    ns = settings["background_noise"]
    nrd = settings["ccd"]
    if settings["mode"] == "E":
        mode = "exposure time"
        s = settings["signal_noise_ratio"]
        output = (s ** 2 * (npix * nd + npix * ns + nstar) + math.sqrt((s ** 2 * (npix * nd + npix * ns + nstar)) ** 2 - 4 * nstar ** 2 * s ** 2 * npix * nrd ** 2)) / (2 * nstar ** 2)
    elif settings["mode"] == "S/N":
        mode = "signal to noise ratio"
        t = settings["exposure_time"]
        output = nstar * t / (math.sqrt(nstar * t + npix * (ns * t + nd * t + nrd ** 2)))
    else:
        print("Error: invalid mode provided.")
        return
    print("Your final " + mode + " is:" + str(output))
    return output

main()

