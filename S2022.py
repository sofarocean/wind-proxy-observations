"""The purpose of this file is to illustrate how to process Spotter wave spectra to calculate wind speed using the
S2022 (Shimura et al. 2022) method in Dorsay et al. 2023."""

from datetime import datetime, timezone
from roguewave import get_spotter_data, load
from roguewave.wavephysics.windestimate import estimate_u10_from_spectrum
import matplotlib.pyplot as plt
import pandas as pd

spotter_id = "SPOT-010340"

### Define method parameters
s2022_params = load('s3://sofar-wx-data-dev-os1/proxy_wind/calibration/final_calibration_peak_weighted=True.zip')
methods_to_plot = {
    'peak': {
        'method': 'peak',
        'params': s2022_params,
        'recalc': False
    }
}

### Get Spotter data, output format pandas DataFrame
wave_spectra = load('./data/SPOT-010340_spectra_1d')

### Calculate wind estimates for 1 month of Spotter data along Spotter's track
wind_estimate = estimate_u10_from_spectrum(spectrum=wave_spectra,
                                           method=methods_to_plot['peak']['method'],
                                           **methods_to_plot['peak']['params']) # spectra needs to be 1D


### Plot output
fig, axs = plt.subplots(nrows=1,
                        ncols=1,
                        figsize=(14, 10))
fig.suptitle(f'{spotter_id} wind estimates from S2022: '
             f'{pd.to_datetime(wind_estimate.time.values[0]).month}/{pd.to_datetime(wind_estimate.time.values[0]).day}/'
             f'{pd.to_datetime(wind_estimate.time.values[0]).year} - '
             f'{pd.to_datetime(wind_estimate.time.values[-1]).month}/{pd.to_datetime(wind_estimate.time.values[-1]).day}/'
             f'{pd.to_datetime(wind_estimate.time.values[-1]).year}',
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


