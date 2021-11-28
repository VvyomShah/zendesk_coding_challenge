import requests
import getpass
import os

import credentials

class Authenticate:

    def __init__(self):
        self.SUBDOMAIN = None
        self.USERNAME = None
        self.PASSWORD = None
        # self.getCredentials()

        self.SUBDOMAIN = credentials.credentials['domain']
        self.USERNAME = credentials.credentials['email']
        self.PASSWORD = credentials.credentials['password']

    def getCredentials(self):
        self.USERNAME = input('Username: ')
        
        try:
            self.PASSWORD = getpass.getpass('Password: ')
            print(self.USERNAME, self.PASSWORD)

        except Exception as error:
            print(self.USERNAME, self.PASSWORD)
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
            print(response.status_code)
            return 'Error'
        return response.json()

    def getTickets(self, credentials, change=0):
        if change == 0: 
            ticketsData = self.request('api/v2/tickets.json', credentials=credentials, payload = {"page[size]": "25"})
        
        elif change == 1:
            ticketsData = self.request('api/v2/tickets.json', credentials=credentials, payload = {"page[size]": "25", "page[after]": self.after})
            if ticketsData['meta']['has_more'] == False:
                print('No more tickets to display.')
                return

        elif change == -1:
            ticketsData = self.request('api/v2/tickets.json', credentials=credentials, payload = {"page[size]": "25", "page[before]": self.before})
            if ticketsData['meta']['has_more'] == False:
                print('No more previous tickets to display.')
                return

        self.has_more = ticketsData['meta']['has_more']
        self.before = ticketsData['meta']['before_cursor']
        self.after = ticketsData['meta']['after_cursor']
        self.current_tickets = ticketsData['tickets']
        

class Display:

    def __init__(self):
        Auth = Authenticate()
        allTickets = Tickets()
        credentials = (Auth.USERNAME, Auth.PASSWORD)
        allTickets.getTickets(credentials)
        self.displayMenu()
    
    def displayMenu(self):
        while True:
            print('(1) - Next page \n(2) - Previous page \n(3) - Select Ticket by Ticket ID \n')
            choice = input('Enter Choice: ')

            if int(choice) == 1:
                self.allTickets.getTickets(credentials, change=1)
            if int(choice) == 2:
                self.allTickets.getTickets(credentials, change=-1)



if __name__ == '__main__':
    view = Display()


            
