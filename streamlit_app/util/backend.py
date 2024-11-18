import requests
import csv
import streamlit as st

# Replace these variables with your Directus instance details
BASE_URL = 'https://preceptorial-tracker-3lwwuw7l2q-uc.a.run.app' 
EMAIL = 'person@email.com'
PASSWORD = 'mypassword'

@st.cache_data
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

@st.cache_data
def get_teacher_users(headers, base_url=BASE_URL):
    """Retrieve users with the role of 'teacher'."""
    users_url = f'{base_url}/users'
    params = {
        'filter[role][name][_eq]': 'Teacher',  # Filter users where the role name is 'Teacher'
        'fields': 'first_name,last_name,email,location' # Fields to retrieve
    }
    response = requests.get(users_url, headers=headers, params=params)
    response.raise_for_status()
    users = response.json()['data']
    return users

def write_users_to_csv(users, filename='teachers.csv'):
    """Write user data to a CSV file."""
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['first_name', 'last_name', 'email', 'location']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for user in users:
            writer.writerow({
                'first_name': user.get('first_name', ''),
                'last_name': user.get('last_name', ''),
                'location': user.get('location', ''),
                'email': user.get('email', '')

            })
    print(f'Successfully wrote {len(users)} users to {filename}')

def main():
    try:
        # Step 1: Authenticate and get the access token
        access_token = authenticate(EMAIL, PASSWORD, BASE_URL)
        headers = {
            'Authorization': f'Bearer {access_token}'
        }

        # Step 2: Get users with the role 'teacher'
        users = get_teacher_users(BASE_URL, headers)

        if not users:
            print('No users with the role of teacher found.')
            return

        # Step 3: Write users to CSV
        write_users_to_csv(users)

    except requests.exceptions.HTTPError as http_err:
        print(f'HTTP error occurred: {http_err.response.text}')
    except Exception as err:
        print(f'An error occurred: {err}')

if __name__ == '__main__':
    main()
