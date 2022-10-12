# Iportação das bibliotecas necessárias
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Lê os dados e os atribui a um dataframe pandas
spacex_df = pd.read_csv("C:/Users/Oliveira/Desktop/Curso cientista de dados/10 - Applied Data Science Capstone/3 - Interactive visual analytics and Dashboard/spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Cria uma aplicação dash
app = dash.Dash(__name__)

# Cria um layout do aplicativo
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # Adiciona uma lista suspensa para habilitar a seleção do local de lançamento
                                # O valor de seleção padrão é para TODOS os locais
                                # dcc.Dropdown(id='site-dropdown',...)
                                dcc.Dropdown(id='site-dropdown', 
                                            options=[{'label': 'All Sites', 'value': 'ALL'},
                                            {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                            {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'}, 
                                            {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                            {'label': 'CCAFS SLC-40 ', 'value': 'CCAFS SLC-40'}
                                            ], 
                                            value = 'ALL',
                                            placeholder='Select a Launch Site here',
                                            searchable = True
                                            ),
                                html.Br(),

                                # Adiciona um gráfico de pizza para mostrar a contagem total de lançamentos bem-sucedidos para todos os locais de lançamento
                                # Se um local de lançamento específico foi selecionado, mostre as contagens de sucesso x falha para o local
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # Adiciona um controle deslizante para selecionar o intervalo de carga útil
                                dcc.RangeSlider(id='payload-slider',
                                                min = 0, max = 10000, step = 1000,
                                                marks = {0: '0', 1000: '1000', 2000: '2000', 
                                                        3000: '3000', 4000: '4000', 5000: '5000',
                                                        6000: '6000', 7000: '7000', 8000: '8000',
                                                        9000: '9000', 10000: '10000'},
                                                value = [min_payload, max_payload]),

                                # Adiciona um gráfico de dispersão para mostrar a correlação entre a carga útil e o sucesso do lançamento
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# Adiciona uma função de retorno de chamada para `site-dropdown` como entrada e `success-pie-chart` como saída

# Decorador de função para especificar a entrada e a saída de função
@app.callback(Output(component_id='success-pie-chart', component_property='figure'), 
            Input(component_id='site-dropdown', component_property='value'))

def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        fig = px.pie(data_frame = spacex_df, names='Launch Site', values = 'class',
        title='Total Launches for All Sites')
        return fig

    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        fig = px.pie(data_frame = filtered_df, names = 'class', 
        title = f"Total Success Launches for site {entered_site}")
        return fig

# Adiciona uma função de retorno de chamada para `site-dropdown` e `payload-slider` como entrada e `success-payload-scatter-chart` como saída

@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'), 
            [Input(component_id='site-dropdown', component_property='value'),
            Input(component_id="payload-slider", component_property="value")])

def get_scatter_chart(entered_site, payload_slider):
    
    if entered_site == 'ALL':
        # Configura a coluna de massa de carga útil do dataframe de acordo com controle deslizante payload_slider
        filtered_data = spacex_df[(spacex_df['Payload Mass (kg)'] >= payload_slider[0]) &
        (spacex_df['Payload Mass (kg)'] <= payload_slider[1])]
        fig = px.scatter(data_frame = filtered_data, x = 'Payload Mass (kg)', y = 'class', 
        color = 'Booster Version Category')
        return fig

    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        filtered_data = filtered_df[(filtered_df['Payload Mass (kg)'] >= payload_slider[0]) &
        (filtered_df['Payload Mass (kg)'] <= payload_slider[1])]
        fig = px.scatter(data_frame = filtered_data, x = 'Payload Mass (kg)', y = 'class',
        color = 'Booster Version Category')
        return fig

# Executa o aplicativo para gerar o Dashboard em HTML
if __name__ == '__main__':
    app.run_server()