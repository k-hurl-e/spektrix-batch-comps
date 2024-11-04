# Spektrix to Google Sheets Automated Reporting

## Introduction

[Spektrix](https://www.spektrix.com/) is a ticketing and CRM platform specifically designed for the performing arts sector. As someone who works in the performing arts, I was excited to discover Spektrix's robust API capabilities. While Spektrix provides built-in reporting tools, I wanted to create a customized automated reporting system that would:

1. Pull specific data points I frequently need
2. Automatically update Google Sheets (which I use for simple data visualization)
3. Run without manual intervention
4. Utilize free tools to keep costs minimal

This project demonstrates how to connect Spektrix's API with Google Sheets to create automated daily and weekly reports for ticket sales, capacity tracking, and revenue analysis.

## How It Works

The system performs several key functions:

### 1. Daily Updates
- Tracks daily ticket sales
- Monitors booking status for each performance instance
- Calculates and records capacity metrics
- Updates designated Google Sheets with fresh data

### 2. Weekly Updates (Mondays)
- Calculates average ticket prices
- Compares pricing trends
- Updates weekly summary data

Reference to main execution flow:

```12:34:main.py
def main():
    orders = get_orders_by_confirmation_date(api_user, api_key, client_name, confirmation_date)
    processed_orders = process_orders(orders, event_id)
    total_tickets = calculate_total_tickets(processed_orders)
    instance_statuses = get_event_instances_statuses(api_user, api_key, client_name, event_id, start_date)

    # Update daily ticket sales sheet
    SHEET_NAME = 'GMCT_DAILY_TICKET_SALES_DATA' 
    update_sheet_daily_tickets(total_tickets, pretty_date, SHEET_NAME)

    # Update booked per instance sheet
    SHEET_NAME = 'GMCT_BOOKED_PER_INSTANCE_DATA' 
    update_sheet_booked_per_instance(instance_statuses, SHEET_NAME)

    # Update capacity summary sheet
    SHEET_NAME = 'GMCT_CAPACITY_DATA'
    update_sheet_capacity_summary(calculate_event_capacity_summary(instance_statuses), SHEET_NAME)

    # Get weekly data
    if datetime.now().weekday() == 0:  # Check if today is Monday
        SHEET_NAME = 'GMCT_AVG_PRICE_DATA'
        update_sheet_weekly_ticket_price(SHEET_NAME)
```


## Setup

### Prerequisites
- Python 3.7+
- Spektrix API access
- Google Cloud Platform account with Sheets API enabled
- Service account credentials from Google Cloud Console

### Installation

1. Clone the repository
2. Install required packages:
```bash
pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file with the following variables:

```plaintext
# Spektrix API Credentials
SPEKTRIX_API_USER=your_api_user
SPEKTRIX_API_KEY=your_api_key
SPEKTRIX_CLIENT_NAME=your_client_name

# Google Sheets
SPREADSHEET_ID=your_spreadsheet_id
SERVICE_ACCOUNT_JSON={'your_service_account_json'}

# Event Configuration
EVENT_ID=your_event_id
START_DATE=YYYY-MM-DD
PERFORMANCES=number_of_performances
EXTRA_LOCKS=number_of_extra_locks_per_instance_if_any
```

## Data Collection & Reporting

### 1. Daily Ticket Sales Data
- Records total tickets sold per day

### 2. Performance Instance Data
- Tracks sold, available, and locked seats for each performance

### 3. Capacity Summary
- Calculates total and percentage-based capacity metrics

### 4. Weekly Price Analysis
- Monitors average ticket prices
- Compares against historical data

Reference to weekly data processing:

```9:43:weekly.py
def get_weekly_orders():
    # Get dates for the past week
    end_date = datetime.now() - timedelta(days=1)  # Yesterday
    start_date = end_date - timedelta(days=6)  # 7 days ago
    
    # Initialize dictionary to store daily totals
    weekly_data = {}
    
    # Loop through each day of the week
    current_date = start_date
    while current_date <= end_date:
        date_str = current_date.strftime("%Y-%m-%d")
        pretty_date = current_date.strftime("%m/%d/%Y")
        
        # Get orders for this date using functions from orders.py
        orders = get_orders_by_confirmation_date(
            api_user=api_user,
            api_key=api_key,
            client_name=client_name,
            confirmation_date=date_str
        )
        processed_orders = process_orders(orders, event_id)
        total_tickets = calculate_total_tickets(processed_orders)
        
        # Store the results
        weekly_data[pretty_date] = {
            'tickets': total_tickets if isinstance(total_tickets, int) else 0,
            'orders': len(processed_orders) if isinstance(processed_orders, list) else 0,
            'revenue': sum(float(order['Ticket Revenue']) for order in processed_orders) if isinstance(processed_orders, list) else 0
        }
        
        # Move to next day
        current_date += timedelta(days=1)
    
    return weekly_data
```


## Google Sheets Integration

The system uses Google Sheets API to:
- Clear and update existing data
- Append new rows
- Maintain historical data
- Enable automatic chart updates

Reference to Google Sheets operations:

```24:117:newrows.py
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
```


## Security Notes

- API credentials are stored in environment variables
- Google service account credentials should be kept secure
- The `.gitignore` file excludes sensitive credentials

## Contributing

Feel free to fork this repository and adapt it to your needs. Pull requests are welcome for improvements or bug fixes. Hoping to add additional functionality in the future.

## License

This project is licensed under the MIT License - see the LICENSE file for details.