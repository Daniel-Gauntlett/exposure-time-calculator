Provide the settings in the config file, and run the program from the command line (or in any other way where it won't immediately close) to get an output.

ALL units must match the ones in this document. The only exception is the files, since those are often harder to convert. Instead, you will provide the units in the config there.

However, as eval is ran on the values here, you can provide mathematical expressions and they will work! (Check all config files before running, however, to avoid running of unwanted code. DO NOT run with a config file you haven't read through.)
For example, you can do expressions in python notation: 5 * 10 ** -9 will evaluate to 5 * 10^9. Do this for your unit conversion.

Fields:

mode: either E, if you are calculating exposure time, or S/N, if you are calculating signal-to-noise ratio.
signal_noise_ratio: The desired signal-to-noise ratio. Unused, and thus optional, if mode is S/N. No unit.
exposure_time: The desired exposure time. Unused, and thus optional, if mode is E. Unit is seconds.
target_mag: The magnitude of the object you're observing in the magnitude system.
zero_point: The zero-point of the magnitude system you're using.
target_profile: Either point or extend, this determines the radial profile of your object.
fwhm: The full-width-half-maximum. Only used if target_profile is extend. Units should be SI.
seeing: The seeing. Only used if target_profile is point. Units should be SI.
airmass: The observation's airmass. Always used. Standard units.

background_noise: Noise per pixel. Uses SI units.

star_template: The SED profile for your star. 
star_wavelength_unit and star_energy_unit: The units provided in the file compared to SI units.
filter: The filter file for your star.
filter_wavelength_unit: The wavelength unit for your star, relative to SI units.

filter_set: The filter set being used.
pixel_scale: The pixel scale in radians. 
QE: The quantum efficiency. A percent.
dark_current: The dark current. Electrons per pixel per second.
diameter: The diameter of the mirror. SI units.
ccd: The efficiency of the CCD. A percent.
k: The k constant in airmass. Standard units.