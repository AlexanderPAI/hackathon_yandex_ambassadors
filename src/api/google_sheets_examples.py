import os
from pathlib import Path

from dotenv import load_dotenv
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from .utils import YEAR_MONTHS

# installed packages for Google Sheets API:
# - google-api-python-client
# - google-auth-httplib2
# - google-auth-oauthlib


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
    return result.get("values", [])


# TODO: add logger
def authenticate_sheets_by_oauth_credentials():
    """Grants access to Google Sheets API using credentials.json file."""
    credentials = None
    if os.path.exists("token.json"):
        credentials = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            credentials_path = os.path.join(
                Path(__file__).parent.parent, "credentials.json"
            )
            flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
            credentials = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(credentials.to_json())
    return credentials


def get_private_sheet_values(sheet_id: str, cell_range: str) -> list[str] | None:
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
        print(f"An error occurred: {error}")


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
        print(f"An error occurred: {error}")


def create_new_sheet_example(title: str) -> str:
    """Creates the Sheet the user has access to using credentials.json file."""
    try:
        service = build(
            "sheets", "v4", credentials=authenticate_sheets_by_oauth_credentials()
        )
        spreadsheet_properties = {
            "properties": {"title": title, "locale": "ru", "timeZone": "Europe/Moscow"},
            "sheets": [{"properties": {"title": "Заявки на мерч"}}],
        }
        spreadsheet = (
            service.spreadsheets().create(body=spreadsheet_properties).execute()
        )
        return spreadsheet.get("spreadsheetUrl")
    except HttpError as error:
        return error


def create_merch_applications_sheet(all_applications_qs) -> str:
    """Creates new empty spreadsheet for merch applications."""

    try:
        service = build(
            "sheets", "v4", credentials=authenticate_sheets_by_oauth_credentials()
        )
        sheets = service.spreadsheets()
        worksheet_name = "Заявки на мерч"
        spreadsheet_properties = {
            "properties": {
                "title": "Отправка мерча",
                "locale": "ru",
                "timeZone": "Europe/Moscow",
            },
            "sheets": [{"properties": {"title": worksheet_name}}],
        }
        spreadsheet = sheets.create(body=spreadsheet_properties).execute()
        spreadsheet_id = spreadsheet.get("spreadsheetId")
        column_names = [
            (
                "id заявки",
                "номер заявки",
                "куратор",
                "мерч",
                "количество",
                "размер толстовки",
                "размер носков",
                "ФИО",
                "индекс",
                "страна",
                "город",
                "улица, дом, квартира",
                "телефон",
                "дата и время создания",
                "месяц",
            )
        ]
        value_range_body = {"majorDimension": "ROWS", "values": column_names}
        sheets.values().update(
            spreadsheetId=spreadsheet_id,
            valueInputOption="RAW",
            range=f"{worksheet_name}!A1",
            body=value_range_body,
        ).execute()

        all_applications_list = list(all_applications_qs)
        for row in range(2, len(all_applications_list) + 2):
            item = all_applications_list.pop()

            values = [
                (
                    item.id,
                    item.application_number,
                    item.tutor.get_full_name(),
                    item.merch_in_applications.all()[0].merch.name,
                    item.merch_in_applications.all()[0].quantity,
                    item.ambassador.clothing_size,
                    item.ambassador.shoe_size,
                    item.ambassador.name,
                    item.ambassador.address.postal_code,
                    item.ambassador.address.country,
                    item.ambassador.address.city,
                    item.ambassador.address.street,
                    item.ambassador.phone_number,
                    item.created.isoformat(),
                    YEAR_MONTHS[item.created.month - 1][2],
                )
            ]
            sheets.values().update(
                spreadsheetId=spreadsheet_id,
                valueInputOption="RAW",
                range=f"{worksheet_name}!A{row}",
                body={"values": values},
            ).execute()

        return spreadsheet.get("spreadsheetUrl")
    except HttpError as error:
        print(error)
        return error


if __name__ == "__main__":
    dotenv_path = os.path.join(Path(__file__).parent.parent, "config", ".env")
    load_dotenv(dotenv_path)
    # cell_range = CELL_RANGE.format(sheet_name="Sheet1", cells="A1:D3")
    # print(get_public_sheet_values(SPREADSHEET_PUBLIC_ID, cell_range))
    # print(get_private_sheet_values(SPREADSHEET_PRIVATE_ID, cell_range))
    # print(
    #     write_to_private_sheet(
    #         SPREADSHEET_PRIVATE_ID, sheet_name="Sheet1", first_row=2, last_row=3
    #     )
    # )
    print(create_new_sheet_example("Отправка мерча"))
