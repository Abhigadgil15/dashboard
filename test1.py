import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input,Output, State
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import pandas as pd
import json
import plotly.express as px
import numpy as np
import plotly.offline as py

app = dash.Dash(external_stylesheets=[dbc.themes.GRID, dbc.themes.BOOTSTRAP],)

env = ["Ozone", "CO2", "Death from air pollution"]
with open('data/Worldmap shapes/custom.geo.json') as f:
  geojson = json.load(f)

df1 = pd.read_csv("data/data_situation2.csv")
df2 = pd.read_csv("data\Sea_Level_GMSL.csv")


def sea_level():
    month = [1,2,3,4,5,6,7,8,9,10,11,12]*23
    month = month[0:266]
    month = pd.DataFrame(month)
    year = [1993, 1993, 1993, 1993, 1993, 1993, 1993, 1993, 1993, 1993, 1993, 1993, 1994, 1994, 1994,
       1994, 1994, 1994, 1994, 1994, 1994, 1994, 1994, 1994, 1995, 1995, 1995, 1995, 1995, 1995,
       1995, 1995, 1995, 1995, 1995, 1995, 1996, 1996, 1996, 1996, 1996, 1996, 1996, 1996, 1996,
       1996, 1996, 1996, 1997, 1997, 1997, 1997, 1997, 1997, 1997, 1997, 1997, 1997, 1997, 1997,
       1998, 1998, 1998, 1998, 1998, 1998, 1998, 1998, 1998, 1998, 1998, 1998, 1999, 1999, 1999,
       1999, 1999, 1999, 1999, 1999, 1999, 1999, 1999, 1999, 2000, 2000, 2000, 2000, 2000, 2000,
       2000, 2000, 2000, 2000, 2000, 2000, 2001, 2001, 2001, 2001, 2001, 2001, 2001, 2001, 2001,
       2001, 2001, 2001, 2002, 2002, 2002, 2002, 2002, 2002, 2002, 2002, 2002, 2002, 2002, 2002,
       2003, 2003, 2003, 2003, 2003, 2003, 2003, 2003, 2003, 2003, 2003, 2003, 2004, 2004, 2004,
       2004, 2004, 2004, 2004, 2004, 2004, 2004, 2004, 2004, 2005, 2005, 2005, 2005, 2005, 2005,
       2005, 2005, 2005, 2005, 2005, 2005, 2006, 2006, 2006, 2006, 2006, 2006, 2006, 2006, 2006,
       2006, 2006, 2006, 2007, 2007, 2007, 2007, 2007, 2007, 2007, 2007, 2007, 2007, 2007, 2007,
       2008, 2008, 2008, 2008, 2008, 2008, 2008, 2008, 2008, 2008, 2008, 2008, 2009, 2009, 2009,
       2009, 2009, 2009, 2009, 2009, 2009, 2009, 2009, 2009, 2010, 2010, 2010, 2010, 2010, 2010,
       2010, 2010, 2010, 2010, 2010, 2010, 2011, 2011, 2011, 2011, 2011, 2011, 2011, 2011, 2011,
       2011, 2011, 2011, 2012, 2012, 2012, 2012, 2012, 2012, 2012, 2012, 2012, 2012, 2012, 2012,
       2013, 2013, 2013, 2013, 2013, 2013, 2013, 2013, 2013, 2013, 2013, 2013, 2014, 2014, 2014,
       2014, 2014, 2014, 2014, 2014, 2014, 2014, 2014, 2014, 2015, 2015, 2015, 2015, 2015, 2015,
       2015, 2015, 2015, 2015, 2015, 2015,]
    year = year[0:266]
    month = pd.DataFrame(month)
    year = pd.DataFrame(year)
    Mean_Sea_Level = pd.concat([year, month, df2['GMSL']], axis=1)
    Mean_Sea_Level.columns = ['year', 'month','GMSL']
    Mean_Sea_Level = Mean_Sea_Level.groupby('year').last().reset_index()
    Rise = Mean_Sea_Level['GMSL'].diff()
    Rise.fillna(0)
    Mean_Sea_Level = pd.concat([Mean_Sea_Level, Rise], axis=1)
    Mean_Sea_Level.columns = ['year', 'month','Cumulative_change', 'One_year_rise']
    Mean_Sea_Level=Mean_Sea_Level.fillna("NA")
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=Mean_Sea_Level['year'],
            y=Mean_Sea_Level['Cumulative_change'],
            text = Mean_Sea_Level['One_year_rise'], # text to show on hover from df column
            marker=dict(color="black", size=12),
            mode = 'lines+markers',
            hovertemplate='Cumulative_change: %{y:.2f}'+'<br>Year: %{x}'+'<br>One_year_rise: %{text:.2f}'

        ))

    fig.add_trace(
        go.Bar(
            x=Mean_Sea_Level['year'],
            y=Mean_Sea_Level['Cumulative_change'],
            hovertemplate='Cumulative_change: %{y:.2f}'+'<br>Year: %{x}'
        ))
    fig.update_layout(
        title="Sea level Rise over years",
        xaxis_title="Year",
        yaxis_title="Change",
        #hovermode="x unified",
        font=dict(
            #family="Courier New, monospace",
            size=10,
            color="#7f7f7f"
        )
    )

    return fig


app.layout = html.Div(
    [
        #dbc.Row(dbc.Col(html.Div())),
        dbc.Row(
            [
                dbc.Col(html.Img(src="assets/profile.jpg", style = {
                "height": "100px",
                "width":"auto",
                'display': 'inline-block',
                "margin-left":"50px",
                "margin-top":"25px",
                # 'padding':'5px'
            } ),),
                dbc.Col(html.Div(html.H3("Environmental Awareness"),
                style = {'width': "auto", "color": "white", 'text-align': 'center', "font-family": "Fredoka One","font-size": "20px","margin-top":"25px",})
                ),
                dbc.Col(html.Div(style = {'width': "auto", "color": "white", 'text-align': 'right', "font-family": "Fredoka One","font-size": "20px",},
                children = [
                    dbc.Button("About Us", id="open", n_clicks=0, style={"margin-right":"25px","margin-top":"25px",}, color="primary"),
                    dbc.Modal([
                        dbc.ModalHeader("About Us"),
                        dbc.ModalBody("We are a community of 2 ppl"),
                    dbc.ModalFooter(
                        dbc.Button("Close", id="close", className="ml-auto", n_clicks=0,color="primary")
                            ),
                        ],
            id="modal",
            # size="lg",
            is_open=False,
            backdrop=True,
            centered=True,
            fade=True,
        )  
                        ]
                        )
                        ),
            ]
        ),
        html.Br(),
        dbc.Row([
           dbc.Col(dbc.Card([
               dbc.CardBody([
            #                        dcc.Dropdown(
            #         id='env-id',
            #         options=[{'label': i, 'value': i} for i in env],
            #         value='Ozone',
            #         placeholder='Select something...',
            #         style={
            #     'width': '100%', 
            # }
            #     ),
    #             dcc.Tabs(id='tabs-example', value='tab-1', children=[
    #     dcc.Tab(label='Map view ', value='tab-1' , children =[dcc.Graph( style={
    #             'width': '99%'
    #         })] ),
    #     dcc.Tab(label='Globe view', value='tab-2', children =[dcc.Graph( style={
    #             'width': '99%'
    #         })]),
    # ],           style={"border-radius": "50px",
    #            'display': 'inline-block', "width": "99%"}),     
                      
],

),],
 style={'display': 'inline-block', "height": "auto", "width":"auto","padding":"all","border-color": "black",
                "background-color":"black"},
           )),
             #html.Br(), 
           dbc.Col(dbc.Card(dbc.CardBody([dcc.Graph(
        #        id='indicator-graphic-1',figure = sea_level(), config={
        # "displaylogo": False},
                  ),
                  ]),style={
               'display': 'inline-block', "height": "auto", "width":"auto",
               "padding":"all", 
               "background-color":"black"} ))
        ]), 
        html.Br(),
        dbc.Row([dbc.Col(dbc.Card(style={"border-radius": "50px",
               'display': 'inline-block', "width": "auto", "padding-left":"1%", 
               "padding-right":"1%", "margin-bottom": "50px", "margin-top": "30px", "padding-top": "25px", 
               "background-color":"black", "margin-left":"30px"} )),
               dbc.Col(dbc.Card(style={"border-radius": "50px",
               'display': 'inline-block', "width": "auto", "padding-left":"1%", 
               "padding-right":"1%", "margin-bottom": "50px", "margin-top": "30px", "padding-top": "25px", 
               "background-color":"black", "margin-left":"30px"} )),
                dbc.Col(dbc.Card(style={"border-radius": "50px",
               'display': 'inline-block', "width": "auto", "padding-left":"1%", 
               "padding-right":"1%", "margin-bottom": "50px", "margin-top": "30px", "padding-top": "25px", 
               "background-color":"black", "margin-left":"30px"} ))
               
               
               
               
            ])
    ]
)


# @app.callback(
#      Output("map-view", "figure"),
#      [Input("env-id", "value")])
# def update_map_globe(env_id,):
#     if env_id == "CO2" :
#             fig = px.choropleth_mapbox(df1, locations="CODE",
#                                 geojson = geojson,
#                                 mapbox_style="carto-positron",
#                                 featureidkey="properties.iso_a3",
#                                 zoom=1,
#                                 opacity=0.8,
#                                 center = {"lat": 50.958427, "lon": 10.436234},
#                                 color="CO2_emissions", # lifeExp is a column of gapminder
#                                 hover_name="COUNTRY", # column to add to hover information
#                                 color_continuous_scale=px.colors.sequential.Plasma)
#             fig.update_layout(title='CO2 emission per capita : 2019 (in tons)')
#             fig.update_layout(margin=dict(l=20,r=0,b=0,t=70,pad=0),paper_bgcolor='#f8f7f7',height= 450,width = 750,title_text = 'CO2 emission per capita : 2019 (in tons)',font_size=18)
#     if env_id == "Death from air pollution":
#         fig = px.choropleth_mapbox(df1, locations="CODE",
#                             geojson = geojson,
#                             mapbox_style="carto-positron",
#                             featureidkey="properties.iso_a3",
#                             zoom=1,
#                             opacity=0.8,
#                             labels={'Death_from_air_pollution':'death_rate'},
#                             center = {"lat": 50.958427, "lon": 10.436234},
#                             color="Death_from_air_pollution", # lifeExp is a column of gapminder
#                             hover_name="COUNTRY", # column to add to hover information
#                             color_continuous_scale=px.colors.sequential.Plasma)
#         fig.update_layout(title='Death from air pollution : 2019 (per 100 000 citizens)', )
#         fig.update_layout(margin=dict(l=20,r=0,b=0,t=70,pad=0),paper_bgcolor='#f8f7f7',height= 450,width = 750,title_text = 'Death by air pollution : 2019 (per 100 000 citizens)',font_size=18)
#     if env_id == "Ozone":
#         fig = px.choropleth_mapbox(df1, locations="CODE",
#                             geojson = geojson,
#                             mapbox_style="carto-positron",
#                             featureidkey="properties.iso_a3",
#                             zoom=1,
#                             opacity=0.8,
#                             labels={'Ozone_concentration':'Ozone'},
#                             center = {"lat": 50.958427, "lon": 10.436234},
#                             color="Ozone_concentration", # lifeExp is a column of gapminder
#                             hover_name="COUNTRY", # column to add to hover information
#                             color_continuous_scale=px.colors.sequential.Plasma)
#         fig.update_layout(title='Ozone concentration : 2019')
#         fig.update_layout(margin=dict(l=20,r=0,b=0,t=70,pad=0),paper_bgcolor='#f8f7f7',height= 450,width = 750, title_text = 'Ozone concentration : 2019',font_size=18)
#     return fig

# @app.callback(
#      Output("globe-view", "figure"),
#      [Input("env-id", "value"), Input("tabs-example", "value")])
# def update_map_globe(env_id, tab):
#     if env_id == "CO2" :
#         if tab == 'tab-1':
#             fig = px.choropleth_mapbox(df1, locations="CODE",
#                                 geojson = geojson,
#                                 mapbox_style="carto-positron",
#                                 featureidkey="properties.iso_a3",
#                                 zoom=1,
#                                 opacity=0.8,
#                                 center = {"lat": 50.958427, "lon": 10.436234},
#                                 color="CO2_emissions", # lifeExp is a column of gapminder
#                                 hover_name="COUNTRY", # column to add to hover information
#                                 color_continuous_scale=px.colors.sequential.Plasma)
#             fig.update_layout(title='CO2 emission per capita : 2019 (in tons)')
#             fig.update_layout(margin=dict(l=20,r=0,b=0,t=70,pad=0),paper_bgcolor='#f8f7f7',height= 450,width = 750,title_text = 'CO2 emission per capita : 2019 (in tons)',font_size=18)
#         elif tab == "tab-2":
#             mean_temp = []
#             countries = np.unique(df1['Country_Region'])
#             for country in countries:                
#                 mean_temp.append(df1[df1['Country_Region'] == country]['CO2_emissions'].mean())  
#             data = [ dict(
#                     type = 'choropleth',
#                     locations = countries,
#                     z = mean_temp,
#                     locationmode = 'country names',
#                     text = countries,
#                     marker = dict(
#                         line = dict(color = 'rgb(0,0,0)', width = 1)),
#                         # colorbar = dict(autotick = "True", tickprefix = '', 
#                         # title = ' Co2 emissions')
#                         )
#                 ]

#             layout = dict(
#                 title = 'Average CO2 emissions in countries',
#                 geo = dict(
#                     showframe = False,
#                     showocean = True,
#                     oceancolor = 'rgb(0,255,255)',
#                     projection = dict(
#                     type = 'orthographic',
#                         rotation = dict(
#                                 lon = 60,
#                                 lat = 10),
#                     ),
#                     lonaxis =  dict(
#                             showgrid = True,
#                             gridcolor = 'rgb(102, 102, 102)'
#                         ),
#                     lataxis = dict(
#                             showgrid = True,
#                             gridcolor = 'rgb(102, 102, 102)'
#                             )
#                         ),
#                     )
#             fig=go.Figure(data=data, layout=layout)
#             #fig.show()

#     if env_id == "Death from air pollution":
#         if tab == 'tab-1':
#             fig = px.choropleth_mapbox(df1, locations="CODE",
#                                 geojson = geojson,
#                                 mapbox_style="carto-positron",
#                                 featureidkey="properties.iso_a3",
#                                 zoom=1,
#                                 opacity=0.8,
#                                 center = {"lat": 50.958427, "lon": 10.436234},
#                                 color="Death_from_air_pollution", # lifeExp is a column of gapminder
#                                 hover_name="COUNTRY", # column to add to hover information
#                                 color_continuous_scale=px.colors.sequential.Plasma)
#             fig.update_layout(title='Death from air pollution : 2019 (per 100 000 citizens)')
#             fig.update_layout(margin=dict(l=20,r=0,b=0,t=70,pad=0),paper_bgcolor='#f8f7f7',height= 450,width = 750,title_text = 'Death from air pollution : 2019 (per 100 000 citizens)',font_size=18)
#         elif tab == 'tab-2':
#             mean_temp = []
#             countries = np.unique(df1['Country_Region'])
#             for country in countries:                
#                 mean_temp.append(df1[df1['Country_Region'] == country]['Death_from_air_pollution'].mean())  
#             data = [ dict(
#                     type = 'choropleth',
#                     locations = countries,
#                     z = mean_temp,
#                     locationmode = 'country names',
#                     text = countries,
#                     marker = dict(
#                         line = dict(color = 'rgb(0,0,0)', width = 1),
#                         ),
#                         # colorbar = dict(autotick = "True", tickprefix = '', 
#                         # title = ' Co2 emissions')
                        
#                         )
                    
#                 ]

#             layout = dict(
#                 title = 'Death from air pollution',
#                 geo = dict(
#                     showframe = False,
#                     showocean = True,
#                     oceancolor = 'rgb(0,255,255)',
#                     projection = dict(
#                     type = 'orthographic',
#                         rotation = dict(
#                                 lon = 60,
#                                 lat = 10),
#                     ),
#                     lonaxis =  dict(
#                             showgrid = True,
#                             gridcolor = 'rgb(102, 102, 102)'
#                         ),
#                     lataxis = dict(
#                             showgrid = True,
#                             gridcolor = 'rgb(102, 102, 102)'
#                             )
#                         ),
#                     )
#             fig=go.Figure(data=data, layout=layout)

#     if env_id == "Ozone":
#         if tab == 'tab-1':
#             fig = px.choropleth_mapbox(df1, locations="CODE",
#                                 geojson = geojson,
#                                 mapbox_style="carto-positron",
#                                 featureidkey="properties.iso_a3",
#                                 zoom=1,
#                                 opacity=0.8,
#                                 labels={'Ozone_concentration':'Ozone'},
#                                 center = {"lat": 50.958427, "lon": 10.436234},
#                                 color="Ozone_concentration", # lifeExp is a column of gapminder
#                                 hover_name="COUNTRY", # column to add to hover information
#                                 color_continuous_scale=px.colors.sequential.Plasma)
#             fig.update_layout(title='Ozone concentration : 2019')
#             fig.update_layout(margin=dict(l=20,r=0,b=0,t=70,pad=0),paper_bgcolor='#f8f7f7',height= 450,width = 750, title_text = 'Ozone concentration : 2019',font_size=18)
#         if tab == 'tab-2':
#             mean_temp = []
#             countries = np.unique(df1['Country_Region'])
#             for country in countries:                
#                 mean_temp.append(df1[df1['Country_Region'] == country]['Ozone_concentration'].mean())  
#             data = [ dict(
#                     type = 'choropleth',
#                     locations = countries,
#                     z = mean_temp,
#                     locationmode = 'country names',
#                     text = countries,
#                     marker = dict(
#                         line = dict(color = 'rgb(0,0,0)', width = 1)),
#                         # colorbar = dict(autotick = "True", tickprefix = '', 
#                         # title = ' Co2 emissions')
#                         )
#                 ]

#             layout = dict(
#                 title = 'Ozone concentration',
#                 geo = dict(
#                     showframe = False,
#                     showocean = True,
#                     oceancolor = 'rgb(0,255,255)',
#                     projection = dict(
#                     type = 'orthographic',
#                         rotation = dict(
#                                 lon = 60,
#                                 lat = 10),
#                     ),
#                     lonaxis =  dict(
#                             showgrid = True,
#                             gridcolor = 'rgb(102, 102, 102)'
#                         ),
#                     lataxis = dict(
#                             showgrid = True,
#                             gridcolor = 'rgb(102, 102, 102)'
#                             )
#                         ),
#                     )
#             fig=go.Figure(data=data, layout=layout)

    
#     return fig


def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


app.callback(
    Output("modal", "is_open"),
    [Input("open", "n_clicks"), Input("close", "n_clicks")],
    [State("modal", "is_open")],
    )(toggle_modal)

if __name__ == '__main__':
    app.run_server(debug=True)