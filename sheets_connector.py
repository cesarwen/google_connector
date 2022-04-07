# import the required libraries
from __future__ import print_function
import pickle
import os.path
import pandas as pd

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


import sys


class SheetsAPI:


    def __init__(self):
        """ 
        ## Description

        - Object that helps you to connect to the google API given the oauth credentials tonken 

        ## Functions

        - __init__ it needs the path to the credentials token
        - 
        - ReadFromSheets: given sheets parameters reads the contents in the google sheets and writes it to a dataframe
        """
        SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
        service_name = 'sheets'
        api_version = 'v4'

        # Variable self.creds will
        # store the user access token.
        # If no valid token found
        # we will create one.
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
                self.creds = flow.run_local_server()

            # Save the access token in token.pickle
            # file for future usage
            with open(f'{current_path}/token_{service_name}_{api_version}.pickle', 'wb') as token:
                pickle.dump(self.creds, token)
        self.service = build(service_name, api_version, credentials=self.creds)

    def InsertToSheets(
        self,
        spreadsheet_id,
        df,
        worksheet_name,
        cell_range_insert='A1',
        major_dimension='ROWS',
        input_options='USER_ENTERED',
        use_comma=False
    ):
        """
        # Parameters:
        - spreadsheet_id: the id from the google sheets to be inserted into
        - df: dataframe to be inserted into google sheets
        - worksheet_name: name of the tab for the data to be inserted
        - cell_range_insert: withing the tab in with location it should be added
        - major_dimensions: orientation from the data
        - input_options: to be logged as a user os as formula
        - use_comma: to use comma as decimal separator


        """

        # standard parameters treatment
        worksheet_name += "!"
        columns = df.columns

        # Transforms all the contents in the datafram into text
        for column in columns:
            df[column] = df[column].map(str)
            if (use_comma == "TRUE"):
                df[column] = df[column].str.replace('.', ',', regex=False)

        # inputs the data into the google sheets with the google sheets api
        try:
            values = df.T.reset_index().T.values.tolist()
            value_range_body = {
                'majorDimension': major_dimension,
                'values': values
            }
            self.service.spreadsheets().values().update(
                spreadsheetId=spreadsheet_id,
                valueInputOption=input_options,
                range=worksheet_name + cell_range_insert,
                body=value_range_body
            ).execute()
            return True
        except Exception as err:
            # Return False if something went wrong
            print(err)
            return False

    def ReadFromSheets(
        self,
        spreadsheet_id:str,
        worksheet_name:str,
        cell_range_read:str='A1',
        header:bool=False,
        dropna:bool=True
    ):
        """
        # Parameters:
        - spreadsheet_id: the id from the google sheets to be inserted into
        - worksheet_name: name of the tab for the data to be inserted
        - cell_range_read: withing the tab in with location it should be added (sheets notation)
        - header: uses first row as header for the dataframe
        - dropna: removes lines with empty data

        """
        try:
            # standard parameters treatment
            sheet = self.service.spreadsheets()
            worksheet_name += "!"
            result = sheet.values().get(
                spreadsheetId=spreadsheet_id,
                range=worksheet_name + cell_range_read).execute()
            values = result.get('values', [])
            df = pd.DataFrame(values)

            # Makes the first row header
            if(header):
                df.columns = df.iloc[0]  # set the header row as the df header
                df = df[1:]  # take the data less the header row
            if(dropna):
                df.dropna(inplace=True)
            return(df)
        except Exception as err:
            print(err)
            # Raise UploadError if file is not uploaded.
            # print("Something went wrong")
            return()

# %% For local testing of the object
# if __name__ == "__main__":
#     obj = SheetsAPI()
#     df = pd.DataFrame([[1,2,3],[4,5,6]])
# obj.InsertToSheets('1_0ZvEUSl8Y5kRc4V9blYIMhAmUWgQYYiVNuN7pPrDyk',df,'Queries','B21')
# print("this {}".format(obj.ReadFromSheets('1_0ZvEUSl8Y5kRc4V9blYIMhAmUWgQYYiVNuN7pPrDyk','Queries','B6:D12',True)))
