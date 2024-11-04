from datetime import datetime, timedelta
from orders import get_orders_by_confirmation_date, process_orders, calculate_total_tickets
from inputs import event_id
from credentials import get_api_credentials

api_user, api_key, client_name = get_api_credentials()
confirmation_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

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

def print_weekly_summary(weekly_data):
    print("\nWeekly Sales Summary")
    print("-------------------")
    total_tickets = 0
    total_orders = 0
    total_revenue = 0
    
    for date, data in weekly_data.items():
        print(f"Date: {date}")
        print(f"Tickets Sold: {data['tickets']}")
        print(f"Number of Orders: {data['orders']}")
        print(f"Revenue: ${data['revenue']:.2f}")
        print("-------------------")
        total_tickets += data['tickets']
        total_orders += data['orders']
        total_revenue += data['revenue']
    
    print("\nWeekly Totals")
    print(f"Total Tickets: {total_tickets}")
    print(f"Total Orders: {total_orders}")
    print(f"Total Revenue: ${total_revenue:.2f}")
    print(f"Average Tickets per Day: {total_tickets / 7:.2f}")
    print(f"Average Orders per Day: {total_orders / 7:.2f}")
    if total_tickets > 0:
        print(f"Average Ticket Price: ${total_revenue / total_tickets:.2f}")
    else:
        print("Average Ticket Price: $0.00")

def get_average_ticket_price(weekly_data):
    total_tickets = sum(data['tickets'] for data in weekly_data.values())
    total_revenue = sum(data['revenue'] for data in weekly_data.values())
    
    if total_tickets > 0:
        return round(total_revenue / total_tickets, 2)
    return 0.0
