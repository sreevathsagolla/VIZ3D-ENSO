import numpy as np
from tqdm import tqdm
import glob
import os
import xarray as xr
from utils import renamer, interactive_3d_plotter

for f in tqdm(glob.glob('./data/composites/*.nc')):
    try:
        ds = renamer(xr.open_dataset(f))
        ds = ds.sel(depth = slice(0,240), lon = slice(160,275), lat = slice(-20,20))
        ds = ds.interp(depth = np.arange(0,250,10))
        cbar_range = [(np.nanmean(ds.anomaly)-2*np.nanstd(ds.anomaly)).round(2), (np.nanmean(ds.anomaly)+2*np.nanstd(ds.anomaly)).round(2)]
        mask_range = [(np.nanmean(ds.anomaly)-1*np.nanstd(ds.anomaly)).round(2), (np.nanmean(ds.anomaly)+1*np.nanstd(ds.anomaly)).round(2)]
        title = os.path.basename(f).split('COMPOSITE_')[1][:-13]
        fig = interactive_3d_plotter(ds, var_name = 'anomaly', mask_bounds = mask_range, mask = True, cbar_range = cbar_range, title = title)
        html_output = fig.to_html(full_html=True)
        with open(f.replace('composites','plots')[:-3]+'.html', "w") as f:
            f.write(html_output)
        del fig
    except:
        print('ERROR: Failed to create '+f)
