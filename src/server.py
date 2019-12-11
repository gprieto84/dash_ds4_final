import os
import utils_dash
import data
import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import pandas as pd
import plotly.graph_objs as go
from datetime import datetime
from dash.dependencies import Input, Output

mapbox_access_token = 'pk.eyJ1IjoiaXZhbm5pZXRvIiwiYSI6ImNqNTU0dHFrejBkZmoycW9hZTc5NW42OHEifQ._bi-c17fco0GQVetmZq0Hw'

app = dash.Dash(__name__,
                external_stylesheets=['https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-alpha.6/css/bootstrap.min.css'],
                 meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],)

server = app.server
server.secret_key = os.environ.get('secret_key', 'secret')

# Load the data
df = data.load_data()

bg_color = '#161A28'

# Get all valuable column headers
main_columns2 = { k:v for (k,v) in utils_dash.VALID_COLUMNS_DICT.items()}

def build_banner():
    return html.Div(
        id="banner",
        className="banner",
        children=[
            html.Div(
                id="banner-text",
                children=[
                    html.H6("Car Accidents in Barranquilla"),
                    html.P("Reports from public and private dataset from 2016-2018"),
                ],
            ),
            html.Div(
                id="banner-logo",
                children=[
                    html.Button(
                        id="learn-more-button", children="Team 3 Barranquilla"
                    ),
                    html.Img(src=app.get_asset_url("img/car.png")),
                ],
            ),
        ],
    )

def generate_section_banner(title):
    return html.Div(className="section-banner", children=title)

def generate_date_slider():
    return dcc.RangeSlider( id='date-slider', min=min(df['year']), max=max(df['year']),
                                marks={str(date): str(date) for date in df['year'].unique()},
                                value=[min(df['year']),max(df['year'])],allowCross=False )

def generate_chart(style, title, id):
    return html.Div( className=style,children=[dcc.Graph(id=id)])

def generate_dropdown(classDiv,classLabel,label,id, datalist,initial):
    return  html.Div( className=classDiv,
                        children=[
                            html.Label(className=classLabel, children=label),
                            html.Br(),
                            dcc.Dropdown(id=id,
                                options=sorted(datalist,key = lambda i: i['label'] ),
                                value=datalist[initial]['value'],
                            ),
                        ],
                    )

def generate_year_checklist():
    return dcc.Checklist(id='check-year',
            options=[{'label': i, 'value': i} for i in df['year'].unique()],
            value=[i for i in df['year'].unique()],
            labelStyle={'display': 'inline-block','font-size':'12px'}
    )

def generate_vehicle_checklist():
    return dcc.Checklist(id='check-car',
                options=[
                    {'label': 'Motorcycle', 'value': 'Motorcycle'},
                    {'label': 'Car', 'value': 'Car'},
                    {'label': 'SUV', 'value': 'Suv'},
                    {'label': 'Bus', 'value': 'Bus'},
                    {'label': 'Truck', 'value': 'Truck'},
                    {'label': 'Bycicle', 'value': 'Bycicle'},
                    {'label': 'Industrial', 'value': 'Industrial'},
                    {'label': 'Other Vehicle', 'value': 'Other'}
                ],
                value=['Motorcycle','Car','Suv','Bus','Truck','Bycicle','Industrial','Other'],
                labelStyle={'display': 'inline-block','font-size':'12px'}
            )

def generate_sev_checklist():
    return  dcc.Checklist(id='check-sev',
                                options=[
                                    {'label': 'Casualties', 'value': 'Casualties'},
                                    {'label': 'Wounded', 'value': 'Wounded'},
                                    {'label': 'Only Damages', 'value': 'Damages'},  
                                ],
                                value=['Casualties','Wounded','Damages'],
                                labelStyle={'display': 'inline-block','font-size':'12px'}
                            )
            
def generate_radio(label, id):
    return html.Div( className='metric-select-menu',
        children=[
            html.Label(className="metric-select-title", children=label),
            html.Br(),
            dcc.RadioItems( id=id,
                options=[{'label': '   '+str(i), 'value': i} for i in ['total', 'relative']],
                value='total',
                labelStyle={'display': 'inline-block'}
            )
        ])

def apply_filter(data,check_sev,check_car):
    size = data.shape[0]
    casualties, wounded, damages, motorcycle, car = np.zeros(size, dtype=bool),np.zeros(size, dtype=bool),\
        np.zeros(size, dtype=bool), np.zeros(size, dtype=bool), np.zeros(size, dtype=bool)

    suv, bus, truck, bycicle, industrial = np.zeros(size, dtype=bool),np.zeros(size, dtype=bool), \
        np.zeros(size, dtype=bool), np.zeros(size, dtype=bool), np.zeros(size, dtype=bool)

    other = np.zeros(size, dtype=bool)

    if 'Casualties' in check_sev:
        casualties = data['CANT_MUERTOS_EN _SITIO_ACCIDENTE'] > 0
    if 'Wounded' in check_sev:
        wounded = data['CANT_HERIDOS_EN _SITIO_ACCIDENTE'] > 0
    if 'Damages' in check_sev:
        damages = (data['CANT_MUERTOS_EN _SITIO_ACCIDENTE'] == 0) & (data['CANT_HERIDOS_EN _SITIO_ACCIDENTE'] == 0)
    if 'Motorcycle' in check_car:
        motorcycle = (data['VEHICULO_MOTOCICLETA'] > 0) | (data['VEHICULO_MOTOCARRO'] > 0) | (data['VEHICULO_CUATRIMOTO'] > 0) 
    if 'Car' in check_car:
        car = data['VEHICULO_AUTOMOVIL'] > 0
    if 'Suv' in check_car:
        suv = (data['VEHICULO_CAMIONETA'] > 0) | (data['VEHICULO_CAMPERO'] > 0)
    if 'Bus' in check_car:
        bus = (data['VEHICULO_BUS'] > 0) | (data['VEHICULO_BUSETA'] > 0) | (data['VEHICULO_MICROBUS'] > 0) | (data['VEHICULO_BUS_ARTICULADO'] > 0) 
    if 'Truck' in check_car:
        truck = (data['VEHICULO_CAMION'] > 0) | (data['VEHICULO_TRACTO_CAMION'] > 0) | (data['VEHICULO_VOLQUETA'] > 0) | \
            (data['VEHICULO_DUMPER_VOLQUETAARTICULADA'] > 0) | (data['VEHICULO_REMOLQUE'] > 0) | (data['VEHICULO_SEMIREMOLQUE'] > 0)
    if 'Industrial' in check_car:
        industrial = (data['VEHICULO_MONTACARGAS'] > 0) | (data['VEHICULO_MINICARGADOR'] > 0) | (data['VEHICULO_MINI_EXCAVADORA'] > 0) | \
            (data['VEHICULO_MAQUINARIA_AGRICOLA'] > 0) | (data['VEHICULO_MAQUIRIA_INDUSTRIAL'] > 0) | (data['VEHICULO_RETROEXCAVADORA'] > 0) 
    if 'Bycicle' in check_car:
        bycicle = (data['VEHICULO_BICICLETA'] > 0) 
    if 'Other' in check_car:
        other = (data['VEHICULO_DESCONOCIDO'] > 0) | (data['VEHICULO_NO_REGISTRA'] > 0) | (data['VEHICULO_TRACCION_ANIMAL'] > 0)
    return data[(casualties | wounded | damages) & (motorcycle | car | suv | bus | truck | industrial | bycicle | other)] 

app.layout = html.Div(
    id="big-app-container",
    children=[
        build_banner(),
        html.Table(
            # Header
            [html.Tr([html.Td('Select Year'),html.Td('Select Vehicle'),html.Td('Select Severity')])]  +
            # Body
            [html.Tr([
                html.Td(generate_year_checklist()),html.Td(generate_vehicle_checklist()),html.Td(generate_sev_checklist())
            ]) ]
        ),
        html.Div(
            id="app-container",
            children=[
               
                #TABS
                html.Div(
                    id="tabs",
                    className="tabs",
                    children=[
                        dcc.Tabs(
                            id="app-tabs",
                            value="tab2",
                            className="custom-tabs",
                            children=[
                                dcc.Tab(
                                    id="First-tab",
                                    label="Dynamic Charts",
                                    value="tab1",
                                    className="custom-tab",
                                    selected_className="custom-tab--selected",
                                    children=[
                                        html.Div(className='row metric-row',
                                            children=[
                                                generate_chart('four columns', 'Dynamic Bar Chart', 'bar-chart'),
                                                generate_chart('four columns', 'Dynamic Plot Chart', 'plot-chart'),
                                                html.Div(className='three columns',
                                                    children=[
                                                        generate_dropdown('metric-select-menu','metric-select-title','Select X for bar and plot', 'xaxis-dd',
                                                            [{'label': k, 'value': v} for (k,v) in main_columns2.items()],7),
                                                        html.Br(),
                                                        generate_dropdown('metric-select-menu','metric-select-title','Select Y for plot', 'yaxis-dd', 
                                                            [{'label': k, 'value': v} for (k,v) in main_columns2.items()],5),
                                                        html.Br(),
                                                        generate_radio('Total vs Relative', 'yaxis-type')
                                                    ]
                                                )
                                            ]
                                        )
                                    ]
                                ),
                                dcc.Tab(
                                    id="Second-tab",
                                    label="Dynamic Heatmap",
                                    value="tab2",
                                    className="custom-tab",
                                    selected_className="custom-tab--selected",
                                    children=[
                                        html.Div(className='row metric-row',
                                            children=[
                                                generate_chart('eight columns', 'Heatmap', 'heatmap'),
                                                html.Div( className='three columns', 
                                                    children=[
                                                            generate_dropdown('metric-select-menu','metric-select-title','Select X', 'xaxis-heatmap',[{'label': i, 'value': i} 
                                                                    for i in ['hour','day','day of week','month']],1),
                                                            html.Br(),
                                                            generate_dropdown('metric-select-menu','metric-select-title','Select Y', 'yaxis-heatmap', [{'label': i, 'value': i}
                                                                    for i in ['hour','day','day of week','month']],2)
                                                    ]
                                                )
                                            ]
                                        ),
                                    ]
                                ),
                                dcc.Tab(
                                    id="Third-tab",
                                    label="Dynamic Map",
                                    value="tab3",
                                    className="custom-tab",
                                    selected_className="custom-tab--selected",
                                    children=[
                                        html.Div(
                                            className="eleven columns div-for-charts bg-grey",
                                            children=[
                                                dcc.Graph(id="map-graph")
                                            ]
                                        ),
    
                                    ]
                                ),
                            ],
                            )
                        ],
                    ),
                    html.Br(),html.Br(),html.Br()
            ],
        )
    ]
)

#CALLBACKS
@app.callback(
    Output("heatmap", 'figure'),
    [Input('check-year','value'),Input('xaxis-heatmap', 'value'),Input('yaxis-heatmap', 'value'), Input('check-sev', 'value'),
    Input('check-car', 'value')])
def update_heatmap(year_list,xaxis,yaxis,check_sev, check_car):
    try:
        dff = df[df['year'].isin(year_list)]

        dff = apply_filter(dff,check_sev,check_car)
        if xaxis==yaxis:
            yaxis='year'

        cats= [ 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        months=['January','February','March','April','May','June','July','August','September','October','November' ,'December']

        legend_axis = {'month'   :sorted(list(dff['month_name'].unique()), key=months.index),
                    'hour'       :np.sort(list(dff['hour'].unique())),
                    'day of week':sorted(list(dff['day_name'].unique()), key=cats.index),
                    'day'        :np.sort(list(dff['day'].unique())),
                    'year'       :np.sort(list(dff['year'].unique())) }

        dff=dff[[xaxis,yaxis,'ID']].groupby([xaxis,yaxis]).count().reset_index()
        
        trace = go.Heatmap(
            x=legend_axis[xaxis], 
            y=legend_axis[yaxis], 
            z=dff.pivot(yaxis,xaxis,'ID').fillna(0), 
            colorscale='RdYlGn', 
            reversescale=True,
            colorbar=dict(
                    title='Number of accidents',
                    titlefont={'color':'#D2D2D2'},
                    tickfont={'color':'#D2D2D2'},
                    tickcolor='#D2D2D2',
                ),
            showscale=True)
        return {"data": [trace],
                "layout": go.Layout(
                            xaxis={"title": xaxis,'color': '#D2D2D2',},
                            yaxis={"title": yaxis, "tickmode": "array",
                                    'color': '#D2D2D2'                                  
                            },
                            paper_bgcolor=bg_color,
                            plot_bgcolor=bg_color,
                        )
        }
    except Exception as e:
        print("type error: " + str(e))
        return None 

@app.callback(
    Output('bar-chart', 'figure'),
    [Input('check-year','value'),
     Input('xaxis-dd', 'value'),
     Input('yaxis-type', 'value'),
     Input('check-sev', 'value'),
     Input('check-car', 'value')])
def update_bar_chart(year_list,xaxis,axistype, check_sev, check_car):
    try:
            #Filter year
        dff = df[df['year'].isin(year_list)]

        dff = apply_filter(dff,check_sev,check_car)

        dff=dff[[xaxis,'FECHA_ACCIDENTE','ID','year']]

        dff.dropna()
        dff_xx=dff.groupby([xaxis,"year"], as_index=False).count()

        unique_x=dff_xx[xaxis].unique()

        # Obtaining the x label
        xaxis_label = ''
        for k, v in main_columns2.items():
            if v == xaxis:
                xaxis_label = k 

        ally=[]
        traces=[]
        if len(year_list) > 0 and len(check_sev) > 0 and len(check_car) > 0 and dff.shape[0] > 0:
            for year in range(min(year_list),max(year_list)+1): # for each year - a different bar
                
                # Obtain the number to divide the results. If relative, it will obtain # of days, in order to obtain total accidents per day.
                if axistype=='relative':
                    count_dff=[dff[(dff[xaxis]==i) & (dff['year']==year)]['FECHA_ACCIDENTE'].unique().size for i in unique_x]
                else:
                    count_dff=[1 for i in unique_x]
                
                y0=dff_xx[dff_xx['year']==year][['ID',xaxis]] # Number of accidents per AXIS and YEAR
                y=[]
                counter=0
                for i in range(len(unique_x)): # Iterating all the AXIS unique categories
                    if counter >= len(y0[xaxis]):
                        y.append(pd.Series({'ID':0,xaxis:unique_x[i]}))
                    elif y0[xaxis].iloc[counter]==unique_x[i]:
                        y.append(y0.iloc[counter])
                        counter=counter+1
                    else:
                        y.append(pd.Series({'ID':0,xaxis:unique_x[i]}))
                y=pd.DataFrame(y)
                ally.append(y)

                trace = go.Bar(
                    name=year,
                    x=y[xaxis].unique(),
                    y=y['ID']/count_dff,        
                )
                traces.append(trace)
        else:
            trace = go.Bar()
            traces.append(trace)

        layout = go.Layout(
            autosize=True,
            xaxis= dict(
                gridcolor='#696969',
                gridwidth=2,
                color= '#D2D2D2',
                autorange= True,
                title= xaxis_label,
                showspikes= True
            ),
            yaxis=dict(
                title='Number of accidents',
                autorange=True,
                color='#D2D2D2',
                zeroline=True,
                gridwidth=1,
                zerolinecolor='rgb(255, 255, 255)',
                zerolinewidth=2,
            ),
            colorway=['#9C280F','#FFC300','#DAF7A6','#0C8522'],
            hoverlabel={
                'bgcolor': '#D2D2D2',
                'font': {
                    'color': 'black'
                },
            },
            legend=dict(font={'color':'#D2D2D2'}),
            margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
            hovermode='closest',
            paper_bgcolor=bg_color,
            plot_bgcolor=bg_color,
        )
        return {'data': traces,'layout':layout}
    except Exception as e:
        print("type error: " + str(e))
        return None
 
@app.callback(
    Output('plot-chart', 'figure'),
    [Input('check-year','value'),
     Input('xaxis-dd', 'value'),
     Input('yaxis-dd', 'value'),
     Input('yaxis-type', 'value'),
     Input('check-sev', 'value'),
     Input('check-car', 'value')])
def update_plot(year_list, xaxis_value, yaxis_value, yaxis_type,check_sev, check_car):
    #filter year
    dff = df[df['year'].isin(year_list)]
    
    dff = apply_filter(dff,check_sev,check_car)
    
    dff=dff.groupby([xaxis_value,yaxis_value]).count()['ID']

    #Obtaining the x label
    xaxis_label = ''
    for k, v in main_columns2.items():
        if v == xaxis_value:
            xaxis_label = k 

    #Obtaining the y label
    yaxis_label = ''
    for k, v in main_columns2.items():
        if v == yaxis_value:
            yaxis_label = k 

    if dff.shape[0] > 0:
        den = list(dff)/np.max(list(dff))*50
    else:
        den = 1


    data = go.Data([
        go.Scatter(
            x=[i[0] for i in dff.index],
            y=[i[1] for i in dff.index],
            text= list(dff),
            mode='markers',
            opacity=0.4,
            marker={
                'symbol': 'circle',
                'size': den,
                'color': '#0C8522'
            },
            hoverlabel={
                'bgcolor': '#D2D2D2',
                'font': {
                    'color': 'black'
                },
            },
        )
    ],
        style={
        'color': '#D2D2D2'})

    layout = go.Layout(
        autosize=True,
        xaxis={
            'gridcolor' : '#696969',
            'gridwidth' : 1,
            'color': '#D2D2D2',
            'autorange': True,
            'title': xaxis_label,
            'showspikes': True
        },
        yaxis={
            'gridcolor' : '#696969',
            'gridwidth' : 1,
            'color': '#D2D2D2',
            'autorange': True,
            'title': yaxis_label,
        },
        margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
        hovermode='closest',
        paper_bgcolor=bg_color,
        plot_bgcolor=bg_color,
    )

    return go.Figure(
        data=data,
        layout=layout
    )

@app.callback(
    Output('map-graph', 'figure'),
    [Input('check-year','value'),
    Input('check-sev', 'value'),
    Input('check-car', 'value'),
    ])
def update_map(year_list,check_sev, check_car):

    #Filter year
    dff = df[df['year'].isin(year_list)]

    dff = apply_filter(dff,check_sev,check_car)

    dff=dff[['lat','lon','ID']].groupby(['lat','lon']).count().reset_index()

    # Paint mapbox into the data
    data = go.Data([
        go.Densitymapbox(
            lat=dff['lat'],
            lon=dff['lon'],
            text=dff['ID'],
            radius=6.5,
            opacity=0.5,
            colorbar=None
        )
    ]) 

    # Layout and mapbox properties
    layout = go.Layout(
        autosize=True,
        hovermode='closest',
        margin=go.layout.Margin(l=40, r=0, t=10, b=40),
        mapbox=dict(
            accesstoken=mapbox_access_token,
            bearing=0,
            pitch=0,
            zoom=11.5,
            style='dark'
        ),
        mapbox_center={"lat": 10.981619, "lon": -74.802569},
        paper_bgcolor=bg_color,
        plot_bgcolor=bg_color,
    )

    return go.Figure(
        data=data,
        layout=layout
    )

# Run dash server
if __name__ == '__main__':
    app.run_server(debug=False, host='0.0.0.0')
