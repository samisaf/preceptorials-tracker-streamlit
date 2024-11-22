import requests
import streamlit as st
import pandas as pd
import sys, os
import sqlite3

BASE_URL = 'https://preceptorial-tracker-3lwwuw7l2q-uc.a.run.app'

@st.cache_data
def authenticate(email, password, base_url=BASE_URL):
    """Authenticate with the Directus API and return the access token."""
    return "THIS IS A TEST ACCESS TOKEN"
    # auth_url = f'{base_url}/auth/login'
    # auth_payload = {
    #     'email': email,
    #     'password': password
    # }
    # response = requests.post(auth_url, json=auth_payload)
    # response.raise_for_status() # Raise an exception for HTTP errors
    # access_token = response.json()['data']['access_token']
    # return access_token

@st.cache_data
def get_teachers(access_token, base_url=BASE_URL):
    """Retrieve users with the role of 'teacher'."""
    return pd.read_csv(f'./src/data/teachers.csv')
    # headers = {'Authorization': f'Bearer {access_token}'}
    # users_url = f'{base_url}/users'
    # params = {
    #     'filter[role][name][_eq]': 'Teacher', # Filter users where the role name is 'Teacher'
    #     'fields': 'first_name,last_name,email,location' # Fields to retrieve
    # }
    # response = requests.get(users_url, headers=headers, params=params)
    # response.raise_for_status()
    # users = response.json()['data']
    # return  pd.DataFrame(users)

@st.cache_data
def get_students(access_token, base_url=BASE_URL):
    """Retrieve all fields from the students table."""
    return pd.read_csv(f'./src/data/students.csv')
    # headers = {'Authorization': f'Bearer {access_token}'}
    # students_url = f'../data/{base_url}/items/students'
    # params = {'fields': '*'}
    # response = requests.get(students_url, headers=headers, params=params)
    # response.raise_for_status()
    # students = response.json()['data']
    # return  pd.DataFrame(students)


@st.cache_data
def get_items(access_token, item_name, base_url=BASE_URL):
    """Retrieve all fields from the students table."""
    return pd.read_csv(f'./src/data/{item_name}.csv')
    # headers = {'Authorization': f'Bearer {access_token}'}
    # items_url = f'{base_url}/items/{item_name}'
    # params = {'fields': '*'}
    # response = requests.get(items_url, headers=headers, params=params)
    # response.raise_for_status()
    # items = response.json()['data']
    # return  pd.DataFrame(items)

@st.cache_data
def get_chapters(access_token, base_url=BASE_URL):
    chapters = {}
    for i in 'a b c d e f g h'.split():
        chapter = get_items(access_token, f'preceptorial_chapter_{i}', base_url)
        chapters[i] = chapter
    return chapters

def get_db(access_token):
    # create an SQLite in-memory database and load the data into it
    conn = sqlite3.connect(':memory:')
    # add students
    students = get_students(access_token)
    students.to_sql('students', conn, index=False, if_exists='replace')
    # add teachers
    teachers = get_teachers(access_token)
    teachers.to_sql('teachers', conn, index=False, if_exists='replace')
    # add Chapters
    chapters = get_chapters(access_token)
    letters = 'a b c d e f g h'.split()
    for l in letters:
        chapters[l].to_sql(f'{l}', conn, index=False, if_exists='replace')
    insert_averages(conn)
    create_join_learners(conn)
    return conn
    
def insert_averages(conn):
    from util.queries import queries_calculate_averages
    for q in queries_calculate_averages:
        conn.execute(q)
    conn.commit()

def create_join_learners(conn):
    from util.queries import query_create_join_learners
    conn.execute(query_create_join_learners)
    conn.commit()

@st.cache_data
def get_learners(access_token):
    """Reads joint learners data table, caculates total score, and returns result as pd dataframe"""
    # read learners table
    db = get_db(access_token)
    df = pd.read_sql_query("SELECT * FROM learners", db)
    # calculate total score
    average_columns = ['a_average', 'b_average', 'c_average', 'd_average', 'e_average', 'f_average', 'g_average', 'h_average']
    numer = df[average_columns].sum(axis=1, skipna=True)
    denom = df[average_columns].notnull().sum(axis=1)
    df['total_score'] = numer/denom
    # rounds the scores to 1 decimal
    for c in df.columns:
        if c.endswith("average"):
            df[c] = df[c].round(2) 
    df['total_score'] = df['total_score'].round(2) 
    # clean up dates
    for c in df.columns:
        if c.startswith("date"):
            df[c] = pd.to_datetime(df[c])
            df[c] = df[c].dt.strftime("%Y-%m-%d")
    return df

