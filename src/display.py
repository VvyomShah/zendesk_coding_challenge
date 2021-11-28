from authenticate import Authenticate
from tickets import Tickets
from datetime import datetime

class Display:

    def __init__(self):
        self.Auth = Authenticate()
        self.allTickets = Tickets()
        self.credentials = (self.Auth.USERNAME, self.Auth.PASSWORD)
        self.allTickets.getTickets(self.credentials, change = 0)
        if self.allTickets.current_tickets != None:
            self.displayTickets(self.allTickets.current_tickets)
            self.displayMenu()
    
    def displayMenu(self):
        while True:
            print('(1) - Next page \n(2) - Previous page \n(3) - Select Ticket by Ticket ID \n')
            choice = input('Enter Choice: ')

            try:
                choice = int(choice)
            except ValueError:
                print('Please enter an integer')
                continue

            if choice == 1:
                self.allTickets.getTickets(self.credentials, change = 1)
                self.displayTickets(self.allTickets.current_tickets)

            elif choice == 2:
                self.allTickets.getTickets(self.credentials, change = -1)
                self.displayTickets(self.allTickets.current_tickets)
            
            elif choice == 3:
                ticket_id = input('Enter Ticket ID: ')
                try:
                    ticket_id = int(ticket_id)
                except ValueError:
                    print('Please enter an integer')
                    continue

                print('\n')
                ticket = self.allTickets.getSingleTicket(self.credentials, ticket_id)
                if ticket != None:
                    self.displaySingleTicket(ticket)
                else:
                    self.displayTickets(self.allTickets.current_tickets)
            
            else:
                print('Please enter a valid choice between 1 and 3')
                continue
                

    
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
        print(f'Ticket ID: {ticket_id}')
        print(f'Subject: {subject}')
        print(f'Status: {status}')
        print(f'Created At: {created_at}')
        print(f'Last Updated: {updated_at}')
        print(f'Submitted By: {submitted_by}')
        print(f'Assigned To: {assigned_to}')
        print('\n')
        print(f'Description: {description}')
        print('\n')
