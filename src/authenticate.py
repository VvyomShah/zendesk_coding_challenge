import getpass

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
        self.USERNAME = input('Username: ')
        try:
            self.PASSWORD = getpass.getpass('Password: ')
        except Exception as error:
            print('ERROR', error)