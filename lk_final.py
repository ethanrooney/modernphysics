#!/bin/bash/python

from lightkurve import log, KeplerTargetPixelFile, Periodogram
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import astropy.units as u
from scipy import signal
log.setLevel('WARNING')  # Ignore download messages

#This pandas Data frame contains the objects of interest to analize in a cvs
df = pd.read_csv('koi.csv', header=0) 
exodata = [] 
#The analisis can be run on any number of objects in the Relevent table here I select what value to check
n=100
for a in range(n):
    # kepid is the header of the relevent column for extracting a Kepler ID
    star= df['kepid'][a]
    # Loop over all of the quarters of data for a given Kepler ID
    for i in range(17):
        #This handles any server timeout errors with out quitting, additionally if the object doesn't exist, it will inform and continue.
        try:
            # This function will be removed from lightkuve soon.
            # This function takes input for a kepler objest and quarter, applies a bitmask to it and turns it into a Target Pixel File. If the required data is stored locally than the it uses the local copy. Otherwise it queries the NASA MAST server to download.
            tpf = KeplerTargetPixelFile.from_archive(star, quarter=i, quality_bitmask='hardest');
        #Permit keyboard interupt from being gobbled up by the try error handling
        except KeyboardInterrupt:
            raise
        # on any error other than Keyboard interrupt, informs if Data requested is unavailable.
        except:
            print('no data for {0} quarter {1}'.format(str(star), i))
        #If no error getting TPF Begins analysis of the TPF
        else:
            print('analysing star {0} quarter {1} \n {2} of {3}'.format(str(star),i,(a)*18 + i+1, n*18))
            #converts the postage stamp of kepler data to a lightcurve
            lc = tpf.to_lightcurve(aperture_mask='all'); 
            lc = lc.remove_nans().remove_outliers(sigma_upper=3, sigma_lower=10)
            #Applies a default flattening function to the light curve to removce systemic changes like drift from the curve
            lc_flat = lc.flatten().remove_nans()
            #Allows for easy referance to the time and flux
            time, flux = lc_flat.time, lc_flat.flux 
            #find the diff between min and max flux and if it is big enough do something with it.
            delta_flat = ((np.mean(flux)-min(flux))/np.mean(flux))
            print(delta_flat)
            # If the diffence between the max and min in the flattened curve is more than 0.5% we want to look more closely at the data. For that we might want to look at the raw data.
            if 0.5 > delta_flat > 0.003:
                #Preserves the original light curve for further observation
                lc.plot()
                #outputs to file with the name and quarter of the object
                plt.savefig('raw/{0}_quarter_{1}_raw.png'.format(str(star), i))
                #Same thing but for the flattened curve
                lc_flat.plot(linestyle='solid');
                plt.savefig('flat/{0}_quarter_{1}_flat.png'.format(str(star), i))
                #Outputs a periodogram for observation
                p = lc_flat.to_periodogram(min_period=1, max_period=90,oversample_factor=8).to_table()
                
                periodarray = signal.find_peaks(p, distance=2)
                plt.savefig('periodogram/{0}_quarter_{1}.png'.format(str(star),i))
                for period in periodarray:
                        lc_flat.fold(period.value).scatter();
                        plt.title(period)
                        plt.savefig('fold/{0}_quarter_{1}'.format(str(star), i, period))
                        plt.close()
                        exodata.append([star,i,delta_flat,period,lower,upper])
                    
                plt.close('all')
print(exodata)
