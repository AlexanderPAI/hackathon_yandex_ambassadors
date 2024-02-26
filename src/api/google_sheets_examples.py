import os
from pathlib import Path

from dotenv import load_dotenv
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# installed packages for Google Sheets API:
# - google-api-python-client
# - google-auth-httplib2
# - google-auth-oauthlib

# installed dev dependencies:
# - flake8
# - isort
# - black

dotenv_path = os.path.join(Path(__file__).parent.parent, "config", ".env")
load_dotenv(dotenv_path)

SPREADSHEET_PUBLIC_ID = "1VfxFH8l9bKNxD90NCAab_sqVL8nBmDWWgulxLOGOI7A"
SPREADSHEET_PRIVATE_ID = "1l43PvR4rRxh-Umu7zeeRMO_XYJAzf75ZJhjGBgtr-5A"
CELL_RANGE = "{sheet_name}!{cells}"  # cells pattern example: 'A1:D5'
API_KEY = os.getenv("GOOGLE_API_KEY")

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]


def authenticate_sheets_by_api_key(api_key: str):
    """
    Constructs a spreadsheets resource object using api key and returns this object.
    """
    return build("sheets", "v4", developerKey=api_key).spreadsheets()


def get_public_sheet_values(sheet_id: str, cell_range: str) -> list[str]:
    """
    Returns values from a selected range of cells in a public spreadsheet
    (visible to anyone with a link), no OAuth used.
    """
    sheets = authenticate_sheets_by_api_key(API_KEY)
    result = sheets.values().get(spreadsheetId=sheet_id, range=cell_range).execute()
    values = result.get("values", [])
    return values


def authenticate_sheets_by_oauth_credentials():
    """Grants access to Google Sheets API using credentials.json file."""
    credentials = None
    if os.path.exists("token.json"):
        credentials = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            # credentials.json file was placed in the root folder, if we want to move it
            # to another place, we need to figure out how to set the correct path to it
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            credentials = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(credentials.to_json())
    return credentials


def get_private_sheet_values(sheet_id: str, cell_range: str) -> list[str]:
    """
    Returns values from a selected range of cells in a private spreadsheet using OAuth.
    """
    try:
        service = build(
            "sheets", "v4", credentials=authenticate_sheets_by_oauth_credentials()
        )
        sheets = service.spreadsheets()
        result = sheets.values().get(spreadsheetId=sheet_id, range=cell_range).execute()
        values = result.get("values", [])
        return values
    except HttpError as error:
        print(error)


def write_to_private_sheet(
    sheet_id: str, sheet_name: str, first_row: int, last_row: int
) -> None:
    try:
        service = build(
            "sheets", "v4", credentials=authenticate_sheets_by_oauth_credentials()
        )
        sheets = service.spreadsheets()

        for row in range(first_row, last_row + 1):
            num1 = int(
                sheets.values()
                .get(spreadsheetId=sheet_id, range=f"{sheet_name}!E{row}")
                .execute()
                .get("values")[0][0]
            )
            num2 = int(
                sheets.values()
                .get(spreadsheetId=sheet_id, range=f"{sheet_name}!F{row}")
                .execute()
                .get("values")[0][0]
            )
            calculation_result = num1 + num2
            print(f"Processing {num1} + {num2}")

            sheets.values().update(
                spreadsheetId=sheet_id,
                range=f"{sheet_name}!G{row}",
                valueInputOption="USER_ENTERED",
                body={"values": [[f"{calculation_result}"]]},
            ).execute()

            sheets.values().update(
                spreadsheetId=sheet_id,
                range=f"{sheet_name}!H{row}",
                valueInputOption="USER_ENTERED",
                body={"values": [["Done"]]},
            ).execute()

    except HttpError as error:
        print(error)


if __name__ == "__main__":
    cell_range = CELL_RANGE.format(sheet_name="Sheet1", cells="A1:D3")
    print(get_public_sheet_values(SPREADSHEET_PUBLIC_ID, cell_range))
    print(get_private_sheet_values(SPREADSHEET_PRIVATE_ID, cell_range))
    print(
        write_to_private_sheet(
            SPREADSHEET_PRIVATE_ID, sheet_name="Sheet1", first_row=2, last_row=3
        )
    )
