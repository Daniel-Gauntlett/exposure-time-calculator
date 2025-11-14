import mathfunctions
import math
pi = 3.1415926535897932384626
e = 2.718281828459

def normalize(star,vega,star_mag):
    star_input = []
    starx = []
    stary = []
    starpairs = []
    with open(star, 'r') as curve:
        for line in curve:
            if len(line.strip()) > 0 and line.strip()[0] not in ["#", '"', "-"]:
                if line[-1] == '\n':
                    end = -1
                else:
                    end = len(line)
                star_input.append(list(filter(lambda num: num != "", line[0:end].split(" "))))
                starx.append(float(star_input[-1][0]))
                stary.append(float(star_input[-1][1]) / 100)
                starpairs.append((starx[-1],stary[-1]))
    vega_input = []
    vegax = []
    vegay = []
    vegapairs = []
    with open(vega, 'r') as curve:
        for line in curve:
            if len(line.strip()) > 0 and line.strip()[0] not in ["#", '"', "-"]:
                if line[-1] == '\n':
                    end = -1
                else:
                    end = len(line)
                vega_input.append(list(filter(lambda num: num != "", line[0:end].split(" "))))
                vegax.append(float(vega_input[-1][0]))
                vegay.append(float(vega_input[-1][1]) / 100)
                vegapairs.append((vegax[-1],vegay[-1]))
    vegainterped = mathfunctions.interpolate(vegapairs, [pair[0] for pair in starpairs])
    scaled = [(starpairs[i][0], 10 ** ((vegainterped[i][1] - star_mag) / -2.5)) for i in range(len(starpairs))]
    return scaled
    

def starfilter(starpairs,starfilter):
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
                sed_pairs.append((sedx[-1],sedy[-1]))

    # interpolate sed_pairs over v filter for proper multiplication

    interpolated = mathfunctions.interpolate(sed_pairs, [pair[0] for pair in starpairs])

    flux = mathfunctions.integrate([(interpolated[i][0], interpolated[i][1] * starpairs[i][1]) for i in range(len(starpairs))], starpairs[0][0], starpairs[-1][0])
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
                if not templine[0] in ["filter", "vega_template", "star_template"]:
                    settings[templine[0]] = eval(templine[1])
                else:
                    settings[templine[0]] = templine[1]
            except:
                settings[templine[0]] = templine[1]
    # step 1: normalize template
    template = normalize(settings["star_template"],settings["vega_template"],settings["target_mag"])
    # step 2: filter
    flux = starfilter(template,settings["filter"])
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
        output = (s ** 2 * (npix * nd + npix * ns + nstar) * t + math.sqrt((s ** 2 * (npix * nd + npix * ns + nstar) * t) ** 2 - 4 * nstar ** 2 * s ** 2 * npix * nrd ** 2)) / (2 * nstar ** 2)
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

