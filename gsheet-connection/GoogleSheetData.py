#%%
import os.path
import pandas as pd 
import json

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

'''
PREREQUISITES:
  Get an environment variable called GOOGLE_CREDS with the json of credentials
  used to access google API (cf. 1Password)

'''

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]


class GoogleSheetData:
  """ Class that handles data requests about google sheets
  """

  def __init__(self):
    """ Connects to gsheet using env variable GOOGLE_CREDS (1st time connecting)
    or local file token.json if exists (subsequent connections).  
    """

    credentials = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
      credentials = Credentials.from_authorized_user_file("token.json", SCOPES)

    # If there are no (valid) credentials available, let the user log in.
    if not credentials or not credentials.valid:
      if credentials and credentials.expired and credentials.refresh_token:
        credentials.refresh(Request())
      else:
        config = json.loads(os.environ['GOOGLE_CREDS'])
        flow = InstalledAppFlow.from_client_config(
            config, SCOPES)

        credentials = flow.run_local_server(port=0)

      # Save the credentials for the next run
      with open("token.json", "w") as token:
        token.write(credentials.to_json())

    self.creds = credentials
    return print('Connected to GSheets')


  def get_dataframe(self, spreadsheet_id, worksheet_name, range_name, headers=1):
    """ Returns pandas dataframe from a spreadsheet.
      :param spreadsheet_id:  ID of the spreadhsheet, found in its URL: str
      :param worksheet_name:  name of worksheet e.g. "Sheet1": str
      :param range_name:      range to take into account e.g. "A1:E15": str
      :param headers:         whether selection has headers (1) or not (0). Default 1: int

      :return:                pandas dataframe of the selection
    """

    total_range = worksheet_name + '!' + range_name

    try:
      service = build("sheets", "v4", credentials=self.creds)

      # Call the Sheets API
      sheet = service.spreadsheets()
      result = (
          sheet.values()
          .get(spreadsheetId=spreadsheet_id, range=total_range)
          .execute()
      )
      values = result.get("values", [])

      if not values:
        print("No data found.")
        return
      
      if headers > 0:
        df = pd.DataFrame(values[1:], columns=values[0])
      else:
        df = pd.DataFrame(values)

      return df

    except HttpError as err:
      print(err)


  def write_dataframe(self, df, spreadsheet_id, worksheet_name, row=1, col=1):
    """ Writes a dataframe into a google worksheet.
      :param df:                  pandas dataframe to write to GSheet: df
      :param spreadsheet_id:      ID of the spreadhsheet, found in its URL: str
      :param worksheet_name:      name of worksheet, e.g. "Sheet1": str
      :param row:                 row number where df is going to be written, default 1: int
      :param col:                 column number where df is going to be written, default 1: int
      
      :return:                    dict of spreadsheet & range that has been updated, with which cells have been written on: dict
    """

    col_letter_start = chr(ord('@') + col) # Transforms a column nb into a letter, e.g. 2 -> B
    row_number_start = row

    range_name = col_letter_start + str(row_number_start)
    total_range = worksheet_name + '!' + range_name

    try:
      service = build("sheets", "v4", credentials=self.creds)

      col_names = [df.columns.values.tolist()]
      values = col_names + df.values.tolist()

      body = {"values": values}

      result = (
          service.spreadsheets()
          .values()
          .update(
              spreadsheetId=spreadsheet_id,
              range=total_range,
              valueInputOption="USER_ENTERED",
              body=body,
          )
          .execute()
      )
      return result
    
    except HttpError as error:
      print(f"An error occurred: {error}")
      return error
    

  def clear_worksheet(self, spreadsheet_id, worksheet_name):
    """ Clears data from a worksheet
      :param spreadsheet_id:      ID of the spreadhsheet, found in its URL: str
      :param worksheet_name:      name of worksheet, e.g. "Sheet1": str

      :return:                    dict of spreadsheet & range that has been cleared: dict
    """

    try:
      service = build("sheets", "v4", credentials=self.creds)

      result = (
          service.spreadsheets()
          .values()
          .clear(
              spreadsheetId=spreadsheet_id,
              range=worksheet_name,
          )
          .execute()
      )
      return result
    
    except HttpError as error:
      print(f"An error occurred: {error}")
      return error

#%%

# if __name__ == "__main__":
  # print(creds)
gs = GoogleSheetData()
df = gs.get_dataframe("1R3Bw9aUNvJm-1HxPTYLJyDPT9Vt0mINwQI2bq1HMfxA", "Sheet1", "A1:B100", 1)
str(df.values.tolist())
#%%
result = gs.write_dataframe(df, "1R3Bw9aUNvJm-1HxPTYLJyDPT9Vt0mINwQI2bq1HMfxA", "Sheet2", 3, 2)
#   print(df)
print(result)

#%%
gs = GoogleSheetData()
gs.clear_worksheet("1R3Bw9aUNvJm-1HxPTYLJyDPT9Vt0mINwQI2bq1HMfxA", "Sheet2")
# %%
worksheet_name = 'Sheet2'
# %%
np.empty([100, 26], dtype=object)
# %%
