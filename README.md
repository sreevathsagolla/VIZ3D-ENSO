# VIZ3D-ENSO (BETA version)
3-D visualization dashboard for ENSO composites from coupled and ocean-only model simulations.<br><br>

To install required packages:
```pip install numpy tqdm xarray dash```


To run the dashboard:
```python3 dashboard.py```

Open the link on the browser of your choice.
<br><br>
**Dropdown options**:
1. Event Type: EL_NINO, LA_NINA
2. Time Period: 1976-2023, 1950-2023, 1950-2050
3. Composite: Observations + NPD Runs  + CMIP6 HighResMIP Runs

For the sake of dashboard responsiveness, composites have been **interpolated to 1˚x1˚ horizontal resolution and evenly spaced 10m depth levels**.
