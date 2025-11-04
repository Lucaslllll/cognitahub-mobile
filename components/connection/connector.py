import json
from components.connection.authentication import Authenticat
from kaki.app import App
from kivy.storage.jsonstore import JsonStore

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

from components.connection.credentials import URL

class Connector(object):

    def __init__(self, name_url, tag="None"):
        self.name_url = name_url
        self.url = URL
        self.path = App.get_running_app().user_data_dir+"/"
        

        store = JsonStore(self.path+"data.json")
        if store.exists('authentication'):
            self.response = store.get("authentication")["response"]
            self.token_access = store.get("authentication")["token_access"]
        else:
            self.response = False
            self.token_access = None
        
        self.head = {'Content-Type': 'application/json', 'Authorization': 'Bearer {}'.format(self.token_access)}

        
    def get(self, id_object=None, page=None, image=False):
        if self.response == True:
            
            if page != None:
                try:
                    request = requests.get(self.url+"/"+self.name_url+"?page={}".format(page), headers=self.head, verify=False, timeout=(5, 15))
                except:
                    return "Error When Making a Request To The Server"
                
            else:
                if id_object == None:
                    try:
                        request = requests.get(self.url+"/"+self.name_url, headers=self.head, verify=False, timeout=(5, 15))
                    except requests.exceptions.Timeout:
                        return "Erro: O tempo limite foi excedido."
                    except requests.exceptions.ConnectionError:
                        return "Erro: Não foi possível conectar ao servidor."
                    except:
                        return "Error When Making A Request To The Server"
                else:
                    try:
                        request = requests.get(self.url+"/"+self.name_url+"/{}".format(id_object), headers=self.head, verify=False, timeout=(5, 15))
                    except requests.exceptions.Timeout:
                        return "Erro: O tempo limite foi excedido."
                    except requests.exceptions.ConnectionError:
                        return "Erro: Não foi possível conectar ao servidor."
                    except:
                        return "Error When Making A Request To The Server"
            
            if request.status_code == 200 and image == True:
                return request.content
            elif request.status_code == 200:
                return request.json()
            elif request.status_code == 401:
                return "Without Authorization"
            elif request.status_code == 404:
                return 404
            else:
                return "Unexpected Error"
        
        elif self.response == False:
            return "Invalid Credentials"
        else:
            return "Problem contacting the server!"
    

    def post(self, data, files=None, head=None, *args, **kwargs):

        if files != None:
            try:
                request = requests.post(self.url+"/"+self.name_url, data=json.dumps(data), files=files,
                 headers=self.head, verify=False, timeout=(5, 15))
            except requests.exceptions.Timeout:
                return "Erro: O tempo limite foi excedido."
            except requests.exceptions.ConnectionError:
                return "Erro: Não foi possível conectar ao servidor."
            except:
                try:
                    request = requests.post(self.url+"/"+self.name_url, files=files, data=data,
                    headers=self.head, verify=False, timeout=(5, 15))
                except:
                    return "Error When Making A Request To The Server"
            

        else:
            try:
                request = requests.post(self.url+"/"+self.name_url, data=json.dumps(data), headers=self.head, verify=False, timeout=(5, 15))
            except requests.exceptions.Timeout:
                return "Erro: O tempo limite foi excedido."
            except requests.exceptions.ConnectionError:
                return "Erro: Não foi possível conectar ao servidor."
            except:
                try:
                    request = requests.post(self.url+"/"+self.name_url, data=data,
                    headers=self.head, verify=False, timeout=(5, 15))
                except:
                    return "Error When Making A Request To The Server"
        
        #debug

        print(request.content)
        
        if request.status_code == 201:
            return True
        elif request.status_code == 200:
            return request.json()
        elif request.status_code == 401:
            return "Without Authorization"
        elif request.status_code == 400:
            return "Missing or Data Already Repeated By Others"
        else:
            return "Unexpected Error"
        
        
        return False
    

    def get_url(self):
        return self.url+"/"+self.name_url