from datetime import datetime
import re, hmac, hashlib, base64


def get_unique_key(date, secret_key):
    nonce = date.isoformat(timespec='seconds') + '.000Z'
    return secret_key + nonce


def calculate_signature(date, secret_key, request_url, request_method, organization):
    unique_key = get_unique_key(date, secret_key).encode('UTF8')
    print(unique_key)
    converted_url = re.sub('^https?://[^/]+/', '/', request_url)
    params = [
        request_method,
        converted_url,
        'application/json',
        organization
    ]
    params_string = '\n'.join(params).encode('UTF8')
    hmac_sign = hmac.new(unique_key, params_string, hashlib.sha512).digest()
    encode_hmac = base64.b64encode(hmac_sign)
    return encode_hmac.decode()


def get_headers(url, method):
    bsp_organization = "4ab1d81f45334e438c0d937d28ea2770"
    bsp_shared_key = "ad54ad6e5e174cc8a73c869a8c9275cc"
    bsp_secret_key = "3e755fdcd27042b2aa72e10be25de354"
    current_dt = datetime.now()
    date = current_dt.strftime('%a, %d %b %Y %H:%M:%S GMT')
    bsp_access_key = f"AccessKey {bsp_shared_key}:{calculate_signature(current_dt, bsp_secret_key, url, method, bsp_organization)}"
    return {
        'Content-Type': 'application/json',
        'Authorization': bsp_access_key,
        'nep-organization': bsp_organization,
        'Date': date
    }
