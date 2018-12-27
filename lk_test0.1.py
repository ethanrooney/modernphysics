#!/bin/bash/python
from lightkurve import KeplerTargetPixelFile
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

df = pd.read_csv('koi.csv', header=0) 
for a in range(30):
    star = df['kepid'][a]
        for i in range(17):
            #function checks the local folder for the data if it doesn't find it, it downloads it from NASA's FTP server
            try:
                tpf = KeplerTargetPixelFile.from_archive(star, quarter=i, quality_bitmask='hardest');
            except:
                print('no data for {0} quarter {1}'.format(str(star), i))
            else:
                print('analysing star {0} quarter {1}'.format(str(star),i))
                #converts the postage stamp of kepler data to a lightcurve
                lc = tpf.to_lightcurve(aperture_mask='all'); 
                #Applies a default flattening function to the light curve to removce systemic changes like drift from the curve
                lc_flat = lc.flatten()
                time, flux = lc_flat.time, lc_flat.flux #what is the data structure here?
                #find the diff between min and max flux and if it is big enough do something with it.
                delta_flat = ((max(flux)-min(flux))/np.mean(flux))
                # If the diffence between the max and min in the flattened curve is more than 1% we want to look more closely at the data. For that we might want to look at the raw data.
                if delta_flat > 0.01:
                    lc.plot()
                    plt.savefig('raw/{0}_quarter_{1}_uncorrected.png'.format(str(star), i))
                    lc_flat.plot(linestyle='solid');
                    plt.savefig('flat/{0}_quarter_{1}_flat.png'.format(str(star), i))
                    try:
                        p = lc_flat.to_periodogram(min_period=5*u.day, max_period=50*u.day, oversample_factor=10)
                        p.plot(format='period', scale='log')
                        plt.savefig('periodogram/{0}_quarter_{1}'.format(str(star),i))
                        period = p.period_at_max_power
                        print('Best period: {}'.format(period))
                        lc_flat.fold(period.value).scatter();
                        plt.savefig('fold/{0}_quarter_{1}'.format(str(star), i))
                    except:
                        print('periodogram isnt doing what you want')
                    plt.close('all')   

