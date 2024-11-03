import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash.dependencies import Input, Output
from linkedin_dashboard.process.process_data import (
    add_global_dataset, filter_by_skills, filter_predict_jobs_by_skills, get_global_dataset,
    get_remote_distribution, get_salary_means, load_geolocation_data,
    merge_geolocation_with_jobs, predict_job_postings_2025,
    process_job_postings, save_predict_job_postings_by_skills)

from project.linkedin_dashboard.Enums.dataset_enum import DatasetName
from project.linkedin_dashboard.constants.const import SKILLS_LIST
from project.linkedin_dashboard.settings.settings import get_settings
cached_processed_df = None

def create_callbacks(app):
    global cached_processed_df
    @app.callback(Output('remote-job-pie-chart', 'figure'), [
        Input('skill-dropdown', 'value'),
    ])
    def update_pie_chart(selected_skills):
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
    ])
    def update_salary_bar_chart(selected_skills):
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
        Input('skill-dropdown', 'value'),
    ])
    def display_position(selected_skills):
        if (df := get_global_dataset(DatasetName.JOB_POSTINGS)) is None:
            df = process_job_postings()
        df = filter_by_skills(df, selected_skills)
        median_salaries = df[[
            "formatted_experience_level", "med_salary"
        ]].groupby("formatted_experience_level").median().reset_index()

        fig = go.Figure(
            data=go.Bar(x=median_salaries["formatted_experience_level"],
                        y=median_salaries["med_salary"],
                        textposition='outside'))
        return fig

    @app.callback(Output('job-postings-2025-map', 'figure'),
                  [Input('skill-dropdown', 'value')])
    def update_map(selected_skills):
        settings = get_settings()
        print("Habilidades selecionadas:", selected_skills)
        geolocation_gdf = load_geolocation_data(
            settings.geo_settings.united_states_geo)

        if selected_skills is None or selected_skills == '':
            print("selecionou")
            if (cached_processed_df := get_global_dataset(
                    DatasetName.PREDICT_JOB_POSTINGS_2025)) is None:
                if (df:=get_global_dataset(DatasetName.JOB_POSTINGS)) is None:
                    df = process_job_postings()
                print("caiu")
                save_predict_job_postings_by_skills(df)
                filter_predict_job_df = predict_job_postings_2025(df)
        elif selected_skills == 'DSGN':
            filter_predict_job_df = get_global_dataset(DatasetName.PREDICT_JOB_POSTINGS_DSGN)
            print(f'linha 84: {filter_predict_job_df.head()}')
            if filter_predict_job_df is None:
                if (df:=get_global_dataset(DatasetName.JOB_POSTINGS)) is None:
                    df = process_job_postings()
                print(f'linha 88: {df.head()}')
                temp_df = filter_by_skills(df, selected_skills)
                print(f'linha 90: {temp_df.head()}')
                filter_predict_job_df = predict_job_postings_2025(temp_df)
                print(f'linha 92: {filter_predict_job_df.head()}')
        elif selected_skills == 'IT':
            filter_predict_job_df = get_global_dataset(DatasetName.PREDICT_JOB_POSTINGS_IT)
            print(f'linha 84: {filter_predict_job_df.head()}')
            if filter_predict_job_df is None:
                if (df:=get_global_dataset(DatasetName.JOB_POSTINGS)) is None:
                    df = process_job_postings()
                print(f'linha 88: {df.head()}')
                temp_df = filter_by_skills(df, selected_skills)
                print(f'linha 90: {temp_df.head()}')
                filter_predict_job_df = predict_job_postings_2025(temp_df)
                print(f'linha 92: {filter_predict_job_df.head()}')
        elif selected_skills == 'PRDM':
            filter_predict_job_df = get_global_dataset(DatasetName.PREDICT_JOB_POSTINGS_PRDM)
            print(f'linha 84: {filter_predict_job_df.head()}')
            if filter_predict_job_df is None:
                if (df:=get_global_dataset(DatasetName.JOB_POSTINGS)) is None:
                    df = process_job_postings()
                print(f'linha 88: {df.head()}')
                temp_df = filter_by_skills(df, selected_skills)
                print(f'linha 90: {temp_df.head()}')
                filter_predict_job_df = predict_job_postings_2025(temp_df)
                print(f'linha 92: {filter_predict_job_df.head()}')
        elif selected_skills == 'QA':
            filter_predict_job_df = get_global_dataset(DatasetName.PREDICT_JOB_POSTINGS_QA)
            print(f'linha 84: {filter_predict_job_df.head()}')
            if filter_predict_job_df is None:
                if (df:=get_global_dataset(DatasetName.JOB_POSTINGS)) is None:
                    df = process_job_postings()
                print(f'linha 88: {df.head()}')
                temp_df = filter_by_skills(df, selected_skills)
                print(f'linha 90: {temp_df.head()}')
                filter_predict_job_df = predict_job_postings_2025(temp_df)
                print(f'linha 92: {filter_predict_job_df.head()}')


        if filter_predict_job_df.empty:
            print("Nenhum dado disponível para as habilidades selecionadas.")
            # Retorne um gráfico vazio ou um aviso, conforme necessário
            return go.Figure()  # Retorna um gráfico vazio se não houver dados

        predict_job_df = merge_geolocation_with_jobs(
                filter_predict_job_df, geolocation_gdf)

        add_global_dataset(DatasetName.PREDICT_JOB_POSTINGS_2025,
            pd.DataFrame(predict_job_df))

        color_scale = 'RdBu' if (predict_job_df['predicted_postings'] > 0).any() else [(0, 'red'), (1, 'white')]


        fig = px.choropleth_mapbox(
            predict_job_df,
            locations='state',
            geojson=geolocation_gdf,
            featureidkey='properties.name',
            color='predicted_postings',
            hover_name='state',
            mapbox_style="carto-positron",
            zoom=1.8,
            center={"lat": 37.1, "lon": -95.7},
            opacity=0.5,
            color_continuous_scale=color_scale,
            labels={'predicted_postings': 'Vagas Previstas'},
            title='Previsão de Vagas em 2025 por Estado nos EUA',
        )

        fig.update_layout(coloraxis_colorbar=dict(
            titleside='right',
            ticks='outside',
        ), template=None)

        return fig
