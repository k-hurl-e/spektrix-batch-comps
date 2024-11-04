from datetime import datetime, timedelta
from orders import get_orders_by_confirmation_date, process_orders, calculate_total_tickets
from newrows import update_sheet_daily_tickets, update_sheet_booked_per_instance, update_sheet_capacity_summary, update_sheet_weekly_ticket_price
from credentials import get_api_credentials
from instances import get_event_instances_statuses, calculate_event_capacity_summary
from inputs import event_id, start_date

api_user, api_key, client_name = get_api_credentials()
confirmation_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
pretty_date = (datetime.now() - timedelta(days=1)).strftime("%m/%d/%Y")

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

if __name__ == "__main__":
    main()
