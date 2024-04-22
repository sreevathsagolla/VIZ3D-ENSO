import dash
from dash import dcc, html, Input, Output
import os
from itertools import product
import webbrowser
from threading import Timer

EVENTS = ['EL_NINO', 'LA_NINA']
TIME_PERIODS = ['1976-2023', '1950-2023', '1950-2050']

HIGHRESMIP_MODELS = ['CMCC-CM2-VHR4', 'CNRM-CM6-1-HR', 'EC-Earth3P-HR', 'HadGEM3-GC31-HH', 'MPI-ESM1-2-HR', 'MPI-ESM1-2-XR']
HIGHRESMIP_EXPTYPE = ['control', 'historical']
HIGHRESMIP_EXPS = [x[0]+'_'+x[1]+'_run' for x in product(HIGHRESMIP_MODELS, HIGHRESMIP_EXPTYPE)]

NPD_EXPS = ['eORCA025_ERA5', 'eORCA025_JRA55']
OBS = ['EN4', 'ORAS5']

app = dash.Dash(__name__) 

app.layout = html.Div([
    html.H1(children='VIZ3D-ENSO', style={'textAlign':'center'}),
    html.H2(children='A 3-D ENSO temperature anomalies visualizer', style={'textAlign':'center'}),
    dcc.Dropdown(
        id='event-dropdown',
        options=[{'label': event, 'value': event} for event in EVENTS],
        value=EVENTS[0]
    ),
    dcc.Dropdown(
        id='time-period-dropdown',
        options=[{'label': period, 'value': period} for period in TIME_PERIODS],
        value=TIME_PERIODS[0]
    ),
    dcc.Dropdown(
        id='exp-dropdown',
        options=[],
        value=''
    ),
    html.Div(id='plot-container')
])

@app.callback(
    Output(component_id='exp-dropdown', component_property='options'),
    Input(component_id='time-period-dropdown', component_property='value')
)
def update_exp_dropdown(time_period):
    if time_period == '1976-2023':
        options = NPD_EXPS + OBS + HIGHRESMIP_EXPS
    elif time_period == '1950-2023':
        options = ['EN4'] + HIGHRESMIP_EXPS
    else:
        options = HIGHRESMIP_EXPS
    return [{'label': exp, 'value': exp} for exp in options]

@app.callback(
    Output(component_id='plot-container', component_property='children'),
    Input(component_id='event-dropdown', component_property='value'),
    Input(component_id='time-period-dropdown', component_property='value'),
    Input(component_id='exp-dropdown', component_property='value')
)
def update_plot(event, time_period, exp):
    if not exp:
        return

    filename = f"./data/plots/INTERPOLATED_1deg_{event}_COMPOSITE_{exp}_{time_period}.html"
    if os.path.exists(filename):
        return html.Iframe(srcDoc=open(filename, 'r').read(), width='100%', height='500px')
    else:
        return "Plot file not found"

if __name__ == '__main__':
    app.run_server(debug=True)
