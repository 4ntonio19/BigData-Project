import plotly.express as px
import plotly.graph_objects as go
from dash.dependencies import Input, Output
from linkedin_dashboard.process.process_data import (
    filter_by_skills, get_global_dataset, get_remote_distribution,
    get_salary_means, load_geolocation_data, merge_geolocation_with_jobs,
    predict_job_postings_2025, process_job_postings, train_job_posting_model)

from project.linkedin_dashboard.Enums.dataset_enum import DatasetName
from project.linkedin_dashboard.settings.settings import get_settings


def create_callbacks(app):

    @app.callback(Output('remote-job-pie-chart', 'figure'), [
        Input('skill-dropdown', 'value'),
        Input('interval-component', 'n_intervals')
    ])
    def update_pie_chart(selected_skills, n_intervals):
        if (df := get_global_dataset(DatasetName.JOB_POSTINGS)) is None:
            df = process_job_postings()

        filtered_df = filter_by_skills(df, selected_skills)
        remote_counts = get_remote_distribution(filtered_df)
        fig = px.pie(remote_counts,
                     values='Contagem',
                     names='Tipo',
                     title='Distribuição de Vagas Remotas e Não Remotas')
        return fig

    @app.callback(Output('salary-bar-chart', 'figure'), [
        Input('skill-dropdown', 'value'),
        Input('interval-component', 'n_intervals')
    ])
    def update_salary_bar_chart(selected_skills, n_intervals):
        if (df := get_global_dataset(DatasetName.JOB_POSTINGS)) is None:
            df = process_job_postings()

        filtered_df = filter_by_skills(df, selected_skills)
        salary_means = get_salary_means(filtered_df)
        fig = px.bar(salary_means,
                     x='Tipo',
                     y='Média Salarial',
                     title='Média Salarial: Vagas Remotas vs Não Remotas')
        return fig

    @app.callback(Output("graph", "figure"), [
        Input("dropdown", "value"),
        Input('skill-dropdown', 'value'),
        Input('interval-component', 'n_intervals')
    ])
    def display_position(cargo, selected_skills, n_intervals):
        if (df := get_global_dataset(DatasetName.JOB_POSTINGS)) is None:
            df = process_job_postings()
        df = filter_by_skills(df, selected_skills)
        df = df[df["title"].str.contains(cargo, case=False, na=False)]
        median_salaries = df[[
            "formatted_experience_level", "med_salary"
        ]].groupby("formatted_experience_level").median().reset_index()
        fig = go.Figure(
            data=go.Bar(x=median_salaries["formatted_experience_level"],
                        y=median_salaries["med_salary"],
                        textposition='outside'))
        return fig

    @app.callback(Output('job-postings-2025-map', 'figure'),
                  [Input('interval-component', 'n_intervals')])
    def update_map(n_intervals):
        if (df := get_global_dataset(DatasetName.JOB_POSTINGS)) is None:
            df = process_job_postings()
        print(df.columns.to_list())
        settings = get_settings()
        model = train_job_posting_model(df)
        df_2025 = predict_job_postings_2025(model, df)
        #print(df_2025[['year', 'predicted_postings']].head())
        geolocation_gdf = load_geolocation_data(
            settings.geo_settings.united_states_geo)
        merged_df = merge_geolocation_with_jobs(df_2025, geolocation_gdf)
        #print(merged_df.head())

        colorscale = [
            "#d9d9d9",
            "#f7fbff",
            "#ebf3fb",
            "#deebf7",
            "#d2e3f3",
            "#c6dbef",
            "#b3d2e9",
            "#9ecae1",
            "#85bcdb",
            "#6baed6",
            "#57a0ce",
            "#4292c6",
            "#3082be",
            "#2171b5",
            "#1361a9",
            "#08519c",
            "#0b4083",
            "#08306b",
        ]
        fig = px.choropleth(
            merged_df,
            locations='state',
            geojson=geolocation_gdf,
            featureidkey='properties.name',
            color='predicted_postings',
            hover_name='state',
            color_continuous_scale=colorscale,
            labels={'predicted_postings': 'Vagas Previstas'},
            title='Previsão de Vagas em 2025 por Estado nos EUA')

        fig.update_geos(fitbounds="locations",
                        visible=False,
                        center={
                            "lat": 37.1,
                            "lon": -95.7
                        },
                        projection_type="albers usa")

        fig.update_layout(coloraxis_colorbar=dict(
            titleside='right',
            ticks='outside',
        ),
                          template=None)

        return fig
