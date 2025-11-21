import requests
import base64
import json


class APIClient:
    def __init__(self, base_url='http://localhost:8000/api'):
        self.base_url = base_url
        self.auth_header = None
    
    def set_auth(self, username, password):
        credentials = f"{username}:{password}"
        encoded = base64.b64encode(credentials.encode()).decode()
        self.auth_header = {'Authorization': f'Basic {encoded}'}
    
    def upload_csv(self, file_path):
        url = f"{self.base_url}/upload/"
        with open(file_path, 'rb') as f:
            files = {'file': f}
            response = requests.post(url, files=files, headers=self.auth_header)
            response.raise_for_status()
            return response.json()
    
    def get_summary(self):
        url = f"{self.base_url}/summary/"
        response = requests.get(url, headers=self.auth_header)
        response.raise_for_status()
        return response.json()
    
    def get_history(self):
        url = f"{self.base_url}/history/"
        response = requests.get(url, headers=self.auth_header)
        response.raise_for_status()
        return response.json()
    
    def download_pdf(self, save_path):
        url = f"{self.base_url}/report/pdf/"
        response = requests.get(url, headers=self.auth_header, stream=True)
        response.raise_for_status()
        with open(save_path, 'wb') as f:
            f.write(response.content)
    
    def register(self, username, email, password):
        url = f"{self.base_url}/register/"
        data = {
            'username': username,
            'email': email,
            'password': password,
            'password_confirm': password
        }
        response = requests.post(url, json=data)
        response.raise_for_status()
        return response.json()

