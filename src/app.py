import requests
import getpass
import json

from werkzeug.wrappers import response

class Authenticate:

    def __init__(self):
        self.SUBDOMAIN = 'https://zccvvyomshah.zendesk.com'
        self.USERNAME = None
        self.PASSWORD = None
        self.getCredentials()

    def getCredentials(self):
        get_username = getpass.getuser()
        get_password = getpass.getpass()

        try:
            self.USERNAME = getpass.getpass('Username: ', get_username)
            self.PASSWORD = getpass.getpass('Password: ', get_password)

        except Exception as error:
            print('ERROR', error)


class Tickets:

    def __init__(self):
        pass

    def getTickets(self, APIUrl, username, password):
            response = requests.get(APIUrl, auth=(username, password))

            if response.status_code != 200:
                print('Error')
                exit()
            
            