import requests
import threading

class geneacity_API_request(threading.Thread):
    """Class used to make requests to the Geneacity API.

    Args:
        threading (_type_): Allows the execution of a sequence of instructions without interrupting the main process.
    """
    def __init__(self, url: str):
        """Creates an instance to make requests to the Geneacity API.

        Args:
            url (str): Receives the URL that will be used to make calls to the API.
        """
        super().__init__()
        self.url = url
        self.json = None
        self.status = 0
        self.error = None
        self.valid = False  

    def run(self):
        """Makes the call to the API and receives the status code to verify if it's working, showing the API's response.
        """
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
        """Obtains the response given by the API so it can be used in the main code.

        Returns:
            _type_: Returns the response of the API after making the call.
        """
        self.join()  
        return self.json