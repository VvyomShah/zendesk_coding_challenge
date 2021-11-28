import requests
import getpass
import json
import os

import credentials

class Authenticate:

    def __init__(self):
        self.SUBDOMAIN = None
        self.USERNAME = None
        self.PASSWORD = None
        self.getCredentials()

        # self.SUBDOMAIN = credentials.credentials['domain']
        # self.USERNAME = credentials.credentials['email']
        # self.PASSWORD = credentials.credentials['password']

    def getCredentials(self):
        get_username = getpass.getuser()
        get_password = getpass.getpass()

        try:
            self.USERNAME = getpass.getpass('Username: ', get_username)

        except Exception as error:
            print('ERROR', error)
        
        try:
            self.PASSWORD = getpass.getpass('Password: ', get_password)

        except Exception as error:
            print('ERROR', error)


class Tickets:

    def __init__(self):
        self.SUBDOMAIN = credentials.credentials['domain']
        self.current_tickets = None
        self.after = None
        self.before = None
        self.has_more = None

    def request(self, API, payload, credentials):
        url = os.path.join(self.SUBDOMAIN, API)
        response = requests.get(url, auth=credentials, params=payload)
        if response.status_code != 200:
            print('Error')
            return 'Error'
        return response.json()

    def getTickets(self, credentials):

        if not self.after and not self.before and not self.has_more: 
            ticketsData = self.request('api/v2/tickets.json', credentials=credentials, payload = {"page[size]": "25"})
            self.has_more = ticketsData['meta']['has_more']
            self.before = ticketsData['meta']['before_cursor']
            self.after = ticketsData['meta']['after_cursor']
            self.current_tickets = ticketsData['tickets']
            print(self.current_tickets)





class Display:

    def __init__(self):
        Auth = Authenticate()
        allTickets = Tickets()

        allTickets.getTickets((Auth.USERNAME, Auth.PASSWORD))

if __name__ == '__main__':
    view = Display()


            
