import logging
import gspread
import os
from dotenv import load_dotenv

load_dotenv()

CREDENTIALS_FILE_PATH = os.getenv("CREDENTIALS_PATH")
SHEET_ID = os.getenv("SHEET_ID")
INCOME_COLUMN = 4
EXPENSE_COLUMN = 5
START_ROW = 2

logging.basicConfig(level=logging.INFO)

def fill_data_sheets(data: list, check: bool):
    try:
        client = gspread.service_account(filename=CREDENTIALS_FILE_PATH)

        sheet = client.open_by_key(SHEET_ID)
        worksheet = sheet.get_worksheet(0)
        all_data = worksheet.get_all_values()
        for i in range(START_ROW, len(all_data)):
            if all_data[i][0] == "":
                range_to_update = f"A{i + 1}:C{i + 1}"
                worksheet.update(range_name=range_to_update, values=[data[:-1]])
                if check:
                    worksheet.update_cell(row=i + 1, col=INCOME_COLUMN, value=data[-1])
                else:
                    worksheet.update_cell(row=i + 1, col=EXPENSE_COLUMN, value=data[-1])
                break

    except gspread.exceptions.APIError:
        raise ValueError("Sheets API error")
    except FileNotFoundError:
        raise ValueError("Service_account doesn't existing")