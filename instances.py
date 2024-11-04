import requests
from datetime import datetime, timedelta, timezone
import authorize
from inputs import performances, extra_locks

def get_instances(api_user, api_key, client_name, event_name=None, start_date=None, end_date=None):
    # Spektrix API base URL
    base_url = f"https://system.spektrix.com/{client_name}/api/v3"
    
    # Endpoint for retrieving orders
    endpoint = f"{base_url}/instances?startFrom={start_date}"

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

def get_instance_status(api_user, api_key, client_name, instance_id):
    # Spektrix API base URL
    base_url = f"https://system.spektrix.com/{client_name}/api/v3"
    
    # Endpoint for retrieving orders
    endpoint = f"{base_url}/instances/{instance_id}/status?includeLockInformation=true"

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

def filter_instances_by_event(instances, event_id):
    instance_dict = {}
    for instance in instances:
        if instance['event']['id'] == event_id:
            start_time = instance['start']
            instance_id = instance['id']
            instance_dict[start_time] = instance_id
    return instance_dict

def get_event_instances_statuses(api_user, api_key, client_name, event_id, start_date):
    # Get all instances from the start date
    instances = get_instances(api_user, api_key, client_name, start_date=start_date)
    
    if instances is None:
        return None

    # Filter instances by the given event_id
    filtered_instances = filter_instances_by_event(instances, event_id)

    # Get status for each filtered instance and format the output
    instance_statuses = {}
    for start_time, instance_id in filtered_instances.items():
        status = get_instance_status(api_user, api_key, client_name, instance_id)
        if status is not None:
            instance_statuses[start_time] = {
                'instance_id': instance_id,
                'sold': status['sold'],
                'locked': (status['locked'] - extra_locks),
                'available': status['available']
            }

    # Print the formatted output
    # for performance_time, data in instance_statuses.items():
    #     print(f"Performance Time: {performance_time}")
    #     print(f"Instance ID: {data['instance_id']}")
    #     print(f"Tickets Sold: {data['sold']}")
    #     print(f"Tickets Locked: {data['locked']}")
    #     print(f"Tickets Available: {data['available']}")
    #     print("---")

    return instance_statuses

def calculate_event_capacity_summary(instance_statuses):
    total_sold = 0
    total_locked = 0
    total_available = 0
    total_capacity = 0

    for data in instance_statuses.values():
        total_sold += data['sold']
        total_locked += data['locked']
        total_available += data['available']
    
    # total_locked = total_locked - (performances * extra_locks)
    total_capacity = total_sold + total_locked + total_available

    percent_sold_raw = (total_sold / total_capacity) * 100 if total_capacity > 0 else 0
    percent_locked_raw = (total_locked / total_capacity) * 100 if total_capacity > 0 else 0
    percent_available_raw = (total_available / total_capacity) * 100 if total_capacity > 0 else 0

    percent_sold = percent_sold_raw / 100
    percent_locked = percent_locked_raw / 100
    percent_available = percent_available_raw / 100

    summary = {
        'total_sold': total_sold,
        'total_locked': total_locked,
        'total_available': total_available,
        'percent_sold': round(percent_sold, 2),
        'percent_locked': round(percent_locked, 2),
        'percent_available': round(percent_available, 2)
    }

    print("Date\tCapacity Sold\tCapacity Locked\tCapacity Available\t% Capacity Sold\t% Capacity Locked\t% Capacity Available")
    print(f"{datetime.now().strftime('%m-%d-%Y')}\t{total_sold}\t{total_locked}\t{total_available}\t{percent_sold:.2f}%\t{percent_locked:.2f}%\t{percent_available:.2f}%")

    return summary



# Example usage
# api_user, api_key, client_name = get_api_credentials()
# event_id = "8201APNKPTCPSVLMMRDKJCTKBHRDCGHGR"
# start_date = "2024-10-22"
# result = get_event_instances_statuses(api_user, api_key, client_name, event_id, start_date)
# The formatted output is now printed within the function, so we don't need to repeat it here
