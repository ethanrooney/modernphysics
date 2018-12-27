#!/bin/bash/python
from lightkurve import KeplerTargetPixelFile
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
star = 757076
tpf = KeplerTargetPixelFile.from_fits(kplr008462852-2013098041711_lpd-targ.fits.gz);
lc = tpf.to_lightcurve(aperture_mask='all'); #this takes takes all of the data on the postage stamp sums it and puts it into a light curve
lc.time, lc.flux #what is the data structure here?
#find the diff between min and max flux and if it is big enough do something with it.
delta = (max(lc.flux) - min (lc.flux))/np.mean(lc.flux)
if delta > 0.05:
    lc.plot(linestyle='solid');
    plt.savefig('{0}_quarter_{1}.png'.format(str(star), i))
    print(lc, 'is being plotted.')
