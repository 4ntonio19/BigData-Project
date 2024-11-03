from dash import dcc, html
from linkedin_dashboard.process.process_data import (get_skill_dict,
                                                     get_skill_names)

skill_dict = get_skill_dict()

skill_names = ['Design', 'Product Manager',"Quality Assurance", "Information Technology"]

skill_list = {
    "Design": "DSGN",
    "Product Manager": "PRDM",
    "Quality Assurance": "QA",
    "Information Technology": "IT"
}


layout = html.Div([
    html.H1("Análise de Vagas no Linkedin por Habilidades",
            style={
                'position': 'absolute',
                'top': '0',
                'left': '0',
                'right': '0',
                'margin': '0',
                'padding': '10px',
                'color': '#4CAF50',
                'fontFamily': 'Arial',
                'fontSize': '28px',
                'fontWeight': 'bold',
                'backgroundColor': '#F0F0F0',
                'borderRadius': '10px 0 0 10px',
                'boxShadow': '2px 2px 10px rgba(0, 0, 0, 0.1)'
            }),
    html.Div([
        html.Label("Selecione a área:"),
        dcc.Dropdown(
            id='skill-dropdown',
            options=[{
                'label': name,
                'value': skill_list[name]
            } for name in skill_names],
            multi=False,
            placeholder="Selecione uma ou mais habilidades",
            clearable=False,
        ),
    ],
             style={'paddingTop': '60px'}),
    html.Div([
        html.Div(
            [
                 dcc.Loading(
            id="loading-1",
            type="circle",
            children=dcc.Graph(id='job-postings-2025-map',
                               figure={'layout': {
                                   'width': 1400,
                                   'height': 700,
                               }})
                ),
            ],
            style={
                'width': '100%',
                'display': 'inline-block'
            },
        ),
        html.Div([

            dcc.Graph(id='graph')
        ],
                 style={
                     'width': '100%',
                     'display': 'inline-block'
                 }),
    ]),
    html.Div([
        html.Div([dcc.Graph(id='remote-job-pie-chart')],
                 style={
                     'width': '50%',
                     'display': 'inline-block'
                 }),
        html.Div([dcc.Graph(id='salary-bar-chart')],
                 style={
                     'width': '50%',
                     'display': 'inline-block'
                 }),
    ]),
],
                  style={'position': 'relative'})
