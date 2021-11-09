# client id = 113346928299-g777fst21ktjkm5eqtdp9s6ia1a75m7p.apps.googleusercontent.com
# client secret = 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

from __future__ import print_function
import os.path
import io
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# If modifying these scopes, delete the file token.json.
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload

SCOPES = ['https://www.googleapis.com/auth/drive']


def main():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
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
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('drive', 'v3', credentials=creds)

    # Call the Drive v3 API

    # Searching For A File
    # results = service.files().list(pageSize=10, fields="nextPageToken, files(id, name)", q="name='input.txt'").execute()
    # items = results.get('files', [])
    #
    # if not items:
    #     print('No files found.')
    # else:
    #     print('Files:')
    #     for item in items:
    #         print(u'{0} ({1})'.format(item['name'], item['id']))

    # Uploading a File
    # file_metadata = {'name': "input.txt"}
    # filePath = "input.txt"
    # media = MediaFileUpload(filePath, mimetype="text/plain")
    # file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    # fileID = file.get('id')
    # print('File ID: ' + fileID)

    # Downloading A File
    request = service.files().get_media(fileId='1RiC3TBKkUIh6Fkb8P9Om2KFQbbpH_q15')
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print("Download %d%%." % int(status.progress() * 100))
    with io.open("Downloads/dinput.txt", "wb") as f:
        fh.seek(0)
        f.write(fh.read())


if __name__ == '__main__':
    main()
