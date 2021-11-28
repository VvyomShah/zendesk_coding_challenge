import credentials
import requests
import os

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
        if response.status_code == 401:
            print('Invalid Credentials')
            quit()
        if response.status_code == 404:
            print('Ticket(s) not found.')
            return
        if response.status_code == 429:
            print('Resource limit exhausted. Please try again later.')
        if response.status_code == 200:
            return response.json()
    

    def getSingleTicket(self, credentials, ticket_id):
        return self.request(f'api/v2/tickets/{ticket_id}.json', credentials=credentials, payload = {"ticket_id": ticket_id})

    def getTickets(self, credentials, change=0):
        if change == 0: 
            ticketsData = self.request('api/v2/tickets.json', credentials=credentials, payload = {"page[size]": "25"})
        
        elif change == 1:
            ticketsData = self.request('api/v2/tickets.json', credentials=credentials, payload = {"page[size]": "25", "page[after]": self.after})
            if ticketsData and ticketsData['meta']['has_more'] == False:
                print('No more tickets to display.\n')
                return

        elif change == -1:
            ticketsData = self.request('api/v2/tickets.json', credentials=credentials, payload = {"page[size]": "25", "page[before]": self.before})
            if ticketsData and ticketsData['meta']['has_more'] == False:
                print('No more previous tickets to display.\n')
                return

        self.has_more = ticketsData['meta']['has_more']
        self.before = ticketsData['meta']['before_cursor']
        self.after = ticketsData['meta']['after_cursor']
        self.current_tickets = ticketsData['tickets']