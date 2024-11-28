import streamlit as st
import pandas as pd
import sqlite3
from util.queries import queries_calculate_averages, query_create_join_learners
from util.directus_connector import get_teachers, get_students, get_chapters

def create_db(access_token):
    """Creates an SQLite in-memory database, then connects to directus API and load the data into it"""
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
    # Calculate Chapter Averages
    for q in queries_calculate_averages:
        conn.execute(q)
    conn.commit()
    # creates "learners" data table which joins students, and all chapters
    conn.execute(query_create_join_learners)
    conn.commit()
    return conn
   
@st.cache_data
def get_learners(access_token):
    """Reads joint learners data table, caculates total score, and returns result as pd dataframe"""
    # read learners table
    db = create_db(access_token)
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