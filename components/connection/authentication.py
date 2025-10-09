import requests
import json
from components.connection.credentials import USERNAME, PASSWORD, URL

class Authenticat(object):
    def __init__(self):
        self.token_access = None
        self.url_token = URL+"/accounts/token" 
        self.res = None # response
    
    def do_auth(self):
        valores = {
            "email": USERNAME,
            "password": PASSWORD
        }

        try:
            req = requests.post(self.url_token, data=json.dumps(valores), timeout=5)
        except:
            return None
        
        
        if req.status_code == 200:
            dic_content = req.json()
            self.token_access = dic_content[0]['token']
        elif req.status_code == 401:
            return False
        
        return True
    
    def get_response(self):
        return self.res
    
    def get_token(self):
        return self.token_access