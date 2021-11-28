from datetime import datetime
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
    

    def getSingleTicket(self, credentials, ticket_id):
        return self.request(f'api/v2/tickets/{ticket_id}.json', credentials=credentials, payload = {"ticket_id": ticket_id})

    def getTickets(self, credentials, change=0):
        if change == 0: 
            ticketsData = self.request('api/v2/tickets.json', credentials=credentials, payload = {"page[size]": "25"})
        
        elif change == 1:
            ticketsData = self.request('api/v2/tickets.json', credentials=credentials, payload = {"page[size]": "25", "page[after]": self.after})
            if ticketsData['meta']['has_more'] == False:
                print('No more tickets to display.\n')
                return

        elif change == -1:
            ticketsData = self.request('api/v2/tickets.json', credentials=credentials, payload = {"page[size]": "25", "page[before]": self.before})
            if ticketsData['meta']['has_more'] == False:
                print('No more previous tickets to display.\n')
                return

        self.has_more = ticketsData['meta']['has_more']
        self.before = ticketsData['meta']['before_cursor']
        self.after = ticketsData['meta']['after_cursor']
        self.current_tickets = ticketsData['tickets']
        

class Display:

    def __init__(self):
        self.Auth = Authenticate()
        self.allTickets = Tickets()
        self.credentials = (self.Auth.USERNAME, self.Auth.PASSWORD)
        self.allTickets.getTickets(self.credentials, change = 0)
        self.displayTickets(self.allTickets.current_tickets)
        self.displayMenu()
    
    def displayMenu(self):
        while True:
            print('(1) - Next page \n(2) - Previous page \n(3) - Select Ticket by Ticket ID \n')
            choice = input('Enter Choice: ')

            if int(choice) == 1:
                self.allTickets.getTickets(self.credentials, change = 1)
                self.displayTickets(self.allTickets.current_tickets)

            elif int(choice) == 2:
                self.allTickets.getTickets(self.credentials, change = -1)
                self.displayTickets(self.allTickets.current_tickets)
            
            elif int(choice) == 3:
                ticket_id = input('Enter Ticket ID: ')
                print('\n')
                ticket = self.allTickets.getSingleTicket(self.credentials, ticket_id)
                self.displaySingleTicket(ticket)
                

    
    def printTicket(self, ticket):
        ticket_id = ticket['id']
        submitted_by = ticket['submitter_id']
        assigned_to = ticket['assignee_id']
        subject = ticket['subject']
        created_at = str(datetime.strptime(ticket['created_at'], '%Y-%m-%dT%H:%M:%SZ'))

        print_format = "{:{fill}{align}{width}}"
        print(
            print_format.format(ticket_id, fill='', align='<', width=15) + 
            print_format.format(subject, fill='', align='<', width=80) + 
            print_format.format(created_at, fill='', align='<', width=25) +
            print_format.format(submitted_by, fill='', align='<', width=15) +
            print_format.format(assigned_to, fill='', align='<', width=15))
        
    
    def displayTickets(self, tickets):
        print_format = "{:{fill}{align}{width}}"
        print(
            print_format.format('Ticket ID', fill='', align='<', width=15) + 
            print_format.format('Subject', fill='', align='<', width=80) + 
            print_format.format('Date Create On', fill='', align='<', width=25) +
            print_format.format('Submitted By', fill='', align='<', width=15) +
            print_format.format('Assigned To', fill='', align='<', width=15))

        for ticket in tickets:
            self.printTicket(ticket)

    def displaySingleTicket(self, ticket):
        ticket = ticket['ticket']
        ticket_id = ticket['id']
        submitted_by = ticket['submitter_id']
        assigned_to = ticket['assignee_id']
        subject = ticket['subject']
        created_at = str(datetime.strptime(ticket['created_at'], '%Y-%m-%dT%H:%M:%SZ'))
        updated_at = str(datetime.strptime(ticket['updated_at'], '%Y-%m-%dT%H:%M:%SZ'))
        description = ticket['description']
        status = ticket['status']
        if ticket['tags'] is list:
            tags = ''.join([tag + ', ' for tag in ticket['tags']])
        else:
            tags = None
        print(f'Ticket ID: {ticket_id}')
        print(f'Subject: {subject}')
        print(f'Created At: {created_at}')
        print(f'Last Updated: {updated_at}')
        print(f'Submitted By: {submitted_by}')
        print(f'Assigned To: {assigned_to}')
        print('\n')
        print(f'Description: {description}')
        print('\n')





if __name__ == '__main__':
    view = Display()
