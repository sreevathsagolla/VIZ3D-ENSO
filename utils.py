import plotly.graph_objects as go
import numpy as np

def interactive_3d_plotter(ds, var_name = 'con_temperature', lon_varname = 'lon',
                           lat_varname = 'lat', mask_bounds = [-1.5,1.5], mask = False,
                           cbar_range = [-2,2], title = 'EN4', depth_varname = 'depth'):
    lons, lats = np.meshgrid(ds[lon_varname], ds[lat_varname])
    x = np.stack([lons.transpose()]*ds[depth_varname].shape[0], axis = 2)
    y = np.stack([lats.transpose()]*ds[depth_varname].shape[0], axis = 2)
    z = np.stack([-ds[depth_varname]]*x.shape[0]*x.shape[1], axis = 0)
    z = z.reshape(x.shape[0],x.shape[1],x.shape[2])
    mid_point = (0-cbar_range[0])/(cbar_range[1]-cbar_range[0])

    x = np.where(np.isnan(x), 0, x)
    y = np.where(np.isnan(x), 0, y)
    z = np.where(np.isnan(x), 0, z)

    temperatures = np.swapaxes(ds[var_name].values.squeeze(), 0, -1)

    if mask == True:
        temperatures = np.where((temperatures >= mask_bounds[0])
        & (temperatures <= mask_bounds[1]), np.nan, temperatures)

    fig = go.Figure(data=go.Volume(
        x=x.flatten(),
        y=y.flatten(),
        z=z.flatten(),
        value=temperatures.flatten(),
        isomin=cbar_range[0],
        isomax=cbar_range[1],
        opacity=0.1, # max opacity
        opacityscale=[[-0.5, 1], [-0.2, 0], [0.2, 0], [0.5, 1]],
        surface_count=21,
        colorscale='RdBu_r',
        cmid=0,
        ))
    fig.update_layout(plot_bgcolor='white',paper_bgcolor = 'white',
                      title = {
                            'text': title,
                            'y':0.98, # new
                            'x':0.5,
                            'xanchor': 'center',
                            'yanchor': 'top' # new
                            },
                      scene = dict(
                          xaxis_title='Longitude',
                          yaxis_title='Latitude',
                          zaxis_title='Depth (m)'),
                      width=700,
                      margin=dict(r=20, b=10, l=10, t=10),)
    #fig.show()
    return fig

def renamer(ds_f):
    if 'deptht' in list(ds_f.coords):
        ds_f = ds_f.rename({'deptht':'depth'})
    if 'lev' in list(ds_f.coords):
        ds_f = ds_f.rename({'lev':'depth'})
    if 'longitude' in list(ds_f.coords):
        ds_f = ds_f.rename({'longitude':'lon', 'latitude':'lat'})
        ds_f = ds_f.rename({'i':'x', 'j':'y'})
    if 'y_2' in list(ds_f.dims):
        ds_f = ds_f.rename({'x_2':'x','y_2':'y'})
    if 'time_counter' in list(ds_f.coords):
        ds_f = ds_f.rename({'time_counter':'time'})
    return ds_f
