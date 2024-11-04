import requests
from datetime import datetime, timedelta, timezone
import authorize

def get_orders_by_confirmation_date(api_user, api_key, client_name, confirmation_date):
    # Spektrix API base URL
    base_url = f"https://system.spektrix.com/{client_name}/api/v3"
    
    # Endpoint for retrieving orders
    endpoint = f"{base_url}/orders?confirmedOn={confirmation_date}"
    
    # Generate date for use in signature generation and header
    date = datetime.now(timezone.utc).strftime('%a, %d %b %Y %H:%M:%S GMT')
    
    # HTTP method
    http_method = 'GET'
    
    # Parameters for the API request
    params = {}

    # Generate headers
    headers = authorize.generate_headers(http_method, endpoint, date, api_key, api_user)
    
    # Make the API request
    response = requests.get(endpoint, headers=headers)
    
    # Check if the request was successful
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code} - {response.text}")
        print(headers)
        return None

def process_orders(orders, event_id):
    matching_orders = []
    for order in orders:
        # Check if any ticket in the order matches the event_id
        for ticket in order.get('tickets', []):
            if ticket['event']['id'] == event_id:
                total = float(order['total'])
                total_transaction_charges = float(order.get('totalTransactionCharges', 0))
                
                # Extract donation amount
                donations = order.get('donations', [])
                donation_amount = sum(float(donation.get('amount', 0)) for donation in donations)
                
                ticket_revenue = total - donation_amount
                price = float(ticket['price']) if float(ticket['price']) != 0 else 1
                num_tickets = round((ticket_revenue - total_transaction_charges) / price)
                matching_orders.append({
                    "Order ID": order['id'],
                    "Ticket Revenue": ticket_revenue,
                    "Donation": donation_amount,
                    "Number of Tickets": num_tickets,
                    "Ticket Price": ticket['price']
                })
                break
    
    return matching_orders if matching_orders else "No matching orders found"
    
    if not matching_orders_found:
        print("No matching orders found")

def calculate_total_tickets(processed_orders):
    if isinstance(processed_orders, list):
        total_tickets = sum(order['Number of Tickets'] for order in processed_orders if float(order['Ticket Revenue']) > 0)
        return total_tickets
    else:
        print(processed_orders)