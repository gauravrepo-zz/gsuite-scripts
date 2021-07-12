from __future__ import print_function
from os import name
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/admin.directory.user', 'https://www.googleapis.com/auth/admin.directory.group', 'https://www.googleapis.com/auth/admin.directory.group.member']

# Before running the script copy your google API authorization file in client_secrets.json

CLIENT_SECRETS_FILE = os.path.abspath('client_secrets.json')

USER_EMAIL = input("Enter the email address of account, you want to offboard: ")

def main():
    """Shows basic usage of the Admin SDK Directory API.
    """

    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CLIENT_SECRETS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('admin', 'directory_v1', credentials=creds)

    #Call the Admin SDK Directory API

    user = service.users().get(userKey = USER_EMAIL).execute()
    print(user)
    print('Suspending user and moving to terminated OU')

    body = {
        'suspended': 'true',
        'orgUnitPath': "/Terminated"
    }

    updateUser = service.users().update(userKey = USER_EMAIL, body=body).execute()
    print(updateUser)
    
    print('List of Groups the user account is member of')
    groups = service.groups().list(userKey=USER_EMAIL).execute()
    
    if 'groups' in groups:
        for group in groups['groups']:
            print(group['name'])
        print('Removing user from the groups')

        for group in groups['groups']:
            group_email = group['email']
            r = service.members().delete(groupKey=group_email, memberKey=USER_EMAIL).execute()

        print('user removed from the groups')
    else:
        print('no groups found')
        


if __name__ == '__main__':
    main()