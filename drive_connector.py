# Based on:
# https://www.geeksforgeeks.org/upload-and-download-files-from-google-drive-storage-using-python/

# import the required libraries
from __future__ import print_function
import pickle
import os.path
import io
import shutil
# import requests
from mimetypes import MimeTypes
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload


class DriveAPI:

    global SCOPES

    # Define the scopes
    SCOPES = ['https://www.googleapis.com/auth/drive']

    def __init__(self):
        service_name = 'drive'
        api_version = 'v3'
        self.creds = None
        current_path = os.path.dirname(__file__)

        # The file token.pickle stores the
        # user's access and refresh tokens. It is
        # created automatically when the authorization
        # flow completes for the first time.

        # Check if file token.pickle exists
        if os.path.exists(f'{current_path}/token_{service_name}_{api_version}.pickle'):

            # Read the token from the file and
            # store it in the variable self.creds
            with open(f'{current_path}/token_{service_name}_{api_version}.pickle', 'rb') as token:
                self.creds = pickle.load(token)

        # If no valid credentials are available,
        # request the user to log in.
        if not self.creds or not self.creds.valid:

            # If token is expired, it will be refreshed,
            # else, we will request a new one.
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    f'{current_path}/credentials.json', SCOPES)
                self.creds = flow.run_local_server(port=0)

            # Save the access token in token.pickle
            # file for future usage
            with open(f'{current_path}/token_{service_name}_{api_version}.pickle', 'wb') as token:
                pickle.dump(self.creds, token)

        # Connect to the API service
        self.service = build('drive', 'v3', credentials=self.creds)

        # request a list of first N files or
        # folders with name and id from the API.
        # results = self.service.files().list(
        #     pageSize=100,
        #     fields="files(id, name)",
        #     q="'1tl2tVcc3FBokIKSqQrqCAeuTY8Oa6LNJ' in parents and trashed=false"
        #     ).execute()
        # items = results.get('files', [])

        # print a list of files

        # print("Here's a list of files: \n")
        # print(*items, sep="\n", end="\n\n")

    def FileDownload(self, file_id, file_name):
        request = self.service.files().get_media(fileId=file_id)
        fh = io.BytesIO()

        # Initialise a downloader object to download the file
        downloader = MediaIoBaseDownload(fh, request, chunksize=204800)
        done = False

        try:
            # Download the data in chunks
            while not done:
                status, done = downloader.next_chunk()

            fh.seek(0)

            # Write the received data to the file
            with open(file_name, 'wb') as f:
                shutil.copyfileobj(fh, f)

            # Return True if file Downloaded successfully
            return True
        except Exception as err:
            print(err)
            # Return False if something went wrong
            return False

    def FolderDownload(self, folder_id, path=""):

        # Lists every file inside the given folder in order to get each file key
        results = self.service.files().list(
            pageSize=100,
            fields="files(id, name)",
            q="'{}' in parents and trashed=false".format(folder_id)).execute()
        # Using the file key downloads the files
        items = results.get('files', [])
        for item in items:
            self.FileDownload(item['id'], '{}/{}'.format(path, item['name']))

    def FileUpload(self, filepath):
        # Extract the file name out of the file path
        name = filepath.split('/')[-1]

        # Find the MimeType of the file
        mimetype = MimeTypes().guess_type(name)[0]

        # create file metadata
        file_metadata = {'name': name}

        try:
            media = MediaFileUpload(filepath, mimetype=mimetype)

            # Create a new file in the Drive storage
            self.service.files().create(
                body=file_metadata, media_body=media, fields='id').execute()

            print("File Uploaded.")

        except Exception as err:

            # Raise UploadError if file is not uploaded.
            print(err)

# %% For local testing of the object
# if __name__ == "__main__":
#     obj = DriveAPI()

#     obj.FolderDownload('1SauYlBU0gw21ggh7k-kIx099kBuNAtQM','queries')
