import os
import json
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.oauth2 import service_account
from datetime import datetime, timezone, timedelta
from weekly import get_average_ticket_price, get_weekly_orders

from credentials import SPREADSHEET_ID
from service_account_creds import get_service_account_creds

# Set up Google Sheets API credentials
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# For local testing - DELETE BEFORE DEPLOYING
service_account_info = get_service_account_creds()

creds = service_account.Credentials.from_service_account_info(
    service_account_info, scopes=SCOPES)

# Connect to the Google Sheets API
service = build('sheets', 'v4', credentials=creds)

def update_sheet_booked_per_instance(instances_data, sheet_name):
    values = []
    for performance_time, data in instances_data.items():
        values.append([
            performance_time,
            data['sold'],
            data['available'],
            data['locked']
        ])

    body = {
        'values': values
    }

    # Clear existing data starting from row 2
    clear_range = f'{sheet_name}!A2:D'
    service.spreadsheets().values().clear(
        spreadsheetId=SPREADSHEET_ID,
        range=clear_range
    ).execute()

    # Update with new data starting from row 2
    try:
        result = service.spreadsheets().values().update(
            spreadsheetId=SPREADSHEET_ID,
            range=f'{sheet_name}!A2',
            valueInputOption='RAW',
            body=body
        ).execute()

        if result and 'updates' in result:
            print(f"{result['updates'].get('updatedRows', 0)} rows updated in {sheet_name}.")
        else:
            print(f"Update operation completed, but no 'updates' information returned for {sheet_name}.")
    except Exception as e:
        print(f"An error occurred while updating {sheet_name}: {str(e)}")
        # You might want to re-raise the exception or handle it differently based on your needs
        raise

def update_sheet_daily_tickets(total_tickets, confirmation_date, sheet_name):
    values = [[confirmation_date.strip("'"), total_tickets]]  # Remove any leading/trailing ' from the date

    body = {
        'values': values
    }

    result = service.spreadsheets().values().append(
        spreadsheetId=SPREADSHEET_ID,
        range=f'{sheet_name}!A1',
        valueInputOption='USER_ENTERED',  
        insertDataOption='INSERT_ROWS',
        body=body
    ).execute()

    print(f"{result.get('updates').get('updatedRows')} rows appended to {sheet_name}.")

def update_sheet_capacity_summary(capacity_summary, sheet_name):
    values = [
        [
            (datetime.now(timezone.utc) - timedelta(days=1)).strftime('%m-%d-%Y'),
            capacity_summary['total_sold'],
            capacity_summary['total_locked'],
            capacity_summary['total_available'],
            f"=TO_PERCENT({capacity_summary['percent_sold']})",
            f"=TO_PERCENT({capacity_summary['percent_locked']})",
            f"=TO_PERCENT({capacity_summary['percent_available']})"
        ]
    ]

    body = {
        'values': values
    }

    result = service.spreadsheets().values().append(
        spreadsheetId=SPREADSHEET_ID,
        range=f'{sheet_name}!A1',
        valueInputOption='USER_ENTERED',
        insertDataOption='INSERT_ROWS',
        body=body
    ).execute()

    print(f"{result.get('updates').get('updatedRows')} rows appended to {sheet_name}.")

def update_sheet_weekly_ticket_price(sheet_name):
    values = [[datetime.now().strftime('%m/%d/%Y'), "GMCT weekly", get_average_ticket_price(get_weekly_orders()), "27.11", "23.22", "26.77", "13.82", "=AVERAGE(C:C)", "30.00"]]
    body = {'values': values}
    result = service.spreadsheets().values().append(
        spreadsheetId=SPREADSHEET_ID,
        range=f'{sheet_name}!A1',
        valueInputOption='USER_ENTERED',
        insertDataOption='INSERT_ROWS',
        body=body
    ).execute()
    print(f"{result.get('updates').get('updatedRows')} rows appended to {sheet_name}.")
    