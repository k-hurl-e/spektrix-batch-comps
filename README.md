# Spektrix to Google Sheets Automated Reporting

[Spektrix](https://www.spektrix.com/) is a ticketing and CRM platform specifically designed for the performing arts sector. While Spektrix provides great built-in reporting tools, I wanted to create a customized automated reporting system that would:

1. Pull specific data points I frequently need
2. Automatically update Google Sheets (which I use for simple data visualization)
3. Run without manual intervention
4. Utilize free tools to keep costs minimal

This project demonstrates how to connect Spektrix's API with Google Sheets to create automated daily and weekly reports for ticket sales, capacity tracking, and revenue analysis.

This repository is entirely third-party and not supported by or affiliated with Spektrix or Google.

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

## Google Sheets Integration

The system uses Google Sheets API to:
- Clear and update existing data
- Append new rows
- Maintain historical data
- Enable automatic chart updates

## Security Notes

- API credentials are stored in environment variables
- Google service account credentials should be kept secure
- The `.gitignore` file excludes sensitive credentials

## Contributing

Feel free to fork this repository and adapt it to your needs. Pull requests are welcome for improvements or bug fixes. Hoping to add additional functionality in the future.

## License

This project is licensed under the MIT License - see the LICENSE file for details.