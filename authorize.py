import base64
import hashlib
import hmac

def generate_signature(http_method, http_uri, http_date, secret_key, login_name):
    # Construct StringToSign
    string_to_sign = f"{http_method.upper()}\n{http_uri}\n{http_date}"
    
    # Ensure the secret key is base64-decoded
    decoded_secret_key = base64.b64decode(secret_key)
    
    # Generate the HMAC-SHA1 signature
    hmac_sha1 = hmac.new(decoded_secret_key, string_to_sign.encode('utf-8'), hashlib.sha1)
    signature = base64.b64encode(hmac_sha1.digest()).decode('utf-8')
    
    return signature

def generate_headers(http_method, endpoint, date, api_key, api_user):
    # Generate signature
    signature = generate_signature(http_method, endpoint, date, api_key, api_user)
        
    # Generate authorization header
    authorization_header = f"SpektrixAPI3 {api_user}:{signature}"
        
    # Headers for the request
    headers = {
            "Authorization": authorization_header,
            "Content-Type": "application/json",
            "Host": "system.spektrix.com",
            "Date": date
        }

    return headers