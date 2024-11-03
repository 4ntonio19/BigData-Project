from functools import lru_cache
from typing import Optional

# from geopy.geocoders import Nominatim
# from geopy.exc import GeocoderTimedOut
import geopandas as gpd
import pandas as pd
from linkedin_dashboard.settings.settings import get_settings
from prophet import Prophet

from project.linkedin_dashboard.Enums.dataset_enum import DatasetName

from project.linkedin_dashboard.constants.const import ALL_STATES, GLOBAL_DATASETS, EXTERNAL_DICT, SKILLS_LIST, SKILLS_WITH_DATASET_MAPPING


def get_global_dataset(dataset_name: str) -> pd.DataFrame:
    """
    Atualiza a variável global com um dataset tratado.

    :param dataset_name: Nome do dataset (chave) para atualização.
    :param df: DataFrame processado.
    """
    global GLOBAL_DATASETS
    return GLOBAL_DATASETS.get(dataset_name, None)


def add_global_dataset(dataset_name: str, df: pd.DataFrame) -> None:
    """
    Atualiza a variável global com um dataset tratado.

    :param dataset_name: Nome do dataset (chave) para atualização.
    :param df: DataFrame processado.
    """
    global GLOBAL_DATASETS
    GLOBAL_DATASETS[dataset_name] = df


def get_dataset(csv_path: str, nrows: Optional[int] = None) -> pd.DataFrame:
    """
    Loads a dataset from a provided CSV file.

    :param csv_path: Path to the CSV file.
    :return: DataFrame with the content of the CSV file.
    """
    try:
        if nrows:
            return pd.read_csv(csv_path, nrows=nrows)
        return pd.read_csv(csv_path)
    except FileNotFoundError:
        print(f"Error: File not found at the path: {csv_path}")
        raise
    except pd.errors.EmptyDataError:
        print(f"Error: CSV file is empty: {csv_path}")
        raise
    except Exception as e:
        print(f"Error loading the CSV file: {e}")
        raise



def save_predict_job_postings_by_skills(job_posting):
    new_job_posting = job_posting.copy(deep=True)
    for skill in SKILLS_LIST: # sua var global
        df = filter_by_skills(new_job_posting, skill)
        df = predict_job_postings_2025(df)
        dataset_name = SKILLS_WITH_DATASET_MAPPING.get(skill)
        add_global_dataset(dataset_name, df)


def process_job_postings() -> pd.DataFrame:
    """
    Loads and processes job postings data, merging it with job skills.

    :return: Processed DataFrame of job postings.
    """
    settings = get_settings()

    job_postings_df = get_dataset(settings.dataset_settings.job_postings_path,
                                  nrows=120000)
    job_skills_df = get_dataset(settings.dataset_settings.job_skills_path)
    # company_specialities_df = get_dataset(
    #     settings.dataset_settings.company_specialities_path)

    # job_postings_df = job_postings_df.merge(company_specialities_df,
    #                                         on="company_id",
    #                                         how="left")

    job_postings_df = merge_skills_with_jobs(job_postings_df, job_skills_df)

    job_postings_df = remove_unused_columns(job_postings_df)

    job_postings_df = process_postings_data(job_postings_df)

    geolocation_df = load_geolocation_data(
        settings.geo_settings.united_states_geo)

    job_postings_df[[
        'city', 'state'
    ]] = job_postings_df['location'].apply(split_location).apply(pd.Series)

    job_postings_df = replace_state_to_abbreviation(job_postings_df, EXTERNAL_DICT)

    job_postings_df = merge_geolocation_with_jobs(job_postings_df,
                                                  geolocation_df)

    add_global_dataset(DatasetName.JOB_POSTINGS, job_postings_df)

    return job_postings_df


def merge_skills_with_jobs(job_postings_df: pd.DataFrame,
                           job_skills_df: pd.DataFrame) -> pd.DataFrame:
    """Merges job skills with job postings."""

    job_skills_df = job_skills_df.groupby('job_id')['skill_abr'].agg(
        lambda x: ', '.join(x)).reset_index()

    job_postings_df = job_postings_df.merge(job_skills_df,
                                            on="job_id",
                                            how="left")

    job_postings_df['skill_abr'] = job_postings_df['skill_abr'].fillna('')

    return job_postings_df


def process_postings_data(job_postings_df: pd.DataFrame) -> pd.DataFrame:
    """Processes job postings data: handling missing values, salary, and adding year."""
    job_postings_df = process_salary(job_postings_df)
    job_postings_df = handle_missing_values(job_postings_df)

    job_postings_df['remote_allowed'] = job_postings_df[
        'remote_allowed'].fillna(0)
    job_postings_df['is_remote'] = job_postings_df['remote_allowed'].apply(
        lambda x: 'Remota' if x == 1 else 'Não Remota')

    job_postings_df['listed_time_y_m_d'] = pd.to_datetime(
        job_postings_df['listed_time'] / 1000, unit='s')
    job_postings_df['year'] = job_postings_df['listed_time_y_m_d'].dt.year
    return job_postings_df


def remove_unused_columns(job_postings_df: pd.DataFrame) -> pd.DataFrame:
    """Removes unused columns from the job postings dataframe."""
    cols_to_remove = [
        'sponsored',
        'currency',
        'work_type',
        'job_posting_url',
        'expiry',
        'posting_domain',
        'application_type',
        'fips',
        'application_url',
        'compensation_type',
        'formatted_work_type',
        'description',
        'closed_time',
        'zip_code',
        'normalized_salary',
        'original_list_time',
    ]
    return job_postings_df.drop(columns=cols_to_remove, errors='ignore')


@lru_cache
def get_skill_dict() -> dict:
    """
    Loads and creates a skill dictionary mapping skill names to their abbreviations.

    :return: Dictionary mapping skill names to abbreviations.
    """
    settings = get_settings()
    df_skills = get_dataset(settings.dataset_settings.skills_path)

    skill_dict = dict(zip(df_skills['skill_name'], df_skills['skill_abr']))

    return skill_dict


@lru_cache
def get_skill_names() -> list:
    """
    Loads the list of skill names.

    :return: List of skill names.
    """
    settings = get_settings()
    df_skills = get_dataset(settings.dataset_settings.skills_path)

    skill_names = df_skills['skill_name'].tolist()

    return skill_names


def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    Fills missing values in the job postings DataFrame for specified columns.

    :param df: The DataFrame containing job postings data.
    """
    cols_fill_not_specified = [
        'skills_desc', 'applies', 'formatted_experience_level', 'company_name'
    ]
    cols_fill_zero = ['applies', 'company_id', 'views']

    df[cols_fill_not_specified] = df[cols_fill_not_specified].fillna(
        "Not Specified")
    df[cols_fill_zero] = df[cols_fill_zero].fillna(0)

    if not df['company_name'].isnull().all():
        df['company_name'] = df['company_name'].fillna(
            df['company_name'].mode()[0])

    return df


def split_location(location: str):
    if ',' in location:
        state = location.split(', ')[-1].strip()
        city = location.split(', ')[0].strip()
    else:
        state = location
        city = None
    return city, state


def process_salary(df: pd.DataFrame) -> pd.DataFrame:
    df['max_salary'] = pd.to_numeric(df['max_salary'], errors='coerce')
    df['min_salary'] = pd.to_numeric(df['min_salary'], errors='coerce')

    #df['max_salary'] = df['max_salary'].fillna(df['max_salary'].median())
    #df['min_salary'] = df['min_salary'].fillna(df['min_salary'].median())

    df[['max_salary', 'min_salary', 'pay_period']] = df.apply(
        lambda row: (
            # Caso o pay_period seja 'HOURLY'
            ((row['max_salary'] * 44) * 4) * 12,
            ((row['min_salary'] * 44) * 4) * 12,
            'YEARLY') if row['pay_period'] == 'HOURLY' else (
                # Caso o pay_period seja 'MONTHLY'
                row['max_salary'] * 12,
                row['min_salary'] * 12,
                'YEARLY') if row['pay_period'] == 'MONTHLY' else (
                    # Caso contrário, mantenha os valores originais
                    row['max_salary'],
                    row['min_salary'],
                    row['pay_period']),
        axis=1,
        result_type='expand')

    df['med_salary'] = df['med_salary'].fillna(
        (df['max_salary'] + df['min_salary']) / 2)

    df['med_salary'] = df['med_salary'].round(-3)
    return df


# def process_salary2(df: pd.DataFrame):
#     # Condições para transformar os valores com base no pay_period
#     is_hourly = df['pay_period'] == 'HOURLY'
#     is_monthly = df['pay_period'] == 'MONTHLY'

#     # Cálculos para 'HOURLY' e 'MONTHLY'
#     df.loc[is_hourly, ['max_salary', 'min_salary']] = df.loc[
#         is_hourly, ['max_salary', 'min_salary']] * 44 * 4 * 12
#     df.loc[is_monthly, ['max_salary', 'min_salary']] = df.loc[
#         is_monthly, ['max_salary', 'min_salary']] * 12

#     # Atualizar 'pay_period' para 'YEARLY' onde for 'HOURLY' ou 'MONTHLY'
#     df.loc[is_hourly | is_monthly, 'pay_period'] = 'YEARLY'

#     # Calcular média salarial
#     df['calculated_med_salary'] = (df['max_salary'] + df['min_salary']) / 2

#     # Substituir valores de 'med_salary' se nulo ou menor ou igual a zero
#     df['med_salary'] = df['med_salary'].where(df['med_salary'] > 0,
#                                               df['calculated_med_salary'])

#     # Arredondar 'med_salary' para o milhar mais próximo
#     df['med_salary'] = df['med_salary'].round(-3)

#     return df


def filter_by_skills(df: pd.DataFrame, selected_skills: list[str]) -> pd.DataFrame:
    """
    Filters job postings by selected skills.

    :param df: DataFrame containing job postings data.
    :param selected_skills: List of selected skills to filter by.
    :return: Filtered DataFrame.
    """
    if selected_skills:
        filtered_df = df[df['skill_abr'].apply(
            lambda x: any(skill in x for skill in selected_skills))]
    else:
        filtered_df = df
    return filtered_df

def filter_predict_jobs_by_skills(df: pd.DataFrame, selected_skills: str) -> pd.DataFrame:
    """
    Filters job postings by a selected skill.

    :param df: DataFrame containing job postings data.
    :param selected_skills: A single selected skill to filter by.
    :return: Filtered DataFrame.
    """
    if selected_skills:
        print("Selected skill:", selected_skills)  # Debugging output
        # Assume that each entry in 'skill_abr' is a list of skills
        filtered_df = df[df['skill_abr'].apply(
            lambda x: selected_skills in x if isinstance(x, list) else False)]
    else:
        filtered_df = df

    missing_states = set(ALL_STATES) - set(filtered_df['state'].unique())
    missing_df = pd.DataFrame({
        'state': list(missing_states),
        'predicted_postings': 0,
        'skill_abr': [''] * len(missing_states)
    })

    final_df = pd.concat([filtered_df, missing_df], ignore_index=True)

    return final_df




def get_remote_distribution(df: pd.DataFrame) -> list:
    """
    Calculates the distribution of remote and non-remote job postings.

    :param df: DataFrame containing job postings data.
    :return: DataFrame with the count of remote and non-remote postings.
    """
    remote_counts = df['is_remote'].value_counts().reset_index()
    remote_counts.columns = ['Tipo', 'Contagem']
    return remote_counts


def get_salary_means(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates the average salary for remote and non-remote job postings.

    :param df: DataFrame containing job postings data.
    :return: DataFrame with the average salary for remote and non-remote jobs.
    """
    salary_means_df = df.groupby(
        'is_remote')['med_salary'].mean().reset_index()
    salary_means_df.columns = ['Tipo', 'Média Salarial']
    salary_means_df['Média Salarial'] = salary_means_df[
        'Média Salarial'].apply(lambda x: int(x) if pd.notna(x) else x)
    salary_means_df['Média Salarial'] = salary_means_df['Média Salarial'].round(-3)
    return salary_means_df


def load_geolocation_data(json_path: str) -> pd.DataFrame:
    """
    Load geolocation data from a JSON file.

    :param json_path: Path to the JSON file containing geolocation data.
    :return: DataFrame with geolocation data.
    """
    return gpd.read_file(json_path)


def merge_geolocation_with_jobs(
        job_postings_df: pd.DataFrame,
        geolocation_gdf: gpd.GeoDataFrame) -> pd.DataFrame:
    """
    Merge job postings with geolocation data.

    :param job_postings_df: DataFrame of job postings.
    :param geolocation_df: DataFrame of geolocation data.
    :return: Merged DataFrame with job postings and geolocation.
    """
    geolocation_gdf['state'] = geolocation_gdf['name']
    return job_postings_df.merge(geolocation_gdf[['state', 'geometry']],
                                 on='state',
                                 how='left')


def predict_job_postings_2025(predict_job_df: pd.DataFrame) -> pd.DataFrame:

    states = predict_job_df['state'].unique()
    predict_job_df['ds'] = predict_job_df['listed_time_y_m_d']

    results = []

    for state in states:
        df_state: pd.DataFrame = predict_job_df[predict_job_df['state'] ==
                                                state]

        skills_for_state = df_state['skill_abr'].unique().tolist()

        df_weekly = df_state.set_index('ds').resample('D').size().reset_index(
            name='y')

        if df_weekly.empty or df_weekly.shape[0] < 2:
            results.append({
                'state': state,
                'predicted_postings': 0,
                'skill_abr': skills_for_state
            })
            continue

        model = Prophet()
        model.fit(df_weekly)

        future = model.make_future_dataframe(periods=365, freq='D')

        forecast = model.predict(future)

        total_jobs_2025 = forecast[(forecast['ds'] >= '2025-01-01') & (
            forecast['ds'] <= '2025-12-31')]['yhat_lower'].sum()

        total_jobs_2025 = round(total_jobs_2025, 0)


        results.append({
            'state': state,
            'predicted_postings': total_jobs_2025,
            'skill_abr': skills_for_state

        })

    for state in ALL_STATES:
        if state not in [result['state'] for result in results]:
            results.append({
                'state': state,
                'predicted_postings': 0,
                'skill_abr': []
            })

    return pd.DataFrame(results)

def replace_state_to_abbreviation(job_postings_df: pd.DataFrame, external_dict: dict) -> pd.DataFrame:
    """
    Replaces the values in the 'state' column of the provided DataFrame with abbreviations 
    based on an external dictionary.
    :param job_postings_df: DataFrame containing job postings data, including a 'state' column.
    :param external_dict: Dictionary with full state names as keys and their abbreviations as values.
    :return: Updated DataFrame with 'state' values replaced by abbreviations.
    """
    job_postings_df['state'] = job_postings_df['state'].replace(external_dict)
    return job_postings_df

