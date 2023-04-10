"""The purpose of this file is to illustrate how to process Spotter wave spectra to calculate wind speed using the
S2022 (Shimura et al. 2022) method in Dorsay et al. 2023."""

from roguewave import load
from roguewave.wavephysics.windestimate import estimate_u10_from_spectrum
import matplotlib.pyplot as plt
from datetime import datetime

spotter_id = "SPOT-010340"

### Define method parameters
params = load('./data/S2022_calibration.zip')

### Get Spotter data, output format pandas DataFrame
wave_spectra = load('./data/SPOT-010340_spectra_1d')

### Calculate wind estimates for 1 month of Spotter data along Spotter's track
wind_estimate = estimate_u10_from_spectrum(spectrum=wave_spectra,
                                           method='peak',
                                           **params) # spectra needs to be 1D
start_date = datetime.strptime(str(wind_estimate.time.values[0]), "%Y-%m-%dT%H:%M:%S.%f000")
end_date = datetime.strptime(str(wind_estimate.time.values[-1]), "%Y-%m-%dT%H:%M:%S.%f000")

### Plot output
fig, axs = plt.subplots(nrows=1,
                        ncols=1,
                        figsize=(14, 10))
fig.suptitle(f'{spotter_id} wind estimates from S2022: '
             f'{start_date.month}/{start_date.day}/{start_date.year} - '
             f'{end_date.month}/{end_date.day}{end_date.year}',
             fontsize=20)
fig.tight_layout()
axs.plot(wind_estimate['time'], wind_estimate['u10'], color='#020966')
axs.grid()
axs.set_xlabel('Time (UTC)', fontsize=16)
axs.set_ylabel('$U_{10}$ [m/s]', fontsize=16)
axs.set_xticks(axs.get_xticks(), axs.get_xticklabels(), rotation=45)
fig.subplots_adjust(top=0.92, bottom=0.12, left=0.08, right=0.92)
fig.savefig('./figures/S2022_wind_estimates.png', dpi=300)
plt.show()


