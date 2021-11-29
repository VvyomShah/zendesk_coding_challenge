import unittest
import json

class displayTest(unittest.TestCase):

    def test_displayTickets(self):

        f = open('/home/vvyom/Desktop/Assignments/zendesk_coding_challenge/test/samples/sample_tickets.json')
        tickets = json.load(f)
        f.close()

        self.assertTrue(tickets, dict)
        self.assertLessEqual(len(list(tickets.keys())), 25)

    def test_displaySingleTicket(self):

        f = open('/home/vvyom/Desktop/Assignments/zendesk_coding_challenge/test/samples/sample_ticket.json')
        single_ticket = json.load(f)
        f.close()

        self.assertTrue(single_ticket, dict)
        self.assertTrue(single_ticket['ticket']['id'], int)                

if __name__ == '__main__':
    unittest.main()