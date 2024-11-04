import os
import json
from pathlib import Path

def get_service_account_creds():
    """
    Get service account credentials either from environment variable or creds.json file.
    Returns dict with credentials.
    """
    # First try to get from environment variable
    service_account_json = os.getenv('SERVICE_ACCOUNT_JSON')
    if service_account_json:
        try:
            # First try normal JSON parsing
            return json.loads(service_account_json)
        except json.JSONDecodeError:
            try:
                # If that fails, try evaluating as Python literal
                import ast
                return ast.literal_eval(service_account_json)
            except (SyntaxError, ValueError) as e:
                print(f"Error parsing SERVICE_ACCOUNT_JSON environment variable: {e}")
    
    # If not in env var, try to load from creds.json
    creds_file = Path('creds.json')
    if creds_file.exists():
        try:
            with open(creds_file) as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            print(f"Error parsing creds.json file: {e}")
            raise
    
    raise FileNotFoundError("No valid service account credentials found. Ensure either SERVICE_ACCOUNT_JSON environment variable is set or creds.json file exists.")