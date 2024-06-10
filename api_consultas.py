import requests
import threading

class geneacity_API_request(threading.Thread):
    def __init__(self, url: str):
        super().__init__()
        self.url = url
        self.json = None
        self.status = 0
        self.error = None
        self.valid = False  

    def run(self):
        response = requests.get(self.url)
        if response.status_code == 200:
            self.json = response.json()
            self.status = self.json['status']
            self.valid = True if self.status == 1 else False  
            print(f"Solicitud a {self.url} exitosa, status: {self.status}")
        else:
            self.error = f"Error al hacer la solicitud: {response.status_code}"
            print(self.error)
            self.valid = False  

    def get_response(self):
        self.join()  
        return self.json