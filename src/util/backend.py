import requests
import streamlit as st
import pandas as pd

BASE_URL = 'https://preceptorial-tracker-3lwwuw7l2q-uc.a.run.app'

@st.cache_data
def authenticate(email, password, base_url=BASE_URL):
    """Authenticate with the Directus API and return the access token."""
    return "this is a test token"
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
    return pd.read_csv(f'./data/teachers.csv')
    # headers = {'Authorization': f'Bearer {access_token}'}
    # users_url = f'{base_url}/users'
    # params = {
    #     'filter[role][name][_eq]': 'Teacher', # Filter users where the role name is 'Teacher'
    #     'fields': 'first_name,last_name,email,location' # Fields to retrieve
    # }
    # response = requests.get(users_url, headers=headers, params=params)
    # response.raise_for_status()
    # users = response.json()['data']
    # return users

@st.cache_data
def get_students(access_token, base_url=BASE_URL):
    """Retrieve all fields from the students table."""
    return pd.read_csv(f'./data/students.csv')
    # headers = {'Authorization': f'Bearer {access_token}'}
    # students_url = f'../data/{base_url}/items/students'
    # params = {'fields': '*'}
    # response = requests.get(students_url, headers=headers, params=params)
    # response.raise_for_status()
    # students = response.json()['data']
    # return students


@st.cache_data
def get_items(access_token, item_name, base_url=BASE_URL):
    """Retrieve all fields from the students table."""
    return pd.read_csv(f'./data/{item_name}.csv')
    # headers = {'Authorization': f'Bearer {access_token}'}
    # items_url = f'{base_url}/items/{item_name}'
    # params = {'fields': '*'}
    # response = requests.get(items_url, headers=headers, params=params)
    # response.raise_for_status()
    # items = response.json()['data']
    # return items

@st.cache_data
def get_chapters(access_token, base_url=BASE_URL):
    chapters = {}
    for i in 'a b c d e f g h'.split():
        chapter = get_items(access_token, f'preceptorial_chapter_{i}', base_url)
        chapters[i] = chapter
    return chapters

