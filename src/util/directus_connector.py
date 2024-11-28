import requests
import pandas as pd
import json
BASE_URL = 'https://preceptorial-tracker-3lwwuw7l2q-uc.a.run.app'

def authenticate(email, password, base_url=BASE_URL):
    """Authenticate with the Directus API and return the access token."""
    auth_url = f'{base_url}/auth/login'
    auth_payload = {
        'email': email,
        'password': password
    }
    response = requests.post(auth_url, json=auth_payload)
    response.raise_for_status() # Raise an exception for HTTP errors
    access_token = response.json()['data']['access_token']
    return access_token

def get_teachers(access_token, base_url=BASE_URL):
    """Retrieve users with the role of 'teacher'."""
    headers = {'Authorization': f'Bearer {access_token}'}
    url = f'{base_url}/users'
    all_items = []
    limit = 100  # Adjust this if the API allows a higher limit
    offset = 0

    while True:
        params = {
            'filter[role][name][_eq]': 'Teacher',  # Filter users where the role name is 'Teacher'
            'fields': '*',
            'limit': limit,
            'offset': offset
        }
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        items = response.json()['data']

        if not items:  # Exit the loop if no more items are returned
            break

        all_items.extend(items)
        offset += limit

    return pd.DataFrame(all_items)

def get_students(access_token, base_url=BASE_URL):
    """Retrieve all fields from the students table."""
    headers = {'Authorization': f'Bearer {access_token}'}
    url = f'{base_url}/items/students'
    all_items = []
    limit = 100  # Adjust this if the API allows a higher limit
    offset = 0

    while True:
        params = {
            'fields': '*',
            'limit': limit,
            'offset': offset
        }
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        items = response.json()['data']

        if not items:  # Exit the loop if no more items are returned
            break

        all_items.extend(items)
        offset += limit

    # preceptors column is a list, and will need to convert to text in order for the table to convert to sql
    students = pd.DataFrame(all_items)
    students['preceptors'] = students['preceptors'].apply(json.dumps)

    return students

def get_items(access_token, item_name, base_url=BASE_URL):
    """Retrieve all fields from the specified item table, handling pagination."""
    headers = {'Authorization': f'Bearer {access_token}'}
    url = f'{base_url}/items/{item_name}'
    all_items = []
    limit = 100  # Adjust this if the API allows a higher limit
    offset = 0

    while True:
        params = {
            'fields': '*',
            'limit': limit,
            'offset': offset
        }
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        items = response.json()['data']

        if not items:  # Exit the loop if no more items are returned
            break

        all_items.extend(items)
        offset += limit

    return pd.DataFrame(all_items)

def get_chapters(access_token, base_url=BASE_URL):
    chapters = {}
    for i in 'a b c d e f g h'.split():
        chapter = get_items(access_token, f'preceptorial_chapter_{i}', base_url)
        chapters[i] = chapter
    return chapters