import gspread
import os
from dotenv import load_dotenv

load_dotenv()

CREDENTIALS_FILE_PATH = 'app/service_account.json'
SHEET_ID = os.getenv("SHEET_ID")

def fill_sheets(data: list, check: bool):
    try:
        client = gspread.service_account(filename=CREDENTIALS_FILE_PATH)

        sheet = client.open_by_key(SHEET_ID)
        worksheet = sheet.get_worksheet(0)
        all_data = worksheet.get_all_values()
        for i in range(2, len(all_data)):
            if all_data[i][0] == "":
                range_to_update = f"A{i + 1}:C{i + 1}"
                worksheet.update(range_name=range_to_update, values=[data[:-1]])
                if check:
                    worksheet.update_cell(row=i + 1, col=4, value=data[-1])
                else:
                    worksheet.update_cell(row=i + 1, col=5, value=data[-1])
                break
        print("Complete")

    except gspread.exceptions.APIError as e:
        print(f"API Error {e}")
    except FileNotFoundError:
        print("File doesn't exist")